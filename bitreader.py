#!/usr/bin/python

import sys
import copy
from globalconstant import Constant as Constant


class BitReader:

    def __init__(self, data):
        self.data = data
        self.cur_byte = 0
        self.num_remaining_bits_in_cur_byte = 0
        # self.bytes_left = len(data)
        self.prev_two_bytes = 0xffff
        self.emulation_prevention_bytes = 0
        self.buf = data
        self.buf_len = len(data)
        self.used_bits = 0
        self.need_prevention_detection = 0

    def update_curbyte(self):
        if len(self.data) < 1:
            return Constant.PVA_ERR_READ_BIT
        if self.need_prevention_detection and self.data[0] == 0x03 \
                and (self.prev_two_bytes & 0xffff) == 0:
            del self.data[0]
            self.emulation_prevention_bytes += 1
            self.prev_two_bytes = 0xffff
            if len(self.data) < 1:
                return Constant.PVA_ERR_READ_BIT
        self.cur_byte = self.data[0] & 0xff
        del self.data[0]
        self.num_remaining_bits_in_cur_byte = 8
        self.prev_two_bytes = (self.prev_two_bytes << 8) | self.cur_byte
        return Constant.PVA_OK

    def read_bits(self, num_bits, out):
        bits_left = num_bits
        out[0] = 0
        if num_bits > 31:
            return Constant.PVA_ERR_READ_BIT
        while self.num_remaining_bits_in_cur_byte < bits_left:
            out[0] |= (
                self.cur_byte << (bits_left - self.num_remaining_bits_in_cur_byte))
            bits_left -= self.num_remaining_bits_in_cur_byte
            if self.update_curbyte():
                return Constant.PVA_ERR_READ_BIT
        out[0] |= (
            self.cur_byte >> (self.num_remaining_bits_in_cur_byte - bits_left))
        out[0] &= ((1 << num_bits) - 1)
        self.num_remaining_bits_in_cur_byte -= bits_left
        self.used_bits += num_bits
        return Constant.PVA_OK

    def read_longbits(self, num_bits, out):
        val = [0]
        val1 = [0]
        if self.read_bits(16, val):
            return Constant.PVA_ERR_READ_BIT
        if self.read_bits(num_bits - 16, val1):
            return Constant.PVA_ERR_READ_BIT
        val[0] = val[0] << 16
        out[0] = (val[0] | val1[0])
        return PVA_OK

    def skip_bits(self, num_bits):
        bits_left = num_bits
        while self.num_remaining_bits_in_cur_byte < bits_left:
            bits_left -= self.num_remaining_bits_in_cur_byte
            if self.update_curbyte():
                return Constant.PVA_ERR_READ_BIT
        self.num_remaining_bits_in_cur_byte -= bits_left
        self.used_bits += num_bits
        return Constant.PVA_OK

    def skip_longbits(self, num_bits):
        if self.skip_bits(16):
            return Constant.PVA_ERR_READ_BIT
        if self.skip_bits(num_bits - 16):
            return Constant.PVA_ERR_READ_BIT
        return Constant.PVA_OK

    def show_bits(self, num_bits, out):
        tmp_self = copy.deepcopy(self)
        ret = 0
        if num_bits <= 31:
            ret = self.read_bits(num_bits, out)
        else:
            ret = self.read_longbits(num_bits, out)
        self = copy.deepcopy(tmp_self)
        return ret

    def show_longbits(self, num_bits, out):
        ret = 0
        tmp_self = copy.deepcopy(self)
        ret = read_longbits(num_bits, out)
        self = copy.deepcopy(tmp_self)
        return ret

    def read_ue(self, val):
        num_bits = -1
        bit = [0]
        rest = [0]
        if self.read_bits(1, bit):
            return Constant.PVA_ERR_READ_BIT
        num_bits += 1
        while bit[0] == 0:
            if self.read_bits(1, bit):
                return Constant.PVA_ERR_READ_BIT
            num_bits += 1
        if num_bits > 31:
            return -1
        val[0] = (1 << num_bits) - 1
        if num_bits > 0:
            if self.read_bits(num_bits, rest):
                return Constant.PVA_ERR_READ_BIT
            val[0] += rest[0]
        return Constant.PVA_OK

    def read_se(self, val):
        ue = [0]
        if self.read_ue(ue):
            return Constant.PVA_ERR_READ_BIT
        if ue[0] % 2 == 0:
            val[0] = -(ue[0] >> 1)
        else:
            val[0] = (ue[0] >> 1) + 1
        return Constant.PVA_OK

    def has_more_rbsp_data(self):
        if self.num_remaining_bits_in_cur_byte == 0 and self.update_curbyte():
            return 0
        if len(self.data):
            return 1
        return (self.cur_byte & ((1 << (self.num_remaining_bits_in_cur_byte - 1))
                                 - 1)) != 0

    def align_get_bits(self):
        if self.num_remaining_bits_in_cur_byte:
            self.skip_bits(n)
        return self.data

    def set_pre_detection(self):
        self.need_prevention_detection = 1
