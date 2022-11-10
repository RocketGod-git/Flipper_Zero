@echo off
echo Dieses Fenster schliesst sich automatisch! Bitte nutze die Enter-Taste, nachdem der Download Abgeschlossen wurde
pause
cd ../
rename platform-tools*.zip platform-tools.zip
tar -xf platform-tools.zip