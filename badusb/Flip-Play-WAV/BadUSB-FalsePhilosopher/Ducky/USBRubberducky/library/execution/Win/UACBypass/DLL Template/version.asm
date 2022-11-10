ifndef _M_X64
    .model flat
else
    include ksamd64.inc
endif

ifndef _M_X64
    prx_find_function proto stdcall, arg1:word, arg2:dword
else
    extern prx_find_function:proc
endif

PRX_EXPORT32 macro langtype:req, procname:req, ordinal:req
    .erre ordinal

    ifndef _M_X64
        .data
        procname&_ptr dd 0

        .code
        procname proc langtype
            mov eax, procname&_ptr
            test eax, eax
            jnz skip_find
                invoke prx_find_function, ordinal, offset procname&_ptr

        skip_find:
            jmp eax
        procname endp
    endif
endm

PRX_EXPORT64 macro procname:req, ordinal:req
    .erre ordinal

    ifdef _M_X64
        .data
        procname&_ptr dq 0

        .code
        procname proc frame
            save_reg r9, 20h
            save_reg r8, 18h
            save_reg rdx, 10h
            save_reg rcx, 8
            alloc_stack 28h
            END_PROLOGUE
            
            mov rax, procname&_ptr
            test rax, rax
            jnz skip_find
                mov rcx, ordinal
                mov rdx, offset procname&_ptr
                call prx_find_function

        skip_find:
            add rsp, 28h
            mov rcx, [rsp + 8]
            mov rdx, [rsp + 10h]
            mov r8, [rsp + 18h]
            mov r9, [rsp + 20h]
            
            BEGIN_EPILOGUE
            rex_jmp_reg rax
        procname endp
    endif
endm

PRX_EXPORT macro langtype:req, procname:req, ordinal1:req, ordinal2
    PRX_EXPORT32 langtype, procname, ordinal1
    
    ifb <ordinal2>
        PRX_EXPORT64 procname, ordinal1
    else
        PRX_EXPORT64 procname, ordinal2
    endif
endm

PRX_EXPORT stdcall, GetFileVersionInfoA, 1
PRX_EXPORT stdcall, GetFileVersionInfoByHandle, 2
PRX_EXPORT stdcall, GetFileVersionInfoExW, 3
PRX_EXPORT stdcall, GetFileVersionInfoSizeA, 4
PRX_EXPORT stdcall, GetFileVersionInfoSizeExW, 5
PRX_EXPORT stdcall, GetFileVersionInfoSizeW, 6
PRX_EXPORT stdcall, GetFileVersionInfoW, 7
PRX_EXPORT stdcall, VerFindFileA, 8
PRX_EXPORT stdcall, VerFindFileW, 9
PRX_EXPORT stdcall, VerInstallFileA, 10
PRX_EXPORT stdcall, VerInstallFileW, 11
PRX_EXPORT stdcall, VerLanguageNameA, 12
PRX_EXPORT stdcall, VerLanguageNameW, 13
PRX_EXPORT stdcall, VerQueryValueA, 14
PRX_EXPORT stdcall, VerQueryValueW, 15

end
