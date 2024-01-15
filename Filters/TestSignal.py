import matplotlib .pyplot as plt
import numpy as np
import os
import csv

def sinusSignal():
    #Create the parameters for the signal
    time = np.arange(0, 40, 0.004)
    amplitude = np.sin(time)

    Pure_signal = [[None, None]] * len(time)

    for x in range(len(time)):
        Pure_signal[x] = [amplitude[x], time[x]]

    return Pure_signal

def noisyRandomSignal():
    #Create the parameters for the signal
    time = np.arange(0, 40, 0.004)
    noise = np.random.normal(0,1,10000)
    amplitude = np.sin(time)

    #Create the noisy signal
    noisy = amplitude + noise

    noisy_signal = [[None, None]] * len(time)

    for x in range(len(time)):
        noisy_signal[x] = [noisy[x], time[x]]

    return noisy_signal

def noisyFrequencyignal(Frequency):
    #Create the parameters for the signal
    time = np.arange(0, 40, 0.004)
    noise = 0.2*np.cos(2*np.pi*Frequency*time)
    amplitude = np.sin(time)

    #Create the noisy signal
    noisy = amplitude + noise

    noisy_signal = [[None, None]] * len(time)

    for x in range(len(time)):
        noisy_signal[x] = [noisy[x], time[x]]

    return noisy_signal

#Read the contents of a csv file from mimic database to find teh abp
#values. The reading wants the data to be per sample.
#The input is the name of the csv file and path. The second
#input is the length in seconds that you want to extract.
#The output is three values a array of sample number, a array
#of values in same order as the time and lastly the sampling
#frequency.
def readCSVABP(fileName, timeLength):
    time = []
    sample = []
    row_lentgh = 0
    ABP_index = 2
    rows_processed = 0
    sample_interval_string = ""
    sample_interval = 0
    rowsMax = None

    try:
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                #Do read first and get properties
                if rows_processed == 0:
                    rows_processed += 1
                    row_lentgh = len(row)
                    #Save where ABP values are
                    for x in range(len(row)):
                        if row[x] == "'ABP'":
                            ABP_index = x
                    continue
                #Save sample time
                elif rows_processed == 1:
                    sample_interval_string = row[0]
                    #Gets the sample rate of the signal
                    sample_interval = float(sample_interval_string.split()[0].replace("'", ""))
                    rows_processed += 1
                    if timeLength != None:
                        rowsMax = timeLength / sample_interval
                    continue
                #read only max number of samples
                elif rowsMax != None and rows_processed - 2 == rowsMax:
                    break

                if len(row) >= row_lentgh:  # Ensure the row has all values
                    time.append(row[0])  # First column values
                    sample.append(float(row[ABP_index]))  # Fourth column values
                    rows_processed += 1
                else:
                    print(f"Skipping row: {row} as it doesn't have enough columns")
                    rows_processed += 1
    #If the file can't be found
    except FileNotFoundError:
        print(f"File '{fileName}' not found")

    return time, sample, sample_interval

#This function converts to arrays to a signle array with a given interval
#between timestamps.
#The input is the time array [] which is the sample numbers but can be time if
#the sample_interval is set to 1. The second parameter is the array [] of 
#values for each sample and the last parameter is the sample interval or the
#time between each sample
#The ouput is a two dimensional array in the order of [[value, time]] with the
#time staring at 0. The last element in the array is the time_interval between 
#samples
def convertSignal(time, sample, sample_interval):
    newtime = [None] * len(time)
    for x in range(len(newtime)):
        newtime[x] = x * sample_interval

    #Converts two arrays to a signle array
    total_array = [[x, y] for x, y in zip(sample, newtime)]
    total_array.append(sample_interval)

    return total_array

#This function creates a ABP signal from the csv file specified of a certain
#length.
#The first paremeter is the length of the signal in seconds and the second
#parameter is the csv file from mimic with the values.
#The ouput is a ABP signal in array form with the value [[value, time]] and
#the last element in the list is the time between samples
def ABPTestSignal(timeLength, file_name):
    timeValues, values, sample_interval = readCSVABP(file_name, timeLength)

    TestSignal = convertSignal(timeValues, values, sample_interval)

    return TestSignal

#This function plots the signal to visulise the signal.
#The input is the signal in the format of [[value, time]]
def ABPprintSignal(TestSignal):    
    #Get the seperate values of the array 
    array1, array2 = zip(*TestSignal)

    #Creates the lists
    samples = list(array1)
    newtime = list(array2)

    #Plot everything
    plt.figure(figsize=(8, 6))
    plt.plot(newtime, samples)
    plt.xlabel('time')
    plt.ylabel('ABP')
    plt.title('Example signal')
    plt.show()

#This function creates a noisy ABP signal from the csv file specified of a certain
#length.
#The first paremeter is the nois frewuency, the second paramteer is the 
# amplitude of noise, the third parameter is the length of the signal in seconds 
# and the fourth parameter is the csv file from mimic with the values.
#The ouput is a ABP signal in array form with the value [[value, time]]
def noisyABPSignal(Frequency, amplitude, time_length, File_name):
    #Create the parameters for the signal
    timeValues, values, sample_interval = readCSVABP(File_name, time_length)
    new_time = np.arange(0, time_length, sample_interval)

    noise = amplitude*np.cos(2*np.pi*Frequency*new_time)

    #Create the noisy signal
    noisy = values + noise

    #Converts two arrays to a signle array
    noisy_signal = [[x, y] for x, y in zip(noisy, new_time)]

    return noisy_signal

#This function adds noise to a signal in the format of [[value, time]]
#The first paremeter is the nois frequency, the second paramteer is the 
# amplitude of noise, the third parameter is the signal in the format 
# of [[value, time]] 
#The ouput is a the signal with noise in array form with the value [[value, time]]
def Addnoise(Frequency, amplitude, signal,):
    #Seperate signal
    array1, array2 = zip(*signal)

    #Creates the lists
    values = list(array1)
    time = list(array2)

    sample_interval = time[1] - time[0]
    new_time = np.arange(0, len(time) * sample_interval, sample_interval)

    noise = amplitude*np.cos(2*np.pi*Frequency*new_time)

    #Create the noisy signal
    noisy = values + noise

    #Converts two arrays to a signle array
    noisy_signal = [[x, y] for x, y in zip(noisy, new_time)]

    return noisy_signal