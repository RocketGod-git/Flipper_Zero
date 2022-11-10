### Emotet Malware 

Emotet is a malware. Originally intended to steal banking information, its malware has since diversified. It was distributed mainly through phishing campaigns. The malware uses Spearphishing emails with malicious attachments sent to user, Users launch the malicious attachments delivered via spearphishing emails. **WMI was used to execute powershell.exe**.


![image](https://user-images.githubusercontent.com/75935486/153730523-892b9b98-2699-48c9-a919-5bc6d6824673.png)




### **EMOTET PPID Spoofing using WMI:**

we can try do it on CLI with Poweshell but it is more detectable because the command will be logged.

```powershell
PS > wmic /namespace:\\root\CIMV2 path Win32_Process call create "notepad.exe"
```
```json
{
   "ProcessId": 23468
   "ReturnValue": 0
}
```
**ReturnValue** is equal which means that the operation is completed successfully on PID 22396 (ProcessId).

![image](https://user-images.githubusercontent.com/75935486/153729571-33b13901-b82b-4307-95be-1ab6530fdeb0.png)



### **Using COM API and WMI for PPID Spoofing**

First we'll Initializes the COM library using `CoInitializeEx`, after that we will add security levels on COM with `CoInitializeSecurity` and we need to obtain the initial locator to WMI by calling CoCreateInstance.
```cpp
CoInitializeEx(0, COINIT_MULTITHREADED);
CoInitializeSecurity(NULL, -1, NULL, NULL, RPC_C_AUTHN_LEVEL_DEFAULT, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE, NULL); // we can replace EOAC_NONE with 0 because EOAC_NONE is equal to 0.
CoCreateInstance(CLSID_WbemLocator, 0, CLSCTX_INPROC_SERVER, IID_IWbemLocator, (LPVOID *) &pLoc);
```

for `CoInitializeSecurity` function, we simply use the default security for WMI.

![image](https://user-images.githubusercontent.com/75935486/153731697-1c4e8611-8449-4ede-86f6-35eba60fcce5.png)


Using the IWbemLocator interface will allow us to obtain the initial namespace pointer to the IWbemServices interface for WMI on a specific host computer. as a reminder, WMI is an implementation of WBEM.

**RPC_C_IMP_LEVEL_IMPERSONATE**

Specifies an impersonation level, which indicates the amount of authority given to the server when it is impersonating the client.
we use this level of impersonation to access local resources such as files. When impersonating at this level, the impersonation token can only be passed across one machine boundary.

**CLSCTX & CLSCTX_INPROC_SERVER**

CLSCTX Values that are used in activation calls to indicate the execution contexts in which an object is to be run.
**CLSCTX_INPROC_SERVER** will make sure that the code that creates and manages the objects of this class is a DLL that runs in the same process as the caller of the function specifying the class context.


once the instance is created we will need `pLoc` which is the pointer to this instance to connect to the local `rootCIMV2` namespace using `ConnectServer()` function. now that we are connected to the namespace, the pointer of this object is `pSvc`. Before accessing the namespace classes (`Win32_Process`), we need to define security for the proxy with the `CoSetProxyBlanket()` function using the `pSvc` object pointer because this object needs a proxy to communicate with the classes.

**CoSetProxyBlanket()** function sets the authentication information that will be used to make calls on the specified proxy.

```cpp
pLoc->ConnectServer(_bstr_t(L"ROOT\\CIMV2"), NULL, NULL, 0, NULL, 0, 0, &pSvc);
CoSetProxyBlanket(pSvc, RPC_C_AUTHN_WINNT, RPC_C_AUTHN_NONE, NULL, RPC_C_AUTHN_LEVEL_CALL, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE);
```

After that we can Access to the Class and Specify a Method, we'll need to use IWbemServices pointer to make requests to WMI and access to Specific Instances of the class using `SpawnInstance()`

![image](https://user-images.githubusercontent.com/75935486/153733039-14c15fcb-5c79-44a7-be77-337b67d5fcfa.png)


For the final part we need to execute our command (notepad.exe) using `ExecMethod()` with the Class which is **Win32_Process**, the Method which is **Create**, the ClassInstance Pointer and the pointer of the parameter output.

```cpp
VARIANT varCommand;
varCommand.vt = VT_BSTR;
varCommand.bstrVal = _bstr_t(L"notepad.exe");
hres = pClassInstance->Put(L"CommandLine", 0, &varCommand, 0);

IWbemClassObject * pOutParams = NULL;
hres = pSvc->ExecMethod(ClassName, MethodName, 0, NULL, pClassInstance, &pOutParams, NULL);
```


![image](https://user-images.githubusercontent.com/75935486/153729993-192b6fff-e24f-40fa-9756-0f1d2d14339c.png)
