#true_turn_count.py

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

# Determine the truth turn count
def true_turn_count( file_name ):
#------------------------------------------------------------------------------------------------------------------------
	file_profile = file_name.split("_")
	pool_length = int(file_profile[-1])
	true_distence = file_profile[-3].split("m")
	
	return int(true_distence[0]) / pool_length -1

#------------------------------------------------------------------------------------------------------------------------

# file_name_test = "0818_184637_Conlin_FCS_17_18_400m_L_50"
# print true_turn_count(file_name_test)