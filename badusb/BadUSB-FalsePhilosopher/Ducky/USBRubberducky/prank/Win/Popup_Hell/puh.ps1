Add-Type -a system.windows.forms
foreach($i in 1..9999)
{
$x=Get-Random -Min 10 -Max 1910
$y=Get-Random -Min 10 -Max 1070
[System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x,$y)
}