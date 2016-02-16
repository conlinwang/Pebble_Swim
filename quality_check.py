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

def quality_check( into_file_name ):
	file_name = into_file_name
	input_acc_data = open("./stroke_count_Evaluation/"+file_name+"/smoothen_acc/acc_LPF_5Hz.txt", "r+") # input_acc_data
	input_gyro_data = open("./stroke_count_Evaluation/"+file_name+"/smoothen_gyro/smoothen_gyro.txt", "r+") # input_acc_data

	stroke_count_file_root = "./stroke_count_Evaluation/"+file_name+"/quality_check.png"

	print "in quality_check now"

	line = input_acc_data.readlines()
	length = len(line)
	max_interval_temp = 0
	max_interval = 0

	acc_data_array = [] # for acc
	gyro_data_array_final = [] # for gyro
	# magnetic_data_array_final = [] # for magnetic_data
	for index in range(0, len(line), 1):
		acc_data_1 = line[index].split(',')
		acc_data_array.append(acc_data_1[0:4])

	total_time_duration = int(acc_data_array[length-1][0]) - int(acc_data_array[0][0])

	sampling_interval = 0
	max_interval_temp = 0
	max_interval = 0
	square_sampling_interval = 0

	plot_sampling_interval = []
	more_than_thousand = 0
	aggregate_lost_time = 0 

	for index in range(1, len(acc_data_array), 1):
		sampling_interval = sampling_interval + (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) )
		plot_sampling_interval.append( int(acc_data_array[index][0]) - int(acc_data_array[index-1][0])  )
		square_sampling_interval = square_sampling_interval + math.pow((  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) ), 2)
		max_interval_temp = (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) )
		if ( max_interval_temp > max_interval ):
			max_interval = max_interval_temp
		if ( (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) ) > 120 ):
			more_than_thousand = more_than_thousand + 1
			aggregate_lost_time = aggregate_lost_time + (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) ) 

	print "The average sampling rate of Acc is = " + str( float(sampling_interval) / len(acc_data_array) )
	print "The Max sampling gap of Acc is = " + str(max_interval)
	print "The STD of sampling rate of Acc is = " + str(math.sqrt((square_sampling_interval - math.pow( float(sampling_interval), 2) / len(acc_data_array) ) / len(acc_data_array)))
	print ""
	print str(more_than_thousand) + " of the data smapling interval more than 1 sec"
	print float( more_than_thousand) / length
	print float(aggregate_lost_time) / total_time_duration

	fig = figure(1)
	ax = fig.add_subplot(111)
	ax.set_title('quality_check')
	lns1 = ax.plot(plot_sampling_interval, lw=2, color='red', label = 'Sampling_Interval')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("number of data")
	ax.set_ylabel(r"Acceleration ($msec$)")
	fig.savefig(stroke_count_file_root)
	plt.close(fig)

	# plt.plot(plot_sampling_interval)
	# plt.ylabel('Sampling_Interval')
	# show()


	# plt.plot(plot_sampling_interval)
	# plt.ylabel('Sampling_Interval')
	# fig.savefig(stroke_count_file_root)








# # fo = open("./0705_155314_Still_Sit_Shake_once_N_W1/smoothen_acc/acc_LPF_5Hz.txt", "r+") # input training data
# line = fo.readlines()
# length = len(line)
# print "The total number of this data is = "+ str(length)

# #Acc sampling rate
# max_interval_temp = 0
# max_interval = 0

# acc_data_array = [] # for acc
# gyro_data_array_final = [] # for gyro
# magnetic_data_array_final = []
# for index in range(0, length, 1):
# 	acc_data_1 = line[index].split(',')
# 	acc_data_array.append(acc_data_1[0:4])


# #time interval of the whole data
# total_time_duration = int(acc_data_array[length-1][0]) - int(acc_data_array[0][0])


# sampling_interval = 0
# max_interval_temp = 0
# max_interval = 0
# square_sampling_interval = 0

# plot_sampling_interval = []
# more_than_thousand = 0
# aggregate_lost_time = 0 
# for index in range(1, len(acc_data_array), 1):
# 	sampling_interval = sampling_interval + (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) )
# 	plot_sampling_interval.append( int(acc_data_array[index][0]) - int(acc_data_array[index-1][0])  )
# 	square_sampling_interval = square_sampling_interval + math.pow((  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) ), 2)
# 	max_interval_temp = (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) )
# 	if ( max_interval_temp > max_interval ):
# 		max_interval = max_interval_temp
# 	if ( (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) ) > 120 ):
# 		more_than_thousand = more_than_thousand + 1
# 		aggregate_lost_time = aggregate_lost_time + (  int(acc_data_array[index][0]) - int(acc_data_array[index-1][0]) ) 


# print "The average sampling rate of Acc is = " + str( float(sampling_interval) / len(acc_data_array) )
# print "The Max sampling gap of Acc is = " + str(max_interval)
# print "The STD of sampling rate of Acc is = " + str(math.sqrt((square_sampling_interval - math.pow( float(sampling_interval), 2) / len(acc_data_array) ) / len(acc_data_array)))
# print ""
# print str(more_than_thousand) + " of the data smapling interval more than 1 sec"
# print float( more_than_thousand) / length
# print float(aggregate_lost_time) / total_time_duration

# plt.plot(plot_sampling_interval)
# plt.ylabel('Sampling_Interval')
# plt.show()

# # #for gyro
# # sampling_interval_gyro = 0
# # max_interval_temp = 0
# # max_interval = 0
# # square_sampling_interval = 0
# # for index in range(1, len(gyro_data_array_final), 1):
# # 	sampling_interval_gyro = sampling_interval_gyro + (  int(gyro_data_array_final[index][0]) - int(gyro_data_array_final[index-1][0]) )
# # 	square_sampling_interval = square_sampling_interval + math.pow((  int(gyro_data_array_final[index][0]) - int(gyro_data_array_final[index-1][0]) ), 2)
# # 	max_interval_temp = (  int(gyro_data_array_final[index][0]) - int(gyro_data_array_final[index-1][0]) )
# # 	if ( max_interval_temp > max_interval ):
# # 		max_interval = max_interval_temp

# # print "The average sampling rate of Gyro is = " + str( float(sampling_interval_gyro) / len(gyro_data_array_final) )
# # print "The Max sampling gap of Gyro is = " + str(max_interval)
# # print "The STD of sampling rate of Gyro is = " + str(math.sqrt((square_sampling_interval - math.pow( float(sampling_interval_gyro), 2) / len(gyro_data_array_final) ) / len(gyro_data_array_final)))
# # print ""

# # #for magne
# # sampling_interval_mag = 0
# # max_interval_temp = 0
# # max_interval = 0
# # square_sampling_interval = 0
# # for index in range(1, len(magnetic_data_array_final), 1):
# # 	sampling_interval_mag = sampling_interval_mag + (  int(magnetic_data_array_final[index][0]) - int(magnetic_data_array_final[index-1][0]) )
# # 	square_sampling_interval = square_sampling_interval + math.pow((  int(magnetic_data_array_final[index][0]) - int(magnetic_data_array_final[index-1][0]) ), 2)
# # 	max_interval_temp = (  int(magnetic_data_array_final[index][0]) - int(magnetic_data_array_final[index-1][0]) )
# # 	if ( max_interval_temp > max_interval ):
# # 		max_interval = max_interval_temp

# # print "The average sampling rate of Magnetic is = " + str( float(sampling_interval_mag) / len(magnetic_data_array_final) )
# # print "The Max sampling gap of Magnetic is = " + str(max_interval)
# # print "The STD of sampling rate of Magnetic is = " + str(math.sqrt((square_sampling_interval - math.pow( float(sampling_interval_mag), 2) / len(magnetic_data_array_final) ) / len(magnetic_data_array_final)))
# # print ""
# fo.close()