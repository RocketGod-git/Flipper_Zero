#!/usr/bin/env python3
"""

    ir_plot.py

    plot data from flipper IR raw data save files

    Warning:   this is 5 min hack code, use at own risk

    Written By: Peter Shipley github.com/evilpete

    From pkg https://github.com/evilpete/flipper_toolbox

"""

#
#   name: Left_Button
#   type raw
#   frequency: 38000
#   duty_cycle: 0.330000
#   data: 176 1028 174 293 173 241 178 263 177
#

import sys
import os
# from statistics import mean
import argparse
from pprint import pprint
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt

PRINT_BITS = True       # this is a hack


def arg_opts():

    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', dest="verbose",
                        default=0,
                        help='Increase debug verbosity', action='count')

    parser.add_argument("-n", "--name", dest="cmd_name",
                        default=None,
                        help="IR Command Name")

    parser.add_argument("-f", "--file", dest="filename",
                        default=None,
                        help="IR Filename")

    parser.add_argument("-i", "--invert", dest="invert",
                        default=False,
                        action='store_true',
                        help="Invert Wave plot")

    parser.add_argument("-d", "--dir", dest="destdir",
                        default=None,
                        help="Destination")

    parser.add_argument("-o", "--output", dest="out_format",
                        choices=['png', 'pdf', 'svg'],
                        default="None",
                        help="Output Format")

    parser.add_argument("-s", "--screen", dest="screen",
                        default=False, action='store_true',
                        help="Display on Screen")

    # data_grp = parser.add_mutually_exclusive_group()

    return parser.parse_known_args()


def load_cmd_data(filename):
    name = data_str = sig_type = duty_cycle = freq = None

    ret = []
    with open(filename, 'r', encoding="utf-8") as fd:

        header = fd.readline().strip()
        if header != 'Filetype: IR signals file':
            print(f"Error: {filename} is not a 'Flipper IR signals file'")
            sys.exit(1)

        for line in fd:

            line = line.strip()

            if not line or line[0] == '#':        # skip blank lines
                continue

            try:
                if line.startswith('name:'):
                    name = line.split(':')[1].strip()
                    sig_type = freq = duty_cycle = data_str = None

                if line.startswith('type:'):
                    sig_type = line.split(':')[1].strip()

                if line.startswith('frequency:'):
                    freq = line.split(':')[1].strip()

                if line.startswith('duty_cycle:'):
                    duty_cycle = line.split(':')[1].strip()

                if line.startswith('data:'):
                    data_str = line.split(':')[1].strip()

            except IndexError:
                print("Line format error: {line)")

            if name and sig_type and freq and duty_cycle and data_str:
                if sig_type == 'raw':
                    dat = {
                        'name': name,
                        'type': sig_type,
                        'freq': freq,
                        'duty_cycle': duty_cycle,
                        'data_str': data_str,
                    }
                    ret.append(dat)

                name = sig_type = freq = duty_cycle = data_str = None

    return ret


def split_data_str(dat, max_val=15000):

    dat_list = dat.split()
    ret = []
    cur_dat = []

    # print(f"dat_list: {len(dat_list)}")

    for x in dat_list:
        i = int(x)
        if i > max_val:
            ret.append(cur_dat)
            # print(f"cur_dat: {len(cur_dat)}")
            cur_dat = []
        else:
            cur_dat.append(i)

    ret.append(cur_dat)

    return ret


LOW_PLOT_VAL = 1
HIGH_PLOT_VAL = 5


def convert_dat(dat_list, invert=False, verbose=0):  # normalize=0,

    high_val = HIGH_PLOT_VAL
    low_val = LOW_PLOT_VAL
    # print("== convert_dat")

    if len(dat_list) % 2 != 0:
        dat_list.append(0)

    dat_len = len(dat_list)

    if verbose > 1:
        print(f"dat_len {dat_len}")

    if invert:
        high_val = LOW_PLOT_VAL
        low_val = HIGH_PLOT_VAL

#    i_min = 15
#    # o_min = 23
#    if normalize:
#        e = dat_list[2::2]
#        i_min = min(e) // 10
#        if verbose > 2:
#            o = dat_list[3::2]
#            print(min(dat_list), mean(dat_list),
#                  max(dat_list), "\n", dat_list, "\n")
#            print(min(e), mean(e), max(e), "\n", e, "\n")
#            print(min(o), mean(o), max(o), "\n", o, "\n")
#            print("\n\n")

    res = [low_val]
    for x in range(0, dat_len, 2):

        i = dat_list[x]   # // 10
        # if normalize:
        #     i = (i // i_min) * i_min

        j = int(dat_list[x + 1])   #  // 10
        # if normalize:
        #     j = (j // 23) * 26

        # print(f"{x}: {i} {j} {len(res)}")
        # res += [LOW_PLOT_VAL] * i
        # res += [HIGH_PLOT_VAL] * j

        res += [high_val] * i
        res += [low_val] * j
        res.append(1)

    # print("\n")
    return res


# An Experiment
def decode_dat(dat_list, verbose=0):

    dat_len = len(dat_list)
    if verbose > 1:
        print("== decode_dat")
    resA = []
    resB = []
    i = j = 0
    for x in range(0, dat_len, 2):

        i = dat_list[x]  # // 10

        j = int(dat_list[x + 1])  #  // 10

        A = '1' if i > j else '0'
        resA.append(A)
        B = '1' if j > 500 else '0'
        resB.append(B)

        # if verbose > 1:#test
        #     print(f"{x:3d}: {i:4d} {j:4d} : {A}   {B}")

    if verbose > 1:  # test
        print(f"A: {resA}")
        print(f"B: {resB}")

# def printbits
#        # this method is total hack and only works on a
#        if debug or PRINT_BITS:
#            # Print Bits
#            o = d[1::2]
#            avg_val = mean(o)
#            bits = ['0' if b < avg_val else '1' for b in o]
#            # print(o)
#            bit_str = "".join(bits)
#            print(bits, bit_str, "{0:02x} {0:d}".format(int(bit_str, 2)))


def main():

    filen = 'Test.ir'  # None
    cmd_name = destdir = None
    verbose = 0

    arg, av = arg_opts()
    # print("arg", arg, "av=", av)

    disp = False

    if arg.verbose:
        verbose = arg.verbose

    # get input filename from argparse or fist arg
    if arg.filename:
        filen = arg.filename
    elif av:
        filen = av.pop(0)

    if filen is None:
        print('Usage:\n\tir_plot.py <flipper_ir_file.ir> <ir_command_name>')
        sys.exit(0)

    if not os.path.exists(filen):
        print(f"file {filen} not found")
        sys.exit(0)

    if arg.cmd_name:
        cmd_name = arg.cmd_name
    elif av:
        cmd_name = av.pop(0)

    if arg.destdir:
        destdir = arg.destdir
        if not os.path.exists(destdir):
            os.mkdir(destdir)

#    if arg.out_format in ['png', 'pdf', 'svg']:
#        if not os.path.exists(destdir):
#            os.mkdir(destdir)

    if arg.screen or arg.out_format not in ['png', 'pdf', 'svg']:
        disp = True

    # print("arg", arg, "disp=", disp)

    cmd_data = load_cmd_data(filen)

    # pprint(cmd_data, compact=True)
    # print(f"cmd_data len {len(cmd_data)}")

    if cmd_name:
        cmd_data = [x for x in cmd_data if cmd_name == x['name']]

    if not cmd_data:
        print(f'Was not able to find raw data for "{cmd_name}" in {filen}')
        sys.exit()

    if verbose:
        print(f"{len(cmd_data)} found in {filen}")

    if destdir is None and arg.out_format in ['png', 'pdf', 'svg']:
        if len(cmd_data) == 1:
            destdir = '.'
        else:   # cmd_data is > 1
            destdir = os.path.splitext(filen)[0]

    # if verbose:
    #     print(f"destdir = {destdir}")

    # if not os.path.exists(destdir):
    #     os.mkdir(destdir)

    for dat in cmd_data:
        dat['data'] = split_data_str(dat['data_str'])

    ii = 0
    for dat in cmd_data:

        dat_lists = dat['data']
        name = dat['name']

        plt.figure(ii)
        ax = plt.gca()
        ax.axes.yaxis.set_visible(False)
        plt.title(f"IR Signal: {dat['name']}")

        # if verbose > 1:#test
        #     print(f'\n{ii} {name} == {len(dat_lists)}')

        if verbose > 2:
            pprint(dat_lists, indent=4, compact=True)

        list_lenghts = []
        conv_dat_lists = []
        y_off = 0
        for d in dat_lists:

            if verbose > 1:
                print('o:', d[1::2])
                print('e:', d[0::2])

                print(f"d: {d}")

            # normalize=True,
            n_dat = convert_dat(d, invert=arg.invert, verbose=arg.verbose)

            conv_dat_lists.append(n_dat)
            list_lenghts.append(len(n_dat))

            if verbose > 1:
                print(f"d: {d}")

            # decode_dat(d)

            # print(list_lenghts)

        max_len = max(list_lenghts)
        # print(max_len)
        plot_x = np.arange(max_len)

        for d in conv_dat_lists:
            d_len = len(d)
            if d_len < max_len:
                l = max_len - d_len
                d += [1] * l

            plot_y = np.array(d) + (y_off * (HIGH_PLOT_VAL + 1))

            plt.plot(plot_x, plot_y)

            # y_off += HIGH_PLOT_VAL + 1
            y_off += 1

        plt.gcf().set_size_inches(6, 1 + (.5 * y_off))

        if arg.out_format == 'png':
            if arg.verbose:
                print(f'{destdir}/{ii}_{cmd_name}.png  y_off={y_off}')
            plt.savefig(f'{destdir}/{ii}_{cmd_name}.png', pad_inches=0.3)

        ii += 1

    if disp:
        plt.show()


if __name__ == '__main__':
    main()
