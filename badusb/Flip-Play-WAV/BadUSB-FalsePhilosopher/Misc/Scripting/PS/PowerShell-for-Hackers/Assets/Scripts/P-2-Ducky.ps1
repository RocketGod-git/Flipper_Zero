############################################################################################################################################################                      
#                                  |  ___                           _           _              _             #              ,d88b.d88b                     #                                 
# Title        : Ducky-Base64-Exec | |_ _|   __ _   _ __ ___       | |   __ _  | | __   ___   | |__    _   _ #              88888888888                    #           
# Author       : I am Jakoby       |  | |   / _` | | '_ ` _ \   _  | |  / _` | | |/ /  / _ \  | '_ \  | | | |#              `Y8888888Y'                    #           
# Version      : 1.0               |  | |  | (_| | | | | | | | | |_| | | (_| | |   <  | (_) | | |_) | | |_| |#               `Y888Y'                       #
# Category     : Execute           | |___|  \__,_| |_| |_| |_|  \___/   \__,_| |_|\_\  \___/  |_.__/   \__, |#                 `Y'                         #
# Target       : Windows 7,10,11   |                                                                   |___/ #           /\/|_      __/\\                  #     
#                                  |                                                           |\__/,|   (`\ #          /    -\    /-   ~\                 #             
#                                  |  My crime is that of curiosity                            |_ _  |.--.) )#          \    = Y =T_ =   /                 #      
#                                  |   and yea curiosity killed the cat                        ( T   )     / #   Luther  )==*(`     `) ~ \   Hobo          #                                                                                              
#                                  |    but satisfaction brought him back                     (((^_(((/(((_/ #          /     \     /     \                #    
#__________________________________|_________________________________________________________________________#          |     |     ) ~   (                #
#                                                                                                            #         /       \   /     ~ \               #
#  github.com/I-Am-Jakoby                                                                                    #         \       /   \~     ~/               #         
#  twitter.com/I_Am_Jakoby                                                                                   #   /\_/\_/\__  _/_/\_/\__~__/_/\_/\_/\_/\_/\_#                     
#  instagram.com/i_am_jakoby                                                                                 #  |  |  |  | ) ) |  |  | ((  |  |  |  |  |  |#              
#  youtube.com/c/IamJakoby                                                                                   #  |  |  |  |( (  |  |  |  \\ |  |  |  |  |  |#
############################################################################################################################################################

<#
.SYNOPSIS
  This is a powershell cmdlet that will convert a script to Base64 then format it into ducky script ready payload
  
.DESCRIPTION 
  This is a cmdlet that takes a file path and converts the contents of that file to a Base64 string 
  That Base64 string is then formatted into ducky script ready to be used with the OMG devices or rubber ducky
  The output of that conversion will be saved to the desktop by default
  Estimated time to execute script is calculate and provided at the top of the output file 
  The name of the file will be "converted.txt" by default

  
.PARAMETER Source
  (Mandatory = $True)
  Provide the exact path to the file to be converted
 
.PARAMETER Path
  (Mandatory = $False)
  Provide the exact path to where the output file will be saved 
  
.PARAMETER File
  (Mandatory = $False)
  Provide the name of the file   
  
.PARAMETER Delay
  (Mandatory = $False)
  Provide a custom delay between commands  
.PARAMETER Title
  (Mandatory = $False)
  Provide the name of the payload 
.PARAMETER Author
  (Mandatory = $False)
  Provide the name of the author
.PARAMETER Description
  (Mandatory = $False)
  Provide a brief description 
  
.EXAMPLE
  PS-2-Ducky -source "C:\Users\USER\Desktop\script.ps1" -Path "C:\Users\User\Desktop" -File example -Title Super-Payload -Author Jakoby -Description "Does cool stuff"
  PS-2-Ducky -s "C:\Users\USER\Desktop\script.ps1" -p "C:\Users\User\Desktop" -f example -t Super-Payload -a Jakoby -d "Does cool stuff"
  "C:\Users\USER\Desktop\script.ps1" | PS-2-Ducky -f example -p "C:\Users\User\Desktop" -f example -t Super-Payload -a Jakoby -d "Does cool stuff"
  
#>

function PS-2-Ducky {
	[CmdletBinding()]
	param (
	
	[Parameter (Mandatory = $True, ValueFromPipeline = $True)]
	[Alias("s")]
	[string]$Source,

	[Parameter (Mandatory = $False)]
	[Alias("p")]
	[string]$Path, 

	[Parameter (Mandatory = $False)]
	[Alias("f")]
	[string]$File, 

	[Parameter (Mandatory = $False)]
	[Alias("de")]
	[string]$Delay, 

	[Parameter (Mandatory = $False)]
	[Alias("t")]
	[string]$Title, 

	[Parameter (Mandatory = $False)]
	[Alias("a")]
	[string]$Author, 

	[Parameter (Mandatory = $False)]
	[Alias("d")]
	[string]$Description 

	)	

	if (!$File) { $File = "converted" }

	if (!$Path) { $Path = [Environment]::GetFolderPath("Desktop") }

	if (!$Delay) { $Delay = 250 }
	
	$FilePath = ($Path+"\"+$File+".txt")

	$converted = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes((Get-Content -Path $Source -Raw -Encoding UTF8)))

	$numChar = $converted.length
	$Time = $numChar/140 
	$estTime = [math]::Round($Time,2)

	function splitLines{
		While ($converted)
		{ 
		$x,$converted = ([char[]]$converted).where({$_},'Split',$incriment)
		$x -join ''
		}
	}

	$lSplit = splitLines

	echo "REM --> $numChar Characters: Estimated $estTime seconds to execute `n" >> $FilePath

	if ($Title)        { echo "REM		Title:       $Title"       >> $FilePath}
	if ($Author)       { echo "REM		Author:      $Author"      >> $FilePath}
	if ($Description)  { echo "REM		Description: $Description" >> $FilePath}

	echo "" >> $FilePath
	echo "GUI r" >> $FilePath
	echo "DELAY $Delay" >> $FilePath
	echo "STRING powershell" >> $FilePath
	echo "DELAY $Delay" >> $FilePath
	echo "ENTER" >> $FilePath
	echo "DELAY $Delay" >> $FilePath
	echo "STRING powershell -enc " >> $FilePath
	echo "DELAY $Delay" >> $FilePath

	echo "STRING $converted" >> $FilePath

	echo "DELAY $Delay" >> $FilePath
	echo "ENTER" >> $FilePath
}
