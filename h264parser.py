#!/usr/bin/python

import sys
from videoparser import VideoParser as VideoParser
from filestream import FileReader as FileReader
from bitreader import BitReader as BitReader


class H264Parser(VideoParser):
    NALU_TYPE_NULL = 0
    NALU_TYPE_SLICE = 1
    NALU_TYPE_DPA = 2
    NALU_TYPE_DPB = 3
    NALU_TYPE_DPC = 4
    NALU_TYPE_IDR = 5
    NALU_TYPE_SEI = 6
    NALU_TYPE_SPS = 7
    NALU_TYPE_PPS = 8
    NALU_TYPE_AUD = 9
    NALU_TYPE_EOSEQ = 10
    NALU_TYPE_EOSTREAM = 11
    NALU_TYPE_FILL = 12
    NALU_TYPE_SPSEXT = 13
    NALU_TYPE_PREFIX = 14
    NALU_TYPE_SUB_SPS = 15
    NALU_TYPE_SLICE_AUX = 19
    NALU_TYPE_SLC_EXT = 20
    NALU_TYPE_VDRD = 24

    def __init__(self):
        pass


def main():
    parser = H264Parser()
    print "input argv ", len(sys.argv)
    if len(sys.argv) <= 1:
        parser.usage()
        sys.exit(1)
    parser.parse_options(sys.argv)
    fsreader = FileReader(parser.input_name, "rb")
    oneframe_bytes = fsreader.get_one_frame()
    bitsreader = BitReader(oneframe_bytes)
    bitsreader.set_pre_detection()
    value = [0]
    bitsreader.skip_longbits(32)
    bitsreader.read_bits(4, value)
    print value[0]
    bitsreader.read_bits(2, value)
    print value[0]
    bitsreader.read_bits(2, value)
    print value[0]
    bitsreader.read_bits(8, value)
    print value[0]
    bitsreader.read_ue(value)
    print value[0]
    del fsreader

if __name__ == "__main__":
    main()
