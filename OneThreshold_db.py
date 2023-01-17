import math
import numpy as np

# adaptive endpointing algorithm
def check_stop(frame_data,frame_len,level, background, onSpeechFlag, forgetfactor = 3,adjustment = 0.05, threshold = 1):
    _, en_log = energy(frame_data,frame_len)
    current = en_log[0]
    isSpeech = 0
    level = ((level * forgetfactor) + current)/(forgetfactor + 1)
    if current < background:
        background = current
    else:
        background += (current - background) * adjustment
    if level < background:
        level = background
    if level - background > threshold:
        isSpeech = 1
        # first time entering speech part, turn the on-speech flag on
        onSpeechFlag = True
    print((level - background))
    return isSpeech, level, background, onSpeechFlag

# calculate the energy of frames
def energy(frame_data,frame_len):
    en, en_log = [], []
    for i in range(0,len(frame_data),frame_len):
        temp_en = 0
        for j in range(frame_len):
            temp_en += frame_data[i+j]**2
        if temp_en == 0:
            en.append(0.0)
            en_log.append(0.0)
        else:
            en.append(temp_en)
            en_log.append(math.log10(temp_en))
    return(en,en_log)

# a helper function to calculate the sum
def part_sum(start,end,target):
    sum = 0
    for i in range(start,end):
        sum += target[i]
    return sum