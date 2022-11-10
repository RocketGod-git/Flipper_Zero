using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Configuration;
using System.Net.NetworkInformation;

namespace GDRLauncher
{
    static class Bot
    {
        #region Variables
        private static int MinToWait = 0;

        private const string GDRWindow = "GDR";
        private const string GDRWindowFirstButton = "登录卡密";
        private const string GDRStartButton = "启动";

        private const string SelectWindow = "运行";
        private const string SelectWindowFirstButton = "订阅信息";
        private const string SecondWindowStartButton = "运行";


        public delegate bool Win32Callback(IntPtr hwnd, IntPtr lParam);
        private const int BM_CLICK = 0x00F5;
        private static string GdrPath = "";
        private static bool CheckVPN = false;
        private static bool CheckBsod = false;

        private static string LogTextFile = "log.txt";
        private static IntPtr GdrWindowHandle;
        #endregion

        #region Dll Calls
        [DllImport("user32.dll")]
        private static extern IntPtr GetDlgItem(IntPtr hWnd, int nIDDlgItem);
        [DllImport("user32.dll")]
        private static extern IntPtr SendMessage(IntPtr hWnd, int Msg, int wParam, IntPtr lParam);
        [DllImport("user32.dll", SetLastError = true)]
        private static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
        [DllImport("user32.dll", EntryPoint = "FindWindowEx", CharSet = CharSet.Auto)]
        private static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool IsWindow(IntPtr hWnd);
        #endregion
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        static extern IntPtr SendMessage(IntPtr hWnd, UInt32 Msg, IntPtr wParam, IntPtr lParam);
        [DllImport("user32.dll")]
        public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
        [DllImport("user32.dll")]
        public static extern int GetWindowTextLength(int hWnd);
        [DllImport("user32")]
        internal static extern int GetWindowText(int hWnd, String text, int nMaxCount);
        [DllImport("user32.dll")]
        public static extern int FindWindowEx(int parent, int start, String class_name);
        [DllImport("user32.dll")]
        public static extern int GetWindow(int parent, uint cmd);
        [DllImport("user32.dll")]
        static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll")]
        static extern bool SetForegroundWindow(IntPtr hWnd);
        /// <summary>
        /// Log to a text file, it appends Time at the begginig of the message
        /// </summary>
        /// <param name="Message"></param>
        private static void LogToFile(string Message)
        {
            Console.WriteLine(Message);
            string datenow = "[" + DateTime.Now.ToString("dddd, dd MMMM yyyy HH:mm:ss") + "] ";
            if (!File.Exists(LogTextFile))
            {
                using (StreamWriter sw = File.CreateText(LogTextFile))
                {
                    sw.WriteLine(datenow + Message);
                }
            }

            using (StreamWriter sw = File.AppendText(LogTextFile))
            {
                sw.WriteLine(datenow + Message);
            }
        }

        public async static Task<bool> NewMinidumb()
        {
            if (CheckBsod)
            {
                bool exist = Directory.Exists(Environment.GetFolderPath(Environment.SpecialFolder.Windows) + @"\Minidump");
                if (exist)
                {
                    string windowsPath = Environment.GetFolderPath(Environment.SpecialFolder.Windows) + @"\Minidump";
                    int Minidumpcount = System.IO.Directory.EnumerateFiles(windowsPath).Count();

                    string text = File.ReadAllText(@"minidumpcount.txt");
                    int lastcount = 0;
                    int.TryParse(text, out lastcount);
                    if (Minidumpcount > lastcount)
                    {
                        File.WriteAllText("minidumpcount.txt", Minidumpcount.ToString());
                        return true;
                    }
                    else
                    {
                        return false;
                    }
                }
                else
                {
                    return false;
                }
            }
            else
            {
                return true;
            }
            return false;
        }
        static private IntPtr ActiveWindowHandle()
        {
            IntPtr handle = IntPtr.Zero;
            handle = GetForegroundWindow();
            return handle;
        }

        public static IntPtr LaunchAndHandler()
        {
           for (int a = MinToWait * 60; a >= 0; a--)
           {
                TimeSpan time = TimeSpan.FromSeconds(a);
                Console.Write($"\rLaunching GDR in {time.ToString(@"mm\:ss")}", a);
                Thread.Sleep(1000);
           }
            if (File.Exists(GdrPath))
            {
                if (CheckVPN)
                {
                    Console.WriteLine("\nChecking Vpn");

                    while (!VpnIsConnected())
                    {
                        Thread.Sleep(10000);
                    }
                }
                Process p = Process.Start(GdrPath);
                p.WaitForInputIdle();
                SetForegroundWindow(p.MainWindowHandle);
                GdrWindowHandle = p.MainWindowHandle;
                return p.MainWindowHandle;
            }
            else
            {
                LogToFile($"[ERROR] GDR was not found in {GdrPath}");
                return IntPtr.Zero;
            }
        }
        
        /// <summary>
        /// Look for window caption and returns it handler
        /// </summary>
        /// <param name="WindowName"></param>
        /// <returns></returns>
        private static IntPtr LookForWindow(string WindowName)
        {
            LogToFile($"Looking for {WindowName} Window");
            IntPtr windowHandle = IntPtr.Zero;
            bool iswindowOpen = false;
            while (iswindowOpen == false)
            {
                windowHandle = FindWindow(null, WindowName);

                iswindowOpen = IsWindow(windowHandle);
                if (iswindowOpen == false)
                {
                    LogToFile($"Not found yet");
                    System.Threading.Thread.Sleep(1000);
                }
            }
            LogToFile($"{WindowName} Window found");
            return windowHandle;
        }
      
        /// <summary>
        /// Look for button that are inside another button using window handler
        /// </summary>
        /// <param name="windowHandle"></param>
        /// <param name="ButtonName1"></param>
        /// <param name="ButtonName2"></param>
        private static void LookForButtonWithinButton(IntPtr windowHandle, string ButtonName1, string ButtonName2)
        {
            IntPtr btnHandle = IntPtr.Zero;
            LogToFile($"Looking for button {ButtonName2}");
            while (btnHandle == (IntPtr)0x0000000000000000)
            {
                btnHandle = FindWindowEx(windowHandle, IntPtr.Zero, null, ButtonName1);

                if (btnHandle == IntPtr.Zero)
                {
                    LogToFile($"Not found yet");
                    System.Threading.Thread.Sleep(1000);
                }
            }
            LogToFile($"{ButtonName2} button Found");
            var btnHandle2 = FindWindowEx(btnHandle, IntPtr.Zero, null, ButtonName2);
            SendMessage(btnHandle2, BM_CLICK, 0, IntPtr.Zero);
        }

        private static void lookForButton(IntPtr windowHandle, string ButtonName1)
        {
            IntPtr btnHandle = IntPtr.Zero;
            while (btnHandle == IntPtr.Zero)
            {
                btnHandle = FindWindowEx(windowHandle, IntPtr.Zero, null, ButtonName1);

                if (btnHandle == IntPtr.Zero)
                {
                    LogToFile($"Not found yet");
                    System.Threading.Thread.Sleep(2000);
                }
            }
            SendMessage(btnHandle, BM_CLICK, IntPtr.Zero, IntPtr.Zero);
        }

        /// <summary>
        /// Variable initializer with paths and variable values
        /// </summary>
        public static void InitialSetup()
        {
            GdrPath = ConfigurationManager.AppSettings.Get("GDRPath");
            CheckVPN = Convert.ToBoolean(int.Parse(ConfigurationManager.AppSettings.Get("CheckVPN")));
            MinToWait = int.Parse(ConfigurationManager.AppSettings.Get("MinsToWait"));
            CheckBsod = Convert.ToBoolean(int.Parse(ConfigurationManager.AppSettings.Get("CheckForBSOD")));



        }


        private static bool VpnIsConnected()
        {
            if (NetworkInterface.GetIsNetworkAvailable())
            {

                NetworkInterface[] interfaces = NetworkInterface.GetAllNetworkInterfaces();
                foreach (NetworkInterface Interface in interfaces)
                {
                    if (Interface.OperationalStatus == OperationalStatus.Up)
                    {
                        if ((Interface.NetworkInterfaceType == NetworkInterfaceType.Ppp) && (Interface.NetworkInterfaceType != NetworkInterfaceType.Loopback))
                        {
                            Console.WriteLine("VPN Connected");

                            return true;
                        }
                    }
                }
            }
            Console.WriteLine("VPN not connected, checking again in 10secs");

            return false;
        }


        /// <summary>
        /// Main bot logic
        /// </summary>
        public static void BotLogic()
        {
            IntPtr GDRWindow = LaunchAndHandler();
            if (GDRWindow != IntPtr.Zero)
            {
                Console.WriteLine("\nWindow 1 handle = " + GDRWindow.ToString("X"));
                //Use GDR window handle to look for button and click it
                //LookForButtonWithinButton(windowHandle, GDRWindowFirstButton, GDRWindowSecondButton);
                lookForButton(GDRWindow, GDRStartButton);
                // Look for second windows to open
                SetForegroundWindow(GdrWindowHandle);
                IntPtr PostGDRWindow = ActiveWindowHandle();
                int tries = 1;
                while (PostGDRWindow == GDRWindow)
                {
                   Console.WriteLine($"Looking for second Window [Tries {tries}/3]");
                    SetForegroundWindow(GdrWindowHandle);
                    PostGDRWindow = ActiveWindowHandle();
                    Thread.Sleep(3000);
                    if (tries == 3)
                    {
                        Console.WriteLine($"Clicking start again");
                        //lookForButton(windowHandle, GDRWindowSecondButton);

                        lookForButton(GDRWindow, GDRStartButton);
                        tries = 0;
                    }
                    tries++;
                }
                Console.WriteLine("Window 2 handle = " + PostGDRWindow.ToString("X"));

                //Use second window handle to look for the button and click it
                lookForButton(PostGDRWindow, SecondWindowStartButton);
                Environment.Exit(0);
            }
        }
    }
}
