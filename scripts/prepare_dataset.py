import mat73
import numpy as np
import pandas as pd

import pyCBPE.constants as consts

base_filename = "Part_"
n_of_dataset_files = 4
base_ppg_output_name = "ppg_seg_matrix_split_"
base_abp_output_name = "abp_seg_matrix_split_"

def main():
    sampling_freq = 125 # in hz
    segment_time = 5 # in seconds

    for p in range(n_of_dataset_files):
        dataset_index = consts.ORIGINAL_DATASET_PREFIX + str(p + 1)
        dataset_path = consts.ROOT_PATH + consts.DATASET_PATH + dataset_index + consts.MAT_SUFIX
        print("Carregando dataset " + dataset_index)
        data_dict = mat73.loadmat(dataset_path)

        n_of_recordings = len(data_dict[dataset_index])
        segment_samples = segment_time * sampling_freq

        samples_index = np.linspace(0, segment_samples, num=segment_samples, endpoint=False)
        samples_index = samples_index.astype(int)

        ppg_seg_df = pd.DataFrame(columns=samples_index)
        abp_seg_df = pd.DataFrame(columns=samples_index)

        for i in range(n_of_recordings):
            print("Record number " + str(i))
            ppg_recording = data_dict[dataset_index][i][0]
            abp_recording = data_dict[dataset_index][i][1]

            n_of_samples = len(ppg_recording)
            n_of_segments = int(n_of_samples / segment_samples)

            for k in range(n_of_segments):
                ppg_segment = ppg_recording[k * segment_samples: (k + 1) * segment_samples]
                abp_segment = abp_recording[k * segment_samples: (k + 1) * segment_samples]

                ppg_seg_series = pd.Series(ppg_segment)
                abp_seg_series = pd.Series(abp_segment)

                ppg_seg_df = ppg_seg_df.append(ppg_seg_series, ignore_index=True)
                abp_seg_df = abp_seg_df.append(abp_seg_series, ignore_index=True)

        # Exportar os dataframes
        ppg_seg_df_path = consts.ROOT_PATH + consts.DATASET_PATH + consts.PPG_DF_PREFIX + str(p + 1) + ".csv"
        abp_seg_df_path = consts.ROOT_PATH + consts.DATASET_PATH + consts.ABP_DF_PREFIX + str(p + 1) + ".csv"
        ppg_seg_df.to_csv(ppg_seg_df_path, index=False)
        abp_seg_df.to_csv(abp_seg_df_path, index=False)


if __name__ == "__main__":
    main()