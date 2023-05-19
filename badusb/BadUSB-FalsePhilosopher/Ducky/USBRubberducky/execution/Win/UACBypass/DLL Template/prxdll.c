#include "pch.h"
#include "prxdll.h"

static PIMAGE_DOS_HEADER g_pImageBase;
static PIMAGE_EXPORT_DIRECTORY g_pExportDirectory;
static HMODULE g_hModule;

PVOID __stdcall prx_find_function(WORD ordinal, PVOID *fn)
{
    HMODULE hModule;
    DWORD Index;
    LPCSTR ModuleName;
    TCHAR Path[MAX_PATH];
    DWORD Count;
    PVOID temp;
    PVOID Result;
    DWORD *Names;
    WORD *NameOrdinals;
    LPCSTR ProcName;

    if ( !ordinal )
        return NULL;

    Index = ordinal - g_pExportDirectory->Base;
    if ( Index >= g_pExportDirectory->NumberOfFunctions )
        return NULL;

    if ( !(hModule = InterlockedCompareExchangePointer(&(PVOID)g_hModule, NULL, NULL)) ) {
        ModuleName = OffsetToPointer(g_pImageBase, g_pExportDirectory->Name);

        if ( !(Count = GetSystemDirectory(Path, _countof(Path)))
            || FAILED(StringCchPrintf(Path + Count, _countof(Path) - Count, _T("\\%hs"), ModuleName)) )
            return NULL;

        if ( !(hModule = LoadLibraryEx(Path, NULL, LOAD_WITH_ALTERED_SEARCH_PATH)) )
            return NULL;

        if ( temp = InterlockedCompareExchangePointer(&(PVOID)g_hModule, hModule, NULL) ) {
            FreeLibrary(hModule);
            hModule = temp;
        }
    }

    if ( !(Result = InterlockedCompareExchangePointer(fn, NULL, NULL)) ) {
        NameOrdinals = OffsetToPointer(g_pImageBase,
            g_pExportDirectory->AddressOfNameOrdinals);
        Names = OffsetToPointer(g_pImageBase,
            g_pExportDirectory->AddressOfNames);
        ProcName = MAKEINTRESOURCEA(ordinal);

        for ( DWORD i = 0; i < g_pExportDirectory->NumberOfNames; ++i ) {
            if ( Index != NameOrdinals[i] )
                continue;

            ProcName = OffsetToPointer(g_pImageBase, Names[i]);
            break;
        }
        if ( (Result = GetProcAddress(hModule, ProcName))
            && (temp = InterlockedCompareExchangePointer(fn, Result, NULL)) )
            Result = temp;
    }
    return Result;
}

// call this exactly once in the DllMain DLL_PROCESS_ATTACH handler
BOOLEAN __stdcall prx_attach(HINSTANCE instance)
{
    PIMAGE_NT_HEADERS pNtHeader;

    g_pImageBase = (PIMAGE_DOS_HEADER)instance;
    if ( g_pImageBase->e_magic != IMAGE_DOS_SIGNATURE )
        return FALSE;

    pNtHeader = OffsetToPointer(g_pImageBase, g_pImageBase->e_lfanew);
    if ( pNtHeader->Signature != IMAGE_NT_SIGNATURE
        || pNtHeader->OptionalHeader.Magic != IMAGE_NT_OPTIONAL_HDR_MAGIC )
        return FALSE;

    g_pExportDirectory = OffsetToPointer(g_pImageBase,
        pNtHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);

    return TRUE;
}

// call this exactly once in the DllMain DLL_PROCESS_DETACH handler
void __stdcall prx_detach(PVOID reserved)
{
    if ( !reserved )
        FreeLibrary(g_hModule);
}
