""" This module will contain all the constants used in cbpe-python package """

ROOT_PATH = "/home/luigi/git/cbpe-python"

PPG_SEG_PATH = "/files/ppg_seg.csv"
ABP_SEG_PATH = "/files/abp_seg.csv"

PPG_SEG_MATRIX = "/files/ppg_matrix.csv"
PPG_SEG_MATRIX_01 = "/files/ppg_matrix_01.csv"
PPG_SEG_MATRIX_02 = "/files/ppg_matrix_02.csv"
PPG_SEG_MATRIX_03 = "/files/ppg_matrix_03.csv"
PPG_SEG_MATRIX_04 = "/files/ppg_matrix_04.csv"

ABP_SEG_MATRIX = "/files/abp_matrix.csv"
ABP_SEG_MATRIX_01 = "/files/abp_matrix_01.csv"
ABP_SEG_MATRIX_02 = "/files/abp_matrix_02.csv"
ABP_SEG_MATRIX_03 = "/files/abp_matrix_03.csv"
ABP_SEG_MATRIX_04 = "/files/abp_matrix_04.csv"


LINEAR_REGRESSOR_OUTPUT_PATH = "/files/estimators/linear_regressor.joblib"

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

# Features columns
HEART_RATE = ["Heart rate"]
MNPV = ["MNPV"]
AREA_RELATED_FEATURES = [
    "Max slope sys peak area",
    "Sys peak dic notch area",
    "Dic notch infl point area",
    "Infl point dias peak area",
    "Pulse area",
    "Infl point area"
]
AMPLITUDE_RELATED_FEATURES = [
    "Max slope reflection index",
    "Dias peak reflection index",
    "Dic notch reflection index",
    "Infl point reflection index"
]
TIME_RELATED_FEATURES = [
    "Max slope sys peak LASI",
    "Dias peak sys peak LASI",
    "Dic notch sys peak LASI",
    "Infl point sys peak LASI",
    "Crest time",
    "Pulse width"
]
HRV_PROPERTIES = [
    "Mean HRV",
    "Std HRV",
    "HRV total power",
    "HRV low frequency",
    "HRV high frequency",
    "HRV lf/hf ratio"
]
NON_LINEAR_FUNCTIONS = [
    "ln(Heart rate)",
    "exp(Heart rate)",
    "ln(mnpv)",
    "exp(mnpv)",
    "ln(dic_notch_refl_index)",
    "ln(infl_pint_refl_index)",
    "ln(hr * mnpv)"
]
FEATURES_COLUMNS = (
                    HEART_RATE +
                    MNPV +
                    AREA_RELATED_FEATURES +
                    AMPLITUDE_RELATED_FEATURES +
                    TIME_RELATED_FEATURES +
                    HRV_PROPERTIES +
                    NON_LINEAR_FUNCTIONS
                    )
# Labels columns
SBP = "Systolic blood pressure"
DBP = "Diastolic blood pressure"
MAP = "Mean absolute pressure"
LABELS_COLUMNS = [
    SBP,
    DBP,
    MAP
]
# Dataframe columns
FEATURES_AND_LABELS_COLUMNS = FEATURES_COLUMNS + LABELS_COLUMNS
