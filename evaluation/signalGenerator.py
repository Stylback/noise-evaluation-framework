# External Modules
import numpy as np

#-------------------

"""
A module to create mock waveform values for testing purposes.
If you do not already have values for a single period, use this mock ABP signal:

period = [1.070, 1.070, 1.073, 1.077, 1.077, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.078,
          1.082, 1.085, 1.087, 1.089, 1.091, 1.095, 1.099, 1.103, 1.107, 1.109, 1.109, 1.111, 1.118, 1.133, 1.162,
          1.215, 1.296, 1.409, 1.547, 1.709, 1.882, 2.056, 2.220, 2.367, 2.478, 2.564, 2.644, 2.713, 2.768, 2.812,
          2.847, 2.873, 2.893, 2.908, 2.918, 2.925, 2.928, 2.923, 2.912, 2.903, 2.893, 2.881, 2.863, 2.841, 2.813,
          2.782, 2.747, 2.706, 2.660, 2.613, 2.562, 2.503, 2.435, 2.358, 2.275, 2.188, 2.101, 2.016, 1.935, 1.861,
          1.798, 1.743, 1.701, 1.669, 1.638, 1.610, 1.585, 1.561, 1.538, 1.515, 1.494, 1.473, 1.453, 1.431, 1.413,
          1.396, 1.377, 1.359, 1.339, 1.320, 1.300, 1.282, 1.265, 1.249, 1.234, 1.219, 1.206, 1.196, 1.189, 1.178,
          1.167, 1.156, 1.147, 1.137, 1.129, 1.123, 1.117, 1.112, 1.108, 1.106, 1.106, 1.103, 1.100, 1.096, 1.091,
          1.087, 1.084, 1.082, 1.081, 1.081]
"""

def generate_signal(period_values: list[float], no_of_periods: int) -> list[float]:
    """ This function take values from one period (period_values) and replicates it N times (no_of_periods).
    It also generates mock timestamps.
    The output is a 2D array where the waveform values can be found in the first dimension (clean_signal[0])
    and the timestamps in the second dimension (clean_signal[1]).

    Examples:
        >>> from signal_generator import *
        >>> period = [...]
        >>> clean_signal = generate_signal(period, 3)
    """

    signal = period_values * no_of_periods
    timestamps = np.arange(len(signal)) / 100 # arbitrary values
    clean_signal = np.vstack([signal, timestamps]) # stacks row-wise

    return clean_signal

#-------------------

def generate_noise_signal(period_values: list[float], no_of_periods: int, frequency: float) -> list[float]:
    """ This function take values from one period (period_values) and replicates it N times (no_of_periods).
    It then generates sinusodial noise which follows the original waveform.
    It also generates mock timestamps.
    The output is a 2D array where the noisy waveform values can be found in the first dimension (noise_signal[0])
    and the timestamps in the second dimension (noise_signal[1]).

    Examples:
        >>> from signal_generator import *
        >>> period = [...]
        >>> noisy_signal = generate_noise_signal(period, 3, 50)
    """

    signal = period_values * no_of_periods
    timestamps = np.arange(len(signal)) / 100 # arbitrary values
    
    signal_values = np.arange(len(signal)) / len(period_values)
    noise = 0.2 * np.cos(2 * np.pi * frequency * signal_values)
    noise += 0.1 * np.cos(2 * np.pi * (frequency/3) * signal_values)
    noise_signal = signal+noise
    
    noise_signal = np.vstack([noise_signal, timestamps]) # stacks row-wise

    return noise_signal