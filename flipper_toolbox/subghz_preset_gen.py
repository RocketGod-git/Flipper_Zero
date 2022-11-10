#!/usr/bin/env python3
"""

    subghz_preset_gen.py

    Modify / Generates CC1101 "SubGhzPresetCustom" settings

    Written By: Peter Shipley github.com/evilpete

    From pkg https://github.com/evilpete/flipper_toolbox

"""

# import sys
# import os
# import pprint
import argparse

from subghz_decode_presets import CC_Config    # CC_REG

# ppylint: disable=no-member

_DEBUG = 0


# See : https://github.com/flipperdevices/flipperzero-firmware/blob/dev/firmware/targets/f7/furi_hal/furi_hal_subghz_configs.h


rf_presets = {
    # PresetOok270Async : OOK, bandwidth 270kHz, async
    "AM270": ("Custom_preset_data: 02 0D 03 47 08 32 0B 06 10 67 11 32 "
              "12 30 13 00 14 00 18 18 19 18 1B 03 1C 00 1D 40 20 FB "
              "21 B6 22 11 00 00 00 C0 00 00 00 00 00 00"),

    # PresetOok650Async : OOK, bandwidth 650kHz, async
    "AM650": ("Custom_preset_data: 02 0D 03 07 08 32 0B 06 10 17 11 32 "
              "12 30 13 00 14 00 18 18 19 18 1B 07 1C 00 1D 91 20 FB "
              "21 B6 22 11 00 00 00 C0 00 00 00 00 00 00"),

    # Preset2FSKDev238Async : FM, deviation 2.380371 kHz, async
    "FM238": ("Custom_preset_data: 02 0D 07 04 08 32 0B 06 10 67 11 83 "
              "12 04 13 02 14 00 15 04 18 18 19 16 1B 07 1C 00 1D 91 20 FB "
              "21 56 22 10 00 00 C0 00 00 00 00 00 00 00"),

    # Preset2FSKDev476Async : FM, deviation 47.60742 kHz, async
    "FM476": ("Custom_preset_data: 02 0D 07 04 08 32 0B 06 10 67 11 83 "
              "12 04 13 02 14 00 15 47 18 18 19 16 1B 07 1C 00 1D 91 20 FB "
              "21 56 22 10 00 00 C0 00 00 00 00 00 00 00"),

    # PresetMSK99_97KbAsync : MSK, deviation 47.60742 kHz, 99.97Kb/s, async
    "MSK999": ("Custom_preset_data: 02 06 03 07 04 46 05 4c 06 00 08 05 "
               "09 00 0a 00 0b 06 0c 23 10 5b 11 f8 12 72 13 22 14 f8 15 "
               "47 18 18 19 16 1a 1c 1b c7 1c 00 1d b2 21 56 22 10 29 59 "
               "00 00 c0 00 00 00 00 00 00 00"),

    # PresetGFSK9_99KbAsync : GFSK, deviation 19.042969 kHz, 9.996Kb/s, async
    "GFSK99": ("Custom_preset_data: 02 06 03 47 04 46 05 4c 06 00 08 05 "
               "09 00 0b 06 10 c8 11 93 12 12 15 34 18 18 19 16 1b 43 "
               "1c 40 1d 91 20 fb 00 00 c0 00 00 00 00 00 00 00"),
}


# Intermediate_freq:        152343.75 Hz
# Modulations:              2FSK
# Data_Rate:                4797.94 Hz
# Bit_Width:                208.42 ms
# Channel_Bandwidth:        270833.33 Hz
# Deviation:                2380.37 Hz
# Sync_Mode:                SYNCM_CARRIER
# Channel_spacing:          101562.50 Hz
# Manchester:               0
# Variable_length_packet:   Infinite packet length
# Enable_Pkt_CRC:           0
# Preamble_Quality_Threshold: 0
# Pkt_DataWhitening         0
# Min_TX_Preamble:          0
# PA_Table:                 [192, 0, 0, 0, 0, 0, 0, 0]

MOD_2FSK = 0x00
MOD_GFSK = 0x10
MOD_ASK_OOK = 0x30
MOD_4FSK = 0x40
MOD_MSK = 0x70

PKT_FMT = {
    "Normal": 0x03,
    "Sync":  0x01,
    "Random":  0x02,
    "Async":  0x03,
}

mods = {
    "2FSK": 0x00,   # MOD_2FSK,
    "GFSK": 0x10,    # MOD_GFSK,
    "OOK": 0x30,     # MOD_ASK_OOK
    "4FSK": 0x40,    # MOD_4FSK
    "MSK": 0x70,     # MOD_MSK
}

sync_modes = ['SYNCM_NONE', 'SYNCM_15_of_16', 'SYNCM_16_of_16',
              'SYNCM_30_of_32', 'SYNCM_CARRIER', 'SYNCM_CARRIER_15_of_16',
              'SYNCM_CARRIER_16_of_16', 'SYNCM_CARRIER_30_of_32']

sync_help = """
    SYNCM_NONE                      = 0
    SYNCM_15_of_16                  = 1
    SYNCM_16_of_16                  = 2
    SYNCM_30_of_32                  = 3
    SYNCM_CARRIER                   = 4
    SYNCM_CARRIER_15_of_16          = 5
    SYNCM_CARRIER_16_of_16          = 6
    SYNCM_CARRIER_30_of_32          = 7
"""


def _interpret_val(opt):
    opt = opt.upper()

    if opt in ["ON", "TRUE", "T", "YES", "Y", "1"]:
        return 1

    if opt in ["OFF", "FALSE", "F", "NO", "N", "0"]:
        return 0

    if opt.isdigit():
        return int(opt)

    return None


def arg_opts():
    """argument parse"""

    preset_namelist = sorted(rf_presets.keys())
    modulation_namelist = sorted(CC_Config.mod_num.values())
    length_namelist = sorted(CC_Config.PKT_LENGTH_CONF.keys())
    pkt_fmt_namelist = sorted(PKT_FMT.keys())
    # modulation_namelist = sorted(mods.keys())
    # length_namelist = sorted(length_conf.keys())

    parser = argparse.ArgumentParser(add_help=True, allow_abbrev=True,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
                        # argument_default=argparse.SUPPRESS,

    parser.add_argument("-p", "--preset", dest="preset_profile",
                        choices=preset_namelist,
                        default=None,
                        help="preset profile")

    parser.add_argument("-pr", "--print", dest="print_profile",
                        action='store_true',
                        default=None,
                        help="Print Profile Description")

    parser.add_argument("-sw", "--syncword", dest="sync_word",
                        type=int,
                        # choices=sync_modes,
                        default=None,
                        help="Sync Word")

    parser.add_argument("-sm", "--syncmode", dest="sync_mode",
                        type=int,
                        # choices=sync_modes,
                        default=None,
                        help=sync_help)

    parser.add_argument("-mod", "--modulation", dest="modulation",
                        choices=modulation_namelist,
                        default=None,
                        help="Modulation")

    parser.add_argument("-lc", "--length_conf", dest="length_conf",
                        choices=length_namelist,
                        default=None,
                        help="Length Config")

    parser.add_argument("-pf", "--pktfmt", dest="pkt_fmt",
                        choices=pkt_fmt_namelist,
                        default="Async",
                        help="Packet Format")

    parser.add_argument("-pl", "--pkt_len", dest="pkt_len",
                        type=int,
                        default=None,
                        help="Packet Length")

    parser.add_argument('-v', '--verbose', dest="verbose",
                        default=0,
                        help='Increase debug verbosity', action='count')

    parser.add_argument("-n", "--name", dest="conf_name",
                        default="NewPreset",
                        help="Name For Preset")

    parser.add_argument("-if", "--IntermediateFreq", dest="intermediate_freq",
                        type=int,
                        default=None,
                        help="Intermediate frequency")

    parser.add_argument("-dr", "--datarate", dest="data_rate",
                        type=int,
                        default=None,
                        help="Date Rate")

    parser.add_argument("-fr", "--frequency", dest="frequency",
                        type=int,
                        default=None,
                        help="frequency")

    parser.add_argument("-bw", "--bandwidth", dest="band_width",
                        type=int,
                        default=None,
                        help="Band Width")

    parser.add_argument("-np", "--numpreamble", dest="num_preamble",
                        type=int,
                        default=None,
                        help="Minimum number of preamble bytes to be transmitted\n"
                             "0=2bytes 1=3b 2=4b 3=6b 4=8b 5=12b 6=15b 7=24b"
                        )

    parser.add_argument("-dev", "--deviation", dest="deviation",
                        type=int,
                        default=None,
                        help="FM Deviation")

    parser.add_argument("-cs", "--channelspacing", "--spacing", dest="channel_spacing",
                        type=int,
                        default=None,
                        help="Channel Spacing")

    parser.add_argument("-man", "--manchester", dest="manchester",
                        default=False, action='store_true',
                        help="Manchester Encoding")

    # crc_grp = parser.add_mutually_exclusive_group()

    parser.add_argument("-crc", "--enable_crc", dest="enable_crc",
                        choices=['on', 'off'],
                        default=None,
                        help="Enable/Disable CRC")

    parser.add_argument("-dw", "--datawhitening", "--datawhite", dest="data_whiten",
                        choices=['on', 'off'],
                        default=None,
                        help="Enable/DisableData Whitening")


#    data_grp.add_argument("-c", "--cmd-file", dest="cmd_file",
#                          type=argparse.FileType('r', encoding='UTF-8'),
#                          default=None,
#                          help="Command File")

    return parser.parse_known_args()


def main():

    # print(rf_presets)

    reg_conf = CC_Config()
    reg_conf.reg_list[2] = 13 # Output Pin Configuration
    reg_conf.reg_list[3] = 7 # RX FIFO and TX FIFO Thresholds


    args, u = arg_opts()

    # print(f"args: {args}\n")
    # print(f"u: {u}\n")

    if args.preset_profile:
        reg_conf.load_str(rf_presets[args.preset_profile])

    if args.deviation is not None:
        reg_conf.set_Deviatn(args.deviation)

    if args.modulation is not None:
        reg_conf.set_Modulation(args.modulation)

    if args.manchester is not None:
        reg_conf.set_Manchester(args.manchester)

    if args.length_conf is not None:
        reg_conf.set_Pktlen_conf(args.length_conf)

    if args.pkt_len is not None:
        if args.pkt_len > 255:
            raise ValueError("Max Packet Length 255")
        reg_conf.set_pktlen(args.pkt_len)

    if args.intermediate_freq is not None:
        reg_conf.set_FsIF(args.intermediate_freq)

    if args.data_rate is not None:
        reg_conf.set_DRate(args.data_rate)

    if args.channel_spacing is not None:
        reg_conf.set_ChanSpc(args.channel_spacing)

    if args.enable_crc is not None:
        if args.enable_crc == 'on':
            reg_conf.set_Enable_CRC(enable=True)
        else:
            reg_conf.set_Enable_CRC(enable=False)

    if args.data_whiten is not None:
        if args.data_whiten == 'yes':
            reg_conf.set_PktDataWhitening(1)
        else:
            reg_conf.set_PktDataWhitening(1)

    if args.num_preamble is not None:
        reg_conf.set_NumPreamble(args.num_preamble)

    if args.band_width is not None:
        if args.band_width < 54170:
            raise ValueError("Bandwith must me over 54kHz")
        reg_conf.set_ChanBW(args.band_width)

    if args.frequency is not None:
        reg_conf.set_Freq(args.frequency)
        print("Warning: frequency is set in subghz flipper file")

    if args.pkt_fmt is not None:
        if args.pkt_fmt in PKT_FMT:
            reg_conf.set_pktfmt(args.pkt_fmt)

    mod = reg_conf.get_Modulation()
    manch = reg_conf.get_Manchester()

    if mod == 0x30 and args.deviation:
        print("Warning: Deviation value is ignored when modulation is 'OOK'")

    if mod is not None and manch is not None:
        if args.modulation == 0x40 and manch:
            print("Warning: radio doesn't support Manchester encoding in 4FSK")

    # print("as_preset_tuples:\n", pprint.pformat(reg_conf.as_preset_data_tuples(), compact=True))

    print("\n")
    print(f"Custom_preset_name: {args.conf_name}\n"
          "Custom_preset_module: CC1101\n"
          "Custom_preset_data:", reg_conf.as_preset_data())
    print("\n")

    if args.print_profile:
        for a, b in reg_conf.rf_conf():
            print(f"    {a:<28s} {b:<10s}")

        # print(reg_conf.as_tuples())


if __name__ == '__main__':
    main()
