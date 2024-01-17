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
# save_directory = 'results/**_intact_embryo/'
# save_directory = 'results/study_calcium/D_50/'
save_directory = 'results/vary_params_2023/beta_V_2_19/'
# save_directory = 'results/vary_params_2023/standard_cut/'

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
print("")
print("Basic time data")
print(t.shape)
print(t[0],t[-1])

timepoint_N = t.shape[0]

########################################################################################
print("")
print("Check time scaling")
time_scaling = int((t.shape[0]-1) / (c.shape[1]-1))
print(time_scaling)

########################################################################################
print("")
print("Find time of cut")
cut_time_idx = 0

while all(i >= 0 for i in c[:,cut_time_idx]):
    cut_time_idx += 1

# print(cut_time_idx - 1, t[cut_time_idx - 1])
# print(t[cut_time_idx - 1], c[:,cut_time_idx - 1])
# print(t[cut_time_idx], c[:,cut_time_idx])

########################################################################################
print("")
print("Find shape after cut")

bool_cells_after_cut = c[:,cut_time_idx]>=0
idx_cells_after_cut = [i for i, x in enumerate(bool_cells_after_cut) if x]
cells_after_cut_N = sum(bool_cells_after_cut)
print(cells_after_cut_N)

print(min(bool_cells_after_cut * c[:,cut_time_idx]))

########################################################################################
print("")
print("Calcium data")

print("Min max just precut", min(c[:,cut_time_idx-1]), max(c[:,cut_time_idx-1]))
c_at_end = [c[idx, -1] for idx in idx_cells_after_cut]
print("Min max end,", min(c_at_end), max(c_at_end))

########################################################################################
print("")
print("When does calcium come on precut?")
temp_c = 0
t_idx_counter = 0
while temp_c == 0:
    temp_c = np.max(c[:,t_idx_counter])
    t_idx_counter += 1
print(t_idx_counter, t[t_idx_counter]*time_scaling)
ca_on_idx = t_idx_counter
ca_zero_idx = ca_on_idx - 1
    
########################################################################################
print("")
print("Does calcium reach equilibrium precut?")

print("Min max just precut minus 1", min(c[:,cut_time_idx-2]), max(c[:,cut_time_idx-2]))
print("Min max just precut", min(c[:,cut_time_idx-1]), max(c[:,cut_time_idx-1]))

print("Precut bool, ", min(c[:,cut_time_idx-2]) == min(c[:,cut_time_idx-1]), max(c[:,cut_time_idx-2]) == max(c[:,cut_time_idx-1]))

########################################################################################
print("")
print("Does calcium reach equilibrium postcut?")

c_at_end_minus_1 = [c[idx, -2] for idx in idx_cells_after_cut]
print("Min max end minus 1", min(c_at_end_minus_1), max(c_at_end_minus_1))
print("Min max end", min(c_at_end), max(c_at_end))

print("End bool, ", min(c_at_end_minus_1) == min(c_at_end), max(c_at_end_minus_1) == max(c_at_end))

########################################################################################
print("")
print("When does calcium reach equilibrium postcut?")
max_c = max(c_at_end)
temp_max_c = 0
t_idx_counter_max = 0
while temp_max_c < max_c:
    temp_max_c = np.max(c[:,t_idx_counter_max])
    t_idx_counter_max += 1
print(t_idx_counter_max, t[t_idx_counter_max]*time_scaling)

########################################################################################
print("")
print("Verify calcium reached equilibrium postcut")
t_idx = t_idx_counter_max - 2

print('Time')
print(t_idx, t[t_idx])
print(t_idx+1, t[t_idx+1])
print(t_idx+2, t[t_idx+2])

print('\nCalcium')
left_cell_post_cut = min(idx_cells_after_cut)
right_cell_post_cut = max(idx_cells_after_cut)
print(c[left_cell_post_cut, t_idx], c[right_cell_post_cut, t_idx])
print(c[left_cell_post_cut, t_idx+1], c[right_cell_post_cut, t_idx+1])
print(c[left_cell_post_cut, t_idx+2], c[right_cell_post_cut, t_idx+2])

########################################################################################
print("\nTotal calcium in the system at pre cut")
print(np.sum(c[:,cut_time_idx-1]))

print("\nTotal calcium in the system at equilibrium post cut")
print(np.sum(c_at_end))

########################################################################################
print("\nBMP and Vg1 min and max at end")
print("BMP ", b[left_cell_post_cut, -1], b[right_cell_post_cut, -1])
print("Vg1 ", v[left_cell_post_cut, -1], v[right_cell_post_cut, -1])


