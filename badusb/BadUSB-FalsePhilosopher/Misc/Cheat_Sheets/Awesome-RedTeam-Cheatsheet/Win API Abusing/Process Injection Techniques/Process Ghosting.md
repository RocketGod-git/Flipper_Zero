**I - Introduction

Just like other **Process Injection** techniques, Process Ghosting is a technique to bypass AVs and endpoints, 
This technique is recent and remains similar to previous techniques like Process **Doppelganging** and **Herpaderping**.

**Process:** 

![](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt930f0b0e46dd0d53/60aeb7b447ebc9669e1e8174/4-blog-process-ghosting.png)





**II - step :**

- **1:** **Create** a file
```c
h = CreateFile()
```
- **2:** Place the file in a Delete-Pending State using `NtSetInformationFile(FileDispositionInformation)`.
you can also use `FILE_DELETE_ON_CLOSE`.
- **3:** **Write** the payload to the file. The contents are not retained because the file is already pending deletion. The pending-delete state also blocks attempts to open an external file.
```c
WriteFile(h)
```
- **4:** **Create** an image section for the file.
- **5:** **Close** the descriptor waiting to be deleted by **deleting the file**.
- **6:** **Create a process** using the image section.
- **7:** **Assign** process arguments and environment variables.
- **8:** **Create a thread** to run in the process.
```c
CreateThreadEx() -> CreateProcessEx()
```

we can exploit the proc ghosting via [kinghamlet](https://github.com/IkerSaint/KingHamlet) which has the possibility to encrypt in AES, we can also exploit it with the [traditional technique](https://github.com/hasherezade/process_ghosting)

![image](https://user-images.githubusercontent.com/75935486/151682211-d276ce18-afa8-43fb-bddf-23462af9a0a7.png)



Function CreateFile() :

![image](https://user-images.githubusercontent.com/75935486/151682187-2b675d9c-5e4e-4cd1-a215-0cbce12efc13.png)

Delete Pending State :

![image](https://user-images.githubusercontent.com/75935486/151682372-0ae10ef6-f51d-48fb-ba92-1b728881713f.png)



References :
- https://github.com/IkerSaint/KingHamlet
- https://www.elastic.co/fr/blog/process-ghosting-a-new-executable-image-tampering-attack
- https://github.com/hasherezade/process_ghosting
