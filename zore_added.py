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

def zero_added( into_file_name ):

	file_name = into_file_name
	
	# input_acc_data = open("./"+file_name+"/RAW/AGM_RAW_separate/acc.txt", "r+") # input_acc_data
	input_acc_data = open("./stroke_count_Evaluation/0606_144601_Tina_FCS_17_18_100m_L_50/smoothen_acc/acc_LPF_5Hz.txt", "r+") # input_acc_data	
	# input_gyro_data = open("./"+file_name+"/RAW/AGM_RAW_separate/gyro.txt", "r+") # input_acc_data

	# file_write_to = open("./"+file_name+"/RAW/AGM_RAW_separate/acc_zero_added.txt", "wb")
	file_write_to = open("./stroke_count_Evaluation/0606_144601_Tina_FCS_17_18_100m_L_50/smoothen_acc/acc_LPF_5Hz_zero_added.txt", "wb")
	
	acc_data = input_acc_data.readlines() # load data into python
	# gyro_data = input_gyro_data.readlines()

	acc_length = len(acc_data)    # get how many data had being loaded 
	# gyro_length = len(gyro_data)

	print acc_length


	for index in range(0, acc_length, 1):
		element = acc_data[index].split(",")
		element0 = element[0].split("[") 
		element1 = element[5].split("]")
		element2 = element1[0].split("\n")
		# print element0[0], element[1], element[2], element[3], element[4], element2[0]

		file_write_to.write( 
			str(int(element0[0])) +','+ 
			str(float(element[1]))+','+
			str(float(element[2]))+','+
			str(float(element[3]))+','+
			str(float(element[4]))+','+
			# str(float(element[5]))+','+
			# str(float(element[6]))+','+
			# str(float(element[7]))+','+
			str(float(element2[0])) +"\n");

	temp   = acc_data[acc_length-1].split(",")
	temp01 = temp[0].split("[") 
	temp02 = int(temp01[0])
	for index in range(0, 1000, 1):
		file_write_to.write( 
			str(int(temp02+((index+1)*50))) +','+ 
			str(0)+','+  # acc_x
			str(0)+','+  # acc_y
			str(0)+','+  # acc_z
			str(0)+','+  # acc_N
			# str(0)+','+  # acc_xy
			# str(0)+','+  # acc_xz
			# str(0)+','+  # acc_yz
			str(0) +"\n"); # acc_zSQ


file_for_SC = "0712_180117_Conlin_FCS_16_17_100m_R"
zero_added(file_for_SC)
