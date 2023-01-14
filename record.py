import pyaudio
import wave
from endpointing import *
import numpy as np
import OneThreshold
import keyboard

chunk = 1024      # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16      # 16 bits per sample
channels = 1      # Number of audio channels
fs = 16000        # Record at 16000 samples per second
time_in_seconds = 10
filename = "recording.wav"

print('Press "space" to start recording.')
keyboard.wait('space')
p = pyaudio.PyAudio()  # Create an interface to PortAudio


print('-----Now Recording-----')
 
#Open a Stream with the values we just defined
stream = p.open(format=sample_format,
                channels = channels,
                rate = fs,
                frames_per_buffer = chunk,
                input = True)
 
frames = []  # Initialize array to store frames
frame_data = []
loop = True
# Store data in chunks for 10 seconds

for i in range(20):
    data = stream.read(chunk)
    frames.append(data)
    rt_data = np.frombuffer(data, np.dtype('<i2'))
    rt_data.shape = -1,1
    rt_data = rt_data.T[0].tolist()
    frame_data += rt_data
    #print(len(frame_data)/1024)

while loop:
    data = stream.read(chunk)
    frames.append(data)
    
    rt_data = np.frombuffer(data, np.dtype('<i2'))
    rt_data.shape = -1,1
    rt_data = rt_data.T[0].tolist()
    frame_data +=rt_data
    #print(len(frame_data)/1024)
    if OneThreshold.check_stop(frame_data,1024):
        stream.stop_stream()
        stream.close()
        p.terminate()
        loop = False
    else:
        loop = True
    #print(rt_data.shape)
    
 
# Stop and close the Stream and PyAudio

 
print('-----Finished Recording-----')
 
# Open and Set the data of the WAV file
file = wave.open(filename, 'wb')
file.setnchannels(channels)
file.setsampwidth(p.get_sample_size(sample_format))
file.setframerate(fs)
 
#Write and Close the File
file.writeframes(b''.join(frames))
file.close()