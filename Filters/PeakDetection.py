from scipy import signal as Filterps
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import os

#A lowpass filter that utilises a buttersworth filter.
#The parameters are the cutoff frequency, the sampleing 
#frequency, the order of filter and the signal that one
#whishes to filter.
#It is important that the sampeling frequency is atleast dubble
#the cutoff frequency to match NyQuisty law.
#The output is the filtered signal in the format of
#[[amplitude, time], [another sample]]
def lowPass(cutoff_frequency, sampling_frequency, order, signal):
    #Create the filter
    normilised_cutoff = cutoff_frequency / (0.5 * sampling_frequency)
    b, a = Filterps.butter(order, normilised_cutoff, btype="low", analog=False)

    #Get the signal values
    amplitude = np.zeros(len(signal))
    for x in range(len(signal)):
        amplitude[x] = signal[x][0]
    
    #Filter signbal
    Filtered_signal = Filterps.lfilter(b, a, amplitude)

    #Create the return array
    back_signal = [[0, 0]] * len(signal)
    for x in range(len(back_signal)):
        back_signal[x] = [Filtered_signal[x], signal[x][1]]
    return back_signal

#Gernerates the slope sum function depending on the window size.
#to see when the values are rising. Windows size should be about
#one cycle or 128ms which is 32 samples at 250Hz.
#Input is the windows size of and the signal in with the signal
#format of [[value, time]]
#The output is a array of the format [[value, time]]
def SlopeSum(windowSize, signal):
    #Create the delta y values
    DeltaY = np.zeros(len(signal))
    DeltaY[0] = 0
    for x in range(1, len(signal)):
        DeltaY[x] = signal[x][0] - signal[x-1][0]

    #Create the delta u values
    DeltaU = np.zeros(len(DeltaY))
    for x in range(len(DeltaY)):
        if DeltaY[x] > 0:
            DeltaU[x] = DeltaY[x]
    
    #Create new values
    window = np.zeros(windowSize) #The window of values
    ssf = np.zeros(len(signal)) #The new values
    for x in range(windowSize + 1, len(signal)):
        index = x % windowSize
        window[index] = DeltaU[x]
        ssf[x] = sum(window)

    #Create the return array
    back_signal = [[0, 0]] * len(ssf)
    for x in range(len(back_signal)):
        back_signal[x] = [ssf[x], signal[x][1]]
    return back_signal

def Threshold_init(signal):
    return 3*(sum(signal) / len(signal))

#finds the min and max values for the windows of
#150ms before and after the time designated at
#sample number x.
def min_max(x, signal):
    small_signal = []
    index_start = None
    index_end = None
    #Find the start and end times
    for y in range(len(signal)):
        if signal[x-y][1] <= (signal[x][1] - 0.15):
            index_start = x-y
            break
        else:
            continue
    for y in range(len(signal)):
        if x+y >= len(signal):
            index_end = len(signal)-1
        elif signal[x+y][1] >= (signal[x][1] + 0.15):
            index_end = x+y
            break
        else:
            continue

    #Create the new signal
    for y in range(index_start, index_end):
        small_signal.append(signal[y])

    #Find the smallest and largets values
    min = [999, 999]
    max = [0, 0]
    for y in range(len(small_signal)):
        if small_signal[y][0] > max[0]:
            max = small_signal[y]
        elif small_signal[y][0] < min[0]:
            min = small_signal[y]
        else:
            continue
    return min, max


def find_onset(x, signal, max):
    for y in range(0, x):
        if signal[x-y][0] < (0.1 * max):
            return signal[x-y-5][1]

def check_dubbles(onsets):
    back_array = []
    for x in range(len(onsets)-1):
        if onsets[x] != onsets[x+1]:
            back_array.append(onsets[x])
    if len(onsets) != 0:
        back_array.append(onsets[len(onsets)-1])
    return back_array


#Find the potential peaks of the beats and needs a start
#value which is the time variable, usually 10 seconds
def decision_rule(time, signal):
    #start parameters
    dection_point = 20 #The difference between max and min to detect a onset
    onsets = []
    maximum = 0
    index_wait = 0
    wait_time = [1] * 10
    wait = 0

    #Creates the signal with the values for the first
    #seconds defined by the time variable.
    init_signal = []
    for x in range(len(signal)):
        if signal[x][1] >= time:
            break
        else:
            init_signal.append(signal[x][0])

    base_threshold = Threshold_init(init_signal)
    actual_threshold = 0.6 * base_threshold

    for x in range(len(signal)):
        #Find the maximum ssf in a beat
        if signal[x][0] > maximum and signal[x][0] < 100:
            maximum = signal[x][0]

        #Find the next beat when it is above thershold
        if signal[x][0] > actual_threshold and wait <= 0:
            min, max = min_max(x, signal)
            #If the difference is large enough for new beat
            if (max[0] - min[0]) >= dection_point:
                onsets.append(find_onset(x, signal, maximum))
                wait = (stat.median(wait_time))/2
                wait_time[index_wait%len(wait_time)] = onsets[len(onsets)-1] - onsets[len(onsets)-2]
                index_wait += 1
                actual_threshold = 0.6 * maximum
                maximum = 10
                continue
        elif wait > 0:
            wait = wait - (signal[x][1] - signal[x-1][1])
            
    onsets.sort()
    onsets = check_dubbles(onsets)

    return onsets

#Finds the systol values with the use of the signal and the
#vlaues for the beat onsets.
#Input is the signal one wants to look at and the array of
#onset times.
#The output is a array of the systolic values and time in
#format of [[value, time]]
def findSystol(signal, onsets):
    systols = []
    time_end = onsets[1]
    index = 0
    maximum = signal[0]

    #Finds the time for first beat cycle
    for x in range(len(signal)):
        if signal[x][1] >= onsets[0]:
            break
        else:
            index += 1

    #Go through all onsets
    for x in range(2, len(onsets)):
        #Get maximum until next onset value
        for y in range(index, len(signal)):
            #If we reach next beat or end of signal
            if signal[y][1] >= time_end or y == (len(signal)-1):
                systols.append(maximum)
                maximum = signal[y]
                break
            #If current value is new maximum
            elif maximum[0] < signal[y][0]:
                maximum = signal[y]
                index += 1
            else:
                index += 1
                continue
        time_end = onsets[x]

    #The second to last value
    for y in range(index, len(signal)):
            #If we reach next beat or end of signal
            if signal[y][1] >= time_end or y == (len(signal)-1):
                systols.append(maximum)
                maximum = signal[y]
                break
            #If current value is new maximum
            elif maximum[0] < signal[y][0]:
                maximum = signal[y]
                index += 1
            else:
                index += 1
                continue
    
    #The last value
    for y in range(index, len(signal)):
            #If we reach end of signal
            if y == (len(signal)-1):
                systols.append(maximum)
                break
            #If current value is new maximum
            elif maximum[0] < signal[y][0]:
                maximum = signal[y]
                index += 1
            else:
                index += 1
                continue
    return systols

#Finds the diastolic values with the use of the signal and the
#vlaues for the beat onsets.
#Input is the signal one wants to look at and the array of
#systolic values and times.
#The output is a array of the diastolic values and time in
#format of [[value, time]]
def findDiastolic(signal, systolics):
    diastolic = []
    time_end = systolics[1][1]
    index = 0
    min = signal[0]

    #Finds the time for first beat cycle
    for x in range(len(signal)):
        if signal[x][1] >= systolics[0][1]:
            break
        else:
            index += 1

    #Go through all systolic values
    for x in range(2, len(systolics)):
        #Get minimum until next onset value
        for y in range(index+10, len(signal)):
            #If we reach next beat or end of signal
            if signal[y][1] >= time_end or y == (len(signal)-1):
                diastolic.append(min)
                min = signal[y]
                break
            #If current value is new maximum
            elif min[0] > signal[y][0]:
                min = signal[y]
                index += 1
            else:
                index += 1
                continue
        time_end = systolics[x][1]
    #To get the last value
    for y in range(index, len(signal)):
            #If we reach next beat or end of signal
            if signal[y][1] >= time_end or y == (len(signal)-1):
                diastolic.append(min)
                min = signal[y]
                break
            #If current value is new maximum
            elif min[0] > signal[y][0]:
                min = signal[y]
                index += 1
            else:
                index += 1
                continue
    return diastolic

#A function that gets the onsets of the beats, systolic pressures
#and diastolic pressures from a signal.
#The input is the signal and the ineterval between each sample.
#The aoutput is three arrays with the first being the onsets in the
#format of [time, time], the systolic values in the format of 
#[[value, time]] and diastolic values in format [[value, time]]
def onsetDetection(signal, sampeling_interval):
    #Filtering properties
    sampling_frequency = 1.0 / sampeling_interval
    signal_filtered = lowPass(16, sampling_frequency, 2, signal)

    #Creates the ssf signal
    ssf = SlopeSum(32, signal_filtered)
    time = (signal[len(signal)-1][1])/5

    onsets = decision_rule(time, ssf)

    systols = findSystol(signal, onsets)
    diastolic = findDiastolic(signal, systols)

    return onsets, systols, diastolic