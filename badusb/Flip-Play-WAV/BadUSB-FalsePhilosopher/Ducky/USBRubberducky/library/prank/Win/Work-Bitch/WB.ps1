

#Movie Path
[uri]$VideoSource = "$env:TMP\WB\WB.mp4"

#Devide All Objects on XAML
$XAMLReader=(New-Object System.Xml.XmlNodeReader $XAML)
$Window=[Windows.Markup.XamlReader]::Load( $XAMLReader )
$VideoPlayer = $Window.FindName("VideoPlayer")


#Video Default Setting
$VideoPlayer.Volume = 100;
$VideoPlayer.Source = $VideoSource;
#$VideoPlayer.Padding = new Thickness(5);

$VideoPlayer.Play()

#Show Up the Window
$Window.ShowDialog() | out-null
