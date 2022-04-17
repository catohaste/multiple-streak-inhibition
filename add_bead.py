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

from models import solve_ivp_odes, calcium_periodic_boundary, calcium_no_flux_boundary

from plot import create_animated_output

from params import params

'''
dy / dt = f(t, y)
y(t0) = y0
'''

total_start = time.time()

########################################################################################
""" Set run details """

now = datetime.now()
date_time_str = 'results/' + now.strftime("%Y_%m_%d_%H%M") + '/'

# save_directory = date_time_str
# save_directory = 'results/add_bmp_bead/'
# save_directory = 'results/add_vg1_bead/'
save_directory = 'results/testing/'
if not os.path.isdir(save_directory):
    os.mkdir(save_directory)
    
########################################################################################
""" Save code """
    
code_directory = save_directory + 'code/'
if not os.path.isdir(code_directory):
    os.mkdir(code_directory)

filenames = ['add_bead.py', 'params.py', 'models.py', 'plot.py']
for filename in filenames:
    copy2(filename, code_directory + filename)

########################################################################################
""" Set 'length' parameters """

number_of_cells = 100
dx = 0.094248
dt = 0.0001 # /4
sample_rate = 200

bead_center = 46
bead_half_width = 2 # doesn't include centre cell { bead_half_width = (bead_width - 1) / 2 }
bead_concentration = 0.2

def add_bead(bead_var_atbead, bead_center, bead_half_width, bead_concentration):
    bead_cells = list(range(bead_center - bead_half_width, bead_center + bead_half_width + 1))
    for bead_cell in bead_cells:
        bead_var_atbead[bead_cell] = bead_var_atbead[bead_cell] + bead_concentration
        
    return bead_var_atbead
    

# number_of_cells = 748
# dx = 0.0126
# dt = 0.0001/64
# sample_rate = int(200 * 64)
# params['k'] = params['k'] * 7.48

# bead_center = 344
# bead_half_width = 15 # doesn't include centre cell { bead_half_width = (bead_width - 1) / 2 }
# bead_concentration = 0.2

########################################################################################
""" Set desired timepoints """

start_time = 0
# total_time = 20
# bead_time = 2.4
total_time = 10
bead_time = 1.2
postbead_time = total_time - bead_time

t_prebead = np.append(np.arange(0, bead_time, dt), bead_time)
number_of_timepoints_prebead = len(t_prebead)
store_t_prebead = t_prebead[::sample_rate]
store_timepoints_prebead = len(store_t_prebead)
# print(number_of_timepoints_prebead, store_timepoints_prebead)
# print(store_t_prebead[0], store_t_prebead[-1])

t_postbead = np.append(np.arange(bead_time, total_time, dt), total_time)
number_of_timepoints_postbead = len(t_postbead)
store_t_postbead = t_postbead[::sample_rate]
store_timepoints_postbead = len(store_t_postbead)
# print(number_of_timepoints_postbead, store_timepoints_postbead)
# print(store_t_postbead[0], store_t_postbead[-1])


########################################################################################
""" BEFORE BEAD """

# Set initial conditions
a0 = np.zeros((number_of_cells), dtype=float)
c0 = np.zeros((number_of_cells), dtype=float)
v0 = np.zeros((number_of_cells), dtype=float)
b0 = np.zeros((number_of_cells), dtype=float)
b_min = 1.1
b_max = 1.3
# b_min = 1.1
# b_max = 2.2
for i in range(int(number_of_cells/2)):
    j = number_of_cells - i - 1
    b0[i] = ((b_max - b_min)/number_of_cells) * 2 * i + b_min
    b0[j] = ((b_max - b_min)/number_of_cells) * 2 * i + b_min

start = time.time()

a_prebead, b_prebead, c_prebead, v_prebead = solve_ivp_odes(number_of_cells, number_of_timepoints_prebead, dt, dx, a0, b0, c0, v0, calcium_periodic_boundary, params, sample_rate)

end = time.time()
print("Time consumed solving prebead: ",end - start)

########################################################################################
""" PLACE BEAD AND SOLVE """

# Set initial conditions for post bead
a_atbead = a_prebead[:, -1]
b_atbead = b_prebead[:, -1]
c_atbead = c_prebead[:, -1]
v_atbead = v_prebead[:, -1]

# Place bmp bead
# b_atbead = add_bead(b_atbead, bead_center, bead_half_width, bead_concentration)

# Place DM bead
# b_atbead = add_bead(b_atbead, bead_center, bead_half_width, -bead_concentration)

# Place ionomycin bead
# this doesn't work. this implies removing all calcium (at bead location) instantaneously. system quickly requilibrates
c_atbead = add_bead(c_atbead, bead_center, bead_half_width, -5.0)

# Place vg1 bead
# v_atbead = add_bead(v_atbead, bead_center, 1, 1.0)

start = time.time()

a_postbead, b_postbead, c_postbead, v_postbead = solve_ivp_odes(number_of_cells, number_of_timepoints_postbead, dt, dx, a_atbead, b_atbead, c_atbead, v_atbead, calcium_periodic_boundary, params, sample_rate)

end = time.time()
print("Time consumed solving postbead: ",end - start)

########################################################################################
""" Concatenate pre- and post-bead """

# the time index '1' here gets rid of the duplicate of t=0.1 at bead placement
t_postbead = store_t_postbead[1:]
postbead_steps = len(t_postbead)

# # must also remove corresponding point in variable arrays
a_postbead_alt = a_postbead[:,1:]
b_postbead_alt = b_postbead[:,1:]
c_postbead_alt = c_postbead[:,1:]
v_postbead_alt = v_postbead[:,1:]

t = np.concatenate((store_t_prebead, t_postbead))
t_relative_to_bead = t - bead_time

a = np.concatenate((a_prebead, a_postbead_alt),axis=1)
b = np.concatenate((b_prebead, b_postbead_alt),axis=1)
c = np.concatenate((c_prebead, c_postbead_alt),axis=1)
v = np.concatenate((v_prebead, v_postbead_alt),axis=1)

########################################################################################
""" Pickle variables """

pickle_directory = save_directory + 'vars/'
if not os.path.isdir(pickle_directory):
    os.mkdir(pickle_directory)
    
pickle.dump( t_relative_to_bead, open(pickle_directory + 't.p','wb') )
pickle.dump( a, open(pickle_directory + 'a.p','wb') )
pickle.dump( b, open(pickle_directory + 'b.p','wb') )
pickle.dump( c, open(pickle_directory + 'c.p','wb') )
pickle.dump( v, open(pickle_directory + 'v.p','wb') )

########################################################################################
""" Create animated output """

create_animated_output(number_of_cells, t_relative_to_bead, a, b, v, c, params, save_directory)

total_end = time.time()
print("Total time consumed in working: ",total_end - total_start)
