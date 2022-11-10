Possible solution taken from https://github.com/exploitagency/ESPloitV2/issues/3

Find and edit boards.txt, it may be located at

Linux: /root/.arduino15/packages/arduino/hardware/avr/1.6.19/
 
 or

Windows:  C:\Users\USER\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.6.19\ 

 or somewhere else...

Add the below quote to the end of boards.txt, RESTART THE ARDUINO IDE(boards.txt is loaded at startup I believe), select Cactus WHID under boards instead of LilyPadUSB when you upload the Arduino_32u4_Code sketch.

    ##############################################################

    CactusWHID.name=Cactus WHID
    CactusWHID.vid.0=0x1B4F
    CactusWHID.pid.0=0x9207
    CactusWHID.vid.1=0x1B4F
    CactusWHID.pid.1=0x9208

    CactusWHID.upload.tool=avrdude
    CactusWHID.upload.protocol=avr109
    CactusWHID.upload.maximum_size=28672
    CactusWHID.upload.maximum_data_size=2560
    CactusWHID.upload.speed=57600
    CactusWHID.upload.disable_flushing=true
    CactusWHID.upload.use_1200bps_touch=true
    CactusWHID.upload.wait_for_upload_port=true

    CactusWHID.bootloader.tool=avrdude
    CactusWHID.bootloader.low_fuses=0xff
    CactusWHID.bootloader.high_fuses=0xd8
    CactusWHID.bootloader.extended_fuses=0xce
    CactusWHID.bootloader.file=caterina-LilyPadUSB/Caterina-LilyPadUSB.hex
    CactusWHID.bootloader.unlock_bits=0x3F
    CactusWHID.bootloader.lock_bits=0x2F

    CactusWHID.build.mcu=atmega32u4
    CactusWHID.build.f_cpu=8000000L
    CactusWHID.build.vid=0x0000
    CactusWHID.build.pid=0xFFFF
    CactusWHID.build.usb_product="Cactus WHID"
    CactusWHID.build.usb_manufacturer="April Brother"
    CactusWHID.build.board=AVR_LILYPAD_USB
    CactusWHID.build.core=arduino
    CactusWHID.build.variant=leonardo
    CactusWHID.build.extra_flags={build.usb_flags}



Replace this portion with your spoofed VID/PID.

    CactusWHID.build.vid=0x0000
    CactusWHID.build.pid=0xFFFF
    CactusWHID.build.usb_product="Cactus WHID"
    CactusWHID.build.usb_manufacturer="April Brother"

On Apple Devices I believe you can bypass the unknown keyboard hurdle by spoofing an Apple VID/PID thus running payload upon insertion vs having to identify the keyboard first.

I believe the below will work.

    CactusWHID.build.vid=0x05ac
    CactusWHID.build.pid=0x021e
    CactusWHID.build.usb_product="Aluminum Keyboard IT USB"
    CactusWHID.build.usb_manufacturer="Apple Inc."

Some examples of Apple and Logitech VID/PID:

**Apple:**

Apple, Inc.

**VID**	**PID**

05ac	0201  USB Keyboard [Alps or Logitech, M2452]

05ac	0202  Keyboard [ALPS]

05ac	0205  Extended Keyboard [Mitsumi]

05ac	0206  Extended Keyboard [Mitsumi]

05ac	020b  Pro Keyboard [Mitsumi, A1048/US layout]

05ac	020c  Extended Keyboard [Mitsumi]

05ac	020d  Pro Keyboard [Mitsumi, A1048/JIS layout]

05ac	020e  Internal Keyboard/Trackpad (ANSI)

05ac	020f  Internal Keyboard/Trackpad (ISO)

05ac	0214  Internal Keyboard/Trackpad (ANSI)

05ac	0215  Internal Keyboard/Trackpad (ISO)

05ac	0216  Internal Keyboard/Trackpad (JIS)

05ac	0217  Internal Keyboard/Trackpad (ANSI)

05ac	0218  Internal Keyboard/Trackpad (ISO)

05ac	0219  Internal Keyboard/Trackpad (JIS)

05ac	021a  Internal Keyboard/Trackpad (ANSI)

05ac	021b  Internal Keyboard/Trackpad (ISO)

05ac	021c  Internal Keyboard/Trackpad (JIS)

05ac	021d  Aluminum Mini Keyboard (ANSI)

05ac	021e  Aluminum Mini Keyboard (ISO)

05ac	021f  Aluminum Mini Keyboard (JIS)

05ac	0220  Aluminum Keyboard (ANSI)

05ac	0221  Aluminum Keyboard (ISO)

05ac	0222  Aluminum Keyboard (JIS)

05ac	0223  Internal Keyboard/Trackpad (ANSI)

05ac	0224  Internal Keyboard/Trackpad (ISO)

05ac	0225  Internal Keyboard/Trackpad (JIS)

05ac	0229  Internal Keyboard/Trackpad (ANSI)

05ac	022a  Internal Keyboard/Trackpad (MacBook Pro) (ISO)

05ac	022b  Internal Keyboard/Trackpad (MacBook Pro) (JIS)

05ac	0230  Internal Keyboard/Trackpad (MacBook Pro 4,1) (ANSI)

05ac	0231  Internal Keyboard/Trackpad (MacBook Pro 4,1) (ISO)

05ac	0232  Internal Keyboard/Trackpad (MacBook Pro 4,1) (JIS)

05ac	0236  Internal Keyboard/Trackpad (ANSI)

05ac	0237  Internal Keyboard/Trackpad (ISO)

05ac	0238  Internal Keyboard/Trackpad (JIS)

05ac	023f  Internal Keyboard/Trackpad (ANSI)

05ac	0240  Internal Keyboard/Trackpad (ISO)

05ac	0241  Internal Keyboard/Trackpad (JIS)

05ac	0242  Internal Keyboard/Trackpad (ANSI)

05ac	0243  Internal Keyboard/Trackpad (ISO)

05ac	0244  Internal Keyboard/Trackpad (JIS)

05ac	0245  Internal Keyboard/Trackpad (ANSI)

05ac	0246  Internal Keyboard/Trackpad (ISO)

05ac	0247  Internal Keyboard/Trackpad (JIS)

05ac	024a  Internal Keyboard/Trackpad (MacBook Air) (ISO)

05ac	024d  Internal Keyboard/Trackpad (MacBook Air) (ISO)

05ac	0250  Aluminium Keyboard (ISO)

05ac	0252  Internal Keyboard/Trackpad (ANSI)

05ac	0253  Internal Keyboard/Trackpad (ISO)

05ac	0254  Internal Keyboard/Trackpad (JIS)

05ac	0259  Internal Keyboard/Trackpad

05ac	0263  Apple Internal Keyboard / Trackpad (MacBook Retina)

05ac	0267  Magic Keyboard A1644


**Logitech:**

Logitech, Inc.

**VID**	**PID**
046d	c221  G11/G15 Keyboard / Keyboard

046d	c222  G15 Keyboard / LCD

046d	c223  G11/G15 Keyboard / USB Hub

046d	c225  G11/G15 Keyboard / G keys

046d	c226  G15 Refresh Keyboard

046d	c227  G15 Refresh Keyboard

046d	c228  G19 Gaming Keyboard

046d	c229  G19 Gaming Keyboard Macro Interface

046d	c22a  Gaming Keyboard G110

046d	c22b  Gaming Keyboard G110 G-keys

046d	c22d  G510 Gaming Keyboard

046d	c22e  G510 Gaming Keyboard onboard audio

046d	c248  G105 Gaming Keyboard

046d	c24d  G710 Gaming Keyboard

046d	c30e  UltraX Keyboard (Y-BL49)

046d	c30f  Logicool HID-Compliant Keyboard (106 key)

046d	c311  Y-UF49 [Internet Pro Keyboard]

046d	c312  DeLuxe 250 Keyboard

046d	c313  Internet 350 Keyboard

046d	c315  Classic Keyboard 200

046d	c316  HID-Compliant Keyboard

046d	c317  Wave Corded Keyboard

046d	c318  Illuminated Keyboard

046d	c31b  Compact Keyboard K300

046d	c31c  Keyboard K120

046d	c31d  Media Keyboard K200

046d	c31f  Comfort Keyboard K290

046d	c326  Washable Keyboard K310

046d	c328  Corded Keyboard K280e

046d	c335  G910 Orion Spectrum Mechanical Keyboard

046d	c33a  G413 Gaming Keyboard
