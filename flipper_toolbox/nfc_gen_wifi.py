#!/usr/local/bin/python3
"""
    Generates NFC with WiFi network data and saves to a Flipper NFC "save" file
    No Guarantees.

    ./nfc_gen_wifi.py
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

    mac = "FF:FF:FF:FF:FF:FF"
    data_list = []
    credential = ndef.wifi.Credential()
    credential.set_attribute('network-index', 1)

    for x in tag_data:
        if x[0] == 'ssid':
            ssidStr = bytes(x[1], encoding="utf-8")
            credential.set_attribute(x[0], ssidStr)
        elif x[0] == 'authentication-type':
            credential.set_attribute(x[0], x[1])
        elif x[0] == 'encryption-type':
            credential.set_attribute(x[0], x[1])
        elif x[0] == 'network-key':
            keyStr = bytes(x[1], encoding="utf-8")
            credential.set_attribute(x[0], keyStr)
        elif x[0] == 'mac-address':
            mac = bytes.fromhex(mac.replace(':', ''))
            credential.set_attribute(x[0], mac)

    record = ndef.wifi.WifiSimpleConfigRecord()
    record.name = 'my config token'
    record.set_attribute('credential', credential)

    for x in tag_data:
        if x[0] == 'rf-bands':
            record.set_attribute(x[0], x[1])

    buf = b"".join((ndef.message_encoder([record])))
    m_len = len(buf)

    data_list.extend(data_static)
    data_list.append(3)         # Message Flags
    data_list.append(m_len)         # Type Length
    data_list.extend(list(buf))
    data_list.append(0xFE)      # end of Data

    data_len = len(data_list)
    
    if verbose:
        print("Verbose Mode ON")
        for b in tag_data:
            print(b, file=sys.stderr)
        print("Broadcast Mac: " + str(mac))
        print("WiFi Credential Token: " + str(credential))
        print(record)
        print("Buffer:", m_len, hex(m_len), buf, file=sys.stderr)
        print("Data List:", data_len, data_list, file=sys.stderr)

    x = 520 - data_len
    data_list.extend([0] * x)
    data_list.extend(conf_pages)

    return data_list


if __name__ == '__main__':

    filename = "WiFi.nfc"
    arg_data = []

    print("NFC WiFi Tag Generator for the Flipper Zero\n"
          "###########################################\n")
    ssid = input("What is the SSID?: ")
    arg_data.append(("ssid", ssid))

    print("Choose an Authentication Type:")
    authChoice = input("Enter 1 for WPA/WPA2-Personal\nEnter 2 for WPA/WPA2-Enterprise (might not work)\n> ")
    if authChoice == "1":
        auth = "WPA2-Personal"
        arg_data.append(("authentication-type", auth))
    elif authChoice == "2":
        auth = "WPA2-Enterprise"
        arg_data.append(("authentication-type", auth))
    else:
        print("ERROR: You typed something else. Exiting...")
        sys.exit()
  
    print("\nChoose an Encryption Type:")    
    encChoice = input("Enter 1 for AES (Select this option if you don't know)\nEnter 2 for TKIP\n> ")
    if encChoice == "1":
        encryption = "AES"
        arg_data.append(("encryption-type", encryption))
    elif encChoice == "2":
        encryption = "TKIP"
        arg_data.append(("encryption-type", encryption))
    else:
        print("ERROR: You typed something else. Exiting...")
        sys.exit()

    password = input("\nWhat is the WiFi Password?: ")
    arg_data.append(("network-key", password))

    print("\nWhat WiFi Band is the network operating on?:")    
    bandChoice = input("Enter 1 for 2.4GHz\nEnter 2 for 5.0GHz\n> ")
    if bandChoice == "1":
        band = "2.4GHz"
        arg_data.append(("rf-bands", band))
    elif bandChoice == "2":
        band = "5.0GHz"
        arg_data.append(("rf-bands", band))
    else:
        print("ERROR: You typed something else. Exiting...")
        sys.exit()

    nfc_data = gen_nfc_sub(arg_data)

    if verbose:
        for i in arg_data:
            print(i[0],i[1])
        print_nfc_sub(nfc_data)
    else:
        with open(filename, mode='w') as f:
            write_nfc_sub(nfc_data)
            print("\nCreated " + filename)

    sys.exit()
