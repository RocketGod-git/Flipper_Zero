`REM Script by Darren Rainey http://github.com/DarrenRainey`

`DELAY 500`

`GUI`

`DELAY 150`

`TAB`

`DELAY 150`

`TAB`

`DELAY 150`

`ENTER`


&nbsp;

&nbsp;

&nbsp;

...Or you could just do
```
REM Leave a little reminder to lock your PC (just delete or comment this out if you don't want that)
GUI r
DELAY 300
STRING notepad
DELAY 300
ENTER
DELAY 300
STRING You forgot to lock your PC.
DELAY 3000


REM Lock the PC
GUI l
```
I've only tested this on Windows 10, but I believe it works on Windows 7 and higher (*maybe* even Vista).

\- Sam van der Kris ([GitLab](https://gitlab.com/warkitteh))