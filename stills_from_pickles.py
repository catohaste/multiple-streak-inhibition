import pickle
import numpy as np
import os.path
from copy import deepcopy

from plot import create_animated_output, create_stills_array

save_directory = 'results/nCellsExp/100cells/'

number_of_cells = 100

########################################################################################
""" Load pickled variables """

pickle_directory = save_directory + 'vars/'
    
t = pickle.load( open(pickle_directory + 't.p','rb') )
a = pickle.load( open(pickle_directory + 'a.p','rb') )
b = pickle.load( open(pickle_directory + 'b.p','rb') )
c = pickle.load( open(pickle_directory + 'c.p','rb') )
v = pickle.load( open(pickle_directory + 'v.p','rb') )
    
########################################################################################
""" Create animated output """

stills_directory = save_directory + 'stills/'
if not os.path.isdir(stills_directory):
    os.mkdir(stills_directory)

t = np.around(t, 2)

# stills_timepoints = [-1.2, -0.6, 0, 0.02, 1, 2.68, 3.4, 3.8, 5.1, 8.8]
stills_early_timepoints = [-1.2, -0.6, 0, 0.02, 1]
stills_late_timepoints = [2.68, 3.4, 3.8, 5.1, 8.8]
stills_early_indices = deepcopy(stills_early_timepoints)
stills_late_indices = deepcopy(stills_late_timepoints)   
for idx, val in enumerate(stills_early_timepoints):
    stills_early_indices[idx] = list(t).index(val)
for idx, val in enumerate(stills_late_timepoints):
    stills_late_indices[idx] = list(t).index(val)

create_stills_array(stills_early_indices, number_of_cells, t, a, b, v, c, stills_directory + 'early_timepoints.png')
create_stills_array(stills_late_indices, number_of_cells, t, a, b, v, c, stills_directory + 'late_timepoints.png')

# create_animated_output(number_of_cells, 1, t, a, b, v, c, stills_directory + )

