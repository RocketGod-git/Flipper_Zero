#!/usr/bin/env python3

#
# Peter Shipley github.com/evilpete
#
# From pkg https://github.com/evilpete/flipper_toolbox
#
#     convert .ook files produced by rtl_433 to the Flipper .sub format

#
# Usage:
#        subghz_ook_to_sub.py FILENAME [freq]")
#
#  default freq 433920000 [433.92Mhz]
#
#


#  to convert unsigned 8-bit sdr data do the following:
#
#   convert rtl-sdr raw data file into .ook file with rtl_sdr
#   (this will partially demodulate the data)
#
#      rtl_443 -r rtl_sample.cu8 -w rf_sample.ook
#
#   convert the .ook file into a Flipper .sub file
#
#      subghz_ook_to_sub.py rf_sample.ook
#
#   this will generate the file rf_sample.sub
#
#   Note: you may have to manually set the frequancy on the
#         command line or by editing the file

#
#  With multiple packets per ook file:
#  currently only reads first header and assumes all
#  following packets use same modulation


# To do:
#   parse header
#   split samples into multiple files (opton)
#   data validation
#   .fsk file format ?
#   insert breaks between pkts


import sys
import os
# import pprint

filen = None
rf_freq = 0
rf_freq_default = 433920000

_debug = 0

# ;pulse data
# ;version 1
# ;timescale 1us
# ;created 2022-11-14 13:59:15-0800
# ;ook 21 pulses
# ;freq1 -75324
# ;centerfreq 0 Hz
# ;samplerate 250000 Hz
# ;sampledepth 8 bits
# ;range 42.1 dB
# ;rssi -0.1 dB
# ;snr 8.0 dB
# ;noise -8.1 dB
# 532 1492


def chunks(lst, n=500):
    """Yield successive 500-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def gen_sub(freq, rf_samples):

    if _debug:
        print("\n\n\nrf_samples", rf_samples)

    dat = rf_samples[0].get('header')

    if _debug:
        print(f"header {dat}")

    comment_text = "generated with ook_to_sub.py"
    rf_Preset = None
    # Preset: FuriHalSubGhzPreset2FSKDev238Async
    # Preset: FuriHalSubGhzPreset2FSKDev476Async
    # Preset: FuriHalSubGhzPresetOok270Async
    # Preset: FuriHalSubGhzPresetOok650Async
    if 'ook' in dat:
        rf_Preset = "FuriHalSubGhzPresetOok650Async"
    elif 'fsk' in dat:
        # calc freq shift deviation
        # f1 = get('freq1', 0)
        # f2 = get('freq2', 0)
        # fq = abs((f1 - f2) / 2)
        # print(f"FSK shift = {fq}")

        rf_Preset = "FuriHalSubGhzPreset2FSKDev476Async"
    else:
        print("Can't determine modulation type from header")
        print(dat)
        sys.exit(1)

    try:
        if rf_freq:
            freq = rf_freq
        else:
            fhz = dat.get('centerfreq', '0 Hz').split()[0]
            fhz = int(fhz)
            if fhz:
                freq = fhz
            else:
                freq = rf_freq_default
                print(f"Using default frequency {rf_freq_default}")
    except ValueError:
        freq = rf_freq_default

    res = f"""Filetype: Flipper SubGhz RAW File
Version: 1
# {comment_text}
Frequency: {freq}
Preset: {rf_Preset}
Protocol: RAW
"""

    data = []
    raw_data = []
    for ds in rf_samples:
        data = []
        dat = ds.get('data', [])

        for d in dat:
            a = list(map(int, d.split()))
            a[1] *= -1
            if a[0] == 0:
                del a[0]
            elif a[1] == 0:
                del a[1]
            data += a

        data = list(map(str, data))

        for i in chunks(data):
            raw_data.append(f'RAW_Data: {" ".join(i)}')

    res += '\n'.join(raw_data)

    return res


def main():

    # file_header = {}

    ook_Headers = [";pulse data"]
    # samp_mod = ""
    # samp_freq1 = 0
    # samp_freq2 = 0

    pulse_samples = []
    dat_sample = None

    if _debug:
        print(f"open {filen}")

    with open(filen, 'r', encoding="utf-8") as fd:

        header = fd.readline().strip()
        if header not in ook_Headers:
            print(f"Error: {filen} is not a 'rtl_443 ook' data file")
            sys.exit(1)

        for line in fd:

            if line.startswith(';end'):
                if _debug:
                    print("\n\ndat_sample", dat_sample)
                    print("pulse_samples", pulse_samples)

                dat_sample = None

                if _debug:
                    print("\nPULSE_SAMPLES", pulse_samples)
                continue

            if dat_sample is None:
                dat_sample = {}
                dat_sample['header'] = file_header = {}
                dat_sample['data'] = pulse_data = []
                pulse_samples.append(dat_sample)

            if line[0] == ';':
                a = line[1:].strip().split(None, 1)
                file_header[a[0]] = a[1]
                continue

            pulse_data.append(line.strip())

    print("Total packets in file",  len(pulse_samples))

    sub_data = gen_sub(rf_freq, pulse_samples)

    if _debug:
        print("\n\n{sub_data}\n\n")

    outfilen = os.path.splitext(filen)[0] + ".sub"
    with open(outfilen, 'w', encoding="utf-8") as fd:
        print(sub_data, file=fd)


if __name__ == '__main__':
    args = sys.argv[1:]

    if args:
        filen = args.pop(0)
    else:
        print("needs filename arg")
        print(f"{sys.argv[0]} FILENAME [freq]")
        sys.exit(0)

    if args:
        rf_freq = int(args.pop(0))

    main()
