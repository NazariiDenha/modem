#!/usr/bin/env python3
import pyaudio
import sys
import time
import struct
import wave
import numpy as np
from bitarray import  bitarray
import nrzi4b5b


def startdecoding():
    a = bitarray()
    #a.append(True)
    print("tadam")
    while True:
        if isfile:
            data = stream.readframes(int(framerate * length))
        else:
            data = stream.read(int(framerate * length))
        if (len(data) == 0):
            break
        res = [struct.unpack('h', data[2 * i:2 * i + 2])[0] / 2 ** 15 for i in range(int(len(data) / 2))]
        fre = np.fft.rfft(res)
        fre = np.abs(fre)
        freq = np.argmax(fre) / length
        if abs(freq - 880) <= 10:
            a.append(True)
        elif abs(freq - 440) <= 10:
            a.append(False)
        else:
            break
        #print(a[-1])
    a = a[:-1]
    print(a)
    a = a[64:]
    a = nrzi4b5b.restore(a)
    # print(a)

    dst = struct.unpack('!LH', a[:48].tobytes())[0] * (2 ** 15) + struct.unpack('!LH', a[:48].tobytes())[1]
    src = struct.unpack('!LH', a[48:96].tobytes())[0] * (2 ** 15) + struct.unpack('!LH', a[48:96].tobytes())[1]
    lenn = struct.unpack('!H', a[96:112].tobytes())[0] * 8
    msg = a[112:112 + lenn].tobytes().decode('utf-8')
    print (src, dst, msg)
    return

stream = 0

isfile = False

if len(sys.argv) >= 2:
    isfile = True
    stream = wave.open(sys.argv[1], 'rb')
    framerate = stream.getframerate()
else:
    pa = pyaudio.PyAudio()

    stream = pa.open(
        input=True,
        channels=2,
        rate=44100,
        format=pa.get_format_from_width(2),
    )
    framerate = 44100

length = 0.1

last = []

#print(isfile)
k = 0
while True:
    if isfile:
        data = stream.readframes(int(framerate * length * 0.1))
    else:
        data = stream.read(int(framerate * length * 0.1))
    if (len(data) == 0):
        break
    res = [ struct.unpack('h', data[2*i:2*i+2])[0] / 2**15 for i in range(int(len(data)/2)) ]
    last.append(res)
    if len(last) > 10:
        last = last[1:]
    k += 1
    if len(last) == 10:
        un = []
        for it in last:
            un.extend(it)
        fre = np.fft.rfft(un)
        fre = np.abs(fre)
        freq = np.argmax(fre) / length
        #print(fre)
        #print(freq)
        if abs(freq - 880) <= 10:
            #print(k)
            last.clear()
            startdecoding()

#stream.stop_stream()
if isfile:
    stream.close()
if not isfile:
    pa.terminate()
