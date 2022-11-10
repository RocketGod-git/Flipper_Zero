#include <iostream>
#include <Windows.h>


int main(){
  
	PIMAGE_IMPORT_BY_NAME func=NULL;
	LPCSTR func_name = NULL;
	LPCSTR lib_name = NULL;
	LPVOID baseModule = GetModuleHandle(NULL);
	PIMAGE_DOS_HEADER dos_header = (PIMAGE_DOS_HEADER)baseModule;
	PIMAGE_NT_HEADERS nt_header = (PIMAGE_NT_HEADERS)((DWORD_PTR)(baseModule)+dos_header->el_fanew);
	IMAGE_DATA_DIRECTORY data_directory = (IMAGE_DATA_DIRECTORY)(nt_header->OptionnalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]);
	PIMAGE_IMPORT_DESCRIPTOR import_descriptor = (PIMAGE_IMPORT_DESCRIPTOR)((DWORD_PTR)baseModule+data_directory.VirtualAddress);
	
	
	while(import_descriptor->Name != NULL){
		
		lib_name = (LPCSTR)import_descriptor->Name+(DWORD_PTR)baseModule;
		HMODULE current_mod = LoadLibraryA(lib_name);
		
		if(current_mod != INVALID_HANDLE_VALUE){
			
			std::cout<<"parsing functions for library : "<<lib_name<<"\n";
			
			PIMAGE_THUNK_DATA originalFirstThunk = NULL, firstThunk = NULL;
			originalFirstThunk = (PIMAGE_THUNK_DATA)((DWORD_PTR)baseModule + import_descriptor->OriginalFirstThunk);
			firstThunk = (PIMAGE_THUNK_DATA)((DWORD_PTR)baseModule+ import_descriptor->FirstThunk);
			
			while(originalFirstThunk->u1.AddressOfData != NULL){
				
				func = (PIMAGE_IMPORT_BY_NAME)((DWORD_PTR)baseModule + originalFirstThunk->u1.AddressOfData);
				func_name = (LPCSTR)func->Name;
				
				std::cout<<"Function : "<<func->Name<<"\n";
			}
			
			
		}
	}
	return 0;
  
}
