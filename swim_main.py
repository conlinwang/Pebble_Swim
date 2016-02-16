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

import raw_data_preprocessor

import acc_resample
import gyro_resample
import magn_resample

import acc_smooth
import acc_LPF_5Hz
import gyro_smooth
import magn_smooth
import acc_smooth_HP

import step_count
import step_count_x
import step_count_dev_10
# import stroke_count_dev
# import stroke_type
# import quality_check



SMAPLE_RATE = 50 # 20 Hz

# For Single data testing 
#-------------------------------------------------------------
file_for_SC = "20151105_112309_Foot_Walk_Inhand_Hsuanchao_Sony_200_0"

raw_data_preprocessor.raw_data_preprocess(file_for_SC)
acc_resample.acc_resample(SMAPLE_RATE, file_for_SC)
gyro_resample.gyro_resample(SMAPLE_RATE, file_for_SC)

acc_LPF_5Hz.acc_LPF(file_for_SC)
acc_smooth_HP.acc_HPF(file_for_SC)
gyro_smooth.gyro_smooth(file_for_SC)
step_count_x.step_count_x(file_for_SC)
print step_count_dev_10.step_count(file_for_SC,10)


# stroke_count_dev.stroke_count(file_for_SC)
# quality_check.quality_check(file_for_SC)

# End of For Single data testing
#-------------------------------------------------------------

# input_data = open("./file_list_step_count.txt", "r+") # input_data
# line = input_data.readlines() # load data into python

# for index in range(0, len(line), 1):
# 	element = line[index].split("\n")
# 	element01 = element[0].split("_")
# 	if(element[0] =="20151106_162336_Foot_Walk_InHand_ChengMinYuan_Sony_200_0"):
# 		step_count_result = step_count_dev_10.step_count(element[0], 400)
# 	else:
# 		step_count_result = step_count_dev_10.step_count(element[0], 10)
# 	step_count_result_x = int(step_count_result[0])
# 	step_count_result_y = int(step_count_result[1])
# 	step_count_result_z = int(step_count_result[2])
# 	ground_truth = int(element01[7])
# 	x_recall = float(abs(step_count_result_x-ground_truth)) / ground_truth
# 	y_recall = float(abs(step_count_result_y-ground_truth)) / ground_truth
# 	z_recall = float(abs(step_count_result_z-ground_truth)) / ground_truth
# 	if(x_recall < 0.05 or y_recall < 0.05 or z_recall < 0.05):
# 		print ground_truth, step_count_result, element[0],  "passed"
# 	else:
# 		print ground_truth, step_count_result, element[0],  x_recall, y_recall, z_recall 
	
	

