#acc_smooth.py
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


def acc_LPF( into_file_name ):
	file_name = into_file_name
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/smoothen_acc"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/smoothen_acc")
	acc_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/smoothen_acc/Acc_LPF_5Hz.png"
	
	re_sample_acc = open("./stroke_count_Evaluation/"+file_name+"/re_sample_acc/re_sample_acc.txt", "r+") # input training data

	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc/acc_LPF_5Hz.txt", "wb")

	line = re_sample_acc.readlines()
	length = len(line)

	alpha = 0.48
	acc_t = np.zeros(len(line))
	acc_x_LP = np.zeros(len(line))
	acc_y_LP = np.zeros(len(line))
	acc_z_LP = np.zeros(len(line))
	acc_N_LP = np.zeros(len(line))

	# Initialize acc x, y, z
	element_init = line[0].split(",")
	acc_t[0] = int(element_init[0])
	acc_x_LP[0] = float(element_init[1])
	acc_y_LP[0] = float(element_init[2])
	acc_z_LP[0] = float(element_init[3])
	acc_N_LP[0] = float(element_init[4])

	for index in range(1, len(line), 1):
		element = line[index].split(",")
		acc_t[index] = int(element[0])
		acc_x_LP[index] = alpha * ( float(element[1]) ) + (1 - alpha ) * acc_x_LP[index-1]
		acc_y_LP[index] = alpha * ( float(element[2]) ) + (1 - alpha ) * acc_y_LP[index-1]
		acc_z_LP[index] = alpha * ( float(element[3]) ) + (1 - alpha ) * acc_z_LP[index-1]
		acc_N_LP[index] = alpha * ( float(element[4]) ) + (1 - alpha ) * acc_N_LP[index-1]
		file_write_to.write( str(int(acc_t[index]))+","+str(acc_x_LP[index])+","+str(acc_y_LP[index])+","+str(acc_z_LP[index])+","+str(acc_N_LP[index]) +"\n")

	# 5 points moving average
	for index in range(2, len(line)-2, 1):
		acc_x_LP[index] = (acc_x_LP[index] + acc_x_LP[index+1] + acc_x_LP[index+2] + acc_x_LP[index-1] + acc_x_LP[index-2]) / 5
		acc_y_LP[index] = (acc_y_LP[index] + acc_y_LP[index+1] + acc_y_LP[index+2] + acc_y_LP[index-1] + acc_y_LP[index-2]) / 5
		acc_x_LP[index] = (acc_x_LP[index] + acc_x_LP[index+1] + acc_z_LP[index+2] + acc_z_LP[index-1] + acc_z_LP[index-2]) / 5
		acc_x_LP[index] = (acc_x_LP[index] + acc_x_LP[index+1] + acc_x_LP[index+2] + acc_x_LP[index-1] + acc_x_LP[index-2]) / 5


	re_sample_acc.close()

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,180000), ylim=(-20,5))
	ax.set_title('Acc_X_HP')
	lns1 = ax.plot(acc_t, acc_x_LP, lw=2, color='green', label = 'acc_x_HP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,180000), ylim=(-10,5))
	ax.set_title('Acc_Y_HP')
	lns1 = ax.plot(acc_t, acc_y_LP, lw=2, color='purple', label = 'acc_y_LP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")


	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_Z_HP')
	lns1 = ax.plot(acc_t, acc_z_LP, lw=2, color='black', label = 'acc_z_HP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(414, autoscale_on=False, xlim=(0,180000), ylim=(5,18))
	ax.set_title('Acc_N_HP')
	lns1 = ax.plot(acc_t, acc_N_LP, lw=2, color='red', label = 'acc_N_LP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig.savefig(acc_xyz_file_root)
	plt.close(fig)

acc_LPF("20151105_111648_Foot_Walk_Dangle_Hsuanchao_Sony_200_0")