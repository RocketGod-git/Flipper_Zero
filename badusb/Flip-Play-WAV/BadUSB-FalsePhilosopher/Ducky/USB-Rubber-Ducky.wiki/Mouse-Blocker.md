<h1>Mouse Blocker</h1>
<pre>REM this program disables the primary mouse on Windows 10 home. I don't know if this works on other versions. Uses the run box to open main.cpl, then
REM disables the mouse. Might need to change the number of times to press tab for other computers.</pre>
<h2>Code for Windows 10 Home</h2>

<pre><code>REM Mouse disable
REM Open mouse properties
DELAY 100
GUI r
DELAY 200
STRING main.cpl
DELAY 100
ENTER
DELAY 500
REM disable mouse
TAB
DELAY 100
TAB
DELAY 100
ENTER
DELAY 200
ENTER
REM Close window
DELAY 100
TAB
DELAY 50
TAB
DELAY 50
TAB
DELAY 50
TAB
DELAY 50
TAB
DELAY 50
ENTER</pre></code>