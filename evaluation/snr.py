# External Modules
import os
import sys
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

#-------------------

"""
This is a collection of functions to evaluate the performance of a digital filter on a waveform.
Signal-to-noise ratio (SNR) is the main performance metric.
Additionally, a plot is created to visualize the filter impact on the waveform.
The result of the evaluation can be saved to a text file.

To perform evaluation, call snrMain with the given parameters.
snrCalc, snrPrint and snrPlot can also be called directly to customize evaluation further.

Inspired by the excellent work of Patrik Lechner, which is licensed
under Creative Commons, Attribution-ShareAlike 4.0 International.
Source: https://github.com/hrtlacek/SNR/tree/main
"""

#-------------------

def snrCalc(original_signal: list[float], filtered_signal: list[float]) -> float:
    """Calculates the signal-to-noise ratio (SNR).

    Args:
        original_signal: The original, unfiltered waveform values.
        filtered_signal: The filtered waveform values.

    Examples:
        >>> array1 = [...]
        >>> array2 = [...]
        >>> snr_value_db = snrCalc(array1, array2)
        >>> print(snr_db)
        20.01
    """
    noise = filtered_signal - original_signal
    power_noise = np.average(noise**2)
    power_filtered = np.average(filtered_signal**2)
    snr_db = 10*np.log10((power_filtered - power_noise) / power_noise)
    
    return snr_db

#-------------------

def snrPrint(snr_value: float, filename: str = None) -> None:
    """Creates a "pretty-print" of the calculated signal-to-noise ratio (SNR).
    Will always output to terminal but can also be saved to a text file if a filename is provided.
    If a filename is provided, the file will be created (if does not already exist) and output will be appeneded at the end.

    Args:
        snr_value: The calculated SNR value.
        filename: Name of the text file to save the evaluation in. If no filename is provided, only terminal output will be given. Default None.

    Examples:
        >>> array1 = [...]
        >>> array2 = [...]
        >>> snr_value_db = snrCalc(array1, array2)
        >>> filename = "results.txt"
        >>> snrPrint(snr_value_db, filename)
        Timestamp: 2024-01-08 17:29:46.889352
        -------------------------EVALUATION-------------------------
        The Signal-to-noise ratio was found to be 21.09 dB.
        A ratio greater than 0 dB indicates more signal than noise.
        ------------------------------------------------------------
    """

    if filename:
        with open(os.path.join("evaluation", filename),'a') as f:
            for out in [sys.stdout, f]:
                print("\nTimestamp:", dt.datetime.now(), file=out)
                print("\n" + "-" * 25 + "EVALUATION" + "-" * 25, file=out)
                print("The Signal-to-noise ratio was found to be {0:.2f} dB.".format(snr_value), file=out)
                print("A ratio greater than 0 dB indicates more signal than noise.", file=out)
                print("-" * 60 + "\n", file=out)
    else:
        print("No filename selected, terminal output only.")
        print("\nTimestamp:", dt.datetime.now())
        print("\n" + "-" * 25 + "EVALUATION" + "-" * 25)
        print("The Signal-to-noise ratio was found to be {0:.2f} dB.".format(snr_value))
        print("A ratio greater than 0 dB indicates more signal than noise.")
        print("-" * 60 + "\n")
    
    return

#-------------------

def snrPlot(orignal_signal: list[float], filtered_signal: list[float], snr_value: float) -> None:
    """Creates graphical plots for filter evaluation.

    Args:
        original_signal: The original, unfiltered waveform values.
        filtered_signal: The filtered waveform values.
        snr_value: The calculated SNR value.

    Examples:
        >>> array1 = [...]
        >>> array2 = [...]
        >>> snr_value_db = snrCalc(array1, array2)
        >>> snrPlot(array1, array2, snr_value_db)
    """
    
    figure(figsize=(12, 6), dpi=100)
    plt.plot(orignal_signal, color="lightblue", label="Raw")
    plt.plot(filtered_signal, color="orange", label="Filter (SNR=%1.2fdB)" % snr_value)
    plt.legend()
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.title("Evaluation: Filter Performance")
    plt.show()

    return

#-------------------

def snrMain(original_signal: list[float], filtered_signal: list[float], filename: str = None) -> None:
    """Calls other module functions to perform filter performance evaluation.

    Args:
        original_signal: The original, unfiltered waveform values.
        filtered_signal: The filtered waveform values.
        filename: Name of the text file to save the evaluation in. If no filename is provided, only terminal output will be given. Default None.

    Examples:
        >>> from snr import *
        >>> original_signal = [...]
        >>> filtered_signal = [...]
        >>> filename = "results.txt"
        >>> snrMain(original_signal, filtered_signal, filename)
        Timestamp: 2024-01-08 17:29:46.889352
        -------------------------EVALUATION-------------------------
        The Signal-to-noise ratio was found to be 21.09 dB.
        A ratio greater than 0 dB indicates more signal than noise.
        ------------------------------------------------------------      
    """

    filtered_signal = np.array(filtered_signal)
    original_signal = np.array(original_signal)

    snr_value = snrCalc(original_signal, filtered_signal)
    snrPrint(snr_value, filename)
    snrPlot(original_signal, filtered_signal, snr_value)

    return