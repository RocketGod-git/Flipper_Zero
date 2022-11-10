#include <iostream>
#include <Windows.h>


int main(){
	
	wchar_t dllPath[] = TEXT("C:\\test.dll");
	LPVOID buffer=NULL;
	LPVOID addr = VirtualAlloc(NULL,sizeof path,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);
	WriteProcessMemory(GetCurrentProcess(), buffer, (LPVOID)path, sizeof path, NULL);
	PTHREAD_START_ROUTINE threatStartRoutineAddress = (PTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandle(TEXT("Kernel32")), "LoadLibraryW");

	CreateRemoteThread(GetCurrentProcess(), NULL, 0, threatStartRoutineAddress, buffer, 0, NULL);
  
	return 0;
}
