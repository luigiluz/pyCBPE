""" This is the package responsible for realizing the ppg pulse normalization.
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pyampd.ampd import find_peaks


def normalize(signal):
    minimals = _detect_minimals(signal)
    central_pulse = _get_central_pulse(signal, minimals)
    normalized_pulse = _normalize_pulse(central_pulse)

    return normalized_pulse


def _detect_minimals(signal):
    minimals = find_peaks(-signal)

    return minimals


def _get_central_pulse(signal, minimals):
    n_of_minimals = len(minimals)
    central_minimal = int(np.floor(n_of_minimals / 2))
    minimal_after_central = central_minimal + 1

    central_pulse = signal[minimals[central_minimal] : minimals[minimal_after_central]]

    return central_pulse


def _normalize_pulse(pulse_signal):
    peaks = find_peaks(pulse_signal)
    systolic_peak = peaks[0]

    ascending_section = pulse_signal[0:systolic_peak].reshape(-1, 1)
    descending_section = pulse_signal[systolic_peak:-1].reshape(-1, 1)

    scaler = MinMaxScaler()

    scaler.fit(ascending_section)
    norm_ascending_section = scaler.transform(ascending_section)

    scaler.fit(descending_section)
    norm_descending_section = scaler.transform(descending_section)

    # TO DO: Verify if this is returning the expecteed behavior
    norm_pulse = np.concatenate((norm_ascending_section, norm_descending_section[1:-1]))

    return norm_pulse