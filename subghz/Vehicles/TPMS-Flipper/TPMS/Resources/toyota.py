import time
import os
from lib.crc import crc8
from bitstring import BitArray

#home_directory = os.path.expanduser( '~' )

MODEL='Toyota'

PRESSURE=int((33.5 + 7)*4)
TEMP=int(25 + 40)
State = int('0', 16)

    
def main():
        
    id = input('What is the 8 digit hex ID?\n')
    id = int('f0d681a0', 16)
    
    start= str(100001)
    device= format((id), '032b')
    psi= format((PRESSURE), '08b')
    t = int(psi, 2)
    inverse_s = t ^ (2 ** (len(psi) + 1) - 1)
    invpsi = bin(inverse_s)[3 : ]
    temp= format((TEMP), '08b')
    s= format((State), '07b')
    
    payload= device + str(1) + psi + temp + s + invpsi
    
    print('Payload = %s' % payload)
    
    crc_bytes = int(payload, 2).to_bytes(len(payload) // 8, byteorder='big')
    
    print(crc_bytes)
    
    crc = crc8(crc_bytes,8,0x7,0x80)
    print(crc)
    
    check = format((crc), '08b')
    
    payload=BitArray(bin=start + device + str(1) + psi + temp + s + invpsi + check)
    
    print('Payload = %s' % payload.bin)
  
if __name__ == '__main__':
    exit(main())
