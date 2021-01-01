""" This is the module responsible for testing the functionalities
of cbpe-python package. """

# Python libraries
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

# Package modules
import preprocessing
import normalization
import key_points
import features
import labels
import constants as consts


ROOT_PATH = "/home/lfml-cesar/Documents/UACSA/cbpe-python"

def main():
    print("####### Tester module #######")
    ppg_seg = np.genfromtxt(consts.ROOT_PATH + consts.PPG_SEG_PATH, delimiter=',')
    abp_seg = np.genfromtxt(consts.ROOT_PATH + consts.ABP_SEG_PATH, delimiter=',')

    t = np.arange(0, len(ppg_seg)/consts.SAMPLING_FREQ, 1/consts.SAMPLING_FREQ)

    print("### Run preprocessing ###")
    preprocessed_ppg = preprocessing.preprocess(ppg_seg)
    t_pp = np.arange(0, len(preprocessed_ppg)/(4*consts.SAMPLING_FREQ), 1/(4*consts.SAMPLING_FREQ))

    print("### Run normalization ###")
    normalized_ppg_pulse = normalization.normalize(preprocessed_ppg)
    t_norm = np.arange(0, len(normalized_ppg_pulse)/(4*consts.SAMPLING_FREQ), 1/(4*consts.SAMPLING_FREQ))

    print("### Run key_points ###")
    key_points_loc = key_points.extract(normalized_ppg_pulse)

    print("key_points_loc:")
    print(key_points_loc)

    print("### Run features ###")
    features_list = features.extract(consts.SAMPLING_FREQ, ppg_seg, normalized_ppg_pulse, key_points_loc)
    print("features")
    print(features_list)

    print("### Run labels ###")
    labels_list = labels.extract(abp_seg)
    print("labels")
    print(labels_list)

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    ax1.plot(t, ppg_seg)
    ax1.set_xlabel('Tempo (seg)')
    ax1.set_title('Sinal puro')

    ax2.plot(t_pp, preprocessed_ppg)
    ax2.set_xlabel('Tempo (seg)')
    ax2.set_title('Sinal preprocessado')
    plt.show()

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