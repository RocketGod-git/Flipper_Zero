/*******************************************************************************
*
*  (C) COPYRIGHT AUTHORS, 2017 - 2021
*
*  TITLE:       AIC.C
*
*  VERSION:     3.56
*
*  DATE:        30 July 2021
*
* THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF
* ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED
* TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
* PARTICULAR PURPOSE.
*
*******************************************************************************/
#include "consts.h"
#ifdef _WIN64
#include "appinfo/x64/appinfo64.h"
#else
#include "appinfo/x86-32/appinfo32.h"
#endif
/*
* AicpAsyncInitializeHandle
*
* Purpose:
*
* Init RPC_ASYNC_STATE structure.
*
*/
RPC_STATUS AicpAsyncInitializeHandle(
    _Inout_ RPC_ASYNC_STATE* AsyncState)
{
    RPC_STATUS status;

    status = RpcAsyncInitializeHandle(AsyncState, sizeof(RPC_ASYNC_STATE));
    if (status == RPC_S_OK) {
        AsyncState->NotificationType = RpcNotificationTypeEvent;
        AsyncState->u.hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
        if (AsyncState->u.hEvent == NULL)
            status = GetLastError();
    }

    return status;
}

/*
* AicpAsyncCloseHandle
*
* Purpose:
*
* Close RPC_ASYNC_STATE notification event.
*
*/
VOID AicpAsyncCloseHandle(
    _Inout_ RPC_ASYNC_STATE* AsyncState)
{
    if (AsyncState->u.hEvent) {
        CloseHandle(AsyncState->u.hEvent);
        AsyncState->u.hEvent = NULL;
    }
}



/*
* supCreateBindingHandle
*
* Purpose:
*
* Bind handle to the RPC interface.
*
*/
RPC_STATUS supCreateBindingHandle(
    _In_ RPC_WSTR RpcInterfaceUuid,
    _Out_ RPC_BINDING_HANDLE* BindingHandle
)
{
    RPC_STATUS status = RPC_S_INTERNAL_ERROR;
    RPC_SECURITY_QOS_V3 sqos;
    RPC_WSTR StringBinding = NULL;
    RPC_BINDING_HANDLE Binding = NULL;
    PSID LocalSystemSid = NULL;
    DWORD cbSid = SECURITY_MAX_SID_SIZE;


    if (BindingHandle)
        *BindingHandle = NULL;

    RtlSecureZeroMemory(&sqos, sizeof(sqos));

    status = RpcStringBindingComposeW(RpcInterfaceUuid,
        (RPC_WSTR)(L"ncalrpc"),
        NULL,
        NULL,
        NULL,
        &StringBinding);

    if (status == RPC_S_OK) {

        status = RpcBindingFromStringBindingW(StringBinding, &Binding);
        RpcStringFreeW(&StringBinding);

        if (status == RPC_S_OK) {

            LocalSystemSid = LocalAlloc(LPTR, cbSid);
            if (LocalSystemSid) {
                if (CreateWellKnownSid(WinLocalSystemSid, NULL, LocalSystemSid, &cbSid)) {

                    sqos.Version = 3;
                    sqos.ImpersonationType = RPC_C_IMP_LEVEL_IMPERSONATE;
                    sqos.Capabilities = RPC_C_QOS_CAPABILITIES_MUTUAL_AUTH;
                    sqos.IdentityTracking = 0;
                    sqos.Sid = LocalSystemSid;

                    status = RpcBindingSetAuthInfoExW(Binding,
                        NULL,
                        RPC_C_AUTHN_LEVEL_PKT_PRIVACY,
                        RPC_C_AUTHN_WINNT,
                        0,
                        0,
                        (RPC_SECURITY_QOS*)&sqos);

                    if (status == RPC_S_OK) {
                        *BindingHandle = Binding;
                        Binding = NULL;
                    }

                }
                else {
                    status = GetLastError();
                }
                LocalFree(LocalSystemSid);
            }
            else {
                status = ERROR_NOT_ENOUGH_MEMORY;
            }
        }
    }

    if (Binding)
        RpcBindingFree(&Binding);

    return status;
}
/*
* AicLaunchAdminProcess
*
* Purpose:
*
* Create process by talking to APPINFO via RPC.
*
*/
BOOLEAN AicLaunchAdminProcess(
    _In_opt_ LPWSTR ExecutablePath,
    _In_opt_ LPWSTR CommandLine,
    _In_ DWORD StartFlags,
    _In_ DWORD CreationFlags,
    _In_ LPWSTR CurrentDirectory,
    _In_ LPWSTR WindowStation,
    _In_opt_ HWND hWnd,
    _In_ DWORD Timeout,
    _In_ DWORD ShowFlags,
    _Out_ PROCESS_INFORMATION* ProcessInformation
)
{
    BOOLEAN bResult = FALSE;
    RPC_BINDING_HANDLE rpcHandle;
    RPC_ASYNC_STATE asyncState;
    APP_PROCESS_INFORMATION procInfo;
    APP_STARTUP_INFO appStartup;
    RPC_STATUS status;
    VOID* Reply = NULL;

    LONG elevationType = 0;

    if (ProcessInformation) {
        ProcessInformation->hProcess = NULL;
        ProcessInformation->hThread = NULL;
        ProcessInformation->dwProcessId = 0;
        ProcessInformation->dwThreadId = 0;
    }

    RtlSecureZeroMemory(&procInfo, sizeof(procInfo));
    RtlSecureZeroMemory(&appStartup, sizeof(appStartup));

    appStartup.dwFlags = STARTF_USESHOWWINDOW;
    appStartup.wShowWindow = (SHORT)ShowFlags;

    RtlSecureZeroMemory(&asyncState, sizeof(RPC_ASYNC_STATE));

    if ((supCreateBindingHandle((RPC_WSTR)APPINFO_RPC, &rpcHandle) == RPC_S_OK) &&
        (AicpAsyncInitializeHandle(&asyncState) == RPC_S_OK))
    {

        __try {

            RAiLaunchAdminProcess(&asyncState,
                rpcHandle,
                ExecutablePath,
                CommandLine,
                StartFlags,
                CreationFlags,
                CurrentDirectory,
                WindowStation,
                &appStartup,
                (ULONG_PTR)hWnd,
                Timeout,
                &procInfo,
                &elevationType);

            if (WaitForSingleObject(asyncState.u.hEvent, INFINITE) == WAIT_FAILED)
            {
                RpcRaiseException(-1);
            }

            status = RpcAsyncCompleteCall(&asyncState, &Reply);
            if (status == 0 && Reply == NULL) {

                if (ProcessInformation) {
                    ProcessInformation->hProcess = (HANDLE)procInfo.ProcessHandle;
                    ProcessInformation->hThread = (HANDLE)procInfo.ThreadHandle;
                    ProcessInformation->dwProcessId = (DWORD)procInfo.ProcessId;
                    ProcessInformation->dwThreadId = (DWORD)procInfo.ThreadId;
                }

                bResult = TRUE;

            }

            AicpAsyncCloseHandle(&asyncState);

        }
        __except (EXCEPTION_EXECUTE_HANDLER) {
            SetLastError(RpcExceptionCode());
            return FALSE;
        }

        RpcBindingFree(&rpcHandle);
    }

    return bResult;
}
