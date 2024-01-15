from scipy import signal as Filterps
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import os
import sys
import math

directory = os.path.dirname(os.path.realpath(__file__)) #This was simply done to not have peakdetection in testfilter folder

parent = os.path.dirname(directory)

# setting path
sys.path.append(parent)
import PeakDetection as peak

#Saves the values that are less than the lower limit and above the
#upper limit. 
#The perameters are the onset times of a beat in the format of 
#[time1, time2,...], the systolic values in the format of [[value, time]]
#and lastly the diastolic values in the format of [[value, time]]
#The return is a array of the time for beats that contain a fault in them
#this is in the format of [[start time of beat, end time of beat]].
def LimitFilter(onsets, systolic, diastolic, signal):
    sys_upr = 250
    sys_lwr = 30
    dia_upr = 200
    dia_lwr = 15 #Should be 15
    faulty = []

    #Find faulty systolic values
    for x in range(len(systolic)):
        if systolic[x][0] < sys_lwr or systolic[x][0] > sys_upr:
            if x + 1 < len(onsets):
                faulty.append([onsets[x], onsets[x+1]])
            else:
                faulty.append([onsets[x], signal[len(signal)-1][1]])
    
    #Find faulty diastolic values
    for x in range(len(diastolic)):
        if diastolic[x][0] < dia_lwr or diastolic[x][0] > dia_upr:
            if x + 1 < len(onsets):
                faulty.append([onsets[x], onsets[x+1]])
            else:
                faulty.append([onsets[x], signal[len(signal)-1][1]])
    faulty = sorted(faulty, key=lambda x: x[0], reverse=False)
    return faulty

def long(onset, length, signal):
    window = [None] * length
    average = 0
    faulty = []

    for x in range(length):
        window[x] = onset[x+1] - onset[x]

    for x in range(length, len(onset)-2):
        average = sum(window) / length
        tested = onset[x+1] - onset[x]
        if tested > 2*average:
            if x + 1 < len(onset):
                faulty.append([onset[x], onset[x+1]])
            else:
                faulty.append([onset[x], signal[len(signal)-1][1]])

    faulty = sorted(faulty, key=lambda x: x[0], reverse=False)
    return faulty

def avg_negative(signal):
    for x in range(len(signal) - 1):
        if signal[x][0] < 0:

            max_length = len(signal)-1

            value1 = 0
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            
            if x-2 >= 0:
                value1 = signal[x-2][0]
            if x-1 >= 0:
                value2 = signal[x-1][0]
            if x >= 0 and x <= max_length:
                value3 = signal[x][0]
            if x+1 <= max_length:
                value4 = signal[x+1][0]
            if x+2 <= max_length:
                value5 = signal[x+2][0]

            if value1 < 0:
                value1 = 0
            if value2 < 0:
                value2 = 0
            if value3 < 0:
                value3 = 0
            if value4 < 0:
                value4 = 0
            if value5 < 0:
                value5 = 0
            signal[x][0] = (value1+value2+value3+value4+value5)/5
        else:
            continue


def negative(onsets, signal):
    faulty = []

    for x in range(len(signal) - 1):
        if signal[x][0] < 0:
            index = find_negative(onsets, signal[x][1])
            if index != len(onsets)-1:
                faulty.append([onsets[index], onsets[index+1]])
            else:
                faulty.append([onsets[index], signal[len(signal)-1][1]])

    faulty = sorted(faulty, key=lambda x: x[0], reverse=False)
    #Remove duplicates
    saved = []
    deleted = 0
    for x in range(len(faulty)-2):
        if faulty[x][0] == faulty[x+1][0] and faulty[x][1] == faulty[x+1][1]:
            saved.append(x)
    for x in saved:
        del faulty[x-deleted]
        deleted += 1
    return faulty

def find_negative(onsets, time):
    for x in range(len(onsets)-1):
        if onsets[x] > time:
            return x-1
    return len(onsets)-1

def bigChanges(onsets, systolic, diastolic, signal):
    systolic_limit = 15
    diastolic_limit = 10
    time_limit = 20
    faulty = []
    start_time = 0

    #Gets the widnows of first 10 seconds
    for x in range(len(onsets)):
        if onsets[x] >= time_limit:
            start_time = x
    
    #Gets the values for the 10 second window
    systolic_window = [0] * start_time
    diastolic_window = [0] * start_time
    for x in range(start_time):
        systolic_window[x] = systolic[x][0]
        diastolic_window[x] = diastolic[x][0]

    #Tries to find the fauty signals
    for x in range(start_time, len(onsets)-1):
        sysQ3, sysQ1 = np.percentile(systolic_window, [75, 25])
        sysIQR = sysQ3 - sysQ1
        diaQ3, diaQ1 = np.percentile(diastolic_window, [75, 25])
        diaIQR = diaQ3 - diaQ1
        sysMedian = stat.median(systolic_window)
        diaMedian = stat.median(diastolic_window)

        if sysIQR < 1 and abs(systolic[x] - sysMedian) > systolic_limit:
            if x + 1 < len(onsets):
                faulty.append([onsets[x], onsets[x+1]])
            else:
                faulty.append([onsets[x], signal[len(signal)-1][1]])
        elif abs(systolic[x] - sysMedian) > 3*sysIQR:
            if x + 1 < len(onsets):
                faulty.append([onsets[x], onsets[x+1]])
            else:
                faulty.append([onsets[x], signal[len(signal)-1][1]])
        if diaIQR < 1 and abs(diastolic[x] - diaMedian) > diastolic_limit:
            if x + 1 < len(onsets):
                faulty.append([onsets[x], onsets[x+1]])
            else:
                faulty.append([onsets[x], signal[len(signal)-1][1]])
        elif abs(diastolic[x] - diaMedian) > 3*diaIQR:
            if x + 1 < len(onsets):
                faulty.append([onsets[x], onsets[x+1]])
            else:
                faulty.append([onsets[x], signal[len(signal)-1][1]])
        
        systolic_window[x%len(systolic_window)] = systolic[x]
        diastolic_window[x%len(diastolic_window)] = diastolic[x]

    return faulty

def dampening(onsets, systolic, diastolic):
    faulty = []
    lenght = 0
    if len(systolic) >= len(diastolic):
        lenght = len(diastolic)
    else:
        lenght = len(systolic)
    pp = [0] * lenght
    for x in range(len(pp)):
        pp[x] = systolic[x][0]-diastolic[x][0]
    
    
    b, a = Filterps.butter(2, 1/16, btype="low", analog=False)
    Filtered_pp = Filterps.lfilter(b, a, pp)

    pp = [[0,0]] * len(systolic)
    for x in range(lenght):
        pp[x] = systolic[x]
        pp[x][0] = Filtered_pp[x]
        pp[x][1] = onsets[x]

    for x in range(len(pp)):
        if pp[x][0] < 10:
            if x+10 < len(pp)-1:
                check = True #Used to know if 8 samples in a row is less than 10
                for y in range(x, x+10):
                    if pp[y][0] > 10:
                        check = False
                        break
                if check:
                    start = dampening_back(pp, x)
                    end = dampening_forward(pp, x)
                    faulty.append([start, end])
    
    return faulty

def dampening_back(pp, x):
    values = np.array([pp[x][0]])
    for y in range(x):
        limit = np.percentile(values, [25])
        if pp[x-y][0] > limit:
            return y
        else:
            values = np.insert(values, len(values), pp[x-y])
    return 0

def dampening_forward(pp, x):
    values = np.array([pp[x][0]])
    for y in range(len(pp)-x-1):
        limit = np.percentile(values, [25])
        if pp[y][0] > limit:
            return y
        else:
            values = np.insert(values, len(values), pp[x-y])
    return len(pp)
    
def delete_faulty(signal, faulty):
    index = 0
    #goes through the list of faulty signal
    for x in range(0, len(faulty)):
        place = index
        for y in range(place, len(signal)):
            if signal[index][1] < faulty[x][0]:
                index += 1
                continue
            elif signal[index][1] >= faulty[x][1]:
                break
            else:
                signal[index][0] = 0
                index += 1
                continue

def average_faulty(signal, faulty, wide):
    index = 0
    start = 0
    end = 0
    #goes through the list of faulty signal
    for x in range(0, len(faulty)):
        place = index
        for y in range(place, len(signal)):
            if signal[index][1] < faulty[x][0]:
                start = index
                index += 1
                continue
            elif signal[index][1] >= faulty[x][1]:
                end = index
                break
            else:
                index += 1
                continue
        medel(signal, start, end, wide)
        start = index
        end = index + 1

def medel(signal, start, end, wide):

    start1 = start
    end1 = end

    if start - wide > 0 and end + wide < len(signal):
        star1 = start-wide
        end1 = end+wide
    elif start - wide < 0 and end + wide < len(signal):
        end1 = end+wide
    elif start - wide >= 0 and end + wide >= len(signal):
        start1= start-wide

    length = end1 - start1

    if length == 0:
        return
    temp = [0] * length
    for x in range(start1, end1):
        temp[x - start1] = signal[x][0]
    
    avg = sum(temp) / len(temp)

    for x in range(start, end):
        signal[x][0] = avg

def FIR_faulty(signal, faulty, wide):
    index = 0
    start = 0
    end = 0
    #goes through the list of faulty signal
    for x in range(0, len(faulty)):
        place = index
        for y in range(place, len(signal)):
            if signal[index][1] < faulty[x][0]:
                start = index
                index += 1
                continue
            elif signal[index][1] >= faulty[x][1]:
                end = index
                break
            else:
                index += 1
                continue
        Window_smooth = math.floor((faulty[x][1]-faulty[x][0]) / 20)
        FIR_medel(signal, start, end, wide, Window_smooth)
        start = index
        end = index + 1

def FIR_medel(signal, start, end, wide, Window_smooth):

    if Window_smooth == None or Window_smooth == 0:
        return
    if end - start <= 0:
        return

    start1 = start
    end1 = end

    if start - wide > 0 and end + wide < len(signal):
        star1 = start-wide
        end1 = end+wide
    elif start - wide < 0 and end + wide < len(signal):
        end1 = end+wide
    elif start - wide >= 0 and end + wide >= len(signal):
        start1= start-wide

    length = end1 - start1

    if length == 0:
        return
    temp = [0] * length
    for x in range(start1, end1):
        temp[x - start1] = signal[x][0]
    
    avg = sum(temp) / len(temp)

    temp_faulty = []
    for x in range(start, end):
        temp_faulty.append(signal[x][0])
    avg_faulty = sum(temp_faulty) / len(temp_faulty)
    
    for x in range(start, (end - Window_smooth)):
        window = []
        for y in range(x, x + Window_smooth):
            window.append(signal[y][0])
        window_avg = sum(window) / len(window)
        signal[x][0] = window_avg

    for x in range(start, end):
        signal[x][0] = (avg + (signal[x][0] - avg_faulty)) 


def Filter_delete(signal):
    sample_interval = signal[1][1] - signal[0][1]
    sample_frequency = 1.0 / sample_interval

    print("Lowpass")
    back = peak.lowPass(8, sample_frequency, 3, signal)

    print("Onset")
    onsets, systolic, diastolic = peak.onsetDetection(back, sample_interval)

    wide = math.floor(len(back) / 200)

    #Find all of the faulty signals
    print("Find")
    faulty1 = LimitFilter(onsets, systolic, diastolic, back)
    faulty2 = bigChanges(onsets, systolic, diastolic, back)
    #faulty3 = dampening(onsets, systolic, diastolic)
    faulty3 = []
    faulty4 = long(onsets, 100, back)
    faulty5 = negative(onsets, back)

    if len(faulty1) < 1:
        faulty1.append([0,0])
    if len(faulty2) < 1:
        faulty2.append([0,0])
    if len(faulty3) < 1:
       faulty3.append([0,0])
    if len(faulty4) < 1:
        faulty4.append([0,0])
    if len(faulty5) < 1:
        faulty5.append([0,0])

    faulty1 = np.array(faulty1)
    faulty2 = np.array(faulty2)
    faulty3 = np.array(faulty3)
    faulty4 = np.array(faulty4)
    faulty5 = np.array(faulty5)

    faulty = np.concatenate((faulty1, faulty2, faulty3, faulty4))
    faulty = list(faulty)

    faulty = sorted(faulty, key=lambda time: time[0])


    print("Delete")
    #average_faulty(back, faulty5, wide)
    FIR_faulty(back, faulty, wide)
    print("Negative")
    avg_negative(back)

    return back


#This one is called main for easy calling with GUI solution but
#same as Filtere_delete
def main(signal):
    sample_interval = signal[1][1] - signal[0][1]
    onsets, systolic, diastolic = peak.onsetDetection(signal, sample_interval)

    #Find all of the faulty signals
    faulty1 = LimitFilter(onsets, systolic, diastolic)
    faulty2 = bigChanges(onsets, systolic, diastolic)
    faulty3 = dampening(onsets, systolic, diastolic)

    faulty = []
    faulty.append(faulty1)
    faulty.append(faulty2)
    faulty.append(faulty3)

    delete_faulty(signal, faulty)

    return signal

