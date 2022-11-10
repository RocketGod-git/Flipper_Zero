using System;

namespace UAC_Escaper.Build
{
    public class Builder
    {
        public string PayloadPath { get; set; }
        public string SaveFileName { get; set; }
        public string TempDirectory { get; set; }
        public string StubCs { get; set; }
        public string ResourceManager { get; set; }
        public string PayloadResources { get; set; }

        public void Replacer(string oldString, string newString)
        {
            if (string.IsNullOrWhiteSpace(StubCs))
            {
                throw new Exception("Stub is null");
            }
            StubCs = StubCs.Replace(oldString, newString);
        }
    }
}
