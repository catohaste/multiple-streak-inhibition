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

filenames = ['make_cut.py', 'params.py', 'models.py', 'plot.py']
for filename in filenames:
    copy2(filename, code_directory + filename)

########################################################################################
""" Set 'length' parameters """

number_of_cells_precut = 100
dx = 0.094248
# left_post_cut = 26
# right_post_cut = 24
left_post_cut = 35
right_post_cut = 24
dt = 0.0001 # /4
sample_rate = 200

# nCellsExp
# space_multiple = 1
# time_multiple = 1
# number_of_cells_precut = 100 * space_multiple
# dx = 0.094248 / space_multiple
# left_post_cut = int(35 * space_multiple)
# right_post_cut = int(24 * space_multiple)
# dt = 0.0001 / (time_multiple * time_multiple)
# sample_rate = 200 * (time_multiple * time_multiple)
# params['k'] = params['k'] * space_multiple
# print(params['k'])

# number_of_cells_precut = 748
# dx = 0.0126
# left_post_cut = 262
# right_post_cut = 178
# dt = 0.0001/64
# sample_rate = int(200 * 64)
# params['k'] = params['k'] * 7.48

########################################################################################
""" Set desired timepoints """

start_time = 0
# total_time = 20
# cut_time = 2.4
total_time = 10
cut_time = 1.2
postcut_time = total_time - cut_time

t_precut = np.append(np.arange(0, cut_time, dt), cut_time)
number_of_timepoints_precut = len(t_precut)
store_t_precut = t_precut[::sample_rate]
store_timepoints_precut = len(store_t_precut)
# print(number_of_timepoints_precut, store_timepoints_precut)
# print(store_t_precut[0], store_t_precut[-1])

t_postcut = np.append(np.arange(cut_time, total_time, dt), total_time)
number_of_timepoints_postcut = len(t_postcut)
store_t_postcut = t_postcut[::sample_rate]
store_timepoints_postcut = len(store_t_postcut)
# print(number_of_timepoints_postcut, store_timepoints_postcut)
# print(store_t_postcut[0], store_t_postcut[-1])

########################################################################################
""" BEFORE CUT """

# Set initial conditions
a0 = np.zeros((number_of_cells_precut), dtype=float)
c0 = np.zeros((number_of_cells_precut), dtype=float)
v0 = np.zeros((number_of_cells_precut), dtype=float)
b0 = np.zeros((number_of_cells_precut), dtype=float)
b_min = 1.1
b_max = 2.2
for i in range(int((number_of_cells_precut+1)/2)):
    j = number_of_cells_precut - i - 1
    b0[i] = ((b_max - b_min)/number_of_cells_precut) * 2 * i + b_min
    b0[j] = ((b_max - b_min)/number_of_cells_precut) * 2 * i + b_min
    
# rotated initial conditions, only one 'posterior cell'
# b0[0] = b_min
# for i in range(1, int(number_of_cells_precut/2) + 1):
#     j = number_of_cells_precut - i
#     b0[i] = ((b_max - b_min)/number_of_cells_precut) * 2 * i + b_min
#     b0[j] = ((b_max - b_min)/number_of_cells_precut) * 2 * i + b_min

start = time.time()

a_precut, b_precut, c_precut, v_precut = solve_ivp_odes(number_of_cells_precut, number_of_timepoints_precut, dt, dx, a0, b0, c0, v0, calcium_periodic_boundary, params, sample_rate)
# a_precut, b_precut, c_precut, v_precut = solve_ivp_odes_Hill(number_of_cells_precut, number_of_timepoints_precut, dt, dx, a0, b0, c0, v0, calcium_periodic_boundary, params, sample_rate)

end = time.time()
print("Time consumed solving precut: ",end - start)

########################################################################################
""" MAKE CUT AND SOLVE """

anterior_half = range(left_post_cut, number_of_cells_precut - right_post_cut)

# Set initial conditions for post cut
a_atcut = [a_precut[ant_idx, -1] for ant_idx in anterior_half]
b_atcut = [b_precut[ant_idx, -1] for ant_idx in anterior_half]
c_atcut = [c_precut[ant_idx, -1] for ant_idx in anterior_half]
v_atcut = [v_precut[ant_idx, -1] for ant_idx in anterior_half]

number_of_cells_postcut = len(anterior_half)
print(anterior_half, number_of_cells_postcut)

start = time.time()

# "short" refers to number of cells present. arrays do not include cells removed at cut
a_postcut_short, b_postcut_short, c_postcut_short, v_postcut_short = solve_ivp_odes(number_of_cells_postcut, number_of_timepoints_postcut, dt, dx, a_atcut, b_atcut, c_atcut, v_atcut, calcium_no_flux_boundary, params, sample_rate)
# a_postcut_short, b_postcut_short, c_postcut_short, v_postcut_short = solve_ivp_odes_Hill(number_of_cells_postcut, number_of_timepoints_postcut, dt, dx, a_atcut, b_atcut, c_atcut, v_atcut, calcium_no_flux_boundary, params, sample_rate)

end = time.time()
print("Time consumed solving postcut: ",end - start)

########################################################################################
""" Concatenate pre- and post-cut, adding zeros to replace cut portion """

# the time index '1' here gets rid of the duplicate of t=1.2
t_postcut = store_t_postcut[1:]
postcut_steps = len(t_postcut)

# add zeros in-place of the cells removed at cut
# also removes first timepoint
# a_postcut = np.concatenate((np.zeros((left_post_cut,postcut_steps)), a_postcut_short[:,1:], np.zeros((right_post_cut,postcut_steps))))
# b_postcut = np.concatenate((np.zeros((left_post_cut,postcut_steps)), b_postcut_short[:,1:], np.zeros((right_post_cut,postcut_steps))))
# c_postcut = np.concatenate((np.zeros((left_post_cut,postcut_steps)), c_postcut_short[:,1:], np.zeros((right_post_cut,postcut_steps))))
# v_postcut = np.concatenate((np.zeros((left_post_cut,postcut_steps)), v_postcut_short[:,1:], np.zeros((right_post_cut,postcut_steps))))

# add -1s in-place of the cells removed at cut
# also removes first timepoint
a_postcut = np.concatenate((-1 * np.ones((left_post_cut,postcut_steps)), a_postcut_short[:,1:], -1 * np.ones((right_post_cut,postcut_steps))))
b_postcut = np.concatenate((-1 * np.ones((left_post_cut,postcut_steps)), b_postcut_short[:,1:], -1 * np.ones((right_post_cut,postcut_steps))))
c_postcut = np.concatenate((-1 * np.ones((left_post_cut,postcut_steps)), c_postcut_short[:,1:], -1 * np.ones((right_post_cut,postcut_steps))))
v_postcut = np.concatenate((-1 * np.ones((left_post_cut,postcut_steps)), v_postcut_short[:,1:], -1 * np.ones((right_post_cut,postcut_steps))))

t = np.concatenate((store_t_precut, t_postcut))
t_relative_to_cut = t - cut_time

a = np.concatenate((a_precut, a_postcut),axis=1)
b = np.concatenate((b_precut, b_postcut),axis=1)
c = np.concatenate((c_precut, c_postcut),axis=1)
v = np.concatenate((v_precut, v_postcut),axis=1)

########################################################################################
""" Pickle variables """

pickle_directory = save_directory + 'vars/'
if not os.path.isdir(pickle_directory):
    os.mkdir(pickle_directory)
    
pickle.dump( t_relative_to_cut, open(pickle_directory + 't.p','wb') )
pickle.dump( a, open(pickle_directory + 'a.p','wb') )
pickle.dump( b, open(pickle_directory + 'b.p','wb') )
pickle.dump( c, open(pickle_directory + 'c.p','wb') )
pickle.dump( v, open(pickle_directory + 'v.p','wb') )

########################################################################################
""" Create animated output """

create_animated_output(number_of_cells_precut, t_relative_to_cut, a, b, v, c, params, save_directory + 'cut')

# concentric_circle_animation(t, a, b, c, v, save_directory)

total_end = time.time()
print("Total time consumed in working: ", total_end - total_start)
