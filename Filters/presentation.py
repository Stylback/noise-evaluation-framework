from PeakDetection import *
import matplotlib.pylab as plt
import numpy as np

#Plots the old and new signal
def compareGraphs(signalOG, systolic_signal, dyastolic_signal):
    #Extract the values of the orgiginal signal
    timeOG= [None] * len(signalOG)
    amplitudeOG = [None] * len(signalOG)

    for x in range(len(signalOG)):
        timeOG[x] = signalOG[x][1]
        amplitudeOG[x] = signalOG[x][0]

    #Extarcts the values of systol
    systolic = np.zeros(len(signalOG))
    index = 0
    for x in range(len(signalOG)):
        if index < len(systolic_signal) and signalOG[x][1] == systolic_signal[index][1]:
            systolic[x] = systolic_signal[index][0] * 0.7
            index += 1
        elif index >= len(systolic_signal):
            break

    #Extarcts the values of dyastolic
    dyastolic = np.zeros(len(signalOG))
    index = 0
    for x in range(len(signalOG)):
        if index < len(dyastolic_signal) and signalOG[x][1] == dyastolic_signal[index][1]:
            dyastolic[x] = dyastolic_signal[index][0] * 0.7
            index += 1
        elif index >= len(dyastolic_signal):
            break
    
    plt.figure(figsize=(10, 6))

    # Plot original signal
    plt.subplot(1, 1, 1)
    plt.plot(timeOG, amplitudeOG, label='Original Signal')
    plt.plot(timeOG, systolic, label='systolic', color='red')
    plt.plot(timeOG, dyastolic, label='dyastolic', color='blue')
    plt.title('Original Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.show()

#Plots the old and new signal
def compareGraphs(signalOG, time_interval):

    onsets, systolic_signal, dyastolic_signal = onsetDetection(signalOG, time_interval)

    #Extract the values of the orgiginal signal
    timeOG= [None] * len(signalOG)
    amplitudeOG = [None] * len(signalOG)

    for x in range(len(signalOG)):
        timeOG[x] = signalOG[x][1]
        amplitudeOG[x] = signalOG[x][0]

    #Extarcts the values of systol
    systolic = np.zeros(len(signalOG))
    index = 0
    for x in range(len(signalOG)):
        if index < len(systolic_signal) and signalOG[x][1] == systolic_signal[index][1]:
            systolic[x] = systolic_signal[index][0] * 0.7
            index += 1
        elif index >= len(systolic_signal):
            break

    #Extarcts the values of dyastolic
    dyastolic = np.zeros(len(signalOG))
    index = 0
    for x in range(len(signalOG)):
        if index < len(dyastolic_signal) and signalOG[x][1] == dyastolic_signal[index][1]:
            dyastolic[x] = dyastolic_signal[index][0] * 0.7
            index += 1
        elif index >= len(dyastolic_signal):
            break
    
    plt.figure(figsize=(10, 6))

    # Plot original signal
    plt.subplot(1, 1, 1)
    plt.plot(timeOG, amplitudeOG, label='Original Signal')
    plt.plot(timeOG, systolic, label='systolic', color='red')
    plt.plot(timeOG, dyastolic, label='dyastolic', color='blue')
    plt.title('Original Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.show()

#Plots the old, new signal, sff and onsets
def showGraphs(signalOG, sampeling_interval):
    #Gets all of the signal values
    sampling_frequency = 1.0 / sampeling_interval
    signal_filtered = lowPass(16, sampling_frequency, 2, signalOG)
    ssf = SlopeSum(32, signal_filtered)
    time = (signalOG[len(signalOG)-1][1])/5
    onsets = decision_rule(time, ssf)

    #Extract the values of the orgiginal signal
    timeOG= [None] * len(signalOG)
    amplitudeOG = [None] * len(signalOG)

    for x in range(len(signalOG)):
        timeOG[x] = signalOG[x][1]
        amplitudeOG[x] = signalOG[x][0]

    #Extract the values of the filtered signal
    timeNew= [None] * len(signal_filtered)
    amplitudeNew = [None] * len(signal_filtered)

    for x in range(len(signal_filtered)):
        timeNew[x] = signal_filtered[x][1]
        amplitudeNew[x] = signal_filtered[x][0]

    #Extract the values of the ssf signal
    timeSSF= [None] * len(ssf)
    amplitudeSSF = [None] * len(ssf)

    for x in range(len(ssf)):
        timeSSF[x] = ssf[x][1]
        amplitudeSSF[x] = ssf[x][0]

    #Extract the values of the onsets of beats
    new_onsets = np.zeros(len(signal_filtered))
    index = 0
    for x in range(len(signal_filtered)):
        if index < len(onsets) and signal_filtered[x][1] == onsets[index]:
            new_onsets[x] = 1
            index += 1
        elif index >= len(onsets):
            break

    plt.figure(figsize=(10, 6))

    # Plot original signal
    plt.subplot(4, 1, 1)
    plt.plot(timeOG, amplitudeOG, label='Original Signal')
    plt.title('Original Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    # Plot filtered signal
    plt.subplot(4, 1, 2)
    plt.plot(timeNew, amplitudeNew, label='new Signal', color='orange')
    plt.title('Filtered Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    # Plot ssf
    plt.subplot(4, 1, 3)
    plt.plot(timeSSF, amplitudeSSF, label='ssf', color='green')
    plt.title('ssf signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    # Plot onsets
    plt.subplot(4, 1, 4)
    plt.plot(timeNew, new_onsets, label='onsets', color='red')
    plt.title('Onsets of beats')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.show()

    #Plots the old, new signal, sff and onsets
def showSSF(signalOG, sampeling_interval):
    #Gets all of the signal values
    sampling_frequency = 1.0 / sampeling_interval
    signal_filtered = lowPass(16, sampling_frequency, 2, signalOG)
    ssf = SlopeSum(32, signal_filtered)
    time = (signalOG[len(signalOG)-1][1])/5

    #Extract the values of the orgiginal signal
    timeOG= [None] * len(signalOG)
    amplitudeOG = [None] * len(signalOG)

    for x in range(len(signalOG)):
        timeOG[x] = signalOG[x][1]
        amplitudeOG[x] = signalOG[x][0]

    #Extract the values of the filtered signal
    timeNew= [None] * len(signal_filtered)
    amplitudeNew = [None] * len(signal_filtered)

    for x in range(len(signal_filtered)):
        timeNew[x] = signal_filtered[x][1]
        amplitudeNew[x] = signal_filtered[x][0]

    #Extract the values of the ssf signal
    timeSSF= [None] * len(ssf)
    amplitudeSSF = [None] * len(ssf)

    for x in range(len(ssf)):
        timeSSF[x] = ssf[x][1]
        amplitudeSSF[x] = ssf[x][0]

    plt.figure(figsize=(10, 6))

    # Plot original signal
    plt.subplot(3, 1, 1)
    plt.plot(timeOG, amplitudeOG, label='Original Signal')
    plt.title('Original Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    # Plot filtered signal
    plt.subplot(3, 1, 2)
    plt.plot(timeNew, amplitudeNew, label='new Signal', color='orange')
    plt.title('Filtered Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    # Plot ssf
    plt.subplot(3, 1, 3)
    plt.plot(timeSSF, amplitudeSSF, label='ssf', color='green')
    plt.title('ssf signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()


    plt.tight_layout()
    plt.show()
                
