# LOG4SHELL

Original repo:https://github.com/ishan-saha/LOG4SHELL

This is a simple automated Log4j exploit script written in python and using older version of java binaries.

## Usage

- AttackerIP - Your public IP where the lister is waiting for connection
- TargetURL - IP/URL which will be tested
- WebServerPort - Port to initiate the python based web server where the ```Exploit.class``` will be present
- Lport - Netcat listner port

## Setup

The  **setup.sh**  file should be run to install the requirements. Run the following:
>chmod +x setup.sh 
>
>./setup.sh

This file simply downloads the older version of JDK and extracts it. Secondly, it installs ```colorama``` and ```requests``` python3 package

