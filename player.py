#!/usr/bin/env python3
 
import pyaudio
import wave
import sys
 
CHUNK = 1024
 
if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)
print(sys.argv[1])
 
wf = wave.open(sys.argv[1], 'rb')
 
pa = pyaudio.PyAudio()
print(wf.getnchannels())
print(wf.getframerate())
print(wf.getsampwidth())
 
stream = pa.open(
            output=True,
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            format=pa.get_format_from_width(wf.getsampwidth()),
        ) 

k = 0

#data = wf.readframes(44100)
#stream.write(data)

while True:
    data = wf.readframes(CHUNK)
    if data:
        stream.write(data)
    else:
        break
    k += 1

print(k)
stream.stop_stream()
stream.close()
pa.terminate()
