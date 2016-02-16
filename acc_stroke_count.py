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

def raw_data_preprocess( into_file_name ):
	file_name = into_file_name

	if not os.path.exists("./"+file_name+"/stroke_count"):
		os.mkdir("./"+file_name+"/stroke_count")   

	input_data = open("./"+file_name+"/acc_cut/acc_LPF_5Hz.txt", "r+") # input_data
	line = input_data.readlines() # load data into python
	length = len(line)    # get how many data had being loaded 