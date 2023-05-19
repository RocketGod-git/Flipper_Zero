#!/bin/bash
rm -rf /opt/Genesis;
cp Genesis /usr/bin/genesis;
mkdir /opt/Genesis/;
mkdir Storage;
cp * -r /opt/Genesis/;
chmod +x /usr/bin/genesis;
echo "install complete! run genesis!";
chmod +x update_genesis;
cp update_genesis /usr/bin/update_genesis;
