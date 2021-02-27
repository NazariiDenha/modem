#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import bitarray

def divide(a, b):
    c = bitarray.bitarray()
    for i in range(len(a) - len(b) + 1):
        if a[i] and i + len(b) <= len(a):
            a[i:i+len(b)] = a[i:i+len(b)] ^ b
            c.append(1)
        else:
            c.append(0)
    c = c[c.index(True):]
    a = a[a.index(True):]
    return (c, a)
