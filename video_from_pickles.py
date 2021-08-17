import pickle
import matplotlib.pyplot as plt

from plot import create_animated_output, create_animated_output_extra_calcium, create_circle_animation, concentric_circle_animation

from params import params

save_directory = 'results/testing/'

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

# create_animated_output_extra_calcium(number_of_cells, 1, t, a, b, v, c, params, save_directory)

concentric_circle_animation(t, a, b, c, v, save_directory)