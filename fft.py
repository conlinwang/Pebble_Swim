from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt

file_name = "0606_144601_Tina_FCS_17_18_100m"
re_sample_acc = open("./"+file_name+"/re_sample_acc/re_sample_acc.txt", "r+") # input training data
line = re_sample_acc.readlines()
length = len(line)
alpha = 0.01
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



# Number of samplepoints
N = 3717
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(200.0 * 2.0*np.pi*x)
print len(x), len(y)

yf = fft(acc_N)
print len(yf)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

# plt.plot(x, y)
plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))

plt.grid()
plt.show()