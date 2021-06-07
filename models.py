import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy


def calcium_periodic_boundary(c, number_of_cells, cell_idx):
    
    cell_idx_plus_one = (cell_idx + 1) % number_of_cells
    cell_idx_minus_one = (cell_idx - 1) % number_of_cells
    
    c_bar = 0.5 * (c[cell_idx_plus_one] + c[cell_idx_minus_one])
    
    return c_bar
    
def calcium_no_flux_boundary(c, number_of_cells, cell_idx):
    
    if cell_idx in range(1, number_of_cells - 1):
        c_bar = (c[cell_idx - 1] + c[cell_idx + 1]) / 2
    elif cell_idx == 0:
        c_bar = (c[0] + c[1]) / 2
    elif cell_idx == (number_of_cells - 1):
        c_bar = (c[number_of_cells - 2] + c[number_of_cells - 1]) / 2
    else:
        print('whoops')
        
    # print(c_bar.shape)
        
    # if len(c_bar) is not 1:
    #     print(cell_idx)
       
    return c_bar
    
def solve_ivp_odes(number_of_cells, number_of_timepoints, dt, dx, a0, b0, c0, v0, calcium_boundary_condition, params, sample_rate):
    
    # unpack params
    c_threshold = params["c_threshold"]
    c_b_threshold = params["c_b_threshold"]
    v_b_threshold = params["v_b_threshold"]
    rho = params["rho"]
    gamma_0 = params["gamma_0"]
    gamma = params["gamma"]
    k = params["k"]
    k_v = params["k_v"]
    mu = params["mu"]
    lambda_const = params["lambda_const"]
    lambda_const_v_0 = params["lambda_const_v_0"]
    lambda_const_v_b = params["lambda_const_v_b"]
    
    store_timepoints = int(((number_of_timepoints - 1) / sample_rate) + 1)
    t = range(number_of_timepoints)
    store_t = t[::sample_rate]
    
    # Preallocate
    a_store = np.ndarray((number_of_cells, store_timepoints), dtype=float)
    b_store = np.ndarray((number_of_cells, store_timepoints), dtype=float)
    c_store = np.ndarray((number_of_cells, store_timepoints), dtype=float)
    v_store = np.ndarray((number_of_cells, store_timepoints), dtype=float)

    H_c = np.ndarray((number_of_cells), dtype=int)
    H_c_b = np.ndarray((number_of_cells), dtype=int)
    H_v_b = np.ndarray((number_of_cells), dtype=int)

    # Initialize
    a_store[:,0] = a0
    b_store[:,0] = b0
    c_store[:,0] = c0
    v_store[:,0] = v0
    
    a_current = a0
    b_current = b0
    c_current = c0
    v_current = v0
    
    a_new = a0
    b_new = b0
    c_new = c0
    v_new = v0
    
    store_idx = 1
    for t_idx in range(1, number_of_timepoints):

        for cell_idx in range(number_of_cells):
        
            c_bar = calcium_boundary_condition(c_current, number_of_cells, cell_idx)

            H_c[cell_idx] = np.heaviside(c_current[cell_idx] - c_threshold,1)
            H_v_b[cell_idx] = np.heaviside(v_b_threshold - b_current[cell_idx], 1)

            b_new[cell_idx] = b_current[cell_idx] + dt * ((rho * H_c[cell_idx]) - (b_current[cell_idx] * (gamma_0 + (gamma * c_current[cell_idx]))))
            c_new[cell_idx] = c_current[cell_idx] + dt * ((k * a_current[cell_idx]) + (mu * np.power(1/dx,2) * (c_bar - c_current[cell_idx])) - (lambda_const * c_current[cell_idx]))
            v_new[cell_idx] = v_current[cell_idx] + dt * ((k_v * H_v_b[cell_idx]) - (v_current[cell_idx] * (lambda_const_v_0 + (lambda_const_v_b * b_current[cell_idx]))))

            H_c_b[cell_idx] = np.heaviside(c_b_threshold - b_new[cell_idx], 1)
            a_new[cell_idx] = max(a_current[cell_idx], H_c_b[cell_idx])
            
        if t_idx in store_t:
            a_store[:,store_idx] = a_new
            b_store[:,store_idx] = b_new
            c_store[:,store_idx] = c_new
            v_store[:,store_idx] = v_new
            store_idx = store_idx + 1
            
        a_current = a_new
        b_current = b_new
        c_current = c_new
        v_current = v_new
            
    return a_store, b_store, c_store, v_store
