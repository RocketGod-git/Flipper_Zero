```
DELAY 2000
GUI r
DELAY 150
STRING CMD /ADMINISTRATOR 
DELAY 150
ENTER
DELAY 150
STRING CD c:\
DELAY 150
ENTER
STRING MD Audit
DELAY 150
ENTER
DELAY 150
STRING CD c:\Audit
DELAY 150
ENTER
DELAY 150
STRING MD Audit-%date:/=_%"
DELAY 70
ENTER
DELAY 1000
REM This variable is used so that robocopy can create a date stamped folder to help 
REM Id the folder 
STRING set DST=Audit-%date:/=_%
DELAY 1000
ENTER
DELAY 1000
STRING systeminfo.exe>C:\Audit\Audit-%date:/=_%"\systemSpecs.txt
ENTER
DELAY 250
STRING Exit
ENTER
GUI r 
DELAY 100
STRING POWERSHELL
DELAY 20
ENTER
DELAY 1000
STRING Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, Size, InstallDate | Format-Table -AutoSize > C:\Audit\InstallList.txt
ENTER
DELAY 1000
STRING EXIT
DELAY 20 
ENTER
DELAY 320
GUI r
DELAY 100
STRING CMD
ENTER 
DELAY 150 
STRING ROBOCOPY "c:\Audit" "\\PC NETWORK PATH\Audits" /s /e /r:0 /w:0 /np
ENTER
DELAY 100
STRING ROBOCOPY "c:\Audit\Audit-%date:/=_%"" "\Audits" /s /e /r:0 /w:0 /np 
ENTER
DELAY 100
STRING EXIT
ENTER
REM Made by Phantom Santa 
```

