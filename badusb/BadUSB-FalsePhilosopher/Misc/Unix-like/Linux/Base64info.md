#encode term
echo  'linuxhint.com' | base64
#
#encode file(useful for multiple bracked strings that don't work using echo)
base64 sample.txt
#
#base 64 exec
base64 -d <<< base64string | sh
#
