""" This is the package responsible for realizing the photoplethysmogram
pulse key points extraction. """

import numpy as np
import pyampd

# consider moving all of this to a constants.py
ASCENDING_POL_ORDER = 5
ASCENDING_POL_N_OF_COEFS = ASCENDING_POL_ORDER + 1
DESCENDING_POL_ORDER = 7
DESCENDING_POL_N_OF_COEFS = DESCENDING_POL_ORDER + 1

SYS_PEAK = "systolic peak"
MAX_SLP = "max slope"
DIAS_PEAK = "diastolic peak"
DIC_NOTCH = "dicrotic notch"
INFL_POINT = "inflection point"

ASC_POL = "ascending_pol"
DESC_POL = "descending_pol"
ASC_SEC_EVAL = "ascending_section_eval"
DESC_SEC_EVAL = "descending_section_eval"
PULSE_EVAL = "pulse_eval"


def extract(normalized_pulse):
    is_normalized_pulse_empty = normalized_pulse.size == 0
    if is_normalized_pulse_empty:
        key_points = {}
        return key_points

    # group all key points in this dictionary
    key_points = {
        SYS_PEAK: 0,
        MAX_SLP: 0,
        DIAS_PEAK: 0,
        DIC_NOTCH: 0,
        INFL_POINT: 0
    }

    key_points[SYS_PEAK] = _find_systolic_peak_location(normalized_pulse)
    if key_points[SYS_PEAK] == 0:
        key_points = {}
        return key_points

    regular_pulse, pulse_first_derivative, pulse_second_derivative = _fit_section_polynoms(normalized_pulse, key_points[SYS_PEAK])

    key_points[MAX_SLP] = _find_max_slope(pulse_first_derivative, key_points)
    if key_points[MAX_SLP] == 0:
        key_points = {}
        return key_points

    key_points[DIAS_PEAK] = _find_diastolic_peak(pulse_first_derivative, pulse_second_derivative, key_points)
    if key_points[DIAS_PEAK] == 0:
        key_points = {}
        return key_points

    key_points[DIC_NOTCH] = _find_dicrotic_notch(pulse_second_derivative, key_points)
    if key_points[DIC_NOTCH] == 0:
        key_points = {}
        return key_points

    key_points[INFL_POINT] = _find_inflection_poiint(pulse_second_derivative, key_points)
    if key_points[INFL_POINT] == 0:
        key_points = {}
        return key_points

    return key_points


def _find_systolic_peak_location(normalized_pulse):
    systolic_peak = 0

    peaks = pyampd.ampd.find_peaks(normalized_pulse)
    if len(peaks) == 0:
        return systolic_peak

    systolic_peak = peaks[0]

    return systolic_peak


def _fit_section_polynoms(normalized_pulse, systolic_peak):
    sampling_freq = 125
    pulse_length = len(normalized_pulse)
    pulse_time = np.arange(0, pulse_length / (4*sampling_freq), 1 / (4*sampling_freq))

    ascending_section, descending_section = _separate_pulse_in_sections(normalized_pulse, systolic_peak)

    ascending_len = len(ascending_section)
    descending_len = len(descending_section)

    # prealocation
    regular_pulse = {
        ASC_POL : np.zeros(ASCENDING_POL_N_OF_COEFS),
        DESC_POL : np.zeros(DESCENDING_POL_N_OF_COEFS),
        ASC_SEC_EVAL : np.zeros(ascending_len),
        DESC_SEC_EVAL : np.zeros(descending_len),
        PULSE_EVAL: np.zeros(ascending_len + descending_len)
    }

    pulse_first_derivative = {
        ASC_POL : np.zeros(ASCENDING_POL_N_OF_COEFS),
        DESC_POL : np.zeros(DESCENDING_POL_N_OF_COEFS),
        ASC_SEC_EVAL : np.zeros(ascending_len),
        DESC_SEC_EVAL : np.zeros(descending_len),
        PULSE_EVAL: np.zeros(ascending_len + descending_len)
    }

    pulse_second_derivative = {
        ASC_POL : np.zeros(ASCENDING_POL_N_OF_COEFS),
        DESC_POL : np.zeros(DESCENDING_POL_N_OF_COEFS),
        ASC_SEC_EVAL : np.zeros(ascending_len),
        DESC_SEC_EVAL : np.zeros(descending_len),
        PULSE_EVAL: np.zeros(ascending_len + descending_len)
    }

    ascending_time = pulse_time[0:systolic_peak]
    descending_time = pulse_time[systolic_peak + 1 : -1]

    ###### without derivative ######
    # fit sections polynoms
    regular_pulse[ASC_POL] = np.polyfit(ascending_time, ascending_section, deg=5)
    regular_pulse[DESC_POL] = np.polyfit(descending_time, descending_section, deg=7)
    # evaluate sections polynoms
    regular_pulse[ASC_SEC_EVAL] = np.polyval(regular_pulse[ASC_POL], ascending_time)
    regular_pulse[DESC_SEC_EVAL] = np.polyval(regular_pulse[DESC_POL], descending_time)
    # concatenate sections polynoms
    regular_pulse[PULSE_EVAL] = np.concatenate((regular_pulse[ASC_SEC_EVAL], regular_pulse[DESC_SEC_EVAL]))

    ###### first derivative ######
    # fit sections first derivatives polynoms
    pulse_first_derivative[ASC_POL] = np.polyder(regular_pulse[ASC_POL])
    pulse_first_derivative[DESC_POL] = np.polyder(regular_pulse[DESC_POL])
    # evaluate sections first derivatives polynoms
    pulse_first_derivative[ASC_SEC_EVAL] = np.polyval(pulse_first_derivative[ASC_POL], ascending_time)
    pulse_first_derivative[DESC_SEC_EVAL] = np.polyval(pulse_first_derivative[DESC_POL], descending_time)
    # concatenate first derivates sections polynoms
    pulse_first_derivative[PULSE_EVAL] = np.concatenate((pulse_first_derivative[ASC_SEC_EVAL], pulse_first_derivative[DESC_SEC_EVAL]))

    ###### second derivative ######
    # fit sections second derivatives polynoms
    pulse_second_derivative[ASC_POL] = np.polyder(pulse_first_derivative[ASC_POL])
    pulse_second_derivative[DESC_POL] = np.polyder(pulse_first_derivative[DESC_POL])
    # evaluate sections second derivatives polynoms
    pulse_second_derivative[ASC_SEC_EVAL] = np.polyval(pulse_second_derivative[ASC_POL], ascending_time)
    pulse_second_derivative[DESC_SEC_EVAL] = np.polyval(pulse_second_derivative[DESC_POL], descending_time)
    # concatenate second derivatives sections polynoms
    pulse_second_derivative[PULSE_EVAL] = np.concatenate((pulse_second_derivative[ASC_SEC_EVAL], pulse_second_derivative[DESC_SEC_EVAL]))

    return regular_pulse, pulse_first_derivative, pulse_second_derivative


# todo: change this to receive key_points dict
def _separate_pulse_in_sections(normalized_pulse, systolic_peak):
    ascending_section = normalized_pulse[0 : systolic_peak]
    descending_section = normalized_pulse[systolic_peak + 1 : -1]

    return ascending_section, descending_section


def _find_max_slope(pulse_first_derivative, key_points):
    max_slope = 0 # always returns 0 if the key point hasn't been detected

    maximals = pyampd.ampd.find_peaks(pulse_first_derivative[PULSE_EVAL])
    maximals_before_sys_peak = maximals[maximals < key_points[SYS_PEAK]]

    if (len(maximals_before_sys_peak) > 0):
        max_slope = maximals_before_sys_peak[0]

    return max_slope


def _find_diastolic_peak(pulse_first_derivative, pulse_second_derivative, key_points):
    fs = 125
    ts = np.round(1/(4*fs), 3)
    t = np.arange(0, len(pulse_second_derivative[PULSE_EVAL]) * ts, ts)

    diastolic_peak = 0 # always returns 0 if the key point hasn't been detected

    second_derivative_minimals = pyampd.ampd.find_peaks(-pulse_second_derivative[PULSE_EVAL])
    second_derivative_min_after_sys_peak = second_derivative_minimals[second_derivative_minimals > key_points[SYS_PEAK]]

    if len(second_derivative_minimals > 0):
        # Validate if we should get the first or the last minimal
        diastolic_peak = second_derivative_min_after_sys_peak[0]

    first_derivative_roots = np.roots(pulse_first_derivative[DESC_POL])
    positive_roots = first_derivative_roots[first_derivative_roots > 0]

    is_complex = np.iscomplex(positive_roots)
    if all(is_complex):
        return diastolic_peak

    is_real = np.isreal(positive_roots)
    real_roots = positive_roots[is_real]
    first_real_root = real_roots[0]
    min_root = first_real_root - ts
    max_root = first_real_root + ts

    is_greater_than_min = t > min_root
    is_less_than_max = t < max_root

    value_index = is_greater_than_min & is_less_than_max
    if not any(value_index):
        return diastolic_peak

    if pulse_first_derivative[PULSE_EVAL][value_index] and (pulse_second_derivative[PULSE_EVAL][value_index] < 0):
        diastolic_peak = np.where(t == t[value_index])
        return diastolic_peak

    return diastolic_peak


def _find_dicrotic_notch(pulse_second_derivative, key_points):
    dicrotic_notch = 0 # always returns 0 if the key point hasn't been detected

    second_derivative_maximals = pyampd.ampd.find_peaks(pulse_second_derivative[PULSE_EVAL])
    after_sys_peak = second_derivative_maximals > key_points[SYS_PEAK]
    before_dias_peak = second_derivative_maximals < key_points[DIAS_PEAK]

    second_derivative_maximals_between_sys_and_dias_peak = second_derivative_maximals[after_sys_peak & before_dias_peak]
    if (len(second_derivative_maximals_between_sys_and_dias_peak) > 0):
        dicrotic_notch = second_derivative_maximals_between_sys_and_dias_peak[0]

    return dicrotic_notch


def _find_inflection_poiint(pulse_second_derivative, key_points):
    fs = 125
    ts = np.round(1/(4*fs), 3)
    t = np.arange(0, len(pulse_second_derivative[PULSE_EVAL]) * ts, ts)

    inflection_point = 0 # always returns 0 if the key point hasn't been detected

    inflection_point = int(np.floor((key_points[DIC_NOTCH] + key_points[DIAS_PEAK]) / 2))

    second_derivative_roots = np.roots(pulse_second_derivative[DESC_POL])
    positive_roots = second_derivative_roots[second_derivative_roots > 0]

    roots_after_dic_notch = positive_roots > t[key_points[DIC_NOTCH]]
    roots_before_dias_peak = positive_roots < t[key_points[DIAS_PEAK]]

    roots_in_interval = positive_roots[roots_after_dic_notch & roots_before_dias_peak]

    is_complex = np.iscomplex(roots_in_interval)
    if all(is_complex):
        return inflection_point

    is_real = np.isreal(roots_in_interval)
    real_roots = roots_in_interval[is_real]
    if len(real_roots == 0):
        return inflection_point

    first_real_root_in_interval = real_roots[0]
    min_root = first_real_root_in_interval - ts
    max_root = first_real_root_in_interval + ts

    is_greater_than_min = t > min_root
    is_less_than_max = t < max_root

    is_in_interval = is_greater_than_min & is_less_than_max & after_dic_notch & before_dias_peak
    if not any(is_in_interval):
        return inflection_point

    inflection_point = np.where(t == t[is_in_interval])

    return inflection_point
