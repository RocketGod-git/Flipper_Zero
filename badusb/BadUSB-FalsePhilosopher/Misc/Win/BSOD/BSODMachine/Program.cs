using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

class Program
{
    [DllImport("ntdll.dll")]
    private static extern uint RtlAdjustPrivilege(
        int Privilege,
        bool bEnablePrivilege,
        bool IsThreadPrivilege,
        out bool PreviousValue
    );
    [DllImport("ntdll.dll")]
    private static extern uint NtRaiseHardError(
        uint ErrorStatus,
        uint NumberOfParameters,
        uint UnicodeStringParameterMask,
        IntPtr Parameters,
        uint ValidResponseOption,
        out uint Response
    );

    public const uint ASSERT_FAILURE = 0xc0000420;

    static void Main(string[] args)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.Write("Do you want me to kill windows? [Y]es - [N]o:");
        Console.ForegroundColor = ConsoleColor.White;
        int x = Console.Read();
        try
        {
            char y = Convert.ToChar(x).ToUpper();
            
            switch(y)
            {
                case 'Y':
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    //yeet windows out the window (pun intended)
                    Console.WriteLine("Attempting to kill windows...");
                    RtlAdjustPrivilege(19, true, false, out bool idk);
                    //                 ^^ Shutdown priviledge
                    NtRaiseHardError(ASSERT_FAILURE, 0, 0, IntPtr.Zero, 6, out uint output);
                    //                                                  ^ Makes the PC shut down instead
                    //                                                  of restarting.
                    break;
                default:
                    Console.ForegroundColor = ConsoleColor.Green;
                    //user is a boring guy and doesnt want to watch windows explode
                    Console.WriteLine("Understandable, have a great day :)");
                    System.Threading.Thread.Sleep(3000);
                    Environment.Exit(0);
                    break;
            }
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Woops! We caught an exception! Message: {0}", ex.Message);
            Console.WriteLine("The program will exit in 10 seconds.");
            System.Threading.Thread.Sleep(10000);
            Environment.Exit(1);
        }
    }
}
