""" This module will contain all the constants used in cbpe-python package """

ROOT_PATH = "/home/lfml-cesar/Documents/UACSA/cbpe-python"
PPG_SEG_PATH = "/files/ppg_seg.csv"
ABP_SEG_PATH = "/files/abp_seg.csv"

SAMPLING_FREQ = 125

# PPG Signal key points dictionary keys
SYS_PEAK = "systolic peak"
MAX_SLP = "max slope"
DIAS_PEAK = "diastolic peak"
DIC_NOTCH = "dicrotic notch"
INFL_POINT = "inflection point"

# Interpolation polynoms orders and coefficients
ASCENDING_POL_ORDER = 5
ASCENDING_POL_N_OF_COEFS = ASCENDING_POL_ORDER + 1
DESCENDING_POL_ORDER = 7
DESCENDING_POL_N_OF_COEFS = DESCENDING_POL_ORDER + 1

# Polynoms dictionary keys
ASC_POL = "ascending_pol"
DESC_POL = "descending_pol"
ASC_SEC_EVAL = "ascending_section_eval"
DESC_SEC_EVAL = "descending_section_eval"
PULSE_EVAL = "pulse_eval"