### DTK_Downloader

The DTK(ducktoolkit user script https://ducktoolkit.com/userscripts) downloader doesn't work. So if you get it to work send in a PR and I will add the resulting dump here.

# Writing duckyScript

https://github.com/dekuNukem/duckyPad

[Get duckyPad](https://www.tindie.com/products/21984/) | [Official Discord](https://discord.gg/4sJCBx5) | [Getting Started](getting_started.md) | [Table of Contents](#table-of-contents)

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

## Table of Contents

[Main page](README.md)

[Getting Started Guide](getting_started.md)

[Kit Assembly Guide](kit_assembly_guide.md)

[Using duckyScript](duckyscript_info.md)

[Common issues / Troubleshooting](troubleshooting.md)

[Firmware Updates and Version History](firmware_updates_and_version_history.md)

[Make Your Own Keymap](./keymap_instructions.md)

[Manual Setup](./manual_setup.md)

[Build a duckyPad Yourself](build_it_yourself.md)

[Kickstarter Backer Acknowledgments](kickstarter_backers.md)

## Questions or Comments?

Please feel free to [open an issue](https://github.com/dekuNukem/duckypad/issues), ask in the [official duckyPad discord](https://discord.gg/4sJCBx5), DM me on discord `dekuNukem#6998`, or email `dekuNukem`@`gmail`.`com` for inquires.
