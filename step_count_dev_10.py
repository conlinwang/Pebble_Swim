# step_count.py
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

def step_count( into_file_name, init_point ):
	x_init_point = init_point
	y_init_point = init_point
	z_init_point = init_point

	end_point = 11

	x_end_point = end_point
	y_end_point = end_point
	z_end_point = end_point

	file_name = into_file_name

	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/step_count"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/step_count")   

	acc_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/step_count/step_count.png"
	
	input_acc = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc_HP/smoothen_acc_HP.txt", "r+") # input training data

	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/step_count/step_count.txt", "wb")

	acc_input = input_acc.readlines()

	# For step counting X ----------------------------------------------------------------------
	step_counter = 0
	initial_Threshold_x = 0.5    	   #1.5
	peak_point_xy = [0, 0, 0]
	stroke_count_x = [0, 0, 0]
	stroke_count_x_list = []
	pre_stroke_count_x = [0, 0, 0]
	time_interval_threshold = 800 	#500 for run, 800 for walking
	SC_x_Threshold = 0.6         	#3.0 for run, 0.6 for walking
	range_of_local_max = 7

	peak_point_x_list = [] 
	Time_threshold_xy_list = []
	state_indicator = 0

	# input three samples at a time acc_pre, acc_now, acc_nex  len(acc_input)-1, 2239
	for index01 in range(x_init_point, len(acc_input)-end_point, 1): 

		element_01 = acc_input[index01].split(",")
		element_02 = element_01[4].split("\n")
		element_03 = acc_input[index01-1].split(",")
		element_04 = element_03[4].split("\n")
		element_05 = acc_input[index01+1].split(",")
		element_06 = element_05[4].split("\n")

		acc_t_now = int(element_01[0])
		acc_x_now = float(element_01[1])
		acc_x_pre = float(element_03[1])
		acc_x_nex = float(element_05[1])

		# Initial step count
		if (state_indicator == 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0
			if( (float(acc_x_pre) > initial_Threshold_x) or (float(acc_x_nex) > initial_Threshold_x) ): # acc_x_pre and acc_x_nex > magnitude threshold, 
				if( (acc_x_nex - acc_x_now < 0) and (acc_x_now - acc_x_pre) > 0 ): # confirm is a peak point
					peak_point_xy[0] = int(element_01[0]) 			# mark down the time of this peak
					peak_point_xy[1] = float(acc_x_now)   			# mark down the magnitude of this peak
					peak_point_xy[2] = float(initial_Threshold_x)   # mark down the Threshold using for this peak
					peak_point_x_list.append(str(peak_point_xy))    # record the primiary peak 

					max_in_ten_sample = float(acc_x_now)			# look for local max
					max_in_ten_sample_time = int(element_01[0])

					for index2 in range(1, range_of_local_max, 1):					# look for local max in 8 x 80 = 640 msec
						element_f = acc_input[index01+index2].split(",")
						acc_x_future = float(element_f[1])
						if(float(acc_x_future) > max_in_ten_sample):
							max_in_ten_sample = float(acc_x_future)    # confirmed local max
							max_in_ten_sample_time = int(element_f[0])

					step_counter = step_counter + 1					   # step counter increases
					state_indicator = 1

					stroke_count_x[0] = int(max_in_ten_sample_time)  # mark down the 1st step count point, time
					stroke_count_x[1] = float(max_in_ten_sample)     # mark down the 1st step count point, magnitude
					stroke_count_x[2] = float(initial_Threshold_x)   # mark down the 1st step count point, magnitude threshold
					stroke_count_x_list.append(str(stroke_count_x))  # mark down the 1st step count point info

					# Keep track of the previous peak position: time, magnitude, threshold
					pre_stroke_count_x[0] = int(stroke_count_x[0])
					pre_stroke_count_x[1] = float(stroke_count_x[1])
					pre_stroke_count_x[2] = float(stroke_count_x[2])
					Time_threshold_xy_list.append(str(initial_Threshold_x))

		# Follow up step count			
		if (step_counter > 0 and state_indicator == 1):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0  
			# check time threshold  and (int(element_01[0]) - int(pre_stroke_count_x[0]) < 5000)
			if( ( int(element_01[0]) - int(pre_stroke_count_x[0]) >= time_interval_threshold)  ):
				if( (float(acc_x_now) > SC_x_Threshold) or (float(acc_x_nex) > SC_x_Threshold) ): # check magnitude threshold
					if( (float(acc_x_nex) - float(acc_x_now) < 0) & (float(acc_x_now) - float(acc_x_pre) > 0) ): # is a peak point
						
						peak_point_xy[0] = int(element_01[0]) 		 # mark down the time position
						peak_point_xy[1] = float(acc_x_now)   		 # mark down the magnitude
						peak_point_xy[2] = float(SC_x_Threshold) 	 # mark down the magnitude threshold
						peak_point_x_list.append(str(peak_point_xy)) # record the primiary peak 

						max_in_ten_sample = float(acc_x_now)         # check local max
						max_in_ten_sample_time = int(element_01[0])
						
						for index3 in range(1, range_of_local_max, 1):
							element_ff = acc_input[index01+index3].split(",")
							acc_x_future = float(element_ff[1])
							if(float(acc_x_future) > max_in_ten_sample):
								max_in_ten_sample = float(acc_x_future)
								max_in_ten_sample_time = int(element_ff[0])

						step_counter = step_counter + 1              # step counter increases

						stroke_count_x[0] = int(max_in_ten_sample_time)  # mark down the 1st step count point, time
						stroke_count_x[1] = float(max_in_ten_sample)
						stroke_count_x[2] = float(SC_x_Threshold)
						stroke_count_x_list.append(str(stroke_count_x))

						# Keep track of the previous peak position: time, magnitude, threshold
						pre_stroke_count_x[0] = int(stroke_count_x[0])
						pre_stroke_count_x[1] = float(stroke_count_x[1])
						pre_stroke_count_x[2] = float(stroke_count_x[2])

						Time_threshold_xy_list.append(str(time_interval_threshold))

		if( (int(element_01[0]) - int(pre_stroke_count_x[0]) > 3000) and (state_indicator == 1) ):
			state_indicator = 0
			if(len(stroke_count_x_list) < 16):
				stroke_count_x_list = []

	# print step_counter

	step_freq_x = 0
	total_time_x = 1
	x_init_time = 0
	x_final_time = 0

	if(step_counter >10 and len(stroke_count_x_list) > 0):
		element_x_init_time = stroke_count_x_list[0].split(",")
		element_x_init_time01 = element_x_init_time[0].split("[")
		
		element_x_final_time = stroke_count_x_list[len(stroke_count_x_list)-1].split(",")
		element_x_final_time01 = element_x_final_time[0].split("[")
		
		x_init_time = int(element_x_init_time01[1])
		x_final_time = int(element_x_final_time01[1])

		total_time_x =  ( x_final_time - x_init_time) / 1000
		step_freq_x = float(step_counter) / total_time_x
	print "stroke_count_x_list len = ",len(stroke_count_x_list)
	
	# End of Acc x step counting ----------------------------------------------------------------------

	# For step counting Y ----------------------------------------------------------------------

	step_counter_Y = 0
	step_counter_interal_result_list = []
	initial_Threshold_y = 0.5
	peak_point_y = [0, 0, 0]
	stroke_count_y = [0, 0, 0]
	stroke_count_y_list = []
	stroke_count_y_list_histroy = []
	pre_stroke_count_y = [1000000, 0, 0]
	time_interval_threshold = 800 # 800
	SC_y_Threshold = 0.9
	range_of_local_max = 7

	peak_point_y_list = [] 
	Time_threshold_y_list = []

	for index01 in range(y_init_point, len(acc_input)-end_point, 1): 
		element_01 = acc_input[index01].split(",")
		element_02 = element_01[4].split("\n")
		element_03 = acc_input[index01-1].split(",")
		element_04 = element_03[4].split("\n")
		element_05 = acc_input[index01+1].split(",")
		element_06 = element_05[4].split("\n")


		acc_t_now = int(element_01[0])
		acc_y_now = float(element_01[2])		
		acc_y_pre = float(element_03[2])
		acc_y_nex = float(element_05[2])

		if (step_counter_Y == 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0
			if( (float(acc_y_pre) > initial_Threshold_y) or (float(acc_y_nex) > initial_Threshold_y) ):
				if( (acc_y_nex - acc_y_now < 0) and (acc_y_now - acc_y_pre) > 0 ):
					peak_point_y[0] = int(element_01[0])
					peak_point_y[1] = float(acc_y_now)
					peak_point_y[2] = float(initial_Threshold_y)
					peak_point_y_list.append(str(peak_point_y)) # record the primiary peak 

					max_in_ten_sample = float(acc_y_now)
					max_in_ten_sample_time = int(element_01[0])

					for index2 in range(1, 21, 1):
						element_f = acc_input[index01+index2].split(",")
						acc_y_future = float(element_f[2])
						if(float(acc_y_future) > max_in_ten_sample):
							max_in_ten_sample = float(acc_y_future)
							max_in_ten_sample_time = int(element_f[0])

					step_counter_Y = step_counter_Y + 1

					stroke_count_y[0] = int(max_in_ten_sample_time)
					stroke_count_y[1] = float(max_in_ten_sample)
					stroke_count_y[2] = float(initial_Threshold_y)
					stroke_count_y_list.append(str(stroke_count_y))

					# Keep track of the previous peak position: time, magnitude, threshold
					pre_stroke_count_y[0] = int(stroke_count_y[0])
					pre_stroke_count_y[1] = float(stroke_count_y[1])
					pre_stroke_count_y[2] = float(stroke_count_y[2])
					Time_threshold_y_list.append(str(initial_Threshold_y))

		# Follow up step count			
		elif (step_counter_Y > 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0  
			# check time threshold
			if( ( int(element_01[0]) - int(pre_stroke_count_y[0]) >= time_interval_threshold) & (int(element_01[0]) - int(pre_stroke_count_y[0]) < 5000) ):
				if( (float(acc_y_now) > SC_y_Threshold) or (float(acc_y_nex) > SC_y_Threshold) ): # check magnitude threshold
					if( (float(acc_y_nex) - float(acc_y_now) < 0) & (float(acc_y_now) - float(acc_y_pre) > 0) ): # is a peak point
						
						peak_point_y[0] = int(element_01[0]) # time position
						peak_point_y[1] = float(acc_y_now)   # magnitude
						peak_point_y[2] = float(SC_y_Threshold) # magnitude threshold
						peak_point_y_list.append(str(peak_point_y)) # record the primiary peak 

						max_in_ten_sample = float(acc_y_now)        # check local max
						max_in_ten_sample_time = int(element_01[0])
						

						for index3 in range(1, range_of_local_max, 1):
							element_ff = acc_input[index01+index3].split(",")
							acc_y_future = float(element_ff[2])
							if(float(acc_y_future) > max_in_ten_sample):
								max_in_ten_sample = float(acc_y_future)
								max_in_ten_sample_time = int(element_ff[0])

						step_counter_Y = step_counter_Y + 1

						stroke_count_y[0] = int(max_in_ten_sample_time)
						stroke_count_y[1] = float(max_in_ten_sample)
						stroke_count_y[2] = float(SC_y_Threshold)
						stroke_count_y_list.append(str(stroke_count_y))

						# Keep track of the previous peak position: time, magnitude, threshold
						pre_stroke_count_y[0] = int(stroke_count_y[0])
						pre_stroke_count_y[1] = float(stroke_count_y[1])
						pre_stroke_count_y[2] = float(stroke_count_y[2])


						Time_threshold_y_list.append(str(time_interval_threshold))
		
		if(acc_t_now - int(pre_stroke_count_y[0]) > 4000 and len(stroke_count_y_list) < 15):
			# print stroke_count_y_list
			step_counter_interal_result_list.append(step_counter_Y)
			step_counter_Y = 0
			pre_stroke_count_y = [1000000, 0, 0]
			stroke_count_y_list = []
	
			stroke_count_y_list_histroy.append(stroke_count_y_list)
	
		# print acc_t_now - int(pre_stroke_count_y[0])
	
	print "stroke_count_y_list_histroy", len(stroke_count_y_list_histroy)
	# print stroke_count_y_list_histroy


	step_freq_y = 0
	total_time_y = 1
	y_init_time = 0
	y_final_time = 0

	if(step_counter_Y >10):
		element_y_init_time = stroke_count_y_list[0].split(",")
		element_y_init_time01 = element_y_init_time[0].split("[")
		element_y_final_time = stroke_count_y_list[step_counter_Y-1].split(",")
		element_y_final_time01 = element_y_final_time[0].split("[")
		
		y_init_time = int(element_y_init_time01[1])
		y_final_time = int(element_y_final_time01[1])

		total_time_y = ( y_final_time - y_init_time ) / 1000
		step_freq_y = float(step_counter_Y) / total_time_y
	# print "step_freq_y=", step_freq_y, y_final_time, y_init_time, step_counter_Y

	# if( len(stroke_count_y_list) * 2 >= 12 ):
	# 	print "step count y=",len(stroke_count_y_list)  #, step_counter  #, stroke_count_x_list
	# 	# return len(stroke_count_x_list) * 2
	# else:
	# 	print "step count y=", 0

	# print stroke_count_z_list


	# End of step counting Y----------------------------------------------------------------------

	# For step counting Z ----------------------------------------------------------------------

	step_counter_Z = 0
	initial_Threshold_z = 0.5
	peak_point_z = [0, 0, 0]
	stroke_count_z = [0, 0, 0]
	stroke_count_z_list = []
	pre_stroke_count_z = [0, 0, 0]
	time_interval_threshold = 500 #800
	SC_z_Threshold = 2.2
	range_of_local_max = 10

	peak_point_z_list = [] 
	Time_threshold_z_list = []

	for index01 in range(z_init_point, len(acc_input)-end_point, 1): 
		element_01 = acc_input[index01].split(",")
		element_02 = element_01[4].split("\n")
		element_03 = acc_input[index01-1].split(",")
		element_04 = element_03[4].split("\n")
		element_05 = acc_input[index01+1].split(",")
		element_06 = element_05[4].split("\n")

		acc_z_now = float(element_01[3])
		acc_z_pre = float(element_03[3])
		acc_z_nex = float(element_05[3])

		if (step_counter_Z == 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0
			if( (float(acc_z_pre) > initial_Threshold_z) or (float(acc_z_nex) > initial_Threshold_z) ):
				if( (acc_z_nex - acc_z_now < 0) and (acc_z_now - acc_z_pre) > 0 ):
					peak_point_z[0] = int(element_01[0])
					peak_point_z[1] = float(acc_z_now)
					peak_point_z[2] = float(initial_Threshold_z)
					peak_point_z_list.append(str(peak_point_z)) # record the primiary peak 

					max_in_ten_sample = float(acc_z_now)
					max_in_ten_sample_time = int(element_01[0])

					for index2 in range(1, 21, 1):
						element_f = acc_input[index01+index2].split(",")
						acc_z_future = float(element_f[3])
						if(float(acc_z_future) > max_in_ten_sample):
							max_in_ten_sample = float(acc_z_future)
							max_in_ten_sample_time = int(element_f[0])

					step_counter_Z = step_counter_Z + 1

					stroke_count_z[0] = int(max_in_ten_sample_time)
					stroke_count_z[1] = float(max_in_ten_sample)
					stroke_count_z[2] = float(initial_Threshold_z)
					stroke_count_z_list.append(str(stroke_count_z))

					# Keep track of the previous peak position: time, magnitude, threshold
					pre_stroke_count_z[0] = int(stroke_count_z[0])
					pre_stroke_count_z[1] = float(stroke_count_z[1])
					pre_stroke_count_z[2] = float(stroke_count_z[2])
					Time_threshold_z_list.append(str(initial_Threshold_z))

		# Follow up step count			
		elif (step_counter_Z > 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0  
			# check time threshold
			if( ( int(element_01[0]) - int(pre_stroke_count_z[0]) >= time_interval_threshold) & (int(element_01[0]) - int(pre_stroke_count_z[0]) < 5000) ):
				if( (float(acc_z_now) > SC_z_Threshold) or (float(acc_z_nex) > SC_z_Threshold) ): # check magnitude threshold
					if( (float(acc_z_nex) - float(acc_z_now) < 0) & (float(acc_z_now) - float(acc_z_pre) > 0) ): # is a peak point
						
						peak_point_z[0] = int(element_01[0]) # time position
						peak_point_z[1] = float(acc_z_now)   # magnitude
						peak_point_z[2] = float(SC_z_Threshold) # magnitude threshold
						peak_point_z_list.append(str(peak_point_z)) # record the primiary peak 

						max_in_ten_sample = float(acc_z_now)        # check local max
						max_in_ten_sample_time = int(element_01[0])
						

						for index3 in range(1, range_of_local_max, 1):
							element_ff = acc_input[index01+index3].split(",")
							acc_z_future = float(element_ff[3])
							if(float(acc_z_future) > max_in_ten_sample):
								max_in_ten_sample = float(acc_z_future)
								max_in_ten_sample_time = int(element_ff[0])

						step_counter_Z = step_counter_Z + 1

						stroke_count_z[0] = int(max_in_ten_sample_time)
						stroke_count_z[1] = float(max_in_ten_sample)
						stroke_count_z[2] = float(SC_z_Threshold)
						stroke_count_z_list.append(str(stroke_count_z))

						# Keep track of the previous peak position: time, magnitude, threshold
						pre_stroke_count_z[0] = int(stroke_count_z[0])
						pre_stroke_count_z[1] = float(stroke_count_z[1])
						pre_stroke_count_z[2] = float(stroke_count_z[2])

						Time_threshold_z_list.append(str(time_interval_threshold))

	total_time_z = 0
	step_freq_z = 0
	z_init_time = 0
	z_final_time = 0

	if(step_counter_Z >10):
		element_z_init_time = stroke_count_z_list[0].split(",")
		element_z_init_time01 = element_z_init_time[0].split("[")
		element_z_final_time = stroke_count_z_list[step_counter_Z-1].split(",")
		element_z_final_time01 = element_z_final_time[0].split("[")

		z_init_time = int(element_z_init_time01[1])
		z_final_time = int(element_z_final_time01[1])

		total_time_z = (z_final_time - z_init_time ) / 1000
		step_freq_z = float(step_counter_Z) / total_time_z
	# print "step_freq_z=", step_freq_z, z_final_time, z_init_time, step_counter_Z

	# if( len(stroke_count_z_list) * 2 >= 12 ):
	# 	print "step count z=",len(stroke_count_z_list)  #, step_counter  #, stroke_count_x_list
	# 	# return len(stroke_count_x_list) * 2
	# else:
	# 	print "step count z=", 0

	# print stroke_count_z_list




	# End of step counting Z----------------------------------------------------------------------

	# For ploting ------------------------------------------------------------------------

	acc_t = np.zeros(len(acc_input))
	acc_x = np.zeros(len(acc_input)) 
	acc_y = np.zeros(len(acc_input))
	acc_z = np.zeros(len(acc_input))
	acc_N = np.zeros(len(acc_input))

	for index in range(0, len(acc_input), 1):
		element = acc_input[index].split(",")
		element01 = element[4].split("\n")
	
		acc_t[index] = int(element[0])
		acc_x[index] = float(element[1])
		acc_y[index] = float(element[2])
		acc_z[index] = float(element[3])
		acc_N[index] = float(element01[0])

	peak_t = []
	peak_acc = []
	peak_th = []
	for index in range(0, len(peak_point_x_list), 1):
		element = peak_point_x_list[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[2].split("]")

		peak_t.append(int(element_1[1]))
		peak_acc.append(float(element[1]))
		peak_th.append(float(element_2[0]))
	# ----------------------------------------------------------------------------

	peak_t_y = []
	peak_acc_y = []
	peak_th_y = []
	for index in range(0, len(peak_point_y_list), 1):
		element = peak_point_y_list[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[2].split("]")

		peak_t_y.append(int(element_1[1]))
		peak_acc_y.append(float(element[1]))
		peak_th_y.append(float(element_2[0]))

	# ----------------------------------------------------------------------------

	peak_t_z = []
	peak_acc_z = []
	peak_th_z = []
	for index in range(0, len(peak_point_z_list), 1):
		element = peak_point_z_list[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[2].split("]")

		peak_t_z.append(int(element_1[1]))
		peak_acc_z.append(float(element[1]))
		peak_th_z.append(float(element_2[0]))

	# ----------------------------------------------------------------------------

	Time_Thresold_t = []
	Time_Thresold_magnitude = [] 
	for index in range(0, len(Time_threshold_xy_list), 1):
		element = peak_point_x_list[index].split(",")
		element_1 = element[0].split("[")
		# print int(element_1[1])
		element_2 = element[2].split("]")
		magnitude = element_2[0].strip()
		Time_Thresold_t.append( int(int(element_1[1])  + float(Time_threshold_xy_list[index]))  )  
		Time_Thresold_magnitude.append(float(magnitude))

	# ----------------------------------------------------------------------------

	Time_Thresold_t_y = []
	Time_Thresold_magnitude_y = [] 
	for index in range(0, len(Time_threshold_y_list), 1):
		element = peak_point_y_list[index].split(",")
		element_1 = element[0].split("[")
		# print int(element_1[1])
		element_2 = element[2].split("]")
		magnitude = element_2[0].strip()
		Time_Thresold_t_y.append( int(int(element_1[1])  + float(Time_threshold_y_list[index]))  )  
		Time_Thresold_magnitude_y.append(float(magnitude))
	# ----------------------------------------------------------------------------

	Time_Thresold_t_z = []
	Time_Thresold_magnitude_z = [] 
	for index in range(0, len(Time_threshold_z_list), 1):
		element = peak_point_z_list[index].split(",")
		element_1 = element[0].split("[")
		# print int(element_1[1])
		element_2 = element[2].split("]")
		magnitude = element_2[0].strip()
		Time_Thresold_t_z.append( int(int(element_1[1])  + float(Time_threshold_z_list[index]))  )  
		Time_Thresold_magnitude_z.append(float(magnitude))

	# ----------------------------------------------------------------------------	
	

	input_acc.close()
	# For ploting ------------------------------------------------------------------------

	# ------------------------------ plot x ------------------------------------
	#

	
	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))  
	ax.set_title('Acc_X')
	lns1 = ax.plot(acc_t, acc_x, lw=2, color='green', label = 'acc_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	for index in range(0, len(stroke_count_x_list) ,1):
		element = stroke_count_x_list[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[1].split("]")
		time_stemp = float(element_1[1]) / 1000
		acc_value = round(float(element_2[0]), 1)
		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1[1], element_2[0]),  xycoords='data', color='magenta',
			xytext=(0.5, 60), textcoords='offset points',
			arrowprops=dict(arrowstyle="->",
				connectionstyle="angle3,angleA=0,angleB=-90"),
			)

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))
	lns2 = ax.plot(peak_t, peak_acc, "ro", markersize=8, color='red')

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))
	lns2 = ax.plot(peak_t, peak_th, "ro", markersize=5, color='green')

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(411, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))
	lns2 = ax.plot(Time_Thresold_t, Time_Thresold_magnitude, "x", markersize=15, color='blue')

	ax = plt.errorbar(peak_t, peak_th, xerr=0.1, color='green')

	# End of plot X
	# ------------------------------ plot x ------------------------------------



	# ------------------------------ plot y ------------------------------------

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_y, lw=2, color='purple', label = 'acc_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	for index in range(0, step_counter_Y ,1):
		element_y = stroke_count_y_list[index].split(",")
		element_1y = element_y[0].split("[")
		element_2y = element_y[1].split("]")
		# print element_2z
		time_stemp = float(element_1y[1]) / 1000
		acc_value = round(float(element_2y[0]), 1)
		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1y[1], element_2y[0]),  xycoords='data', color='magenta',
			xytext=(1.5, 60), textcoords='offset points',
			arrowprops=dict(arrowstyle="->",
				connectionstyle="angle3,angleA=0,angleB=-90"),
		)

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,190000), ylim=(-5,5) )
	lns2 = ax.plot(peak_t_y, peak_acc_y, "ro", markersize=8, color='red')

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,190000), ylim=(-5,5) )
	lns2 = ax.plot(peak_t_y, peak_th_y, "ro", markersize=5, color='green')

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(412, autoscale_on=False, xlim=(0,190000), ylim=(-5,5) )
	lns2 = ax.plot(Time_Thresold_t_y, Time_Thresold_magnitude_y, "x", markersize=15, color='blue')

	ax = plt.errorbar(peak_t_y, peak_th_y, xerr=0.1, color='green')

	# ------------------------------ plot Z ------------------------------------


	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,190000), ylim=(-10,10))
	ax.set_title('Acc_Z')
	lns1 = ax.plot(acc_t, acc_z, lw=2, color='black', label = 'acc_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	for index in range(0, step_counter_Z ,1):
		element_z = stroke_count_z_list[index].split(",")
		element_1z = element_z[0].split("[")
		element_2z = element_z[1].split("]")
		# print element_2z
		time_stemp = float(element_1z[1]) / 1000
		acc_value = round(float(element_2z[0]), 1)
		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1z[1], element_2z[0]),  xycoords='data', color='magenta',
			xytext=(1.5, 60), textcoords='offset points',
			arrowprops=dict(arrowstyle="->",
				connectionstyle="angle3,angleA=0,angleB=-90"),
		)

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,190000), ylim=(-10,10) )
	lns2 = ax.plot(peak_t_z, peak_acc_z, "ro", markersize=8, color='red')

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,190000), ylim=(-10,10) )
	lns2 = ax.plot(peak_t_z, peak_th_z, "ro", markersize=5, color='green')

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(413, autoscale_on=False, xlim=(0,190000), ylim=(-10,10) )
	lns2 = ax.plot(Time_Thresold_t_z, Time_Thresold_magnitude_z, "x", markersize=15, color='blue')

	ax = plt.errorbar(peak_t_z, peak_th_z, xerr=0.1, color='green')

	# ------------------------------ plot N ------------------------------------
	

	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(414, autoscale_on=False, xlim=(0,190000), ylim=(-5,5))
	ax.set_title('Acc_N')
	lns1 = ax.plot(acc_t, acc_N, lw=2, color='red', label = 'acc_N')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig.savefig(acc_xyz_file_root)
	plt.close(fig)

	# ------------------------------ plot End ------------------------------------

	final_step_count_x = 0
	final_step_count_y = 0
	final_step_count_z = 0

	if(step_freq_x < 1.3):
		final_step_count_x = step_counter *2
	else:
		final_step_count_x = step_counter

	if(step_freq_y < 1.3):
		final_step_count_y = step_counter_Y *2
	else:
		final_step_count_y = step_counter_Y

	if(step_freq_z < 1.3):
		final_step_count_z = step_counter_Z *2
	else:
		final_step_count_z = step_counter_Z




	return final_step_count_x, final_step_count_y, final_step_count_z



# print 425, step_count("20140718_170104_Foot_Walkfast_Dang_Ren_K89_425_0")
# print 400, step_count("20140718_170547_Foot_Walkfast_Dang_Lin_K89_400_0")
# print 200, step_count("20151105_111648_Foot_Walk_Dangle_Hsuanchao_Sony_200_0")
# print 200, step_count("20151105_112309_Foot_Walk_Inhand_Hsuanchao_Sony_200_0")
# print 200, step_count("20151105_112752_Foot_Walk_InPocket_Hsuanchao_Sony_200_0")
# print 200, step_count("20151105_113400_Foot_Walk_InPocket_Hsuanchao_Sony_200_0")
# print 200, step_count("20151106_155133_Foot_Walk_Dangle_Conlin_Sony_200_0")
# print 216, step_count("20151106_155624_Foot_Walk_Dangle_Conlin_Sony_216_0")
# print 200, step_count("20151106_161034_Foot_Walk_InHand_Brianz_Sony_200_0")
# print 200, step_count("20151106_161548_Foot_Walk_Dangle_Brianz_Sony_200_0")
# print 200, step_count("20151106_162336_Foot_Walk_InHand_ChengMinYuan_Sony_200_0")
# print 200, step_count("20151106_162933_Foot_Walk_Dangle_ChengMinYuan_Sony_200_0")

print 200, step_count("20151106_162336_Foot_Walk_InHand_ChengMinYuan_Sony_200_0", 10)