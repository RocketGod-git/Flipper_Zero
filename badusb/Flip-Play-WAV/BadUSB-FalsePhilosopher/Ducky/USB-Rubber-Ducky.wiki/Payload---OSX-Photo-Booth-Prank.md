```
REM Author: Cameron Glass
REM Description: This payload opens a photo booth window and automatically takes a picture. Once this picture is taken, this payload proceeds to open terminal and tell it to say "You look ugly!". This payload is great for friends and family.
REM Credits: I must give all of the credit to Hak5 for their amazing product. This is my first payload and I hope it is a good one!
REM --------------------------------
DELAY 1000
GUI SPACE
DELAY 100
STRING photo booth
DELAY 100
ENTER
DELAY 1000
ENTER
DELAY 3000
GUI SPACE
DELAY 100
STRING terminal
DELAY 100
ENTER
DELAY 1000
STRING say You look ugly!
DELAY 100
ENTER
```