# --------------------
# External modules
from enum import Enum
import vitaldb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------
# Global
track_names = ['CardioQ/ABP']  # Track name of interest --> CardioQ/ABP
caseids = vitaldb.find_cases(track_names)  # specific caseids of above tracks


# --------------------


"""
Use of vitalDB requires instalation of the vitaldb package. To download this, run the following python terminal command:

python -m pip install vitaldb
"""

class WaveformType(Enum):
    LIST = 1
    LIST_LISTS = 2


def main():
    """
    Run Program
    """

    # Plot all waveforms for trackname
    # plot_all()

    # Get specific waveform from caseID
    waveform = get_waveform(
        caseids[9], track_names[0], timestamp=True, dropna=False, interval=1/100)

    
    # plot specific waveform
    plot(waveform)


def plot_all(caseids: list[int] = caseids, track_name: str = ['CardioQ/ABP'], interval: float = None, dropna: bool = False):
    """
    Plot waveforms for all caseids of specificed tracks.

    caseids: array -> case id's of open dataset
    track_name: str -> specific track name you want to use. (for our purposes, 'CardioQ/ABP')
    interval: float -> waveform resolution. if None, maximum resolution. if no resolution, 1/500 
    dropna: bool -> plot with na values or  not. (suggestion: dropna = False)
    """

    for caseid in caseids:
        # Case
        vf = vitaldb.VitalFile(caseid, track_name)

        # Save as df
        samples = vf.to_pandas(
            track_name, interval=interval, return_timestamp=True)

        if dropna:
            samples.dropna(inplace=True)

        # plot
        plot = samples.plot(x='Time', y=track_name)
        plt.show()

"""
NOTE: This plot will no longer work correctly for GUI as it was changed for demonstration purposes in test.py

TODO: Reverse X and Y assignment in line: y_values, x_values = zip(*waveform)

"""
def plot(waveform: list):
    """
    Plot a specific waveform

    waveform: list -> A waveform. Either 1D or 2D (list or list[tuple]). If 1D, list of data: [data]. if 2D, list of tuple time & data: [(time, data)]
    """

    waveform_type = None

    if isinstance(waveform, list) and all(isinstance(item, list) and len(item) ==  2 for item in waveform):
        waveform_type = WaveformType.LIST_LISTS
    elif isinstance(waveform, list):
        waveform_type = WaveformType.LIST
    else:
        raise Exception(
            "Waveform must be either a list or a list of tuples to plot.")

    match waveform_type:
        case WaveformType.LIST_LISTS:
            y_values, x_values = zip(*waveform)
            plt.plot(x_values, y_values)
        case WaveformType.LIST:
            plt.plot(waveform)

    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Waveform')
    plt.show()



def get_waveform(caseid: int, track_name: str, interval: float = None, timestamp: bool = True, trim: bool = True, dropna=False) -> list | list[list]:
    """
    Pulls a waveform from VitalDB

    caseid: int -> specific waveform you want to pull. (see caseids for options)
    track_name: str -> specific track name you want to use. (for our purposes, 'CardioQ/ABP')
    interval: float -> waveform resolution. if None, maximum resolution. if no resolution, 1/500 
    timestamp: bool -> return array with timestamps or not.
    trim: bool -> trim nan values off just the ends of the dataframe or not. (suggestion: trim = True)
    dropna: bool -> (suggestion: dropna = False. Use trim instead)
    """

    # Case file
    vf = vitaldb.VitalFile(caseid, track_name)

    # Save as df
    samples = vf.to_pandas(track_name, interval, return_timestamp=timestamp)

    if dropna:
        samples.dropna(inplace=True)

    if trim:
        samples = samples.loc[samples.first_valid_index():samples.last_valid_index()]

    if timestamp:
        data = samples[track_name]
        time = samples['Time']
        return ([list(item) for item in zip(data, time)])
    else:
        data = samples[track_name]
        return (data.to_list())