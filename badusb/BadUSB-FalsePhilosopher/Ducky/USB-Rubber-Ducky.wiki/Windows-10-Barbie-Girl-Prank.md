

```
REM <---- These delay values seem to work great for me. Over all it will take 
REM <----- 17.5 secs to execute. Mostly because of YouTube ads. Play around
REM <----- with the delay values to decrease execute time. 
REM <----- If you don't care about the ads delete the step for tabbing to the skip ad. 
REM <----- Tested on Windows 10
DELAY 3000
REM <----- Minimize all windows
GUI D
DELAY 400
REM <----- Opens run
GUI R
DELAY 400
REM <----- Go to my specified YouTube video
STRING https://www.youtube.com/watch?v=ZyhrYis509A&feature=player_embedded
DELAY 600
REM <----- Press Enter
ENTER
REM <----- Some videos have 2-3 min ads the next part will wait 5.5 secs and tab to
REM <----- skip ad. Sometimes it pauses the video if there is no ad.
DELAY 5500
TAB
DELAY 100
TAB
DELAY 100
ENTER
DELAY 1000
REM <----- Opens run
GUI R
DELAY 500
REM <----- Goes specified image url (if it doesnt work the url changed. Find another
REM <----- anoying Barbie pic and use that url ;)
STRING https://i.ytimg.com/vi/U_GTMYjnnoY/maxresdefault.jpg
DELAY 600
ENTER
DELAY 1000
REM <----- Set window to right
GUI RIGHT
DELAY 400
REM <----- Press Esc (exit out of 'choose neighbor window')
ESC
DELAY 400
REM <----- Opens run
GUI R
DELAY 400
REM <----- Type notepad
STRING notepad
DELAY 400
ENTER
DELAY 500
REM <----- Type these lines in notepad
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 50
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 50
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 50
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 50
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 50
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 50
STRING DON'T FORGET TO LOCK YOUR COMPUTER!
DELAY 50
ENTER
DELAY 50
STRING Or else Barbie will visit you again!
DELAY 50
ENTER
DELAY 400
REM <----- Set window to the left so you can see both text and image
GUI LEFT
REM <--- SUPER SIMPLE -HAVE FUN! - TYLER D. 
```