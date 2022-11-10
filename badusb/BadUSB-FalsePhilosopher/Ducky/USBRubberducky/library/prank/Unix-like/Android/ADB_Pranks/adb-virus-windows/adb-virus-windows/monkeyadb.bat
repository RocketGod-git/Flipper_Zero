@echo off
timeout /T 1 /nobreak >nul
if not exist \Users\%username%\Downloads\platform-tools\ echo Bitte lade zuerst die platform tools (Windows) auf der Website die gleich auf gemacht wird herunter!
if not exist \Users\%username%\Downloads\platform-tools\ timeout /T 2 /nobreak >nul
if not exist \Users\%username%\Downloads\platform-tools\ echo ansonsten wird es nicht funktionieren...
if not exist \Users\%username%\Downloads\platform-tools\ pause
if not exist \Users\%username%\Downloads\platform-tools\ start https://developer.android.com/studio/releases/platform-tools
if not exist \Users\%username%\Downloads\adb-virus-windows\ rename adb-virus-windows-master\ adb-virus-windows\
if not exist \Users\%username%\Downloads\platform-tools\ start cmd /C monkeyadb-download.bat
if not exist \Users\%username%\Downloads\platform-tools\ echo Nutze bitte die Enter-Taste nachdem sich das andere Fenster geschlossen hat!
if not exist \Users\%username%\Downloads\platform-tools\ pause
if not exist \Users\%username%\Downloads\platform-tools\ echo Ready?
pause
echo Dieses Script wird ein Programm auf deinem Handy starten!
timeout /T 3 /nobreak
echo Sicher, das du dies tun willst?
timeout /T 2 /nobreak >nul
echo Ok, du hast dich gegen den Abbruch entschieden...
timeout /T 2 /nobreak >nul
echo 3
timeout /T 1 /nobreak >nul
echo 2
timeout /T 1 /nobreak >nul
echo 1
timeout /T 1 /nobreak >nul
cd ../platform-tools/
adb shell monkey -p com.android.settings -v 500