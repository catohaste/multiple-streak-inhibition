########################################################################################
"""
File allowing the inspection of variables from pickles
"""
########################################################################################

import pickle
import numpy as np

from plot import create_animated_output

# save_directory = 'results/100cells/'
# save_directory = 'results/**_asymmetric_cut/remove_35L_24R/'
save_directory = 'results/**_intact_embryo/'

number_of_cells = 100

########################################################################################
""" Pickle variables """

pickle_directory = save_directory + 'vars/'
    
t = pickle.load( open(pickle_directory + 't.p','rb') )
a = pickle.load( open(pickle_directory + 'a.p','rb') )
b = pickle.load( open(pickle_directory + 'b.p','rb') )
c = pickle.load( open(pickle_directory + 'c.p','rb') )
v = pickle.load( open(pickle_directory + 'v.p','rb') )

########################################################################################
print("Basic time data")
print(t.shape)
print(t[0],t[-1])
print("")

########################################################################################
print("Basic calcium data")
print(c.shape)
print(np.min(c),np.max(c))
print("")

########################################################################################
print("Rescale time")
time_scaling = int((t.shape[0]-1) / (c.shape[1]-1))
print(time_scaling)

########################################################################################
print("When does calcium come on intact embryo?")
temp_c = 0
t_idx_counter = 0
while temp_c == 0:
    temp_c = np.max(c[:,t_idx_counter])
    t_idx_counter += 1
print(t_idx_counter, t[t_idx_counter]*time_scaling)
print('')
ca_on_idx = 15
ca_zero_idx = ca_on_idx - 1
    
########################################################################################
print("When does calcium reach equilibrium intact embryo?")
max_c = np.max(c)
temp_max_c = 0
t_idx_counter = 0
while temp_max_c < max_c:
    temp_max_c = np.max(c[:,t_idx_counter])
    t_idx_counter += 1
print(t_idx_counter, t[t_idx_counter]*time_scaling)
print('')
# c_idx = 229, t = 0.0229???
# 228 == 229

########################################################################################
print("Verify calcium reached equilibrium")
t_idx = 227

print('Time')
print(t_idx, t[t_idx])
print(t_idx+1, t[t_idx+1])
print(t_idx+2, t[t_idx+2])

print('\nCalcium')
print(c[0, t_idx], c[49, t_idx], c[50, t_idx], c[99,t_idx])
print(c[0, t_idx+1], c[49, t_idx+1], c[50, t_idx+1], c[99,t_idx+1])
print(c[0, t_idx+2], c[49, t_idx+2], c[50, t_idx+2], c[99,t_idx+2])

########################################################################################
print("\nWhat is the rate of increase of calcium")
# choose random cell
cell_idx = 25

def get_rate_of_increase(cal, t, cell_idx, t_idx, time_scaling):
    change_cal = cal[cell_idx, t_idx+1] - cal[cell_idx, t_idx]
    change_time = t[int((t_idx+1)*time_scaling)] - t[int(t_idx*time_scaling)]
    return change_cal / change_time
    
print('rate', get_rate_of_increase(c, t, 25, ca_zero_idx, time_scaling))
print('rate', get_rate_of_increase(c, t, 25, 50, time_scaling))
print('rate', get_rate_of_increase(c, t, 25, 100, time_scaling))
print('rate', get_rate_of_increase(c, t, 25, 150, time_scaling))
print('rate', get_rate_of_increase(c, t, 25, 200, time_scaling))



########################################################################################
print("\nHow long does it take for calcium to increase 5%")

def get_increase_10_percent_time(cal, t, cell_idx, t_idx, time_scaling):
    start_cal = cal[cell_idx, t_idx]
    t_inc = 0
    temp_cal = cal[cell_idx, t_idx + t_inc]
    while temp_cal < start_cal*1.05:
        print(start_cal, temp_cal, start_cal*1.05)
        t_inc += 1
        temp_cal = cal[cell_idx, t_idx + t_inc]
    start_time = t[int(t_idx*time_scaling)]
    end_time = t[int((t_idx+t_inc)*time_scaling)]
    return t_idx, start_time,  end_time - start_time
    
print(get_increase_10_percent_time(c, t, 3, 15, time_scaling))


########################################################################################
print("\nTotal calcium in the system at equilibrium")
print(np.sum(c[:,228]))


