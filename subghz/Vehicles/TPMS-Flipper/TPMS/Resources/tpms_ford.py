#!/usr/bin/env python

"""
Coding based on rtl_433 device source code from  https://github.com/merbanan/rtl_433
rtl_433/src/devices/tpms_renault.c
"""

from binascii import unhexlify,hexlify
from struct import pack,unpack_from
import argparse
import os

"""
 Default values
 based on test file: https://github.com/merbanan/rtl_433_tests/raw/master/tests/Ford_TPMS/gfile059.cu8
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : @0.184300s
model     : Ford         type      : TPMS          id        : 45bb320f
code      : 6ad446       mic       : CHECKSUM
"""
home_directory = os.path.expanduser( '~' )

MODEL='Ford'

SENSORID=int('6ad446',16)
PRESSURE=int('23',16)
TEMPERATURE=int('cb',16)
FLAGS=int('46',16)
UNKNOWN=0xffff

# Manchester levels
HIGH = 0xff
LOW = HIGH ^ HIGH
MMODE='manch' # diffmanch | manch
NBYTES=8

def get_payload(sensorid=SENSORID,pressure=PRESSURE,temperature=TEMPERATURE,flags=FLAGS):

  int_payload = 0x00

  int_payload = int_payload << 32

  int_payload += sensorid & 0xffffffff

  int_payload = int_payload << 8

  int_payload += int(pressure) & 0xff

  int_payload = int_payload << 8

  int_payload += int(temperature) & 0xff

  int_payload = int_payload << 8

  int_payload += int(flags) & 0xff

  int_payload = int_payload << 8

  payload = pack('>Q',int_payload)

  payload = payload[:-1]

  checksum = sum(unpack_from('<7B',payload)) & 0xff

  payload += pack('<B',checksum)

  return payload

def get_manchester(payload):
        
  # sync '0101 0101  0101 0101  0101 0101  0101 0110'
  manchester = pack('<32B',* [LOW,HIGH] * 14 + [LOW,HIGH,HIGH,LOW] )

  #for i,c in enumerate(payload):
  #  byte = ord(c)
  for byte in unpack_from('<%dB' % NBYTES,payload):
    for i in range(8):
      if byte & 0x80:
        manchester += pack('<2B', HIGH, LOW)
      else:
        manchester += pack('<2B', LOW, HIGH)

      byte = (byte << 1) & 0xff

  return manchester

def main():

  parser = argparse.ArgumentParser(description='Generate Renault TPMS symbols (manchester)')
  parser.add_argument('-i','--sensor-id',metavar='SENSOR-ID',default=hex(SENSORID)[2:],
                      help='Sensor ID, 4 bytes id, hex string (default: %s )' % hex(SENSORID)[2:] )

  parser.add_argument('-p','--pressure',metavar='PRESSURE',default=PRESSURE,type=int,
                      help='RAW pressure (default: %s)' % hex(PRESSURE))

  parser.add_argument('-t','--temperature',metavar='TEMPERATURE',default=TEMPERATURE,type=int,
                      help='RAW temperature (default: %s)' % hex(TEMPERATURE))

  parser.add_argument('-f','--flags',metavar='FLAGS',default=FLAGS,type=int,
                      help='RAW flags (default: %s)' % hex(FLAGS))

  parser.add_argument('-o','--output-file',metavar='OUTPUT-FILE',
                      help='Output file. Will be automatically genereated if not provided')

  args = parser.parse_args()

  output_file = ''

  if args.output_file is None:
    output_file = '%s.u8' % (MODEL)
  else:
    output_file = args.output_file

  payload = get_payload(int(args.sensor_id,16),args.pressure,args.temperature,args.flags)

  print(('payload = %s' % hexlify(payload)))

  manchester = get_manchester(payload)

  print(( 'manchester = %s' % str(manchester).replace('\xff','1').replace('\x00','_') ))

  f = open(os.path.join( home_directory, 'TPMS', 'Output', output_file),'wb')
  f.write(manchester)

  print(('signal written to %s' % output_file))

if __name__ == '__main__':
    exit(main())
