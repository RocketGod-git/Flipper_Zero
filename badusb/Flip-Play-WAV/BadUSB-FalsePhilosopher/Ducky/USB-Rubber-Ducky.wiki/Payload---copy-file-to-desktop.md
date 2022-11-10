The following is something I have been working on based on the payload "Runexe from SD". This payload will work on the twin duck firmwares by executing a script that waits for the ducky to mount the removable storage. The payload also uses some of the member googleknowsbest's code. The for loop which polls for the ducky is the code to which I am referring to. This payload is not hacking related per say, but it could be useful to those who miss autorun files, and sneaker nets.

```
REM Author: overwraith
REM Name: CopyFileToDesktop.txt
REM Purpose: Wait for ducky mass storage to mount, then copy file to desktop. 
REM Encoder V2.4
REM Using the run command for a broader OS base. 
DEFAULT_DELAY 75
DELAY 3000
GUI r
DELAY 1000
STRING cmd /Q /D /T:7F /F:OFF /V:ON /K
DELAY 500
ENTER
DELAY 750
ALT SPACE
STRING M
DOWNARROW
REPEAT 100
ENTER

REM Change directories because System32 appears to be protected. 
STRING CD %TEMP%
ENTER

REM Make batch file that waits for SD card to mount. 
REM Delete batch file if already exists
STRING erase /Q DuckyWait.bat
ENTER
STRING copy con DuckyWait.bat
ENTER
REM DuckyWait.bat
STRING :while1
ENTER
STRING for /f "tokens=3 delims= " %%A in ('echo list volume ^| diskpart ^| findstr "DUCKY"') do (set DUCKYdrive=%%A:)
ENTER
STRING if Exist %DUCKYdrive% (
ENTER
STRING goto :break
ENTER
STRING )
ENTER
STRING timeout /t 30
ENTER
STRING goto :while1
ENTER
STRING :break
ENTER
REM Continue script.
REM Remove the next two lines if you don't place your payloads in separate folders. 
STRING set DUCKYdrive=%DUCKYdrive%\CopyFileToDesktop\
ENTER
STRING copy %DUCKYdrive%HelloWorld.exe %userprofile%\Desktop\HelloWorld.exe
ENTER
CONTROL z
ENTER

REM MAKE THE VBS FILE THAT ALLOWS RUNNING INVISIBLY.
REM Delete vbs file if already exists
STRING erase /Q invis.vbs
ENTER
REM FROM: http://stackoverflow.com/questions/289498/running-batch-file-in-background-when-windows-boots-up
STRING copy con invis.vbs
ENTER
STRING CreateObject("Wscript.Shell").Run """" & WScript.Arguments(0) & """", 0, False
ENTER
CONTROL z
ENTER

REM RUN THE BATCH FILE
STRING wscript.exe invis.vbs DuckyWait.bat
ENTER
STRING EXIT
ENTER
```

There is a group of lines you may wish to remove if you are operating from the root of the ducky, I have the script running out of a folder on the ducky, not the root.

```
REM Remove the next two lines if you don't place your payloads in separate folders. 
STRING set DUCKYdrive=%DUCKYdrive%\CopyFileToDesktop\
ENTER
```
The script copies HelloWorld.exe out of the folder "CopyFileToDesktop".