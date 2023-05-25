#https://github.com/SomnambulantDead/F0_SubGhz

Flipper Zero RAW .sub files for Walgreens Customer Service Buttons.

Help Button: Signals form Help Buttons that send 3 alerts consecutive alerts and must be shut off with Reset Button.

Button Resets: Signals from Reset buttons for associated Customer Service Buttons.

Dwell Sensor: Signals from dwell/proximity sensorts that send single, instant alerts.

Handheld Call Buttons: Signals from Handheld call buttons that send single, instant alerts.

Info on related codes within folders if someone wanted to reverse engineer. FCC registration indicates OOK using 303.825 MHz Freq.
Related boxes from Indyme using the same frequency contain this info:

Description of operation: CB520 
The microprocessor controlled callbox is a self contained, low transmit power unit with integral lifetime battery (estimated lifetime is 7-10 years under normal use). It is installed in a nonconductive plastic enclosure with customer specific graphic overlays. 
When a SET button is pressed, the P (which is in “sleep” mode with the oscillator stopped) starts up, reads the button press, then transmits the approximate 20 bit word, repeated 20 times (about 2.5 seconds oftransmit time). One led will blink for the duration of the transmission. The P then resumes the “sleep” mode. The word coding consists of 8 “address” bit as a system address, 8 “ID” bits as a point or channel ID, and 4 “Status” bits to indicate low battery, etc (presently not all bits are used). 
If multiple set buttons are pressed the unit will transmit a separate set message for each button.  P
rogramming is done via the front panel buttons as described in the installation instructions.  
Modes may be changed during the programming process. 
The charge pump is turned on before a transmission to keep the output of the transmitter more nearlyconstant over the lifetime of the battery. The charge pump supplies a constant output voltage over a wide range of input voltages. 
The units operate at a nominal frequency of 303.825 MHz using an RFM HX1002-1 hybrid transmitter module, and a permanently attached wire antenna
https://fccid.io/J69CB520/Operational-Description/Operational-description-258745

WAG callboxes utilize an RFM TX5003 transmitter rather than the RFM HX1002-1.
