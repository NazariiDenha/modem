#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import bitarray


def nrzi4b5b(a):
    q = {'0000': '11110', '0001': '01001', '0010': '10100', '0011': '10101',
         '0100': '01010', '0101': '01011', '0110': '01110', '0111': '01111',
         '1000': '10010', '1001': '10011', '1010': '10110', '1011': '10111',
         '1100': '11010', '1101': '11011', '1110': '11100', '1111': '11101'}
    b = bitarray.bitarray()
    for i in range(len(a) // 4):
        b.extend(bitarray.bitarray(q[a[i * 4:i * 4 + 4].to01()]))
    if len(a) % 4 != 0:
        b.extend(a[-(len(a) % 4):])
    c = bitarray.bitarray([(b.count(True, 0, i + 1) + 1) % 2 for i in range(len(b))])
    return c


def restore(a):
    a = bitarray.bitarray([1]) + a
    b = bitarray.bitarray([a[i] ^ a[i + 1] for i in range(len(a) - 1)])
    q = {'11110': '0000', '01001':'0001', '10100':'0010', '10101':'0011',
         '01010':'0100', '01011':'0101', '01110':'0110', '01111':'0111',
         '10010':'1000', '10011':'1001', '10110':'1010', '10111':'1011',
         '11010':'1100', '11011':'1101', '11100':'1110', '11101':'1111'}
    c = bitarray.bitarray()
    for i in range(len(b) // 5):
        c.extend(bitarray.bitarray(q[b[i * 5:i * 5 + 5].to01()]))
    if len(b) % 5 != 0:
        c.extend(b[-(len(b) % 5):])
    return c
