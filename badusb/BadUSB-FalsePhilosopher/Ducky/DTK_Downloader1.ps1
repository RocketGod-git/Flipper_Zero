$SavePath = 'C:\Payloads'
New-Item -Path $SavePath -ItemType Directory -Force
$URL = 'https://ducktoolkit.com/userscripts';
$counter = 0;
$Response = Invoke-WebRequest -Uri $URL;
$HTML = $Response.ParsedHtml;
$HTML.getElementById('userscripts').rows | 
% {
    $Att = $_.getAttribute('data-href',1);
    if($Att.Trim.Length -gt 0){ 
        $json = ((Invoke-WebRequest -Uri ($URL + '/' + $Att)) | ConvertFrom-Json);
        [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String($json.b64ducktext)) | Set-Content "$($SavePath)\$((++$counter)).txt"
    }
}
