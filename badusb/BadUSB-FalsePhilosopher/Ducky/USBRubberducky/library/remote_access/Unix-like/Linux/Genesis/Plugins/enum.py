import os
import sys




def inputplease():
    ip = str(input("IP Adress to scan[10.10.10.40]: ")) or "10.10.10.10"
    main(ip)

def main(ip_addr):
    command = "nmap -sC -sV -oA Storage/nmap-"+ip_addr+" "+ ip_addr
    print("\033[1;32m[!]\033[0m \033[1m Starting Nmap scan!\033[21m")
    os.system("dirbuster &")
    try:
        os.system(command)
    except Exception as e:
        print(e)

help1 =  """ \t Basic Enumeration That I like to start a CTF with!\n
\t Type Execute to begin!"""
def hello():
    try:
        print(help1)
        while 1:
            select = str(input("\033[34m(Enum)\033[0m>"))
            z = select.lower()
            if z =="execute":
                inputplease()
            elif z == "help" or z == "h":
                print(help1)
                pass
            elif z =="exit" or z == "quit":
                sys.exit()
            else:
                pass
    except KeyboardInterrupt:
        sys.exit()
hello()
