# Setup Testing Environment for log4Shell Vulnerability (CVE-2021-44228)

Original repo:https://github.com/vidrez/test-log4shell

**The execution of this script was tested only on Ubuntu Server 22.04**

The script will install the following applications:

* Minecraft Server 1.18
* Apache Solr 8.11.0
* A Vulnerable Proof-of-concept (POC) Web App made by [kozmer](https://github.com/kozmer/log4j-shell-poc)
* A Vulnerable Proof-of-concept (POC) Java application to see how log4j vulnerability + java unsafe deserialization works [vidrez/log4j-deserialization-rce-POC](https://github.com/vidrez/log4j-deserialization-rce-POC)

And the following tools:

* [pimps/JNDI-Exploit-Kit](https://github.com/pimps/JNDI-Exploit-Kit)
* [pimps/ysoserial-modified](https://github.com/pimps/ysoserial-modified)

## Instructions

Add executable permissions to the script:

```
sudo chmod +x setup-log4Shell.sh
```

Execute the script with root privileges:

```
sudo ./setup-log4Shell.sh
```

**The addresses of the installed applications will be shown at the end of the script**

## Autorestart (optional)

After the setup is completed inside the *setup* folder will be generated an *autostart.sh* script file that you can use to easily restart the docker web app and the minecraft server on system startup/reboot. Also you can add the *autostart.sh* script as a reboot cron by:

1. Executing `sudo crontab -e`
2. Adding at the end of the file the line `@reboot /path/to/autostart.sh` changing '/path/to/autostart.sh' with the actual path to the autostart script

## Disclaimer

This script was written only to be able to quickly set up a test environment for the Log4Shell vulnerability (CVE-2021-44228). **Do not use this script on a production server**

![](./meme.jpg "meme")
