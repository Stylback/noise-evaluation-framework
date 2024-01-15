from scipy import signal as Filterps
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import os
import sys

#A lowpass filter that utilises a buttersworth filter.
#The parameters are the cutoff frequency, the sampleing 
#frequency, the order of filter and the signal that one
#whishes to filter.
#It is important that the sampeling frequency is atleast dubble
#the cutoff frequency to match NyQuisty law.
#The output is the filtered signal in the format of
#[[amplitude, time], [another sample]]
def lowPassButter(cutoff_frequency, sampling_frequency, order, signal):
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

#A lowpass filter that utilises a buttersworth filter.
#The parameters are the cutoff frequency, the sampleing 
#frequency, the order of filter and the signal that one
#whishes to filter.
#It is important that the sampeling frequency is atleast dubble
#the cutoff frequency to match NyQuisty law.
#The output is the filtered signal in the format of
#[[amplitude, time], [another sample]]
def lowPassCheby(cutoff_frequency, sampling_frequency, order, signal):
    #Create the filter
    normilised_cutoff = cutoff_frequency / (0.5 * sampling_frequency)
    b, a = Filterps.cheby1(order, rp = 1, Wn = normilised_cutoff, btype="low", analog=False)

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

#A lowpass filter that utilises a buttersworth filter.
#The parameters are the cutoff frequency, the sampleing 
#frequency, the order of filter and the signal that one
#whishes to filter.
#It is important that the sampeling frequency is atleast dubble
#the cutoff frequency to match NyQuisty law.
#The output is the filtered signal in the format of
#[[amplitude, time], [another sample]]
def lowPassEllip(cutoff_frequency, sampling_frequency, order, signal):
    #Create the filter
    normilised_cutoff = cutoff_frequency / (0.5 * sampling_frequency)
    b, a = Filterps.ellip(order, normilised_cutoff, btype="low", analog=False)

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

#A lowpass filter that utilises a buttersworth filter.
#The parameters are the cutoff frequency, the sampleing 
#frequency, the order of filter and the signal that one
#whishes to filter.
#It is important that the sampeling frequency is atleast dubble
#the cutoff frequency to match NyQuisty law.
#The output is the filtered signal in the format of
#[[amplitude, time], [another sample]]
def lowPassBessel(cutoff_frequency, sampling_frequency, order, signal):
    #Create the filter
    normilised_cutoff = cutoff_frequency / (0.5 * sampling_frequency)
    b, a = Filterps.bessel(order, normilised_cutoff, btype="low", analog=False)

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

#This one is called main for easy calling with GUI solution but
#same as Filtere_delete
def main(signal):
    sample_interval = signal[1][1] - signal[0][1]
    sampling_frequency = 1.0 / sample_interval
    
    filteredButter = lowPassButter(8, sampling_frequency, 3, signal)
    filteredCheby = lowPassCheby(8, sampling_frequency, 3, signal)

    return filteredButter, filteredCheby