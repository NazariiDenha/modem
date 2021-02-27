#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import struct
import bitarray
import wave
import sys

import numpy as np


def readfromfile(length, freq0, freq1, filename):

    # print(bytes1)

    wf = wave.open(filename, 'rb')
    a = bitarray.bitarray()
    framerate = wf.getframerate()
    while True:
        data = wf.readframes(int(framerate * length))
        if data:
            data = [struct.unpack('h', data[2 * i:2 * i + 2])[0] / 2 ** 15 for i in range(int(len(data) / 2))]
            fre = np.fft.rfft(data)
            fre = np.abs(fre)
            freq = np.argmax(fre) / length
            print(freq)
            if abs(freq - freq0) < abs(freq - freq1):
                a.append(0)
            else:
                a.append(1)
        else:
            break
    # print(a)
    return a

if len(sys.argv)>=2:
    print(readfromfile(0.1, 440, 880, sys.argv[1]))

# readfromfile(0.1, 440, 880, 'denha.wav')
