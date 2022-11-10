$file="$env:TMP"+'\dg\GooseDesktop.exe'
$exec=New-Object -com shell.application
$exec.shellexecute($file)
break
