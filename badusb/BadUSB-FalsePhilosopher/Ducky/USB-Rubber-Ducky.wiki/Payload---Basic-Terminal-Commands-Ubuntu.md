The following script is an example of how to execute commands in Ubuntu Linux through xterm. The script first initiates the run application window through ubuntu and later on it triggers the command xterm. After the execution of the terminal it issues the commands "pwd", "id" and "cat /etc/passwd".  

    DELAY 3000
    ALT F2
    DELAY 500
    STRING xterm
    DELAY 500
    ENTER
    DELAY 750 
    STRING pwd
    DELAY 500
    ENTER
    DELAY 300
    STRING id
    DELAY 300
    ENTER
    DELAY 500
    STRING cat /etc/passwd
    DELAY 500
    ENTER