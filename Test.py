from data import main as data
from Data_Cleaning import Segmentation_and_interpolation #I needed to change the file name as having spaces in filenames made it harder to work with
from Filters import FilterLow
from evaluation import snr
#from evaluation import ml
from noise import artifacts
import matplotlib.pyplot as plt

import vitaldb

# --------------------
# Global
track_names = ['CardioQ/ABP']  # Track name of interest --> CardioQ/ABP
caseids = vitaldb.find_cases(track_names)  # specific caseids of above tracks

# --------------------

#I noticed when I was trying to use vitalcb that I got a ssl error.
#This was fixed by getting the cirtifi function and adding vitaldbs
#certification manually

#Here is the test function
def main():
    #Get the waveform from vitaldb
    signal = data.get_waveform(
        caseids[1], track_names[0], timestamp=True, dropna=True, interval=1/100)
    
    data.plot(signal)

    # Separate the timestamps and signal values
    timestamps = [item[1] for item in signal]
    signal_values = [item[0] for item in signal]

    # Add artificial noise to the signal
    signal_noisy = artifacts.add_random_noise(signal_values, 10)
    zipped_noise_time = [list(item) for item in zip(signal_noisy, timestamps)]

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, signal_noisy)
    plt.title('Random Noise Artifact')
    plt.xlabel('Time')
    plt.ylabel('Signal Value')
    plt.show()

    processed_segments = Segmentation_and_interpolation.segment_and_interpolate(data.get_waveform(
        caseids[1], track_names[0], timestamp=False, dropna=False, interval=1/100), timestamps, 50, 5)

    # Plot the results
    plt.figure(figsize=(12, 6))
    for segment_signal, segment_timestamps in processed_segments:
        plt.plot(segment_timestamps, segment_signal)

    plt.xlabel('Time')
    plt.ylabel('Signal Value')
    plt.title('Segmented and Interpolated Signal')
    plt.show()

    # Test filter with noisy signal
    _, filtered_noisy_signal = FilterLow.main(zipped_noise_time)
    timestamps_noisy_filtered = [item[1] for item in filtered_noisy_signal]
    signal_values_noise_filtered = [item[0] for item in filtered_noisy_signal]

    # Test filter with raw singal
    _, filtered_signal = FilterLow.main(signal)
    timestamps_filtered = [item[1] for item in filtered_signal]
    signal_values_filtered = [item[0] for item in filtered_signal]

    # # Plot the original and filtered signals
    # plt.figure(figsize=(15, 6))

    # # Plot original signal
    # plt.subplot(1, 2, 1)
    # plt.plot(timestamps, signal_noisy)
    # plt.title('Original Signal')
    # plt.xlabel('Time')
    # plt.ylabel('Signal Value')

    # # Plot filtered signal
    # plt.subplot(1, 2, 2)
    # plt.plot(timestamps_noisy_filtered, signal_values_noise_filtered)
    # plt.title('Filtered Signal')
    # plt.xlabel('Time')
    # plt.ylabel('Signal Value')

    # plt.tight_layout()
    # plt.show()
    
    #Try to filter the signal (buggy)
    #filtered = Filter.main(signal)

    filename = "results.txt"
    snr.snrMain(signal_values, signal_values_filtered, filename)

    directory = 'C:\\Users\\axelm\\Documents\\1. School - KTH\\Year 1\\S1 P1&2\\CM2015 Project Carrier Course for Medical Engineers\\Project\\VSCode Workspace\\HealthSyS\\machineLearning\\'
    modelName = "lee_model_matched.hdf5"


    ml.mlMain(directory, modelName, signal_values, signal_values_filtered, 2500)
    # ml.mlMain(directory, modelName, signal_noisy, signal_values_filtered, 2500)

main()