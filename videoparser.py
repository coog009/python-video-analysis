#!/usr/bin/python

import sys
import getopt


class VideoParser:

    def __init__(self):
        self.input_name = ''
        self.output_name = ''

    def usage(self):
        print "usage"
        print "./main -i input_stream -o stat.csv"

    def parse_options(self, argv):
        try:
            opts, args = getopt.getopt(
                argv[1:], "i:o:h", ["input=", "output=", "help"])
        except getopt.GetoptError:
            print("find a error in input args")
            self.usage()
            sys.exit(1)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.usage()
                sys.exit(1)
            elif opt in ("-i", "--input"):
                self.input_name = arg
            elif opt in ("-o", "--output"):
                self.output_name = arg
        print "parse input parameters:"
        print "input file name ", self.input_name
        print "output file name ", self.output_name


def main():
    parser = VideoParser()
    if len(sys.argv) <= 1:
        parser.usage()
        sys.exit(1)
    parser.parse_options(sys.argv)

if __name__ == "__main__":
    main()
