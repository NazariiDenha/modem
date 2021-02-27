#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import struct
import sys

import numpy as np
import pyaudio

pa = pyaudio.PyAudio()

amplitude = 0.1
framerate = 44100

length = 1
freq1  = 440
freq2  = 880

points = np.round(framerate*length)
#print(points)
#print(np.arange(points))

tone1 = np.sin(np.arange(points)/points*2*np.pi*freq1*length)
tone2 = np.sin(np.arange(points)/points*2*np.pi*freq2*length)

bytes1 = b''.join([struct.pack('h', int(e * (2**15) * amplitude)) for e in np.array(tone1)])
bytes2 = b''.join([struct.pack('h', int(e * (2**15) * amplitude)) for e in np.array(tone2)])
#print(bytes1)

stream = pa.open(
            output=True,
            channels=1,
            rate=framerate,
            format=pa.get_format_from_width(2),
        )
#while True:
stream.write( bytes1 )
stream.write( bytes2 )