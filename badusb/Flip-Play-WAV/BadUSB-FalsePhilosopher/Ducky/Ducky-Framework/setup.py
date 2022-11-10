#!/bin/python3

from subprocess import PIPE, run
import os

file = open('prompt.py','r')
fileLines = file.readlines()

#this will chnge the 'default path vaiable form prompt.py to the location where
#fduck is installed

location = run('/usr/bin/pwd', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=False)
location = location.stdout.replace('\n','')
#there will be an \n in the middle

fileLines[25] = "\tdefaultPath = "+ chr(39) + location + chr(39) + "\n\n" #I can't put another '

file = open('prompt.py', 'w')
file.writelines(fileLines)
file.close

#the same with the fduck
file = open('fduck','r')
fileLines = file.readlines()
fileLines[55] = "\t\t\tos.system(" +chr(39) + location + "/duckyFuzz.sh " + chr(39) +"+ file)" + "\n"

file = open('fduck', 'w')
file.writelines(fileLines)
file.close

#giving exec permissions
os.system('chmod +x fduck duckyFuzz.sh')
print('You can use fduck now!')
