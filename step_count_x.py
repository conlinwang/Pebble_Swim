# step_count_x.py
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

def step_count_x( into_file_name ):
	print "step_count_x is entering"
	global step_count_x_result
	step_count_x_result = 100

# 	file_name = into_file_name

# 	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/step_count"):
# 		os.mkdir("./stroke_count_Evaluation/"+file_name+"/step_count")   

# 	acc_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/step_count/step_count.png"
	
# 	input_acc = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc_HP/smoothen_acc_HP.txt", "r+") # input training data

# 	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/step_count/step_count.txt", "wb")

# 	acc_input = input_acc.readlines()

# 	# For step counting X ----------------------------------------------------------------------
# 	step_counter = 0
# 	initial_Threshold_x = 1.5
# 	peak_point_xy = [0, 0, 0]
# 	stroke_count_x = [0, 0, 0]
# 	stroke_count_x_list = []
# 	pre_stroke_count_x = [0, 0, 0]
# 	time_interval_threshold = 400
# 	SC_x_Threshold = 1.2
# 	range_of_local_max = 10

# 	peak_point_x_list = [] 
# 	Time_threshold_xy_list = []

# 	# input three samples at a time acc_pre, acc_now, acc_nex  len(acc_input)-1, 2239
# 	for index01 in range(10, len(acc_input)-15, 1): 

# 		element_01 = acc_input[index01].split(",")
# 		element_02 = element_01[4].split("\n")
# 		element_03 = acc_input[index01-1].split(",")
# 		element_04 = element_03[4].split("\n")
# 		element_05 = acc_input[index01+1].split(",")
# 		element_06 = element_05[4].split("\n")

# 		acc_x_now = float(element_01[1])
# 		acc_x_pre = float(element_03[1])
# 		acc_x_nex = float(element_05[1])

# 		acc_z_now = float(element_01[3])
# 		acc_z_pre = float(element_03[3])
# 		acc_z_nex = float(element_05[3])

# 		acc_N_now = float(element_02[0])
# 		acc_N_pre = float(element_04[0])
# 		acc_N_nex = float(element_06[0])

# 		# Initial step count
# 		if (step_counter == 0):
# 			max_in_ten_sample = 0
# 			max_in_ten_sample_time = 0
# 			if( (float(acc_x_pre) > initial_Threshold_x) or (float(acc_x_nex) > initial_Threshold_x) ):
# 				if( (acc_x_nex - acc_x_now < 0) and (acc_x_now - acc_x_pre) > 0 ):
# 					peak_point_xy[0] = int(element_01[0])
# 					peak_point_xy[1] = float(acc_x_now)
# 					peak_point_xy[2] = float(initial_Threshold_x)
# 					peak_point_x_list.append(str(peak_point_xy)) # record the primiary peak 

# 					max_in_ten_sample = float(acc_x_now)
# 					max_in_ten_sample_time = int(element_01[0])

# 					for index2 in range(1, 21, 1):
# 						element_f = acc_input[index01+index2].split(",")
# 						acc_x_future = float(element_f[1])
# 						if(float(acc_x_future) > max_in_ten_sample):
# 							max_in_ten_sample = float(acc_x_future)
# 							max_in_ten_sample_time = int(element_f[0])

# 					step_counter = step_counter + 1

# 					stroke_count_x[0] = int(max_in_ten_sample_time)
# 					stroke_count_x[1] = float(max_in_ten_sample)
# 					stroke_count_x[2] = float(initial_Threshold_x)
# 					stroke_count_x_list.append(str(stroke_count_x))

# 					# Keep track of the previous peak position: time, magnitude, threshold
# 					pre_stroke_count_x[0] = int(stroke_count_x[0])
# 					pre_stroke_count_x[1] = float(stroke_count_x[1])
# 					pre_stroke_count_x[2] = float(stroke_count_x[2])
# 					Time_threshold_xy_list.append(str(initial_Threshold_x))

# 		# Follow up step count			
# 		elif (step_counter > 0):
# 			max_in_ten_sample = 0
# 			max_in_ten_sample_time = 0  
# 			# check time threshold
# 			if( ( int(element_01[0]) - int(pre_stroke_count_x[0]) >= time_interval_threshold) & (int(element_01[0]) - int(pre_stroke_count_x[0]) < 2000) ):
# 				if( (float(acc_x_now) > SC_x_Threshold) or (float(acc_x_nex) > SC_x_Threshold) ): # check magnitude threshold
# 					if( (float(acc_x_nex) - float(acc_x_now) < 0) & (float(acc_x_now) - float(acc_x_pre) > 0) ): # is a peak point
						
# 						peak_point_xy[0] = int(element_01[0]) # time position
# 						peak_point_xy[1] = float(acc_x_now)   # magnitude
# 						peak_point_xy[2] = float(SC_x_Threshold) # magnitude threshold
# 						peak_point_x_list.append(str(peak_point_xy)) # record the primiary peak 

# 						max_in_ten_sample = float(acc_x_now)        # check local max
# 						max_in_ten_sample_time = int(element_01[0])
						

# 						for index3 in range(1, range_of_local_max, 1):
# 							element_ff = acc_input[index01+index3].split(",")
# 							acc_x_future = float(element_ff[1])
# 							if(float(acc_x_future) > max_in_ten_sample):
# 								max_in_ten_sample = float(acc_x_future)
# 								max_in_ten_sample_time = int(element_ff[0])

# 						step_counter = step_counter + 1

# 						stroke_count_x[0] = int(max_in_ten_sample_time)
# 						stroke_count_x[1] = float(max_in_ten_sample)
# 						stroke_count_x[2] = float(SC_x_Threshold)
# 						stroke_count_x_list.append(str(stroke_count_x))

# 						# Keep track of the previous peak position: time, magnitude, threshold
# 						pre_stroke_count_x[0] = int(stroke_count_x[0])
# 						pre_stroke_count_x[1] = float(stroke_count_x[1])
# 						pre_stroke_count_x[2] = float(stroke_count_x[2])

# 						Time_threshold_xy_list.append(str(time_interval_threshold))

# 	if( len(stroke_count_x_list) * 2 >= 12 ):
# 		print "step count x=",len(stroke_count_x_list) * 2 #, step_counter  #, stroke_count_x_list
# 		# return len(stroke_count_x_list) * 2
# 	else:
# 		print "step count x=", 0
# 		# return 0
# 	# End of Acc x step counting ----------------------------------------------------------------------

# 	# For step counting Y ----------------------------------------------------------------------

# 	step_counter_Y = 0
# 	initial_Threshold_y = 0.5
# 	peak_point_y = [0, 0, 0]
# 	stroke_count_y = [0, 0, 0]
# 	stroke_count_y_list = []
# 	pre_stroke_count_y = [0, 0, 0]
# 	time_interval_threshold = 400
# 	SC_y_Threshold = 0.2
# 	range_of_local_max = 7

# 	peak_point_y_list = [] 
# 	Time_threshold_y_list = []

# 	for index01 in range(10, len(acc_input)-20, 1): 
# 		element_01 = acc_input[index01].split(",")
# 		element_02 = element_01[4].split("\n")
# 		element_03 = acc_input[index01-1].split(",")
# 		element_04 = element_03[4].split("\n")
# 		element_05 = acc_input[index01+1].split(",")
# 		element_06 = element_05[4].split("\n")

# 		acc_y_now = float(element_01[2])
# 		acc_y_pre = float(element_03[2])
# 		acc_y_nex = float(element_05[2])

# 		if (step_counter_Y == 0):
# 			max_in_ten_sample = 0
# 			max_in_ten_sample_time = 0
# 			if( (float(acc_y_pre) > initial_Threshold_y) or (float(acc_y_nex) > initial_Threshold_y) ):
# 				if( (acc_y_nex - acc_y_now < 0) and (acc_y_now - acc_y_pre) > 0 ):
# 					peak_point_y[0] = int(element_01[0])
# 					peak_point_y[1] = float(acc_y_now)
# 					peak_point_y[2] = float(initial_Threshold_y)
# 					peak_point_y_list.append(str(peak_point_y)) # record the primiary peak 

# 					max_in_ten_sample = float(acc_y_now)
# 					max_in_ten_sample_time = int(element_01[0])

# 					for index2 in range(1, 21, 1):
# 						element_f = acc_input[index01+index2].split(",")
# 						acc_y_future = float(element_f[2])
# 						if(float(acc_y_future) > max_in_ten_sample):
# 							max_in_ten_sample = float(acc_y_future)
# 							max_in_ten_sample_time = int(element_f[0])

# 					step_counter_Y = step_counter_Y + 1

# 					stroke_count_y[0] = int(max_in_ten_sample_time)
# 					stroke_count_y[1] = float(max_in_ten_sample)
# 					stroke_count_y[2] = float(initial_Threshold_y)
# 					stroke_count_y_list.append(str(stroke_count_y))

# 					# Keep track of the previous peak position: time, magnitude, threshold
# 					pre_stroke_count_y[0] = int(stroke_count_y[0])
# 					pre_stroke_count_y[1] = float(stroke_count_y[1])
# 					pre_stroke_count_y[2] = float(stroke_count_y[2])
# 					Time_threshold_y_list.append(str(initial_Threshold_y))

# 		# Follow up step count			
# 		elif (step_counter_Y > 0):
# 			max_in_ten_sample = 0
# 			max_in_ten_sample_time = 0  
# 			# check time threshold
# 			if( ( int(element_01[0]) - int(pre_stroke_count_y[0]) >= time_interval_threshold) & (int(element_01[0]) - int(pre_stroke_count_y[0]) < 5000) ):
# 				if( (float(acc_y_now) > SC_y_Threshold) or (float(acc_y_nex) > SC_y_Threshold) ): # check magnitude threshold
# 					if( (float(acc_y_nex) - float(acc_y_now) < 0) & (float(acc_y_now) - float(acc_y_pre) > 0) ): # is a peak point
						
# 						peak_point_y[0] = int(element_01[0]) # time position
# 						peak_point_y[1] = float(acc_y_now)   # magnitude
# 						peak_point_y[2] = float(SC_y_Threshold) # magnitude threshold
# 						peak_point_y_list.append(str(peak_point_y)) # record the primiary peak 

# 						max_in_ten_sample = float(acc_y_now)        # check local max
# 						max_in_ten_sample_time = int(element_01[0])
						

# 						for index3 in range(1, range_of_local_max, 1):
# 							element_ff = acc_input[index01+index3].split(",")
# 							acc_y_future = float(element_ff[2])
# 							if(float(acc_y_future) > max_in_ten_sample):
# 								max_in_ten_sample = float(acc_y_future)
# 								max_in_ten_sample_time = int(element_ff[0])

# 						step_counter_Y = step_counter_Y + 1

# 						stroke_count_y[0] = int(max_in_ten_sample_time)
# 						stroke_count_y[1] = float(max_in_ten_sample)
# 						stroke_count_y[2] = float(SC_y_Threshold)
# 						stroke_count_y_list.append(str(stroke_count_y))

# 						# Keep track of the previous peak position: time, magnitude, threshold
# 						pre_stroke_count_y[0] = int(stroke_count_y[0])
# 						pre_stroke_count_y[1] = float(stroke_count_y[1])
# 						pre_stroke_count_y[2] = float(stroke_count_y[2])

# 						Time_threshold_y_list.append(str(time_interval_threshold))

# 	if( len(stroke_count_y_list) * 2 >= 12 ):
# 		print "step count y=",len(stroke_count_y_list)  #, step_counter  #, stroke_count_x_list
# 		# return len(stroke_count_x_list) * 2
# 	else:
# 		print "step count y=", 0

# 	# print stroke_count_z_list


# 	# End of step counting Y----------------------------------------------------------------------

# 	# For step counting Z ----------------------------------------------------------------------

# 	step_counter_Z = 0
# 	initial_Threshold_z = 0.5
# 	peak_point_z = [0, 0, 0]
# 	stroke_count_z = [0, 0, 0]
# 	stroke_count_z_list = []
# 	pre_stroke_count_z = [0, 0, 0]
# 	time_interval_threshold = 400
# 	SC_z_Threshold = 0.2
# 	range_of_local_max = 10

# 	peak_point_z_list = [] 
# 	Time_threshold_z_list = []

# 	for index01 in range(10, len(acc_input)-20, 1): 
# 		element_01 = acc_input[index01].split(",")
# 		element_02 = element_01[4].split("\n")
# 		element_03 = acc_input[index01-1].split(",")
# 		element_04 = element_03[4].split("\n")
# 		element_05 = acc_input[index01+1].split(",")
# 		element_06 = element_05[4].split("\n")

# 		acc_z_now = float(element_01[3])
# 		acc_z_pre = float(element_03[3])
# 		acc_z_nex = float(element_05[3])

# 		if (step_counter_Z == 0):
# 			max_in_ten_sample = 0
# 			max_in_ten_sample_time = 0
# 			if( (float(acc_z_pre) > initial_Threshold_z) or (float(acc_z_nex) > initial_Threshold_z) ):
# 				if( (acc_z_nex - acc_z_now < 0) and (acc_z_now - acc_z_pre) > 0 ):
# 					peak_point_z[0] = int(element_01[0])
# 					peak_point_z[1] = float(acc_z_now)
# 					peak_point_z[2] = float(initial_Threshold_z)
# 					peak_point_z_list.append(str(peak_point_z)) # record the primiary peak 

# 					max_in_ten_sample = float(acc_z_now)
# 					max_in_ten_sample_time = int(element_01[0])

# 					for index2 in range(1, 21, 1):
# 						element_f = acc_input[index01+index2].split(",")
# 						acc_z_future = float(element_f[3])
# 						if(float(acc_z_future) > max_in_ten_sample):
# 							max_in_ten_sample = float(acc_z_future)
# 							max_in_ten_sample_time = int(element_f[0])

# 					step_counter_Z = step_counter_Z + 1

# 					stroke_count_z[0] = int(max_in_ten_sample_time)
# 					stroke_count_z[1] = float(max_in_ten_sample)
# 					stroke_count_z[2] = float(initial_Threshold_z)
# 					stroke_count_z_list.append(str(stroke_count_z))

# 					# Keep track of the previous peak position: time, magnitude, threshold
# 					pre_stroke_count_z[0] = int(stroke_count_z[0])
# 					pre_stroke_count_z[1] = float(stroke_count_z[1])
# 					pre_stroke_count_z[2] = float(stroke_count_z[2])
# 					Time_threshold_z_list.append(str(initial_Threshold_z))

# 		# Follow up step count			
# 		elif (step_counter_Z > 0):
# 			max_in_ten_sample = 0
# 			max_in_ten_sample_time = 0  
# 			# check time threshold
# 			if( ( int(element_01[0]) - int(pre_stroke_count_z[0]) >= time_interval_threshold) & (int(element_01[0]) - int(pre_stroke_count_z[0]) < 5000) ):
# 				if( (float(acc_z_now) > SC_z_Threshold) or (float(acc_z_nex) > SC_z_Threshold) ): # check magnitude threshold
# 					if( (float(acc_z_nex) - float(acc_z_now) < 0) & (float(acc_z_now) - float(acc_z_pre) > 0) ): # is a peak point
						
# 						peak_point_z[0] = int(element_01[0]) # time position
# 						peak_point_z[1] = float(acc_z_now)   # magnitude
# 						peak_point_z[2] = float(SC_z_Threshold) # magnitude threshold
# 						peak_point_z_list.append(str(peak_point_z)) # record the primiary peak 

# 						max_in_ten_sample = float(acc_z_now)        # check local max
# 						max_in_ten_sample_time = int(element_01[0])
						

# 						for index3 in range(1, range_of_local_max, 1):
# 							element_ff = acc_input[index01+index3].split(",")
# 							acc_z_future = float(element_ff[3])
# 							if(float(acc_z_future) > max_in_ten_sample):
# 								max_in_ten_sample = float(acc_z_future)
# 								max_in_ten_sample_time = int(element_ff[0])

# 						step_counter_Z = step_counter_Z + 1

# 						stroke_count_z[0] = int(max_in_ten_sample_time)
# 						stroke_count_z[1] = float(max_in_ten_sample)
# 						stroke_count_z[2] = float(SC_z_Threshold)
# 						stroke_count_z_list.append(str(stroke_count_z))

# 						# Keep track of the previous peak position: time, magnitude, threshold
# 						pre_stroke_count_z[0] = int(stroke_count_z[0])
# 						pre_stroke_count_z[1] = float(stroke_count_z[1])
# 						pre_stroke_count_z[2] = float(stroke_count_z[2])

# 						Time_threshold_z_list.append(str(time_interval_threshold))

# 	if( len(stroke_count_z_list) * 2 >= 12 ):
# 		print "step count z=",len(stroke_count_z_list)  #, step_counter  #, stroke_count_x_list
# 		# return len(stroke_count_x_list) * 2
# 	else:
# 		print "step count z=", 0

# 	# print stroke_count_z_list




# 	# End of step counting Z----------------------------------------------------------------------

# 	# For ploting ------------------------------------------------------------------------

# 	acc_t = np.zeros(len(acc_input))
# 	acc_x = np.zeros(len(acc_input)) 
# 	acc_y = np.zeros(len(acc_input))
# 	acc_z = np.zeros(len(acc_input))
# 	acc_N = np.zeros(len(acc_input))

# 	for index in range(0, len(acc_input), 1):
# 		element = acc_input[index].split(",")
# 		element01 = element[4].split("\n")
	
# 		acc_t[index] = int(element[0])
# 		acc_x[index] = float(element[1])
# 		acc_y[index] = float(element[2])
# 		acc_z[index] = float(element[3])
# 		acc_N[index] = float(element01[0])

# 	peak_t = []
# 	peak_acc = []
# 	peak_th = []
# 	for index in range(0, len(peak_point_x_list), 1):
# 		element = peak_point_x_list[index].split(",")
# 		element_1 = element[0].split("[")
# 		element_2 = element[2].split("]")

# 		peak_t.append(int(element_1[1]))
# 		peak_acc.append(float(element[1]))
# 		peak_th.append(float(element_2[0]))

# 	Time_Thresold_t = []
# 	Time_Thresold_magnitude = [] 
# 	for index in range(0, len(Time_threshold_xy_list), 1):
# 		element = peak_point_x_list[index].split(",")
# 		element_1 = element[0].split("[")
# 		# print int(element_1[1])
# 		element_2 = element[2].split("]")
# 		magnitude = element_2[0].strip()
# 		Time_Thresold_t.append( int(int(element_1[1])  + float(Time_threshold_xy_list[index]))  )  
# 		Time_Thresold_magnitude.append(float(magnitude))

	

# 	input_acc.close()
# 	# For ploting ------------------------------------------------------------------------

# 	# ------------------------------ plot x ------------------------------------
# 	#	
# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-20,20))  
# 	ax.set_title('Acc_X')
# 	lns1 = ax.plot(acc_t, acc_x, lw=2, color='green', label = 'acc_x')
# 	lns = lns1
# 	labs = [l.get_label() for l in lns]
# 	ax.legend(lns, labs, loc=0)
# 	ax.grid()
# 	# ax.set_xlabel("Time (msec)")
# 	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

# 	for index in range(0, step_counter ,1):
# 		element = stroke_count_x_list[index].split(",")
# 		element_1 = element[0].split("[")
# 		element_2 = element[1].split("]")
# 		time_stemp = float(element_1[1]) / 1000
# 		acc_value = round(float(element_2[0]), 1)
# 		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1[1], element_2[0]),  xycoords='data', color='magenta',
# 			xytext=(0.5, 60), textcoords='offset points',
# 			arrowprops=dict(arrowstyle="->",
# 				connectionstyle="angle3,angleA=0,angleB=-90"),
# 			)

# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-20,20))
# 	lns2 = ax.plot(peak_t, peak_acc, "ro", markersize=8, color='red')

# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-20,20))
# 	lns2 = ax.plot(peak_t, peak_th, "ro", markersize=5, color='green')

# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-20,20))
# 	lns2 = ax.plot(Time_Thresold_t, Time_Thresold_magnitude, "x", markersize=15, color='blue')

# 	ax = plt.errorbar(peak_t, peak_th, xerr=0.1, color='green')

# 	# End of plot X
# 	# ------------------------------ plot x ------------------------------------



# 	# ------------------------------ plot y ------------------------------------

# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))
# 	ax.set_title('Acc_Y')
# 	lns1 = ax.plot(acc_t, acc_y, lw=2, color='purple', label = 'acc_y')
# 	lns = lns1
# 	labs = [l.get_label() for l in lns]
# 	ax.legend(lns, labs, loc=0)
# 	ax.grid()
# 	# ax.set_xlabel("Time (msec)")
# 	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

# 	for index in range(0, step_counter_Y ,1):
# 		element_y = stroke_count_y_list[index].split(",")
# 		element_1y = element_y[0].split("[")
# 		element_2y = element_y[1].split("]")
# 		# print element_2z
# 		time_stemp = float(element_1y[1]) / 1000
# 		acc_value = round(float(element_2y[0]), 1)
# 		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1y[1], element_2y[0]),  xycoords='data', color='magenta',
# 			xytext=(1.5, 60), textcoords='offset points',
# 			arrowprops=dict(arrowstyle="->",
# 				connectionstyle="angle3,angleA=0,angleB=-90"),
# 		)


# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,190000), ylim=(-3,3))
# 	ax.set_title('Acc_Z')
# 	lns1 = ax.plot(acc_t, acc_z, lw=2, color='black', label = 'acc_z')
# 	lns = lns1
# 	labs = [l.get_label() for l in lns]
# 	ax.legend(lns, labs, loc=0)
# 	ax.grid()
# 	# ax.set_xlabel("Time (msec)")
# 	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

# 	for index in range(0, step_counter_Z ,1):
# 		element_z = stroke_count_z_list[index].split(",")
# 		element_1z = element_z[0].split("[")
# 		element_2z = element_z[1].split("]")
# 		# print element_2z
# 		time_stemp = float(element_1z[1]) / 1000
# 		acc_value = round(float(element_2z[0]), 1)
# 		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1z[1], element_2z[0]),  xycoords='data', color='magenta',
# 			xytext=(1.5, 60), textcoords='offset points',
# 			arrowprops=dict(arrowstyle="->",
# 				connectionstyle="angle3,angleA=0,angleB=-90"),
# 		)
	

# 	fig = figure(1,figsize=(120,15))
# 	ax = fig.add_subplot(414, autoscale_on=False, xlim=(0,190000), ylim=(-20,20))
# 	ax.set_title('Acc_N')
# 	lns1 = ax.plot(acc_t, acc_N, lw=2, color='red', label = 'acc_N')
# 	lns = lns1
# 	labs = [l.get_label() for l in lns]
# 	ax.legend(lns, labs, loc=0)
# 	ax.grid()
# 	ax.set_xlabel("Time (msec)")
# 	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

# 	fig.savefig(acc_xyz_file_root)
# 	plt.close(fig)



# # step_count("20151113_095219_Foot_Walk_holdCup_Conlin_Sony_200_0")