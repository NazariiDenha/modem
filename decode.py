#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import nrzi4b5b
import struct
import readfromfile
import sys


def decode(filename):
    a = readfromfile.readfromfile(0.1, 440, 800, filename)
    # print(a)
    a = a[64:]
    # print(a)
    # print("hahaha")
    a = nrzi4b5b.restore(a)
    # print(a)

    dst = struct.unpack('!LH', a[:48].tobytes())[0] * (2 ** 15) + struct.unpack('!LH', a[:48].tobytes())[1]
    src = struct.unpack('!LH', a[48:96].tobytes())[0] * (2 ** 15) + struct.unpack('!LH', a[48:96].tobytes())[1]
    lenn = struct.unpack('!H', a[96:112].tobytes())[0] * 8
    print(lenn, len(a) - 112)
    msg = a[112:112 + lenn].tobytes().decode('utf-8')
    return (src, dst, msg)

if __name__ == "__main__":
    src, dst, msg = decode(sys.argv[1])
    print(src, dst, msg)


