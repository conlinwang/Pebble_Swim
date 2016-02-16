#acc_stroke_count.py

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

def stroke_count( into_file_name ):
	file_name = into_file_name

	if not os.path.exists("./"+file_name+"/stroke_count"):
		os.mkdir("./"+file_name+"/stroke_count")   

	input_acc_data = open("./"+file_name+"/acc_cut/acc_LPF_5Hz.txt", "r+") # input_acc_data
	input_gyro_data = open("./"+file_name+"/gyro_cut/smoothen_gyro.txt", "r+") # input_acc_data

	stroke_count_file_root = "./"+file_name+"/stroke_count/stroke_count.png"
	
	acc_data = input_acc_data.readlines() # load data into python
	gyro_data = input_gyro_data.readlines()

	acc_length = len(acc_data)    # get how many data had being loaded 
	gyro_length = len(gyro_data)

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

# stroke count for acc_xy ----------------------------


	initial_Threshold = 15
	down_grade_ratio = 0.75
	SC_indicator = 0
	peak_point_xy = [0, 0]
	pre_peak_point_xy = [0, 0]
	peak_point_list_xy = []
	for index in range(1, len(acc_data)-1, 1):
		
		element0 = acc_data[index-1].split(",")
		element1 = acc_data[index].split(",")
		element2 = acc_data[index+1].split(",")

		element0_1 = element0[5].split("\n")
		element1_1 = element1[5].split("\n")
		element2_1 = element2[5].split("\n")
		
		acc_xy_pre = element0_1[0]
		acc_xy_now = element1_1[0]
		acc_xy_next = element2_1[0]
		
		if (SC_indicator == 0):
			if( (float(acc_xy_now) > initial_Threshold) or (float(acc_xy_next) > initial_Threshold) ):
				if((float(acc_xy_next) - float(acc_xy_now) < 0) & (float(acc_xy_now) - float(acc_xy_pre) > 0)): 
					max_in_twenty_sample = float(acc_xy_now)
					for index2 in range(1, 21, 1):
						element_f = acc_data[index+index2].split(",")
						element_f_1 = element_f[5].split("\n")
						acc_xy_future = element_f_1[0]
						if(float(acc_xy_future) > max_in_twenty_sample):
							max_in_ten_sample = acc_xy_future 
					SC_indicator = SC_indicator + 1
					print acc_xy_now, acc_xy_next
					peak_point_xy[0] = int(element1[0])
					peak_point_xy[1] = float(acc_xy_now)
					peak_point_list_xy.append(str(peak_point_xy))
					pre_peak_point_xy[0] = peak_point_xy[0]
					pre_peak_point_xy[1] = peak_point_xy[1]
					print SC_indicator
					print initial_Threshold

		elif (SC_indicator > 0):
			if( (float(acc_xy_now) > FCS_Threshold) or (float(acc_xy_next) > FCS_Threshold) ):
				if((float(acc_xy_next) - float(acc_xy_now) < 0) & (float(acc_xy_now) - float(acc_xy_pre) > 0)): 
					if( (int(element1[0]) - int(pre_peak_point_xy[0]) > 1500) & (int(element1[0]) - int(pre_peak_point_xy[0]) < 15000) ):
						SC_indicator = SC_indicator + 1
						peak_point_xy[0] = int(element1[0])
						peak_point_xy[1] = float(acc_xy_now)
						peak_point_list_xy.append(str(peak_point_xy))
						pre_peak_point_xy[0] = peak_point_xy[0]
						pre_peak_point_xy[1] = peak_point_xy[1]
						print SC_indicator
						print FCS_Threshold

		if (SC_indicator == 1):
			element = peak_point_list_xy[0].split(",")
			element1 = element[1].split("]")
			FCS_Threshold = float(element1[0]) * down_grade_ratio
		elif (SC_indicator == 2):
			element = peak_point_list_xy[0].split(",")
			element1 = element[1].split("]")
			element_1 = peak_point_list_xy[1].split(",")
			element_11 = element[1].split("]")
			FCS_Threshold = (float(element1[0]) + float(element_11[0])) /2 * down_grade_ratio
		elif (SC_indicator >= 3):
			FCS_Threshold = 0
			for index in range(len(peak_point_list_xy)-3, len(peak_point_list_xy), 1):
				element = peak_point_list_xy[index].split(",")
				element1 = element[1].split("]")
				FCS_Threshold = FCS_Threshold + float(element1[0])

			FCS_Threshold = float(FCS_Threshold) / 3 * down_grade_ratio




	print len(peak_point_list_xy)
	stroke_time_interval = 0
	for index in range(1, len(peak_point_list_xy), 1):
		element = peak_point_list_xy[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[1].split("]")

		element1 = peak_point_list_xy[index-1].split(",")
		element1_1 = element1[0].split("[")
		element1_2 = element1[1].split("]")
		
		stroke_time_interval = stroke_time_interval + ( int(element_1[1]) - int(element1_1[1]))

	# print float(stroke_time_interval) / (len(peak_point_list_xy) -1)

	for index in range(0, len(peak_point_list_xy), 1):
		print peak_point_list_xy[index]

# END of stroke count for acc_xy ----------------------------------------------------------------------------------------------------------




	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(511, autoscale_on=False, xlim=(0,180000), ylim=(-40,35))
	ax.set_title('Acc_X')
	lns1 = ax.plot(acc_t, acc_x, lw=2, color='green', label = 'acc_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(512, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_y, lw=2, color='purple', label = 'acc_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(513, autoscale_on=False, xlim=(0,180000), ylim=(-40,40))
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_z, lw=2, color='black', label = 'acc_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(514, autoscale_on=False, xlim=(0,180000), ylim=(0,50))
	ax.set_title('Acc_N')
	lns1 = ax.plot(acc_t, acc_N, lw=2, color='red', label = 'acc_N')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(515, autoscale_on=False, xlim=(0,180000), ylim=(0,50))
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_xy, lw=2, color='blue', label = 'acc_xy')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	for index in range(0, SC_indicator ,1):
		element = peak_point_list_xy[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[1].split("]")
		ax.annotate('SC '+ str(index+1), xy=(element_1[1], element_2[0]),  xycoords='data', color='magenta',
			xytext=(50, 30), textcoords='offset points',
			arrowprops=dict(arrowstyle="->",
				connectionstyle="angle3,angleA=0,angleB=-90"),
			)
	fig.savefig(stroke_count_file_root)


	# show()
	plt.close(fig)





