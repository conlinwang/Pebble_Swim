#acc_smooth_HP.py
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

def acc_HPF( into_file_name ):
	file_name = into_file_name
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/smoothen_acc_HP"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/smoothen_acc_HP")
	acc_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/smoothen_acc_HP/Acc_HPF.png"
	
	re_sample_acc = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc/acc_LPF_5Hz.txt", "r+") # input training data

	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc_HP/smoothen_acc_HP.txt", "wb")

	line = re_sample_acc.readlines()
	length = len(line)

	alpha = 0.76
	acc_t = np.zeros(len(line))
	acc_x_HP = np.zeros(len(line))
	acc_y_HP = np.zeros(len(line))
	acc_z_HP = np.zeros(len(line))
	acc_N_HP = np.zeros(len(line))

	# Initialize acc x, y, z
	element_init = line[0].split(",")
	acc_t[0] = int(element_init[0])
	acc_x_HP[0] = float(element_init[1])
	acc_y_HP[0] = float(element_init[2])
	acc_z_HP[0] = float(element_init[3])
	acc_N_HP[0] = float(element_init[4])


	for index in range(1, len(line), 1):
		element = line[index].split(",")
		element02 = line[index-1].split(",")
		acc_t[index] = int(element[0])
		acc_x_HP[index] = alpha * acc_x_HP[index-1] + alpha*( float(element[1]) -  float(element02[1]) )
		acc_y_HP[index] = alpha * acc_y_HP[index-1] + alpha*( float(element[2]) -  float(element02[2]) )
		acc_z_HP[index] = alpha * acc_z_HP[index-1] + alpha*( float(element[3]) -  float(element02[3]) )
		acc_N_HP[index] = alpha * acc_N_HP[index-1] + alpha*( float(element[4]) -  float(element02[4]) )
		file_write_to.write( str(int(acc_t[index]))+","+str(acc_x_HP[index])+","+str(acc_y_HP[index])+","+str(acc_z_HP[index])+","+str(acc_N_HP[index]) +"\n")

	

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_X_HP')
	lns1 = ax.plot(acc_t, acc_x_HP, lw=2, color='green', label = 'acc_x_HP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_Y_HP')
	lns1 = ax.plot(acc_t, acc_y_HP, lw=2, color='purple', label = 'acc_y_HP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")


	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_Z_HP')
	lns1 = ax.plot(acc_t, acc_z_HP, lw=2, color='black', label = 'acc_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(414, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('acc_N_HP')
	lns1 = ax.plot(acc_t, acc_N_HP, lw=2, color='red', label = 'acc_N_HP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig.savefig(acc_xyz_file_root)
	plt.close(fig)

acc_HPF("20151105_111648_Foot_Walk_Dangle_Hsuanchao_Sony_200_0")

