#-------------------
# Modules

import numpy as np

#-------------------

"""
Artifact Functions
"""

def add_random_noise(signal_values, noise_level):
    """ Adds random noise to a signal.

    signal_values (list or numpy array): The original signal values.
    noise_level (float): The standard deviation of the noise.

    Returns:The signal with added random noise.
    """
    chunk_size=1000

    # Convert signal_values to numpy array
    signal_values = np.array(signal_values)
    
    noisy_signal = np.empty_like(signal_values)

    for i in range(0, len(signal_values), chunk_size):
        chunk = signal_values[i:i+chunk_size]
        noise = np.random.normal(0, noise_level, size=chunk.shape)
        noisy_signal[i:i+chunk_size] = chunk + noise

    return noisy_signal

def add_noise_with_snr(signal, desired_snr_db):
    """ Adds Gaussian noise to a signal based on a desired Signal-to-Noise Ratio (SNR).

    signal (numpy array or list): The original signal.
    desired_snr_db (float): The desired SNR in decibels.
    """
    # Ensure signal is a numpy array
    signal = np.array(signal)

    # Convert desired SNR from dB to linear scale
    desired_snr = 10 ** (desired_snr_db / 10)

    # Calculate signal power and desired noise power
    signal_power = np.mean(signal ** 2)
    noise_power = signal_power / desired_snr

    # Generate noise with the desired power
    noise = np.sqrt(noise_power) * np.random.normal(size=signal.shape)

    # Add noise to the signal
    noisy_signal = signal + noise

    return noisy_signal

def modulate_amplitude(signal, modulation_factor):
    """ Modulates the amplitude of the signal.

    signal (numpy array or list): The original signal.
    modulation_factor (float): The factor by which to modulate the amplitude.
    """
    # Ensure signal is a numpy array
    signal = np.array(signal)

    # Modulate the signal values
    modulated_signal = signal * modulation_factor

    return modulated_signal

def add_motion_artifacts(signal, num_artifacts, artifact_strength):
    """ Adds simulated motion artifacts to the signal.

    signal (numpy array or list): The original signal.
    num_artifacts (int): Number of artifacts to add.
    artifact_strength (float): The strength of the artifacts.
    """
    # Ensure signal is a numpy array
    signal = np.array(signal)

    for _ in range(num_artifacts):
        artifact_index = np.random.randint(len(signal))
        signal[artifact_index] += np.random.uniform(-artifact_strength, artifact_strength)

    return signal