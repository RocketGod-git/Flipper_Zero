#!/usr/local/bin/python3

"""
    Reads: proxmark3 MiFare json dump files
    Outputs: Flipper NFC compatable format

    nfc_prox2flip.py test_dat/mf-classic-1k-23AD7C86.json > mfc1k-23AD7C86.nfc

    Written By: Peter Shipley github.com/evilpete

    From pkg https://github.com/evilpete/flipper_toolbox
"""

import sys
import json


# Nfc device type can be UID, Mifare Ultralight, Mifare Classic, Bank card
# ATQA SAK
CARD_TYPE = {
    ("0400", "08"): "Mifare Classic",      # 1k
    ("0200", "18"): "Mifare Classic",      # 1k
    ("0400", "09"): "Mifare Mini",
    ("4400", "00"): "Mifare Ultralight",   # "NTAG213" "NTAG216"
    ("4400", "20"): "Bank card",
    ("4403", "20"): "Mifare DESFire",
}


def convert_dat(in_dat):
    """
        Take a parsed proxmark json dump arg
        returns list in Flipper NFC compatable format
    """

    # output list
    out_dat = []

    x = in_dat["Card"]

    # Guess card type by looking at ATQA/SAK combo
    j = (x['ATQA'], x['SAK'])

    t = CARD_TYPE.get(j, x['UID'])

    # this is a hack to generate Key maps
    # should add code to actually parse "SectorKeys"
    y = len(in_dat["SectorKeys"])
    s = int("1" * y, 2)
    ska = skb = f"{s:016X}"

    out_dat.append(f"""
Filetype: Flipper NFC device
Version: 2
# generated with flipper_toolbox
# Nfc device type can be UID, Mifare Ultralight, Mifare Classic, Bank card
Device type: {t}
# UID, ATQA and SAK are common for all formats
UID: {x['UID'][0:2]} {x['UID'][2:4]} {x['UID'][4:6]} {x['UID'][6:8]}
ATQA: {x['ATQA'][0:2]} {x['ATQA'][2:4]}
SAK: {x['SAK']}
# Mifare Classic specific data
Mifare Classic type: 1K
Data format version: 1
# Key map is the bit mask indicating valid key in each sector
Key A map: {ska}
Key B map: {skb}
# Mifare Classic blocks""")

    # Loop through blocks spliting data into 1 byte pieces
    for k, v in in_dat["blocks"].items():
        b = " ".join([v[i:i + 2] for i in range(0, len(v), 2)])
        out_dat.append(f"Block {k}: {b}")

    return out_dat


if __name__ == '__main__':

    in_filename = "test_dat/mf-classic-1k-23AD7C86.json"

    if len(sys.argv) > 2:
        in_filename = int(sys.argv[2])

    with open(in_filename, encoding="utf-8") as fd:
        input_dat = json.load(fd)

    output_list = convert_dat(input_dat)

    print("\n".join(output_list))

    sys.exit()
