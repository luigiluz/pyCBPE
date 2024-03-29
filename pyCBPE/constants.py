""" This module will contain all the constants used in pyCBPE package """

ROOT_PATH = "/home/luigiluz/Documents/pessoal/pyCBPE"

N_OF_DATASET_FILES = 4

# Dataset paths
DATASET_PATH = "/files/dataset/"

PPG_SEG_MATRIX_SPLIT_1_PATH = DATASET_PATH + "ppg_matrix_split_1.csv"
ABP_SEG_MATRIX = "/files/dataset/abp_matrix_split_1.csv"

FEATURES_AND_LABELS_DF_PREFIX = "features_and_labels_df_split_"
ORIGINAL_DATASET_PREFIX = "Part_"
CSV_SUFIX = ".csv"
MAT_SUFIX = ".mat"

PPG_DF_PREFIX = "ppg_seg_df_split_"
ABP_DF_PREFIX = "abp_seg_df_split_"

FEATURES_AND_LABELS_DF_SPLIT_1_PATH = ROOT_PATH + DATASET_PATH + "features_and_labels_df_split_1.csv"
FEATURES_AND_LABELS_DF_SPLIT_2_PATH = ROOT_PATH + DATASET_PATH + "features_and_labels_df_split_2.csv"
FEATURES_AND_LABELS_DF_SPLIT_3_PATH = ROOT_PATH + DATASET_PATH + "features_and_labels_df_split_3.csv"
FEATURES_AND_LABELS_DF_SPLIT_4_PATH = ROOT_PATH + DATASET_PATH + "features_and_labels_df_split_4.csv"

OUTPUT_PATH = "/files/dataset/features_and_labels_df.csv"


# Estimators paths
ALL_METRICS_FILENAME = "all_metrics.csv"
BHS_METRICS_FILENAME = "bhs_metrics.csv"
AAMI_METRICS_FILENAME = "aami_metrics.csv"
STATS_METRICS_FILENAME = "stats_metrics.csv"


# Code related paths
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
