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

def f2():
    global b
    b = 1
    print "in f2", b

b = 2
print "out of f2 1st time=", b
f2()
print "out of f2 2nd time=", b

print 3**2
print 2**0.5