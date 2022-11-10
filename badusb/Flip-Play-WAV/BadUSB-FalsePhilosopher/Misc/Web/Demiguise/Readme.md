# Demiguise - HTA encryption tool https://github.com/nccgroup/demiguise

Released as open source by NCC Group Plc - http://www.nccgroup.trust/

Developed by Richard Warren, richard [dot] warren [at] nccgroup [dot] trust

http://www.github.com/nccgroup/demiguise

Released under AGPL, see LICENSE for more information

## What does it do? ##

The aim of this project is to generate `.html` files that *contain an encrypted HTA file*. The idea is that when your target visits the page, the key is fetched and the HTA is decrypted dynamically within the browser and pushed directly to the user. This is an evasion technique to get round content / file-type inspection implemented by some security-appliances. This tool is not designed to create awesome HTA content. There are many other [tools](https://github.com/vysec/morphHTA "morphHTA")/[techniques](https://github.com/subTee/Shellcode-Via-HTA "Shellcode-Via-HTA") that can help you with that. What it might help you with is getting your HTA into an environment in the first place, and (if you use environmental keying) to avoid it being sandboxed.

## How does it do it? ##

This is achieved by encrypting the HTA file using RC4, and then using `navigator.msSaveBlob` to "save" the file at runtime - rather than fetching the HTA directly from the server. Meaning that at no point is there any HTTP request/response that contains your HTA file in a plain-text form - the proxy will simply see a `text/html` file containing your encrypted blob. In the latest version of Edge, this will result in the user being prompted to "run" the HTA.

Although not the primary aim of this tool, there are a couple of payload-options for the underlying HTA. Each option uses different techniques as previously documented by [Matt Nelson](https://twitter.com/enigma0x3/status/870810601483894784 "Matt Nelson"), [Matthew Demaske](https://github.com/MatthewDemaske/ThreatHuntingStuff/tree/master/HTAtricks "Matthew Demaske"), [Ryan Hanson](https://twitter.com/ryHanson) and [Etienne Stalmans](https://twitter.com/_staaldraad/status/889171980641021954 "Etienne Stalmans"). The benefit of using these techniques is that your code does not execute as a child of `mshta.exe`. As mentioned previously, the content of the HTA is not the primary aim of this tool. I'd encourage you to modify the HTA template to contain your own custom code :)

## How do I run it? ##

Run the `demiguise.py` file, giving it your encryption-key, payload-type, output file-name and command that you want the HTA run.

Example: ```python demiguise.py -k hello -c "notepad.exe" -p Outlook.Application -o test.hta```

![](https://media.giphy.com/media/l1J3HdXkbCCe7sqWY/giphy.gif)

![](https://media.giphy.com/media/l0IylM6alcr7PwEyk/giphy.gif)

## Environmental Keying ##

In order to evade sandboxes, you shouldn't embed your key directly in the HTA. Instead you should get this dynamically from the environment the target is based in. An example of this may be to use the client's external IP address as a key. The benefit of this is that if the code is run in a 3rd-party sandbox, the HTA will not decrypt. In fact, the file-name will not even decrypt, meaning that nobody will know what your payload is/does :)

Some examples of environmental keying are given in [examples/externalip.js](examples/externalip.js) and [examples/virginkey.js](examples/virginkey.js).

## Bonus ##

Since the tool outputs an HTML file containing JavaScript, you can simply take this JS and host it wherever you like. This means that if your client's website is vulnerable to reflected-XSS, you can use this to serve your HTA file from their (*highly trusted*) domain.

Also, Outlook doesn't block `.html` attachments by default , and neither do some other applications - use your imagination! :)

## Detection ##

Currently it is not detected on VT:

[https://www.virustotal.com/en/file/24b86ee6210b2abc446021feacfe25502b60403455aa24a32c80b2e7b0f81a70/analysis/1499880541/](https://www.virustotal.com/en/file/24b86ee6210b2abc446021feacfe25502b60403455aa24a32c80b2e7b0f81a70/analysis/1499880541/)

## Defense ##

Although obfuscation techniques may be hard to signature, one way to defend against HTA attacks is to prevent the HTA itself from being able to run in the first place. This can be achieved either through the use of [Software Restriction Policy (SRP)](https://technet.microsoft.com/en-us/library/cc734043(v=ws.10).aspx), [Device Guard (on Windows 10 and Server 2016)](https://technet.microsoft.com/en-us/library/cc734043(v=ws.10).aspx), or by changing the default file-handler associated with .hta files.

Please note that these changes may potentially affect the running of software that relies on HTA execution. Therefore it is recommended that a fix is fully tested in your own environment.

**Using SRP:**

![](https://media.giphy.com/media/3oKIPwzrm6okTJwcEM/giphy.gif)

**Changing the default file-handler:**

    ftype htafile=%SystemRoot%\system32\NOTEPAD.EXE %1

![](https://media.giphy.com/media/xUOrwiKh5KcKMYl89q/giphy.gif)

**Changing it back (x64):**

    ftype htafile=C:\Windows\SysWOW64\mshta.exe "%1" {1E460BD7-F1C3-4B2E-88BF-4E770A288AF5}%U{1E460BD7-F1C3-4B2E-88BF-4E770A288AF5} %*

## FAQ ##

- Doesn't this drop to disk?
	- Testing in the latest version of Edge, this only "drops to disk" in the same way that serving a regular HTA does. It's going to end up as a temp file on disk either way.
- Why would I use this when I already have a sandbox detection for $product by checking for domain joined status / printers etc.?
	- The aim of the tool is to avoid being executed in a sandbox in the first place. If you pick your keys wisely, the HTA will not even decrypt correctly, nor will $product know it's an HTA file - meaning it cannot be executed by the sandbox.
- How do I find an environmental key source without first having access to the target network?
	- This is left as an exercise for the reader, however this can often be discovered with some good OSINT. If you are carrying out fingerprinting campaigns, check out [WebFEET](https://github.com/nccgroup/WebFEET "WebFEET") and [BeEF](https://github.com/beefproject/beef/wiki/Network-Discovery#get-http-servers "BeEF") for some inspiration.

## Greetz / Prior Art ##

- [Matt Nelson](https://twitter.com/enigma0x3 "Matt Nelson") - `WbemScripting.SWbemLocator` & ShellBrowserWindow COM execution Techniques
- [Matthew Demaske](https://github.com/MatthewDemaske/ThreatHuntingStuff/tree/master/HTAtricks) - `WbemScripting.SWbemLocator` COM execution PoC
- [Ryan Hanson](https://gist.github.com/ryhanson/227229866af52e2d963cf941af135a52) - `Excel.Application.RegisterXLL` COM execution technique
- [Etienne Stalmans](https://twitter.com/_staaldraad/status/889171980641021954) - `Outlook.Application.CreateObject` COM execution technique
- [Brandon Arvanaghi](https://twitter.com/arvanaghi) and [Chris Truncer's](https://twitter.com/christruncer) [CheckPlease tool.](https://github.com/Arvanaghi/CheckPlease)
- [The Empire Project](https://github.com/EmpireProject/Empire)



