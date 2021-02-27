#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import struct
import sys
import wave

import numpy as np


def writetofile(length, freq0, freq1, a, filename):

    amplitude = 0.1
    framerate = 44100

    points = np.round(framerate * length)
    # print(points)
    # print(np.arange(points))

    tone1 = np.sin(np.arange(points) / points * 2 * np.pi * freq0 * length)
    tone2 = np.sin(np.arange(points) / points * 2 * np.pi * freq1 * length)

    bytes0 = b''.join([struct.pack('h', int(e * (2 ** 15) * amplitude)) for e in np.array(tone1)])
    bytes1 = b''.join([struct.pack('h', int(e * (2 ** 15) * amplitude)) for e in np.array(tone2)])
    # print(bytes1)

    wf = wave.open(filename, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(44100)

    for i in a:
        if i:
            wf.writeframes(bytes1)
        else:
            wf.writeframes(bytes0)
