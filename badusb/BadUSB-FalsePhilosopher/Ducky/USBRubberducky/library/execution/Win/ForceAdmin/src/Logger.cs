using static System.Console;
using System.Windows.Forms;

namespace Logger
{
    public class logger
    {
        public static void Log(string message)
        {
            Console.ForegroundColor = ConsoleColor.Gray;
            Write("[");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Write("*");
            Console.ForegroundColor = ConsoleColor.Gray;
            Write("] ");
            WriteLine($"{message}");
            Console.ResetColor();
        }

        public static string Ask(string message)
        {
            Console.ForegroundColor = ConsoleColor.Gray;
            Write("[");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Write("?");
            Console.ForegroundColor = ConsoleColor.Gray;
            Write("] ");
            Write($"{message} > ");
            Console.ResetColor();

            string input = ReadLine();
            return input;
        }

        public static string CustomAsk(string message,  string defaulttext)
        {
            Console.ForegroundColor = ConsoleColor.Gray;
            Write("[");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Write("?");
            Console.ForegroundColor = ConsoleColor.Gray;
            Write("] ");
            Write($"{message} > ");
            Console.ResetColor();
            SendKeys.SendWait(defaulttext);

            string input = ReadLine();
            return input;
        }
    }
}