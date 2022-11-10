#!/usr/bin/env python3

#
#       A command line bases generator for  Flipper SubGhz RAW File
#
# Peter Shipley github.com/evilpete
#
# From pkg https://github.com/evilpete/flipper_toolbox
#
# Based heavily on jinschoi/create_sub.py
#
# https://gist.github.com/jinschoi/f39dbd82e4e3d99d32ab6a9b8dfc2f55
#
#

import sys
# import os
# from typing import Iterable, Union, Any
import argparse

# pylint: disable=unspecified-encoding, too-many-arguments, too-many-locals, unused-argument

_verbose = 0

# Preset: FuriHalSubGhzPreset2FSKDev238Async
# Preset: FuriHalSubGhzPreset2FSKDev476Async
# Preset: FuriHalSubGhzPresetOok270Async
# Preset: FuriHalSubGhzPresetOok650Async        <Default>
# listed in Firmware but not avalible (yet)
#    FuriHalSubGhzPresetMSK99_97KbAsync
#    FuriHalSubGhzPresetGFSK9_99KbAsync


def gen_sub(freq, zerolen, onelen, baudrate=None, pause=0, bits="", modu='Ook', modopt=650):
    """generate Flipper SubGhz RAW data

        Parameters
        ----------
        int : freq
            frequency in Hz
        int : zerolen
            length of space bit in us
        int ; onelen
            length of mark bit in us
        int : baud
            baud rate, is given options zerolen and onelen are ignored
        int : repeats
            number of times to repeat sequence
        int : pause
            time to wait in us between sequence, defaults to value zerolen
        str : bits
            string of ones and zeros to represent sequence
        str : modu
            modulation, valid values 2FSK or Ook, default="Ook"
        str : modopt
            modulation option, valid values:
            Ook: '270' or '650'
            2FSK: Dev238' or 'Dev476

        Returns
        -------
        str
            binary data in string form

    """

    res = f"""Filetype: Flipper SubGhz RAW File
Version: 1
Frequency: {freq}
Preset: FuriHalSubGhzPreset{modu}{modopt}Async
Protocol: RAW
"""

    if baudrate is not None:
        zerolen = onelen = (1 / baudrate) * 1000000

#    if modu not in ['Ook', "2FSK"]:
#        raise ValueError("modu value can only be 'Ook' or '2FSK'")
#
#    if modu == 'Ook' and modopt not in ['270', '650']:
#        raise ValueError("Ook: modopt value can only be '270' or '650'")
#
#    if modu == '2FSK' and modopt not in ['Dev238', 'Dev476']:
#        raise ValueError("2FSK: modopt value can only be 'Dev238' or 'Dev476'")

    zerolen_off = zerolen % 1
    onelen_off = onelen % 1
    delta_off = 0.0

    zerolen = int(zerolen)
    onelen = int(onelen)

#    if _verbose:
#        print( f"zerolen={zerolen}, onelen={onelen}, baudrate={baudrate}, "
#              f"zerolen_off={zerolen_off:0.04f}, onelen_off={onelen_off:0.03f}" )

    if pause == 0:
        # Pause must be non-zero.
        pause = zerolen

    data = []
    prevbit = None
    prevbitlen = 0
    for bit in bits:
        if prevbit and prevbit != bit:
            data.append(prevbitlen)
            prevbitlen = 0

        if bit == '1':
            delta_off += onelen_off
            prevbitlen += onelen
            if delta_off > 1:
                prevbitlen += 1
                delta_off -= 1
        else:
            delta_off += zerolen_off
            prevbitlen -= zerolen
            if delta_off > 1:
                prevbitlen -= 1
                delta_off -= 1

        prevbit = bit

    if prevbit == '1':
        data.append(prevbitlen)
        data.append(-pause)
    else:
        data.append(prevbitlen - pause)

    # data = (data * repeats)[:-1] # Drop the last pause.
    datalines = []
    for i in range(0, len(data), 512):
        batch = [str(n) for n in data[i:i + 512]]
        datalines.append(f'RAW_Data: {" ".join(batch)}')

    res += '\n'.join(datalines)

    if _verbose > 1:
        print(f"delta_off {delta_off}")

    return res


def hex2bin(s):
    """Convert strings of Hedecimal data into binary strings

        Parameters
        ----------
        str
            hexadecimal data in string form

        Returns
        -------
        str
            binary data in string form

    """

    r = []
    if s[:2] in ["0x", "OX"]:
        s = s[2:]
    sl = len(s)
#    if (sl % 2):
#        s += '0'
    for i in range(0, sl, 1):
        b = "{:04b}".format(int(s[i], 16))  # pylint: disable=consider-using-f-string
        # print(s[i], b)
        r.append(b)
    return ''.join(r)


Modulation_Presets = {
    '2FSKDev238': ('2FSK', 'Dev238'),   # FuriHalSubGhzPreset2FSKDev238Async
    '2FSKDev476': ('2FSK', 'Dev476'),   # FuriHalSubGhzPreset2FSKDev476Async
    'Ook270':     ('Ook', '270'),       # FuriHalSubGhzPresetOok270Async
    'Ook650':     ('Ook', '650'),       # FuriHalSubGhzPresetOok650Async
}


def arg_line():
    """ Parse command line args.

        Parameters
        ----------
        None

        Returns
        -------
        argparse Namespace obj

    """
    # pylint: disable=global-statement
    global _verbose

    epilog  = f'''
    example:\n\t {sys.argv[0]} -f 302500000 -0 333 -1 333 -m -B 0110100001000
    \n\t {sys.argv[0]} -f 302500000 -b 3015 -m -H 0x6840  -p Ook650

    If baud is given options zerolen and onelen are ignored

    Modulation presets:
        2FSKDev238: FuriHalSubGhzPreset2FSKDev238Async
        2FSKDev476: FuriHalSubGhzPreset2FSKDev476Async
        Ook270:     FuriHalSubGhzPresetOok270Async
        Ook650:     FuriHalSubGhzPresetOok650Async
'''

    parser = argparse.ArgumentParser(add_help=True,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-v', '--verbose', dest="verb",
                        default=0,
                        help='Increase debug verbosity', action='count')

    parser.add_argument("-o", "--outfile", dest="out_file",
                        default="subghz.sub",
                        help="Output filename")

    parser.add_argument("-f", "--freq", dest="send_freq",
                        type=int,
                        default=433920000,
                        help="Transmit frequency")

    parser.add_argument("-0", "--zerolen", dest="zero_len",
                        type=int,
                        default=None,
                        help="Length of space bit in ms")

    parser.add_argument("-1", "--onelen", dest="one_len",
                        type=int,
                        default=None,
                        help="Length of mark bit in ms")

    parser.add_argument("-i", "--invert", dest="invert",
                        action='store_true',
                        help="Invert bits")

    parser.add_argument("-b", "--baud", dest="baud_rate",
                        type=int,
                        default=None,
                        help="data baud rate")

    data_grp = parser.add_mutually_exclusive_group(required=True)

    data_grp.add_argument("-H", "--Hex", dest="hex_data",
                          default=None,
                          help="Packet data in hex")

    data_grp.add_argument("-B", "--Binary", dest="bin_data",
                          default='None',
                          help="Packet data as string of ones and zeros")

    # Preset: FuriHalSubGhzPreset2FSKDev238Async
    # Preset: FuriHalSubGhzPreset2FSKDev476Async
    # Preset: FuriHalSubGhzPresetOok270Async
    # Preset: FuriHalSubGhzPresetOok650Async        <Default>
    parser.add_argument("-p", "--preset", dest="mod_preset",
                        default='Ook650',
                        help="Modulation preset")

    parser.add_argument("-m", "--manchester", dest="manch_encode",
                        action='store_true',
                        help="manchester encoded")

    parser.add_argument("-r", "--repeat", dest="repeat_cnt",
                        type=int, default=1,
                        help="number of times to repeat sequence")

    parser.add_argument("-d", "--delay", dest="delay_padding",
                        type=int, default=1,
                        help="delay padding between repeated sequences")

    args_data, _unknown_args = parser.parse_known_args()

    if args_data.verb:
        _verbose += args_data.verb

    if _verbose:
        print(f"\nargs: {args_data}\n")

    return args_data


def main():

    args = arg_line()
    zero_len = one_len = None

    if args.baud_rate is None:
        if args.zero_len and args.one_len:
            zero_len = args.zero_len
            one_len = args.one_len
        elif args.zero_len or args.one_len:
            zero_len = one_len = args.zero_len or args.one_len
        else:
            print("Error:  Bit Length or Baudrate must be given")
            print("\tuse --help opton for more info\n")
            # parser.print_help()
            sys.exit(1)

    mod_settings = ('Ook', '650')
    if args.mod_preset in Modulation_Presets:
        mod_settings = Modulation_Presets[args.mod_preset]

    if args.hex_data:
        bin_data = hex2bin(args.hex_data)
        if _verbose:
            print(f"hex_data: {args.hex_data}")
    else:
        bin_data = args.bin_data

    # print(f"bin_data: {bin_data}")

    if args.manch_encode:
        bin_data = ''.join(['10' if b == '1' else '01' for b in bin_data])

    if args.invert:
        bin_data = ''.join(['0' if b == '1' else '1' for b in bin_data])

    if _verbose:
        print(f"bin_data: {bin_data}")

    packet_data = gen_sub(args.send_freq,
                          zero_len, one_len, args.baud_rate, 0,
                          bin_data,
                          mod_settings[0], mod_settings[1])

    if _verbose > 1:
        print(f"packet_data: {packet_data}")

    with open(args.out_file, 'w', encoding="utf-8") as fd:
        print(packet_data, file=fd)

    sys.exit()


if __name__ == '__main__':
    main()
