Author: KTibow  
Target: Any platform that supports Alt+F2, Command+Space, or Control+R.  
Description: A simple script that opens a webpage. It's based on [Hak5 2124](https://www.youtube.com/watch?v=qGPGOoJn54E), but it presses Command+Space 3 times, because on Windows it changes the keyboard layout, and it has 3 options. Make sure to change the firmware as in [the original video](https://youtu.be/qGPGOoJn54E?t=861) on Macs to avoid the pop-up about the layout. 
```
DELAY 600
REM Linux run dialog
ALT F2
DELAY 200
REM Mac OS run dialog
GUI SPACE
DELAY 200
REM On Windows this changes the input language, so press 3 times
GUI SPACE
DELAY 200
GUI SPACE
DELAY 200
GUI r
DELAY 200
REM On another OS, this could have typed "   r". Backspace 4 times.
DELETE
REPEAT 4
REM Type in URL and open page!
STRING http://example.com/
ENTER
```