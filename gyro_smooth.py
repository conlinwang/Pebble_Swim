#gyro_smooth.py
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

def gyro_smooth( into_file_name ):
	file_name = into_file_name
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/smoothen_gyro"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/smoothen_gyro")
	
	gyro_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/smoothen_gyro/Gyro_raw.png"

	re_sample_gyro = open("./stroke_count_Evaluation/"+file_name+"/re_sample_gyro/re_sample_gyro.txt", "r+") # input training data

	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/smoothen_gyro/smoothen_gyro.txt", "wb") # output file to txt

	line = re_sample_gyro.readlines()
	length = len(line)

	smoothen_list = []
	smoothen_array = [0, 0, 0, 0]
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
		smoothen_list.append(str(smoothen_array))

	gyro_t = []
	gyro_x = []
	gyro_y = []
	gyro_z = []
	for index in range(0, len(smoothen_list), 1):
		element = smoothen_list[index].split(",")
		element0 = element[0].split("[")
		element1 = element[3].split("]")
		gyro_t.append(int(element0[1]))
		gyro_x.append(float(element[1]))
		gyro_y.append(float(element[2]))
		gyro_z.append(float(element1[0]))
		file_write_to.write(str(int(element0[1])) +','+ str(float(element[1])) +','+ str(float(element[2])) +','+ str(float(element1[0])) +"\n")


	

	stroke_count = 0
	for index in range(1, len(smoothen_list)-1, 1):
		element  = smoothen_list[index].split(",")
		element2 = smoothen_list[index+1].split(",")
		element3 = smoothen_list[index-1].split(",")
		if((float(element[2]) > 2 ) & ((float(element2[2]) > 2 )) ):
			if(  (( float(element2[2]) - float(element[2]) ) < 0) & (( float(element[2]) - float(element3[2]) ) > 0)  ):
				stroke_count = stroke_count +1
	print "stroke_count on gyro y", stroke_count

	stroke_count_z = 0
	for index in range(1, len(smoothen_list)-1, 1):
		element  = smoothen_list[index].split(",")
		element_1 = element[3].split("]")
		element2 = smoothen_list[index+1].split(",")
		element_2 = element2[3].split("]")
		element3 = smoothen_list[index-1].split(",")
		element_3 = element3[3].split("]")
		if((float(element_1[0]) < -4) & ((float(element_2[0]) < -4)) ):
			if(  (( float(element_2[0]) - float(element_1[0]) ) > 0) & (( float(element_1[0]) - float(element_3[0]) ) < 0)  ):
				stroke_count_z = stroke_count_z +1
	print "stroke_count on gyro z", stroke_count_z

	re_sample_gyro.close()

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(311, autoscale_on=False, xlim=(0,180000), ylim=(-5,5))
	ax.set_title('Gyro_X')
	lns1 = ax.plot(gyro_t, gyro_x, lw=2, color='green', label = 'gyro_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(312, autoscale_on=False, xlim=(0,180000), ylim=(-5,5))
	ax.set_title('Gyro_Y')
	lns1 = ax.plot(gyro_t, gyro_y, lw=2, color='purple', label = 'gyro_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(313, autoscale_on=False, xlim=(0,180000), ylim=(-5,5))
	ax.set_title('Gyro_Z')
	lns1 = ax.plot(gyro_t, gyro_z, lw=2, color='black', label = 'gyro_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")
	
	fig.savefig(gyro_xyz_file_root)
	plt.close(fig)