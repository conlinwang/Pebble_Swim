#raw_data_preprocessor.py
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import os
import math

def magn_resample( into_SMAPLE_RATE, into_file_name ):
	SMAPLE_RATE = into_SMAPLE_RATE
	file_name = into_file_name

	if not os.path.exists("./"+file_name+"/re_sample_magn"):
		os.mkdir("./"+file_name+"/re_sample_magn")

	magn_raw = open("./"+file_name+"/RAW/AGM_RAW_separate/magn.txt", "r+") # input training data
	file_write_to = open("./"+file_name+"/re_sample_magn/re_sample_magn.txt", "wb")

	magn_xyz_file_root = "./"+file_name+"/re_sample_magn/Magn_raw.png"

	line = magn_raw.readlines()
	length = len(line)
	print length

	element = line[length-1].split(",")
	total_time = int(round( float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
	print total_time

	magn_re_sample_list = []
	magn_re_sample_array = [0 , 0, 0, 0]
	element = line[0].split(",")
	magn_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
	magn_re_sample_array[1] = element[1]
	magn_re_sample_array[2] = element[2]
	element2 = element[3].split("\n")
	magn_re_sample_array[3] = element2[0]
	magn_re_sample_list.append(magn_re_sample_array)

	for index in range(1, length, 1):
		magn_re_sample_array = [0 , 0, 0, 0]
		element = line[index].split(",")
		magn_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
		magn_re_sample_array[1] = element[1]
		magn_re_sample_array[2] = element[2]
		element2 = element[3].split("\n")
		magn_re_sample_array[3] = element2[0]
		if(magn_re_sample_list[len(magn_re_sample_list)-1][0] != magn_re_sample_array[0]):
			magn_re_sample_list.append(magn_re_sample_array)

	for index in range(1, length, 1):
		magn_re_sample_array = [0 , 0, 0, 0]
		element = line[index].split(",")
		magn_re_sample_array[0] = int(round(float(element[0]) / SMAPLE_RATE , 0)) * SMAPLE_RATE
		magn_re_sample_array[1] = element[1]
		magn_re_sample_array[2] = element[2]
		element2 = element[3].split("\n")
		magn_re_sample_array[3] = element2[0]
		for item in range (0, len(magn_re_sample_list), 1):
			if (magn_re_sample_list[item][0] == magn_re_sample_array[0]):
				magn_re_sample_list[item][1] = magn_re_sample_array[1]
				magn_re_sample_list[item][2] = magn_re_sample_array[2]
				magn_re_sample_list[item][3] = magn_re_sample_array[3]

	if (len(magn_re_sample_list) != int(round(float(total_time)/SMAPLE_RATE, 0)) + 1):
		print "there might be some missing data"

	for index in range(0, len(magn_re_sample_list), 1):
		file_write_to.write( str(magn_re_sample_list[index][0]) +','+ str(magn_re_sample_list[index][1]) +','+ str(magn_re_sample_list[index][2]) +','+ str(magn_re_sample_list[index][3]) +"\n");

	magn_raw.close()
	file_write_to.close()

	magn_t = []
	magn_x = []
	magn_y = []
	magn_z = []
	for index in range(0, len(magn_re_sample_list), 1):
		magn_t.append(magn_re_sample_list[index][0])
		magn_x.append(magn_re_sample_list[index][1])
		magn_y.append(magn_re_sample_list[index][2])
		magn_z.append(magn_re_sample_list[index][3])

	# Three subplots sharing both x/y axes
	fg, (mx1, mx2, mx3) = plt.subplots(3, sharex=True, sharey=True)
	mx1.plot(magn_t, magn_x,  color='r')
	mx1.set_title('Magn X, Y, Z')
	mx2.plot(magn_t, magn_y,  color='b')
	mx3.plot(magn_t, magn_z,  color='k')
	fg.savefig(magn_xyz_file_root)
	# Fine-tune figure; make subplots close to each other and hide x ticks for
	# all but bottom plot.
	fg.subplots_adjust(hspace=0)

	plt.plot(magn_x)
	plt.ylabel('magn X')
	# plt.show()

	plt.plot(magn_y)
	plt.ylabel('magn Y')
	# plt.show()	

	plt.plot(magn_z)
	plt.ylabel('magn Z')
	# plt.show()