""" This is the package responsible for realizing the preprocessment of
photoplethysmogram signals. """

import scipy as sp

def preprocess(signal):
    preprocessed_signal = _remove_high_frequency_components(signal)
    preprocessed_signal = _remove_baseline_wander(signal)
    preprocessed_signal = _upsample(signal)

    return preprocessed_signal


def _remove_high_frequency_components(signal):
    sampling_freq = 125
    filter_order = 5
    max_ripple = 0.5
    cut_off_freq_hz = 10
    cut_off_freq_rad_smp = (2 * cut_off_freq)/sampling_freq

    cheby_num, cheby_den = sp.signal.cheby1(filter_order, max_ripple, cut_off_freq_rad_smp, btype='lowpass')
    low_pass_filtered_signal = sp.signal.filtfilt(cheby_num, cheby_den, signal)

    return low_pass_filtered_signal


def _remove_baseline_wander(signal):
    signal_length = len(signal)
    first_window_size = np.floor(0.7 * signal_length)
    second_window_size = np.floor(0.3 * signal_length)

    first_window_output = sp.signal.medfilt(signal, first_window_size)
    second_window_output = sp.signal.medfilt(first_window_output, second_window_size)

    return second_window_output


def _upsample(signal):
    signal_length = len(signal)
    curr_sampling_freq = 125
    desired_sampling_freq = 500

    desired_n_of_samples = (desired_sampling_freq * signal_length) / (curr_sampling_freq)
    upsampled_signal = sp.signal.resample(signal, desired_n_of_samples)

    return upsampled_signal