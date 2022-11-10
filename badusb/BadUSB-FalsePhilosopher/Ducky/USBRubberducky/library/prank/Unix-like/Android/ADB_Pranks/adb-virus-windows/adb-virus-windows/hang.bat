@echo off
FOR /F "USEBACKQ TOKENS=2,*" %%a IN (
	`REG QUERY "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /V {374DE290-123F-4565-9164-39C4925E467B}`
) DO (
	SET DOWNLOADS=%%b
)
echo This will hang/crash your android device!
timeout /T 2 /nobreak >nul
echo To Cancel: CTRL+C
timeout /T 2 /nobreak >nul
echo Last chance to cancel!
timeout /T 5 /nobreak >nul
echo Ok, say goodbye to your phone (at least for now)!
timeout /T 1 /nobreak >nul
%DOWNLOADS%\platform-tools\adb shell am hang --allow-restart
timeout /T 2 /nobreak >nul
echo Bye
timeout /T 5 /nobreak >nul