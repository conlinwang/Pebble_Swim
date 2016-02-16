#dev_peak_dep.py

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


def peak( into_file_name ):
	file_name = into_file_name

	if not os.path.exists("./"+file_name+"/stroke_count"):
		os.mkdir("./"+file_name+"/stroke_count")   

	input_acc_data = open("./"+file_name+"/smoothen_acc/acc_LPF_5Hz.txt", "r+") # input_acc_data
	input_gyro_data = open("./"+file_name+"/smoothen_gyro/smoothen_gyro.txt", "r+") # input_acc_data

	stroke_count_file_root = "./"+file_name+"/stroke_count/peak_dip.png"
	
	acc_data = input_acc_data.readlines() # load data into python
	gyro_data = input_gyro_data.readlines()

	acc_length = len(acc_data)    # get how many data had being loaded 
	gyro_length = len(gyro_data)

	print acc_length

	acc_t = []
	acc_x = []
	acc_y = []
	acc_z = []
	acc_N = []
	acc_xy = []
	for index in range(0, len(acc_data), 1):
		element = acc_data[index].split(",")
		element_1 = element[5].split("\n")
		acc_t.append(int(element[0]))
		acc_x.append(float(element[1]))
		acc_y.append(float(element[2]))
		acc_z.append(float(element[3]))
		acc_N.append(float(element[4]))
		acc_xy.append(float(element_1[0]))


	peak_point_xy = [0, 0]
	peak_point_xy_list = []
	for index in range(1, len(acc_data)-1, 1):
		element0 = acc_data[index-1].split(",")
		element1 = acc_data[index].split(",")
		element2 = acc_data[index+1].split(",")

		element0_1 = element0[3].split("\n")
		element1_1 = element1[3].split("\n")
		element2_1 = element2[3].split("\n")

		acc_xy_pre = element0_1[0]
		acc_xy_now = element1_1[0]
		acc_xy_next = element2_1[0]

		if(   (float(acc_xy_next) - float(acc_xy_now) < 0) & (float(acc_xy_now) - float(acc_xy_pre) > 0)  or (float(acc_xy_next) - float(acc_xy_now) > 0) & (float(acc_xy_now) - float(acc_xy_pre) < 0)  ):
			peak_point_xy[0] = int(element1[0])
			peak_point_xy[1] = float(acc_xy_now)
			peak_point_xy_list.append(str(peak_point_xy))

	peak_t = []
	peak_x = []
	for index in range(0, len(peak_point_xy_list), 1):
		element  = peak_point_xy_list[index].split(",")
		element1 = element[0].split("[")
		# print element1[1]
		element2 = element[1].split("]")
		# print element2[0]
		peak_t.append(element1[1])
		peak_x.append(element2[0])

	# print peak_t
	# print peak_x

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(511, autoscale_on=False, xlim=(0,126000), ylim=(-40,35))
	ax.set_title('Acc_X')                                 
	lns1 = ax.plot(peak_t, peak_x, lw=2, color='green', label = 'acc_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	
	fig.savefig(stroke_count_file_root)
	plt.close(fig)
	


file_for_SC = "0718_072501_BigFish_Back_XX_100m_L"
peak(file_for_SC)