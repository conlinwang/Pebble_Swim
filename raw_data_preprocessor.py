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

def raw_data_preprocess( into_file_name ):
	file_name = into_file_name
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/RAW"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/RAW")   

	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/RAW/Acc"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/RAW/Acc")	
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/RAW/Gyro"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/RAW/Gyro")
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/RAW/Magn"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/RAW/Magn")
	if not os.path.exists("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate"):
		os.mkdir("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate")	
	
	# 3 figures together
	acc_xyz_file_root   = "./stroke_count_Evaluation/"+file_name+"/RAW/Acc_raw.png"
	gyro_xyz_file_root  = "./stroke_count_Evaluation/"+file_name+"/RAW/Gyro_raw.png"
	magne_xyz_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Magne_raw.png"
	# 3 acc figures
	acc_x_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Acc/Acc_X_raw.png"
	acc_y_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Acc/Acc_Y_raw.png"
	acc_z_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Acc/Acc_Z_raw.png"
	acc_n_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Acc/Acc_N_raw.png"
	# 3 gyro figures
	gyro_x_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Gyro/Gyro_X_raw.png"
	gyro_y_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Gyro/Gyro_Y_raw.png"
	gyro_z_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Gyro/Gyro_Z_raw.png"
	# 3 magne figures
	magne_x_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Magn/Magn_X_raw.png"
	magne_y_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Magn/Magn_Y_raw.png"
	magne_z_file_root = "./stroke_count_Evaluation/"+file_name+"/RAW/Magn/Magn_Z_raw.png"

	file_write_to = open("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate/acc.txt", "wb")
	file_write_to_gyro = open("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate/gyro.txt", "wb")
	file_write_to_magn = open("./stroke_count_Evaluation/"+file_name+"/RAW/AGM_RAW_separate/magn.txt", "wb")



	input_data = open("./stroke_count_Evaluation/"+file_name+"/"+file_name+".txt", "r+") # input_data
	line = input_data.readlines() # load data into python
	lenght = len(line)    # get how many data had being loaded 


	# split the data into acc, gyro, and magnetic
	acc_data_array_final = [] # for acc
	gyro_data_array_final = [] # for gyro
	magnetic_data_array_final = [] # for magnetic
	pressure_data_array_final = []
	proximity_data_array_final = []
	light_data_array_final = []
	temperature_data_array_final = []
	flag_data_array_final = []

	for index in range(0, lenght-1, 1):
		acc_data_1 = line[index].split(',')
		# print acc_data_1
		if (acc_data_1[1] !=''): # If Acc x != empty read all the Acc data
			acc_data_array_final.append(acc_data_1[0:4])
		if ( acc_data_1[4] !=''): # If Gyroscope x != empty read all the Gyro data
			gyro_data_array = []
			gyro_data_array.append(acc_data_1[0])
			gyro_data_array.append(acc_data_1[4])
			gyro_data_array.append(acc_data_1[5])
			gyro_data_array.append(acc_data_1[6])
			gyro_data_array_final.append(gyro_data_array)
		if (acc_data_1[7] !=''): # If Magnetometer x != empty read all the Magne data 
			magnetic_data_array = []
			magnetic_data_array.append(acc_data_1[0])
			magnetic_data_array.append(acc_data_1[7])
			magnetic_data_array.append(acc_data_1[8])
			magnetic_data_array.append(acc_data_1[9])
			magnetic_data_array_final.append(magnetic_data_array)
		if (acc_data_1[10] !=''): # If Pressure sensor x != empty read all the Pressure data 
			pressure_data_array = []
			pressure_data_array.append(acc_data_1[10])
			pressure_data_array_final.append(pressure_data_array)
		if (acc_data_1[11] !=''):
			proximity_data_array = []
			proximity_data_array.append(acc_data_1[11])
			proximity_data_array_final.append(proximity_data_array)
		if (acc_data_1[12] !=''):
			light_data_array = []
			light_data_array.append(acc_data_1[12])
			light_data_array_final.append(light_data_array)
		if (acc_data_1[13] !=''):
			temperature_data_array = []
			temperature_data_array.append(acc_data_1[13])
			temperature_data_array_final.append(temperature_data_array)
		if (acc_data_1[14] !=''):
			flag_data_array = []
			flag_data_array.append(acc_data_1[14])
			flag_data_array_final.append(flag_data_array)



		 # If Proximity sensor x != empty read all the Proximity data 
		 


	print "the amount of (acc_data, gyro_data, magn_data, Pressure, Proximity, Light, Temperature,   Flag  ) ="
	print "              ( ",len(acc_data_array_final), ",   " , len(gyro_data_array_final), ",   " , len(magnetic_data_array_final), ",  ", len(pressure_data_array_final), ",       ", len(proximity_data_array_final), ", ", len(light_data_array_final), ",         ", len(temperature_data_array_final), ",  ", len(flag_data_array_final),")"

	acc_t = []
	acc_x = []
	acc_y = []
	acc_z = []
	acc_N = []
	acc_xy = []
	acc_xz = []
	acc_yz = []
	acc_zSQ = []


	for index in range(0, len(acc_data_array_final), 1):
		acc_t.append(float(int(acc_data_array_final[index][0]) - int(acc_data_array_final[0][0])) / 1000)
		acc_x.append(acc_data_array_final[index][1])
		acc_y.append(acc_data_array_final[index][2])
		acc_z.append(acc_data_array_final[index][3])
		acc_N.append( math.sqrt(math.pow(float(acc_data_array_final[index][1]), 2) + math.pow(float(acc_data_array_final[index][2]), 2) + math.pow(float(acc_data_array_final[index][3]), 2)) )
		acc_xy.append( math.sqrt(math.pow(float(acc_data_array_final[index][1]), 2) + math.pow(float(acc_data_array_final[index][2]), 2) ))
		acc_xz.append( math.sqrt(math.pow(float(acc_data_array_final[index][1]), 2) + math.pow(float(acc_data_array_final[index][3]), 2) ))
		acc_yz.append( math.sqrt(math.pow(float(acc_data_array_final[index][2]), 2) + math.pow(float(acc_data_array_final[index][3]), 2) ))
		acc_zSQ.append( math.sqrt(math.pow(float(acc_data_array_final[index][3]), 2)) )


		file_write_to.write( str(   int(acc_data_array_final[index][0]) - int(acc_data_array_final[0][0])  ) +","+ 
			                 str(acc_data_array_final[index][1]) +","+ 
			                 str(acc_data_array_final[index][2]) +","+
			                 str(acc_data_array_final[index][3]) +","+
			                 str(math.sqrt(math.pow(float(acc_data_array_final[index][1]), 2) + math.pow(float(acc_data_array_final[index][2]), 2) + math.pow(float(acc_data_array_final[index][3]), 2))) +","+
			                 str(math.sqrt(math.pow(float(acc_data_array_final[index][1]), 2) + math.pow(float(acc_data_array_final[index][2]), 2) )) +","+
			                 str(math.sqrt(math.pow(float(acc_data_array_final[index][1]), 2) + math.pow(float(acc_data_array_final[index][3]), 2) )) +","+
		                     str(math.sqrt(math.pow(float(acc_data_array_final[index][2]), 2) + math.pow(float(acc_data_array_final[index][3]), 2) )) +","+
		                     str(  float(acc_data_array_final[index][3]) * (-1.0)   ) +","+
		                     "\n" );
	gyro_t = []
	gyro_x = []
	gyro_y = []
	gyro_z = []	
	for index in range(0, len(gyro_data_array_final), 1):
		gyro_t.append(float(int(gyro_data_array_final[index][0]) - int(gyro_data_array_final[0][0]))/ 1000)
		gyro_x.append(gyro_data_array_final[index][1])
		gyro_y.append(gyro_data_array_final[index][2])
		gyro_z.append(gyro_data_array_final[index][3])
		file_write_to_gyro.write( str(   int(gyro_data_array_final[index][0]) - int(gyro_data_array_final[0][0])  ) +","+ 
			                      str(gyro_data_array_final[index][1]) +","+ 
			                      str(gyro_data_array_final[index][2]) +","+
			                      str(gyro_data_array_final[index][3]) + "\n" );

	magne_t = []
	magne_x = []
	magne_y = []
	magne_z = []	
	for index in range(0, len(magnetic_data_array_final), 1):
		magne_t.append(float(int(magnetic_data_array_final[index][0]) - int(magnetic_data_array_final[0][0]))/ 1000)
		magne_x.append(magnetic_data_array_final[index][1])
		magne_y.append(magnetic_data_array_final[index][2])
		magne_z.append(magnetic_data_array_final[index][3])
		file_write_to_magn.write( str(   int(magnetic_data_array_final[index][0]) - int(magnetic_data_array_final[0][0])  ) +","+ 
			                      str(magnetic_data_array_final[index][1]) +","+ 
			                      str(magnetic_data_array_final[index][2]) +","+
			                      str(magnetic_data_array_final[index][3]) + "\n" );

	input_data.close()
	file_write_to.close()
	file_write_to_gyro.close()
	file_write_to_magn.close()

	# acc figures x, y, z, N, zy -----------------------------------------------------
	
	fig = figure(1,figsize=(240,15))
	ax = fig.add_subplot(811, autoscale_on=False, xlim=(0,130), ylim=(-30,30))
	# ax = fig.add_subplot(811)
	ax.set_title('Acc_X')
	lns1 = ax.plot(acc_t, acc_x, lw=2, color='green', label = 'acc_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(812, autoscale_on=False, xlim=(0,130), ylim=(-35,35))
	ax = fig.add_subplot(812)
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_y, lw=2, color='purple', label = 'acc_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(813, autoscale_on=False, xlim=(0,130), ylim=(-40,40))
	ax = fig.add_subplot(813)
	ax.set_title('Acc_Y')
	lns1 = ax.plot(acc_t, acc_z, lw=2, color='black', label = 'acc_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(814, autoscale_on=False, xlim=(0,130), ylim=(0,40))
	ax = fig.add_subplot(814)
	ax.set_title('Acc_N')
	lns1 = ax.plot(acc_t, acc_N, lw=2, color='red', label = 'acc_N')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(815, autoscale_on=False, xlim=(0,130), ylim=(0,40))
	ax = fig.add_subplot(815)
	ax.set_title('Acc_xy')
	lns1 = ax.plot(acc_t, acc_xy, lw=2, color='blue', label = 'acc_xy')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	
	

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(816, autoscale_on=False, xlim=(0,130), ylim=(0,40))
	ax = fig.add_subplot(816)
	ax.set_title('Acc_xz')
	lns1 = ax.plot(acc_t, acc_xz, lw=2, color='magenta', label = 'acc_xz')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	
	

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(817, autoscale_on=False, xlim=(0,130), ylim=(0,40))
	ax = fig.add_subplot(817)
	ax.set_title('Acc_yz')
	lns1 = ax.plot(acc_t, acc_yz, lw=2, color='green', label = 'acc_yz')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")

	fig = figure(1,figsize=(240,15))
	# ax = fig.add_subplot(818, autoscale_on=False, xlim=(0,130), ylim=(0,40))
	ax = fig.add_subplot(818)
	ax.set_title('Acc_zSQ')
	lns1 = ax.plot(acc_t, acc_zSQ, lw=2, color='red', label = 'acc_zSQ')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Acceleration ($m\,sec^{-2}$)")
	

	fig.savefig(acc_xyz_file_root)
	plt.close(fig)


	# gyro figures x, y, z --------------------------------------------------------------


	fig = figure(2,figsize=(240,15))
	# ax = fig.add_subplot(311, autoscale_on=False, xlim=(0,130), ylim=(-20,20))
	ax = fig.add_subplot(311)
	ax.set_title('gyro_x')
	lns1 = ax.plot(gyro_t, gyro_x, lw=2, color='red', label = 'gyro_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(2,figsize=(240,15))
	# ax = fig.add_subplot(312, autoscale_on=False, xlim=(0,130), ylim=(-20,20))
	ax = fig.add_subplot(312)
	ax.set_title('gyro_y')
	lns1 = ax.plot(gyro_t, gyro_y, lw=2, color='green', label = 'gyro_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(2,figsize=(240,15))
	# ax = fig.add_subplot(313, autoscale_on=False, xlim=(0,130), ylim=(-20,20))
	ax = fig.add_subplot(313)
	ax.set_title('gyro_z')
	lns1 = ax.plot(gyro_t, gyro_x, lw=2, color='blue', label = 'gyro_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")
	fig.savefig(gyro_xyz_file_root)
	plt.close(fig)

	# Magne figures x, y, z --------------------------------------------------------------

	fig = figure(3,figsize=(240,15))
	# ax = fig.add_subplot(311, autoscale_on=False, xlim=(0,130), ylim=(-100,100))
	ax = fig.add_subplot(311)
	ax.set_title('Magn_x')
	lns1 = ax.plot(magne_t, magne_x, lw=2, color='red', label = 'magne_x')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Magne ($tesla\,$)")

	fig = figure(3,figsize=(240,15))
	# ax = fig.add_subplot(312, autoscale_on=False, xlim=(0,130), ylim=(-100,100))
	ax = fig.add_subplot(312)
	ax.set_title('Magne_y')
	lns1 = ax.plot(magne_t, magne_y, lw=2, color='green', label = 'magne_y')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	# ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")

	fig = figure(3,figsize=(240,15))
	# ax = fig.add_subplot(313, autoscale_on=False, xlim=(0,130), ylim=(-100,100))
	ax = fig.add_subplot(313)
	ax.set_title('Magne_z')
	lns1 = ax.plot(magne_t, magne_z, lw=2, color='blue', label = 'magne_z')
	lns = lns1
	labs = [l.get_label() for l in lns]
	ax.legend(lns, labs, loc=0)
	ax.grid()
	ax.set_xlabel("Time (msec)")
	ax.set_ylabel(r"Gyro ($deg\,sec^{-1}$)")
	fig.savefig(magne_xyz_file_root)
	plt.close(fig)	


# raw_data_preprocess("20140718_170104_Foot_Walkfast_Dang_Ren_K89_425_0")

