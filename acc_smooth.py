#acc_smooth.py
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import os
import math

def acc_smooth( into_file_name ):
	file_name = into_file_name
	if not os.path.exists("./"+file_name+"/smoothen_acc"):
		os.mkdir("./"+file_name+"/smoothen_acc")
	acc_xyz_file_root = "./"+file_name+"/smoothen_acc/Acc_raw_smooth.png"
	acc_x_file_root = "./"+file_name+"/smoothen_acc/Acc_X_raw.png"
	acc_y_file_root = "./"+file_name+"/smoothen_acc/Acc_Y_raw.png"
	acc_z_file_root = "./"+file_name+"/smoothen_acc/Acc_Z_raw.png"
	acc_n_file_root = "./"+file_name+"/smoothen_acc/Acc_N_raw.png"
	re_sample_acc = open("./"+file_name+"/re_sample_acc/re_sample_acc.txt", "r+") # input training data
	line = re_sample_acc.readlines()
	length = len(line)

	smoothen_list = []
	smoothen_array = [0, 0, 0, 0, 0, 0]
	for index in range(2, length-2, 1):
		element  = line[index].split(",")
		element2 = line[index+1].split(",")
		element3 = line[index-1].split(",")
		element4 = line[index+2].split(",")
		element5 = line[index-2].split(",")
		smoothen_array[0] = int(element[0])
		smoothen_array[1] = (float(element[1]) + float(element2[1]) + float(element3[1]) + float(element4[1]) + float(element4[1])) / 5
		smoothen_array[2] = (float(element[2]) + float(element2[2]) + float(element3[2]) + float(element4[2]) + float(element4[2])) / 5
		smoothen_array[3] = (float(element[3]) + float(element2[3]) + float(element3[3]) + float(element4[3]) + float(element4[3])) / 5
		smoothen_array[4] = (float(element[4]) + float(element2[4]) + float(element3[4]) + float(element4[4]) + float(element4[4])) / 5
		smoothen_array[5] = (float(element[5]) + float(element2[5]) + float(element3[5]) + float(element4[5]) + float(element4[5])) / 5
		smoothen_list.append(str(smoothen_array))

	acc_t = []
	acc_x = []
	acc_y = []
	acc_z = []
	acc_N = []
	acc_xy = []
	for index in range(0, len(smoothen_list), 1):
		element = smoothen_list[index].split(",")
		element0 = element[0].split("[")
		element1 = element[4].split("]")
		acc_t.append(int(element0[1]))
		acc_x.append(float(element[1]))
		acc_y.append(float(element[2]))
		acc_z.append(float(element[3]))
		acc_N.append(float(element[4]))
		acc_xy.append(float(element1[0]))

	fa, (ax1, ax2, ax3, axN) = plt.subplots(4, sharex=True, sharey=True)
	ax1.plot(acc_t, acc_x,  color='r')
	ax1.set_title('Acc X, Y, Z')
	ax2.plot(acc_t, acc_y,  color='b')
	ax3.plot(acc_t, acc_z,  color='k')
	axN.plot(acc_t, acc_N,  color='c')
	fa.savefig(acc_xyz_file_root)
	# Fine-tune figure; make subplots close to each other and hide x ticks for
	# all but bottom plot.
	fa.subplots_adjust(hspace=0)

	plt.close('all')
	fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	ax.plot(acc_t, acc_x)
	plt.ylabel('Acc_X')
	fig.savefig(acc_x_file_root)
	plt.close(fig)
	plt.show()

	fig, ay = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	ay.plot(acc_t, acc_y)
	plt.ylabel('Acc_Y')
	ay.annotate('arrowstyle', xy=(93300, -11.595750200000001),  xycoords='data',
		xytext=(-50, 30), textcoords='offset points',
		arrowprops=dict(arrowstyle="->")
		)
	fig.savefig(acc_y_file_root)
	plt.close(fig)
	plt.show()	

	fig, az = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	az.plot(acc_t, acc_z)
	plt.ylabel('Acc_Z')
	fig.savefig(acc_z_file_root)
	plt.close(fig)

	fig, aN = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
	aN.plot(acc_t, acc_N)
	plt.ylabel('Acc_Norm')
	fig.savefig(acc_n_file_root)
	plt.close(fig)

	stroke_count = 0
	peak_point = [0, 0]
	peak_point_list = []
	for index in range(1, len(smoothen_list)-1, 1):
		element  = smoothen_list[index].split(",")
		element_1 = element[0].split("[")
		element2 = smoothen_list[index+1].split(",")
		element3 = smoothen_list[index-1].split(",")
		if((float(element[2]) < -10) & ((float(element2[2]) < -10)) ):
			if(  (( float(element2[2]) - float(element[2]) ) > 0) & (( float(element[2]) - float(element3[2]) ) < 0)  ):
				stroke_count = stroke_count +1
				peak_point[0] = element_1[1]
				peak_point[1] = float(element[2])
		peak_point_list.append(peak_point)


	print "stroke_count on acc y", stroke_count
	print peak_point_list

	stroke_count_z = 0
	for index in range(1, len(smoothen_list)-1, 1):
		element  = smoothen_list[index].split(",")
		element_1 = element[3].split("]")
		element2 = smoothen_list[index+1].split(",")
		element_2 = element2[3].split("]")
		element3 = smoothen_list[index-1].split(",")
		element_3 = element3[3].split("]")
		if((float(element_1[0]) > 5) & ((float(element_2[0]) > 5)) ):
			if(  (( float(element_2[0]) - float(element_1[0]) ) < 0) & (( float(element_1[0]) - float(element_3[0]) ) > 0)  ):
				stroke_count_z = stroke_count_z +1
	# print "stroke_count on acc z", stroke_count_z

	re_sample_acc.close()