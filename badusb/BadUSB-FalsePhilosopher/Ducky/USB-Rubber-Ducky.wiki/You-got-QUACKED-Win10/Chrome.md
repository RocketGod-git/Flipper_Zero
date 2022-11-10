* Auther - Justin

* Win10

* Description: Changes the users desktop background to a Rubber Duck saying “YOU GOT QUACKED!” and prints the screen, hides icons, and taskbar. This is my first duckyscript and Git. It works with Win10 with chrome and Windows Photo app. It has long delays for slow computers.

GUI d

DELAY 1000

GUI r

DELAY 1000

STRING chrome https://i.imgflip.com/1dv8ac.jpg

ENTER

DELAY 6000

ENTER

DELAY 1000

CTRL s

DELAY 1000

STRING %userprofile%\Desktop\QUACKED

DELAY 1000

ENTER

DELAY 1000

GUI d

DELAY 1000

GUI r

DELAY 1000

STRING %userprofile%\Desktop\QUACKED.jpg

DELAY 1000

SHIFT F10

DELAY 1000

REM The repeat switch didn't work for me here.

DOWN

DOWN

DOWN

DOWN

DOWN

DOWN

DOWN

DOWN

DOWN

DOWN

DELAY 1000

ENTER

DELAY 1000

DOWN

DELAY 1000

ENTER

GUI d

DELAY 700

PRINTSCREEN

DELAY 700

SHIFT F10

DELAY 700

DOWN

DELAY 700

RIGHT

DELAY 700

STRING D

SHIFT F10

DELAY 700

STRING R

DELAY 1000

TAB

DELAY 700

DOWN

REPEAT 4

ENTER

DELAY 700

TAB

DELAY 700

TAB

DELAY 700

REM To toggle taskbar on or off change to "SPACE" for Win 10 and "UP ARROW" for Server 2016

SPACE

GUI D

DELAY 700

GUI r

DELAY 2000

STRING mspaint

ENTER

DELAY 2000

CTRL v

DELAY 700

CTRL s

DELAY 1000

STRING %userprofile%\a.bmp

ENTER

DELAY 700

ALT f

DELAY 700

STRING K

DELAY 700

STRING F

DELAY 1000

ALT F4

DELAY 700

GUI d

