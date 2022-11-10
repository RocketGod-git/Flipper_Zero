_declspec(dllimport) int _stdcall SetCurrentDirectoryA(const unsigned char *lpPathName);

int WinMain(int hInstance, int hPrevInstance, char *lpCmdLine, int nShowCmd)  {
    SetCurrentDirectoryA("\\\\.\\globalroot\\device\\condrv\\kernelconnect");
}

/*Only a comment*/
#if 0 
#endif
