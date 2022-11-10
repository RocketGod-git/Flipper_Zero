REM Credits To Kylerees64

DELAY 5000

GUI R

DELAY 100

REM -Opens Volume Mixer-

STRING %windir%\System32\SndVol.exe -f 49825268

DELAY 50

ENTER

DELAY 100

REM -Mutes Volume-

END

DELAY 50

ESC

GUI R

DELAY 100

STRING Chrome.exe https://www.youtube.com/watch?v=rtUl0SXOqbM

DELAY 50

ENTER

GUI R

DELAY 100

REM -Opens a New Page Where The Cursor Cant Be Seen (You Can Use Any Other Method)-

STRING Chrome.exe https://fakewindowsupdate.com/gb/vista/index.html

DELAY 250

F11

DELAY 250

GUI R

DELAY 100

STRING %windir%\System32\SndVol.exe -f 49825268

ENTER

DELAY 100

REM -Turns Volume All The Way Up-

HOME

ESC

