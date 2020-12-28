""" This is the package responsible for realizing the photoplethysmogram
signal feature extraction. """

import numpy as np
from pyampd.ampd import find_peaks
from scipy.interpolate import CubicSpline
from scipy.signal import cheby1
from scipy.signal import lfilter
from scipy.fft import fft

SYS_PEAK = "systolic peak"
MAX_SLP = "max slope"
DIAS_PEAK = "diastolic peak"
DIC_NOTCH = "dicrotic notch"
INFL_POINT = "inflection point"

def extract(sampling_freq, ppg_segment, normalized_ppg_pulse, key_points):
    features = []

    is_key_points_empty = not bool(key_points)
    if is_key_points_empty:
        return features

    up_sampled_sampling_freq = 4 * sampling_freq

    # calculate features
    heart_rate = _get_heart_rate(up_sampled_sampling_freq, normalized_ppg_pulse)
    mnpv = _get_mnpv(ppg_segment)
    area_related_features = _get_area_related_features(up_sampled_sampling_freq, normalized_ppg_pulse, key_points)
    amplitude_related_features = _get_amplitude_related_features(normalized_ppg_pulse, key_points)
    time_related_features = _get_time_related_features(up_sampled_sampling_freq, normalized_ppg_pulse, key_points)
    hrv_properties = _get_hrv_properites(sampling_freq, ppg_segment)
    non_linear_functions = _get_non_linear_functions(heart_rate, mnpv, amplitude_related_features)

    # append features to list
    features.append(heart_rate)
    features.append(mnpv)
    features.extend(area_related_features)
    features.extend(amplitude_related_features)
    features.extend(time_related_features)
    features.extend(hrv_properties)
    features.extend(non_linear_functions)

    return features


def _get_heart_rate(sampling_freq, normalized_ppg_pulse):
    heart_rate = np.floor(60 / (len(normalized_ppg_pulse)/sampling_freq))

    return int(heart_rate)


def _get_mnpv(ppg_segment):
    Iac = np.ndarray.max(ppg_segment) - np.ndarray.min(ppg_segment)
    Idc = np.mean(ppg_segment)
    mnpv = Iac / (Iac + Idc)

    return mnpv


def _get_area_related_features(sampling_freq, normalized_ppg_pulse, key_points):
    area_related_features = []

    ts = 1 / sampling_freq
    t = np.arange(0, len(normalized_ppg_pulse) * ts, ts)

    # calculate area related features
    max_slp_sys_peak_area = _area_between_two_points(t, normalized_ppg_pulse, key_points[MAX_SLP], key_points[SYS_PEAK])
    sys_peak_dic_notch_area = _area_between_two_points(t, normalized_ppg_pulse, key_points[SYS_PEAK], key_points[DIC_NOTCH])
    dic_notch_infl_point_area = _area_between_two_points(t, normalized_ppg_pulse, key_points[DIC_NOTCH], key_points[INFL_POINT])
    infl_point_dias_peak = _area_between_two_points(t, normalized_ppg_pulse, key_points[INFL_POINT], key_points[DIAS_PEAK])
    pulse_area = np.trapz(normalized_ppg_pulse, t)
    infl_point_area = np.trapz(normalized_ppg_pulse[key_points[INFL_POINT]:-1], t[key_points[INFL_POINT]:-1]) / np.trapz(normalized_ppg_pulse[0:key_points[INFL_POINT]], t[0:key_points[INFL_POINT]])

    # append area related features to list
    area_related_features.append(max_slp_sys_peak_area)
    area_related_features.append(sys_peak_dic_notch_area)
    area_related_features.append(dic_notch_infl_point_area)
    area_related_features.append(infl_point_dias_peak)
    area_related_features.append(pulse_area)
    area_related_features.append(infl_point_area)

    return area_related_features


def _area_between_two_points(x, y, first_point, last_point):
    area = 0
    if (first_point < last_point):
        area = np.trapz(y[first_point:last_point], x[first_point:last_point])

    return area


def _get_amplitude_related_features(normalized_ppg_pulse, key_points):
    amplitude_related_features = []

    # calculate amplitude related features
    max_slp_reflection_index = normalized_ppg_pulse[key_points[MAX_SLP]]
    dias_peak_reflection_index = normalized_ppg_pulse[key_points[DIAS_PEAK]]
    dic_notch_reflection_index = normalized_ppg_pulse[key_points[DIC_NOTCH]]
    infl_point_reflection_index = normalized_ppg_pulse[key_points[INFL_POINT]]

    # append amplitude related features to list
    amplitude_related_features.append(max_slp_reflection_index)
    amplitude_related_features.append(dias_peak_reflection_index)
    amplitude_related_features.append(dic_notch_reflection_index)
    amplitude_related_features.append(infl_point_reflection_index)

    return amplitude_related_features


def _get_time_related_features(sampling_freq, normalized_ppg_pulse, key_points):
    time_related_features = []

    ts = 1 / sampling_freq
    t = np.arange(0, len(normalized_ppg_pulse) * ts, ts)

    # calculate time related features
    max_slp_sys_peak_lasi = _get_inverse_of_time_interval(t, key_points[MAX_SLP], key_points[SYS_PEAK])
    dias_peak_sys_peak_lasi = _get_inverse_of_time_interval(t, key_points[SYS_PEAK], key_points[DIAS_PEAK])
    dic_notch_sys_peak_lasi = _get_inverse_of_time_interval(t, key_points[SYS_PEAK], key_points[DIC_NOTCH])
    infl_point_sys_peak_lasi = _get_inverse_of_time_interval(t, key_points[SYS_PEAK], key_points[INFL_POINT])

    crest_time = t[key_points[SYS_PEAK]]

    # append time related features to list
    time_related_features.append(max_slp_sys_peak_lasi)
    time_related_features.append(dias_peak_sys_peak_lasi)
    time_related_features.append(dic_notch_sys_peak_lasi)
    time_related_features.append(infl_point_sys_peak_lasi)

    time_related_features.append(crest_time)

    # TO DO: investigate on how to implement pulse width
    #time_related_features.append()

    return time_related_features


def _get_inverse_of_time_interval(t, first_point, last_point):
    inverse_of_time_interval = 0

    if first_point < last_point:
        time_interval = t[last_point] - t[first_point]
        inverse_of_time_interval = 1 / time_interval

    return inverse_of_time_interval


def _get_hrv_properites(sampling_freq, ppg_segment):
    hrv_properties = []

    ppg_minimals = find_peaks(-ppg_segment)
    samples_between_pulses = np.diff(ppg_minimals)
    minimal_to_minimal_interval = samples_between_pulses / sampling_freq

    minimal_to_minimal_cumsum = np.cumsum(minimal_to_minimal_interval)
    minimal_to_minimal_time_axis = np.subtract(minimal_to_minimal_cumsum, minimal_to_minimal_cumsum[0])

    hrv_sampling_freq = 2.5 # in Hz
    hrv_sampling_rate = 1 / hrv_sampling_freq
    interpolation_time = np.arange(0, len(minimal_to_minimal_time_axis) * hrv_sampling_rate, hrv_sampling_rate)

    cubic_spline_interp = CubicSpline(minimal_to_minimal_time_axis, minimal_to_minimal_interval)
    hrv = cubic_spline_interp(interpolation_time)

    dc_free_hrv = hrv - np.mean(hrv)

    cut_off_frequency_rad = 0.03 / (hrv_sampling_freq / 2)
    [b, a] = cheby1(N = 9, rp = 0.5, Wn = cut_off_frequency_rad, btype='high')
    high_pass_filtered_hrv = lfilter(b, a, dc_free_hrv)

    fft_hrv = fft(high_pass_filtered_hrv)
    abs_fft_hrv = np.absolute(fft_hrv)
    psd_hrv = np.power(abs_fft_hrv, 2)
    n_of_psd_samples = len(psd_hrv)

    psd_frequency_axis = np.arange(0, hrv_sampling_freq / 2, hrv_sampling_freq / (2*n_of_psd_samples))

    low_frequency = (0.04 < psd_frequency_axis) & (psd_frequency_axis < 0.15)
    high_frequency = (0.15 < psd_frequency_axis) & (psd_frequency_axis < 0.40)

    # calculate hrv properties
    mean_hrv = np.mean(hrv)
    std_hrv = np.std(hrv)
    hrv_total_power = sum(psd_hrv)
    hrv_low_frequency = sum(psd_hrv[low_frequency]) / hrv_total_power
    hrv_high_frequency = sum(psd_hrv[high_frequency]) / hrv_total_power
    hrv_low_freq_high_freq_ratio = hrv_low_frequency / hrv_high_frequency

    # append hrv properties to list
    hrv_properties.append(mean_hrv)
    hrv_properties.append(std_hrv)
    hrv_properties.append(hrv_total_power)
    hrv_properties.append(hrv_low_frequency)
    hrv_properties.append(hrv_high_frequency)
    hrv_properties.append(hrv_low_freq_high_freq_ratio)

    return hrv_properties


def _get_non_linear_functions(heart_rate, mnpv, amplitude_related_features):
    non_linear_functions = []

    # get the reflection indexes from amplitude_related_features
    dic_notch_reflection_index = amplitude_related_features[2]
    infl_point_reflection_index = amplitude_related_features[3]

    # calculate non linear function of features
    log_heart_rate = np.log(heart_rate)
    exp_heart_rate = np.exp(heart_rate)
    log_mnpv = np.log(mnpv)
    exp_mnpv = np.exp(mnpv)
    log_dic_notch_refl_index = np.log(dic_notch_reflection_index)
    log_infl_point_refl_index = np.log(infl_point_reflection_index)
    log_hr_mnpv = np.log(heart_rate * mnpv)

    # append non linear functions to list
    non_linear_functions.append(log_heart_rate)
    non_linear_functions.append(exp_heart_rate)
    non_linear_functions.append(log_mnpv)
    non_linear_functions.append(exp_mnpv)
    non_linear_functions.append(log_dic_notch_refl_index)
    non_linear_functions.append(log_infl_point_refl_index)
    non_linear_functions.append(log_hr_mnpv)

    return non_linear_functions