import pyaudio
import wave
import numpy as np
import OneThreshold
import keyboard

def convert_data(data):
    rt_data = np.frombuffer(data, np.dtype('<i2'))
    rt_data.shape = -1,1
    rt_data = rt_data.T[0].tolist()
    return rt_data

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
background_data = []
loop = True


# skip the first 0.32 seconds
for i in range(5):
    stream.read(chunk)

# record first 10 frames as backgound
for i  in range(10):
    data = stream.read(chunk)
    frames.append(data)
    background_data += convert_data(data)

background_en, _ = OneThreshold.energy(background_data, chunk)
background = OneThreshold.part_sum(0, 10, background_en)
level = background_en[0]

while loop:
    data = stream.read(chunk)
    frames.append(data)
    rt_data = convert_data(data)
    frame_data += rt_data
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

