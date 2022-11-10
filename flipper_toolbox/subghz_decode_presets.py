#!/usr/bin/env python3
"""

    subghz_decode_presets.py

    Decodes CC1101 settings from Flipper setting_user file or saved sameple file

    Warning:   this is total trash code, use at own risk

    Written By: Peter Shipley github.com/evilpete

    From pkg https://github.com/evilpete/flipper_toolbox

"""

import sys
import os
import pprint

# pylint: disable=no-member

_DEBUG = 0


# ./lib/drivers/cc1101_regs.h
CC1101_QUARTZ = 26000000
mhz = 26

MFMCFG1_NUM_PREAMBLE           = 0x70
MFMCFG1_NUM_PREAMBLE_4         = (0x02 << 4)
DEVIATN_DEVIATION_M            = 0x07
MDMCFG2_MOD_FORMAT             = 0x70
MDMCFG2_MANCHESTER_EN          = 0x08
MDMCFG2_SYNC_MODE              = 0x07
MDMCFG4_DRATE_E                = 0x0F
MDMCFG4_CHANBW_E               = 0xC0
MDMCFG4_CHANBW_M               = 0x30
RF_MAX_TX_BLOCK                = 255
EP5OUT_BUFFER_SIZE             = 516
BSCFG_BS_LIMIT                 = 0x03

PKTCTRL0_LENGTH_CONFIG         = 0x03

MOD_2FSK                        = 0x00
MOD_GFSK                        = 0x10
MOD_ASK_OOK                     = 0x30
MOD_4FSK                        = 0x40
MOD_MSK                         = 0x70

MANCHESTER                      = 0x08


class CC_REG():
    # pylint: disable=too-few-public-methods

    def __init__(self, **kwargs):
        # print("CC_REG __init__")
        self.reg_num = {}
        self._debug = kwargs.get('debug', _DEBUG)
        # for i in range(len(self.reg_names)):
        #    self.reg_num[self.reg_names[i]] = i
        #    self.__setattr__(self.reg_names[i], i)
        for i, n in enumerate(self.reg_names):
            self.reg_num[n] = i
            self.__setattr__(n, i)

        self.mod_names = {}
        for k, v in self.mod_num.items():
            self.mod_names[v] = k
        self.mod_names['ASK'] = self.mod_names['OOK']

    mod_num = {
        MOD_2FSK: "2FSK",
        MOD_GFSK: "GFSK",
        MOD_4FSK: "4FSK",   # note: radio doesn't support Manchester encoding in 4FSK
        MOD_ASK_OOK: "OOK",    # ASK
        MOD_MSK: "MSK",
    }
    PKT_LENGTH_CONF = {
        "Fixed": 0,
        "Variable": 1,
        "Infinite": 2,
    }
    LENGTH_CONFIGS = [
        "Fixed Packet Mode",
        "Variable Packet Mode (len=first byte after sync word)",
        "Infinite packet length", "reserved"]

    sync_modes = ['SYNCM_NONE', 'SYNCM_15_of_16', 'SYNCM_16_of_16', 'SYNCM_30_of_32',
                  'SYNCM_CARRIER', 'SYNCM_CARRIER_15_of_16', 'SYNCM_CARRIER_16_of_16',
                  'SYNCM_CARRIER_30_of_32']

    PKT_FMT = {
        "Normal": 0x00,
        "Sync":  0x01,
        "Random":  0x02,
        "Async":  0x03,
    }
    PKT_FMT_NAMES = ["Normal", "Sync", "Random", "Async"]

    reg_names = ['IOCFG2', 'IOCFG1', 'IOCFG0', 'FIFOTHR', 'SYNC1', 'SYNC0', 'PKTLEN',
                 'PKTCTRL1', 'PKTCTRL0', 'ADDR', 'CHANNR', 'FSCTRL1', 'FSCTRL0', 'FREQ2',
                 'FREQ1', 'FREQ0', 'MDMCFG4', 'MDMCFG3', 'MDMCFG2', 'MDMCFG1', 'MDMCFG0',
                 'DEVIATN', 'MCSM2', 'MCSM1', 'MCSM0', 'FOCCFG', 'BSCFG', 'AGCCTRL2', 'AGCCTRL1',
                 'AGCCTRL0', 'WOREVT1', 'WOREVT0', 'WORCTRL', 'FREND1', 'FREND0', 'FSCAL3',
                 'FSCAL2', 'FSCAL1', 'FSCAL0', 'RCCTRL1', 'RCCTRL0', 'FSTEST', 'PTEST',
                 'AGCTEST', 'TEST2', 'TEST1', 'TEST0']

    num_preamble = [2, 3, 4, 6, 8, 12, 16, 24]

    num_preamble_map = {
        2: 0,
        3: 1,
        4: 2,
        6: 3,
        8: 4,
        12: 5,
        16: 6,
        24: 7,
    }


class CC_Config(CC_REG):
    # pylint: disable=too-many-public-methods

    def __init__(self, **kwargs):

        # print("CC_Config __init__")

        self._debug = kwargs.get('debug', _DEBUG)
        self.name = kwargs.get('name', 'custom')

        super().__init__()

        # print("len self.reg_num", len(self.reg_num))
        if 'reg_list' in kwargs:
            self.reg_list = kwargs['reg_list'][:-8]
            self.pa_list = kwargs['reg_list'][-8:]
        else:
            self.reg_list = [None] * 48
            #self.pa_list = [0] * 8
            self.reg_list[2] = 13 # Output Pin Configuration
            self.reg_list[3] = 7 # RX FIFO and TX FIFO Thresholds
            self.pa_list = [0, 192, 0, 0, 0, 0, 0, 0]

        if 'reg_str' in kwargs:
            self.load_str(kwargs['reg_str'], clear_list=False)

        self.name = kwargs.get('name', "Custom_Preset")

    def load_str(self, reg_str, clear_list=True):

        # print("load_str:", reg_str)

        if reg_str.startswith('Custom_preset_data'):
            reg_str = reg_str.split(':')[1].strip()

        if clear_list:
            self.reg_list[:] = [None] * 50
            # self.pa_list[:] = [None] * 6

        # print("reg_str:", reg_str)
        reg_pairs = reg_str.split()
        rp_len = len(reg_pairs)
        # print("reg_pairs:", reg_pairs)
        # print("rp_len:", rp_len)

        for i in range(0, rp_len, 2):
            n = reg_pairs[i]
            v = reg_pairs[i + 1]
            if n == '00' and v == '00':
                break
            nv = int(n, 16)
            self.reg_list[nv] = int(v, 16)

        self.pa_list = [int(x, 16) for x in reg_pairs[-8:]]

        if self._debug:
            print(">>", self.reg_list)
            print(">>", self.pa_list)

    def get_value(self, name):

        if name not in self.reg_num:
            raise ValueError("setting {name} not recognize")

        x = self.reg_num[name]

        return self.reg_list[x]

    def set_value(self, name, value):

        if name not in self.reg_num:
            raise ValueError("setting {name} not recognize")

        if value > 255:
            raise ValueError("setting value {value} too large (>255)")

        x = self.reg_num[name]
        self.reg_list[x] = value

    def as_tuples(self):
        a = [(k, v) for k, v in zip(self.reg_names, self.reg_list) if v is not None]
        a.append(('PATABLE', self.pa_list))
        return a
        # return dict(zip(self.reg_names, self.reg_list))

    def as_dict(self):
        d = {k: v for k, v in zip(self.reg_names, self.reg_list) if v is not None}
        d['PATABLE'] = self.pa_list
        return d
        # return dict(zip(self.reg_names, self.reg_list))

    def as_preset_data(self):
        a = []
        for i, v in enumerate(self.reg_list):
            if v is not None:
                a.append(f"{i:02X} {v:02X}")
        a.append("00 00")
        a += [f"{i:02X}" for i in self.pa_list]
        return " ".join(a)

    def as_preset_data_tuples(self):
        a = []
        for i, v in enumerate(self.reg_list):
            if v is not None:
                a.append((i, v))
        a.append((None, None))
        a.append(tuple(self.pa_list))
        return a

    # pylint: disable=too-many-statements, too-many-branches
    def rf_conf(self):
        res = []

        # Frequency Configuration

        x = self.get_Channel()
        if x is not None:
            res.append(('Channel:', f'{x}'))

        x = self.get_FsIF()
        if x is not None:
            res.append(('Intermediate_freq:', f'{x} Hz'))

        x = self.get_FsOffset()
        if x is not None:
            res.append(('Frequency_Offset:', f'{x}'))

        # Modem Configuration

        x = self.get_Modulation()
        res.append(('Modulations:', f'{self.mod_num.get(x, "??")}'))
        # res['Modulations'] = self.mod_names.get(x, '??')

        if self.reg_list[self.MDMCFG4] and self.reg_list[self.MDMCFG3]:

            x = self.get_DRate()
            res.append(('Data_Rate:', f'{x:.2f} Hz'))
            y = (1.0 / x) * 1000000
            res.append(('Bit_Width:', f'{y:.2f} ms'))
            # (1 / baudrate) * 1000000 = bit width in ms

        res.append(('Channel_Bandwidth:', f'{self.get_ChanBW():.2f} Hz'))

        x = self.get_Deviatn()
        if x is not None:
            res.append(('Deviation:', f'{self.get_Deviatn():.2f} Hz'))

        x = self.get_SyncMode()
        if x is not None:
            y = self.sync_modes[x]
            res.append(('Sync_Mode:', f'{y}'))

        x = self.get_ChanSpc()
        if x is not None:
            res.append(('Channel_spacing:', f'{x:.2f} Hz'))

        if self.reg_list[self.BSCFG] is not None:
            res.append(('BSLimit:', f'{self.get_BSLimit()}'))

        res.append(('Manchester:', f'{self.get_Manchester()}'))

        #  Packet Config

        if self.reg_list[self.SYNC1]:
            res.append(('SyncWord:', f'0x{self.get_SyncWord():04x}'))

        x = self.get_pktlen()
        if x is not None:
            res.append(('Packet_Length:', f'{x}'))

        x = self.get_pktfmt()
        if x is not None:
            res.append(('Packet_Format:', f'{x}'))

        x = self.get_pktlen_conf()
        if x is not None:
            res.append(('Variable_length_packet:', f'{self.LENGTH_CONFIGS[x]}'))

        x = self.get_Enable_CRC()
        if x is not None:
            res.append(('Enable_Pkt_CRC:', f'{x}'))

        if self.reg_list[self.PKTCTRL1]:
            res.append(('Preamble_Quality_Threshold:', f'{self.get_PktPQT()}'))

        x = self.get_PktDataWhitening()
        if x is not None:
            res.append(('Pkt_DataWhitening', f'{x}'))

        x = self.get_dev_addr()
        if x is not None:
            res.append(('Device_Pkt_Addr', f'{x}'))

        # NUM_PREAMBLE = [2, 3, 4, 6, 8, 12, 16, 24]
        # x = (self.get_NumPreamble() >> 4) & 7
        # num_preamble = self.num_preamble[x]
        x = self.get_NumPreamble()
        if x is not None:
            res.append(('Min_TX_Preamble:', f'{self.get_NumPreamble()} bytes'))

        res.append(('PA_Table:', str(self.pa_list)))

        # res['Est_Freq_Offset'] = self.get_FreqEst()

        return res

    def set_maxpower(self, power=None, invert=False):
        freq = self.get_Freq()

        if freq is None:
            power = 0xC0
        elif freq <= 400000000:
            power = 0xC2
        elif freq <= 464000000:
            power = 0xC0
        elif freq <= 900000000:
            power = 0xC2
        else:
            power = 0xC0

        self.set_power(power, invert)

    def set_power(self, power=None, invert=False):
        mod = self.get_Modulation()
        if power is not None:
            if mod == MOD_ASK_OOK and not invert:
                self.pa_list[0] = 0
                self.pa_list[1] = power
            else:
                self.pa_list[0] = power
                self.pa_list[1] = 0

        frend0 = self.reg_list[self.FREND0]
        if frend0 is None:
            frend0 = 0
        frend0 &= ~0x07    # FREND0_PA_POWER

        if mod == MOD_ASK_OOK:
            frend0 |= 0x01

        self.reg_list[self.FREND0] = frend0

    def set_ChanBW(self, bw):

        chanbw_e = None
        chanbw_m = None

        bw = float(bw)
        for e in range(4):
            # m = int(((old_div(mhz*1000000.0, (bw *pow(2, e) * 8.0 ))) - 4) + .5)        # rounded evenly
            m = int(((CC1101_QUARTZ / (bw * pow(2, e) * 8.0)) - 4) + 0.5)        # rounded evenly
            # print(f"e={e} m={m}")
            if m < 4:
                chanbw_e = e
                chanbw_m = m
                break
        if chanbw_e is None:
            raise ValueError("ChanBW does not translate into acceptable parameters")

        xbw = 1000.0 * mhz / (8.0 * (4 + chanbw_m) * pow(2, chanbw_e))
        if self._debug:
            print(f"chanbw_e: {e:x}   chanbw_m: {m:x}   chanbw: {xbw:f} kHz")

        mdmcfg4 = self.reg_list[self.MDMCFG4]
        if mdmcfg4 is None:
            mdmcfg4 = 0

        mdmcfg4 &= ~(MDMCFG4_CHANBW_E | MDMCFG4_CHANBW_M)
        mdmcfg4 |= ((chanbw_e << 6) | (chanbw_m << 4))
        self.reg_list[self.MDMCFG4] = mdmcfg4

        # from http://www.cs.jhu.edu/~carlson/download/datasheets/ask_ook_settings.pdf
        if bw > 102e3:
            self.reg_list[self.FREND1] = 0xb6
        else:
            self.reg_list[self.FREND1] = 0x56

        if bw > 325e3:
            self.reg_list[self.TEST2] = 0x88
            self.reg_list[self.TEST1] = 0x31
        else:
            self.reg_list[self.TEST2] = 0x81
            self.reg_list[self.TEST1] = 0x35

    def get_ChanBW(self):

        mdmcfg4 = self.reg_list[self.MDMCFG4]
        chanbw_e = (mdmcfg4 >> 6) & 0x3
        chanbw_m = (mdmcfg4 >> 4) & 0x3
        bw = CC1101_QUARTZ / (8.0 * (4 + chanbw_m) * pow(2, chanbw_e))
        if self._debug:
            print(f"chanbw_e: {chanbw_e:x}   chanbw_m: {chanbw_m:x}   chanbw: {bw:f} hz")
        return bw

    # def get_FreqEst(self):
    #    freqest = self.reg_list[self.FREQEST]
    #    return freqest
    def set_FsIF(self, freq_if):

        ifBits = (freq_if * (pow(2, 10))) / CC1101_QUARTZ
        ifBits = int(ifBits + .5)       # rounded evenly

        if ifBits > 0x1f:
            raise ValueError(f"FAIL:  freq_if is too high?  freqbits: {ifBits:x} (must be <0x1f)")

        fsctrl1 = self.reg_list[self.FSCTRL1]
        if fsctrl1 is None:
            fsctrl1 = 0

        fsctrl1 &= ~(0x1f)
        fsctrl1 |= int(ifBits)
        self.reg_list[self.FSCTRL1] = fsctrl1

    def get_FsIF(self):
        fsctrl1 = self.reg_list[self.FSCTRL1]
        if fsctrl1 is None:
            return None

        freq_if = (fsctrl1 & 0x1f) * (CC1101_QUARTZ / pow(2, 10))
        return freq_if

    def set_FsOffset(self, if_off):
        self.reg_list[self.FSCTRL0] = if_off

    def get_FsOffset(self):
        freqoff = self.reg_list[self.FSCTRL0]
        return freqoff

    def get_Modulation(self):
        mdmcfg2 = self.reg_list[self.MDMCFG2]
        if mdmcfg2 is None:
            return None
        mod = (mdmcfg2) & MDMCFG2_MOD_FORMAT
        return mod

    def set_Modulation(self, mod, invert=False):

        if isinstance(mod, str):
            if mod not in self.mod_names:
                raise ValueError(f"Unknown Modulation: {mod}")

            mod = self.mod_names[mod]

        mdmcfg2 = self.reg_list[self.MDMCFG2]
        if mdmcfg2 is None:
            mdmcfg2 = 0
        mdmcfg2 &= ~MDMCFG2_MOD_FORMAT
        mdmcfg2 |= mod
        self.reg_list[self.MDMCFG2] = mdmcfg2

        power = self.pa_list[0] or self.pa_list[1]

        self.set_power(power, invert)

    def set_Deviatn(self, deviatn):
        for e in range(8):
            m = int(((deviatn * pow(2, 17)) / ((pow(2, e) * CC1101_QUARTZ)) - 8) + .5)
            # int((old_div(deviatn * pow(2, 17), (pow(2, e) * (mhz*1000000.0)))-8) + .5)
            # (old_div(deviatn * pow(2, 17), (pow(2, e) * (mhz*1000000.0)))-8) + .5
            # ((deviatn * pow(2, 17)) / ((pow(2, e) * (mhz*1000000.0)))-8) + .5
            if m < 8:
                dev_e = e
                dev_m = m
                break

        if dev_e is None:
            raise ValueError("Deviation does not translate into acceptable parameters.")

        dev = CC1101_QUARTZ * (8 + dev_m) * pow(2, dev_e) / pow(2, 17)

        if self._debug:
            print(f"dev_e: {e:X}   dev_m: {m:X}   deviatn: {dev:f} Hz")

        reg_id = self.reg_num['DEVIATN']
        d_reg = (dev_e << 4) | dev_m
        self.reg_list[reg_id] = d_reg

    def get_Deviatn(self):

        reg_id = self.reg_num['DEVIATN']
        dev = self.reg_list[reg_id]

        if dev is None:
            return None

        dev_e = dev >> 4
        dev_m = dev & DEVIATN_DEVIATION_M
        deviatn = CC1101_QUARTZ * (8 + dev_m) * pow(2, dev_e) / pow(2, 17)

        return deviatn


    def set_PktDataWhitening(self, enable=True):

        if self.reg_list[self.PKTCTRL0] is None:
            self.reg_list[self.PKTCTRL0] = 0

        dwEnable = (0, 1)[enable] << 6
        pktctrl0 = self.reg_list[self.PKTCTRL0]

        pktctrl0 &= ~0x40                # PKTCTRL0_WHITE_DATA
        pktctrl0 |= dwEnable
        self.reg_list[self.PKTCTRL0] = pktctrl0

    def get_PktDataWhitening(self):

        if self.reg_list[self.PKTCTRL0] is None:
            return None
        return (self.reg_list[self.PKTCTRL0] >> 6) & 0x1

    def get_PktPQT(self):
        """ preamble quality threshold """
        if self.reg_list[self.PKTCTRL1] is None:
            return None

        return (self.reg_list[self.PKTCTRL1] >> 5) & 7

    def set_dev_addr(self, addr):
        self.reg_list[self.ADDR] = (addr & 0xff)

    def get_dev_addr(self):
        if self.reg_list[self.ADDR] is None:
            return None
        return self.reg_list[self.ADDR]

    def set_pktfmt(self, pfmt=3):
        # pfmt cnan be the conf val or name string
        if isinstance(pfmt, str):
            sval = pfmt.capitalize()   # capitalize first chat
            if sval not in self.PKT_FMT:
                raise ValueError(f"Unknown Packet Format: {pfmt}")
            pfmt = self.PKT_FMT[sval]

        pfmt &= 0x03

        pktctrl0 = self.reg_list[self.PKTCTRL0] or 0
        pktctrl0 &= ~0x30
        pktctrl0 |= (pfmt << 4)
        self.reg_list[self.PKTCTRL0] = pktctrl0

    def get_pktfmt(self, pfmt=3):
        if self.reg_list[self.PKTCTRL0] is None:
            return None

        pktctrl0 = self.reg_list[self.PKTCTRL0] 
        pfmt = (pktctrl0 >> 4) & 0x03

        return self.PKT_FMT_NAMES[pfmt]

    def set_pktlen(self, plen):
        self.reg_list[self.PKTLEN] = (plen & 0xff)

    def get_pktlen(self):
        if self.reg_list[self.PKTLEN] is None:
            return None
        return self.reg_list[self.PKTLEN]

    def get_pktlen_conf(self):
        if self.reg_list[self.PKTCTRL0] is None:
            return None
        return self.reg_list[self.PKTCTRL0] & PKTCTRL0_LENGTH_CONFIG

    def get_Enable_CRC(self):
        if self.reg_list[self.PKTCTRL0] is None:
            return None
        return (self.reg_list[self.PKTCTRL0] >> 2) & 0x1

    def set_Enable_CRC(self, enable=True):
        if self.reg_list[self.PKTCTRL0] is None:
            self.reg_list[self.PKTCTRL0] = 0

        pktctrl0 = self.reg_list[self.PKTCTRL0]

        crcE = (0, 1)[enable] << 2
        crcM = ~(1 << 2)
        pktctrl0 &= crcM
        pktctrl0 |= crcE
        self.reg_list[self.PKTCTRL0] = pktctrl0

    PKT_LENGTH_CONF = {
        "Fixed": 0,
        "Variable": 1,
        "Infinite": 2,
    }

    def set_Pktlen_conf(self, pconf=2, maxlen=RF_MAX_TX_BLOCK):

        # pconf cnan be the conf val or name string
        if isinstance(pconf, str):
            sval = pconf.capitalize()   # capitalize first chat
            if sval not in self.PKT_LENGTH_CONF:
                raise ValueError(f"Unknown Length Conf: {pconf}")
            pconf = self.PKT_LENGTH_CONF[sval]

        pconf &= 0x03

        pktctrl0 = self.reg_list[self.PKTCTRL0] or 0
        pktctrl0 &= ~PKTCTRL0_LENGTH_CONFIG
        pktctrl0 |= pconf
        # pktlen = maxlen
        self.reg_list[self.PKTCTRL0] = pktctrl0
        if pconf == 0:   # Fixed
            self.reg_list[self.PKTLEN] = maxlen

    def set_PktVLEN(self, maxlen=RF_MAX_TX_BLOCK):
        if maxlen > RF_MAX_TX_BLOCK:
            raise ValueError(f"Packet too large (maxlen)."
                             f"Maximum variable length packet is {RF_MAX_TX_BLOCK} bytes")

        pktctrl0 = self.reg_list[self.PKTCTRL0]
        pktctrl0 &= ~PKTCTRL0_LENGTH_CONFIG
        pktctrl0 |= 1
        # pktlen = maxlen
        self.reg_list[self.PKTCTRL0] = pktctrl0
        self.reg_list[self.PKTLEN] = maxlen

    def set_PktFLEN(self, flen=RF_MAX_TX_BLOCK):

        if flen > EP5OUT_BUFFER_SIZE - 4:
            raise ValueError(f"Packet too large ({flen})"
                             f"Maximum fixed length packet is {EP5OUT_BUFFER_SIZE - 6} bytes")

        pktctrl0 = self.reg_list[self.PKTCTRL0]
        if pktctrl0 is None:
            pktctrl0 = 0
        pktctrl0 &= ~PKTCTRL0_LENGTH_CONFIG

        if flen > RF_MAX_TX_BLOCK:
            pktlen = 0x00
        else:
            pktlen = flen

        self.reg_list[self.PKTCTRL0] = pktctrl0
        self.reg_list[self.PKTLEN] = pktlen

    def set_Manchester(self, enable=True):

        mdmcfg2 = self.reg_list[self.MDMCFG2]
        mdmcfg2 &= ~MDMCFG2_MANCHESTER_EN
        mdmcfg2 |= (enable << 3)

        self.reg_list[self.MDMCFG2] = mdmcfg2

    def get_Manchester(self):

        mdmcfg2 = self.reg_list[self.MDMCFG2]
        mchstr = (mdmcfg2 >> 3) & 0x01
        return mchstr

    def set_DRate(self, drate):

        drate_e = None

        for e in range(16):
            m = int(((drate * pow(2, 28) / (pow(2, e) * CC1101_QUARTZ)) - 256) + 0.5)        # rounded evenly
            if m < 256:
                drate_e = e
                drate_m = m
                break

        if drate_e is None:
            raise ValueError("DRate does not translate into acceptable parameters.")

        drate = CC1101_QUARTZ * (256 + drate_m) * pow(2, drate_e) / pow(2, 28)

        if self._debug:
            print(f"drate_e: {drate_e:x}  drate_m: {drate_m:x}   drate: {drate:f} Hz")

        self.reg_list[self.MDMCFG3] = drate_m

        if self.reg_list[self.MDMCFG4] is None:
            mdmcfg4 = 0
        else:
            mdmcfg4 = self.reg_list[self.MDMCFG4]

        mdmcfg4 &= ~MDMCFG4_DRATE_E
        mdmcfg4 |= drate_e

        self.reg_list[self.MDMCFG4] = mdmcfg4

    def get_DRate(self):

        drate_e = self.reg_list[self.MDMCFG4] & 0xf
        drate_m = self.reg_list[self.MDMCFG3]

        drate = CC1101_QUARTZ * (256 + drate_m) * pow(2, drate_e) / pow(2, 28)

        return drate

    def get_SyncWord(self):

        if self.reg_list[self.SYNC1] is None:
            return None

        return (self.reg_list[self.SYNC1] << 8) + self.reg_list[self.SYNC0]

    def set_SyncWord(self, word):

        self.reg_list[self.SYNC1] = word >> 8
        self.reg_list[self.SYNC0] = word & 0xff

    def get_SyncMode(self):
        return self.reg_list[self.MDMCFG2] & MDMCFG2_SYNC_MODE

    # SYNCM_NONE                      = 0
    # SYNCM_15_of_16                  = 1
    # SYNCM_16_of_16                  = 2
    # SYNCM_30_of_32                  = 3
    # SYNCM_CARRIER                   = 4
    # SYNCM_CARRIER_15_of_16          = 5
    # SYNCM_CARRIER_16_of_16          = 6
    # SYNCM_CARRIER_30_of_32          = 7

    def set_SyncMode(self, syncmode=5):

        mdmcfg2 = self.reg_list[self.MDMCFG2]
        mdmcfg2 &= ~MDMCFG2_SYNC_MODE
        mdmcfg2 |= syncmode

        self.reg_list[self.MDMCFG2] = mdmcfg2

    # [2, 3, 4, 6, 8, 12, 16, 24]
    # MFMCFG1_NUM_PREAMBLE0          = 0x10
    # MFMCFG1_NUM_PREAMBLE1          = 0x20
    # MFMCFG1_NUM_PREAMBLE2          = 0x40

    # MFMCFG1_NUM_PREAMBLE_2         = (0x00 << 4)
    # MFMCFG1_NUM_PREAMBLE_3         = (0x01 << 4)
    # MFMCFG1_NUM_PREAMBLE_4         = (0x02 << 4)
    # MFMCFG1_NUM_PREAMBLE_6         = (0x03 << 4)
    # MFMCFG1_NUM_PREAMBLE_8         = (0x04 << 4)
    # MFMCFG1_NUM_PREAMBLE_12        = (0x05 << 4)
    # MFMCFG1_NUM_PREAMBLE_16        = (0x06 << 4)
    # MFMCFG1_NUM_PREAMBLE_24        = (0x07 << 4)

    def get_NumPreamble(self):

        if self.reg_list[self.MDMCFG1] is None:
            return None

        preamble = (self.reg_list[self.MDMCFG1]  & MFMCFG1_NUM_PREAMBLE) >> 4
        return self.num_preamble[preamble]

    def set_NumPreamble(self, preamble=MFMCFG1_NUM_PREAMBLE_4):
        if self._debug:
            print("set_NumPreamble {preamble}")

        if preamble not in self.num_preamble_map:
            #  pylint: disable=consider-using-f-string
            raise ValueError("NumPreamble must have value of {}".format(
                ' '.join(map(str, self.num_preamble))))

        preamble = self.num_preamble_map[preamble]

        mdmcfg1 = self.reg_list[self.MDMCFG1]
        mdmcfg1 &= ~MFMCFG1_NUM_PREAMBLE
        mdmcfg1 |= (preamble << 4)

        self.reg_list[self.MDMCFG1] = mdmcfg1

    # BSCFG_BS_LIMIT_0               = (0x00)    # "No data rate offset compensation performed",
    # BSCFG_BS_LIMIT_3               = (0x01)    # "+/- 3.125% data rate offset"
    # BSCFG_BS_LIMIT_6               = (0x02)    # "+/- 6.25% data rate offset",
    # BSCFG_BS_LIMIT_12              = (0x03)    # "+/- 12.5% data rate offset",

    def get_BSLimit(self):
        if self.reg_list[self.BSCFG] is None:
            return None
        return self.reg_list[self.BSCFG] & BSCFG_BS_LIMIT

    def set_BSLimit(self, bslimit):

        bscfg = self.reg_list[self.BSCFG]
        if bscfg is None:
            bscfg = 0

        bscfg &= ~BSCFG_BS_LIMIT
        bscfg |= bslimit
        self.reg_list[self.BSCFG] = bscfg

    def set_Channel(self, channr):
        self.reg_list[self.CHANNR] = channr & 0xff

    def get_Channel(self):
        channr = self.reg_list[self.CHANNR]
        return channr

    def get_ChanSpc(self):

        if self.reg_list[self.MDMCFG0] is None or self.reg_list[self.MDMCFG1] is None:
            return None

        chanspc_m = self.reg_list[self.MDMCFG0]
        chanspc_e = self.reg_list[self.MDMCFG1] & 3
        chanspc = CC1101_QUARTZ / pow(2, 18) * (256 + chanspc_m) * pow(2, chanspc_e)
        if self._debug:
            print(f"chanspc_e: {chanspc_e:x}   chanspc_m: {chanspc_m:x}   chanspc: {chanspc:f} hz")
        return chanspc

    def get_Freq(self):
        freqmult = 0x10000 / CC1101_QUARTZ

        freq2 = self.reg_list[self.FREQ2]
        freq1 = self.reg_list[self.FREQ1]
        freq0 = self.reg_list[self.FREQ0]

        if freq0 is None or freq1 is None or freq2 is None:
            return None

        num = (freq2 << 16) + (freq1 << 8) + freq0
        freq = num // freqmult
        return freq    #  hex(num)

    # not needed for Flipper but included anyway
    def set_Freq(self, freq=433920000):
        # freqmult = (0x10000 / 1000000.0) / mhz
        freqmult = 0x10000 / CC1101_QUARTZ
        num = int(freq * freqmult)
        freq2 = num >> 16
        freq1 = (num >> 8) & 0xff
        freq0 = num & 0xff

        if self._debug:
            print(f"set_Freq: freq={freq} : num={num} : freq0={freq0} freq1={freq1} freq2={freq2}")

        self.reg_list[self.FREQ2] = freq2
        self.reg_list[self.FREQ1] = freq1
        self.reg_list[self.FREQ0] = freq0

    def set_ChanSpc(self, chanspc):

        chanspc_e = None
        chanspc_m = None
        for e in range(4):
            m = int(((chanspc * pow(2, 18) / (CC1101_QUARTZ * pow(2, e))) - 256) + 0.5)    # rounded evenly
            if m < 256:
                chanspc_e = e
                chanspc_m = m
                break
        if chanspc_e is None or chanspc_m is None:
            raise ValueError("ChanSpc does not translate into acceptable parameters.")

        # chanspc = CC1101_QUARTZ/pow(2, 18) * (256 + chanspc_m) * pow(2, chanspc_e)
        # print "chanspc_e: %x   chanspc_m: %x   chanspc: %f hz" % (chanspc_e, chanspc_m, chanspc)

        # mdmcfg0 = self.reg_list[self.MDMCFG0]
        mdmcfg1 = self.reg_list[self.MDMCFG1] or 0
        # if mdmcfg1 is None:
        #     mdmcfg1 = 0

        mdmcfg0 = chanspc_m
        mdmcfg1 &= ~0x03  # MDMCFG1_CHANSPC_E            # clear out old exponent value
        mdmcfg1 |= chanspc_e
        self.reg_list[self.MDMCFG0] = mdmcfg0
        self.reg_list[self.MDMCFG1] = mdmcfg1

    def __repr__(self):
        return str({k: v for k, v in zip(self.reg_names, self.reg_list) if v is not None})


def _main():

    if len(sys.argv) < 2:
        if os.path.isfile("setting_user"):
            filen = 'setting_user'
        else:
            print("requires setting_user file or saved sameple file as first arg")
            return
    else:
        filen = sys.argv[1]

    presets = {}

    SubGhz_Headers = [
        "Filetype: Flipper SubGhz Setting File",
        "Filetype: Flipper SubGhz RAW File"]

    with open(filen, 'r', encoding="utf-8") as fd:
        header = fd.readline().strip()
        if header not in SubGhz_Headers:
            print(f"Error: {filen} is not a 'Flipper SubGhz' file'")
            sys.exit(1)
        preset_name = None
        preset_data = None
        for line in fd:
            if line.startswith('Custom_preset_name') or line.startswith('Preset:'):
                preset_name = line.split(':')[1].strip()

            if line.startswith('Custom_preset_data'):
                preset_data = line.split(':')[1].strip()

            if preset_name and preset_data:
                presets[preset_name] = CC_Config(name=preset_name, reg_str=preset_data)
                preset_name = None
                preset_data = None

    for k, v in presets.items():
        print(f"\n\n{k}")
        print("\nas_tuples: ")
        pprint.pprint(v.as_tuples(), indent=4, compact=True)
        # print("\nas_dict: ")
        # pprint.pprint(v.as_dict(), indent=4, compact=True)
        # print("\nas_preset_data:")
        # pprint.pprint(v.as_preset_data(), compact=True)
        print("\nrf_conf")
        for a, b in v.rf_conf():
            print(f"    {a:<25s} {b:<10s}")

    # print(dir(presets['AM_1']))


if __name__ == '__main__':
    _main()
