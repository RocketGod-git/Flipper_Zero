# Writing duckyScript

From the duckypad repo https://github.com/dekuNukem/duckyPad

[Get duckyPad](https://www.tindie.com/products/21984/) | [Official Discord](https://discord.gg/4sJCBx5)

------

## Overview

duckyScript is a simple scripting language for automating keypresses. It was originally developed for [USB Rubber Ducky](https://shop.hak5.org/products/usb-rubber-ducky-deluxe).

This guide gives an concise overview of duckyScript. For more information, [see this page](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript).

## Examples

duckyScript is very easy and straightforward to write, you basically just tell it what key to press!

Let's take a look at some examples first:

### Open Task Manager

```
CONTROL SHIFT ESC
```

### Open a webpage on windows

```
WINDOWS r
DELAY 400
STRING https://www.youtube.com/watch?v=dQw4w9WgXcQ
ENTER
```

### Save a webpage then close it

```
CONTROL s
DELAY 600
ENTER
DELAY 600
CONTROL w
```

## Syntax Details

* One command per line. **`Each line has a 256 character limit!`**

* 1000 milliseconds = 1 second.

* Check out the [sample profiles](https://github.com/dekuNukem/duckyPad/tree/master/sample_profiles) for more examples.

## List of Commands

[REM](#REM)

[DEFAULTDELAY](#DEFAULTDELAY)

[DEFAULTCHARDELAY](#DEFAULTCHARDELAY)

[DELAY](#DELAY)

[STRING](#STRING)

[REPEAT](#REPEAT)

[Special Keys](#Special-Keys)

[Mouse Buttons](#Mouse-Buttons)

[MOUSE_MOVE](#MOUSE_MOVE-X-Y)

[MOUSE_WHEEL](#MOUSE_WHEEL-X)

[KEYDOWN / KEYUP](#KEYDOWN--KEYUP)

[SWCOLOR](#SWCOLOR)

[DP_SLEEP](#DP_SLEEP)

[PREV_PROFILE / NEXT_PROFILE](#PREV_PROFILE--NEXT_PROFILE)

[GOTO_PROFILE](#GOTO_PROFILE)

[HOLD](#HOLD-experimental)

[LOOP](#LOOP-experimental)

-----

### REM

`REM` is comment, any line starting with `REM` is ignored.

### DEFAULTDELAY

`DEFAULTDELAY` specifies how long (in milliseconds) to wait between **`each line of command`**.

If unspecified, `DEFAULTDELAY` is 18ms in duckyPad.

```
DEFAULTDELAY 100

REM duckyPad will wait 100ms between each subsequent command
```

### DEFAULTDELAYFUZZ X

Adds an additional random delay from 0 to X milliseconds after `each line of command`, can be used to make typing more human-like.

Set to 0 to disable.

### DEFAULTCHARDELAY

`DEFAULTCHARDELAY` specifies how long (in milliseconds) to wait between each **`key stroke`**.

If unspecified, `DEFAULTCHARDELAY` is 18ms in duckyPad.

```
DEFAULTCHARDELAY 50

REM duckyPad will wait 50ms between each key stroke
```

### DEFAULTCHARDELAYFUZZ X

Adds an additional random delay from 0 to X milliseconds after `each key stroke`, can be used to make typing more human-like.

Set to 0 to disable.

### DELAY

`DELAY` creates a momentary pause in script execution. Useful for waiting for UI to catch up.

```
DELAY 1000

REM waits 1000 milliseconds, or 1 second
```

### STRING

`STRING` types out whatever after it **`as-is`**.

```
STRING Hello world!!!

REM types out "Hello world!!!"
```

### REPEAT

Repeats the last command **`n`** times.

```
STRING Hello world
REPEAT 10

REM types out "Hello world" 11 times (1 original + 10 repeats)
```

### Special Keys

duckyScript also supports a bunch of special keys:

```
CTRL / RCTRL
SHIFT / RSHIFT
ALT / RALT
WINDOWS / RWINDOWS
COMMAND / RCOMMAND (mac)
OPTION / ROPTION (mac)
ESC
ENTER
UP
DOWN
LEFT
RIGHT
SPACE
BACKSPACE
TAB
CAPSLOCK
PRINTSCREEN
SCROLLLOCK
PAUSE
BREAK
INSERT
HOME
PAGEUP
PAGEDOWN
DELETE
END
MENU
POWER

F1
F2
F3
F4
F5
F6
F7
F8
F9
F10
F11
F12
F13
F14
F15
F16
F17
F18
F19
F20
F21
F22
F23
F24

(media keys)
MK_VOLUP
MK_VOLDOWN
MK_MUTE
MK_PREV
MK_NEXT
MK_PP (play/pause)
MK_STOP

(numpad keys)
NUMLOCK
KP_SLASH
KP_ASTERISK
KP_MINUS
KP_PLUS
KP_ENTER
KP_0
KP_1
KP_2
KP_3
KP_4
KP_5
KP_6
KP_7
KP_8
KP_9
KP_DOT
KP_EQUAL
```

Those special keys can be used on their own:

`WINDOWS`

...or can be combined with a character to form shortcuts:

`WINDOWS s`

...or can be combined with other special keys:

`WINDOWS SHIFT s`

------

* Type the key names as-is in **`ALL CAPS`**.

* **`UP TO 6 KEYS`** can be pressed simultaneously.

### Mouse Buttons

* `LMOUSE`: Click LEFT mouse button

* `RMOUSE`: Click RIGHT mouse button

* `MMOUSE`: Click MIDDLE mouse button

### MOUSE_MOVE X Y

Move mouse cursor `X` pixels horizontally, and `Y` pixels vertically.

* `X` and `Y` must be between `-127` and `127`

* For `X`, a positive number moves RIGHT, negative number moves LEFT.

* For `Y`, a positive number moves UP, negative number moves DOWN.

* Set `X` or `Y` to 0 if no movement needed.

* Use `REPEAT` command to move further.

### MOUSE_WHEEL X

Scroll mouse wheel `X` lines.

* `X` must be between `-127` and `127`

* A positive number scrolls UP, negative number scrolls DOWN.

### KEYDOWN / KEYUP

Holds / Releases a key.

Can be character key, modifier key, special key, or even mouse button!

Example:

```
KEYDOWN SHIFT
STRING hello
KEYUP SHIFT
```

### SWCOLOR

You can change the colour of a key on-the-fly with `SWCOLOR` command.

To change the colour of the **current key**, use `SWCOLOR R G B`:

`SWCOLOR 128 0 0`

To change the colour of a **particular key**, use `SWCOLOR_n R G B`:

`SWCOLOR_1 0 128 0`

* The `R G B` value should between `0` and `255`. 0 being off, 255 brightest.

### DP_SLEEP

You can use `DP_SLEEP` command to make duckyPad go to sleep.

Backlight and screen are turned off.

Press any key to wake it up.

### PREV_PROFILE / NEXT_PROFILE

You can use `PREV_PROFILE` or `NEXT_PROFILE` command to switch to the previous / next profile.

### GOTO_PROFILE

Use this command to jump to a particular profile.

`GOTO_PROFILE 3` // jump to profile #3

### HOLD (experimental)

Holds a key when you press it, and release only when you release it. This command makes duckyPad behave more like a traditional keyboard.

Possible uses include push-to-talk voice chat, or WASD gamepad.

You should only use `HOLD` command on its own, i.e. the script should only have a single line of `HOLD` command and nothing else.

`HOLD` command can be followed by up to 2 keys, they can be character or special keys.

```
HOLD w
```
```
HOLD SHIFT
```
This command is experimental, if you run into any bugs, [let me know](#questions-or-comments)!

### LOOP (experimental)

This command allows you to **assign different actions to the same key**.

You can use it to toggle / cycle through several actions like this:

```
LOOP0:
STRING first action
ENTER

LOOP1:
STRING second action
ENTER

LOOP2:
STRING third action
ENTER
```

* Up to 10 actions are supported (LOOP0 - LOOP9).

* When you press a key, a counter increments, and the script at the corresponding loop is executed.

* This command is not yet supported with test-run on PC app.

* This command is experimental, if you run into any bugs, [let me know](#questions-or-comments)!

## Questions or Comments?

Please feel free to [open an issue](https://github.com/dekuNukem/duckypad/issues), ask in the [official duckyPad discord](https://discord.gg/4sJCBx5), DM me on discord `dekuNukem#6998`, or email `dekuNukem`@`gmail`.`com` for inquires.

-----
# Flipper zero related
-----

## From this gist
https://gist.github.com/methanoliver/efebfe8f4008e167417d4ab96e5e3cac

# DuckyScript commands supported by Flipper's BadUSB

Explanations are only given for commands not present in the original DuckyScript, for everything else refer to [DuckyScript documentation](https://docs.hak5.org/hak5-usb-rubber-ducky/).

## Keys

These mean exactly what one would expect and should need no further explanation.

+ Modifiers: `CTRL`, `CONTROL`, `SHIFT`, `ALT`, `GUI`, `WINDOWS`
+ Combos: `CTRL-ALT`, `CTRL-SHIFT`, `ALT-SHIFT`, `ALT-GUI`, `GUI-SHIFT`
+ Cursor: `DOWNARROW`, `DOWN`, `LEFTARROW`, `LEFT`, `RIGHTARROW`, `RIGHT`, `UPARROW`, `UP`
+ Control and navigation: `ENTER`, `BREAK`, `PAUSE`, `CAPSLOCK`, `DELETE`, `BACKSPACE`, `END`, `ESC`, `ESCAPE`, `HOME`, `INSERT`, `NUMLOCK`, `PAGEUP`, `PAGEDOWN`, `PRINTSCREEN`, `SCROLLOCK`, `SPACE`, `TAB`, `MENU`, `APP`, `SYSRQ`
+ Function: `F1`, `F2`, `F3`, `F4`, `F5`, `F6`, `F7`, `F8`, `F9`, `F10`, `F11`, `F12`

## Input

+ `STRING`
+ `ALTSTRING <string>`, `ALTCODE <string>` -- Not present in DuckyScript, these are the equivalent of `STRING`, as if the string was typed in by holding Alt and entering the unicode code of every character, [as described in Windows documentation](https://support.microsoft.com/en-us/office/insert-ascii-or-unicode-latin-based-symbols-and-characters-d13f58d3-7bcb-44a7-a4d5-972ee12e50e0). This is the way to get around the fact that there are no standard ways to switch input keyboard language and important in parts of the world where default keyboard has no Latin characters on it at all. This only works on Windows.
+ `ALTCHAR <code>` -- Altstring is internally a sequence of `ALTCHAR` invocations.

There is *no* support for `STRINGLN`.

## Structural

+ `REM`
+ `ID <vendor:id>` - Equivalent to certain features of DuckyScript's `ATTACKMODE`. executed in preload phase, sets USB id of the keyboard device. For example, `ID 04d9:1702` is an AJAZZ keyboard.
+ `DELAY`
+ `DEFAULT_DELAY`, `DEFAULTDELAY`
+ `REPEAT`
+ `DUCKY_LANG` - ignored, recognized as a command purely for compatibility with existing scripts.

-----

# Official documentation
https://github.com/DarkFlippers/unleashed-firmware/blob/dev/documentation/file_formats/BadUsbScriptFormat.md

# Command syntax
BadUsb app uses extended Duckyscript syntax. It is compatible with classic USB Rubber Ducky 1.0 scripts, but provides some additional commands and features, such as custom USB ID, ALT+Numpad input method, SYSRQ command and more functional keys.
# Script file format
BadUsb app can execute only text scrips from .txt files, no compilation is required. Both `\n` and `\r\n` line endings are supported. Empty lines are allowed. You can use spaces ore tabs for line indentation.
# Command set
## Comment line
Just a single comment line. All text after REM command will be ignored by interpreter
|Command|Parameters|Notes|
|-|-|-|
|REM|Comment text||

## Delay
Pause script execution by defined time
|Command|Parameters|Notes|
|-|-|-|
|DELAY|Delay value in ms|Single delay|
|DEFAULT_DELAY|Delay value in ms|Add delay before every next command|
|DEFAULTDELAY|Delay value in ms|Same as DEFAULT_DELAY|

## Special keys
|Command|Notes|
|-|-|
|DOWNARROW / DOWN||
|LEFTARROW / LEFT||
|RIGHTARROW / RIGHT||
|UPARROW / UP||
|ENTER||
|DELETE||
|BACKSPACE||
|END||
|HOME||
|ESCAPE / ESC||
|INSERT||
|PAGEUP||
|PAGEDOWN||
|CAPSLOCK||
|NUMLOCK||
|SCROLLLOCK||
|PRINTSCREEN||
|BREAK|Pause/Break key|
|PAUSE|Pause/Break key|
|SPACE||
|TAB||
|MENU|Context menu key|
|APP|Same as MENU|
|Fx|F1-F12 keys|

## Modifier keys
Can be combined with special key command or single character
|Command|Notes|
|-|-|
|CONTROL / CTRL||
|SHIFT||
|ALT||
|WINDOWS / GUI||
|CTRL-ALT|CTRL+ALT|
|CTRL-SHIFT|CTRL+SHIFT|
|ALT-SHIFT|ALT+SHIFT|
|ALT-GUI|ALT+WIN|
|GUI-SHIFT|WIN+SHIFT|
## String
|Command|Parameters|Notes|
|-|-|-|
|STRING|Text string|Print text string|
## Repeat
|Command|Parameters|Notes|
|-|-|-|
|REPEAT|Number of additional repeats|Repeat previous command|
## ALT+Numpad input
On Windows and some Linux systems you can print character by pressing ALT key and entering its code on numpad
|Command|Parameters|Notes|
|-|-|-|
|ALTCHAR|Character code|Print single character|
|ALTSTRING|Text string|Print text string using ALT+Numpad method|
|ALTCODE|Text string|Same as ALTSTRING, presents in some Duckyscript implementations|
## SysRq
Send [SysRq command](https://en.wikipedia.org/wiki/Magic_SysRq_key)
|Command|Parameters|Notes|
|-|-|-|
|SYSRQ|Single character||
## USB device ID
You can set custom ID of Flipper USB HID device. ID command should be in the **first line** of script, it is executed before script run.

|Command|Parameters|Notes|
|-|-|-|
|ID|VID:PID Manufacturer:Product||

Example:
`ID 1234:abcd Flipper Devices:Flipper Zero`

VID and PID are hex codes and are mandatory, Manufacturer and Product are text strings and are optional.

-----

## DTK user script downloader
https://github.com/cribb-it/DTKDownloader
The DTK(ducktoolkit user script https://ducktoolkit.com/userscripts) downloader doesn't work for me. So if you get it to work send in a PR and I will add the resulting dump here.

-----

# Helpful hints

Here are a bunch of cheatsheets for use in building your scripts [here](https://github.com/FalsePhilosopher/BadUSB-Playground/tree/main/Misc/Cheat_Sheets)

Shorten your payloads as much as possible by stringing multiple commands together with variables like `&&` and `;;`, read more into each OS/shell you are targeting and how to achieve this.

RTFM for CMD
https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd

RTFM for powershell
https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/04-pipelines?view=powershell-7.3

Other ducky scripts can be found here
http://www.theatomheart.net/post/rubber-ducky-payloads/
