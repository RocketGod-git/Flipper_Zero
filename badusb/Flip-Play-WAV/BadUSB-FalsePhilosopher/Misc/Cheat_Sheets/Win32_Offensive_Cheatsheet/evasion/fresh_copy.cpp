#include <Windows.h>
#include <psapi.h>

int main(){
    MODULEINFO mInfo = { 0 };
    HANDLE hProcess = GetCurrentProcess();
 
    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    GetModuleInformation(hProcess, hNtdll, &mInfo, sizeof(mInfo));
    LPVOID lpNtdllbase = (LPVOID)mInfo.lpBaseOfDll;
    
    HANDLE hNtdllfile = CreateFileA("c:\\windows\\system32\\ntdll.dll", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    HANDLE hNtdllMapping = CreateFileMapping(hNtdllfile, NULL, PAGE_READONLY | SEC_IMAGE, 0, 0, NULL);
    LPVOID lpNtdllmaping = MapViewOfFile(hNtdllMapping, FILE_MAP_READ, 0, 0, 0);

    PIMAGE_DOS_HEADER pDosheader = (PIMAGE_DOS_HEADER)lpNtdllbase;
    PIMAGE_NT_HEADERS pNtheader = (PIMAGE_NT_HEADERS)((DWORD_PTR)lpNtdllbase + pDosheader->e_lfanew);

    for (int i = 0; i < pNtheader->FileHeader.NumberOfSections; i++) {
        PIMAGE_SECTION_HEADER pSectionheader = (PIMAGE_SECTION_HEADER)((DWORD_PTR)IMAGE_FIRST_SECTION(pNtheader) + ((DWORD_PTR)IMAGE_SIZEOF_SECTION_HEADER * i));

        if (!strcmp((char*)pSectionheader->Name, (char*)".text")) {
            DWORD oldProtection = 0;
            bool isProtected = VirtualProtect((LPVOID)((DWORD_PTR)lpNtdllbase + (DWORD_PTR)pSectionheader->VirtualAddress), pSectionheader->Misc.VirtualSize, PAGE_EXECUTE_READWRITE, &oldProtection);
            memcpy((LPVOID)((DWORD_PTR)lpNtdllbase + (DWORD_PTR)pSectionheader->VirtualAddress), (LPVOID)((DWORD_PTR)lpNtdllmaping + (DWORD_PTR)pSectionheader->VirtualAddress), pSectionheader->Misc.VirtualSize);
            isProtected = VirtualProtect((LPVOID)((DWORD_PTR)lpNtdllbase + (DWORD_PTR)pSectionheader->VirtualAddress), pSectionheader->Misc.VirtualSize, oldProtection, NULL);
        }
    }

    CloseHandle(hProcess);
    CloseHandle(hNtdllfile);
    CloseHandle(lpNtdllmaping);
    FreeLibrary(hNtdll);

    return 0;
}
