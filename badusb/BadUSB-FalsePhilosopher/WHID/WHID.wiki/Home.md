# **What is WHID?**

It stands for WiFi HID Injector. 
It is a WiFi remotely-controlled {Keyboard, Mouse} Emulator.
Practically is an USB Rubberducky or BadUSB device on Steroids!

**Video Introduction**  https://youtu.be/U-TtobZXJcw

**Blog Post** https://medium.com/@LucaBongiorni/whid-injector-how-to-bring-hid-attacks-to-the-next-level-b06a40b7df22

# **Where to Buy?** 

http://www.ebay.com/itm/Cactus-WHID-WiFi-HID-InjectorAn-USB-Rubberducky-On-Steroids-for-hackers-pentests-/252927790606

https://www.aliexpress.com/item/Cactus-Micro-compatible-board-plus-WIFI-chip-esp8266-for-atmega32u4/32318391529.html

https://blog.aprbrother.com/product/cactus-whid

https://www.tindie.com/products/aprbrother/cactus-whid-wifi-hid-injector-usb-rubberducky/

# **Main Requirements**

- Arduino IDE

- esptool from https://github.com/whid-injector/esptool  Checkout https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/flash-firmware on how to install it!

First of all you need to install the ESP8266 Libraries.
- Go on File > Preferences > Additional Board Manager URLs
- Paste there http://arduino.esp8266.com/stable/package_esp8266com_index.json and press OK
- Go Tools > Board: > Board Manager
- Type ESP8266 and Install the 2.3.0 version.

# **How To Configure WHID software (WINDOWS)**
Please keep in mind that the following Video is for installing WHID Software into Cactus Micro (which has 512K/64K Flash). If you wanna install on Cactus WHID hardware, select 4M/3M option in Arduino's settings

**[VIDEO]** https://youtu.be/MRGUSPW-Cr0

# **How To Configure WHID software (OSX)**
**[VIDEO]** https://youtu.be/3FOLTxtehf0

`git clone https://github.com/whid-injector/esptool`

`cd esptool/`

`sudo pip install pyserial`

`sudo python ./setup.py install`

`python esptool.py --port=/dev/cu.usbmodem1411 -b 115000 write_flash 0x00000 ../WHID/sketches/cactus_micro_rev2/ESP_Sketch/compiled.bin `

# **Third Party Softwares**
## ESPloit V2
Enhanced version of WHID GUI (pre-installed on Cactus WHID)
https://github.com/exploitagency/ESPloitV2

## USaBuse
Used for Airgapped Environments BYPASS!
https://github.com/sensepost/USaBUSe

coming soon...

## Wifi Ducky

https://github.com/spacehuhn/wifi_ducky

    ###[IMPORTANT]###
    If you wanna switch from WHID software to WifiDucky (or viceversa), you HAVE to:
        1) Hard Reset WHID by using the magnet 
           (as described in https://github.com/whid-injector/WHID/wiki#unbrick--hard-reset).

        2) Erase the ESP's Flash: python esptool.py -p WHID-PORT erase_flash
           You need to do it AFTER uploading the ESP_Programmer.ino and BEFORE uploading the ESP_Sketch.ino 
           (or esp8266_wifi_duck.ino).


    ###[IMPORTANT]###
    It is recommended to reduce Wifi Ducky's Serial speed from:
    #define BAUD_RATE 57200 to #define BAUD_RATE 9600
    In https://github.com/spacehuhn/wifi_ducky/blob/master/arduino_wifi_duck/arduino_wifi_duck.ino
    and https://github.com/spacehuhn/wifi_ducky/blob/master/esp8266_wifi_duck/esp8266_wifi_duck.ino
    ### This repo has been already patched and ready to be used! https://github.com/whid-injector/wifi_ducky ###


For the Wifi Ducky you also need to install the following Libraries
- ESPAsyncWebServer - https://github.com/me-no-dev/ESPAsyncTCP/archive/master.zip
- ESPAsyncTCP - https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip

How to install Libraries in Arduino:
https://www.baldengineer.com/installing-arduino-library-from-github.html

**[VIDEO] How to configure Wifi Ducky (WINDOWS)** https://youtu.be/PGa_ByyQw8Q

# **Software Unbrick & Reset to Default Configuration**

Plug the device into your computer.  
Open the Arduino IDE.  
Select Tools - Board - "LilyPad Arduino USB".  
Select Tools - Port and the port the device is connected to.  
Select Tools - "Serial Monitor".  
Select "38400 baud".  
Now type in "ResetDefaultConfig:". Without the quotes but be sure to include the colon symbol.  
Click Send.  
You should now receive the following reply "Resetting configuration files back to default settings."  
Wait about 15 seconds or until the LED blinks and unplug and replug in the device.  
The device has now been reset back to default settings.  
Connect to the Access Point with the SSID "Exploit" with a password of "DotAgency".  
Open a web browser pointed to "http://192.168.1.1"  
The default administration username is "admin" and password "hacktheplanet".  
  
NOTE: Certain devices seem to have trouble connecting to a password protected ESP8266 access point. The symptoms of this involve repeatedly being prompted to enter the password and being unable to connect to the ESP8266 via WiFi. This can be solved by following the above instructions but instead issuing the command "ResetDefaultConfig:OpenNetwork" via serial. The device will be restored to the factory defaults(with the exception of now being an unsecured network). The device will reboot and you may now connect to it as an unsecured WiFi access point with an SSID of "Exploit". You should now be able to establish a connection.  

Source: https://github.com/exploitagency/ESPloitV2/blob/master/README.md#resetting-to-default-configurationrecovering-device

# **Hardware Unbrick & Hard-Reset**

Incorporating all of the USB tasks on a single chip is an awesome feature that makes the WHID and boards like it truly unique. But it also places more stress on a single chip, and if anything goes wrong with that chip, the board becomes nearly unusable. It’s not uncommon for WHID’s to become “bricked” and unprogrammable. 
But, in most cases, the bricking is reversible!

The most common source of WHID “bricking” is uploading code to it with an incorrectly set board.

To revive the WHID, you’ll need to find a way to upload a sketch (even a default one is ok) to it with the board option correctly set. We can do this with a little help from the bootloader.

First, you’ll need to set the serial port to the bootloader. But that port is only visible when the board is in bootloader mode, so pull the reset line low twice quickly to invoke the bootloader reset feature discussed above. You can quickly press the **reset button**** twice. While the WHID is in the bootloader mode, change the ‘Tools > Serial Port’ menu to the bootloader COM port. Quick! You’ve only got eight seconds. [On Windows, the bootloader’s COM port number is usually one number higher than the Cactus WHID/Micro’s regular port number.]

****The reset button is a HALL sensor, that means you need to place a magnet close that side of the PCB, in order to simulate the "button pressure". And yes, it works also with WHID inside the USB case! So you don't need to extract the PCB from the plastic case everytime!** :smiley:

1) open Arduino IDE and open ESP PRogrammer sketch

2) Insert WHID

3) Press Upload sketch

4) Start the unbrick phase with a magnet by placing it close that side of the PCB where the hall sensor is located (do it two times). Close-away-close-away

https://youtu.be/-ohGYx5zBko

![](http://i.imgur.com/pAclUTM.jpg)

**For Cactus Micro Rev2:**

http://wiki.aprbrother.com/wiki/Cactus_Micro_Rev2_Troubleshooting_and_FAQ#How_to_Revive_a_.E2.80.9CBricked.E2.80.9D_Cactus_Micro

# **Still Issues? Here some Tips...**

Here some tips that might help:
1) Reduce BAUDRATE from 57200bps to 9600bps in both Wifi Ducky sketches. (9600bps for the serial between atmega32u4 and ESP is more than enough).
2) When you flash with ESPTool or Flasher.exe, use a bit lower baudrates (e.g. 115000 instead of 115200)
3) Upload the ESP Programmer sketch and then erase its flash with:
python esptool.py -p WHID-PORT erase_flash

If above will not work... there is a 99,9% of probability the cause is your computer (i.e. USB controller, drivers, etc.) or something got fucked-up on the Arduino IDE!

-  Try with another PC (if u can) or at least use a USB 2.0 port or a USB 2.0 HUB.
-  Change Arduino IDE version (sometimes it get screwed-up)
-  Completely uninstall and reinstall the existing version of Arduino IDE

# **HOW TO OPEN A TICKET!**

1) Which OS are you using?
2) Which Arduino IDE Version?
3) The ESPtool you are using is from https://github.com/whid-injector/esptool ?
4) The USB port you are using is USB 3.0? (sometimes they may create issues with arduino boards. try a usb 2.0 or a usb hub)
5) Did you try with an older version of Arduino IDE (i.e. 1.6.0)?
6) Did you try to use an USB 2.0 port?
7) Did you try with another laptop/PC?

# **General Resources**

- https://learn.adafruit.com/building-and-running-micropython-on-the-esp8266/flash-firmware
