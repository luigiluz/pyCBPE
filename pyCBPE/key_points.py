""" This is the package responsible for realizing the photoplethysmogram
pulse key points extraction. """

import numpy as np
import pyampd
import constants as consts


def extract(normalized_pulse):
    is_normalized_pulse_empty = normalized_pulse.size == 0
    if is_normalized_pulse_empty:
        key_points = {}
        return key_points

    # group all key points in this dictionary
    key_points = {
        consts.SYS_PEAK: 0,
        consts.MAX_SLP: 0,
        consts.DIAS_PEAK: 0,
        consts.DIC_NOTCH: 0,
        consts.INFL_POINT: 0
    }

    key_points[consts.SYS_PEAK] = _find_systolic_peak_location(normalized_pulse)
    if key_points[consts.SYS_PEAK] == 0:
        key_points = {}
        return key_points

    regular_pulse, pulse_first_derivative, pulse_second_derivative = _fit_section_polynoms(normalized_pulse, key_points[consts.SYS_PEAK])

    key_points[consts.MAX_SLP] = _find_max_slope(pulse_first_derivative, key_points)
    if key_points[consts.MAX_SLP] == 0:
        key_points = {}
        return key_points

    key_points[consts.DIAS_PEAK] = _find_diastolic_peak(pulse_first_derivative, pulse_second_derivative, key_points)
    if key_points[consts.DIAS_PEAK] == 0:
        key_points = {}
        return key_points

    key_points[consts.DIC_NOTCH] = _find_dicrotic_notch(pulse_second_derivative, key_points)
    if key_points[consts.DIC_NOTCH] == 0:
        key_points = {}
        return key_points

    key_points[consts.INFL_POINT] = _find_inflection_point(pulse_second_derivative, key_points)
    if key_points[consts.INFL_POINT] == 0:
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
    pulse_length = len(normalized_pulse)
    up_sampled_rate = 1 / (4*consts.SAMPLING_FREQ)
    pulse_time = np.linspace(0, pulse_length * up_sampled_rate, num = pulse_length, endpoint=False)

    ascending_section, descending_section = _separate_pulse_in_sections(normalized_pulse, systolic_peak)

    ascending_len = len(ascending_section)
    descending_len = len(descending_section)

    # prealocation
    regular_pulse = {
        consts.ASC_POL : np.zeros(consts.ASCENDING_POL_N_OF_COEFS),
        consts.DESC_POL : np.zeros(consts.DESCENDING_POL_N_OF_COEFS),
        consts.ASC_SEC_EVAL : np.zeros(ascending_len),
        consts.DESC_SEC_EVAL : np.zeros(descending_len),
        consts.PULSE_EVAL: np.zeros(ascending_len + descending_len)
    }

    pulse_first_derivative = {
        consts.ASC_POL : np.zeros(consts.ASCENDING_POL_N_OF_COEFS),
        consts.DESC_POL : np.zeros(consts.DESCENDING_POL_N_OF_COEFS),
        consts.ASC_SEC_EVAL : np.zeros(ascending_len),
        consts.DESC_SEC_EVAL : np.zeros(descending_len),
        consts.PULSE_EVAL: np.zeros(ascending_len + descending_len)
    }

    pulse_second_derivative = {
        consts.ASC_POL : np.zeros(consts.ASCENDING_POL_N_OF_COEFS),
        consts.DESC_POL : np.zeros(consts.DESCENDING_POL_N_OF_COEFS),
        consts.ASC_SEC_EVAL : np.zeros(ascending_len),
        consts.DESC_SEC_EVAL : np.zeros(descending_len),
        consts.PULSE_EVAL: np.zeros(ascending_len + descending_len)
    }

    ascending_time = pulse_time[0:systolic_peak]
    descending_time = pulse_time[systolic_peak + 1 : -1]

    ###### without derivative ######
    # fit sections polynoms
    regular_pulse[consts.ASC_POL] = np.polyfit(ascending_time, ascending_section, deg=5)
    regular_pulse[consts.DESC_POL] = np.polyfit(descending_time, descending_section, deg=7)
    # evaluate sections polynoms
    regular_pulse[consts.ASC_SEC_EVAL] = np.polyval(regular_pulse[consts.ASC_POL], ascending_time)
    regular_pulse[consts.DESC_SEC_EVAL] = np.polyval(regular_pulse[consts.DESC_POL], descending_time)
    # concatenate sections polynoms
    regular_pulse[consts.PULSE_EVAL] = np.concatenate((regular_pulse[consts.ASC_SEC_EVAL], regular_pulse[consts.DESC_SEC_EVAL]))

    ###### first derivative ######
    # fit sections first derivatives polynoms
    pulse_first_derivative[consts.ASC_POL] = np.polyder(regular_pulse[consts.ASC_POL])
    pulse_first_derivative[consts.DESC_POL] = np.polyder(regular_pulse[consts.DESC_POL])
    # evaluate sections first derivatives polynoms
    pulse_first_derivative[consts.ASC_SEC_EVAL] = np.polyval(pulse_first_derivative[consts.ASC_POL], ascending_time)
    pulse_first_derivative[consts.DESC_SEC_EVAL] = np.polyval(pulse_first_derivative[consts.DESC_POL], descending_time)
    # concatenate first derivates sections polynoms
    pulse_first_derivative[consts.PULSE_EVAL] = np.concatenate((pulse_first_derivative[consts.ASC_SEC_EVAL], pulse_first_derivative[consts.DESC_SEC_EVAL]))

    ###### second derivative ######
    # fit sections second derivatives polynoms
    pulse_second_derivative[consts.ASC_POL] = np.polyder(pulse_first_derivative[consts.ASC_POL])
    pulse_second_derivative[consts.DESC_POL] = np.polyder(pulse_first_derivative[consts.DESC_POL])
    # evaluate sections second derivatives polynoms
    pulse_second_derivative[consts.ASC_SEC_EVAL] = np.polyval(pulse_second_derivative[consts.ASC_POL], ascending_time)
    pulse_second_derivative[consts.DESC_SEC_EVAL] = np.polyval(pulse_second_derivative[consts.DESC_POL], descending_time)
    # concatenate second derivatives sections polynoms
    pulse_second_derivative[consts.PULSE_EVAL] = np.concatenate((pulse_second_derivative[consts.ASC_SEC_EVAL], pulse_second_derivative[consts.DESC_SEC_EVAL]))

    return regular_pulse, pulse_first_derivative, pulse_second_derivative


# todo: change this to receive key_points dict
def _separate_pulse_in_sections(normalized_pulse, systolic_peak):
    ascending_section = normalized_pulse[0 : systolic_peak]
    descending_section = normalized_pulse[systolic_peak + 1 : -1]

    return ascending_section, descending_section


def _find_max_slope(pulse_first_derivative, key_points):
    max_slope = 0 # always returns 0 if the key point hasn't been detected

    maximals = pyampd.ampd.find_peaks(pulse_first_derivative[consts.PULSE_EVAL])
    maximals_before_sys_peak = maximals[maximals < key_points[consts.SYS_PEAK]]

    if (len(maximals_before_sys_peak) > 0):
        max_slope = maximals_before_sys_peak[0]

    return max_slope


def _find_diastolic_peak(pulse_first_derivative, pulse_second_derivative, key_points):
    diastolic_peak = 0 # always returns 0 if the key point hasn't been detected
    ppg_pulse_second_derivative = pulse_second_derivative[consts.PULSE_EVAL]
    ts = np.round(1/(4*consts.SAMPLING_FREQ), 3)
    t = np.linspace(0, len(ppg_pulse_second_derivative) * ts, num=len(ppg_pulse_second_derivative), endpoint=False)

    if len(ppg_pulse_second_derivative) != len(t):
        return diastolic_peak

    second_derivative_minimals = pyampd.ampd.find_peaks(-ppg_pulse_second_derivative)
    second_derivative_min_after_sys_peak = second_derivative_minimals[second_derivative_minimals > key_points[consts.SYS_PEAK]]

    if len(second_derivative_min_after_sys_peak) > 0:
        # Validate if we should get the first or the last minimal
        diastolic_peak = second_derivative_min_after_sys_peak[0]

    first_derivative_roots = np.roots(pulse_first_derivative[consts.DESC_POL])
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

    ppg_pulse_second_derivative_at_roots = ppg_pulse_second_derivative[value_index]
    # TO DO: Consider add treatment to when value index has more than one value
    if (ppg_pulse_second_derivative_at_roots[0]) < 0:
        t_at_roots = t[value_index]
        tmp_diastolic_peak = np.where(t == t_at_roots[0])
        diastolic_peak = tmp_diastolic_peak[0][0]
        return diastolic_peak

    return diastolic_peak


def _find_dicrotic_notch(pulse_second_derivative, key_points):
    dicrotic_notch = 0 # always returns 0 if the key point hasn't been detected

    second_derivative_maximals = pyampd.ampd.find_peaks(pulse_second_derivative[consts.PULSE_EVAL])
    after_sys_peak = second_derivative_maximals > key_points[consts.SYS_PEAK]
    before_dias_peak = second_derivative_maximals < key_points[consts.DIAS_PEAK]

    second_derivative_maximals_between_sys_and_dias_peak = second_derivative_maximals[after_sys_peak & before_dias_peak]
    if (len(second_derivative_maximals_between_sys_and_dias_peak) > 0):
        dicrotic_notch = second_derivative_maximals_between_sys_and_dias_peak[0]

    return dicrotic_notch


def _find_inflection_point(pulse_second_derivative, key_points):
    ts = np.round(1/(4*consts.SAMPLING_FREQ), 3)
    t = np.linspace(0, len(pulse_second_derivative[consts.PULSE_EVAL]) * ts, num=len(pulse_second_derivative[consts.PULSE_EVAL]), endpoint=False)

    inflection_point = 0 # always returns 0 if the key point hasn't been detected

    inflection_point = int(np.floor((key_points[consts.DIC_NOTCH] + key_points[consts.DIAS_PEAK]) / 2))

    second_derivative_roots = np.roots(pulse_second_derivative[consts.DESC_POL])
    positive_roots = second_derivative_roots[second_derivative_roots > 0]

    roots_after_dic_notch = positive_roots > t[key_points[consts.DIC_NOTCH]]
    roots_before_dias_peak = positive_roots < t[key_points[consts.DIAS_PEAK]]

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

    tmp_inflection_point = np.where(t == t[is_in_interval])
    inflection_point = tmp_inflection_point[0][0]

    return inflection_point
