@echo off
timeout /T 1 /nobreak >nul
FOR /F "USEBACKQ TOKENS=2,*" %%a IN (
	`REG QUERY "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /V {374DE290-123F-4565-9164-39C4925E467B}`
) DO (
	SET DOWNLOADS=%%b
)
if not exist %DOWNLOADS%\platform-tools\ echo Please download the windows Platform Tools first! The Website will be automatically opened
if not exist %DOWNLOADS%\platform-tools\ timeout /T 2 /nobreak >nul
if not exist %DOWNLOADS%\platform-tools\ echo otherwise it wont work...
if not exist %DOWNLOADS%\platform-tools\ start https://developer.android.com/studio/releases/platform-tools
if not exist %DOWNLOADS%\adb-virus-windows\ rename adb-virus-windows-master\ adb-virus-windows\
if not exist %DOWNLOADS%\platform-tools\ start cmd /C monkeyadb-download.bat
if not exist %DOWNLOADS%\platform-tools\ echo Please press enter!
if not exist %DOWNLOADS%\platform-tools\ pause
if not exist %DOWNLOADS%\platform-tools\ echo Ready?
echo Hey
timeout /T 2 /nobreak >nul
echo Your device is being connected
timeout /T 1 /nobreak >nul
echo .
timeout /T 1 /nobreak >nul
echo ..
timeout /T 1 /nobreak >nul
echo ...
timeout /T 2 /nobreak >nul
%DOWNLOADS%\platform-tools\adb.exe devices
%DOWNLOADS%\platform-tools\
timeout /T 2 /nobreak >nul
echo Device connected
timeout /T 2 /nobreak >nul
echo Testing connection
timeout /T 2 /nobreak >nul
adb shell uname -a
timeout /T 2 /nobreak >nul
echo Connection succesfull
timeout /T 3 /nobreak >nul
echo Deleting data
timeout /T 2 /nobreak >nul
%DOWNLOADS%\platform-tools\adb shell dumpsys battery unplug
%DOWNLOADS%\platform-tools\adb shell dumpsys battery set level 3
timeout /T 2 /nobreak >nul
echo Deleted files succesfully
timeout /T 1 /nobreak >nul
echo Destroying System
timeout /T 3 /nobreak >nul
echo System destroyed
timeout /T 2 /nobreak >nul
%DOWNLOADS%\platform-tools\adb shell reboot
timeout /T 3 /nobreak >nul
echo Retesting Connection
timeout /T 60 /nobreak >nul
%DOWNLOADS%\platform-tools\adb devices
timeout /T 2 /nobreak >nul
%DOWNLOADS%\platform-tools\adb shell uname -a
timeout /T 2 /nobreak >nul
echo Actually nevermind
timeout /T 2 /nobreak >nul
echo You've been pranked!
start https://youtu.be/O91DT1pR1ew
pause
del output.txt