**The plan is to  rewrite the sketch in order to be compatible with Rubberducky's Syntax though.**

<br>
<b>Writing a Payload:</b><br>
* For individual keypresses or combinations of key presses<br>
"Press:X" or "Press:X+Y" or "Press:X+Y+Z" and so forth.<br> (It expects DECIMAL Values for X,Y,Z,etc)<br>
[Example: "Press:131+114" would output KEY_LEFT_GUI(Windows_Key)+r thus launching the run prompt if connected to a Windows machine]<br>
* List of modifier keys(GUI,ALT,CTRL,ETC) at https://www.arduino.cc/en/Reference/KeyboardModifiers<br>
* ASCII table lookup at http://www.asciitable.com/<br>
<br>
<b>To type out strings of text</b><br>
"Print:XYZ" Types out "XYZ"<br>
<br>
<b>To type out strings of text followed by the ENTER Key</b><br>
"PrintLine:XYZ" Types out "XYZ" then presses enter<br>

## Decimal Keys Reference

- **AsciiTable from:** http://www.asciitable.com/

![](http://i.imgur.com/REkQedy.gif)

- **Keyboard_modifiers from:** https://www.arduino.cc/en/Reference/KeyboardModifiers

Key                   Decimal value<br>
KEY_LEFT_CTRL         128<br>
    KEY_LEFT_SHIFT        129<br>
    KEY_LEFT_ALT          130<br>
    KEY_LEFT_GUI          131<br>
    KEY_RIGHT_CTRL        132<br>
    KEY_RIGHT_SHIFT       133<br>
    KEY_RIGHT_ALT         134<br>
    KEY_RIGHT_GUI         135<br>
    KEY_UP_ARROW          218<br>
    KEY_DOWN_ARROW        217<br>
    KEY_LEFT_ARROW        216<br>
    KEY_RIGHT_ARROW       215<br>
    KEY_BACKSPACE         178<br>
    KEY_TAB               179<br>
    KEY_RETURN            176<br>
    KEY_ESC               177<br>
    KEY_INSERT            209<br>
    KEY_DELETE            212<br>
    KEY_PAGE_UP           211<br>
    KEY_PAGE_DOWN         214<br>
    KEY_HOME              210<br>
    KEY_END               213<br>
    KEY_CAPS_LOCK         193<br>
    KEY_F1                194<br>
    KEY_F2                195<br>
    KEY_F3                196<br>
    KEY_F4                197<br>
    KEY_F5                198<br>
    KEY_F6                199<br>
    KEY_F7                200<br>
    KEY_F8                201<br>
    KEY_F9                202<br>
    KEY_F10               203<br>
    KEY_F11               204<br>
    KEY_F12               205<br>
