from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    file_name = "0621_190929_Still_RestNorm_Wear_C_W1"

    re_sample_acc = open("./"+file_name+"/re_sample_acc/re_sample_acc.txt", "r+") # input training data
    line = re_sample_acc.readlines()
    length = len(line)
    alpha = 0.02
    LPF_list = []
    LPF_array = [0, 0, 0, 0, 0]
    
    element  = line[0].split(",")
    element2 = element[4].split("\n")
    LPF_array[0] = int(element[0])
    LPF_array[1] = float(element[1])
    LPF_array[2] = float(element[2])
    LPF_array[3] = float(element[3])
    LPF_array[4] = float(element2[0])
    LPF_list.append(str(LPF_array))

    for index in range(1, length, 1):
        element0  = line[index-1].split(",")
        element02 = element0[4].split("\n")
        pre_acc_x = float(element0[1])
        pre_acc_y = float(element0[2])
        pre_acc_z = float(element0[3])
        pre_acc_N = float(element02[0])
        element  = line[index].split(",")
        element03 = element[4].split("\n")
        LPF_array[0] = int(element[0])
        LPF_array[1] = alpha * float(element[1]) + (1-alpha) * pre_acc_x
        LPF_array[2] = alpha * float(element[2]) + (1-alpha) * pre_acc_y
        LPF_array[3] = alpha * float(element[3]) + (1-alpha) * pre_acc_z
        LPF_array[4] = alpha * float(element03[0]) + (1-alpha) * pre_acc_N
        LPF_list.append(str(LPF_array))

    smoothen_list = []
    smoothen_array = [0, 0, 0, 0, 0]
    for index in range(2, length-2, 1):
        element  = LPF_list[index].split(",")
        element_1 = element[0].split("[")
        element_2 = element[4].split("]")

        element2 = LPF_list[index+1].split(",")
        element2_2 = element2[4].split("]")

        element3 = LPF_list[index-1].split(",")
        element3_2 = element3[4].split("]")

        element4 = LPF_list[index+2].split(",")
        element4_2 = element4[4].split("]") 

        element5 = LPF_list[index-2].split(",")
        element5_2 = element5[4].split("]") 

        smoothen_array[0] = int(element_1[1])
        smoothen_array[1] = (float(element[1])   + float(element2[1]) + float(element3[1]) + float(element4[1]) + float(element4[1])) / 5
        smoothen_array[2] = (float(element[2])   + float(element2[2]) + float(element3[2]) + float(element4[2]) + float(element4[2])) / 5
        smoothen_array[3] = (float(element[3])   + float(element2[3]) + float(element3[3]) + float(element4[3]) + float(element4[3])) / 5
        smoothen_array[4] = (float(element_2[0]) + float(element2_2[0]) + float(element3_2[0]) + float(element4_2[0]) + float(element5_2[0])) / 5
        smoothen_list.append(str(smoothen_array))
    print len(smoothen_list)

    # for index0 in range(0, len(smoothen_list), 1):
    #   print smoothen_array[index0]
    acc_t = []
    acc_x = []
    acc_y = []
    acc_z = []
    acc_N = []
    for index in range(0, len(smoothen_list), 1):
        element = smoothen_list[index].split(",")
        element0 = element[0].split("[")
        element1 = element[4].split("]")
        acc_t.append(int(element0[1]))
        acc_x.append(float(element[1]))
        acc_y.append(float(element[2]))
        acc_z.append(float(element[3]))
        acc_N.append(float(element1[0]))




    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 15.0
    highcut = 25.0

    # Plot the frequency response for a few different orders.
    plt.figure(1)
    plt.clf()
    for order in [3, 6, 9]:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')

    # Filter a noisy signal.
    T = 0.05
    nsamples = T * fs
    t = np.linspace(0, T, nsamples, endpoint=False)
    a = 0.02
    f0 = 600.0
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += a * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    plt.figure(2)
    plt.clf()
    plt.plot(t, x, label='Noisy signal')

    y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
    plt.plot(acc_t, acc_N, label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()