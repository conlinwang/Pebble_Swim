from sklearn import linear_model
import numpy as np
import os
import math

from pylab import *
from matplotlib.pyplot import figure, show
from matplotlib.patches import Ellipse
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost

from matplotlib import rc

#data
#---------------------------------------------------------------


file_name = '0627_183021_NTUST.LG_FCS_16_16_100m'
re_sample_acc = open("./"+file_name+"/re_sample_acc/re_sample_acc.txt", "r+") # input training data for acc
re_sample_gyro = open("./"+file_name+"/re_sample_gyro/re_sample_gyro.txt", "r+") # input training data for gyro

line = re_sample_acc.readlines() # read acc re_sample_acc.txt
line_gyro = re_sample_gyro.readlines() # read gyro re_sample_gyro.txt
length = len(line)
length_g = len(line_gyro)
alpha = 0.1
LPF_list = []
LPF_array = [0, 0, 0, 0, 0, 0]

element  = line[0].split(",")
element2 = element[5].split("\n")
LPF_array[0] = int(element[0])
LPF_array[1] = float(element[1])
LPF_array[2] = float(element[2])
LPF_array[3] = float(element[3])
LPF_array[4] = float(element[4])
LPF_array[5] = float(element2[0])
LPF_list.append(str(LPF_array))

for index in range(1, len(line), 1):
    element0  = line[index-1].split(",")
    element02 = element0[5].split("\n")
    pre_acc_x = float(element0[1])
    pre_acc_y = float(element0[2])
    pre_acc_z = float(element0[3])
    pre_acc_N = float(element0[4])
    pre_acc_xy = float(element02[0])
    
    element  = line[index].split(",")
    element03 = element[5].split("\n")
    LPF_array[0] = int(element[0])
    LPF_array[1] = alpha * float(element[1]) + (1-alpha) * pre_acc_x
    LPF_array[2] = alpha * float(element[2]) + (1-alpha) * pre_acc_y
    LPF_array[3] = alpha * float(element[3]) + (1-alpha) * pre_acc_z
    LPF_array[4] = alpha * float(element[4]) + (1-alpha) * pre_acc_N
    LPF_array[5] = alpha * float(element03[0]) + (1-alpha) * pre_acc_xy
    LPF_list.append(str(LPF_array))

smoothen_list = []
smoothen_array = [0, 0, 0, 0, 0, 0]
for index in range(2, length-2, 1):
    element  = LPF_list[index].split(",")
    element_1 = element[0].split("[")
    element_2 = element[5].split("]")

    element2 = LPF_list[index+1].split(",")
    element2_2 = element2[5].split("]")

    element3 = LPF_list[index-1].split(",")
    element3_2 = element3[5].split("]")

    element4 = LPF_list[index+2].split(",")
    element4_2 = element4[5].split("]")

    element5 = LPF_list[index-2].split(",")
    element5_2 = element5[5].split("]")

    smoothen_array[0] = int(element_1[1])
    smoothen_array[1] = (float(element[1])   + float(element2[1]) + float(element3[1]) + float(element4[1]) + float(element4[1])) / 5
    smoothen_array[2] = (float(element[2])   + float(element2[2]) + float(element3[2]) + float(element4[2]) + float(element4[2])) / 5
    smoothen_array[3] = (float(element[3])   + float(element2[3]) + float(element3[3]) + float(element4[3]) + float(element4[3])) / 5
    smoothen_array[4] = (float(element[4])   + float(element2[4]) + float(element3[4]) + float(element4[4]) + float(element4[4])) / 5
    smoothen_array[5] = (float(element_2[0]) + float(element2_2[0]) + float(element3_2[0]) + float(element4_2[0]) + float(element5_2[0])) / 5
    smoothen_list.append(str(smoothen_array))

smoothen_list_gyro = []
smoothen_array_gyro = [0, 0, 0, 0]
for index in range(2, length_g-2, 1):
    element  = line_gyro[index].split(",")
    element2 = line_gyro[index+1].split(",")
    element3 = line_gyro[index-1].split(",")
    element4 = line_gyro[index+2].split(",")
    element5 = line_gyro[index-2].split(",")
    smoothen_array_gyro[0] = int(element[0])
    smoothen_array_gyro[1] = (float(element[1]) + float(element2[1]) + float(element3[1]) + float(element4[1]) + float(element4[1])) / 5
    smoothen_array_gyro[2] = (float(element[2]) + float(element2[2]) + float(element3[2]) + float(element4[2]) + float(element4[2])) / 5
    smoothen_array_gyro[3] = (float(element[3]) + float(element2[3]) + float(element3[3]) + float(element4[3]) + float(element4[3])) / 5
    smoothen_list_gyro.append(str(smoothen_array_gyro))



acc_t = []
acc_x = []
acc_y = []
acc_z = []
acc_N = []
acc_xy = []
for index in range(0, len(smoothen_list), 1):
	element = smoothen_list[index].split(",")
	element0 = element[0].split("[")
	element1 = element[5].split("]")
	acc_t.append(int(element0[1]))
	acc_x.append(float(element[1]))
	acc_y.append(float(element[2]))
	acc_z.append(float(element[3]))
	acc_N.append(float(element[4]))
	acc_xy.append(float(element1[0]))



#---------------------------------------------------------------
#data end
rc('mathtext', default='regular')



fig = figure(1,figsize=(60,15))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(0,100000), ylim=(-35,30))

lns1 = ax.plot(acc_t, acc_x, '-', label = 'acc_x', lw=3)
lns2 = ax.plot(acc_t, acc_y, '-', label = 'acc_y')
lns3 = ax.plot(acc_t, acc_z, '-', label = 'acc_z')
lns4 = ax.plot(acc_t, acc_N, '-', label = 'acc_N')
lns5 = ax.plot(acc_t, acc_xy, '-', label = 'acc_xy')


# added these three lines
lns = lns1+lns2+lns3+lns4+lns5
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
ax.set_xlabel("Time (msec)")
ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
ax.set_ylim(-30,30)

plt.show()