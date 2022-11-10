This process is designed to disable windows defender, 
then copy the wifi information with passwords in clear text into a new directory.

You will need to modify the output to be in the newly created "l" directory, 
as this will be added to the email. 
as this is a .ps1 file you may be able to host this powersploit on a free service,
such as 000webhost or similar.

Email.ps1:
You will need to substitute your email and password where it is stated.
This script will email all the files that are in the new folder "l" in a single email. 
this will include all the stored wifi access point information, and the information obtained from "Chrome Dump". 
If you did not wish to waste time with displaying the names of folders, or that the email has been sent successfully, remove these from the script

Note that you will need to acces via some way the email.ps1 in the victim machine!!
