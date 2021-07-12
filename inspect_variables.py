import pickle
import numpy as np

from plot import create_animated_output

save_directory = 'results/100cells/'

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
""" Create animated output """

# print(len(t))
# print(t)

idx = 60

idx_2 = 500

print(idx, t[idx])
# print(c.shape)
print(c[0, idx], c[49, idx], c[50, idx], c[99,idx])
print(c[0, idx_2], c[49, idx_2], c[50, idx_2], c[99, idx_2])
print(c[35, idx_2-1], c[75, idx_2-1])
print(c[35, idx_2], c[75, idx_2])
print(np.max(c))

print(v[0, idx], v[49, idx], v[50, idx], v[99,idx])
print(v[0, idx_2], v[49, idx_2], v[50, idx_2], v[99, idx_2])
print(v[35, idx_2-1], v[75, idx_2-1])
print(v[35, idx_2], v[75, idx_2])
print(np.max(v))



# create_animated_output(number_of_cells, 1, t, a, b, v, c, params, save_directory)

