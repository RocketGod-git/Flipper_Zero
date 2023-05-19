#!/usr/bin/env python

"""
Coding based on rtl_433 device source code from  https://github.com/merbanan/rtl_433
rtl_433/src/devices/tpms_renault.c
"""

from binascii import unhexlify,hexlify
from struct import pack,unpack_from
import argparse
from lib.crc import crc8
import os

"""
 Default values
 based on test file: https://github.com/merbanan/rtl_433_tests/raw/master/tests/Renault_TPMS/gfile070.cu8
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : @0.214588s
model     : Renault      type      : TPMS          id        : 87f293
flags     : 34           pressure_kPa: 202.5 kPa   temperature_C: 25 C       mic       : CRC
"""
home_directory = os.path.expanduser( '~' )

MODEL='Renault'

SENSORID=int('142f67',16)
PRESSURE=261
TEMPERATURE=24
FLAGS=int('36',16)
UNKNOWN=0xffff

# Manchester levels
HIGH = 0xff
LOW = HIGH ^ HIGH
MMODE='manch' # diffmanch | manch
NBYTES=9

def get_payload(sensorid=SENSORID,pressure=PRESSURE,temperature=TEMPERATURE,flags=FLAGS,unknown=UNKNOWN):

  int_payload = 0x00

  int_payload = int_payload << 6

  int_payload += flags & 0x7f

  int_payload = int_payload << 2

  int_payload += (int(pressure / 0.75) >> 8) & 0x3

  int_payload = int_payload << 8

  int_payload += int(pressure / 0.75) & 0xff

  int_payload = int_payload << 8

  int_payload += int( temperature + 30 ) & 0xff

  int_payload = int_payload << 24

  int_payload += sensorid & 0xffffff

  int_payload = int_payload << 16

  int_payload += unknown & 0xffff

  payload = pack('>Q',int_payload)

  crc = crc8(payload,8)

  payload += pack('<B',crc)

  return payload

def get_manchester(payload):

  # sync '0000 0000 0 0101 0101  0101 0101  0101 0101  0101 0110'
  manchester = pack('<39B',* [LOW] * 7 + [LOW,HIGH] * 14 + [LOW,HIGH,HIGH,LOW] )

  #for i,c in enumerate(payload):
  #  byte = ord(c)
  for byte in unpack_from('<%dB' % NBYTES,payload):
    for i in range(8):
      if byte & 0x80:
        manchester += pack('<2B', HIGH, LOW)
      else:
        manchester += pack('<2B', LOW, HIGH)

      byte = (byte << 1) & 0xff

  # trailing '0000'
  manchester += pack('<4B', *[LOW]*4)

  return manchester

def main():

  parser = argparse.ArgumentParser(description='Generate Renault TPMS symbols (manchester)')
  parser.add_argument('-i','--sensor-id',metavar='SENSOR-ID',default=hex(SENSORID)[2:],
                      help='Sensor ID, 4 bytes id, hex string (default: %s )' % hex(SENSORID)[2:] )

  parser.add_argument('-p','--pressure',metavar='PRESSURE',default=PRESSURE,type=float,
                      help='Pressure, PSI (default: %s)' % PRESSURE)

  parser.add_argument('-t','--temperature',metavar='TEMPERATURE',default=TEMPERATURE,type=int,
                      help='Temperature, Celcius, -50 to 205 (default: %d)' % TEMPERATURE)

  parser.add_argument('-f','--flags',metavar='FLAGS',default=FLAGS,type=int,
                      help='6 bits Flags (default: %d)' % FLAGS)

  parser.add_argument('-u','--unknown',metavar='UNKNOWN',default=UNKNOWN,type=int,
                      help='2 bytes Unknown (default: %d)' % UNKNOWN )

  parser.add_argument('-o','--output-file',metavar='OUTPUT-FILE',
                      help='Output file. Will be automatically genereated if not provided')

  args = parser.parse_args()

  output_file = ''

  if args.output_file is None:
    output_file = '%s.u8' % (MODEL)
  else:
    output_file = args.output_file

  payload = get_payload(int(args.sensor_id,16),args.pressure,args.temperature,args.flags,args.unknown)

  print(('payload = %s' % hexlify(payload)))

  manchester = get_manchester(payload)

  print(( 'manchester = %s' % str (manchester).replace('\xff','1').replace('\x00','_') ))

  f = open(os.path.join( home_directory, 'TPMS', 'Output', output_file),'wb')
  f.write(manchester)

  print(('signal written to %s' % output_file))

if __name__ == '__main__':
    exit(main())
