## Wifi Ducky

Clone this repo https://github.com/whid-injector/wifi_ducky

    ###[IMPORTANT]###
    If you wanna switch from WHID software to WifiDucky (or viceversa), 
    you HAVE to erase the ESP's Flash:
    python esptool.py -p WHID-PORT erase_flash 
    or 
    python esptool.py -p WHID-PORT erase_flash --flash_mode dio


    ###[IMPORTANT]###
    It is recommended to reducey Wifi Ducky's Serial speed from:
    #define BAUD_RATE 57200 to #define BAUD_RATE 9600
    In https://github.com/spacehuhn/wifi_ducky/blob/master/arduino_wifi_duck/arduino_wifi_duck.ino
    and https://github.com/spacehuhn/wifi_ducky/blob/master/esp8266_wifi_duck/esp8266_wifi_duck.ino


For the Wifi Ducky you also need to install the following Libraries
- ESPAsyncWebServer - https://github.com/me-no-dev/ESPAsyncTCP/archive/master.zip
- ESPAsyncTCP - https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip

How to install Libraries in Arduino:
https://www.baldengineer.com/installing-arduino-library-from-github.html

**[VIDEO] How to configure Wifi Ducky (WINDOWS)** https://youtu.be/PGa_ByyQw8Q
