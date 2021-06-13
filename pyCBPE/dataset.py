""" This is the package responsible for realizing the data handling process
for features and labels previously generated. """

import pandas as pd
import numpy as np
import pyCBPE.constants as consts

def load():
    """ Load dataset from filepat and return it as a pandas dataframe. """
    df_split_1 = pd.read_csv(consts.FEATURES_AND_LABELS_DF_SPLIT_1_PATH, index_col=False, header=0)
    df_split_2 = pd.read_csv(consts.FEATURES_AND_LABELS_DF_SPLIT_2_PATH, index_col=False, header=0)
    df_split_3 = pd.read_csv(consts.FEATURES_AND_LABELS_DF_SPLIT_3_PATH, index_col=False, header=0)
    df_split_4 = pd.read_csv(consts.FEATURES_AND_LABELS_DF_SPLIT_4_PATH, index_col=False, header=0)

    dataframe = pd.concat([df_split_1, df_split_2, df_split_3, df_split_4])

    return dataframe.reset_index(drop=True)


def handle(dataframe):
    """ Handle dataset values by dropping values that are not going to be
    used. """
    handled_df = dataframe.copy()

    handled_df = handled_df.replace(-1, np.nan) # TO DO: Change -1 to a constant in constants.py
    handled_df = handled_df.replace([np.inf , -np.inf], np.nan)
    handled_df = handled_df.dropna()

    handled_df[consts.HEART_RATE] = handled_df[consts.HEART_RATE].astype(int)
    handled_df[consts.LABELS_COLUMNS] = handled_df[consts.LABELS_COLUMNS].astype(int)

    return handled_df.reset_index(drop=True)


def remove_outliers(dataframe):
    """ Remove outliers based on labels values. """
    temp_df = dataframe.copy()

    labels_df = temp_df[consts.LABELS_COLUMNS]

    summary_df = pd.DataFrame(labels_df.describe())

    sbp_min = summary_df.loc["min", consts.SBP]
    sbp_max = summary_df.loc["max", consts.SBP]
    dbp_min = summary_df.loc["min", consts.DBP]
    dbp_max = summary_df.loc["max", consts.DBP]
    map_min = summary_df.loc["min", consts.MAP]
    map_max = summary_df.loc["max", consts.MAP]

    sbp_condition = (temp_df.loc[:, consts.SBP] > sbp_min) & (temp_df.loc[:, consts.SBP] < sbp_max)
    dbp_condition = (temp_df.loc[:, consts.DBP] > dbp_min) & (temp_df.loc[:, consts.DBP] < dbp_max)
    map_condition = (temp_df.loc[:, consts.MAP] > map_min) & (temp_df.loc[:, consts.MAP] < map_max)

    outlier_free_df = temp_df.loc[sbp_condition & dbp_condition & map_condition, :]

    return outlier_free_df.reset_index(drop=True)


def get_features_as_array(dataframe):
    """ Get features columns from dataframe as a numpy array."""
    features_dataframe = dataframe.drop(consts.LABELS_COLUMNS, axis=1)
    features_array = np.array(features_dataframe)

    return features_array


def get_labels_as_array(dataframe):
    """ Get labels columns from dataframe as a numpy array."""
    labels_dataframe = dataframe[consts.LABELS_COLUMNS]
    labels_array = np.array(labels_dataframe)

    return labels_array
