#!/usr/bin/python3
import os
import sys
def update():
    print("Attemping to update Genesis")
    os.system("rm -rf /opt/Genesis;cd /opt/;git clone https://github.com/Zchap1/Genesis.git")
    os.system("cd /opt/Genesis/;sudo bash install.sh > /dev/null")
    print("Update has Finished")
    sys.exit()

update()
