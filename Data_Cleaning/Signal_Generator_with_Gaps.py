import numpy as np
import matplotlib.pyplot as plt
import random
<<<<<<<< HEAD:Data_Cleaning/Signal Generator with Gaps.py
========

>>>>>>>> 42412f600cd45f47f88645a25712e853c291655c:Data_Cleaning/Signal_Generator_with_Gaps.py

def generate_signal_with_gaps(period_values: list[float], no_of_periods: int, gap_percentage: float) -> list[float]:
    """
    This function takes values from one period (period_values) and replicates it N times (no_of_periods),
    introducing gaps in the signal. The percentage of the signal that should be gaps is specified by gap_percentage.
    It also generates mock timestamps.
    The output is a 2D array where the waveform values can be found in the first dimension (clean_signal[0])
    and the timestamps in the second dimension (clean_signal[1]).
    """

    # Generate the base signal
    signal = period_values * no_of_periods
    timestamps = np.arange(len(signal)) / 100  # arbitrary values

    # Calculate the number of points to be replaced with gaps
    num_gaps = int(len(signal) * gap_percentage)

    # Randomly select points in the signal to be replaced with NaN
    gap_indices = random.sample(range(len(signal)), num_gaps)
    for idx in gap_indices:
        signal[idx] = np.nan

    clean_signal_with_gaps = np.vstack([signal, timestamps])  # stacks row-wise

    return clean_signal_with_gaps




