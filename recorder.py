#!/usr/bin/env python3
import pyaudio
import wave
import sys
import time

CHUNK = 1024
 
if len(sys.argv) < 2:
    print("Records a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)
print(sys.argv[1])
 
wf = wave.open(sys.argv[1], 'wb')
wf.setnchannels(2)
wf.setsampwidth(2)
wf.setframerate(44100)

 
pa = pyaudio.PyAudio()
 
stream = pa.open(
            input=True,
            channels=2,
            rate=44100,
            format=pa.get_format_from_width(2),
        )

t_end = time.time() + int(sys.argv[2])
while time.time() < t_end:
    data = stream.read(CHUNK)
    if data:
        wf.writeframes(data)
    else:
        break

stream.stop_stream()
stream.close()
pa.terminate()
