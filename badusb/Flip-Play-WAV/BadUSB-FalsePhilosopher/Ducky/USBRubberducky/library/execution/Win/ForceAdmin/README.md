# 💪 ForceAdmin 💪 ![](https://img.shields.io/github/followers/CatzSec.svg?style=social&label=Follow&maxAge=2592000)
# 💪 https://github.com/catzsec/ForceAdmin

![Downloads](https://img.shields.io/github/downloads/CatzSec/ForceAdmin/total.svg?color=red) 
![Stars](https://img.shields.io/github/stars/CatzSec/ForceAdmin.svg?color=yellow)
![Issues](https://img.shields.io/github/issues/CatzSec/ForceAdmin.svg?color=green)
![Last Commit](https://img.shields.io/github/last-commit/CatzSec/ForceAdmin?color=blue)

ForceAdmin is a c# payload builder, creating infinate UAC pop-ups until the user allows the program to be ran. The inputted commands are ran via powershell calling cmd.exe and should be using the batch syntax. Why use? Well some users have UAC set to always show, so UAC bypass techniques are not possible. However - this attack will force them to run as admin. Bypassing these settings

<h1 align="center">A ⭐ and would be greatly apperciated </h1>
<h1 align="center">Follow for more exploits! </h1>

<h1 align="center"><a href="https://github.com/catzsec/ForceAdmin/releases/download/v1.2.0/ForceAdmin.exe" target="_blank">Download!</a></h1>

<div align="center">
<img src="https://cdn.vox-cdn.com/thumbor/SiIyeqmKIJGcOJccz94pHgwmgvQ=/0x0:1400x1400/1200x800/filters:focal(588x588:812x812):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/68837730/poptart1redrainbowfix_1.0.gif" height="350px"></img>
</div>


## Screenshots

![Screenshot](https://github.com/catzsec/ForceAdmin/blob/main/Screenshots/Screenshot_1.png?raw=true)
![Demo](https://github.com/catzsec/ForceAdmin/blob/main/Screenshots/Demo.gif?raw=true)

## ⚡️ Required

For building on your own, the following NuGet packages are needed 

* [`Fody`](https://www.nuget.org/packages/Fody/): "Extensible tool for weaving .net assemblies."
* [`Costura.Fody`](https://www.nuget.org/packages/Costura.Fody/) "Fody add-in for embedding references as resources."
* [`Microsoft.AspNet.WebApi.Client`](https://www.nuget.org/packages/Microsoft.AspNet.WebApi.Client/) "This package adds support for formatting and content negotiation to System.Net.Http. It includes support for JSON, XML, and form URL encoded data."


## ⚡️ Installation

You can download the latest tarball by clicking [here](https://github.com/CatzSec/ForceAdmin/tarball/master) or latest zipball by clicking [here](https://github.com/catzsec/ForceAdmin/zipball/master).

Download the project:
```zsh
$ git clone https://github.com/catzsec/ForceAdmin.git
```

Enter the project folder 
```zsh
$ cd ForceAdmin
```

Run ForceAdmin:
```zsh
$ dotnet run
```

Compile ForceAdmin:
```zsh
$ dotnet publish -r win-x64 -c Release -o ./publish/
```

---

⚠ ONLY USE FOR EDUCATIONAL PURPOSES ⚠

---


Any questions, errors or solutions, create an Issue in the Issues tab.

