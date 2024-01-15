import numpy as np
import matplotlib.pyplot as plt
import random

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


period = [1.070, 1.070, 1.073, 1.077, 1.077, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.076, 1.078,
          1.082, 1.085, 1.087, 1.089, 1.091, 1.095, 1.099, 1.103, 1.107, 1.109, 1.109, 1.111, 1.118, 1.133, 1.162,
          1.215, 1.296, 1.409, 1.547, 1.709, 1.882, 2.056, 2.220, 2.367, 2.478, 2.564, 2.644, 2.713, 2.768, 2.812,
          2.847, 2.873, 2.893, 2.908, 2.918, 2.925, 2.928, 2.923, 2.912, 2.903, 2.893, 2.881, 2.863, 2.841, 2.813,
          2.782, 2.747, 2.706, 2.660, 2.613, 2.562, 2.503, 2.435, 2.358, 2.275, 2.188, 2.101, 2.016, 1.935, 1.861,
          1.798, 1.743, 1.701, 1.669, 1.638, 1.610, 1.585, 1.561, 1.538, 1.515, 1.494, 1.473, 1.453, 1.431, 1.413,
          1.396, 1.377, 1.359, 1.339, 1.320, 1.300, 1.282, 1.265, 1.249, 1.234, 1.219, 1.206, 1.196, 1.189, 1.178,
          1.167, 1.156, 1.147, 1.137, 1.129, 1.123, 1.117, 1.112, 1.108, 1.106, 1.106, 1.103, 1.100, 1.096, 1.091,
          1.087, 1.084, 1.082, 1.081, 1.081]



SWG = generate_signal_with_gaps(period,3,0.10)

#plotting and visualization

# Splitting the signal and timestamps
signal, timestamps= SWG

# Creating the plot
plt.figure(figsize=(50, 4))
plt.plot(timestamps, signal, label='Signal with Gaps')
plt.xlabel('Time')
plt.ylabel('Signal Value')
plt.title('Signal Visualization')
plt.legend()
plt.show()


import numpy as np
from scipy.interpolate import interp1d

def segment_and_interpolate(signal, timestamps, gap_threshold, interpolation_limit):


    """
    Segments the data based on gap length and interpolates small gaps within each segment.

    parameter signal: The signal array with potential NaN gaps.
    parameter timestamps: The corresponding timestamps for the signal.
    parameter gap_threshold: The threshold for gap length to trigger a new segment.
    parameter interpolation_limit: The maximum number of consecutive NaNs to interpolate.
    :return: A list of processed segments, each being a tuple of (segment_signal, segment_timestamps).
    """

      

    def interpolate_segment(segment_signal, segment_timestamps):
        """ Interpolates small gaps in a signal segment. """
        isnan = np.isnan(segment_signal)
        gap_starts = np.where(np.logical_and(~isnan[:-1], isnan[1:]))[0] + 1
        gap_ends = np.where(np.logical_and(isnan[:-1], ~isnan[1:]))[0] + 1

        for start, end in zip(gap_starts, gap_ends):
            if end - start <= interpolation_limit:
                interp_func = interp1d([segment_timestamps[start - 1], segment_timestamps[end]],
                                       [segment_signal[start - 1], segment_signal[end]],
                                       kind='linear')
                segment_signal[start:end] = interp_func(segment_timestamps[start:end])

        return segment_signal

    processed_segments = []
    current_segment_signal = []
    current_segment_timestamps = []

    for value, time in zip(signal, timestamps):
        if np.isnan(value):
            if len(current_segment_signal) >= gap_threshold:
                interpolated_segment = interpolate_segment(np.array(current_segment_signal), np.array(current_segment_timestamps))
                processed_segments.append((interpolated_segment, np.array(current_segment_timestamps)))
                current_segment_signal = []
                current_segment_timestamps = []
        else:
            current_segment_signal.append(value)
            current_segment_timestamps.append(time)

    if current_segment_signal:
        interpolated_segment = interpolate_segment(np.array(current_segment_signal), np.array(current_segment_timestamps))
        processed_segments.append((interpolated_segment, np.array(current_segment_timestamps)))

    return processed_segments

          
#Signal_VitalDB: The signal which is from Vital DB (Dataset)
processed_segments = segment_and_interpolate(SWG[0], SWG[1], gap_threshold=50, interpolation_limit=5)


# processed_segments now contains tuples of (interpolated_segment_signal, segment_timestamps)
#plotting and visualization


# Plotting and visualization after segmentation and interpolation

plt.figure(figsize=(50, 4))

# Iterate over each processed segment and plot
for i, (segment_signal, segment_timestamps) in enumerate(processed_segments):
    plt.plot(segment_timestamps, segment_signal, label=f'Segment {i+1}')

plt.xlabel('Time')
plt.ylabel('Signal Value')
plt.title('Signal Visualization After Segmentation and Interpolation')
plt.legend()
plt.show()






