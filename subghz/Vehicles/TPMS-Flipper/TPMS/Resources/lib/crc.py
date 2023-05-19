#!/usr/bin/env python

"""
  Port of C crc8 function from rtl_433 util
  https://github.com/merbanan/rtl_433/blob/master/src/util.c
"""

def crc8(message,nBytes,polynomial=0x07,init=0x00):
  remainder = init
  nBytes = bytes(nBytes)
  for byte in nBytes:
    remainder ^= message[byte]
    for bit in range(8):
      if(remainder & 0x80):
        remainder = (remainder << 1)  ^ polynomial
      else:
        remainder = (remainder << 1)
    remainder = remainder & 0xff

  return remainder
