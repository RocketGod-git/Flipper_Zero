#!/usr/local/bin/python3
"""
    Generates NFC with a telephone number and saves to a Flipper NFC "save" file
    No Guarantees.

    ./nfc_gen_phone.py 8185551222 +1
    requires ndeflib

    Original Code by: Peter Shipley github.com/evilpete
    Modified by: Sage https://github.com/misusage

    From pkg https://github.com/evilpete/flipper_toolbox
"""

import sys
import ndef

# for debuging
verbose = 0

nfc_header = """Filetype: Flipper NFC device
Version: 2
# generated with flipper_toolbox
Device type: NTAG215
# UID, ATQA and SAK are common for all formats
UID: 04 10 56 01 74 48 03
ATQA: 44 00
SAK: 00
# Mifare Ultralight specific data
Signature: A5 80 A4 CC A0 C3 A1 F6 8B BE 6F EE 83 A6 B9 EE 36 F8 FB C8 14 5A 23 AA 29 DB 78 56 07 B9 6B 92
Mifare version: 00 04 04 02 01 00 11 03
Counter 0: 0
Tearing 0: 00
Counter 1: 0
Tearing 1: 00
Counter 2: 0
Tearing 2: 00
Pages total: 135
"""

data_static = [
    0x04, 0x10, 0x56, 0xCA,     # 01 serial number
    0x01, 0x74, 0x48, 0x03,     # 02 serial number
    0x3E, 0x48, 0x00, 0x00,     # 03 serial number, internal, lock bytes, lock bytes
    0xE1, 0x10, 0x3E, 0x00,     # 04 Capability Container
]

conf_pages = [
    0x00, 0x00, 0x00, 0xBD,      # 130
    0x04, 0x00, 0x00, 0xFF,      # 131
    0x00, 0x05, 0x00, 0x00,      # 132
    0x00, 0x00, 0x00, 0x00,      # 133
    0x00, 0x00, 0x00, 0x00,      # 134
]


def print_nfc_sub(t_data, file=sys.stdout):

    print(nfc_header, end='', file=file)

    p = 0
    for x in range(0, 540, 4):
        print(f"Page {p}: {t_data[x]:02X} {t_data[x + 1]:02X} "
              f"{t_data[x + 2]:02X} {t_data[x + 3]:02X}", file=file)
        p = p + 1


def write_nfc_sub(t_data):

    print(nfc_header, end='', file=f)

    p = 0
    for x in range(0, 540, 4):
        print(f"Page {p}: {t_data[x]:02X} {t_data[x + 1]:02X} "
              f"{t_data[x + 2]:02X} {t_data[x + 3]:02X}", file=f)
        p = p + 1


def gen_nfc_sub(tag_data):

    tag_message = []
    data_list = []

    for x in tag_data:
        if x[0] == 'url':
            tag_message.append(ndef.UriRecord(x[1]))

        if verbose:
            print(x, file=sys.stderr)
            print(tag_message[-1:], file=sys.stderr)

    buf = b"".join((ndef.message_encoder(tag_message)))

    m_len = len(buf)

    if verbose:
        print("buf", m_len, hex(m_len), buf, file=sys.stderr)

    data_list.extend(data_static)
    data_list.append(3)         # Message Flags
    data_list.append(m_len)         # Type Length
    data_list.extend(list(buf))

    data_list.append(0xFE)      # end of Data

    data_len = len(data_list)

    if verbose:
        print("data_list", data_len, data_list, file=sys.stderr)

    x = 520 - data_len
    data_list.extend([0] * x)
    data_list.extend(conf_pages)

    return data_list


if __name__ == '__main__':

    filename = "call-me.nfc"
    telstr = "tel:"
    arg_data = []

    for a in sys.argv[1:]:
        if a.isdigit():

            for b in sys.argv[2:]:
                if b.startswith("+"):
                    a = b + a
                else:
                    exit

            a = str(telstr) + a #add the tel: nfc code
            arg_data.append(("url", a))

            #for i in arg_data:
            #    print(i, end = ' ')
            #print("\n")
        else:
            exit

    if not arg_data:
        print("requires two URL arguments\n"
              "Please provide phone number with area code THEN the +country-code.\n"
              f"{sys.argv[0]} 12345679876 +1")
        sys.exit()

    nfc_data = gen_nfc_sub(arg_data)

    print_nfc_sub(nfc_data)

    if verbose:
        for i in arg_data:
            print(i[0],i[1])
        print_nfc_sub(nfc_data)
    else:
        with open(filename, mode='w') as f:
            write_nfc_sub(nfc_data)
            print("\nDone! NFC File has been created: " + filename)

    sys.exit()
