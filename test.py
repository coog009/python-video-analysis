#!/usr/bin/python

import sys
import copy


class A:
    C = 5
    D = C + 5

    def __init__(self):
        self.a = 5

    def self_print(self):
        print self.a
        tmp_self = copy.deepcopy(self)
        self.a = 6
        print self.a
        self = copy.deepcopy(tmp_self)
        print self.a

a = A()
a.self_print()

print a.a
print "hahah %d" % A.D

value = 0x0
value_list = []

value_list.append(10)
value_list.append(5)

del value_list[0]

print value_list[-1]
print type(value_list[0])
print value_list
