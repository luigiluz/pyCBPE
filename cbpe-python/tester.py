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

SYS_PEAK = "systolic peak"
MAX_SLP = "max slope"
DIAS_PEAK = "diastolic peak"
DIC_NOTCH = "dicrotic notch"
INFL_POINT = "inflection point"

ROOT_PATH = "/home/lfml-cesar/Documents/UACSA/cbpe-python"

def main():
    print("####### Tester module #######")
    ppg_seg = np.genfromtxt(ROOT_PATH + '/files/ppg_seg.csv', delimiter=',')
    abp_seg = np.genfromtxt(ROOT_PATH + '/files/abp_seg.csv', delimiter=',')

    sampling_freq = 125
    t = np.arange(0, len(ppg_seg)/sampling_freq, 1/sampling_freq)

    print("### Run preprocessing ###")
    preprocessed_ppg = preprocessing.preprocess(ppg_seg)
    t_pp = np.arange(0, len(preprocessed_ppg)/(4*sampling_freq), 1/(4*sampling_freq))

    print("### Run normalization ###")
    normalized_ppg_pulse = normalization.normalize(preprocessed_ppg)
    t_norm = np.arange(0, len(normalized_ppg_pulse)/(4*sampling_freq), 1/(4*sampling_freq))

    print("### Run key_points ###")
    key_points_loc = key_points.extract(normalized_ppg_pulse)

    print("key_points_loc:")
    print(key_points_loc)

    print("### Run features ###")
    features_list = features.extract(sampling_freq, ppg_seg, normalized_ppg_pulse, key_points_loc)
    print("features")
    print(features_list)

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    ax1.plot(t, ppg_seg)
    ax1.set_xlabel('Tempo (seg)')
    ax1.set_title('Sinal puro')

    ax2.plot(t_pp, preprocessed_ppg)
    ax2.set_xlabel('Tempo (seg)')
    ax2.set_title('Sinal preprocessado')
    plt.show()

    plt.plot(t_norm, normalized_ppg_pulse)
    plt.plot(t_norm[key_points_loc[SYS_PEAK]], normalized_ppg_pulse[key_points_loc[SYS_PEAK]], marker='o')
    plt.annotate("Systolic peak", xy=(t_norm[key_points_loc[SYS_PEAK]], normalized_ppg_pulse[key_points_loc[SYS_PEAK]]))

    plt.plot(t_norm[key_points_loc[MAX_SLP]], normalized_ppg_pulse[key_points_loc[MAX_SLP]], marker='o', label='Max slope')
    plt.annotate("Max slope", xy=(t_norm[key_points_loc[MAX_SLP]], normalized_ppg_pulse[key_points_loc[MAX_SLP]]))

    plt.plot(t_norm[key_points_loc[DIAS_PEAK]], normalized_ppg_pulse[key_points_loc[DIAS_PEAK]], marker='o', label='Diastolic peak')
    plt.annotate("Diastolic peak", xy=(t_norm[key_points_loc[DIAS_PEAK]], normalized_ppg_pulse[key_points_loc[DIAS_PEAK]]))

    plt.plot(t_norm[key_points_loc[INFL_POINT]], normalized_ppg_pulse[key_points_loc[INFL_POINT]], marker='o', label='Inflection point')
    plt.annotate("Inflection point", xy=(t_norm[key_points_loc[INFL_POINT]], normalized_ppg_pulse[key_points_loc[INFL_POINT]]))

    plt.plot(t_norm[key_points_loc[DIC_NOTCH]], normalized_ppg_pulse[key_points_loc[DIC_NOTCH]], marker='o', label='Dicrotic notch')
    plt.annotate("Dicrotic notch", xy=(t_norm[key_points_loc[DIC_NOTCH]], normalized_ppg_pulse[key_points_loc[DIC_NOTCH]]))

    plt.show()


if __name__ == "__main__":
    main()