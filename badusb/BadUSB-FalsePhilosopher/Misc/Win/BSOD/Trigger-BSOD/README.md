# Trigger-BSOD

**:warning: ONLY FOR COMPUTER SECURITY. DO NOT USE THIS REPO FOR ILLEGAL PURPOSES. :warning:**

## NtRaiseHardError & ZwRaiseHardError

Both functions are undocumented Windows APIs (NTAPI) included in `ntdll.dll`, can cause BlueScreen (BSOD, Blue Screen of Death) with certain parameters.

**Does not triger UAC (User Account Control)**. Works on Windows systems with Windows NT kernel, tested on Windows 7 and Windows 10. 

### NtRaiseHardError

```c++
NtRaiseHardError(
  IN  NTSTATUS                  ErrorStatus,
  IN  ULONG                     NumberOfParameters,
  IN  PUNICODE_STRING           UnicodeStringParameterMask OPTIONAL,
  IN  PVOID                     *Parameters,
  IN  HARDERROR_RESPONSE_OPTION ResponseOption,
  OUT PHARDERROR_RESPONSE       Response
);
```

### ZwRaiseHardError

```c++
ZwRaiseHardError(
  IN  NTSTATUS                  ErrorStatus,
  IN  ULONG                     NumberOfParameters,
  IN  PUNICODE_STRING           UnicodeStringParameterMask OPTIONAL,
  IN  PVOID                     *Parameters,
  IN  HARDERROR_RESPONSE_OPTION ResponseOption,
  OUT PHARDERROR_RESPONSE       Response
);
```

### Parameters

#### PUNICODE_STRING

```c++
#include <SubAuth.h>
```

```c++
typedef struct _UNICODE_STRING {
	USHORT Length;
	USHORT MaximumLength;
	PWSTR Buffer;
} UNICODE_STRING, *PUNICODE_STRING;
```

#### HARDERROR_RESPONSE_OPTION

```c++
typedef enum _HARDERROR_RESPONSE_OPTION {
	OptionAbortRetryIgnore,
	OptionOk,
	OptionOkCancel,
	OptionRetryCancel,
	OptionYesNo,
	OptionYesNoCancel,
	OptionShutdownSystem
} HARDERROR_RESPONSE_OPTION, *PHARDERROR_RESPONSE_OPTION;
```

#### PHARDERROR_RESPONSE

```c++
typedef enum _HARDERROR_RESPONSE {
	ResponseReturnToCaller,
	ResponseNotHandled,
	ResponseAbort,
	ResponseCancel,
	ResponseIgnore,
	ResponseNo,
	ResponseOk,
	ResponseRetry,
	ResponseYes
} HARDERROR_RESPONSE, *PHARDERROR_RESPONSE;
```

## Build

With `MinGW64` (from MSYS2), `CMake 3.22`, `C++11`.

## VirusTotal
| ![NtRaiseHardError](https://user-images.githubusercontent.com/12462465/170830231-0f0ff19e-c732-4d06-873c-ada1c46800aa.png) | ![ZwRaiseHardError](https://user-images.githubusercontent.com/12462465/170830234-c041acaa-2b98-490a-a421-586c444a8907.png) |
| ---- | ---- |


