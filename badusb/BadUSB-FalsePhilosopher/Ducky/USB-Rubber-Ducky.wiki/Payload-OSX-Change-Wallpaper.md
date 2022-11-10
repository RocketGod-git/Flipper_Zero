    REM A script to download (wget) and set a wallpaper on OSX (Tested on OSX Sierra) 
    REM Swap out the link/file name with your own.
    DELAY 500
    GUI SPACE
    DELAY 200
    STRING Terminal
    ENTER
    DELAY 300
    STRING curl -O http://fanaru.com/gudetama/image/246541-gudetama-gudetama.png
    DELAY 600
    ENTER
    DELAY 750
    STRING mv 246541-gudetama-gudetama.png x.png
    DELAY 200
    ENTER
    STRING sqlite3 /$HOME/Library/Application\ Support/Dock/desktoppicture.db "update data set value = '/Users/$USER/x.png'" && killall Dock
    DELAY 200
    ENTER
    DELAY 200
    STRING exit
    DELAY 200
    ENTER