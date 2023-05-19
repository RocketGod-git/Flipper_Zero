import time
import crcmod
import os

home_directory = os.path.expanduser( '~' )

def differential_manchester_encode(s):
        last_bit = 0
        state = 0
        result = []
        for sbit in s:
                bit = 0
                if sbit == '1': bit = 1
                if bit == last_bit:
                        result.append('10')
                        state=0
                else:
                        result.append('01')
                        state=1
                last_bit = state
        return ''.join(result)


def main():

    crc8 = crcmod.mkCrcFun(0x113, rev=False, initCrc=0, xorOut=0)

    # TPMS sensor 7 hex digit ID as printed on the sensor
    id = input('What is the 7 digit hex ID?\n')
    id = int(id, 16)
    device = format((id), '028b')

    # Battery low if set
    battlow = '0'

    # Counter (two bits counts 1,2,3)
    ctr = format(0x3, '02b')

    # Must be zero for packet to be recognized
    mustbezero = '0'
    # Ignored bit, sensor sets this to 0
    ignored = '0'
    # Fault indicator of some sort (if 1 TPMS light starts flashing and values are ignored)
    fault = '0'

    # Tire pressure in PSI/0.363 + 40 constant added or
    # kPa/2.48 + 40 constant added
    pressure = 0/0.363 + 40
    pressureint = int(pressure + 0.5)
    pressurebits = format(pressureint, '08b')
    pressureinvbits = format(pressureint^0xff, '08b')

    # Temperature in Celsius with a constant 40 added (resulting range -40 to 215C)
    temperature = format(42 + 40, '08b')

    # Assemble the complete payload to calculate CRC
    payload = device + battlow + ctr + mustbezero + ignored + fault + pressurebits + pressureinvbits + temperature

    # Pad payload to make it even 8 bits (won't affect CRC8 as long as it's done in front)
    padpayload = '000000'+payload
    crc_bytes = int(padpayload, 2).to_bytes(len(padpayload) // 8, byteorder='big')
    calculated_crc = crc8(crc_bytes[0:8])
    crc_bits = format(calculated_crc, '08b')

    bitstream = '00000000000000001111110' + differential_manchester_encode('1'+payload+crc_bits+'1') + '000000'
    
    f = open(os.path.join( home_directory, 'TPMS', 'Output', 'test.txt'),"w")
    f.write("[_ (8000us) ]\n[0 (-40kHz 100us) ]\n[1 (40kHz 100us) ]\n\n\n_ _ _\n%s" % bitstream) 
            
    print('bitstream = %s' % bitstream)

if __name__ == '__main__':
    main()
