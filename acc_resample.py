#raw_data_preprocessor.py
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

def acc_resample( into_SMAPLE_RATE, into_file_name ):
	print "file", into_file_name, "is running acc_resample"
	SMAPLE_RATE = into_SMAPLE_RATE
	file_name = into_file_name

	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/re_sample_acc"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/re_sample_acc")

	acc_raw = open("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate/acc.txt", "r+") # input training data
	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/re_sample_acc/re_sample_acc.txt", "wb")

	acc_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/re_sample_acc/acc_resample.png"
	acc_x_file_root = "./stroke_count_Evaluation/"+file_name+"/re_sample_acc/Acc_X_raw.png"
	acc_y_file_root = "./stroke_count_Evaluation/"+file_name+"/re_sample_acc/Acc_Y_raw.png"
	acc_z_file_root = "./stroke_count_Evaluation/"+file_name+"/re_sample_acc/Acc_Z_raw.png"
	acc_n_file_root = "./stroke_count_Evaluation/"+file_name+"/re_sample_acc/Acc_N_raw.png"

	line = acc_raw.readlines()
	length = len(line)

	element = line[length-1].split(",")
	total_time = int(round( float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
	print "The acc_resample_data last", total_time, "msec."

	acc_re_sample_list = []
	acc_re_sample_array = [0, 0, 0, 0, 0, 0, 0, 0, 0] # (time. X, Y, Z, N, xy, xz, yz)
	element = line[0].split(",")
	acc_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
	acc_re_sample_array[1] = element[1] # acc_x
	acc_re_sample_array[2] = element[2] # acc_y
	acc_re_sample_array[3] = element[3] # acc_z
	acc_re_sample_array[4] = element[4] # acc_N
	acc_re_sample_array[5] = element[5] # acc_xy
	acc_re_sample_array[6] = element[6] # acc_xz
	acc_re_sample_array[7] = element[7] # acc_yz
	element2 = element[8].split("\n")   # acc_zSQ
	acc_re_sample_array[8] = element2[0] # acc_zSQ
	acc_re_sample_list.append(acc_re_sample_array)


	for index in range(1, length, 1):
		acc_re_sample_array = [0, 0, 0, 0, 0, 0, 0, 0, 0] # (time. X, Y, Z, N, xy, xz, yz)
		element = line[index].split(",")
		acc_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
		acc_re_sample_array[1] = element[1] # acc_x
		acc_re_sample_array[2] = element[2] # acc_y
		acc_re_sample_array[3] = element[3] # acc_z
		acc_re_sample_array[4] = element[4] # acc_N
		acc_re_sample_array[5] = element[5] # acc_xy
		acc_re_sample_array[6] = element[6] # acc_xz
		acc_re_sample_array[7] = element[7] # acc_yz
		element2 = element[8].split("\n")   # acc_yz
		acc_re_sample_array[8] = element2[0] # acc_zSQ
		if(acc_re_sample_list[len(acc_re_sample_list)-1][0] != acc_re_sample_array[0]):
			acc_re_sample_list.append(acc_re_sample_array)

	for index in range(1, length, 1):
		acc_re_sample_array = [0, 0, 0, 0, 0, 0, 0, 0, 0] # (time. X, Y, Z, N, xy, xz, yz)
		element = line[index].split(",")
		acc_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
		acc_re_sample_array[1] = element[1] # acc_x
		acc_re_sample_array[2] = element[2] # acc_y
		acc_re_sample_array[3] = element[3] # acc_z
		acc_re_sample_array[4] = element[4] # acc_N
		acc_re_sample_array[5] = element[5] # acc_xy
		acc_re_sample_array[6] = element[6] # acc_xz
		acc_re_sample_array[7] = element[7] # acc_yz
		element2 = element[8].split("\n")   # acc_yz
		acc_re_sample_array[8] = element2[0] # acc_zSQ
		for item in range (0, len(acc_re_sample_list), 1):
			if (acc_re_sample_list[item][0] == acc_re_sample_array[0]):
				acc_re_sample_list[item][1] = acc_re_sample_array[1]
				acc_re_sample_list[item][2] = acc_re_sample_array[2]
				acc_re_sample_list[item][3] = acc_re_sample_array[3]
				acc_re_sample_list[item][4] = acc_re_sample_array[4]
				acc_re_sample_list[item][5] = acc_re_sample_array[5]
				acc_re_sample_list[item][6] = acc_re_sample_array[6]
				acc_re_sample_list[item][7] = acc_re_sample_array[7]
				acc_re_sample_list[item][8] = acc_re_sample_array[8]

	if (len(acc_re_sample_list) != int(round(float(total_time)/SMAPLE_RATE, 0)) + 1):
		print "there might be some missing data in acc_resample"

	for index in range(0, len(acc_re_sample_list), 1):
		file_write_to.write( str(acc_re_sample_list[index][0]) +','+ 
			                 str(acc_re_sample_list[index][1]) +','+ 
			                 str(acc_re_sample_list[index][2]) +','+ 
			                 str(acc_re_sample_list[index][3]) +','+ 
			                 str(acc_re_sample_list[index][4]) +','+
			                 str(acc_re_sample_list[index][5]) +','+
			                 str(acc_re_sample_list[index][6]) +','+
			                 str(acc_re_sample_list[index][7]) +','+
			                 str(acc_re_sample_list[index][8]) 
			                 +"\n");

	acc_raw.close()
	file_write_to.close()

	acc_t = []
	acc_x = []
	acc_y = []
	acc_z = []
	acc_N = []
	acc_xy = []
	acc_xz = []
	acc_yz = []
	acc_zSQ = []
	for index in range(0, len(acc_re_sample_list), 1):
		acc_t.append(acc_re_sample_list[index][0])
		acc_x.append(acc_re_sample_list[index][1])
		acc_y.append(acc_re_sample_list[index][2])
		acc_z.append(acc_re_sample_list[index][3])
		acc_N.append(acc_re_sample_list[index][4])
		acc_xy.append(acc_re_sample_list[index][5])
		acc_xz.append(acc_re_sample_list[index][6])
		acc_yz.append(acc_re_sample_list[index][7])
		acc_zSQ.append(acc_re_sample_list[index][8])

	print "the amount of (acc_data) after resample = (", len(acc_re_sample_list), ")"

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(811, autoscale_on=False, xlim=(0,180000), ylim=(-20,10))
	ax.set_title('Acc_X')
	lns1 = ax.plot(acc_t, acc_x, lw=2, color='green', label = 'acc_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(812, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_y, lw=2, color='purple', label = 'acc_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(813, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_Z')
	lns1 = ax.plot(acc_t, acc_z, lw=2, color='black', label = 'acc_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(814, autoscale_on=False, xlim=(0,180000), ylim=(0,20))
	ax.set_title('Acc_N')
	lns1 = ax.plot(acc_t, acc_N, lw=2, color='red', label = 'acc_N')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(815, autoscale_on=False, xlim=(0,180000), ylim=(0,20))
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_xy, lw=2, color='blue', label = 'acc_xy')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(816, autoscale_on=False, xlim=(0,180000), ylim=(0,40))
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_xz, lw=2, color='magenta', label = 'acc_xz')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(817, autoscale_on=False, xlim=(0,180000), ylim=(0,20))
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_yz, lw=2, color='green', label = 'acc_yz')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(818, autoscale_on=False, xlim=(0,180000), ylim=(-10,10))
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_zSQ, lw=2, color='red', label = 'acc_zSQ')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")	

	fig.savefig(acc_xyz_file_root)
	plt.close(fig)

	# # show()

	# # Three subplots sharing both x/y axes
	# # f, (ax1, ax2, ax3, axN) = plt.subplots(4, sharex=True, sharey=True)
	# # ax1.plot(acc_t, acc_x,  color='r')
	# # ax1.set_title('Acc X, Y, Z')
	# # ax2.plot(acc_t, acc_y,  color='b')
	# # ax3.plot(acc_t, acc_z,  color='k')
	# # axN.plot(acc_t, acc_N,  color='c')
	# # f.savefig(acc_xyz_file_root)
	# # # Fine-tune figure; make subplots close to each other and hide x ticks for
	# # # all but bottom plot.
	# # f.subplots_adjust(hspace=0)

	# # plt.close('all')
	# # fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	# # ax.plot(acc_t, acc_x)
	# # plt.ylabel('Acc_X')
	# # fig.savefig(acc_x_file_root)
	# # plt.close(fig)
	# # plt.show()

	# # fig, ay = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	# # ay.plot(acc_t, acc_y)
	# # plt.ylabel('Acc_Y')
	# # fig.savefig(acc_y_file_root)
	# # plt.close(fig)
	# # plt.show()	

	# # fig, az = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	# # az.plot(acc_t, acc_z)
	# # plt.ylabel('Acc_Z')
	# # fig.savefig(acc_z_file_root)
	# # plt.close(fig)

	# # fig, aN = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	# # aN.plot(acc_t, acc_N)
	# # plt.ylabel('Acc_Norm')
	# # fig.savefig(acc_n_file_root)
	# # plt.close(fig)