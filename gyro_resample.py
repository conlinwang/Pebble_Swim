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

def gyro_resample( into_SMAPLE_RATE, into_file_name ):
	print "file", into_file_name, "is running gyro_resample"
	SMAPLE_RATE = into_SMAPLE_RATE
	file_name = into_file_name

	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/re_sample_gyro"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/re_sample_gyro")

	gyro_raw = open("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate/gyro.txt", "r+") # input training data
	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/re_sample_gyro/re_sample_gyro.txt", "wb")

	gyro_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/re_sample_gyro/Gyro_raw.png"

	line = gyro_raw.readlines()
	length = len(line)

	element = line[length-1].split(",")
	total_time = int(round( float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
	print total_time

	gyro_re_sample_list = []
	gyro_re_sample_array = [0 , 0, 0, 0]
	element = line[0].split(",")
	gyro_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
	gyro_re_sample_array[1] = element[1]
	gyro_re_sample_array[2] = element[2]
	element2 = element[3].split("\n")
	gyro_re_sample_array[3] = element2[0]
	gyro_re_sample_list.append(gyro_re_sample_array)

	for index in range(1, length, 1):
		gyro_re_sample_array = [0 , 0, 0, 0]
		element = line[index].split(",")
		gyro_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
		gyro_re_sample_array[1] = element[1]
		gyro_re_sample_array[2] = element[2]
		element2 = element[3].split("\n")
		gyro_re_sample_array[3] = element2[0]
		if(gyro_re_sample_list[len(gyro_re_sample_list)-1][0] != gyro_re_sample_array[0]):
			gyro_re_sample_list.append(gyro_re_sample_array)

	for index in range(1, length, 1):
		gyro_re_sample_array = [0 , 0, 0, 0]
		element = line[index].split(",")
		gyro_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
		gyro_re_sample_array[1] = element[1]
		gyro_re_sample_array[2] = element[2]
		element2 = element[3].split("\n")
		gyro_re_sample_array[3] = element2[0]
		for item in range (0, len(gyro_re_sample_list), 1):
			if (gyro_re_sample_list[item][0] == gyro_re_sample_array[0]):
				gyro_re_sample_list[item][1] = gyro_re_sample_array[1]
				gyro_re_sample_list[item][2] = gyro_re_sample_array[2]
				gyro_re_sample_list[item][3] = gyro_re_sample_array[3]

	if (len(gyro_re_sample_list) != int(round(float(total_time)/SMAPLE_RATE, 0)) + 1):
		print "there might be some missing data"

	for index in range(0, len(gyro_re_sample_list), 1):
		file_write_to.write( str(gyro_re_sample_list[index][0]) +','+ str(gyro_re_sample_list[index][1]) +','+ str(gyro_re_sample_list[index][2]) +','+ str(gyro_re_sample_list[index][3]) +"\n");

	gyro_raw.close()
	file_write_to.close()

	gyro_t = []
	gyro_x = []
	gyro_y = []
	gyro_z = []
	for index in range(0, len(gyro_re_sample_list), 1):
		gyro_t.append(gyro_re_sample_list[index][0])
		gyro_x.append(gyro_re_sample_list[index][1])
		gyro_y.append(gyro_re_sample_list[index][2])
		gyro_z.append(gyro_re_sample_list[index][3])

	print "the amount of (gyro_data) after resample = (", len(gyro_re_sample_list), ")"
	print ''

	# Three subplots sharing both x/y axes
	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(311, autoscale_on=False, xlim=(0,180000), ylim=(-40,35))
	ax.set_title('Gyro_X')
	lns1 = ax.plot(gyro_t, gyro_x, lw=2, color='green', label = 'gyro_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(312, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
	ax.set_title('Gyro_Y')
	lns1 = ax.plot(gyro_t, gyro_y, lw=2, color='purple', label = 'gyro_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(313, autoscale_on=False, xlim=(0,180000), ylim=(-40,40))
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