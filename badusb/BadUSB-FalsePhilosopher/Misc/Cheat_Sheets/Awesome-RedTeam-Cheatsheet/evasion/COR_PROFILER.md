an attacker can exploit the COR_PROFILER environment variable to hijack the execution flow of programs that load the **.NET CLR**. 
**COR_PROFILER** is a feature of the **.NET Framework** that allows developers to specify **a DLL file** to load into each .NET process that loads the Common Language Runtime (CLR). These profilers are designed to monitor, troubleshoot, and debug managed code executed by the .NET CLR.



COR_PROFILER: if the COR_ENABLE_PROFILING check succeeds, the CLR connects to the profiler that has that CLSID or ProgID, 
which must have been previously stored in the Registry. The COR_PROFILER environment variable is defined as a string, as shown in the following two examples.




![image](https://user-images.githubusercontent.com/75935486/151682546-e798b414-4757-4ab6-9e30-2b863024dddf.png)





**References :**

- https://attack.mitre.org/techniques/T1574/012/
