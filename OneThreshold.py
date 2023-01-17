import math
import numpy as np

def check_stop(frame_data,frame_len):
    en, en_log = energy(frame_data,frame_len)
    print(en[-1]/10**6)
    #print(len(en))
    IsSpeech, det = endpoint(en,forget_factor = 2, adjustment = 0.05, threshold= 5.4*10**6)
    smooth(IsSpeech)
#   IsSpeech, det = endpoint(en_log, forget_factor=3, adjustment=0.05, threshold=0.36)
    #print(IsSpeech)
    check = 0
    for i in range(len(IsSpeech)-5,len(IsSpeech)):
        check += IsSpeech[i]
    if check == 0:
        return True
    return False
    
def endpoint(data,forget_factor, adjustment, threshold):
    background = part_sum(0,10,data)
    IsSpeech = []    
    det = []

    level = data[0]
    for current in range(len(data)):
        is_speech = 0
        level = ((level*forget_factor) + data[current])/(forget_factor+1)
        
        if data[current] < background:
            background = data[current]
        else:
            background += (data[current]-background) * adjustment
        
        if level < background:
            level = background
        
        #print(level-background)
        
        if (level-background) > threshold:
            is_speech = 1
    
        
        det.append(level-background)
        IsSpeech.append(is_speech)

    return IsSpeech, det



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

def remove_zero(L1, L2):
    for i in range(len(L1)-1):
        if L1[i] == 0:
            if L1[i+1]!= 0:
                L1[i] = L2[i]
            else:
                L1[i] = None    
        if L2[i] == 0:
            if L2[i+1]!= 0:
                L2[i] = L1[i]
            else:
                L2[i] = None 
        
    return L1, L2

def smooth(L1):
    i=0
    while i<=(len(L1)-5):
        if zeroCount(L1[i:i+5])==1:
            for j in range(5):
                L1[i+j]=1
        i=i+3
    return L1

def zeroCount(data):
    for i in range(5):
        if data<3:
            return 1
        else:
            return 0 

def part_sum(start,end,target):
    sum = 0
    for i in range(start,end):
        sum += target[i]
    return sum
