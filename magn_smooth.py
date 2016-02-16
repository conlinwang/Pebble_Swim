#magn_smooth.py
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import os
import math

def magn_smooth( into_file_name ):
	file_name = into_file_name
	if not os.path.exists("./"+file_name+"/smoothen_magn"):
		os.mkdir("./"+file_name+"/smoothen_magn")
	magn_xyz_file_root = "./"+file_name+"/smoothen_magn/Magn_raw.png"
	re_sample_magn = open("./"+file_name+"/re_sample_magn/re_sample_magn.txt", "r+") # input training data
	line = re_sample_magn.readlines()
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

	magn_t = []
	magn_x = []
	magn_y = []
	magn_z = []
	for index in range(0, len(smoothen_list), 1):
		element = smoothen_list[index].split(",")
		element0 = element[0].split("[")
		element1 = element[3].split("]")
		magn_t.append(int(element0[1]))
		magn_x.append(float(element[1]))
		magn_y.append(float(element[2]))
		magn_z.append(float(element1[0]))

	fm, (mx1, mx2, mx3) = plt.subplots(3, sharex=True, sharey=True)
	mx1.plot(magn_t, magn_x,  color='r')
	mx1.set_title('Magn X, Y, Z')
	mx2.plot(magn_t, magn_y,  color='b')
	mx3.plot(magn_t, magn_z,  color='k')
	fm.savefig(magn_xyz_file_root)
	# Fine-tune figure; make subplots close to each other and hide x ticks for
	# all but bottom plot.
	fm.subplots_adjust(hspace=0)

	plt.plot(magn_x)
	plt.ylabel('Magn X')
	# plt.show()

	plt.plot(magn_y)
	plt.ylabel('Magn Y')
	# plt.show()	
	
	plt.plot(magn_z)
	plt.ylabel('Magn Z')
	# plt.show()

	stroke_count = 0
	for index in range(1, len(smoothen_list)-1, 1):
		element  = smoothen_list[index].split(",")
		element2 = smoothen_list[index+1].split(",")
		element3 = smoothen_list[index-1].split(",")
		if((float(element[2]) > 2) & ((float(element2[2]) > 2)) ):
			if(  (( float(element2[2]) - float(element[2]) ) < 0) & (( float(element[2]) - float(element3[2]) ) > 0)  ):
				stroke_count = stroke_count +1
	print "stroke_count on magn y", stroke_count

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
	print "stroke_count on magn z", stroke_count_z

	re_sample_magn.close()