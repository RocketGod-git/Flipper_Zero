using System.Diagnostics;
using System.Net.NetworkInformation;
using System.Runtime.InteropServices;
using System.Text;

namespace GDRLauncher
{
    class Program
    {
        

        private const string GDRVersion = "1.1.9";
        static async Task Main(string[] args)
        {
            Bot.InitialSetup();
            Console.WriteLine($"Relauncher for GDR {GDRVersion}");
#if !DEBUG
            if (await Bot.NewMinidumb())
            {
#endif
                Bot.BotLogic();
#if !DEBUG
            }
            else
            {
                Console.WriteLine("No BSOD detected, closing.");
                Thread.Sleep(5000);
            }
#endif
        }
    }
}