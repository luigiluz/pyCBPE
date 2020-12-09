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
	# group all key points in this dictionary
	key_points = {
		SYS_PEAK: 0,
		MAX_SLP: 0,
		DIAS_PEAK: 0,
		DIC_NOTCH: 0,
		INFL_POINT: 0
	}

	key_points[SYS_PEAK] = _find_systolic_peak_location(normalized_pulse)

	regular_pulse, pulse_first_derivative, pulse_second_derivative = _fit_section_polynoms(normalized_pulse, key_points[SYS_PEAK])

	key_points[MAX_SLP] = _find_max_slope(pulse_first_derivative, key_points)

	# key_points["diastolic peak"] = _find_diastolic_peak()
	# key_points["dicrotic notch"] = _find_dicrotic_notch()
	# key_points["inflection point"] = "find_inflection_point()"


def _find_systolic_peak_location(normalized_pulse):
	systolic_peak = pyampd.ampd.find_peaks(normalized_pulse)

	return systolic_peak


def _fit_section_polynoms(normalized_pulse, systolic_peak):
	sampling_freq = 125
	pulse_length = len(normalized_pulse)
	pulse_time = np.arange(0, pulse_length / sampling_freq, 1 / sampling_freq)
	# prealocation
	regular_pulse = {
		ASC_POL : np.zeros(ASCENDING_POL_N_OF_COEFS), # add this to a constant
		DESC_POL : np.zeros(DESCENDING_POL_N_OF_COEFS), # add this to a constant
		ASC_SEC_EVAL : np.zeros(ascending_len),
		DESC_SEC_EVAL : np.zeros(descending_len),
		PULSE_EVAL: np.zeros(ascending_len + descending_len)
	}

	pulse_first_derivative = {
		ASC_POL : np.zeros(ASCENDING_POL_N_OF_COEFS), # add this to a constant
		DESC_POL : np.zeros(DESCENDING_POL_N_OF_COEFS), # add this to a constant
		ASC_SEC_EVAL : np.zeros(ascending_len),
		DESC_SEC_EVAL : np.zeros(descending_len),
		PULSE_EVAL: np.zeros(ascending_len + descending_len)
	}

	pulse_second_derivative = {
		ASC_POL : np.zeros(ASCENDING_POL_N_OF_COEFS), # add this to a constant
		DESC_POL : np.zeros(DESCENDING_POL_N_OF_COEFS), # add this to a constant
		ASC_SEC_EVAL : np.zeros(ascending_len),
		DESC_SEC_EVAL : np.zeros(descending_len),
		PULSE_EVAL: np.zeros(ascending_len + descending_len)
	}

	ascending_section, descending_section = _separate_pulse_in_sections(normalized_pulse, systolic_peak)

	ascending_len = len(ascending_section)
	descending_len = len(descending_section)

	ascending_time = pulse_time[0 : systolic_peak]
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
	pulse_first_derivative[ASC_POL] = np.polyder(ascending_polynom)
	pulse_first_derivative[DESC_POL] = np.polyder(descending_polynom)
	# evaluate sections first derivatives polynoms
	pulse_first_derivative[ASC_SEC_EVAL] = np.polyval(pulse_first_derivative[ASC_POL], ascending_time)
	pulse_first_derivative[DESC_SEC_EVAL] = np.polyval(pulse_first_derivative[DESC_POL], descending_time)
	# concatenate first derivates sections polynoms
	pulse_first_derivative[PULSE_EVAL] = np.concatenate((pulse_first_derivative[ASC_SEC_EVAL], pulse_first_derivative[DESC_SEC_EVAL]))

	###### second derivative ######
	# fit sections second derivatives polynoms
	pulse_second_derivative[ASC_POL] = np.polyder(ascending_pol_first_der)
	pulse_second_derivative[DESC_POL] = np.polyder(descending_pol_first_der)
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
	# max slope is the point where the first derivative has its largest value
	# it happens BEFORE systolic peak

	maximals = pyampd.ampd.find_peaks(pulse_first_derivative[PULSE_EVAL])
	maximals_before_sys_peak = maximals[maximals < key_points[SYS_PEAK]]

	if (len(maximals_before_sys_peak) > 1):
		max_slope = maximals_before_sys_peak[0]

	return max_slope

# entradas necessarias:
# first_derivative_eval
# first_derivative_pol
# second_derivative_eval
# systolic_peak
def _find_diastolic_peak(pulse_first_derivative, pulse_second_derivative, key_points):
	# the point at which the first derivative of the polynomial is equal to zero
	# and the second derivative is negative
	# it happens AFTER systolic peak
	# if there is no such point
	# then the point at which the second derivative is a local minimum is chosen as the diastolic peak

	diastolic_peak = 0 # always returns 0 if the key point hasn't been detected

	# note: consider using np.roots(p) to find the roots of the polynom

# entradas necessarias:
# systolic_peak
# diastolic_peak
# second_derivative_eval
def _find_dicrotic_notch(pulse_second_derivative, key_points):
	dicrotic_notch = 0 # always returns 0 if the key point hasn't been detected
	# is located BEFORE diastolic peak and AFTER systolic peak
	# the point where the second derivative of the PPG signal is a local maximum

	second_derivative_maximals = pyampd.ampd.find_peaks(pulse_second_derivative[PULSE_EVAL])
	after_sys_peak = second_derivative_maximals > key_points[SYS_PEAK]
	before_dias_peak = second_derivative_maximals < key_points[DIAS_PEAK]

	second_derivative_maximals_between_sys_and_dias_peak = after_sys_peak & before_dias_peak
	if (len(second_derivative_maximals_between_sys_and_dias_peak) > 1):
		dicrotic_notch = second_derivative_maximals_between_sys_and_dias_peak[0]

	return dicrotic_notch

# entradas necessarias:
# dicrotic_notch
# diastolic_peak
# second_derivative_eval
# second_derivative_pol
def _find_inflection_poiint():
	# it lies between the dicrotic notch and diastolic peak
	# it is located AFTER dicrotic notch and BEFORE diastolic peak
	# at this point, the second derivative of the PPG signal is equal to zero
	# if no such point exists, the inflection point is chosen to be
	# the midpoint between the dicrotic notch and the diastolic peak

	inflection_point = 0 # always returns 0 if the key point hasn't been detected

	# note: consider using np.roots(p) to find the roots of the polynom
