# InlineExecute-Assembly https://github.com/anthemtotheego/InlineExecute-Assembly

InlineExecute-Assembly is a proof of concept Beacon Object File (BOF) that allows security professionals to perform in process .NET assembly execution as an alternative to Cobalt Strikes traditional fork and run execute-assembly module. InlineExecute-Assembly will execute any assembly with the entry point of  ```Main(string[] args)``` or ```Main()```. This should allow you to run most released tooling without any prior modification needed. 

The BOF will automatically determine which Common Language Runtime (CLR) is needed to be loaded into the process for your assembly (v2.0.50727 or v4.0.30319) prior to execution and in most cases, should exist gracefully if any issues arise. The BOF also supports several flags which allow the operator to dictate several behaviors prior to .NET execution which include, disabling AMSI via in memory patching, disabling and restoring ETW via in memory patching, customization of the CLR App Domain name to be created, whether to create and direct console output of your assembly to a named pipe or mailslot, and allows the operator to switch the default entry point of Main(string[] args) to Main().  More details on usage, use cases, and possible detections can be found below and https://securityintelligence.com/posts/net-execution-inlineexecute-assembly/.

Lastly the advantage of executing our .NET assemblies in the same process as our beacon implant is that we avoid the default behavior of Cobalt Strike's execute-assembly module which creates a new process to then load/inject the CLR/.NET assembly. However, other opsec considerations still exist, for example, does the process we are executing within normally load the CLR or does the .NET assembly we are executing have any known signatures?  Therefore, the disadvantage is that if something does get detected and killed, for example by AMSI, your beacon is also killed. 

# Subject References

This tool wouldn't exist without being able to piggyback off some really great research, tools, and code already published by members of the security community. So thank you. Lastly, if you feel anyone has been left out below, please let me know and I will be sure to get them added.

- HostingCLR - [here](https://github.com/etormadiv/HostingCLR) - CLR/Executing assembly logic
- Dotnet-Loader-Shellcode - (by [@modexpblog](https://twitter.com/modexpblog)) - [here](https://modexp.wordpress.com/2019/05/10/dotnet-loader-shellcode/) - All around great research including on COM Interfaces for executing .NET in C -> Real MVP
- Donut - (by [@TheRealWover](https://twitter.com/TheRealWover) and [@modexpblog](https://twitter.com/modexpblog)) - [here](https://github.com/TheWover/donut) - COM Interfaces Header
- Memory Patching AMSI Bypass - (by [@_RastaMouse](https://twitter.com/_RastaMouse)) - [here](https://rastamouse.me/memory-patching-amsi-bypass/) - AMSI memory patching research
- Metasploit-Execute-Assembly - (by [@b4rtik](https://twitter.com/b4rtik)) - [here](https://github.com/b4rtik/metasploit-execute-assembly) - Modified AMSI patching and used find .NET version function
- ExecuteAssembly - (by [@med0x2e](https://twitter.com/med0x2e))- [here](https://github.com/med0x2e/ExecuteAssembly) - Modified aggressor script
- Hiding Your .NET ETW - (by [@_xpn_](https://twitter.com/_xpn_)) - [here](https://www.mdsec.co.uk/2020/03/hiding-your-net-etw/) - Great ETW research
- ETW BOF - (by [@ajpc500](https://twitter.com/ajpc500))- [here](https://github.com/ajpc500/BOFs/tree/main/ETW) - Modified ETW patching
- ExecuteAssembly_Mailslot - (by [@N4k3dTurtl3](https://twitter.com/N4k3dTurtl3))- [here](https://github.com/N4kedTurtle/ExecuteAssembly_Mailslot) - Modified using mailslots for console redirection
- [@freefirex2](https://twitter.com/freefirex2) - Was kind enough to share some good BOF inner workings and gotcha's.

## Getting Started

1. Copy the inlineExecute-Assembly folder with all of its contents to a system you plan to connect with via the Cobalt Strike GUI application.
2. Load in the inlineExecute-Assembly.cna Aggressor script
3. Run inlineExecute-Assembly --dotnetassembly /path/to/assembly.exe for most basic execution (see use cases below for specific flag examples)

### Build Your Own

Run the below command inside the src directory via x64 Native Tools Command Prompt for VS 2019
```
cl.exe /c inlineExecute-Assembly.c /GS- /FoinlineExecute-Assemblyx64.o
```
Run the below command inside the src directory via x86 Native Tools Command Prompt for VS 2019
```
cl.exe /c inlineExecute-Assembly.c /GS- /FoinlineExecute-Assemblyx86.o
```

### Flags

```
--dotnetassembly        Directory path to your assembly **required**
--assemblyargs          Assembly arguments to pass
--appdomain             Change default name of AppDomain sent (default value is totesLegit and is set via the included aggressor script) *Domain always unloaded*
--amsi                  Attempts to disable AMSI via in memory patching (If successful AMSI will be disabled for the entire life of process)
--etw                   Attempts to disable ETW via in memory patching (If successful ETW will be disabled for the entire life of process unless reverted)
--revertetw             Attempts to disable ETW via in memory patching and then repatches it back to original state
--pipe                  Change default name of named pipe (default value is totesLegit and is set via the included aggressor script)
--mailslot              Switches to using mailslots to redirect console output. Changes default name of mailslot (If left blank, default value is totesLegit and is set via the included aggressor script)
--main                  Changes entry point to Main() (default value is Main(string[] args))

```
### Use Case

> *Execute .NET assembly*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe
```

### Use Case

> *Execute .NET assembly with arguments*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --assemblyargs AntiVirus AppLocker
```

### Use Case

> *Execute .NET assembly with arguments and disable AMSI*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --assemblyargs AntiVirus AppLocker --amsi
```

### Use Case

> *Execute .NET assembly with arguments and disable ETW*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --assemblyargs AntiVirus AppLocker --etw
```

### Use Case

> *Execute .NET assembly with arguments and redirect output via mailslots instead of the default named pipe*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --mailslot
```

### Use Case

> *Execute .NET assembly with arguments and change the default named pipe name set in the aggressor script*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --pipe forRealLegit
```

### Use Case

> *Execute .NET assembly and change the default app domain set in the aggressor script*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --appdomain forRealLegit
```

### Use Case

> *Execute .NET assembly with Main() entry point instead of the default Main(string[] args)*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/simpleMain.exe --main
```

### Use Case

> *Go HAM*

### Syntax

```
beacon> inlineExecute-Assembly --dotnetassembly /root/Desktop/Seatbelt.exe --assemblyargs AntiVirus AppLocker --amsi --etw --appdomain forRealLegit --mailslot forRealLegit
```

## Caveats

1.	While I have tried to make this as stable as possible, there are no guarantees things will never crash and beacons won’t die. We don’t have the added luxury of fork and run where if something goes wrong our beacon lives. This is the tradeoff with BOFs.  With that said, I can’t stress how important it is that you test your assemblies beforehand to make sure they will work properly with the tool. 
2. Since the BOF is executed in process and takes over the beacon while running, this should be taken into account before being used for long running assemblies. If you choose to run something that will take a long time to get back results, your beacon will not be active to run more commands till the results come back and your assembly finishes running.  This also doesn’t adhere to sleep set.  For example, if your sleep is set at 10 minutes and you run the BOF, you will get results back as soon as the BOF finishes executing.
3.	Unless modification is done to tools that load PE’s in memory (e.g., SafetyKatz), these will most likely kill your beacon.  Many of these tools work fine with execute assembly because they are able to send their console output from the sacrificial process before exiting.  When they exit via our in process BOF, they kill our process, which kills our beacon.  These can be modified to work but I would advise running these types of assemblies via execute assembly since other non-OPSEC friendly things could be loaded into your process that don’t get removed. 
4.	If your assembly uses Environment.Exit this will need to be removed as it will kill the process and beacon.  
5.	Named pipes and mail slots need to be unique.  If you don’t receive data back and your beacon is still alive, the issue is most likely you need to select a different named pipe or mail slot name.

 
## Detection

Some detection and mitigation strategies that could be used:

1. Uses PAGE_EXECUTE_READWRITE when performing AMSI and ETW memory patching. This was done on purpose and should be a red flag as very few programs have memory ranges with the memory protection of PAGE_EXECUTE_READWRITE.
2. Default name of named pipe created is totesLegit. This was done on purpose and signature detections could be used to flag this.
3. Default name of mailslot created is totesLegit. This was done on purpose and signature detections could be used to flag this.
4. Default name of AppDomain loaded is totesLegit. This was done on purpose and signature detections could be used to flag this.
5. Good tips on detecting malicious use of .NET (by [@bohops](https://twitter.com/bohops)) [here](https://bohops.com/2021/03/16/investigating-net-clr-usage-log-tampering-techniques-for-edr-evasion/), (by F-Secure) [here](https://blog.f-secure.com/detecting-malicious-use-of-net-part-1/), and [here](https://blog.f-secure.com/detecting-malicious-use-of-net-part-2/)
6. Looking for .NET CLR loading into suspicious processes, such as unmanaged processes which should never have the CLR loaded.
7. Event Tracing [here](https://docs.microsoft.com/en-us/windows/win32/etw/about-event-tracing)
9. Looking for other known Cobalt Strike Beacon IOC's or C2 egress/communication IOC's. 
