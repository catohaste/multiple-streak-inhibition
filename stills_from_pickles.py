import pickle
import numpy as np
import os.path
from copy import deepcopy

from plot import create_animated_output, create_stills_array

# save_directory = 'results/**_asymmetric_cut/remove_35L_24R/'
# save_directory = 'results/testing/'
# save_directory = 'results/symmetric_large_cut/36_remaining/'

save_directory = 'results/2024_03_18_1117/'

number_of_cells = 100

########################################################################################
""" Load pickled variables """

pickle_directory = save_directory + 'vars/'
    
t = pickle.load( open(pickle_directory + 't.p','rb') )
a = pickle.load( open(pickle_directory + 'a.p','rb') )
b = pickle.load( open(pickle_directory + 'b.p','rb') )
c = pickle.load( open(pickle_directory + 'c.p','rb') )
v = pickle.load( open(pickle_directory + 'v.p','rb') )

print(t)

########################################################################################
""" Load params """

code_directory = save_directory + 'code/'

import sys
sys.path.insert(1, code_directory)

from params import params

    
########################################################################################
""" Create animated output """

stills_directory = save_directory + 'stills/'
if not os.path.isdir(stills_directory):
    os.mkdir(stills_directory)

t = np.around(t, 2)

print(t)
print(len(t))

# # stills_timepoints = [-1.2, -0.6, 0, 0.02, 1, 2.28, 3.04, 3.8, 5.1, 8.8]
# stills_early_timepoints = [-1.2, -0.6, 0, 0.02, 1]
# stills_late_timepoints = [2.28, 3.04, 3.8, 5.1, 8.8]
# # stills_late_timepoints = [2.28, 3.04, 3.8, 4.3, 5.1]
# stills_early_indices = deepcopy(stills_early_timepoints)
# stills_late_indices = deepcopy(stills_late_timepoints)
# for idx, val in enumerate(stills_early_timepoints):
#     stills_early_indices[idx] = list(t).index(val)
# for idx, val in enumerate(stills_late_timepoints):
#     stills_late_indices[idx] = list(t).index(val)
#
# create_stills_array(stills_early_indices, number_of_cells, t, a, b, v, c, params, stills_directory + 'early_timepoints.png')
# create_stills_array(stills_late_indices, number_of_cells, t, a, b, v, c, params, stills_directory + 'late_timepoints.png')

# create_animated_output(number_of_cells, 1, t, a, b, v, c, stills_directory + )

stills_intact_timepoints = [0.0, 0.2, 0.7, 5.0, 8.0]
stills_intact_indices = deepcopy(stills_intact_timepoints)   
for idx, val in enumerate(stills_intact_timepoints):
    stills_intact_indices[idx] = list(t).index(val)
    
# create_stills_array(stills_intact_indices, number_of_cells, t, a, b, v, c, params, stills_directory + 'intact_timepoints.png')

