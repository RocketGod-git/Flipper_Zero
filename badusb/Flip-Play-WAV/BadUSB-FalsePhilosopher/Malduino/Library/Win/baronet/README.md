# The Baronet https://github.com/ishan-saha/baronet
1.	Baronet.ino – This is the scratch file for the atmega32u4 micro controller to be used as the HID attack device that         downloads the password decrypter and sends the password and ipaddress and basic user info to the given mail then it downloads a Metasploit shell or backdoor (could be a custom written backdoor) in the windows registery. This script was made by duckuino github repo…
2.	PASSVIEWER.PY – This is the python script that decrypts the password and emails it to the mail specified (feel free to change the file to your need).
3.	PASSVIEWER.exe – This is the passvierwer executable for getting the passwords into the stdio (cmd or powershell) 

You will have to provide the sender email address its password and the reciever's email address plus the urls for downloading the script. This attack vector works with windows 8, 8.1, 10 but doesnt work with windows 7 or vista due to drives issues and the character printed are not exactly the once writen in the .ino file. Feel free to mail me at ishansaha@outlook.com for any changes and other stuff that might enhance the working of the script.
