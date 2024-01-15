import numpy as np
import matplotlib.pyplot as plt


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


<<<<<<<< HEAD:Data_Cleaning/Validating with visualisation and plotting.py
i
# processed_segments now contains tuples of (interpolated_segment_signal, segment_timestamps)
#plotting and visualization
========
>>>>>>>> 42412f600cd45f47f88645a25712e853c291655c:Data_Cleaning/Validating_with_visualisation_and_plotting.py

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
<<<<<<<< HEAD:Data_Cleaning/Validating with visualisation and plotting.py






========
>>>>>>>> 42412f600cd45f47f88645a25712e853c291655c:Data_Cleaning/Validating_with_visualisation_and_plotting.py
