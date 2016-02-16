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
def pool_length_function( file_name ):
#------------------------------------------------------------------------------------------------------------------------
	true_stroke_count = 0
	file_profile = file_name.split("_")
	pool_length = int(file_profile[-1])
	
	return pool_length

#------------------------------------------------------------------------------------------------------------------------
