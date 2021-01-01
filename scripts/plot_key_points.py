""" This script is responsible for plotting the key points in a normalized
ppg pulse. """

# Python libraries
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

# Package modules
import pyCBPE.preprocessing
import pyCBPE.normalization
import pyCBPE.key_points
import pyCBPE.features
import pyCBPE.labels
import pyCBPE.constants as consts

def main():
    print("##### pyCBPE Framework #####")
    print("### Plot key points script")
    ppg_seg = np.genfromtxt(consts.ROOT_PATH + consts.PPG_SEG_PATH, delimiter=',')
    abp_seg = np.genfromtxt(consts.ROOT_PATH + consts.ABP_SEG_PATH, delimiter=',')

    t = np.arange(0, len(ppg_seg)/consts.SAMPLING_FREQ, 1/consts.SAMPLING_FREQ)

    print("### Run preprocessing ###")
    preprocessed_ppg = pyCBPE.preprocessing.preprocess(ppg_seg)
    t_pp = np.arange(0, len(preprocessed_ppg)/(4*consts.SAMPLING_FREQ), 1/(4*consts.SAMPLING_FREQ))

    print("### Run normalization ###")
    normalized_ppg_pulse = pyCBPE.normalization.normalize(preprocessed_ppg)
    t_norm = np.arange(0, len(normalized_ppg_pulse)/(4*consts.SAMPLING_FREQ), 1/(4*consts.SAMPLING_FREQ))

    print("### Run key_points ###")
    key_points_loc = pyCBPE.key_points.extract(normalized_ppg_pulse)

    plt.plot(t_norm, normalized_ppg_pulse)
    plt.plot(t_norm[key_points_loc[consts.SYS_PEAK]], normalized_ppg_pulse[key_points_loc[consts.SYS_PEAK]], marker='o')
    plt.annotate("Systolic peak", xy=(t_norm[key_points_loc[consts.SYS_PEAK]], normalized_ppg_pulse[key_points_loc[consts.SYS_PEAK]]))

    plt.plot(t_norm[key_points_loc[consts.MAX_SLP]], normalized_ppg_pulse[key_points_loc[consts.MAX_SLP]], marker='o', label='Max slope')
    plt.annotate("Max slope", xy=(t_norm[key_points_loc[consts.MAX_SLP]], normalized_ppg_pulse[key_points_loc[consts.MAX_SLP]]))

    plt.plot(t_norm[key_points_loc[consts.DIAS_PEAK]], normalized_ppg_pulse[key_points_loc[consts.DIAS_PEAK]], marker='o', label='Diastolic peak')
    plt.annotate("Diastolic peak", xy=(t_norm[key_points_loc[consts.DIAS_PEAK]], normalized_ppg_pulse[key_points_loc[consts.DIAS_PEAK]]))

    plt.plot(t_norm[key_points_loc[consts.INFL_POINT]], normalized_ppg_pulse[key_points_loc[consts.INFL_POINT]], marker='o', label='Inflection point')
    plt.annotate("Inflection point", xy=(t_norm[key_points_loc[consts.INFL_POINT]], normalized_ppg_pulse[key_points_loc[consts.INFL_POINT]]))

    plt.plot(t_norm[key_points_loc[consts.DIC_NOTCH]], normalized_ppg_pulse[key_points_loc[consts.DIC_NOTCH]], marker='o', label='Dicrotic notch')
    plt.annotate("Dicrotic notch", xy=(t_norm[key_points_loc[consts.DIC_NOTCH]], normalized_ppg_pulse[key_points_loc[consts.DIC_NOTCH]]))

    plt.show()


if __name__ == "__main__":
    main()
