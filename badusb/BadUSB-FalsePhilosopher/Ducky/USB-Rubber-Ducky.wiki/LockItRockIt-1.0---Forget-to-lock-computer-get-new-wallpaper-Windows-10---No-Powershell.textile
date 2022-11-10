REM LockItRockIt 1.0
REM
REM Author: Bucky67GTO
REM Duckencoder: 2.6.3
REM Target: Windows 10
REM Description: If the User forgets to lock their computer, this script will go to a web image of your choosing and change their desktop to that image.
REM After applying the image to the desktop, it cleans up the image location.  With minor tweeks, you can have it be the lock screen as well.
REM
DEFAULTDELAY 250
DELAY 3000
GUI r
STRING microsoft-edge:http://img13.deviantart.net/fa59/i/2013/148/8/1/pinkie_pie_lockscreen_project_by_sinkurtiz-d66w98s.jpg
ENTER
DELAY 3000
GUI F11
DELAY 1500
PRINTSCREEN
ALT F4
GUI r
STRING mspaint
ENTER
DELAY 2000
CTRL v
ALT H
STRING RE
TAB
STRING 188
TAB
TAB
TAB
TAB
TAB
ENTER
CTRL s
STRING %USERPROFILE%\LockMeUpReminder.jpg
ENTER
ALT F
STRING B
ENTER
ALT F4
GUI r
STRING cmd
ENTER
STRING Del LockMeUpReminder.jpg
ENTER
ALT F4
GUI d
MENU
STRING r
TAB
TAB
TAB
TAB
TAB
STRING t
ENTER
ALT F4
END