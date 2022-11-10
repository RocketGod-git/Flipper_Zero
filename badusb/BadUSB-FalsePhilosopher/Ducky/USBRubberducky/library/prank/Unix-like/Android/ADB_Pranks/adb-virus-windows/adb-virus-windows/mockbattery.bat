@echo off
FOR /F "USEBACKQ TOKENS=2,*" %%a IN (
	`REG QUERY "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /V {374DE290-123F-4565-9164-39C4925E467B}`
) DO (
	SET DOWNLOADS=%%b
)
timeout /T 2 /nobreak >nul
echo Listing connected Devices
timeout /T 1 /nobreak >nul
%DOWNLOADS%\platform-tools\adb devices
timeout /T 2 /nobreak >nul
echo Starting to mock your battery
timeout /T 1 /nobreak >nul
%DOWNLOADS%\platform-tools\adb shell dumpsys battery set level 1
%DOWNLOADS%\platform-tools\adb shell dumpsys battery set wireless 1
%DOWNLOADS%\platform-tools\adb shell dumpsys battery set status 2
timeout /T 2 /nobreak >nul
echo Succesfully mocked your battery
timeout /T 5 /nobreak >nul
echo PRANKED
start https://youtu.be/O91DT1pR1ew
timeout /T 5 /nobreak >nul
echo To return to normal Battery Status, just restart your phone, or open cmd in the platform-tools folder and type: [adb shell dumpsys battery reset]!
timeout /T 10 /nobreak >nul