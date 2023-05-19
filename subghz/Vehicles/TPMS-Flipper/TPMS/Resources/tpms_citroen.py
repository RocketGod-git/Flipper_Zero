#!/usr/bin/env python

"""
Coding based on rtl_433 device source code from  https://github.com/merbanan/rtl_433
rtl_433/src/devices/tpms_citroen.c
"""

from binascii import unhexlify,hexlify
from struct import pack,unpack_from
import argparse
import os

"""
 Default values
 based on test file: https://github.com/merbanan/rtl_433_tests/raw/master/tests/Citroen_TPMS/gfile001.cu8
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : @0.198304s
model     : Citroen      type      : TPMS          state     : d2            id        : 8add48d4
flags     : 0            repeat    : 1             Pressure  : 289 kPa       Temperature: 23 C         maybe_battery: 14         mic       : CHECKSUM
"""
home_directory = os.path.expanduser( '~' )

MODEL='Citroen'

SENSORID=int('8add48d4',16)
PRESSURE=10
TEMPERATURE=23
STATUS=int('d2',16)
FLAGS=0
REPEAT=1
BATTERY=14

# Manchester levels
HIGH = 0xff
LOW = HIGH ^ HIGH
MMODE='manch' # diffmanch | manch
NBYTES=10

def get_payload(sensorid=SENSORID,pressure=PRESSURE,temperature=TEMPERATURE,state=STATUS,flags=FLAGS,repeat=REPEAT,battery=BATTERY):

  int_payload = 0x00

  int_payload = int_payload << 8

  int_payload += sensorid & 0xffffffff

  int_payload = int_payload << 4

  int_payload += flags & 0xf

  int_payload = int_payload << 4

  int_payload += repeat & 0xf

  int_payload = int_payload << 8

  int_payload += int( pressure / 1.364 ) & 0xff

  int_payload = int_payload << 8

  int_payload += int( temperature + 50 ) & 0xff

  int_payload = int_payload << 8

  int_payload += battery & 0xff

  payload = pack('>Q',int_payload)

  checksum = 0x00

  for byte in unpack_from('<8B',payload):
    checksum ^= byte

  payload = pack('<B', state & 0xff) + payload + pack('<B',checksum)

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

  # trailing '01111110'
  manchester += pack('<8B', *[LOW]+ [HIGH] * 6 + [LOW])

  return manchester

def main():

  parser = argparse.ArgumentParser(description='Generate Citroen TPMS symbols (manchester)')
  parser.add_argument('-i','--sensor-id',metavar='SENSOR-ID',default=hex(SENSORID)[2:],
                      help='Sensor ID, 4 bytes id, hex string (default: %s )' % hex(SENSORID)[2:] )

  parser.add_argument('-p','--pressure',metavar='PRESSURE',default=PRESSURE,type=float,
                      help='Pressure, PSI (default: %s)' % PRESSURE)

  parser.add_argument('-t','--temperature',metavar='TEMPERATURE',default=TEMPERATURE,type=int,
                      help='Temperature, Celcius, -50 to 205 (default: %d)' % TEMPERATURE)

  parser.add_argument('-s','--status',metavar='STATUS',default=STATUS,type=int,
                      help='Status, 8 bits unsigned integer (default: %d)' % STATUS)

  parser.add_argument('-f','--flags',metavar='FLAGS',default=FLAGS,type=int,
                      help='4 bits Flags (default: %d)' % FLAGS)

  parser.add_argument('-r','--repeat',metavar='REPEAT',default=REPEAT,type=int,
                      help='Repeat counter 0 to 4 (default: %d)' % REPEAT)

  parser.add_argument('-b','--battery',metavar='BATTERY',default=BATTERY,type=int,
                      help='Battery (default: %d)' % BATTERY)

  parser.add_argument('-o','--output-file',metavar='OUTPUT-FILE',
                      help='Output file. Will be automatically genereated if not provided')


  args = parser.parse_args()

  output_file = ''

  if args.output_file is None:
    output_file = '%s%s.u8' % (MODEL,args.repeat)
  else:
    output_file = args.output_file

  payload = get_payload(int(args.sensor_id,16),args.pressure,args.temperature,args.status,args.flags,args.repeat,args.battery)

  print(('payload = %s' % hexlify(payload)))

  manchester = get_manchester(payload)

  print(( 'manchester = %s' % str(manchester).replace('\xff','1').replace('\x00','_') ))
    
  f = open(os.path.join( home_directory, 'TPMS', 'Output', output_file),'wb')
  f.write(manchester) 

  print(('signal written to %s' % output_file))

if __name__ == '__main__':
    exit(main())
