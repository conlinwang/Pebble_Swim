# copy_file.py


from sklearn import linear_model
import numpy as np
import os
import math
import shutil
import stat

from pylab import *
from matplotlib.pyplot import figure, show
from matplotlib.patches import Ellipse
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost

from matplotlib import rc


path = "./"
dirs = os.listdir( path )

for file in dirs:
   # print file
   print file
   