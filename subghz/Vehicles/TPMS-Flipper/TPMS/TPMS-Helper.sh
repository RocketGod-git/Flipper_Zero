#!/bin/sh
#TPMS Helper
#Generates Flipper Zero .sub files for a variety of car TPMS
#Helper Script, Schrader SMD3MA4 encoding and python modifications by Lord Daikon
#Massive thanks for help wih signals analysis, python fixes, and overall wisdom from Jimilinux
#PMV-107J and tools from https://github.com/triq-org/tx_tools
#Citroen, and Ford from https://github.com/cdeletre/txtpms/
#subghz_ook_to_sub.py by https://github.com/evilpete/flipper_toolbox
#
#Utilizes GNUradio, rtl_433, sox and python 3.10 (Use Ubuntu, Debian stable has issues)
#
#Is there a better way to do this? Probably, but it works.

FILE=$HOME/TPMS/.tpms
if test -f "$FILE"; then
    echo
else

REQUIRED_PKG="python3"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

REQUIRED_PKG="python3-pip"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

REQUIRED_PKG="rtl-433"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

REQUIRED_PKG="gnuradio"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

REQUIRED_PKG="sox"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

pip install crcmod
chmod +x /$HOME/TPMS/Resources/code_gen

touch .tpms

fi


echo Enter the number of the TPMS type:
echo 1. PMV-107J
echo 2. Citroen
echo 3. Ford
echo 4. Schrader SMD3MA4
echo 5. Credits



read num

cd $HOME/TPMS/

case "$num" in
   "1") python3 Resources/PMV-107J.py 
   
   Resources/./code_gen -s 250k -r $HOME/TPMS/Output/test.txt -w $HOME/TPMS/Output/pmv-107j.cu8
   
   rtl_433 -r $HOME/TPMS/Output/pmv-107j.cu8 -w $HOME/TPMS/Output/pmv-107j.ook
   
   python3 Resources/subghz_ook_to_sub.py $HOME/TPMS/Output/pmv-107j.ook 315000000
   
   rm $HOME/TPMS/Output/test.txt
   
   rm $HOME/TPMS/Output/pmv-107j.cu8
   
   rm $HOME/TPMS/Output/pmv-107j.ook
   
   exit 1
   ;;
   "2") echo Enter 8 digit Citroen hex id
   read id
   python3 Resources/tpms_citroen.py -i $id -r 0
   python3 Resources/tpms_citroen.py -i $id -r 1
   python3 Resources/tpms_citroen.py -i $id -r 2
   python3 Resources/tpms_citroen.py -i $id -r 3
   python3 Resources/tpms_fsk.py -b 19200 -r $HOME/TPMS/Output/Citroen0.u8 -w $HOME/TPMS/Output/citroen0.cu8
   python3 Resources/tpms_fsk.py -b 19200 -r $HOME/TPMS/Output/Citroen1.u8 -w $HOME/TPMS/Output/citroen1.cu8
   python3 Resources/tpms_fsk.py -b 19200 -r $HOME/TPMS/Output/Citroen2.u8 -w $HOME/TPMS/Output/citroen2.cu8
   python3 Resources/tpms_fsk.py -b 19200 -r $HOME/TPMS/Output/Citroen3.u8 -w $HOME/TPMS/Output/citroen3.cu8
   
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - > $HOME/TPMS/Output/citroen.cu8
   cat $HOME/TPMS/Output/citroen0.cu8 >> $HOME/TPMS/Output/citroen.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/citroen.cu8
   cat $HOME/TPMS/Output/citroen1.cu8 >> $HOME/TPMS/Output/citroen.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/citroen.cu8
   cat $HOME/TPMS/Output/citroen2.cu8 >> $HOME/TPMS/Output/citroen.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/citroen.cu8
   cat $HOME/TPMS/Output/citroen3.cu8 >> $HOME/TPMS/Output/citroen.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/citroen.cu8
   
   rtl_433 -r $HOME/TPMS/Output/citroen.cu8 -w $HOME/TPMS/Output/citroen.ook
   
   python3 Resources/subghz_ook_to_sub.py $HOME/TPMS/Output/citroen.ook 315000000
   
   rm $HOME/TPMS/Output/Citroen0.u8
   rm $HOME/TPMS/Output/Citroen1.u8
   rm $HOME/TPMS/Output/Citroen2.u8
   rm $HOME/TPMS/Output/Citroen3.u8
   
   rm $HOME/TPMS/Output/citroen0.cu8
   rm $HOME/TPMS/Output/citroen1.cu8
   rm $HOME/TPMS/Output/citroen2.cu8
   rm $HOME/TPMS/Output/citroen3.cu8
   
   rm $HOME/TPMS/Output/citroen.cu8
   
   rm $HOME/TPMS/Output/citroen.ook
   
   exit 1
   ;;
   
   "3") echo Enter 8 digit Ford hex id
   read id
   python3 Resources/tpms_ford.py -i $id
   python3 Resources/tpms_fsk.py -b 19200 -r $HOME/TPMS/Output/Ford.u8 -w $HOME/TPMS/Output/ford1.cu8
   
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - > $HOME/TPMS/Output/ford.cu8
   cat $HOME/TPMS/Output/ford1.cu8 >> $HOME/TPMS/Output/ford.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/ford.cu8
   cat $HOME/TPMS/Output/ford1.cu8 >> $HOME/TPMS/Output/ford.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/ford.cu8
   cat $HOME/TPMS/Output/ford1.cu8 >> $HOME/TPMS/Output/ford.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/ford.cu8
   cat $HOME/TPMS/Output/ford1.cu8 >> $HOME/TPMS/Output/ford.cu8
   dd bs=5000 count=1 if=/dev/zero | sox -t raw -v 0 -c2 -b8 -eunsigned-integer -r 250k - -t raw - >> $HOME/TPMS/Output/ford.cu8
   
   rtl_433 -r $HOME/TPMS/Output/ford.cu8 -w $HOME/TPMS/Output/ford.ook
   
   python3 Resources/subghz_ook_to_sub.py $HOME/TPMS/Output/ford.ook 315000000
   
   rm $HOME/TPMS/Output/Ford.u8
   
   rm $HOME/TPMS/Output/ford1.cu8
   
   rm $HOME/TPMS/Output/ford.cu8
   
   rm $HOME/TPMS/Output/ford.ook
   
   exit 1
   ;;
   
   "4")python3 Resources/tpms_smd3ma4.py 
   
   Resources/./code_gen -s 250k -r $HOME/TPMS/Output/smd3ma4.txt -w $HOME/TPMS/Output/smd3ma4.cu8
   
   rtl_433 -r $HOME/TPMS/Output/smd3ma4.cu8 -w $HOME/TPMS/Output/smd3ma4.ook
   
   python3 Resources/subghz_ook_to_sub.py $HOME/TPMS/Output/smd3ma4.ook 315000000
   
   rm $HOME/TPMS/Output/smd3ma4.txt
   
   rm $HOME/TPMS/Output/smd3ma4.cu8
   
   rm $HOME/TPMS/Output/smd3ma4.ook
   
   exit 1
   ;;
   
   "5")
               echo TPMS Helper
    echo Generates Flipper Zero .sub files for a variety of car TPMS
    echo Helper Script, Schrader SMD3MA4 encoding and python modifications by Lord Daikon
    echo Massive thanks for help wih signals analysis, python fixes, and overall wisdom from Jimilinux
    echo PMV-107J and tools from https://github.com/triq-org/tx_tools
    echo Citroen, and Ford from https://github.com/cdeletre/txtpms/
    echo subghz_ook_to_sub.py by https://github.com/evilpete/flipper_toolbox
    echo Utilizes GNUradio, rtl_433, sox and python 3.10. Use Ubuntu, Debian stable has issues
    echo
    echo Is there a better way to do this? Probably, but it works.
    echo If I missed crediting someone please let me know

    exit 1
    ;;
   
esac

