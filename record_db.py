import pyaudio
import wave
import numpy as np
import OneThreshold_db
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


# skip a little bit
for i in range(16):
    stream.read(chunk)
# record first 10 frames as backgound
for j  in range(10):
    data = stream.read(chunk)
    frames.append(data)
    background_data += convert_data(data)
# calculate the background and initial value of level
_, bg_energy_log = OneThreshold_db.energy(background_data, chunk)
background = OneThreshold_db.part_sum(0, 10, bg_energy_log)/10
level = bg_energy_log[0]
print("backgound: ", background)

IsSpeech = [1 for i in range(5)]
onSpeechFlag = False
while loop:
    data = stream.read(chunk)
    frames.append(data)
    rt_data = convert_data(data)
    # adaptive endpointing algorithm
    terminate, level, background, onSpeechFlag = OneThreshold_db.check_stop(rt_data,1024, level, background, onSpeechFlag)
    IsSpeech.append(terminate)
    check = 0
    # stream terminates with 5 sequential frames not speech
    for idx in range(len(IsSpeech)-5,len(IsSpeech)):
        check += IsSpeech[idx]
    if check == 0:
        loop = False
    else:
        loop = True
    # check the on-speech flag
    if not onSpeechFlag:
        loop = True
stream.stop_stream()
stream.close()
p.terminate()   
 
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

