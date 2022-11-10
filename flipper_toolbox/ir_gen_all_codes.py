#!/usr/bin/env python3
"""
    ir_gen_all_codes.py (was gen_all_ir_codes.py)
    Generates file Flipper IR file will all command codes

    Written By: Peter Shipley github.com/evilpete

    From pkg https://github.com/evilpete/flipper_toolbox
"""

import sys

CMD_LEN = {
    'RC5':    63,      # 6 x40
    'RC5X':    127,    # 7 x80
    'RC6':     256,    # 8 x100
    'NEC':     255,    # 8
    # 'NECext':  65536,  # 16 x10000
    'NEC42':   255,    # 8
    # 'NEC42ext': 65536,   # 16
    'Samsung32': 255,  # 8
    'SIRC':   255,     # 8
    'SIRC15': 255,     # 8
    'SIRC20': 255,     # 8
}

if len(sys.argv) < 4:
    print(f"""
        Requires 3 args:
        {sys.argv[0]} PROTO ADDR SUBA

        {sys.argv[0]} NEC 40 00

        Valid proto {' '.join(CMD_LEN.keys())}
    """)
    sys.exit(1)

PROTO = sys.argv[1]
ADDR = sys.argv[2]
SUBA = sys.argv[3]

if PROTO not in CMD_LEN:
    print("Invalid IR Protocal")
    print(f"Valid proto {' '.join(CMD_LEN.keys())}")
    sys.exit(1)

out_filen = f"IR-CMD-{PROTO}-{ADDR}.ir"

print(f"Creating file: {out_filen}")

with open(out_filen, "w", encoding="utf-8") as fd:
    fd.write("Filetype: IR signals file\nVersion: 1\n")
    fd.write("# generated with flipper_toolbox\n")
    for i in range(CMD_LEN[PROTO], -1, -1):
        fd.write(f"#\nname: Code_{i:02d}\ntype: parsed\n"
                 f"protocol: {PROTO}\naddress: {ADDR} {SUBA} 00 00\ncommand: {i:02X} 00 00 00\n")

sys.exit(0)
