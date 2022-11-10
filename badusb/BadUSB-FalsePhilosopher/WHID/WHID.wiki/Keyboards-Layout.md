# **Keyboard Layouts**

## How to Change Keyboard Layouts in WHID's Software and Wifi Ducky
It is very simple, you just need to copy-paste one of the locales from https://github.com/whid-injector/WHID/tree/master/tools/keyboard_layouts and replace _asciimap of Keyboard.cpp

Just follow this video and it will be clear ;]

https://youtu.be/DPYGKdBjZTw


It can also be automated (thanks @Bluearduino20):

https://www.youtube.com/watch?v=R4KqMYCCu4A

https://www.youtube.com/watch?v=gxE7GKLcC2w


## For the FRENCH Layout
With the French keyboard layout we can't Type the letters ~#{[|`\^@]} with the WHID injector because the keyboard.cpp module is for qwerty, and qwerty only need SHIFT to access all other keys while French keyboard need SHIFT and also ALT RIGHT in order to type all keys.

@Nazime just added a condition to activate the ALT RIGHT modifier for those ASCII letters ~#{[|`\^@]} 
```cpp
// Press ALT RIGHT for ~#{[|`\^@]} for french keyboard
	    if (k == 126|| k == 35|| k == 123|| k == 91|| k == 124|| k == 96|| k == 92|| k == 94|| k == 64|| k == 93|| k == 125){
            _keyReport.modifiers |= 0x40;  // 0x40 is the ALT RIGHT 
      }
```

```cpp
// Release ALT RIGHT for ~#{[|`\^@]} for french keyboard
	    if (k == 126|| k == 35|| k == 123|| k == 91|| k == 124|| k == 96|| k == 92|| k == 94|| k == 64|| k == 93|| k == 125){
            _keyReport.modifiers &= ~(0x40); // 0x40 is the ALT RIGHT 
        }
```
In order to have the french keyboard working alright, you have to upload the sketch Arduino_32u4 with this keyboard.cpp file:
https://github.com/whid-injector/WHID/blob/master/tools/keyboard_layouts/Keyboard_fr_FR.cpp

Using this technique you can also modifies the keyboard.cpp in order to have all ASCII keys in other layout.
***
**[Deprecated] Rubber Ducky against Non-English Environments**

http://akasakatonight.com/elkentaro/2016/09/07/multilingual-rubberducky-and-ducky-script/

It might work even without being Administrator...

    GUI r
    DELAY 500
    STRING cmd
    DELAY 500
    ENTER
    DELAY 1000
    STRING powershell New-WinUserLanguageList en-US
    DELAY 500
    ENTER
    STRING powershell Set-WinUserLanguageList -LanguageList en-US
    DELAY 500
    ENTER
    ENTER
    REM Place here your payload

Here below the original one:

    GUI r
    DELAY 500
    STRING powershell Start-process cmd -Verb runAs
    DELAY 500
    ENTER
    DELAY 2000
    ALT y
    DELAY 1000
    STRING powershell New-WinUserLanguageList en-US
    DELAY 500
    ENTER
    STRING powershell Set-WinUserLanguageList -LanguageList en-US
    DELAY 500
    ENTER
    ENTER
    REM Place here your payload
    DELAY 500
    STRING calc