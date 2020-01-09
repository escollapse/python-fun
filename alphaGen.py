#/usr/bin/env python2
#
# alphaGen.py
# ver 0.1 - 20200109
#
# generates the sequence AAAABBBB...ZZZZ
#     built for probing memory space
#     particularly useful for exploit-exercises' protostar
#
# **************
# * escollapse *
# * CISSP, PT+ *
# *  20200109  *
# **************
from __future__ import print_function
for i in range(0x41, 0x41 + 26):
    for j in range(4):
        print(chr(i), end='')
