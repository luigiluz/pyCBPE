""" This is the package responsible for evaluating an estimator. """

import numpy as np
import pandas as pd
import constants as consts

# Labels indexes
SBP_INDEX = 0
DBP_INDEX = 1
MAP_INDEX = 2

# BHS standard constants
BHS_FIRST_THRESHOLD = "<= 5 mmHg"
BHS_SECOND_THRESHOLD = "<= 10 mmHg"
BHS_THIRD_THRESHOLD = "<= 15 mmHg"

BHS_GRADE_C_1ST_LIMIT = 40
BHS_GRADE_C_2ND_LIMIT = 65
BHS_GRADE_C_3RD_LIMIT = 85

BHS_GRADE_B_1ST_LIMIT = 50
BHS_GRADE_B_2ND_LIMIT = 75
BHS_GRADE_B_3RD_LIMIT = 90

BHS_GRADE_A_1ST_LIMIT = 60
BHS_GRADE_A_2ND_LIMIT = 85
BHS_GRADE_A_3RD_LIMIT = 95

GRADE = "Grade"

GRADE_A = "A"
GRADE_B = "B"
GRADE_C = "C"
GRADE_D = "D"

# AAMI standard constants
AAMI_ME_THRESHOLD = 5
AAMI_STD_THRESHOLD = 8

AAMI_ME_THRESHOLD_STR = "ME (<= 5 mmHg)"
AAMI_STD_THRESHOLD_STR = "STD (<= 8 mmHg)"

AAMI_PASSED = "Passed AAMI"
YES = "Yes"
NO = "No"


def _evaluate_aami_standard(y_true, y_pred):
    error = y_true - y_pred

    sbp_me = np.round(np.mean(error[:, SBP_INDEX]), 2)
    sbp_std = np.round(np.std(y_pred[:, SBP_INDEX]), 2)

    dbp_me = np.round(np.mean(error[:, DBP_INDEX]), 2)
    dbp_std = np.round(np.std(y_pred[:, DBP_INDEX]), 2)

    map_me = np.round(np.mean(error[:, MAP_INDEX]), 2)
    map_std = np.round(np.std(y_pred[:, MAP_INDEX]), 2)

    aami_df = pd.DataFrame({AAMI_ME_THRESHOLD_STR [sbp_me, dbp_me, map_me],
                           AAMI_STD_THRESHOLD_STR: [sbp_std, dbp_std, map_std]},
                          index = consts.LABELS_COLUMNS)

    me_condition = aami_df.loc[:, AAMI_ME_THRESHOLD_STR] < AAMI_ME_THRESHOLD
    std_condition = aami_df.loc[:, AAMI_STD_THRESHOLD_STR] < AAMI_STD_THRESHOLD
    passed_condition = me_condition & std_condition

    aami_df.loc[:, AAMI_PASSED] = NO
    aami_df.loc[passed_condition, AAMI_PASSED] = YES

    return aami_df


def _evaluate_bhs_standard(y_true, y_pred):
    (sbp_error5, sbp_error10, sbp_error15) = bhs_standard(y_true[:, SBP_INDEX], y_pred[:, SBP_INDEX])
    (dbp_error5, dbp_error10, dbp_error15) = bhs_standard(y_true[:, DBP_INDEX], y_pred[:, DBP_INDEX])
    (map_error5, map_error10, map_error15) = bhs_standard(y_true[:, MAP_INDEX], y_pred[:, MAP_INDEX])

    bhs_df = pd.DataFrame({BHS_FIRST_THRESHOLD : [sbp_error5, dbp_error5, map_error5],
                           BHS_SECOND_THRESHOLD : [sbp_error10, dbp_error10, map_error10],
                           BHS_THIRD_THRESHOLD : [sbp_error15, dbp_error15, map_error15]},
                          index = consts.LABELS_COLUMNS)

    # Consider all grades as D
    bhs_df.loc[:, GRADE] = GRADE_D

    # Check if it is grade B
    is_greater_than_c_1st = bhs_df.loc[:, BHS_FIRST_THRESHOLD] > BHS_GRADE_C_1ST_LIMIT
    is_greater_than_c_2nd = bhs_df.loc[:, BHS_SECOND_THRESHOLD] > BHS_GRADE_C_2ND_LIMIT
    is_greater_than_c_3rd = bhs_df.loc[:, BHS_THIRD_THRESHOLD] > BHS_GRADE_C_3RD_LIMIT

    is_grade_c = is_greater_than_c_frst & is_greater_than_c_scnd & is_greater_than_c_third

    bhs_df.loc[is_grade_c, GRADE] = GRADE_C

    # Check if it is grade B
    is_greater_than_b_1st = bhs_df.loc[:, BHS_FIRST_THRESHOLD] > BHS_GRADE_B_1ST_LIMIT
    is_greater_than_b_2nd = bhs_df.loc[:, BHS_SECOND_THRESHOLD] > BHS_GRADE_B_2ND_LIMIT
    is_greater_than_b_3rd = bhs_df.loc[:, BHS_THIRD_THRESHOLD] > BHS_GRADE_B_3RD_LIMIT

    is_grade_b = is_greater_than_b_frst & is_greater_than_b_scnd & is_greater_than_b_third

    bhs_df.loc[is_grade_b, GRADE] = GRADE_B

    # Check if it is grade A
    is_greater_than_c_1st = bhs_df.loc[:, BHS_FIRST_THRESHOLD] > BHS_GRADE_A_1ST_LIMIT
    is_greater_than_c_2nd = bhs_df.loc[:, BHS_SECOND_THRESHOLD] > BHS_GRADE_A_2ND_LIMIT
    is_greater_than_c_3rd = bhs_df.loc[:, BHS_THIRD_THRESHOLD] > BHS_GRADE_A_3RD_LIMIT

    is_grade_a = is_greater_than_a_frst & is_greater_than_a_scnd & is_greater_than_a_third

    bhs_df.loc[is_grade_a, GRADE] = GRADE_A

    return bhs_df


def _bhs_standard(y_true, y_pred):
    absolute_error = abs(y_true - y_pred)

    error5 = np.round(cumulative_error_percentage(absolute_error, 5), 2)
    error10 = np.round(cumulative_error_percentage(absolute_error, 10), 2)
    error15 = np.round(cumulative_error_percentage(absolute_error, 15), 2)

    return (error5, error10, error15)


def _cumulative_error_percentage(array, set_point):
    return (100*len(array[abs(array) <= set_point]))/len(array)
