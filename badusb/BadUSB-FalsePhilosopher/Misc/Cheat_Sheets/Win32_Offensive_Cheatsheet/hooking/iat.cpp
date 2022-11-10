#include <iostream>
#include <string>


typedef DWORD (WINAPI* HookedMessageBox)(HWND,LPCSTR,LPCSTR,UINT);
HookedMessageBox original = MessageBoxA;

int HookedMessageBox(HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType){
	
	MessageBoxW(NULL, L"hacked", L":)", 0);
	return original(hWnd, lpText, lpCaption, uType);		
}


int main(){
	
	
	MessageBoxA(NULL, "Hello Before Hooking", "Hello Before Hooking", 0);
	
	
	LPVOID baseAddress = GetModuleHandleA(NULL);
	PIMAGE_DOS_HEADER  dos_header = (PIMAGE_DOS_HEADER)(DWORD_PTR)baseAddress;
	
	PIMAGE_NT_HEADERS nt_header = (PIMAGE_NT_HEADERS)((DWORD_PTR)baseAddress+dos_header->el_fanew);
	
	IMAGE_DATA_DIRECTORY data_directory = (IMAGE_DATA_DIRECTORY)((DWORD_PTR)nt_header->OptionnalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]);
	IMAGE_IMPORT_DESCRIPTOR import_desc = (IMAGE_IMPORT_DESCRIPTOR)((DWORD_PTR)baseAddress+data_directory.VirtualAddress);
	
	
	while(import_desc->Name != NULL){
		
		LPCSTR lib_name = (LPCSTR)(import_desc->Name+(DWORD_PTR)baseAddress);
		if(LoadLibraryA(lib_name) != NULL){
			
			PIMAGE_THUNK_DATA originalFirstThunk = (PIMAGE_THUNK_DATA)(import_desc->originalFirstThunk+(DWORD_PTR)baseAddress);
			PIMAGE_THUNK_DATA firstThunk = (PIMAGE_THUNK_DATA)(import_desc->FirstThunk+(DWORD_PTR)baseAddress);
			
			while(originalFirstThunk->u1.AddressOfData != NULL){
				
				PIMAGE_IMPORT_BY_NAME import_name = (PIMAGE_IMPORT_BY_NAME)originalFirstThunk.AddressOfData;
				LPCSTR func_name = (LPCSTR)import_name->Name;
				
				
				if(!(strcmp(func_name, "MessageBoxA")){
					
					//patch
					DWORD oldprotect=0;
					VirtualProtect((LPVOID)originalFirstThunk->u1.Function,8,PAGE_READWRITE,&oldprotect); //modify only 8 bytes
					
					originalFirstThunk->u1.Function = (DWORD_PTR)HookedMessageBox;
					
					//VirtualProtect((LPVOID)originalFirstThunk->u1.Function,8,oldprotect,&oldprotect); optionnal
					
				}
				++originalFirstThunk;
				++firstThunk;
			}
		}
		
		import_desc++;
		
	}
	
	MessageBoxA(NULL, "after Hooking", "after Hooking", 0);
	return 0;
}
