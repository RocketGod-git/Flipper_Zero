#!/usr/bin/env python3

import sys

#
#  Generate Insteon command packets in Flipper .sub format
#
# Peter Shipley github.com/evilpete
#
# From pkg https://github.com/evilpete/flipper_toolbox
#

# Usage;
#      ./subghz_insteon.py <dst_node_addr> <src_node_addr> [On|Off]
#
# Example:
#      ./subghz_insteon.py 163FE5 132580 Off > device_off.sub
#


# Insteon Packet encoding format :
#
#    Packet encoding example
#
#    The short Packet Fields are
#        Flags     = byte 0
#        To Addr   = byte 1 2 3
#        From Addr = byte 4 5 6
#        Command   = byte 7
#        Cmd Arg   = byte 8
#        Pkt CRC   = byte 9
#        pad 00    = byte 10 11 ( optional )
#        pad AA    = byte 12    ( optional )
#

_debug = 1

lsfr_table = [0x00, 0x30, 0x60, 0x50,  # 0 1 2 3
              0xC0, 0xF0, 0xA0, 0x90,  # 4 5 6 7
              0x80, 0xB0, 0xE0, 0xD0,  # 8 9 A B
              0x40, 0x70, 0x20, 0x10]  # C D E F


def pkt_crc(dat):
    """
        calc packet CRC

        takes an instion packet in form of a list of ints
        and returns the CRC for RF packet

        This uses a table lookup to effectivly doing:
            r ^= dat[i] ;
            r ^= (( r ^ ( r << 1 )) & 0x0F) << 4 ;

    """

    r = 0
    for i in dat[:9]:
        r ^= i
        r ^= lsfr_table[r & 0x0F]

    return r


def percent_to_byte(p_str, def_val=255):
    if p_str.isdigit():
        p = int(p_str)
        r = int(p * 255 / 100)
        return min(r, 255)

    return def_val


def insteon_encode(b_list):
    # l = len(b_list)

    # print("cmd_hex", cmd_hex)
    aa = ''.join(['10' if b == '1' else '01' for b in "01010101"])
    blks = [aa]
    i = 0
    for x in b_list:
        if i == 0:
            ix = 31
        else:
            ix = 12 - i
        i += 1

        d = x

        ibr = f"{ix:05b}"[::-1]
        dbr = f"{d:08b}"[::-1]

        if _debug > 1:
            print("00", ibr, dbr, " : ", ix, f"{x:02X}", file=sys.stderr)

        # ib = f"{ix:05b}"
        # db = f"{d:08b}"
        # print(ix, cmd_hex[x:x+2], ib, db, '->', ibr, dbr)

        md = ''.join(['10' if b == '1' else '01' for b in f"{ibr}{dbr}"])
        if _debug > 1:
            print("md=", md, file=sys.stderr)
        blks.append('00' + md)

    inst_pkt = ''.join(blks)

#    if _debug:
#        print(cmd_hex)
#        print("blks =", blks)
#        print("     =", inst_pkt)
#        print("AA = ", aa)
#        print([inst_pkt, aa * 10, inst_pkt])

    return inst_pkt


def gen_insteon_pkt():

    pkt_list = [0x0F]

    args = sys.argv[1:]

    if _debug > 1:
        print("args", args, file=sys.stderr)

    if len(args) < 3:
        print("requires three or more args")
        sys.exit()

    # dest addr
    addr = args.pop(0)
    a = [addr[4:6], addr[2:4], addr[0:2]]
    # pkt_list.extend([int(x, 16) for x in a])
    pkt_list.extend(map(lambda x: int(x, 16), a))

    # src addr
    addr = args.pop(0)
    a = [addr[4:6], addr[2:4], addr[0:2]]
    pkt_list.extend(map(lambda x: int(x, 16), a))
    # pkt_list.extend([int(x, 16) for x in a])

    cmd = args.pop(0)
    if cmd.upper() in ["ON", "DIM"]:
        pkt_list.append(0x11)

        val = 0xFF
        if args:
            arg = args.pop(0)
            if arg.isdigit():
                val = int(arg)
            elif arg[0] == '%':
                val = percent_to_byte(arg[1:])
            else:
                print(f"unknown value '{arg}'")
                sys.exit()

        pkt_list.append(val)

    elif cmd.upper() == "OFF":
        pkt_list.append(0x13)
        pkt_list.append(0x00)

    else:
        print(f"unknown value '{cmd}'")
        sys.exit()

    p_crc = pkt_crc(pkt_list)

    pkt_list.extend([p_crc, 0, 0, 0xAA])

    if _debug > 1:
        print("pkt_list", pkt_list, file=sys.stderr)
        # hex_str_list = [f"{x:02X}" for x in pkt_list]
        hex_str_list = list(map(lambda x: f"{x:02X}", pkt_list))
        print(hex_str_list, file=sys.stderr)
        print("".join(hex_str_list), file=sys.stderr)

    return pkt_list


def print_subfile(pkt_bits, note="Insteon Command"):

    pkt_bit_len = 109.6

    bit_len = int(pkt_bit_len)
    bit_len_off = pkt_bit_len % 1
    delta_off = 0.0

    data = []
    prevbit = None
    prevbitlen = 0

    for bit in pkt_bits:
        if prevbit and prevbit != bit:
            data.append(prevbitlen)
            prevbitlen = 0

        if bit == '1':
            delta_off += bit_len_off
            prevbitlen += bit_len
            if delta_off > 1:
                prevbitlen += 1
                delta_off -= 1
        else:
            delta_off += bit_len_off
            prevbitlen -= bit_len
            if delta_off > 1:
                prevbitlen -= 1
                delta_off -= 1

        prevbit = bit

    data.append(prevbitlen)

    # print("data", len(data))

    hdr = f"""Filetype: Flipper SubGhz RAW File
Version: 1
# {note}
# Generated with subghz_insteon.py https://github.com/evilpete/flipper_toolbox
Frequency: 915030000
Preset: FuriHalSubGhzPreset2FSKDev476Async
Protocol: RAW
"""

    res = hdr
    datalines = []
    for i in range(0, len(data), 512):
        # batch = [str(n) for n in data[i:i + 512]]
        batch = map(str, data[i:i + 512])
        datalines.append(f'RAW_Data: {" ".join(batch)}')
    res += '\n'.join(datalines)

    return res


if __name__ == '__main__':

    p_list = gen_insteon_pkt()

    hexstr = ' '.join([f"{x:02X}" for x in p_list])

    if _debug:
        print("p_list", p_list, file=sys.stderr)
        # print([f"{x:02X}" for x in p_list], file=sys.stderr)
        print(hexstr, file=sys.stderr)

    pkt_data = insteon_encode(p_list)

    if _debug > 1:
        print("pkt_data", pkt_data, file=sys.stderr)

    file_comment = "Insteon command : " + \
                   ' '.join(sys.argv[1:])  + " : " + hexstr

    fdata = print_subfile(pkt_data, note=file_comment)

    print(fdata)

    sys.exit()
