""" This is the package responsible for realizing the ppg pulse normalization.
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pyampd.ampd import find_peaks
import pyCBPE.constants as consts


def normalize(signal):
    minimals = _detect_minimals(signal)
    central_pulse = _get_central_pulse(signal, minimals)
    is_central_pulse_empty = central_pulse.size == 0
    if is_central_pulse_empty:
        normalized_pulse = np.array([])
        return normalized_pulse

    normalized_pulse = _normalize_pulse(central_pulse)
    is_normalized_pulse_empty = normalized_pulse.size == 0
    if is_normalized_pulse_empty:
        normalized_pulse = np.array([])
        return normalized_pulse

    return normalized_pulse


def _detect_minimals(signal):
    minimals = find_peaks(-signal)

    return minimals


def _get_central_pulse(signal, minimals):
    n_of_minimals = len(minimals)
    if n_of_minimals < 2:
        central_pulse = np.array([])
        return central_pulse

    central_minimal = int(np.floor(n_of_minimals / 2))
    if n_of_minimals == 2:
        central_minimal = 0

    minimal_after_central = central_minimal + 1

    central_pulse = signal[minimals[central_minimal] : minimals[minimal_after_central]]

    return central_pulse


def _normalize_pulse(pulse_signal):
    peaks = find_peaks(pulse_signal)
    systolic_peak = peaks[0]

    ascending_section = pulse_signal[0:systolic_peak]
    if len(ascending_section) < consts.ASCENDING_POL_N_OF_COEFS:
        normalized_pulse = np.array([])
        return normalized_pulse

    descending_section = pulse_signal[systolic_peak:-1]
    if len(descending_section) < consts.DESCENDING_POL_N_OF_COEFS:
        normalized_pulse = np.array([])
        return normalized_pulse

    ascending_section = ascending_section.reshape(-1, 1)
    descending_section = descending_section.reshape(-1, 1)

    scaler = MinMaxScaler()

    scaler.fit(ascending_section)
    norm_ascending_section = scaler.transform(ascending_section)

    scaler.fit(descending_section)
    norm_descending_section = scaler.transform(descending_section)

    # TO DO: Verify if this is returning the expecteed behavior
    norm_pulse = np.concatenate((norm_ascending_section, norm_descending_section[1:-1]))
    normalized_pulse = norm_pulse[:, 0]

    return normalized_pulse
