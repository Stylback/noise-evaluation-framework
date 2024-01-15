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
# processed_segments = segment_and_interpolate(Signal_VitalDB[0], Signal_VitalDB[1], gap_threshold=50, interpolation_limit=5)


# processed_segments now contains tuples of (interpolated_segment_signal, segment_timestamps)





