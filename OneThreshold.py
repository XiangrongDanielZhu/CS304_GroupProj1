import math
import numpy as np

def check_stop(frame_data,frame_len,level, background, forgetfactor = 1,adjustment = 0.05, threshold = 0):
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
    print((level - background) * 10)
    return isSpeech, level, background

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

def part_sum(start,end,target):
    sum = 0
    for i in range(start,end):
        sum += target[i]
    return sum