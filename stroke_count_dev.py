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
# import stroke_type
import true_turn_count
import true_stroke_count
import pool_length_function

def stroke_count( into_file_name ):
	file_name = into_file_name
	file_profile = file_name.split("_")
	# truth_turn = true_turn_count.true_turn_count(file_name)	 # get the truth_turn from file name
	# truth_count = true_stroke_count.true_stroke_count(file_name) # get the truth_stroke_turn from file name
	# pool_length = pool_length_function.pool_length_function(file_name) # get the pool length

	
# read and write files		
#------------------------------------------------------------------------------------------------------------------------
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/stroke_count"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/stroke_count")   
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/stroke_type"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/stroke_type")   

	input_acc_data = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc/acc_LPF_5Hz.txt", "r+") # input_acc_data
	input_gyro_data = open("./stroke_count_Evaluation/"+file_name+"/smoothen_gyro/smoothen_gyro.txt", "r+") # input_acc_data

	stroke_count_file_root = "./stroke_count_Evaluation/"+file_name+"/stroke_count/stroke_count.png"
	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/stroke_type/stroke_type.txt", "wb")
	
	acc_data = input_acc_data.readlines() # load data into python
	gyro_data = input_gyro_data.readlines()

	acc_length = len(acc_data)    # get how many data had being loaded 
	gyro_length = len(gyro_data)

#------------------------------------------------------------------------------------------------------------------------
# End of read and write files

# creat acc data for futher applications
#------------------------------------------------------------------------------------------------------------------------
	acc_t = []
	acc_x = []
	acc_y = []
	acc_z = []
	acc_z_HP = np.zeros(len(acc_data))
	acc_N = []
	acc_xy = []
	aplpha = 0.94
	aplpha_LP = 0.39
	init_Acc_Z = 1.0
	temp_element =acc_data[0].split(",")
	init_Acc_Z = float(temp_element[3])
	acc_z_HP[0] = float(init_Acc_Z)
	for index in range(0, len(acc_data), 1):
		element = acc_data[index].split(",")
		element_1 = element[5].split("\n")
		acc_t.append(int(element[0]))
		acc_x.append(float(element[1]))
		acc_y.append(float(element[2]))
		acc_z.append(float(element[3]))
		acc_N.append(float(element[4]))
		acc_xy.append(float(element_1[0]))
		if(index > 0):
			element_2 = acc_data[index-1].split(",")
			acc_z_HP[index] =  aplpha * ( float(acc_z_HP[index-1]) + float(element[3]) - float(element_2[3]) )

	for index in range(1, len(acc_z_HP), 1):
		acc_z_HP[index] = (aplpha_LP * acc_z_HP[index] + (1 - aplpha_LP) * acc_z_HP[index-1])

	for index in range(1, len(acc_z_HP), 1):
		acc_z_HP[index] = acc_z_HP[index] * -1

# End of creat acc data for futher applications
#------------------------------------------------------------------------------------------------------------------------
	gyro_t = []
	gyro_x = []
	gyro_y = []
	gyro_z = []
	for index2 in range(0, len(gyro_data), 1):
		element2 = gyro_data[index2].split(",")
		element_2 = element2[3].split("\n")
		gyro_t.append(int(element2[0]))
		gyro_x.append(float(element2[1]))
		gyro_y.append(float(element2[2]))
		gyro_z.append(float(element_2[0]))
# stroke count for acc_xy 
#--------------------------------------------------------------------------------------------------------------------------------------------
	max_in_ten_sec = 0
	second_max_in_ten_sec = 0
	
	acc_x_sum = 0
	acc_xSQ_sum = 0
	
	acc_y_sum = 0
	acc_ySQ_sum = 0

	acc_z_sum = 0
	acc_zSQ_sum = 0
	peak_begin = [0, 0]
	list_of_peak_begin = []
	sorted_list_of_peak_begin = [0, 0, 0]
	inti_time_interval = 0.0
	inti_time_amplitude_interval = 0.0

	initi_counter = 0
	initi_position = 0

	for index0001 in range(1, 400, 1):
		element1 = acc_data[index0001].split(",")
		element1_1 = element1[5].split("\n")
		acc_xy_now = element1_1[0]
		# print acc_xy_now

		if(float(acc_xy_now) > 13.0 and initi_counter ==0):
			initi_counter += 1
			# print "initi_counter=", initi_counter
			# print "haha"
			initi_position = index0001
			# if(int(initi_counter) == 5):
				
	# print "initi_position=", initi_position
	


	for index00 in range(initi_position-20, initi_position+180, 1):
		element0 = acc_data[index00-1].split(",")
		element1 = acc_data[index00].split(",")
		element2 = acc_data[index00+1].split(",")

		acc_bt = int(element1[0])

		element1_1 = element1[5].split("\n")
		acc_xy_now = element1_1[0]

		element0_1 = element0[5].split("\n")
		acc_xy_pre = element0_1[0]

		element2_1 = element2[5].split("\n")
		acc_xy_next = element2_1[0]
		peak_begin = [0 , 0]

		if( (float(acc_xy_now) - float(acc_xy_pre) > 0) &   (float(acc_xy_now) - float(acc_xy_next) > 0) ):
			peak_begin[0] = int(acc_bt)
			peak_begin[1] = float(acc_xy_now)
			list_of_peak_begin.append(peak_begin)
	# print list_of_peak_begin
	for index001 in range(0, 3, 1):
		sorted_list_of_peak_begin[index001] = sorted(list_of_peak_begin, reverse=True, key = lambda x : x[1])[index001]
	# print sorted(sorted_list_of_peak_begin)
	# print int(sorted(sorted_list_of_peak_begin)[1][0]) - int(sorted(sorted_list_of_peak_begin)[0][0])
	# print int(sorted(sorted_list_of_peak_begin)[2][0]) - int(sorted(sorted_list_of_peak_begin)[1][0])

	inti_time_interval = (int(sorted(sorted_list_of_peak_begin)[1][0]) - int(sorted(sorted_list_of_peak_begin)[0][0]) +
                          int(sorted(sorted_list_of_peak_begin)[2][0]) - int(sorted(sorted_list_of_peak_begin)[1][0])
                          ) / 2.0
	# print "inti_time_interval 01 =", inti_time_interval

	# print sorted(sorted_list_of_peak_begin)[0][0]
	inti_time_amplitude_interval = (float(sorted(sorted_list_of_peak_begin)[0][1]) + 
	                                float(sorted(sorted_list_of_peak_begin)[1][1]) + 
	                                float(sorted(sorted_list_of_peak_begin)[2][1])
	                                ) / 3.0

	# first_index = 0

	# for index002 in range(1, 200, 1):
	# 	element1 = acc_data[index002].split(",")
	# 	acc_bt = int(element1[0])
	# 	if(int(sorted(sorted_list_of_peak_begin)[0][0]) == int(acc_bt) ):
	# 		first_index = index002
	# list_of_peak_begin = []

	# for index003 in range(first_index-10, first_index+120, 1):
	# 	element0 = acc_data[index003-1].split(",")
	# 	element1 = acc_data[index003].split(",")
	# 	element2 = acc_data[index003+1].split(",")

	# 	acc_bt = int(element1[0])

	# 	element1_1 = element1[5].split("\n")
	# 	acc_xy_now = element1_1[0]

	# 	element0_1 = element0[5].split("\n")
	# 	acc_xy_pre = element0_1[0]

	# 	element2_1 = element2[5].split("\n")
	# 	acc_xy_next = element2_1[0]
	# 	peak_begin = [0 , 0]

	# 	if( (float(acc_xy_now) - float(acc_xy_pre) > 0) &   (float(acc_xy_now) - float(acc_xy_next) > 0) ):
	# 		peak_begin[0] = int(acc_bt)
	# 		peak_begin[1] = float(acc_xy_now)
	# 		list_of_peak_begin.append(peak_begin)
	# # print list_of_peak_begin
	# for index001 in range(0, 3, 1):
	# 	sorted_list_of_peak_begin[index001] = sorted(list_of_peak_begin, reverse=True, key = lambda x : x[1])[index001]
	# print sorted(sorted_list_of_peak_begin)
	# print int(sorted(sorted_list_of_peak_begin)[1][0]) - int(sorted(sorted_list_of_peak_begin)[0][0])
	# print int(sorted(sorted_list_of_peak_begin)[2][0]) - int(sorted(sorted_list_of_peak_begin)[1][0])

	# inti_time_interval = (int(sorted(sorted_list_of_peak_begin)[1][0]) - int(sorted(sorted_list_of_peak_begin)[0][0]) +
 #                          int(sorted(sorted_list_of_peak_begin)[2][0]) - int(sorted(sorted_list_of_peak_begin)[1][0])
 #                          ) / 2.0

	# inti_time_amplitude_interval = (float(sorted(sorted_list_of_peak_begin)[0][1]) + 
	#                                 float(sorted(sorted_list_of_peak_begin)[1][1]) + 
	#                                 float(sorted(sorted_list_of_peak_begin)[2][1])
	#                                 ) / 3.0
	# print sorted(sorted_list_of_peak_begin)

	# print "inti_time_interval 02 =", inti_time_interval
	# print "inti_time_amplitude_interval=", inti_time_amplitude_interval





	




	for index in range(0, 400, 1): # peek the first 20 seconds data get the Max
		element1 = acc_data[index].split(",")

		acc_x_sum += float(element1[1])
		acc_xSQ_sum += pow(float(element1[1]),2)

		acc_y_sum += float(element1[2])
		acc_ySQ_sum += pow(float(element1[2]),2)
		# print acc_y_sum
		# print acc_ySQ_sum

		acc_z_sum += float(element1[3])
		acc_zSQ_sum += pow(float(element1[3]),2)


		element1_1 = element1[5].split("\n")
		acc_xy_now = element1_1[0]
		if(float(max_in_ten_sec) < float(acc_xy_now)):
			max_in_ten_sec = float(acc_xy_now)
			index_place = index
	# print "index_place",index_place
	# print "max_in_ten_sec", max_in_ten_sec

	
	# print "STD X=",sqrt((acc_xSQ_sum / 200)  -  pow( (float(acc_x_sum) / 200), 2))
	# print "STD Y=",sqrt((acc_ySQ_sum / 200)  -  pow( (float(acc_y_sum) / 200), 2))
	# print "STD Z=",sqrt((acc_zSQ_sum / 200)  -  pow( (float(acc_z_sum) / 200), 2))
	STD_X = sqrt((acc_xSQ_sum / 400)  -  pow( (float(acc_x_sum) / 400), 2))	
	STD_Y = sqrt((acc_ySQ_sum / 400)  -  pow( (float(acc_y_sum) / 400), 2))
	STD_Z = sqrt((acc_zSQ_sum / 400)  -  pow( (float(acc_z_sum) / 400), 2))

	# print "( STD_X,  STD_Y, STD_Z )= (", STD_X, ",",  STD_Y, ",", STD_Z,")"

	list_of_peak = []
	for index02 in range(index_place+20, index_place+120, 1):
		
		element0 = acc_data[index02-1].split(",")
		element1 = acc_data[index02].split(",")
		element2 = acc_data[index02+1].split(",")

		element1_1 = element1[5].split("\n")
		acc_xy_now = element1_1[0]

		element0_1 = element0[5].split("\n")
		acc_xy_pre = element0_1[0]

		element2_1 = element2[5].split("\n")
		acc_xy_next = element2_1[0]

		if( (float(acc_xy_now) - float(acc_xy_pre) > 0) &   (float(acc_xy_now) - float(acc_xy_next) > 0) ):
			list_of_peak.append(float(acc_xy_now))
	
	# print list_of_peak
	# print "after sorting"
	# print sorted(list_of_peak, reverse=True)
	
	Avg_in_three = 0
	list_of_peak_rev = sorted(list_of_peak, reverse=True)
	for index in range(0 , 2, 1):
		Avg_in_three += float(list_of_peak_rev[index])
	# print "Avg_in_three= ", Avg_in_three / 2.0
	Avg_in_three = Avg_in_three / 2.0

	time_down_grade_ratio = 0.72
	range_of_local_max = 18

	# print float(Avg_in_three)

	# show that this is a first tier swimmer (Class 1)
	if(float(Avg_in_three) > 25.0 ): 
		initial_Threshold = 25
		down_grade_ratio = 0.70
		time_interval_threshold = 1900
	# show that this is a second tier swimmer (Class 2)
	elif( (float(Avg_in_three) <= 25.0) & (float(Avg_in_three) > 19.0) ):
		initial_Threshold = 16
		down_grade_ratio = 0.78
		time_interval_threshold = 1750

	elif(float(Avg_in_three) <= 19.0 ):
		initial_Threshold = 12
		down_grade_ratio = 0.55
		time_interval_threshold = 1880
	else:
		print "Error occurred!!"

	time_interval_threshold = inti_time_interval * 0.8
	initial_Threshold = inti_time_amplitude_interval * 0.8
	# print "time_interval_threshold=", time_interval_threshold
	# print "initial_Threshold=", initial_Threshold

	# print "initial_Threshold =", initial_Threshold
	# print ""

	#initialization
	SC_indicator = 0
	MTK_turn_count = 0
	MTK_turn_count_at_SC = 0
	
	peak_point_xy = [0, 0, 0]
	stroke_count_xy = [0, 0, 0]
	pre_stroke_count_xy = [0, 0, 0]
	peak_point_xy_list = []
	stroke_count_xy_list = []
	Time_threshold_xy_list = []
	stroke_interval_now = 0
	stroke_interval_pre = 0
	stroke_interval_diff = 0
	Stroke_Time_Diff_Interval_list = []
	Diff_of_Stroke_Time_Diff_Int_list =[]
	turn_count_position = 0
	turn_detect = 0
	type_STD = [0, 0, 0]
	type_STD_list = []
	# inspect 3 data at a time  (t-1, t, t+1)
	for index in range(1, len(acc_data)-1, 1):

		element0 = acc_data[index-1].split(",")
		element1 = acc_data[index].split(",")
		element2 = acc_data[index+1].split(",")

		element0_1 = element0[5].split("\n")
		element1_1 = element1[5].split("\n")
		element2_1 = element2[5].split("\n")
		
		acc_xy_pre = element0_1[0]
		acc_xy_now = element1_1[0]
		acc_xy_next = element2_1[0]

		acc_z_pre  = element0[3]
		acc_z_now  = element1[3]
		acc_z_next = element2[3]
		
		# For the 1st stroke count ------------------------------------------------------------------------------------------------
		if (SC_indicator == 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0
			if( (float(acc_xy_now) > initial_Threshold) or (float(acc_xy_next) > initial_Threshold) ): # over Threshold
				if((float(acc_xy_next) - float(acc_xy_now) < 0) & (float(acc_xy_now) - float(acc_xy_pre) > 0)): # Is a Peak
					# check for Local Max within 1 sec data
					
					peak_point_xy[0] = int(element1[0])
					peak_point_xy[1] = float(acc_xy_now)
					peak_point_xy[2] = float(initial_Threshold)
					peak_point_xy_list.append(str(peak_point_xy))

					max_in_ten_sample = float(acc_xy_now)
					max_in_ten_sample_time = int(element1[0])

					for index2 in range(1, 21, 1): # 20*50 = 1000 (1 second)
						element_f = acc_data[index+index2].split(",")
						element_f_1 = element_f[5].split("\n")
						# print element_f[0]
						acc_xy_future = element_f_1[0]
						if(float(acc_xy_future) > max_in_ten_sample):
							max_in_ten_sample = float(acc_xy_future)
							max_in_ten_sample_time = int(element_f[0])
							# print max_in_ten_sample_time, max_in_ten_sample

					SC_indicator = SC_indicator + 1
					# print acc_xy_now, acc_xy_next

					stroke_count_xy[0] = int(max_in_ten_sample_time)
					stroke_count_xy[1] = float(max_in_ten_sample)
					stroke_count_xy[2] = float(initial_Threshold)
					stroke_count_xy_list.append(str(stroke_count_xy))
					
					pre_stroke_count_xy[0] = int(stroke_count_xy[0])
					pre_stroke_count_xy[1] = float(stroke_count_xy[1])
					pre_stroke_count_xy[2] = float(stroke_count_xy[2])


					

					# print "stroke count =", SC_indicator
					# print "initial_Threshold =",initial_Threshold
					# print "sample_time =", int(stroke_count_xy[0])
					# print "sample_value =", float(stroke_count_xy[1])
					# print "time_interval_threshold =", time_interval_threshold
					# print " "

					Time_threshold_xy_list.append(str(time_interval_threshold))
		# End of the 1st stroke count ------------------------------------------------------------------------------------------------

		# For the stroke count >= 1
		elif (SC_indicator > 0):
			max_in_ten_sample = 0
			max_in_ten_sample_time = 0
			sample_index = 0
			sample_type_interval = 0
			
			if(float(time_interval_threshold) > 1500):
				time_interval_threshold = 1500
			if(  (int(element1[0]) - int(element0[0])) > 1000 ):# for data Lost
				time_interval_threshold = 1500
			if( (int(element1[0]) - int(pre_stroke_count_xy[0]) >= time_interval_threshold) & (int(element1[0]) - int(pre_stroke_count_xy[0]) < 15000) ): # over time Threshold
				if( (float(acc_xy_now) > FCS_Threshold) or (float(acc_xy_next) > FCS_Threshold) ):  # over acc Threshold
					if( (float(acc_xy_next) - float(acc_xy_now) < 0) & (float(acc_xy_now) - float(acc_xy_pre) > 0) ): # Is a Peak
						
						peak_point_xy[0] = int(element1[0])
						peak_point_xy[1] = float(acc_xy_now)
						peak_point_xy[2] = float(FCS_Threshold)
						peak_point_xy_list.append(str(peak_point_xy))

						max_in_ten_sample = float(acc_xy_now)
						max_in_ten_sample_time = int(element1[0])
						sample_index = index

						for index2 in range(1, range_of_local_max, 1):
							# print index+index2
							element_ff = acc_data[index+index2].split(",")
							element_ff_1 = element_ff[5].split("\n")
							acc_xy_future = element_ff_1[0]
							if(float(acc_xy_future) > max_in_ten_sample):
								max_in_ten_sample = float(acc_xy_future)
								max_in_ten_sample_time = int(element_ff[0])
								sample_index = index+index2

						SC_indicator = SC_indicator + 1
						# print "SC_indicator",SC_indicator

						# print "time_interval_threshold=", time_interval_threshold
						# print FCS_Threshold
						

						stroke_count_xy[0] = int(max_in_ten_sample_time)
						stroke_count_xy[1] = float(max_in_ten_sample)
						stroke_count_xy[2] = float(FCS_Threshold)
						stroke_count_xy_list.append(str(stroke_count_xy))

						# print stroke_count_xy[0], stroke_count_xy[1], (max_in_ten_sample_time - pre_stroke_count_xy[0]), sample_index
						sample_type_interval = (max_in_ten_sample_time - pre_stroke_count_xy[0]) / 50
						# print "sample_type_interval =", sample_type_interval
						sum_for_type_acc_X = 0
						SQ_sum_for_type_acc_X = 0
						sum_for_type_acc_Y = 0
						SQ_sum_for_type_acc_Y = 0
						sum_for_type_acc_Z = 0
						SQ_sum_for_type_acc_Z = 0
						STD_X_type, STD_Y_type, STD_Z_type = 0, 0, 0
						for index3 in range(sample_index - sample_type_interval, sample_index, 1):
							element3 = acc_data[index3].split(",")
							# print element3[1], element3[2], element3[3]
							sum_for_type_acc_X += float(element3[1])
							SQ_sum_for_type_acc_X  += float(element3[1]) ** 2 
							sum_for_type_acc_Y += float(element3[2])
							SQ_sum_for_type_acc_Y  += float(element3[2]) ** 2 
							sum_for_type_acc_Z += float(element3[3])
							SQ_sum_for_type_acc_Z += float(element3[3]) ** 2  

						STD_X_type = ((float(SQ_sum_for_type_acc_X) / sample_type_interval) - ( float(sum_for_type_acc_X) / sample_type_interval ) ** 2  ) ** 0.5 
						STD_Y_type = ((float(SQ_sum_for_type_acc_Y) / sample_type_interval) - ( float(sum_for_type_acc_Y) / sample_type_interval ) ** 2  ) ** 0.5 
						STD_Z_type = ((float(SQ_sum_for_type_acc_Z) / sample_type_interval) - ( float(sum_for_type_acc_Z) / sample_type_interval ) ** 2  ) ** 0.5 
						
						# print "STD =" , STD_X_type, STD_Y_type, STD_Z_type
						type_STD[0] = STD_X_type
						type_STD[1] = STD_Y_type
						type_STD[2] = STD_Z_type
						type_STD_list.append(str(type_STD))




						Stroke_Time_Diff_Interval_list.append(int(max_in_ten_sample_time) - int(pre_stroke_count_xy[0]))
						if(SC_indicator >= 3):
							Diff_of_Stroke_Time_Diff_Int_list.append(int(Stroke_Time_Diff_Interval_list[-1]) - int(Stroke_Time_Diff_Interval_list[-2]))

						# print "SC_indicator", SC_indicator
						# print max_in_ten_sample_time

						# STD_IN_TEN = 0
						# if(pool_length == 50):  
						# 	if( SC_indicator == 14 ):
						# 		sum_of_the_Diff = 0
						# 		SQ_sum_of_the_Diff = 0
								
						# 		# print "len(Diff_of_Stroke_Time_Diff_Int_list)", len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "SC_indicator", SC_indicator
						# 		for index in range(2, len(Diff_of_Stroke_Time_Diff_Int_list), 1):
						# 			sum_of_the_Diff += Diff_of_Stroke_Time_Diff_Int_list[index]
						# 			SQ_sum_of_the_Diff += int(Diff_of_Stroke_Time_Diff_Int_list[index])**2
						# 		STD_IN_TEN = ((SQ_sum_of_the_Diff / 10) - (sum_of_the_Diff / 10 ) **2) ** 0.5
						# 		# print "STD_IN_TEN", STD_IN_TEN
						# 		if( (float(STD_IN_TEN) > 150) and (float(STD_IN_TEN) < 400)):
						# 			turn_count_threshold = -1600
						# 		elif(float(STD_IN_TEN) > 400):
						# 			turn_count_threshold = -3500
						# 		else:
						# 			turn_count_threshold = -1400


						# if(pool_length == 25):  
						# 	if( SC_indicator == 8 ):
						# 		sum_of_the_Diff = 0
						# 		SQ_sum_of_the_Diff = 0
						# 		# print "len(Diff_of_Stroke_Time_Diff_Int_list)", len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "SC_indicator", SC_indicator
						# 		for index in range(2, len(Diff_of_Stroke_Time_Diff_Int_list), 1):
						# 			sum_of_the_Diff += Diff_of_Stroke_Time_Diff_Int_list[index]
						# 			SQ_sum_of_the_Diff += int(Diff_of_Stroke_Time_Diff_Int_list[index])**2
						# 		STD_IN_TEN = ((SQ_sum_of_the_Diff / 6) - (sum_of_the_Diff / 6 ) **2) ** 0.5
						# 		# print "STD_IN_TEN", STD_IN_TEN
						# 		if( (float(STD_IN_TEN) > 150) and (float(STD_IN_TEN) < 400)):
						# 			turn_count_threshold = -1600
						# 		elif(float(STD_IN_TEN) > 400):
						# 			turn_count_threshold = -3500
						# 		else:
						# 			turn_count_threshold = -1400


						
						# if((SC_indicator > 13) and (turn_count_position == 0) and (pool_length == 50) ):
						# 	if(( Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]) <= turn_count_threshold):
						# 		turn_count_position = len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "turn_count_position", turn_count_position
						# 		turn_detect = Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]
						# 		# print "SC_indicator", SC_indicator
						# 		# print "len(Diff_of_Stroke_Time_Diff_Int_list)", len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		MTK_turn_count = 1
						# 		MTK_turn_count_at_SC = SC_indicator
						# 		# print "MTK_turn_count_at_SC", MTK_turn_count_at_SC
						# 		# print "MTK_turn_count", MTK_turn_count
						# if( (turn_count_position != 0) and (SC_indicator <= turn_count_position+14) and (pool_length == 50) ):
						# 	if(( Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]) <= turn_detect):
						# 		turn_count_position = len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "turn_count_position", turn_count_position
						# 		MTK_turn_count_at_SC = SC_indicator
						# 		# print "MTK_turn_count_at_SC", MTK_turn_count_at_SC
						# 		# print "MTK_turn_count", MTK_turn_count

						# if((turn_count_position != 0) and (SC_indicator > turn_count_position+14) and (pool_length == 50) ):
						# 	if(( Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]) <= turn_count_threshold):
						# 		turn_count_position = len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		MTK_turn_count += 1
						# 		MTK_turn_count_at_SC = SC_indicator
						# 		# print "turn_count_position", turn_count_position
						# 		# print "SC_indicator", SC_indicator
						# 		# print "len(Diff_of_Stroke_Time_Diff_Int_list)", len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "MTK_turn_count", MTK_turn_count

						# if((SC_indicator > 8) and (turn_count_position == 0) and (pool_length == 25) ):
						# 	if(( Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]) <= turn_count_threshold):
						# 		turn_count_position = len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "turn_count_position", turn_count_position
						# 		turn_detect = Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]
						# 		# print "SC_indicator", SC_indicator
						# 		# print "len(Diff_of_Stroke_Time_Diff_Int_list)", len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		MTK_turn_count = 1
						# 		MTK_turn_count_at_SC = SC_indicator
						# 		# print "MTK_turn_count_at_SC", MTK_turn_count_at_SC
						# 		# print "1st one"
						# 		# print "MTK_turn_count =", MTK_turn_count
						# if( (turn_count_position != 0) and (SC_indicator <= turn_count_position+5) and (pool_length == 25) ):
						# 	if(( Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]) <= turn_detect):
						# 		turn_count_position = len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "turn_count_position", turn_count_position
						# 		MTK_turn_count_at_SC = SC_indicator
						# 		# print "MTK_turn_count_at_SC", MTK_turn_count_at_SC
						# 		# print "MTK_turn_count =", MTK_turn_count

						# if((turn_count_position != 0) and (SC_indicator > turn_count_position+5) and (pool_length == 25) ):
						# 	if(( Diff_of_Stroke_Time_Diff_Int_list[-1] - Diff_of_Stroke_Time_Diff_Int_list[-2]) <= turn_count_threshold):
						# 		turn_count_position = len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		MTK_turn_count += 1
						# 		MTK_turn_count_at_SC = SC_indicator
						# 		# print "hihih"
						# 		# print "turn_count_position", turn_count_position
						# 		# print "SC_indicator", SC_indicator
						# 		# print "len(Diff_of_Stroke_Time_Diff_Int_list)", len(Diff_of_Stroke_Time_Diff_Int_list)
						# 		# print "MTK_turn_count =", MTK_turn_count



						# stroke_interval_diff = stroke_interval_now - stroke_interval_pre
						# # print SC_indicator, stroke_interval_diff
						# if(SC_indicator > 10 and stroke_interval_diff > 1000):
						# 	turn_count += 1
						# 	# print turn_count


						pre_stroke_count_xy[0] = int(stroke_count_xy[0])
						pre_stroke_count_xy[1] = float(stroke_count_xy[1])
						pre_stroke_count_xy[2] = float(stroke_count_xy[2])

						Time_threshold_xy_list.append(str(time_interval_threshold))
						# stroke_interval_pre = stroke_interval_now

						# print "stroke count =", SC_indicator	
						# print "sample_time =", max_in_ten_sample_time 
						# print "sample_value =", float(stroke_count_xy[1]) 
						# print "FCS_Threshold =", FCS_Threshold
						# print "time_interval_threshold =", time_interval_threshold
						# print "index=", index
						# print ""
						
		if (SC_indicator == 1):
			element = stroke_count_xy_list[0].split(",")
			element1 = element[1].split("]")
			# FCS_Threshold = 10
			FCS_Threshold = float(element1[0]) * down_grade_ratio 
			if( float(FCS_Threshold) < 8.0):
				FCS_Threshold = 8.0
			elif(float(FCS_Threshold) > 25.0):
				FCS_Threshold = 25.0
		elif (SC_indicator == 2):
			element = stroke_count_xy_list[0].split(",")
			element1 = element[1].split("]")
			element_1 = stroke_count_xy_list[1].split(",")
			element_11 = element_1[1].split("]")
			# FCS_Threshold = 10
			FCS_Threshold = (float(element1[0]) + float(element_11[0])) /2 * down_grade_ratio
			if( float(FCS_Threshold) < 8.0):
				FCS_Threshold = 8.0
			elif(float(FCS_Threshold) > 25.0):
				FCS_Threshold = 25.0
				
		elif (SC_indicator >= 3):
			FCS_Threshold = 0

			# for index in range(len(stroke_count_xy_list)-3, len(stroke_count_xy_list), 1):
			# 	element = stroke_count_xy_list[index].split(",")
			# 	element1 = element[1].split("]")
			# 	FCS_Threshold = FCS_Threshold + float(element1[0])
			
			
			index_temp = 0
			
			for index in range(len(stroke_count_xy_list)-3, len(stroke_count_xy_list), 1):
				element = stroke_count_xy_list[index].split(",")
				element1 = element[1].split("]")
				FCS_Threshold = FCS_Threshold + float(element1[0])*(index_temp+1)
				index_temp += 1
	
			

			FCS_Threshold = float(FCS_Threshold) / 6 * down_grade_ratio
			if( float(FCS_Threshold) < inti_time_amplitude_interval * 0.6):
				FCS_Threshold = inti_time_amplitude_interval * 0.6
			elif( float(FCS_Threshold) < 9):
				FCS_Threshold = 9
			elif(float(FCS_Threshold) > inti_time_amplitude_interval * 0.9 ):
				FCS_Threshold = inti_time_amplitude_interval * 0.9
			elif(float(FCS_Threshold) > 25 ):
				FCS_Threshold = 25


			if( SC_indicator >= 6 ):
				temp = [0, 0, 0, 0, 0, 0]
				jitter = 0 
				index_temp_02 = 0
				
				for index in range(len(stroke_count_xy_list)-6, len(stroke_count_xy_list), 1):
					# print index
					element = stroke_count_xy_list[index].split(",")
					element1 = element[1]
					temp[index_temp_02] = float(element1)
					index_temp_02 += 1
				
				jitter = float(
					           abs( float(temp[0]) - float(temp[1]) ) + 
					           abs( float(temp[1]) - float(temp[2]) ) +
					           abs( float(temp[2]) - float(temp[3]) ) +
					           abs( float(temp[3]) - float(temp[4]) ) +
					           abs( float(temp[4]) - float(temp[5]) ) 
					           ) / 5
				# print SC_indicator, jitter
				if((jitter < 2) and (float(stroke_count_xy[1]) > 18.0  ) ):
					down_grade_ratio = 0.80
				elif((jitter > 2)):
					down_grade_ratio = 0.60



			


		


			time_interval_threshold = 2000
			temp_time_interval_threshold_1 = 0
			temp_time_interval_threshold_2 = 0
			pre_time_interval_threshold = 2000 

			element = stroke_count_xy_list[len(stroke_count_xy_list)-1].split(",")
			element_1 = element[0].split("[")
			element2 = stroke_count_xy_list[len(stroke_count_xy_list)-2].split(",")
			element_2 = element2[0].split("[")
			temp_time_interval_threshold_1 = int(element_1[1]) - int(element_2[1])

			element2 = stroke_count_xy_list[len(stroke_count_xy_list)-2].split(",")
			element2_1 = element2[0].split("[")
			element22 = stroke_count_xy_list[len(stroke_count_xy_list)-3].split(",")
			element2_2 = element22[0].split("[")
			temp_time_interval_threshold_2 = int(element2_1[1]) - int(element2_2[1])

			if( (temp_time_interval_threshold_1 < 3500) & (temp_time_interval_threshold_2 < 3500)  ): # normal stroke count time interval
				# time_interval_threshold = (float( temp_time_interval_threshold_1 + temp_time_interval_threshold_2 ) / 2) * 0.7
				time_interval_threshold = min(float( temp_time_interval_threshold_1), float(temp_time_interval_threshold_2) ) * time_down_grade_ratio
			elif( temp_time_interval_threshold_1 > 4500): # shows that turn occor
				time_interval_threshold = float(temp_time_interval_threshold_2) * time_down_grade_ratio

			
				
				# print int(temp_time_interval_threshold_1) , int(temp_time_interval_threshold_2)

		if( time_interval_threshold <= inti_time_interval * 0.8 ):
			time_interval_threshold =  inti_time_interval * 0.8
		if( time_interval_threshold >= inti_time_interval * 1.2 ):
			time_interval_threshold =  inti_time_interval * 1.2
		if( STD_X > 8):
			time_interval_threshold = 1100
			range_of_local_max = 15
			down_grade_ratio = 0.70
		if( (STD_Z > 5) and (STD_X < 3) and (STD_Z > STD_Y > STD_X)):
			time_interval_threshold = 1700
		if( (STD_Z > 8) and (STD_Z > STD_Y ) and (STD_Z > STD_X) ):
			time_interval_threshold = 1400
			down_grade_ratio = 0.65

		




			# for index002 in range(len(peak_point_list_xy), len(peak_point_list_xy)-2, -1):
				
			# 	element = peak_point_list_xy[index002-1].split(",")
			# 	element_1 = element[0].split("[")

			# 	element2 = peak_point_list_xy[index002-2].split(",")
			# 	element_2 = element2[0].split("[")

			# 	temp_time_interval_threshold += int(element_1[1]) - int(element_2[1])
			# time_interval_threshold = (float(temp_time_interval_threshold) / 2) * 0.9
			
			







	# print len(stroke_count_xy_list)
	# stroke_time_interval = 0
	# for index in range(1, len(stroke_count_xy_list), 1):
	# 	element = stroke_count_xy_list[index].split(",")
	# 	element_1 = element[0].split("[")
	# 	element_2 = element[1].split("]")

	# 	element1 = stroke_count_xy_list[index-1].split(",")
	# 	element1_1 = element1[0].split("[")
	# 	element1_2 = element1[1].split("]")
		
	# 	stroke_time_interval = stroke_time_interval + ( int(element_1[1]) - int(element1_1[1]))

	# print float(stroke_time_interval) / (len(stroke_count_xy_list) -1)
	peak_t = []
	peak_acc = []
	peak_th = []
	for index in range(0, len(peak_point_xy_list), 1):
		element = peak_point_xy_list[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[2].split("]")

		peak_t.append(int(element_1[1]))
		peak_acc.append(float(element[1]))
		peak_th.append(float(element_2[0]))
	# print peak_th

	Time_Thresold_t = []
	Time_Thresold_magnitude = [] 
	magnitude = 0
	for index in range(0, len(Time_threshold_xy_list), 1):
		element = peak_point_xy_list[index].split(",")
		element_1 = element[0].split("[")
		# print int(element_1[1])
		element_2 = element[2].split("]")
		magnitude = element_2[0].strip()
		Time_Thresold_t.append( int(int(element_1[1])  + float(Time_threshold_xy_list[index]))  )  
		Time_Thresold_magnitude.append(float(magnitude)-2)

	# # global MTK_turn_count_at_SC
	# if(pool_length == 50):
	# 	if (int(SC_indicator) - int(MTK_turn_count_at_SC)  < 10 ):
	# 		MTK_turn_count -=1
	# if(pool_length == 25):
	# 	if (int(SC_indicator) - int(MTK_turn_count_at_SC)  < 6 ):
	# 		MTK_turn_count -=1

	# print "1. MTK_turn_count= ", MTK_turn_count
	# print "2. truth_turn=", truth_turn
	# print "3. truth_turn - MTK_turn_count=", int(truth_turn) - int(MTK_turn_count)
	# print  ( (int(truth_turn) == int(MTK_turn_count)  )

	# if ( int(truth_turn) - int(MTK_turn_count) != 0):
	# 	print "Turn count error =", MTK_turn_count - truth_turn
	# 	print "truth Turn count =", truth_turn
	# 	print "conlin_TC=", MTK_turn_count
	# print "conlin_TC=", MTK_turn_count


	# print "SC_indicator", SC_indicator		

	# print "MTK_turn_count = ", MTK_turn_count
	# print "stroke_count = ",SC_indicator
	# print "Stroke_Time_Diff_Interval_list", Stroke_Time_Diff_Interval_list
	# print "Diff_of_Stroke_Time_Diff_Int_list", Diff_of_Stroke_Time_Diff_Int_list
	# print type_STD_list
	# print len(type_STD_list)
	for index04 in range(0, len(type_STD_list)-1, 1):
		# print type_STD_list[index04]
		file_write_to.write( str( type_STD_list[index04] )+ "\n" );
	
	file_write_to.write( str( type_STD_list[len(type_STD_list)-1] )+ "\n" );	

	file_write_to.close()
# END of stroke count for acc_xy ----------------------------------------------------------------------------------------------------------


	# stroke_count_Acc_z_HP = 0
	# stroke_count_Acc_z_HP_position = [0, 1.0]
	# stroke_count_Acc_z_HP_position_peak = [0, 1.0]
	# stroke_count_Acc_z_HP_list = []
	# stroke_count_Acc_z_HP_list_peak = []
	# temp_position = 0
	# min_in_local = 0
	# min_in_local_index = 0
	# max_in_local = 0.0
	# max_in_local_index = 0

	# pre_stroke_count_Acc_z_HP_position_t = 0 
	# pre_stroke_count_Acc_z_HP_position_m = 0.0
	# pre_stroke_count_Acc_z_HP_peak_position_t = 0 
	# pre_stroke_count_Acc_z_HP_peak_position_m = 0.0

	# for index in range(10, len(acc_z_HP)-1, 1):
	# 	if(stroke_count_Acc_z_HP ==0):
	# 		if(acc_z_HP[index] < -4):
	# 			if(  (float(acc_z_HP[index]) - float(acc_z_HP[index-1]) )  < 0  and  (float(acc_z_HP[index]) - float(acc_z_HP[index+1]) ) < 0):
	# 				min_in_local_index = index
	# 				temp_position_m = float(acc_z_HP[index])
	# 				min_in_local = float(acc_z_HP[index])
	# 				for index_find_valley in range(index+1, index+20, 1):
	# 					if(float(acc_z_HP[index_find_valley]) <  float(temp_position_m) ):
	# 						min_in_local_index = index_find_valley
	# 						min_in_local = float(acc_z_HP[index_find_valley])
	# 				# print "local min", min_in_local_index, min_in_local
					

	# 				for index_find_peak in range(min_in_local_index+1, min_in_local_index+40, 1):
	# 					if( float(acc_z_HP[index_find_peak]) >  float(max_in_local) ):
	# 						max_in_local_index = int(index_find_peak)
	# 						max_in_local = float(acc_z_HP[index_find_peak])
	# 				# print "local max", max_in_local_index, max_in_local
	# 				# print "diff=", max_in_local - min_in_local
	# 				if(  (float(max_in_local) - float(min_in_local))  > 15.0):
	# 					stroke_count_Acc_z_HP_position_peak[0] = int(acc_t[max_in_local_index])
	# 					stroke_count_Acc_z_HP_position_peak[1] = float(max_in_local)
	# 					stroke_count_Acc_z_HP_list_peak.append(str(stroke_count_Acc_z_HP_position_peak))

	# 					pre_stroke_count_Acc_z_HP_peak_position_t = int(acc_t[max_in_local_index])
	# 					pre_stroke_count_Acc_z_HP_peak_position_m = float(max_in_local)

	# 					stroke_count_Acc_z_HP += 1
	# 					stroke_count_Acc_z_HP_position[0] = int(acc_t[min_in_local_index])
	# 					stroke_count_Acc_z_HP_position[1] = float(min_in_local)
	# 					stroke_count_Acc_z_HP_list.append(str(stroke_count_Acc_z_HP_position))

	# 					pre_stroke_count_Acc_z_HP_position_t = int(acc_t[min_in_local_index])
	# 					pre_stroke_count_Acc_z_HP_position_m = float(min_in_local)

	# 	if(stroke_count_Acc_z_HP > 0):
	# 		if(  (int(acc_t[index]) - int(pre_stroke_count_Acc_z_HP_position_t) ) > 800):
	# 			if(acc_z_HP[index] < -1): # Lower than a threshold
	# 				if(  (float(acc_z_HP[index]) - float(acc_z_HP[index-1]) )  < 0  and  (float(acc_z_HP[index]) - float(acc_z_HP[index+1]) ) < 0): # is a valley
	# 					min_in_local_index = index
	# 					temp_position_m = float(acc_z_HP[index])
	# 					min_in_local = float(acc_z_HP[index])
	# 					for index_find_valley in range(index-10, index+20, 1): # get the local min in 1 sec
	# 						if(float(acc_z_HP[index_find_valley]) <  float(temp_position_m) ):
	# 							min_in_local_index = index_find_valley
	# 							min_in_local = float(acc_z_HP[index_find_valley])
	# 					# print "local min", min_in_local_index, min_in_local

	# 					max_in_local = 8.0

	# 					for index_find_peak in range(min_in_local_index+1, min_in_local_index+50, 1): # get the 
	# 						if( float(acc_z_HP[index_find_peak]) >  float(max_in_local) ):
	# 							if(int(acc_t[index_find_peak]) - int(pre_stroke_count_Acc_z_HP_peak_position_t) > 1000 ):
	# 								max_in_local_index = int(index_find_peak)
	# 								max_in_local = float(acc_z_HP[index_find_peak])

	# 					# print "local max", max_in_local_index, max_in_local

	# 					if(int(acc_t[max_in_local_index]) != int(pre_stroke_count_Acc_z_HP_peak_position_t)):
	# 						# print "diff=", max_in_local - min_in_local
	# 						stroke_count_Acc_z_HP_position_peak[0] = int(acc_t[max_in_local_index])
	# 						stroke_count_Acc_z_HP_position_peak[1] = float(max_in_local)
	# 						stroke_count_Acc_z_HP_list_peak.append(str(stroke_count_Acc_z_HP_position_peak))

	# 						pre_stroke_count_Acc_z_HP_peak_position_t = int(acc_t[max_in_local_index])
	# 						pre_stroke_count_Acc_z_HP_peak_position_m = float(max_in_local)

	# 						stroke_count_Acc_z_HP += 1
	# 						stroke_count_Acc_z_HP_position[0] = int(acc_t[min_in_local_index])
	# 						stroke_count_Acc_z_HP_position[1] = float(min_in_local)
	# 						stroke_count_Acc_z_HP_list.append(str(stroke_count_Acc_z_HP_position))

	# 						pre_stroke_count_Acc_z_HP_position_t = int(acc_t[min_in_local_index])
	# 						pre_stroke_count_Acc_z_HP_position_m = float(min_in_local)


	# 			# for index_find_peak in range(min_in_local_index+1, min_in_local_index+15, 1):
	# 			# 	if(float(acc_z_HP[index_find_peak]) >  float(max_in_local) ):
	# 			# 		max_in_local_index = index_find_peak
	# 			# 		max_in_local = float(acc_z_HP[index_find_peak])
	

				
				
				
	# 			# print acc_t[index], acc_z_HP[index]

	# # print stroke_count_Acc_z_HP
	# # print stroke_count_Acc_z_HP_list
	# Acc_z_HP_count_t = np.zeros(len(stroke_count_Acc_z_HP_list))
	# Acc_z_HP_count_m = np.zeros(len(stroke_count_Acc_z_HP_list))
	# for index in range(0 , len(stroke_count_Acc_z_HP_list), 1):
	# 	# print stroke_count_Acc_z_HP_list[index]
	# 	element = stroke_count_Acc_z_HP_list[index].split(",")
	# 	element2 = element[0].split("[")
	# 	element3 = element[1].split("]")
	# 	Acc_z_HP_count_t[index] = int(element2[1])
	# 	Acc_z_HP_count_m[index] = float(element3[0])

	# Acc_z_HP_count_peak_t = np.zeros(len(stroke_count_Acc_z_HP_list_peak))
	# Acc_z_HP_count_peak_m = np.zeros(len(stroke_count_Acc_z_HP_list_peak))
	
	# for index in range(0 , len(stroke_count_Acc_z_HP_list_peak), 1):
	# 	# print stroke_count_Acc_z_HP_list_peak[index]
	# 	element = stroke_count_Acc_z_HP_list_peak[index].split(",")
	# 	element2 = element[0].split("[")
	# 	element3 = element[1].split("]")
	# 	Acc_z_HP_count_peak_t[index] = int(element2[1])
	# 	Acc_z_HP_count_peak_m[index] = float(element3[0])








# stroke count for gyro -------------------------------------------------------------------------------------------------------------------


	gyro_z_peak_count = [0 ,0]
	gyro_z_peak_count_list = []

	for index in range(1, len(gyro_data)-1, 1):
		element0 = gyro_data[index-1].split(",")
		element0_1 = element0[3].split("\n")
		gyro_x_pre = float(element0[1])
		gyro_y_pre = float(element0[2])
		gyro_z_pre = float(element0_1[0])
		
		element = gyro_data[index].split(",")
		element_1 = element[3].split("\n")
		gyro_x_now = float(element[1])
		gyro_y_now = float(element[2])
		gyro_z_now = float(element_1[0])
		
		element1 = gyro_data[index+1].split(",")
		element1_1 = element1[3].split("\n")
		gyro_x_next = float(element1[1])
		gyro_y_next = float(element1[2])
		gyro_z_next = float(element1_1[0])
		if ( (file_profile[2] == "Tina") & (file_profile[3] == "FCS") ):
			if( gyro_z_now > 6 ):
				if( (  float(gyro_z_now) - float(gyro_z_pre)  > 0 ) & ( float(gyro_z_now) - float(gyro_z_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_z_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))

		if ( (file_profile[2] == "Tina") & (file_profile[3] == "Back") ):
			if( gyro_y_now > 4 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if ( (file_profile[2] == "Tina") & (file_profile[3] == "BrS") ):
			if( gyro_y_now > 3 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if ( (file_profile[2] == "Tina") & (file_profile[3] == "Fly") ):
			if( gyro_y_now > 2 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if ( (file_profile[2] == "Von") & (file_profile[3] == "FCS") ):
			if( gyro_z_now > 3 ):
				if( (  float(gyro_z_now) - float(gyro_z_pre)  > 0 ) & ( float(gyro_z_now) - float(gyro_z_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_z_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if ( (file_profile[2] == "Conlin") & (file_profile[3] == "FCS") ):
			if( gyro_x_now > 3 ):
				if( (  float(gyro_x_now) - float(gyro_x_pre)  > 0 ) & ( float(gyro_x_now) - float(gyro_x_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_x_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (   ((file_profile[2] == "Gabriel") or (file_profile[2] == "YuanZhu"))   & (file_profile[3] == "FCS") ):
			if( gyro_y_now < -4 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  < 0 ) & ( float(gyro_y_now) - float(gyro_y_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(5.0)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Ziv")   ) & (file_profile[3] == "FCS"):
			if( gyro_y_now < -4 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  < 0 ) & ( float(gyro_y_now) - float(gyro_y_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(5.0)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Conlin")   ) & (file_profile[3] == "BrS"):
			if( gyro_x_now < -2.59 ):
				if( (  float(gyro_x_now) - float(gyro_x_pre)  < 0 ) & ( float(gyro_x_now) - float(gyro_x_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(5.0)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Young")   ) & (file_profile[3] == "Back"):
			if( gyro_y_now > 4.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Lui")   ) & (file_profile[3] == "Back"):
			if( gyro_y_now > 4.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "BigFish")   ) & (file_profile[3] == "Back"):
			if( gyro_y_now < -4.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  < 0 ) & ( float(gyro_y_now) - float(gyro_y_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(5.0)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "WatermanLR")   ) & (file_profile[3] == "Back"):
			if( gyro_y_now > 4.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Conlin") or  (file_profile[2] == "Leo") or  (file_profile[2] == "Ray") or  (file_profile[2] == "Josh") or  (file_profile[2] == "Lumi") or  (file_profile[2] == "Wu")) & (file_profile[3] == "Back"):
			if( gyro_y_now > 2.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Wendy01")   ) & (file_profile[3] == "Back"):
			if( gyro_y_now < -3.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  < 0 ) & ( float(gyro_y_now) - float(gyro_y_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = 5.0
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "MTK")   ) & (file_profile[3] == "FCS"):
			if( gyro_z_now < -5.00 ):
				if( (  float(gyro_z_now) - float(gyro_z_pre)  < 0 ) & ( float(gyro_z_now) - float(gyro_z_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = 5.0
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "Wu") ) & (file_profile[3] == "Back"):
			if( gyro_y_now < -2.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  < 0 ) & ( float(gyro_y_now) - float(gyro_y_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_y_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if ( (file_profile[2] == "MKT01") & (file_profile[3] == "FCS") ):
			if( gyro_x_now > 8 ):
				if( (  float(gyro_x_now) - float(gyro_x_pre)  > 0 ) & ( float(gyro_x_now) - float(gyro_x_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = float(gyro_x_now)
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "MKT02")  & (file_profile[3] == "FCS")  ):
			if( gyro_y_now < -4.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  < 0 ) & ( float(gyro_y_now) - float(gyro_y_next) < 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = 5.0
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "MKT03")  & (file_profile[3] == "BrS")  ):
			if( gyro_y_now > 2.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = 5.0
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))
		if (  (file_profile[2] == "ChienYuWang")  & (file_profile[3] == "FCS")  ):
			if( gyro_y_now > 2.00 ):
				if( (  float(gyro_y_now) - float(gyro_y_pre)  > 0 ) & ( float(gyro_y_now) - float(gyro_y_next) > 0) ) :
					gyro_z_peak_count[0] = int(element[0])
					gyro_z_peak_count[1] = 5.0
					gyro_z_peak_count_list.append(str(gyro_z_peak_count))

					

	

	gyro_z_SC_t = []
	gyro_z_SC_x = []
	for index in range(0 , len(gyro_z_peak_count_list), 1):
		element = gyro_z_peak_count_list[index].split(",")
		element1 = element[0].split("[")
		element2 = element[1].split("]")

		gyro_z_SC_t.append(int(element1[1]))
		gyro_z_SC_x.append(float(element2[0]))


		# gyro_z_SC_t.append(int(gyro_z_peak_count_list[index][0]))
		# gyro_z_SC_x.append(float(gyro_z_peak_count_list[index][1]))
	# print len(gyro_z_SC_t), len(gyro_z_SC_x)
	# print gyro_z_SC_t

	# print gyro_z_SC_x






		# gyro_t.append(int(element[0]))
		# gyro_x.append(float(element[1]))
		# gyro_y.append(float(element[2]))
		# gyro_z.append(float(element_1[0]))
	





# END of stroke count for gyro -------------------------------------------------------------------------------------------------------------------


	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(611, autoscale_on=False, xlim=(0,135000), ylim=(-40,35))
	ax.set_title('Acc_X')
	lns1 = ax.plot(acc_t, acc_x, lw=2, color='green', label = 'acc_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(612, autoscale_on=False, xlim=(0,135000), ylim=(-35,35))
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_y, lw=2, color='purple', label = 'acc_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(613, autoscale_on=False, xlim=(0,135000), ylim=(-40,40))
	ax.set_title('Acc_Z')
	lns1 = ax.plot(acc_t, acc_z, lw=2, color='black', label = 'acc_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(614, autoscale_on=False, xlim=(0,135000), ylim=(0,50))
	ax.set_title('Acc_N')
	lns1 = ax.plot(acc_t, acc_N, lw=2, color='red', label = 'acc_N')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")


	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(615, autoscale_on=False, xlim=(0,135000), ylim=(0,50))
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_xy, lw=2, color='blue', label = 'acc_xy')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	for index in range(0, SC_indicator ,1):
		element = stroke_count_xy_list[index].split(",")
		element_1 = element[0].split("[")
		element_2 = element[1].split("]")
		time_stemp = float(element_1[1]) / 1000
		acc_value = round(float(element_2[0]), 1)
		ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1[1], element_2[0]),  xycoords='data', color='magenta',
			xytext=(10, 40), textcoords='offset points',
			arrowprops=dict(arrowstyle="->",
				connectionstyle="angle3,angleA=0,angleB=-90"),
			)

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(615, autoscale_on=False, xlim=(0,135000), ylim=(0,50))
	lns2 = ax.plot(peak_t, peak_acc, "ro", markersize=8, color='red')

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(615, autoscale_on=False, xlim=(0,135000), ylim=(0,50))
	lns2 = ax.plot(peak_t, peak_th, "ro", markersize=5, color='green')

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(615, autoscale_on=False, xlim=(0,135000), ylim=(0,50))
	lns2 = ax.plot(Time_Thresold_t, Time_Thresold_magnitude, "x", markersize=15, color='blue')

	fig = figure(1,figsize=(120,15))
	ax = fig.add_subplot(615, autoscale_on=False, xlim=(0,135000), ylim=(0,50))
	lns2 = ax.plot(gyro_z_SC_t, gyro_z_SC_x, "o", markersize=15, color='magenta')

	ax = plt.errorbar(peak_t, peak_th, xerr=0.1, color='green')

	# fig = figure(1,figsize=(120,15))
	# ax = fig.add_subplot(616, autoscale_on=False, xlim=(0,135000), ylim=(-25,25))
	# ax.set_title('Acc_z_HP')
	# lns1 = ax.plot(acc_t, acc_z_HP, lw=2, color='green', label = 'acc_z_HP')
	# lns = lns1
	# labs = [l.get_label() for l in lns]
	# ax.legend(lns, labs, loc=0)
	# ax.grid()
	# ax.set_xlabel("Time (msec)")
	# ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	# for index in range(0, len(stroke_count_Acc_z_HP_list_peak) ,1):
	# 	element = stroke_count_Acc_z_HP_list_peak[index].split(",")
	# 	element_1 = element[0].split("[")
	# 	element_2 = element[1].split("]")
	# 	time_stemp = float(element_1[1]) / 1000
	# 	acc_value = round(float(element_2[0]), 1)
	# 	ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1[1], element_2[0]),  xycoords='data', color='blue',
	# 		xytext=(10, 20), textcoords='offset points',
	# 		arrowprops=dict(arrowstyle="->",
	# 			connectionstyle="angle3,angleA=0,angleB=-90"),
	# 		)
	# for index in range(0, len(stroke_count_Acc_z_HP_list) ,1):
	# 	element = stroke_count_Acc_z_HP_list[index].split(",")
	# 	element_1 = element[0].split("[")
	# 	element_2 = element[1].split("]")
	# 	time_stemp = float(element_1[1]) / 1000
	# 	acc_value = round(float(element_2[0]), 1)
	# 	ax.annotate('SC '+ str(index+1)+"\n("+str(time_stemp)+","+str(acc_value)+")", xy=(element_1[1], element_2[0]),  xycoords='data', color='red',
	# 		xytext=(10, -30), textcoords='offset points',
	# 		arrowprops=dict(arrowstyle="->",
	# 			connectionstyle="angle3,angleA=0,angleB=-90"),
	# 		)

	# fig = figure(1,figsize=(120,15))
	# ax = fig.add_subplot(616, autoscale_on=False, xlim=(0,135000), ylim=(-25,25))
	# lns2 = ax.plot(Acc_z_HP_count_t, Acc_z_HP_count_m, "ro", markersize=8, color='red')

	# fig = figure(1,figsize=(120,15))
	# ax = fig.add_subplot(616, autoscale_on=False, xlim=(0,135000), ylim=(-25,25))
	# lns2 = ax.plot(Acc_z_HP_count_peak_t, Acc_z_HP_count_peak_m, "ro", markersize=8, color='blue')




	


	
	
	

	fig.savefig(stroke_count_file_root)


	# show()
	plt.close(fig)

	return SC_indicator




file_for_SC = "20151113_095219_Foot_Walk_holdCup_Conlin_Sony_200_0"
stroke_count(file_for_SC)