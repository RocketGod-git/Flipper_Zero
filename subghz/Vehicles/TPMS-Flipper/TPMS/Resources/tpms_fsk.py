#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tpms Fsk
# GNU Radio version: 3.10.4.0

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class tpms_fsk(gr.top_block):

    def __init__(self, baud=20000, deviation=25000, frequency_shift=0, interpolate=1, read_file='/Users/jcsanch8/txtpms/Citroen_i8add48d4_p289_t23_s210_f0x0_r1_b14_tpms_manch.u8', write_file='/Users/jcsanch8/txtpms/Citroen_icafebabe_p40.0_t25_s128_f0x0_r1_b14_tpms_manch.cu8'):
        gr.top_block.__init__(self, "Tpms Fsk", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.baud = baud
        self.deviation = deviation
        self.frequency_shift = frequency_shift
        self.interpolate = interpolate
        self.read_file = read_file
        self.write_file = write_file

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.5e5
        self.sensivity = sensivity = deviation/(samp_rate*0.16)
        self.samp_per_symbol = samp_per_symbol = samp_rate/baud

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interpolate,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, [1], frequency_shift, samp_rate)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_streams_to_stream_0 = blocks.streams_to_stream(gr.sizeof_char*1, 2)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, int(samp_per_symbol))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_ff(127)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(127)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((1.0/127))
        self.blocks_float_to_uchar_0_0 = blocks.float_to_uchar()
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, read_file, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, write_file, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_const_vxx_1_0 = blocks.add_const_ff(1)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-1))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(sensivity)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_add_const_vxx_1_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_streams_to_stream_0, 0))
        self.connect((self.blocks_float_to_uchar_0_0, 0), (self.blocks_streams_to_stream_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_float_to_uchar_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_streams_to_stream_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_float_0, 0))


    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samp_per_symbol(self.samp_rate/self.baud)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_sensivity(self.deviation/(self.samp_rate*0.16))

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.frequency_shift)

    def get_interpolate(self):
        return self.interpolate

    def set_interpolate(self, interpolate):
        self.interpolate = interpolate

    def get_read_file(self):
        return self.read_file

    def set_read_file(self, read_file):
        self.read_file = read_file

    def get_write_file(self):
        return self.write_file

    def set_write_file(self, write_file):
        self.write_file = write_file

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_symbol(self.samp_rate/self.baud)
        self.set_sensivity(self.deviation/(self.samp_rate*0.16))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_sensivity(self):
        return self.sensivity

    def set_sensivity(self, sensivity):
        self.sensivity = sensivity
        self.analog_frequency_modulator_fc_0.set_sensitivity(self.sensivity)

    def get_samp_per_symbol(self):
        return self.samp_per_symbol

    def set_samp_per_symbol(self, samp_per_symbol):
        self.samp_per_symbol = samp_per_symbol
        self.blocks_repeat_0.set_interpolation(int(self.samp_per_symbol))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-b", "--baud", dest="baud", type=intx, default=20000,
        help="Set Baud [default=%(default)r]")
    parser.add_argument(
        "-d", "--deviation", dest="deviation", type=intx, default=25000,
        help="Set Deviation [default=%(default)r]")
    parser.add_argument(
        "-s", "--frequency-shift", dest="frequency_shift", type=intx, default=0,
        help="Set Frequency Shift [default=%(default)r]")
    parser.add_argument(
        "-i", "--interpolate", dest="interpolate", type=intx, default=1,
        help="Set Interpolate [default=%(default)r]")
    parser.add_argument(
        "-r", "--read-file", dest="read_file", type=str, default='',
        help="Set Symbol file [default=%(default)r]")
    parser.add_argument(
        "-w", "--write-file", dest="write_file", type=str, default='',
        help="Set cu8 file [default=%(default)r]")
    return parser


def main(top_block_cls=tpms_fsk, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(baud=options.baud, deviation=options.deviation, frequency_shift=options.frequency_shift, interpolate=options.interpolate, read_file=options.read_file, write_file=options.write_file)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
