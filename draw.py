#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import numpy as np
import sys
import time
import matplotlib.pyplot as plt 
import pyaudio
import struct

pa = pyaudio.PyAudio()

framerate = 44100

length = float( sys.argv[1] if len(sys.argv) > 1 else 0.1)

i=0

plt.ion()
fig = plt.figure()
stream = pa.open(
            input=True,
            channels=2,
            rate=framerate,
            format=pa.get_format_from_width(2),
        )
for i in range(100):
    res = stream.read(int(length * framerate))
    res = [ struct.unpack('h', res[2*i:2*i+2])[0] / 2**15 for i in range(int(len(res)/2)) ]
    fre = np.fft.rfft(res)
    fre = np.abs(fre)
    i = i+1
    if i*length >= 2:
        i = 0
        fig.clear()
        a = fig.add_subplot(311)
        b = fig.add_subplot(312)
        c = fig.add_subplot(313)
        a.plot(range(len(res)), res)
        b.plot(range(len(fre)), fre)
        c.plot(range(len(fre[0:1000])), fre[0:1000])
        fig.canvas.draw()
    print(np.argmax(fre)/length)
plt.ioff()
plt.show()
