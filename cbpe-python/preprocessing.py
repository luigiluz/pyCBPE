""" This is the package responsible for realizing the preprocessment of
photoplethysmogram signals. """

import numpy as np
from scipy import signal
import constants as consts


def preprocess(signal):
    preprocessed_signal = _remove_high_frequency_components(signal)
    preprocessed_signal = _remove_baseline_wander(preprocessed_signal)
    preprocessed_signal = _upsample(preprocessed_signal)

    return preprocessed_signal


def _remove_high_frequency_components(ppg_signal):
    filter_order = 5
    max_ripple = 0.5
    cut_off_freq_hz = 10
    cut_off_freq_rad_smp = (2 * cut_off_freq_hz) / consts.SAMPLING_FREQ
    low_pass_filtered_signal = np.zeros(len(ppg_signal))

    cheby_num, cheby_den = signal.cheby1(filter_order, max_ripple, cut_off_freq_rad_smp, btype='lowpass')
    low_pass_filtered_signal = signal.filtfilt(cheby_num, cheby_den, ppg_signal)

    return low_pass_filtered_signal


def _remove_baseline_wander(ppg_signal):
    signal_length = len(ppg_signal)
    first_window_size = int(np.floor(0.7 * signal_length))
    second_window_size = int(np.floor(0.3 * signal_length))

    mov_median_output = np.zeros(signal_length)
    detrended_signal = np.zeros(signal_length)

    # todo: make sure that window sizes are odd
    mov_median_output = signal.medfilt(ppg_signal, first_window_size)
    mov_median_output = signal.medfilt(mov_median_output, second_window_size)

    detrended_signal = np.subtract(ppg_signal, mov_median_output)

    return detrended_signal


def _upsample(ppg_signal):
    signal_length = len(ppg_signal)
    desired_sampling_freq = 4 * consts.SAMPLING_FREQ

    desired_n_of_samples = int((desired_sampling_freq * signal_length) / (consts.SAMPLING_FREQ))
    upsampled_signal = np.zeros(desired_n_of_samples)
    upsampled_signal = signal.resample(ppg_signal, desired_n_of_samples)

    return upsampled_signal