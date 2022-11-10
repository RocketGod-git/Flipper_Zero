## OG Repo
https://github.com/m0nad/awesome-privilege-escalation

# Awesome Privilege Escalation
A curated list of awesome privilege escalation

## Table of Contents

* [Linux](#linux)
    * [Escape restricted shells](#escape-restricted-shells)
    * [SUDO and SUID](#sudo-and-suid)
    * [Capabilities](#capabilities)
    * [Tools](#tools)
        * [Find CVEs](#find-cves)
    * [Chkrootkit](#chkrootkit)
    * [NFS](#nfs)
    * [Presentations](#presentations)
* [Windows](#windows)
    * [DLL Hijacking](#dll-hijacking)
    * [Potato](#potato)
    * [Unquoted services with spaces](#unquoted-services-with-spaces)
    * [Groups.xml](#groupsxml)
    * [Tools](#tools-1)
    * [Presentations](#presentations-1)
* [Linux and Windows](#linux-and-windows)
* [Docker](#docker)
    * [Tools](#tools-2)
    * [Presentations](#presentations-2)
* [Cloud](#cloud)
   * [AWS](#aws)
   * [GCP](#gcp)

## Linux
 - [A guide to Linux Privilege Escalation](https://payatu.com/guide-linux-privilege-escalation/)
 - [Attack and Defend: LinuxPrivilege Escalation Techniques of 2016](https://www.sans.org/reading-room/whitepapers/linux/attack-defend-linux-privilege-escalation-techniques-2016-37562): This paper will examine Linux privilege escalation techniques used throughout 2016 in detail, highlighting how these techniques work and how adversaries are using them.
 - [Back To The Future: Unix Wildcards Gone Wild](https://www.defensecode.com/public/DefenseCode_Unix_WildCards_Gone_Wild.txt): This article will cover one interesting old-school Unix hacking technique, that will still work in 2013.
 - [Basic Linux Privilege Escalation](https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/): by g0tmi1k
 - [Enumeration is the Key](https://medium.com/basic-linux-privilege-escalation/basic-linux-privilege-escalation-966de11f9997): by Marcos Tolosa
 - [Hackers Hut](https://www.win.tue.nl/~aeb/linux/hh/hh.html): Some random hacking hints, mainly from a Linux point of view.
 - [Hacking Linux Part I: Privilege Escalation](http://www.dankalia.com/tutor/01005/0100501004.htm)
 - [How privileges work in operating systems?](https://www.future-processing.pl/blog/privilege-escalation/)
 - [Linux elevation of privileges ToC](https://guif.re/linuxeop)
 - [Linux - Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md): Methodology from PayloadsAllTheThings 
 - [Linux Privilege Escalation](https://percussiveelbow.github.io/linux-privesc/): an introduction to Linux escalation techniques, mainly focusing on file/process permissions, but along with some other stuff too.
 - [Linux Privilege Escalation](https://github.com/lamontns/pentest/blob/master/privilege-escalation/linux-privilege-escalation.md): Linux Privilege Escalation by lamontns.
 - [Linux Privilege Escalation](https://book.hacktricks.xyz/linux-unix/privilege-escalation): by HackTricks
 - [Linux Privilege Escalation via Dynamically Linked Shared Object Library](https://www.contextis.com/en/blog/linux-privilege-escalation-via-dynamically-linked-shared-object-library): How RPATH and Weak File Permissions can lead to a system compromise.
 - [Local Linux Enumeration & Privilege Escalation Cheatsheet](https://www.rebootuser.com/?p=1623): a few Linux commands that may come in useful when trying to escalate privileges on a target system.
 - [Local Linux Enumeration & Privilege Escalation](https://hackingandsecurity.blogspot.com/2016/05/local-linux-enumeration-privilege.html): a few Linux commands that may come in useful when trying to escalate privileges on a target system.
 - [Local Linux privilege escalation overview](https://myexperiments.io/linux-privilege-escalation.html): This article will give an overview of the basic Linux privilege escalation techniques. It separates the local Linux privilege escalation in different scopes: kernel, process, mining credentials, sudo, cron, NFS, and file permission.
 - [Penetration-Testing-Grimoire/Privilege Escalation/linux.md](https://github.com/weaknetlabs/Penetration-Testing-Grimoire/blob/master/Privilege%20Escalation/linux.md)
 - [PENETRATION TESTING PRACTICE LAB - VULNERABLE APPS / SYSTEMS](https://www.amanhardikar.com/mindmaps/Practice.html)
 - [Pentest Book - Privilege Escalation](https://chryzsh.gitbooks.io/pentestbook/privilege_escalation_-_linux.html): common Linux privilege escalation techniques.
 - [POST CATEGORY : Privilege Escalation](https://www.hackingarticles.in/category/privilege-escalation/): Privilege escalation post category in Raj Chandel's Blog.
 - [Privilege Escalation Cheatsheet (Vulnhub)](https://github.com/Ignitetechnologies/Privilege-Escalation): This cheasheet is aimed at the CTF Players and Beginners to help them understand the fundamentals of Privilege Escalation with examples.
 - [Privilege escalation: Linux](https://vulp3cula.gitbook.io/hackers-grimoire/post-exploitation/privesc-linux)
 - [Privilege Escalation & Post-Exploitation](https://github.com/rmusser01/Infosec_Reference/blob/master/Draft/PrivescPostEx.md)
 - [Reach the root! How to gain privileges in Linux?](https://hackmag.com/security/reach-the-root/)
 - [TTY Input Pushback Privilege Escalation](https://www.halfdog.net/Security/2012/TtyPushbackPrivilegeEscalation/): When user working as root switches to another user with su and happens to execute the pushback program as that user, the tty input data pushed back is executed in the shell and context of user root.
 - [Understanding Privilege Escalation](http://www.admin-magazine.com/Articles/Understanding-Privilege-Escalation): Some techniques malicious users employ to escalate their privileges on a Linux system.

### Escape restricted shells
 - [Breaking out of rbash using scp](http://pentestmonkey.net/blog/rbash-scp)
 - [Escaping from Restricted Shell and Gaining Root Access to SolarWinds Log & Event Manager (SIEM) Product](https://pentest.blog/unexpected-journey-4-escaping-from-restricted-shell-and-gaining-root-access-to-solarwinds-log-event-manager-siem-product/)
 - [Escaping Restricted Linux Shells](https://pen-testing.sans.org/blog/pen-testing/2012/06/06/escaping-restricted-linux-shells): Resource for penetration testers to assist them when confronted with a restricted shell.
 - [Linux Restricted Shell Bypass](https://www.exploit-db.com/docs/english/44592-linux-restricted-shell-bypass-guide.pdf)
 - [Restricted Linux Shell Escaping Techniques](https://fireshellsecurity.team/restricted-linux-shell-escaping-techniques/): The focus of this article is on discussing and summarizing different techniques to escape common Linux restricted shells and also simple recommendations for administrators to protect against it.

### SUDO and SUID
 - [Abusing SUDO](https://touhidshaikh.com/blog/?p=790): Some of the binary which helps you to escalate privilege using the sudo command.
 - [Gaining a Root shell using MySQL User Defined Functions and SETUID Binaries](https://infamoussyn.wordpress.com/2014/07/11/gaining-a-root-shell-using-mysql-user-defined-functions-and-setuid-binaries/): How a MySQL User Defined Function (UDF) and a SETUID binary can be used to elevate user privilege to a root shell.
 - [GTFOBins](https://gtfobins.github.io/): GTFOBins is a curated list of Unix binaries that can be exploited by an attacker to bypass local security restrictions.
 - [How I got root with Sudo](https://www.securusglobal.com/community/2014/03/17/how-i-got-root-with-sudo/)
 - [Sudo (LD_PRELOAD)](https://touhidshaikh.com/blog/?p=827): Privilege Escalation from an LD_PRELOAD environment variable. 

### Capabilities
 - [An Interesting Privilege Escalation vector (getcap/setcap)](https://nxnjz.net/2018/08/an-interesting-privilege-escalation-vector-getcap/)
 - [Capabilities](https://wiki.archlinux.org/index.php/Capabilities)
 - [Exploiting capabilities](http://blog.sevagas.com/IMG/pdf/exploiting_capabilities_the_dark_side.pdf): Parcel root power, the dark side of capabilities
 - [getcap, setcap and file capabilities](https://www.insecure.ws/linux/getcap_setcap.html)
 - [Spicing up your own access with capabilities](https://www.redpill-linpro.com/sysadvent/2016/12/06/spicing-up-your-access.html)

### Tools
 - [AutoLocalPrivilegeEscalation](https://github.com/ngalongc/AutoLocalPrivilegeEscalation): An automated script that download potential exploit for linux kernel from exploitdb, and compile them automatically.
 - [BeRoot](https://github.com/AlessandroZ/BeRoot): BeRoot Project is a post exploitation tool to check common misconfigurations to find a way to escalate our privilege.
exploits.
 - [exploit-suggester](https://github.com/pentestmonkey/exploit-suggester): This tool reads the output of “showrev -p” on Solaris machines and outputs a list of exploits that you might want to try.
is intended to be executed locally on a Linux box to enumerate basic system info and search for common privilege escalation vectors such as word writable files, misconfigurations, clear-text password and applicable
 - [kernelpop](https://github.com/spencerdodd/kernelpop): kernelpop is a framework for performing automated kernel vulnerability enumeration and exploitation.
 - [LES](https://github.com/mzet-/linux-exploit-suggester): LES: Linux privilege escalation auditing tool
 - [LinEnum](https://github.com/rebootuser/LinEnum): Scripted local Linux enumeration & privilege escalation checks
 - [LinPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS): Linux Privilege Escalation Awesome Script
 - [Linux Exploit Suggester 2](https://github.com/jondonas/linux-exploit-suggester-2): Next-generation exploit suggester based on Linux_Exploit_Suggester
 - [Linux_Exploit_Suggester](https://github.com/InteliSecureLabs/Linux_Exploit_Suggester): Linux Exploit Suggester; based on operating system release number.
 - [linux-kernel-exploits](https://github.com/SecWiki/linux-kernel-exploits)
 - [Linuxprivchecker.py](https://github.com/sleventyeleven/linuxprivchecker): This script is intended to be executed locally on a Linux box to enumerate basic system info and search for common privilege escalation vectors such as world writable files, misconfigurations, clear-text passwords and applicable exploits.
 - [Linux Privilege Escalation Check Script](https://github.com/linted/linuxprivchecker): Originally forked from the linuxprivchecker.py (Mike Czumak), this script is intended to be executed locally on a Linux box to enumerate basic system info and search for common privilege escalation vectors such as word writable files, misconfigurations, clear-text password and applicable exploits.
 - [linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration): Linux enumeration tools for pentesting and CTFs
 - [linux-soft-exploit-suggester](https://github.com/belane/linux-soft-exploit-suggester): linux-soft-exploit-suggester finds exploits for all vulnerable software in a system helping with the privilege escalation.
 - [PrivEsc](https://github.com/1N3/PrivEsc): A collection of Windows, Linux and MySQL privilege escalation scripts and exploits.
 - [pspy](https://github.com/DominicBreuker/pspy): unprivileged Linux process snooping
 - [traitor](https://github.com/liamg/traitor): Automatically exploit low-hanging fruit to pop a root shell. Linux privilege escalation made easy!
 - [unix-privesc-check](https://github.com/pentestmonkey/unix-privesc-check): Shell script to check for simple privilege escalation vectors on Unix systems
 - [Unix-Privilege-Escalation-Exploits-Pack](https://github.com/Kabot/Unix-Privilege-Escalation-Exploits-Pack): Exploits for getting local root on Linux, BSD, AIX, HP-UX, Solaris, RHEL, SUSE etc.
 - [uptux](https://github.com/initstring/uptux): Specialized privilege escalation checks for Linux systems.

#### Find CVEs
 - [active-cve-check](https://github.com/davbo/active-cve-check): Checks a list of packages against the "active" (not yet patched) CVE's as listed in the Ubuntu CVE Tracker.
 - [Arch-Audit](https://www.2daygeek.com/arch-audit-a-tool-to-check-vulnerable-packages-in-arch-linux/): A tool to check vulnerable packages in Arch Linux.
 - [cve-check-tool](https://github.com/clearlinux/cve-check-tool): Original Automated CVE Checking Tool.
 - [LPVS](https://github.com/lwindolf/lpvs): Linux Package Vulnerability Scanner for CentOS and Ubuntu.

### Chkrootkit
 - [Local root exploit in Chkrootkit](https://lepetithacker.wordpress.com/2017/04/30/local-root-exploit-in-chkrootkit/): Security researchers have found an local exploit for Chkrootkit 0.49 who allow to a simple user to make root’s commands.

### NFS
 - [Exploiting a Mis-Configured NFS Share](https://www.computersecuritystudent.com/SECURITY_TOOLS/METASPLOITABLE/EXPLOIT/lesson4/index.html)
 - [Linux Privilege Escalation using Misconfigured NFS](https://www.hackingarticles.in/linux-privilege-escalation-using-misconfigured-nfs/): How to exploit a misconfigured NFS share to gain root access to a remote host machine.
 - [NFS weak permissions](https://touhidshaikh.com/blog/?p=788)
 - [Linux Privilege Escalation using weak NFS permissions](https://haiderm.com/linux-privilege-escalation-using-weak-nfs-permissions/): t Linux Privilege Escalation using weak NFS permissions in “/etc/exports”. by Haider Mahmood

### Presentations
 - [Linux privilege escalation for fun, profit, and all around mischief](https://www.irongeek.com/i.php?page=videos/bsidesaugusta2016/its-too-funky-in-here04-linux-privilege-escalation-for-fun-profit-and-all-around-mischief-jake-williams): Examine opportunities for privilege escalation that can vault you from zero to hero in a few easy steps.
 - [Linux Privilege Escalation - Tradecraft Security Weekly #22](https://www.youtube.com/watch?v=oYHAi0cgur4): Methodology for performing various privilege escalation techniques against Linux-based systems.
 - [Privilege Escalation FTW](https://www.youtube.com/watch?v=yXe4X-AIbps): Demonstrate various privilege escalation techniques that are possible primarily due to misconfigurations.

## Windows
 - [awesome-windows-security](https://github.com/chryzsh/awesome-windows-security#-privilege-escalation)
 - [LOLBAS](https://lolbas-project.github.io/): Living Off The Land Binaries and Scripts (and also Libraries)
 - [OSCP Windows PrivEsc - Part 1](https://butter0verflow.github.io/oscp/OSCP-WindowsPrivEsc-Part1/)
 - [Privilege Escalation](https://www.offensive-security.com/metasploit-unleashed/privilege-escalation/): There are also various other (local) exploits that can be used to also escalate privileges.
 - [Privilege Escalation Windows](https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_windows.html)
 - [Privilege escalation: Windows](https://vulp3cula.gitbook.io/hackers-grimoire/post-exploitation/privesc-windows)
 - [Windows elevation of privileges ToC](https://guif.re/windowseop)
 - [Windows Local Privilege Escalation](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation): by HackTricks
 - [Windows Post Gather Modules](https://www.offensive-security.com/metasploit-unleashed/windows-post-gather-modules/): Metasploit offers a number of post exploitation modules that allow for further information gathering on your target network.
 - [Windows Priv Esc](https://www.sock-raw.org/wiki/doku.php/windows_priv_esc)
 - [Windows Privilege Escalation Fundamentals](https://www.fuzzysecurity.com/tutorials/16.html)
 - [Windows Privilege Escalation Guide](https://www.absolomb.com/2018-01-26-Windows-Privilege-Escalation-Guide/)
 - [Windows-Privilege-Escalation](https://github.com/frizb/Windows-Privilege-Escalation): Step-by-step windows privlege escalation methodology.
 - [Windows-Privilege-Escalation-Resources](https://github.com/Gr1mmie/Windows-Privilege-Escalation-Resources): Compilation of Resources from TCM's Windows Priv Esc Udemy Course. By Gr1mmie
 - [Windows - Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
 - [Windows Privilege Escalation](http://www.bhafsec.com/wiki/index.php/Windows_Privilege_Escalation)
 - [Windows Privilege Escalation](https://github.com/lamontns/pentest/blob/master/privilege-escalation/windows-privilege-escalation.md): Windows Privilege Escalation by lamontns.
 - [Windows Privilege Escalations](https://www.exploit-db.com/docs/46131)


### DLL Hijacking
 - [DLL Hijacking](https://ired.team/offensive-security/privilege-escalation/t1038-dll-hijacking): DLL Search Order Hijacking for privilege escalation, code execution, etc. by Red Teaming Experiments
 - [DLL Hijacking](https://pentestlab.blog/2017/03/27/dll-hijacking/): by PentestLab
 - [DLL Search Order Hijacking](https://attack.mitre.org/techniques/T1038/): by MITRE
 - [PrivEsc: DLL Hijacking](https://web.archive.org/web/20210805085547/https://gracefulsecurity.com/privesc-dll-hijacking/): by GracefulSecurity
 - [Windows Privilege Escalation via DLL Hijacking](https://web.archive.org/web/20200215215536/https://hacknpentest.com/windows-privilege-escalation-dll-hijacking/): Crystal-clear view on one of the most used techniques for privilege escalation by the Threat Actors. by HacknPentest


### Potato
 - [Hot Potato](https://pentestlab.blog/2017/04/13/hot-potato/): Hot potato is the code name of a Windows privilege escalation technique that was discovered by Stephen Breen. This technique is actually a combination of two known windows issues  like NBNS spoofing and NTLM relay with the implementation of a fake WPAD proxy server which is running locally on the target host.
 - [Hot Potato](https://securityonline.info/hot-potato-windows-privilege-escalation-metasploit-powershellhot-potato-windows-privilege-escalation/): Windows 7, 8, 10, Server 2008, Server 2012 Privilege Escalation in Metasploit & PowerShell.
 - [Hot Potato – Windows Privilege Escalation](https://foxglovesecurity.com/2016/01/16/hot-potato/): Privilege Escalation on Windows 7, 8, 10, Server 2008, Server 2012 … and a new network attack.
 - [Juicy Potato (abusing the golden privileges)](https://ohpe.it/juicy-potato/)
 - [No more JuicyPotato? Old story, welcome RoguePotato!](https://decoder.cloud/2020/05/11/no-more-juicypotato-old-story-welcome-roguepotato/): by decoder_it and splinter_code/antonioCoco
 - [Remote Potato](https://pentestlab.blog/2021/05/04/remote-potato-from-domain-user-to-enterprise-admin/): Remote Potato – From Domain User to Enterprise Admin
 - [Rotten Potato – Privilege Escalation from Service Accounts to SYSTEM](https://foxglovesecurity.com/2016/09/26/rotten-potato-privilege-escalation-from-service-accounts-to-system/)

### Unquoted services with spaces
 - [Practical Guide to exploiting the unquoted service path vulnerability in Windows](https://trustfoundry.net/practical-guide-to-exploiting-the-unquoted-service-path-vulnerability-in-windows/)
 - [PrivEsc: Unquoted Service Path](https://web.archive.org/web/20210731080629/https://gracefulsecurity.com/privesc-unquoted-service-path/)
 - [Unquoted Service Path](https://pentestlab.blog/2017/03/09/unquoted-service-path/)
 - [UNQUOTED SERVICE PATHS](https://web.archive.org/web/20210421085608/https://www.commonexploits.com/unquoted-service-paths/)
 - [Windows Privilege Escalation — Part 1 (Unquoted Service Path)](https://medium.com/@SumitVerma101/windows-privilege-escalation-part-1-unquoted-service-path-c7a011a8d8ae)
 - [Windows Privilege Escalation – Unquoted Services](https://web.archive.org/web/20210616195939/https://www.ethicalhacker.net/community/windows-privilege-escalation-unquoted-services/)
 - [Windows Privilege Escalation via Unquoted Service Paths](https://hausec.com/2018/10/05/windows-privilege-escalation-via-unquoted-service-paths/)

### Groups.xml
 - [Finding Passwords in SYSVOL & Exploiting Group Policy Preferences](https://adsecurity.org/?p=2288)
 - [gpp-decrypt Package Description](https://tools.kali.org/password-attacks/gpp-decrypt): A simple ruby script that will decrypt a given GPP encrypted string.

### PrintNightmare
 - [Universal Privilege Escalation and Persistence](https://pentestlab.blog/2021/08/02/universal-privilege-escalation-and-persistence-printer/): The Print Spooler is responsible to manage and process printer jobs. It runs as a service with SYSTEM level privileges on windows environments.

### Tools
 - [JAWS - Just Another Windows (Enum) Script](https://github.com/411Hall/JAWS): JAWS is PowerShell script designed to help penetration testers (and CTFers) quickly identify potential privilege escalation vectors on Windows systems. It is written using PowerShell 2.0 so 'should' run on every Windows version since Windows 7.
 - [juicy-potato](https://github.com/ohpe/juicy-potato): A sugared version of RottenPotatoNG, with a bit of juice, i.e. another Local Privilege Escalation tool, from a Windows Service Accounts to NT AUTHORITY\SYSTEM.
 - [Potato](https://github.com/foxglovesec/Potato): Potato Privilege Escalation on Windows 7, 8, 10, Server 2008, Server 2012.
 - [PowerSploit](https://github.com/PowerShellMafia/PowerSploit): PowerSploit is a collection of Microsoft PowerShell modules that can be used to aid penetration testers during all phases of an assessment.
 - [PrivescCheck](https://github.com/itm4n/PrivescCheck): Enumerate common Windows security misconfigurations which can be leveraged for privilege escalation and gather various information which might be useful for exploitation and/or post-exploitation, by itm4n.
 - [RemotePotato0](https://github.com/antonioCoco/RemotePotato0): Just another "Won't Fix" Windows Privilege Escalation from User to Domain Admin by antonioCoco.
 - [RoguePotato](https://github.com/antonioCoco/RoguePotato): Another Windows Local Privilege Escalation from Service Account to System by splinter_code/antonioCoco
 - [RottenPotato](https://github.com/foxglovesec/RottenPotato): RottenPotato local privilege escalation from service account to SYSTEM. (No longer maintained)
 - [RottenPotatoNG](https://github.com/breenmachine/RottenPotatoNG): New version of RottenPotato as a C++ DLL and standalone C++ binary - no need for meterpreter or other tools.
 - [Seatbelt](https://github.com/GhostPack/Seatbelt): Project that performs a number of security oriented host-survey "safety checks" relevant from both offensive and defensive security perspectives.        
 - [SessionGopher](https://github.com/Arvanaghi/SessionGopher): SessionGopher is a PowerShell tool that finds and decrypts saved session information for remote access tools.
 - [Sherlock](https://github.com/rasta-mouse/Sherlock/): PowerShell script to quickly find missing software patches for local privilege escalation vulnerabilities. (Deprecated)
 - [SweetPotato](https://github.com/CCob/SweetPotato):  Local Service to SYSTEM privilege escalation from Windows 7 to Windows 10 / Server 2019 by CCob
 - [Tater](https://github.com/Kevin-Robertson/Tater): Tater is a PowerShell implementation of the Hot Potato Windows Privilege Escalation exploit.
 - [Watson](https://github.com/rasta-mouse/Watson): Watson is a .NET tool designed to enumerate missing KBs and suggest exploits for Privilege Escalation vulnerabilities.
 - [WindowsEnum](https://github.com/absolomb/WindowsEnum): A Powershell Privilege Escalation Enumeration Script.
 - [Windows-Exploit-Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester): This tool compares a targets patch levels against the Microsoft vulnerability database in order to detect potential missing patches on the target. It also notifies the user if there are public exploits and Metasploit modules available for the missing bulletins. By AonCyberLabs
 - [Windows Exploit Suggester - Next Generation (WES-NG)](https://github.com/bitsadmin/wesng): WES-NG is a tool based on the output of Windows' systeminfo utility which provides the list of vulnerabilities the OS is vulnerable to, including any exploits for these vulnerabilities. Every Windows OS between Windows XP and Windows 10, including their Windows Server counterparts, is supported. By bitsadmin
 - [windows-privesc-check](https://github.com/pentestmonkey/windows-privesc-check): Standalone executable that runs on Windows systems. It tries to find misconfigurations that could allow local unprivileged users to escalate privileges to other users or to access local apps (e.g. databases).
 - [winPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/winPEAS): Windows Privilege Escalation Awesome Scripts
 - [WinPwnage](https://github.com/rootm0s/WinPwnage): UAC bypass, Elevate, Persistence and Execution methods. The goal of this repo is to study the Windows penetration techniques.

### Presentations
 - [Level Up! Practical Windows Privilege Escalation - Andrew Smith](https://www.youtube.com/watch?v=PC_iMqiuIRQ)
 - [Level Up! - Practical Windows Privilege Escalation (Presentation Slides)](https://pt.slideshare.net/jakx_/level-up-practical-windows-privilege-escalation)
 - [SANS Webcast: Pen Testing with PowerShell - Local Privilege Escalation Techniques](https://www.youtube.com/watch?v=bAnohAiAQ7U)
 - [Windows Privilege Escalation Techniques (Local) - Tradecraft Security Weekly #2](https://www.youtube.com/watch?v=DlJyKgfkoKQ)
 - [Windows Privilege Escalation Unquoted Service - Part 1](https://www.youtube.com/watch?v=G9yn3qNq7Vw)
 - [Windows Privilege Escalation Unquoted Service - Part 2](https://www.youtube.com/watch?v=jfZ8FKTFNTE)
 - [Windows Privilege Escalation Unquoted Service - Part 3](https://www.youtube.com/watch?v=RORaqh1DIco)

## Linux and Windows
 - [Awesome-Hacking-Resources (Privilege escalation section)](https://github.com/vitalysim/Awesome-Hacking-Resources#privilege-escalation): A collection of hacking / penetration testing resources to make you better!
 - [Metasploit Local Exploit Suggester: Do Less, Get More!](https://blog.rapid7.com/2015/08/11/metasploit-local-exploit-suggester-do-less-get-more/)
 - [My 5 Top Ways to Escalate Privileges](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/my-5-top-ways-to-escalate-privileges/): Bruno Oliveira's top 5 favorite ways for accomplishing privilege escalation in the most practical ways possible.
 - [Privilege Escalation](https://pentestlab.blog/category/privilege-escalation/): Privilege Escalation category by pentestlab.blog
 - [Recipe for Root](https://recipeforroot.com/): Your Cookbook for Privilege Escalation
 - [Windows / Linux Local Privilege Escalation Workshop](https://github.com/sagishahar/lpeworkshop)

## Docker
 - [Bypassing Docker Authz Plugin and Using Docker-Containerd for Privesc](https://staaldraad.github.io/post/2019-07-11-bypass-docker-plugin-with-containerd/): by Staaldraad.
 - [Container security notes](https://gist.github.com/FrankSpierings/5c79523ba693aaa38bc963083f48456c)
 - [Dirty COW - (CVE-2016-5195) - Docker Container Escape](https://blog.paranoidsoftware.com/dirty-cow-cve-2016-5195-docker-container-escape/)
 - [Docker Breakout](https://book.hacktricks.xyz/linux-unix/privilege-escalation/docker-breakout): by HackTricks
 - [Docker security checklist](https://github.com/PercussiveElbow/docker-security-checklist)
 - [Don't expose the Docker socket (not even to a container)](https://web.archive.org/web/20190623234615/https://www.lvh.io/posts/dont-expose-the-docker-socket-not-even-to-a-container.html)
 - [Escaping Docker Privileged Containers](https://betterprogramming.pub/escaping-docker-privileged-containers-a7ae7d17f5a1): by Vickie Li
 - [Escaping Containers to Execute Commands on Play with Docker Servers](https://www.bleepingcomputer.com/news/security/escaping-containers-to-execute-commands-on-play-with-docker-servers/)
 - [Escaping Docker container using waitid() – CVE-2017-5123](https://www.twistlock.com/labs-blog/escaping-docker-container-using-waitid-cve-2017-5123/)
 - [Escaping the Whale: Things you probably shouldn’t do with Docker (Part 1)](https://blog.secureideas.com/2018/05/escaping-the-whale-things-you-probably-shouldnt-do-with-docker-part-1.html)
 - [Hack Allows Escape of Play-with-Docker Containers](https://threatpost.com/hack-allows-escape-of-play-with-docker-containers/140831/)
 - [Hacking Docker the Easy way](https://pt.slideshare.net/BorgHan/hacking-docker-the-easy-way)
 - [Understanding Docker container escapes](https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/): by Trail of Bits

### Tools
 - [BOtB](https://github.com/brompwnie/botb): BOtB is a container analysis and exploitation tool designed to be used by pentesters and engineers while also being CI/CD friendly with common CI/CD technologies.
 - [CDK](https://github.com/cdk-team/CDK): CDK is an open-sourced container penetration toolkit, offering stable exploitation in different slimmed containers without any OS dependency.
 - [Deepce](https://github.com/stealthcopter/deepce): Docker Enumeration, Escalation of Privileges and Container Escapes (DEEPCE)
 - [Dokcer-escape-tool](https://github.com/PercussiveElbow/docker-escape-tool): This tool will help identify if you're in a Docker container and try some quick escape techniques to help assess the security of your containers.
 - [PrivilegedDockerEscape](https://github.com/0x03f3/PrivilegedDockerEscape): A bash script to create an interactive shell from a privileged docker container to the container host

### Presentations
 - [Introduction to Docker Hacking](https://www.youtube.com/watch?v=XiLfEU9wK-w): by NahamSec

## Cloud
### AWS
 - [AWS-IAM-Privilege-Escalation](https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation): A centralized source of all AWS IAM privilege escalation methods released by Rhino Security Labs.

#### Tools
 - [Pacu](https://github.com/RhinoSecurityLabs/pacu): The AWS exploitation framework, designed for testing the security of Amazon Web Services environments. By RhinoSecurityLabs.

### GCP
 - [Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/): Very deep-dive into manual post-exploitation tactics and techniques for GCP.
 - [GCP-IAM-Privilege-Escalation](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation): IAM Privilege Escalation in GCP by RhinoSecurity.

#### Tools
 - [GCPBucketBrute](https://github.com/RhinoSecurityLabs/GCPBucketBrute): A script to enumerate Google Storage buckets, determine what access you have to them, and determine if they can be privilege escalated. By RhinoSecurity.
