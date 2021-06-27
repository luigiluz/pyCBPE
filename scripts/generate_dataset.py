""" This script is responsible for generation the features and labels used
in pyCBPE framework. """

# Libraries
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Package modules
import pyCBPE.preprocessing
import pyCBPE.normalization
import pyCBPE.key_points
import pyCBPE.features
import pyCBPE.labels
import pyCBPE.constants as consts


def main():
    """
    This is the main script, everytime make is run it runs this script,
    so just insert your commands here.
    """
    print("##### pyCBPE Framework #####")
    print("### Dataset generator script ###")

    print("Loading datasets...")
    load_start_time = time.time()
    ppg_matrix_df = pd.read_csv(consts.ROOT_PATH + consts.PPG_SEG_MATRIX, header=None)
    abp_matrix_df = pd.read_csv(consts.ROOT_PATH + consts.ABP_SEG_MATRIX, header=None)
    load_stop_time = time.time()
    load_time_in_sec = load_stop_time - load_start_time
    load_time_in_min = load_time_in_sec / 60
    print("Datasets successfully loaded!")
    print("Time taken loading datasets: ")
    print(load_time_in_min)

    # Create dataframe to store features and labels
    features_and_labels_df = pd.DataFrame(columns=consts.FEATURES_AND_LABELS_COLUMNS)

    # Beginning of for loop
    total_execution_start_time = time.time()
    for segment_index in ppg_matrix_df.columns:
        print("Current segment index:")
        print(segment_index)
        ppg_seg = ppg_matrix_df.loc[:, segment_index].to_numpy()
        abp_seg = abp_matrix_df.loc[:, segment_index].to_numpy()

        print("Running preprocessing module...")
        preprocessed_ppg = pyCBPE.preprocessing.preprocess(ppg_seg)

        print("Running normalization module...")
        normalized_ppg_pulse = pyCBPE.normalization.normalize(preprocessed_ppg)

        print("Running key points module...")
        key_points_loc = pyCBPE.key_points.extract(normalized_ppg_pulse)

        print("Running features module...")
        features_list = pyCBPE.features.extract(consts.SAMPLING_FREQ, ppg_seg, normalized_ppg_pulse, key_points_loc)

        print("Running labels module...")
        labels_list = pyCBPE.labels.extract(abp_seg)

        to_append = []
        to_append.extend(features_list)
        to_append.extend(labels_list)
        pd_series_to_append = pd.Series(to_append, index=features_and_labels_df.columns)
        features_and_labels_df = features_and_labels_df.append(pd_series_to_append, ignore_index=True)
    # End of for loop
    total_execution_stop_time = time.time()
    total_execution_time_sec = total_execution_stop_time - total_execution_start_time
    total_execution_time_min = total_execution_time_sec / 60

    print("Total execution time was:")
    print(total_execution_time_min)
    print("minutes.")

    # Export dataframe as a csv file
    features_and_labels_df.to_csv(consts.ROOT_PATH + consts.OUTPUT_PATH, index=False)
    print("Features and labels dataframe successfully exported.")


if __name__ == "__main__":
    main()
