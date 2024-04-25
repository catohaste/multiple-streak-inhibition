#!/usr/bin/env python3

import time
from datetime import datetime
import os.path
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy
import pickle
from shutil import copy2

from models import solve_ivp_odes, solve_ivp_odes_Hill, calcium_periodic_boundary, calcium_no_flux_boundary

from plot import create_animated_output

from params import params

'''
dy / dt = f(t, y)
y(t0) = y0
'''

total_start = time.time()

########################################################################################
""" Set run details """

if not os.path.isdir('results'):
    os.mkdir('results')

now = datetime.now()
date_time_str = 'results/' + now.strftime("%Y_%m_%d_%H%M") + '/'

save_directory = date_time_str

if not os.path.isdir(save_directory):
    os.mkdir(save_directory)
    
########################################################################################
""" Save code """
    
code_directory = save_directory + 'code/'
if not os.path.isdir(code_directory):
    os.mkdir(code_directory)

filenames = ['intact_embryo.py', 'params.py', 'models.py', 'plot.py']
for filename in filenames:
    copy2(filename, code_directory + filename)

########################################################################################
""" Set 'length' parameters """

number_of_cells = 100
dx = 0.094248 # mm
dt = 0.0001 # /4
sample_rate = 200 # sample_rate of variables when pickling

# number_of_cells = 748
# dx = 0.0126 # 0.094248 / 7.48
# dt = 0.0001/64 # approximately 7.48^2
# sample_rate = int(200 * 64)
# params['k'] = params['k'] * 7.48

########################################################################################
""" Set desired timepoints """

start_time = 0
# total_time = 20
# cut_time = 2.4
total_time = 20

t = np.append(np.arange(0, total_time, dt), total_time)
number_of_timepoints = len(t)
store_t = t[::sample_rate]
store_timepoints = len(store_t)
# print(number_of_timepoints, store_timepoints)
# print(store_t[-1])

########################################################################################
""" BEFORE CUT """

# Set initial conditions
a0 = np.zeros((number_of_cells), dtype=float)
c0 = np.zeros((number_of_cells), dtype=float)
v0 = np.zeros((number_of_cells), dtype=float)
b0 = np.zeros((number_of_cells), dtype=float)
b_min = 1.1
b_max = 2.2
for i in range(int((number_of_cells+1)/2)):
    j = number_of_cells - i - 1
    b0[i] = ((b_max - b_min)/number_of_cells) * 2 * i + b_min
    b0[j] = ((b_max - b_min)/number_of_cells) * 2 * i + b_min

# rotated initial conditions, only one 'posterior cell'
# b0[0] = b_min
# for i in range(1, int(number_of_cells/2) + 1):
#     j = number_of_cells - i
#     b0[i] = ((b_max - b_min)/number_of_cells) * 2 * i + b_min
#     b0[j] = ((b_max - b_min)/number_of_cells) * 2 * i + b_min

start = time.time()

a, b, c, v = solve_ivp_odes(number_of_cells, number_of_timepoints, dt, dx, a0, b0, c0, v0, calcium_periodic_boundary, params, sample_rate)
# a, b, c, v = solve_ivp_odes_Hill(number_of_cells, number_of_timepoints, dt, dx, a0, b0, c0, v0, calcium_periodic_boundary, params, sample_rate)

end = time.time()
print("Time consumed solving: ",end - start)

########################################################################################
""" Pickle variables """

pickle_directory = save_directory + 'vars/'
if not os.path.isdir(pickle_directory):
    os.mkdir(pickle_directory)
    
pickle.dump( store_t, open(pickle_directory + 't.p','wb') )
pickle.dump( a, open(pickle_directory + 'a.p','wb') )
pickle.dump( b, open(pickle_directory + 'b.p','wb') )
pickle.dump( c, open(pickle_directory + 'c.p','wb') )
pickle.dump( v, open(pickle_directory + 'v.p','wb') )

########################################################################################
""" Create animated output """

create_animated_output(number_of_cells, store_t, a, b, v, c, params, save_directory + 'intact')

# concentric_circle_animation(t, a, b, c, v, save_directory)

total_end = time.time()
print("Total time consumed in working: ", total_end - total_start)
