#!/usr/bin/python

import sys


class FileReader:

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        try:
            self.fsin = open(self.filename, mode)
        except IOError:
            print "file open failed " + self.filename
            self.fsin = 0

    def __del__(self):
        if self.fsin and not self.fsin.closed:
            self.fsin.close()

    def get_one_frame(self):
        find_one_frame = False
        find_first = False
        find_second = False
        find_third = False
        oneframe_bytes = []
        for i in range(4):
            onebyte = self.fsin.read(1)
            if not onebyte:
                break
            oneframe_bytes.append(int(hex(ord(onebyte)), 16))
        while 1:
            onebyte = self.fsin.read(1)
            if not onebyte:
                break
            value = int(hex(ord(onebyte)), 16)
            if value == 0x00 and not find_first:
                # print "find first"
                find_first = True
            elif value == 0x00 and find_first and not find_second:
                # print "find second"
                find_second = True
            elif value == 0x00 and find_second and not find_third:
                # print "find Third"
                find_third = True
            elif value == 0x01 and (find_second or find_third) and not find_one_frame:
                # print "find one frame"
                find_one_frame = True
                offset = 1
                if oneframe_bytes[-3] == 0x00:
                    offset += 1
                    oneframe_bytes.pop()
                # remove 0x00 0x00
                oneframe_bytes.pop()
                oneframe_bytes.pop()
                offset += 2
                self.fsin.seek(-offset, 1)
                break
            else:
                find_first = False
                find_second = False
                find_one_frame = False
            oneframe_bytes.append(value)
            # print oneFrameBytes[-1]
        print oneframe_bytes
        return oneframe_bytes
