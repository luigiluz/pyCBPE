""" This is the package responsible for realizing the arterial blood pressure
signal label extraction. """

import numpy as np
from pyampd.ampd import find_peaks

def extract(abp_segment):
    labels = []

    # calculate labels
    systolic_blood_pressure = _get_systolic_blood_pressure(abp_segment)
    diastolic_blood_pressure = _get_diastolic_blood_pressure(abp_segment)
    mean_absolute_pressure = _get_mean_absolute_pressure(abp_segment)

    # append labels to list
    labels.append(systolic_blood_pressure)
    labels.append(diastolic_blood_pressure)
    labels.append(mean_absolute_pressure)

    return labels


def _get_systolic_blood_pressure(abp_segment):
    maximals_locations = find_peaks(abp_segment)
    if len(maximals_locations) == 0:
        systolic_blood_pressure = -1
        return systolic_blood_pressure

    maximals_values = abp_segment[maximals_locations]
    mean_maximal_values = np.mean(maximals_values)
    systolic_blood_pressure = int(np.floor(mean_maximal_values))

    return systolic_blood_pressure


def _get_diastolic_blood_pressure(abp_segment):
    minimals_locations = find_peaks(-abp_segment)
    if len(minimals_locations) == 0:
        diastolic_blood_presure = -1
        return diastolic_blood_presure

    minimals_values = abp_segment[minimals_locations]
    mean_minimal_values = np.mean(minimals_values)
    diastolic_blood_presure = int(np.floor(mean_minimal_values))

    return diastolic_blood_presure


def _get_mean_absolute_pressure(abp_segment):
    mean_value = np.mean(abp_segment)
    mean_absolute_pressure = int(np.floor(mean_value))

    return mean_absolute_pressure
