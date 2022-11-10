![Logo](https://github.com/I-Am-Jakoby/hak5-submissions/blob/main/Assets/logo-170-px.png?raw=true)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Description">Description</a></li>
    <li><a href="#SYNTAX">Syntax</a></li>	  
    <li><a href="#The-Functions">The Functions</a></li>
    <li><a href="#Examples">Examples</a></li>
    <li><a href="#Contact">Contact</a></li>
    <li><a href="#Acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

# Base64 Image Converter

<p align="center">
      <a href="https://www.youtube.com/watch?v=x6H96fxyQ-Y">
        <img src=https://i.ytimg.com/vi/x6H96fxyQ-Y/hqdefault.jpg width="300" alt="Golang" />
      </a>
      <br>YouTube Tutorial
</p>

## Description

These two functions can be used to convert an image to and from base64 format

## [SYNTAX]

### Encode an Image 
```
img-b64 -img "C:\Users\user\Desktop\image.jpg" -location desk
```
### Decode a File 
```
b64-img -file "C:\Users\user\Desktop\image.jpg" -location desk
```
## The Functions

### [img-b64] 

This function will convert your image to base64 format 

Use the image tag to provide the path of the image you are trying to convert

Using the Location parameter will determine if the file containing the base64 code is saved to the desktop or temp folder

If no location is designated it will save it to the desktop by default

```
function img-b64 {
[CmdletBinding()]
param (
[Parameter (Mandatory = $True, ValueFromPipeline = $True)]
[string]$img,

[Parameter (Mandatory = $False)]
[ValidateSet('desk', 'temp')]
[string]$location
)

if (!$location) {$location = "desk"}

$loc = switch ( $location )
{
	"desk"  { "$Env:USERPROFILE\Desktop"
	}
	"temp" { "$env:TMP" 
	}
}

[Convert]::ToBase64String((Get-Content -Path $img -Encoding Byte)) >> "$loc\encImage.txt"
}
```

### [b64-img] 

This function will convert your base64 encoded file back into an image 

Use the file tag to provide the path of the file you are trying to convert

Using the Location parameter will determine if the file containing the base64 code is saved to the desktop or temp folder

If no location is designated it will save it to the desktop by default

```
function b64-img {
[CmdletBinding()]
param (
[Parameter (Mandatory = $True)]
[string]$file,

[Parameter (Mandatory = $False)]
[ValidateSet('desk', 'temp')]
[string]$location
)

if (!$location) {$location = "desk"}

$loc = switch ( $location )
{
	"desk"  { "$Env:USERPROFILE\Desktop"
	}
	"temp" { "$env:TMP" 
	}
}

Add-Type -AssemblyName System.Drawing
$Base64 = Get-Content -Raw -Path $file
$Image = [Drawing.Bitmap]::FromStream([IO.MemoryStream][Convert]::FromBase64String($Base64))
$Image.Save("$loc\decImage.jpg")
}
```

<p align="right">(<a href="#top">back to top</a>)</p>


## Examples 

Listed below are payloads that have used one of these functions:

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

<h2 align="center">📱 My Socials 📱</h2>
<div align=center>
<table>
  <tr>
    <td align="center" width="96">
      <a href="https://youtube.com/c/IamJakoby?sub_confirmation=1">
        <img src=https://github.com/I-Am-Jakoby/I-Am-Jakoby/blob/main/img/youtube-svgrepo-com.svg width="48" height="48" alt="C#" />
      </a>
      <br>YouTube
    </td>
    <td align="center" width="96">
      <a href="https://twitter.com/I_Am_Jakoby">
        <img src=https://github.com/I-Am-Jakoby/I-Am-Jakoby/blob/main/img/twitter.png width="48" height="48" alt="Python" />
      </a>
      <br>Twitter
    </td>
    <td align="center" width="96">
      <a href="https://www.instagram.com/i_am_jakoby/">
        <img src=https://github.com/I-Am-Jakoby/I-Am-Jakoby/blob/main/img/insta.png width="48" height="48" alt="Golang" />
      </a>
      <br>Instagram
    </td>
    <td align="center" width="96">
      <a href="https://discord.gg/MYYER2ZcJF">
        <img src=https://github.com/I-Am-Jakoby/I-Am-Jakoby/blob/main/img/discord-v2-svgrepo-com.svg width="48" height="48" alt="Jsonnet" />
      </a>
      <br>Discord
    </td>
  </tr>
</table>
</div>



<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Hak5](https://hak5.org/)
* [UberGuidoZ](https://github.com/UberGuidoZ)

***

[HOME-PAGE](https://github.com/I-Am-Jakoby/PowerShell-for-Hackers)

<p align="right">(<a href="#top">back to top</a>)</p>
