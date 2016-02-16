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
	
	input_acc_data = open("./imu_03.txt", "r+") # input_acc_data

	acc_data = input_acc_data.readlines() # load data into python

	acc_length = len(acc_data)    # get how many data had being loaded 

	file_write_to = open("./imu_Acc_N_03.txt", "wb")


	acc_t = []
	acc_x = []
	acc_y = []
	acc_z = []
	acc_N = []
	acc_N_HP = np.zeros(len(acc_data))
	init_time = 0
	init_Acc_N = 1.0
	aplpha = 0.94
	for index in range(0, len(acc_data), 1):
		element_time = acc_data[0].split(" ")
		init_time = int(element_time[0])
		init_Acc_N = float((float(element_time[4])**2 + float(element_time[5])**2 + float(element_time[6]) ** 2 )  ** 0.5)
		acc_N_HP[0] = float(init_Acc_N)

		element = acc_data[index].split(" ")
		acc_t.append( int(int(element[0]) - int(init_time)) )
		# acc_t.append( int(element[0]) - int(init_time) )
		acc_N.append(float((float(element[4])**2 + float(element[5])**2 + float(element[6]) ** 2 )  ** 0.5))
		if(index > 0):
			acc_N_HP[index] = aplpha * acc_N_HP[index-1] + aplpha * (float(acc_N[index]) - float(acc_N[index-1]) )

		file_write_to.write( str( int(int(element[0]) - int(init_time)) ) +','+ 
                             str( float((float(element[4])**2 + float(element[5])**2 + float(element[6]) ** 2 )  ** 0.5) ) +','+ 
                             str( acc_N_HP[index] )
			                 + "\n")
		
	# print element_time
	# print init_time
	# print acc_t
	# print acc_N
	print acc_N_HP


	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(211, autoscale_on=False, xlim=(0,125000), ylim=(0,50))
	ax.set_title('Acc_N')
	lns1 = ax.plot(acc_t, acc_N, lw=2, color='blue', label = 'acc_N')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(212, autoscale_on=False, xlim=(0,125000), ylim=(-50,50))
	ax.set_title('acc_N_HP')
	lns1 = ax.plot(acc_t, acc_N_HP, lw=2, color='red', label = 'acc_N_HP')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	
	fig.savefig("./Pedometer03.png")



file_for_SC = "imu_01"
stroke_count(file_for_SC)