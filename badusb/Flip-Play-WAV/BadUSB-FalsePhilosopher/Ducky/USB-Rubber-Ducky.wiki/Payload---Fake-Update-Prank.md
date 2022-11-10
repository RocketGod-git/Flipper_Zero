Using fakeupdate.net, set the screen so it looks like eternal fake update is happening. This one's for Win7 but pick your local OS (or more fun - a different one!). If you can give the mouse a slight "shove" downwards to prevent some instances of the menu bar showing up, all the better.

```
DELAY 5000
GUI d
DELAY 100
CONTROL ESCAPE
DELAY 100
STRING iexplore -k http://fakeupdate.net/win7/index.html
ENTER
DELAY 2000
F11
```