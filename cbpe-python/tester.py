""" This is the module responsible for testing the functionalities
of cbpe-python package. """

# Python libraries
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

# Package modules
import preprocessing

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

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    ax1.plot(t, ppg_seg)
    ax1.set_xlabel('Tempo (seg)')
    ax1.set_title('Sinal puro')
    #ax1.xlabel("Tempo (seg)")
    #ax1.ylabel("PPG Amplitude")
    #ax1.show()

    ax2.plot(t_pp, preprocessed_ppg)
    ax2.set_xlabel('Tempo (seg)')
    ax2.set_title('Sinal preprocessado')
    #ax2.xlabel("Tempo (seg)")
    #ax2.ylabel("PPG Amplitude")
    #ax2.show()

    plt.show()


if __name__ == "__main__":
    main()