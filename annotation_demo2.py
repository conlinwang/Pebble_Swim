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

file_name = '0627_183021_NTUST.LG_FCS_16_16_100m'
re_sample_acc = open("./"+file_name+"/re_sample_acc/re_sample_acc.txt", "r+") # input training data for acc
re_sample_gyro = open("./"+file_name+"/re_sample_gyro/re_sample_gyro.txt", "r+") # input training data for gyro

line = re_sample_acc.readlines() # read acc re_sample_acc.txt
line_gyro = re_sample_gyro.readlines() # read gyro re_sample_gyro.txt
length = len(line)
length_g = len(line_gyro)
alpha = 0.1
LPF_list = []
LPF_array = [0, 0, 0, 0, 0, 0]

element  = line[0].split(",")
element2 = element[5].split("\n")
LPF_array[0] = int(element[0])
LPF_array[1] = float(element[1])
LPF_array[2] = float(element[2])
LPF_array[3] = float(element[3])
LPF_array[4] = float(element[4])
LPF_array[5] = float(element2[0])
LPF_list.append(str(LPF_array))

for index in range(1, len(line), 1):
    element0  = line[index-1].split(",")
    element02 = element0[5].split("\n")
    pre_acc_x = float(element0[1])
    pre_acc_y = float(element0[2])
    pre_acc_z = float(element0[3])
    pre_acc_N = float(element0[4])
    pre_acc_xy = float(element02[0])
    
    element  = line[index].split(",")
    element03 = element[5].split("\n")
    LPF_array[0] = int(element[0])
    LPF_array[1] = alpha * float(element[1]) + (1-alpha) * pre_acc_x
    LPF_array[2] = alpha * float(element[2]) + (1-alpha) * pre_acc_y
    LPF_array[3] = alpha * float(element[3]) + (1-alpha) * pre_acc_z
    LPF_array[4] = alpha * float(element[4]) + (1-alpha) * pre_acc_N
    LPF_array[5] = alpha * float(element03[0]) + (1-alpha) * pre_acc_xy
    LPF_list.append(str(LPF_array))

smoothen_list = []
smoothen_array = [0, 0, 0, 0, 0, 0]
for index in range(2, length-2, 1):
    element  = LPF_list[index].split(",")
    element_1 = element[0].split("[")
    element_2 = element[5].split("]")

    element2 = LPF_list[index+1].split(",")
    element2_2 = element2[5].split("]")

    element3 = LPF_list[index-1].split(",")
    element3_2 = element3[5].split("]")

    element4 = LPF_list[index+2].split(",")
    element4_2 = element4[5].split("]")

    element5 = LPF_list[index-2].split(",")
    element5_2 = element5[5].split("]")

    smoothen_array[0] = int(element_1[1])
    smoothen_array[1] = (float(element[1])   + float(element2[1]) + float(element3[1]) + float(element4[1]) + float(element4[1])) / 5
    smoothen_array[2] = (float(element[2])   + float(element2[2]) + float(element3[2]) + float(element4[2]) + float(element4[2])) / 5
    smoothen_array[3] = (float(element[3])   + float(element2[3]) + float(element3[3]) + float(element4[3]) + float(element4[3])) / 5
    smoothen_array[4] = (float(element[4])   + float(element2[4]) + float(element3[4]) + float(element4[4]) + float(element4[4])) / 5
    smoothen_array[5] = (float(element_2[0]) + float(element2_2[0]) + float(element3_2[0]) + float(element4_2[0]) + float(element5_2[0])) / 5
    smoothen_list.append(str(smoothen_array))

smoothen_list_gyro = []
smoothen_array_gyro = [0, 0, 0, 0]
for index in range(2, length_g-2, 1):
    element  = line_gyro[index].split(",")
    element2 = line_gyro[index+1].split(",")
    element3 = line_gyro[index-1].split(",")
    element4 = line_gyro[index+2].split(",")
    element5 = line_gyro[index-2].split(",")
    smoothen_array_gyro[0] = int(element[0])
    smoothen_array_gyro[1] = (float(element[1]) + float(element2[1]) + float(element3[1]) + float(element4[1]) + float(element4[1])) / 5
    smoothen_array_gyro[2] = (float(element[2]) + float(element2[2]) + float(element3[2]) + float(element4[2]) + float(element4[2])) / 5
    smoothen_array_gyro[3] = (float(element[3]) + float(element2[3]) + float(element3[3]) + float(element4[3]) + float(element4[3])) / 5
    smoothen_list_gyro.append(str(smoothen_array_gyro))





if 1:
    acc_t = []
    acc_x = []
    acc_y = []
    acc_z = []
    acc_N = []
    acc_xy = []
    for index in range(0, len(smoothen_list), 1):
        element = smoothen_list[index].split(",")
        element0 = element[0].split("[")
        element1 = element[5].split("]")
        acc_t.append(int(element0[1]))
        acc_x.append(float(element[1]))
        acc_y.append(float(element[2]))
        acc_z.append(float(element[3]))
        acc_N.append(float(element[4]))
        acc_xy.append(float(element1[0]))
    
    

    
    stroke_count_axy = 0
    peak_point_xy = [0, 0]
    pre_peak_point_xy = [0, 0]
    peak_point_list_xy = []

    for index in range(1, len(smoothen_list)-1, 1):
        element  = smoothen_list[index].split(",")
        element_1 = element[0].split("[")
        element_2 = element[5].split("]")

        element2 = smoothen_list[index+1].split(",") # Next point
        element2_2 = element2[5].split("]")
        
        element3 = smoothen_list[index-1].split(",") # Previous point
        element3_2 = element3[5].split("]")
        
        if(stroke_count_axy == 0):
            if((float(element_2[0]) > 8) & ((float(element2_2[0]) > 8)) ):
                if(  (( float(element2_2[0]) - float(element_2[0]) ) < 0) & (( float(element_2[0]) - float(element3_2[0]) ) > 0)  ):
                    stroke_count_axy = stroke_count_axy +1
                    peak_point_xy[0] = int(element_1[1])
                    peak_point_xy[1] = float(element_2[0])
                    peak_point_list_xy.append(str(peak_point_xy))
                    pre_peak_point_xy[0] = peak_point_xy[0]
                    pre_peak_point_xy[1] = peak_point_xy[1]
        elif(stroke_count_axy >= 1):
            if((float(element_2[0]) > 8) & ((float(element2_2[0]) > 8)) ):
                if(  (( float(element2_2[0]) - float(element_2[0]) ) < 0) & (( float(element_2[0]) - float(element3_2[0]) ) > 0)  ):

                    if ((int(element_1[1]) - int(pre_peak_point_xy[0]) > 1900) & (int(element_1[1]) - int(pre_peak_point_xy[0]) < 15000)):
                        stroke_count_axy = stroke_count_axy +1
                        peak_point_xy[0] = int(element_1[1])
                        peak_point_xy[1] = float(element_2[0])
                        peak_point_list_xy.append(str(peak_point_xy))
                        pre_peak_point_xy[0] = peak_point_xy[0]
                        pre_peak_point_xy[1] = peak_point_xy[1]

    print peak_point_list_xy


    stroke_count_ax = 0
    peak_point_ax = [0, 0]
    pre_peak_point_ax = [0, 0]
    peak_point_list_ax = []
    
    stroke_count_ay = 0
    peak_point_ay = [0, 0]
    pre_peak_point_ay = [0, 0]
    peak_point_list_ay = []

    for index in range(1, len(smoothen_list)-1, 1):
        element  = smoothen_list[index].split(",")
        element_1 = element[0].split("[")

        element2 = smoothen_list[index+1].split(",")
        element3 = smoothen_list[index-1].split(",")
        
        if(stroke_count_ax == 0):
            if((float(element[1]) < -12) & ((float(element2[1]) < -12)) ):
                if(  (( float(element2[1]) - float(element[1]) ) > 0) & (( float(element[1]) - float(element3[1]) ) < 0)  ):
                    stroke_count_ax = stroke_count_ax +1
                    peak_point_ax[0] = int(element_1[1])
                    peak_point_ax[1] = float(element[1])
                    peak_point_list_ax.append(str(peak_point_ax))
                    pre_peak_point_ax[0] = peak_point_ax[0]
                    pre_peak_point_ax[1] = peak_point_ax[1]
        elif(stroke_count_ax >= 1):
            if((float(element[1]) < -12) & ((float(element2[1]) < -12)) ):
                if(  (( float(element2[1]) - float(element[1]) ) > 0) & (( float(element[1]) - float(element3[1]) ) < 0)  ):
                    if ((int(element_1[1]) - int(pre_peak_point_ax[0]) > 1500) & (int(element_1[1]) - int(pre_peak_point_ax[0]) < 10000)):
                        stroke_count_ax = stroke_count_ax +1
                        peak_point_ax[0] = int(element_1[1])
                        peak_point_ax[1] = float(element[1])
                        peak_point_list_ax.append(str(peak_point_ax))
                        pre_peak_point_ax[0] = peak_point_ax[0]
                        pre_peak_point_ax[1] = peak_point_ax[1]
        
    
        if(stroke_count_ay == 0):
            if((float(element[2]) < -10) & ((float(element2[2]) < -10)) ):
                if(  (( float(element2[2]) - float(element[2]) ) > 0) & (( float(element[2]) - float(element3[2]) ) < 0)  ):
                    stroke_count_ay = stroke_count_ay +1
                    peak_point_ay[0] = int(element_1[1])
                    peak_point_ay[1] = float(element[2])
                    peak_point_list_ay.append(str(peak_point_ay))
                    pre_peak_point_ay[0] = peak_point_ay[0]
                    pre_peak_point_ay[1] = peak_point_ay[1]

        elif(stroke_count_ay >= 1):
            if((float(element[2]) < -10) & ((float(element2[2]) < -10)) ):
                if(  (( float(element2[2]) - float(element[2]) ) > 0) & (( float(element[2]) - float(element3[2]) ) < 0)  ):
                    if ((int(element_1[1]) - int(pre_peak_point_ay[0]) > 1500)  & (int(element_1[1]) - int(pre_peak_point_ay[0]) < 10000)):
                        stroke_count_ay = stroke_count_ay +1
                        peak_point_ay[0] = int(element_1[1])
                        peak_point_ay[1] = float(element[2])
                        peak_point_list_ay.append(str(peak_point_ay))
                        pre_peak_point_ay[0] = peak_point_ay[0]
                        pre_peak_point_ay[1] = peak_point_ay[1]
                

    print "stroke_count on acc x in green", stroke_count_ax
    print "stroke_count on acc y in purple", stroke_count_ay
    print "stroke_count on acc xy in magenta", stroke_count_axy
    # print peak_point_list_ax[41]
    # print peak_point_list_ay[40]
    # print peak_point_list[41].split(",")
    # print peak_point_list_ax[40].split(",")
    

    fig = figure(1,figsize=(60,5))
    ay = fig.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
    line, = ay.plot(acc_t, acc_y, lw=3, color='purple')

    for index in range(0, stroke_count_ay ,1):
        element = peak_point_list_ay[index].split(",")
        element_1 = element[0].split("[")
        element_2 = element[1].split("]")

        ay.annotate('SC '+ str(index+1), xy=(element_1[1], element_2[0]),  xycoords='data', color='purple',
            xytext=(-50, -30), textcoords='offset points',
            arrowprops=dict(arrowstyle="->",
                connectionstyle="angle3,angleA=0,angleB=-90"),
            )

    fig_ax = figure(1,figsize=(60,5))
    ax = fig_ax.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
    line, = ax.plot(acc_t, acc_x, lw=3, color='green')

    for index in range(0, stroke_count_ax ,1):
        element = peak_point_list_ax[index].split(",")
        element_1 = element[0].split("[")
        element_2 = element[1].split("]")

        ax.annotate('SC '+ str(index+1), xy=(element_1[1], element_2[0]),  xycoords='data', color='green',
            xytext=(-50, -30), textcoords='offset points',
            arrowprops=dict(arrowstyle="->",
                connectionstyle="angle3,angleA=0,angleB=-90"),
            )

    fig_axy = figure(1,figsize=(60,5))
    axy = fig_axy.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))

    line, = axy.plot(acc_t, acc_xy, lw=3, color='magenta')

    for index in range(0, stroke_count_axy ,1):
        element = peak_point_list_xy[index].split(",")
        element_1 = element[0].split("[")
        element_2 = element[1].split("]")

        ax.annotate('SC '+ str(index+1), xy=(element_1[1], element_2[0]),  xycoords='data', color='magenta',
            xytext=(50, 30), textcoords='offset points',
            arrowprops=dict(arrowstyle="->",
                connectionstyle="angle3,angleA=0,angleB=-90"),
            )



    # fig_az = figure(1,figsize=(60,5))
    # az = fig_az.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))

    # line, = az.plot(acc_t, acc_z, lw=3, color='yellow')

    # fig_aN = figure(1,figsize=(60,5))
    # aN = fig_aN.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))

    # line, = aN.plot(acc_t, acc_N, lw=3, color='white')



    # for index in range(0, stroke_count_ay ,1):
    #     element = peak_point_list_ax[index].split(",")
    #     element_1 = element[0].split("[")
    #     element_2 = element[1].split("]")

    #     ax.annotate('SC '+ str(index+1), xy=(element_1[1], element_2[0]),  xycoords='data', color='green',
    #         xytext=(-50, -30), textcoords='offset points',
    #         arrowprops=dict(arrowstyle="->",
    #             connectionstyle="angle3,angleA=0,angleB=-90"),
    #         )

    # ax.annotate('stroke count 1', xy=(16150, -17.749741448),  xycoords='data',
    #             xytext=(-50, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #                              connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )

    # ax.annotate('stroke count 2', xy=(18800, -21.228140603999996),  xycoords='data',
    #             xytext=(-50, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #              connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )

    # ax.annotate('stroke count 3', xy=(21650., -16.493635826000002),  xycoords='data',
    #             xytext=(-50, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #              connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )
    # ax.annotate('stroke count 4', xy=(24500., -12.536584823999998),  xycoords='data',
    #             xytext=(-50, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #              connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )
    # ax.annotate('stroke count 5', xy=(30050., -17.380316899199997),  xycoords='data',
    #             xytext=(-50, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #              connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )

    # ax.annotate('arc', xy=(1.5, -1),  xycoords='data',
    #             xytext=(-40, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #                             connectionstyle="arc,angleA=0,armA=20,angleB=-90,armB=15,rad=7"),
    #             )

    # ax.annotate('angle', xy=(2., 1),  xycoords='data',
    #             xytext=(-50, 30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #                             connectionstyle="angle,angleA=0,angleB=90,rad=10"),
    #             )

    # ax.annotate('angle3', xy=(2.5, -1),  xycoords='data',
    #             xytext=(-50, -30), textcoords='offset points',
    #             arrowprops=dict(arrowstyle="->",
    #                             connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )


    # ax.annotate('angle', xy=(3., 1),  xycoords='data',
    #             xytext=(-50, 30), textcoords='offset points',
    #             bbox=dict(boxstyle="round", fc="0.8"),
    #             arrowprops=dict(arrowstyle="->",
    #                             connectionstyle="angle,angleA=0,angleB=90,rad=10"),
    #             )

    # ax.annotate('angle', xy=(3.5, -1),  xycoords='data',
    #             xytext=(-70, -60), textcoords='offset points',
    #             size=20,
    #             bbox=dict(boxstyle="round4,pad=.5", fc="0.8"),
    #             arrowprops=dict(arrowstyle="->",
    #                             connectionstyle="angle,angleA=0,angleB=-90,rad=10"),
    #             )

    # ax.annotate('angle', xy=(4., 1),  xycoords='data',
    #             xytext=(-50, 30), textcoords='offset points',
    #             bbox=dict(boxstyle="round", fc="0.8"),
    #             arrowprops=dict(arrowstyle="->",
    #                             shrinkA=0, shrinkB=10,
    #                             connectionstyle="angle,angleA=0,angleB=90,rad=10"),
    #             )


    # ann = ax.annotate('', xy=(4., 1.),  xycoords='data',
    #             xytext=(4.5, -1), textcoords='data',
    #             arrowprops=dict(arrowstyle="<->",
    #                             connectionstyle="bar",
    #                             ec="k",
    #                             shrinkA=5, shrinkB=5,
    #                             )
    #             )


if 1:

    gyro_t = []
    gyro_x = []
    gyro_y = []
    gyro_z = []
    for index in range(0, len(smoothen_list_gyro), 1):
        element = smoothen_list_gyro[index].split(",")
        element0 = element[0].split("[")
        element1 = element[3].split("]")
        gyro_t.append(int(element0[1]))
        gyro_x.append(float(element[1]))
        gyro_y.append(float(element[2]))
        gyro_z.append(float(element1[0]))

    stroke_count_gx = 0
    peak_point_gx = [0, 0]
    pre_peak_point_gx = [0, 0]
    peak_point_list_gx = []

    for index in range(1, len(smoothen_list_gyro)-1, 1):
        element  = smoothen_list_gyro[index].split(",")
        element_1 = element[0].split("[")

        element2 = smoothen_list_gyro[index+1].split(",")
        element3 = smoothen_list_gyro[index-1].split(",")
        
        if(stroke_count_gx == 0):
            if((float(element[1]) < -3.0) & ((float(element2[1]) < -3.0)) ):
                if(  (( float(element2[1]) - float(element[1]) ) > 0.0) & (( float(element[1]) - float(element3[1]) ) < 0.0)  ):
                    stroke_count_gx = stroke_count_gx +1
                    peak_point_gx[0] = int(element_1[1])
                    peak_point_gx[1] = float(element[1])
                    peak_point_list_gx.append(str(peak_point_gx))
                    pre_peak_point_gx[0] = peak_point_gx[0]
                    pre_peak_point_gx[1] = peak_point_gx[1]
        elif(stroke_count_gx >= 1):
            if((float(element[1]) < -3) & ((float(element2[1]) < -3)) ):
                if(  (( float(element2[1]) - float(element[1]) ) > 0) & (( float(element[1]) - float(element3[1]) ) < 0)  ):
                    if ((int(element_1[1]) - int(pre_peak_point_gx[0]) > 1000) & (int(element_1[1]) - int(pre_peak_point_gx[0]) < 10000)):
                        stroke_count_gx = stroke_count_gx +1
                        peak_point_gx[0] = int(element_1[1])
                        peak_point_gx[1] = float(element[1])
                        peak_point_list_gx.append(str(peak_point_gx))
                        pre_peak_point_gx[0] = peak_point_gx[0]
                        pre_peak_point_gx[1] = peak_point_gx[1]

    print "stroke_count_gx = " + str(stroke_count_gx)

    # fig = figure(2)
    # fig.clf()
    # ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1,5), ylim=(-5,3))



    fig_gx = figure(2,figsize=(60,5))
    gx = fig_gx.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
    line, = gx.plot(gyro_t, gyro_x, lw=3, color='purple')

    for index in range(0, len(peak_point_list_gx) ,1):
        element = peak_point_list_gx[index].split(",")
        element_1 = element[0].split("[")
        element_2 = element[1].split("]")

        gx.annotate('SC_gx '+ str(index+1), xy=(element_1[1], element_2[0]),  xycoords='data', color='purple',
            xytext=(-50, -30), textcoords='offset points',
            arrowprops=dict(arrowstyle="->",
                connectionstyle="angle3,angleA=0,angleB=-90"),
            )

    fig_gy = figure(2,figsize=(60,5))
    gy = fig_gy.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
    line, = gy.plot(gyro_t, gyro_y, lw=3, color='green')

    # fig_gz = figure(2,figsize=(60,5))
    # gz = fig_gz.add_subplot(111, autoscale_on=False, xlim=(0,180000), ylim=(-35,35))
    # line, = gz.plot(gyro_t, gyro_z, lw=3, color='magenta')    
    # el = Ellipse((2, -1), 0.5, 0.5)
    # ax.add_patch(el)

    # ax.annotate('$->$', xy=(2., -1),  xycoords='data',
    #             xytext=(-150, -140), textcoords='offset points',
    #             bbox=dict(boxstyle="round", fc="0.8"),
    #             arrowprops=dict(arrowstyle="->",
    #                             patchB=el,
    #                             connectionstyle="angle,angleA=90,angleB=0,rad=10"),
    #             )

    # ax.annotate('fancy', xy=(2., -1),  xycoords='data',
    #             xytext=(-100, 60), textcoords='offset points',
    #             size=20,
    #             #bbox=dict(boxstyle="round", fc="0.8"),
    #             arrowprops=dict(arrowstyle="fancy",
    #                             fc="0.6", ec="none",
    #                             patchB=el,
    #                             connectionstyle="angle3,angleA=0,angleB=-90"),
    #             )

    # ax.annotate('simple', xy=(2., -1),  xycoords='data',
    #             xytext=(100, 60), textcoords='offset points',
    #             size=20,
    #             #bbox=dict(boxstyle="round", fc="0.8"),
    #             arrowprops=dict(arrowstyle="simple",
    #                             fc="0.6", ec="none",
    #                             patchB=el,
    #                             connectionstyle="arc3,rad=0.3"),
    #             )

    # ax.annotate('wedge', xy=(2., -1),  xycoords='data',
    #             xytext=(-100, -100), textcoords='offset points',
    #             size=20,
    #             #bbox=dict(boxstyle="round", fc="0.8"),
    #             arrowprops=dict(arrowstyle="wedge,tail_width=0.7",
    #                             fc="0.6", ec="none",
    #                             patchB=el,
    #                             connectionstyle="arc3,rad=-0.3"),
    #             )


    # ann = ax.annotate('wedge', xy=(2., -1),  xycoords='data',
    #             xytext=(0, -45), textcoords='offset points',
    #             size=20,
    #             bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec=(1., .5, .5)),
    #             arrowprops=dict(arrowstyle="wedge,tail_width=1.",
    #                             fc=(1.0, 0.7, 0.7), ec=(1., .5, .5),
    #                             patchA=None,
    #                             patchB=el,
    #                             relpos=(0.2, 0.8),
    #                             connectionstyle="arc3,rad=-0.1"),
    #             )

    # ann = ax.annotate('wedge', xy=(2., -1),  xycoords='data',
    #             xytext=(35, 0), textcoords='offset points',
    #             size=20, va="center",
    #             bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"),
    #             arrowprops=dict(arrowstyle="wedge,tail_width=1.",
    #                             fc=(1.0, 0.7, 0.7), ec="none",
    #                             patchA=None,
    #                             patchB=el,
    #                             relpos=(0.2, 0.5),
    #                             )
    #             )


show()
