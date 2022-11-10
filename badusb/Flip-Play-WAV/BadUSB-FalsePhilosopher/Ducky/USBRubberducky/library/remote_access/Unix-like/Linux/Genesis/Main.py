#!/usr/bin/python3
# Author 0x5a

import os
import random
import time
import sys

if os.geteuid() != 0:
    print("\033[31m[!]\033[0m\033[1mMust be run as Root!\033[21m")
    sys.exit()


os.system('find Plugins/*.py -maxdepth 1 -type f | xargs -iZ basename Z | cut -d"." -f1 > Storage/plugins')
plugs = open("Storage/plugins","r")
z = plugs.readlines()

plugins = []
for p in z:
    plugins.append(p.replace("\n",""))

loaded = len(plugins)
#Vars to be displayed
mac = os.popen("/sbin/ifconfig wlan0 | awk '/ether/{print $2}'").read()
public_ip = os.popen("wget http://ipinfo.io/ip -qO -").read()
Local_ip = os.popen("/sbin/ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read()
gw = os.popen("/sbin/ip route | awk '/default/ { printf $3 }'").read()
#data = """ \t Public IP: %s \n\t Local IP: %s \n\t MAC: %s""" % (public_ip,Local_ip,mac)
first = "\tPublic IP: %s " % public_ip
second ="\tLocal IP:  %s " % Local_ip
third = "\tMAC Addr:  %s " % mac
fourth ="\tGate Way:  %s " % gw

def banner():
    os.system("clear")
    os.system("figlet Genesis")
    print("\tExploit Framework made by 0x5a\n")
    print("\tFocuses On Practical Exploitation\n")
    print("\tPlugins Loaded: %d" % loaded)


def drama():
    os.system("clear")
    banner()
    print("\t"+'='*36, "\t\n")
    time.sleep(2)
    print(second)
    time.sleep(1)
    print(third)
    time.sleep(1.5)
    print(fourth)
    print("\t"+'='*36, "\t")
    print("\n")

def help():
    print("\t \033[93mCommands \t \033[92mInfo \033[0m\n")
    print("\t"+'='*36, "\t\n")
    print("\t\033[93m! \t        \033[92mRun shell commands\033[0m \n")
    print("\t\033[93mPlugins\t        \033[92mShow Plugins \033[0m \n")
    print("\t\033[93m[plugin_name]\t\033[92mRun Plugin\033[0m \n")
def commands():
    for x in range(0,loaded):
        filename = plugins[x]
        info_file=open("Plugins/"+filename+".info","r")
        print("\t\033[91m"+filename+ "\t|\t\033[33m " + info_file.read()+ "\033[0m")


drama()
while 1:
    try:
        z = str(input("\033[1;39m Genesis \033[1;5m> \033[1;25m  "))
        command = z.lower()
        if command:
            if command == "exit"or command == "quit":
                os.system("clear")
                sys.exit()
            elif command == "help"or command=="h" or command=="?":
                help()
                pass
            elif command == "clear":
                os.system("clear")
            elif command == "banner":
                banner()
            elif command == "plugins" or command == "plugin":
                commands()
            elif command in plugins:
                try:
                    os.system("python3 Plugins/"+command+".py")
                except:
                    print("Error: No such plugin")
                    help()
            elif command[0]== "!":
                print(os.popen(command[1:len(command)]).read())
            else:
                time.sleep(.2)
                print("\033[31m No such command \033[0m")
    except KeyboardInterrupt:
        os.system("clear")
        sys.exit()
