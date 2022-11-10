#!/bin/bash

file="$1"
pay="payload.txt"
touch payload.txt

echo "DELAY 1000" > $pay

for l in $(cat $file)
do echo "DELAY 300 " >> $pay; echo  "STRING $l" >> $pay; echo "ENTER" >> $pay; 

done

