""" This is the main package, this is the entry point for the project. """

# Libraries
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# Package modules
import preprocessing
import normalization
import key_points
import features
import labels
import constants as consts


def main():
    """
    This is the main script, everytime make is run it runs this script,
    so just insert your commands here.
    """
    print("Continuous Blood Pressure Estimation Framework")

    print("Loading datasets...")
    load_start_time = time.time()
    ppg_matrix_df = pd.read_csv(consts.ROOT_PATH + consts.PPG_SEG_MATRIX_01, header=None)
    abp_matrix_df = pd.read_csv(consts.ROOT_PATH + consts.ABP_SEG_MATRIX_01, header=None)
    load_stop_time = time.time()
    load_time_in_sec = load_stop_time - load_start_time
    load_time_in_min = load_time_in_sec / 60
    print("Datasets successfully loaded!")
    print("Time taken loading datasets: ")
    print(load_time_in_min)

    # Create dataframe to store features and labels
    features_and_labels_df = pd.DataFrame(columns=consts.FEATURES_AND_LABELS_COLUMNS)

    execution_time = np.zeros(100)

    # Beginning of for loop
    for segment_index in np.arange(0, execution_time.size):
    #for segment_index in ppg_matrix_df.columns:
        process_start_time = time.time()
        print("Current segment index:")
        print(segment_index)
        ppg_seg = ppg_matrix_df.loc[:, segment_index].to_numpy()
        abp_seg = abp_matrix_df.loc[:, segment_index].to_numpy()

        print("Running preprocessing module...")
        preprocessed_ppg = preprocessing.preprocess(ppg_seg)

        print("Running normalization module...")
        normalized_ppg_pulse = normalization.normalize(preprocessed_ppg)

        print("Running key points module...")
        key_points_loc = key_points.extract(normalized_ppg_pulse)

        print("Running features module...")
        features_list = features.extract(consts.SAMPLING_FREQ, ppg_seg, normalized_ppg_pulse, key_points_loc)

        print("Running labels module...")
        labels_list = labels.extract(abp_seg)

        to_append = []
        to_append.extend(features_list)
        to_append.extend(labels_list)
        pd_series_to_append = pd.Series(to_append, index=features_and_labels_df.columns)
        features_and_labels_df = features_and_labels_df.append(pd_series_to_append, ignore_index=True)
        process_stop_time = time.time()
        execution_time[segment_index] = process_stop_time - process_start_time
    # End of for loop

    # Export dataframe as a csv file
    print("execution_time")
    print(execution_time)

    print("mean_execution_time")
    print(np.mean(execution_time))

    plt.stem(execution_time)
    plt.xlabel("Iteracoes")
    plt.ylabel("Tempo (segundos)")
    plt.show()

    # features_and_labels_df.to_csv(consts.ROOT_PATH + consts.OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
