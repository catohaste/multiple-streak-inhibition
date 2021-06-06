import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy


def calcium_periodic_boundary(c, number_of_cells, cell_idx, t_idx):
    
    cell_idx_plus_one = (cell_idx + 1) % number_of_cells
    cell_idx_minus_one = (cell_idx - 1) % number_of_cells
    
    c_bar = 0.5 * (c[cell_idx_plus_one, t_idx] + c[cell_idx_minus_one, t_idx])
    
    return c_bar
    
def calcium_no_flux_boundary(c, number_of_cells, cell_idx, t_idx):
    
    if cell_idx in range(1, number_of_cells - 1):
        c_bar = (c[cell_idx - 1, t_idx] + c[cell_idx + 1, t_idx]) / 2
    elif cell_idx == 0:
        c_bar = (c[0, t_idx] + c[1, t_idx]) / 2
    elif cell_idx == (number_of_cells - 1):
        c_bar = (c[number_of_cells - 2, t_idx] + c[number_of_cells - 1, t_idx]) / 2
    else:
        print('whoops')
        
    # print(c_bar.shape)
        
    # if len(c_bar) is not 1:
    #     print(cell_idx)
       
    return c_bar
    
def solve_ivp_odes(number_of_cells, number_of_timepoints, dt, dx, a0, b0, c0, v0, calcium_boundary_condition, params):
    
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
    lambda_const_v = params["lambda_const_v"]
    
    # Preallocate
    a = np.ndarray((number_of_cells, number_of_timepoints), dtype=float)
    b = np.ndarray((number_of_cells, number_of_timepoints), dtype=float)
    c = np.ndarray((number_of_cells, number_of_timepoints), dtype=float)
    v = np.ndarray((number_of_cells, number_of_timepoints), dtype=float)

    H_c = np.ndarray((number_of_cells, number_of_timepoints), dtype=int)
    H_c_b = np.ndarray((number_of_cells, number_of_timepoints), dtype=int)
    H_v_b = np.ndarray((number_of_cells, number_of_timepoints), dtype=int)

    # Initialize
    a[:,0] = a0
    b[:,0] = b0
    c[:,0] = c0
    v[:,0] = v0

    for t_idx in range(1, number_of_timepoints):
        
        if t_idx % 100000 == 0:
            print("At time: " + str(t_idx))

        for cell_idx in range(number_of_cells):
        
            c_bar = calcium_boundary_condition(c, number_of_cells, cell_idx, t_idx - 1)

            H_c[cell_idx, t_idx] = np.heaviside(c[cell_idx, t_idx - 1] - c_threshold,1)
            H_v_b[cell_idx, t_idx] = np.heaviside(v_b_threshold - b[cell_idx, t_idx - 1], 1)

            b[cell_idx, t_idx] = b[cell_idx, t_idx - 1] + dt * ((rho * H_c[cell_idx, t_idx]) - (b[cell_idx, t_idx - 1] * (gamma_0 + (gamma * c[cell_idx, t_idx - 1]))))
            c[cell_idx, t_idx] = c[cell_idx, t_idx - 1] + dt * ((k * a[cell_idx, t_idx - 1]) + (mu * np.power(1/dx,2) * (c_bar - c[cell_idx, t_idx - 1])) - (lambda_const * c[cell_idx, t_idx - 1]))
            v[cell_idx, t_idx] = v[cell_idx, t_idx - 1] + dt * ((k_v * H_v_b[cell_idx, t_idx]) - (lambda_const_v * v[cell_idx, t_idx - 1]))

            H_c_b[cell_idx, t_idx] = np.heaviside(c_b_threshold - b[cell_idx, t_idx], 1)
            a[cell_idx, t_idx] = max(a[cell_idx, t_idx - 1], H_c_b[cell_idx, t_idx])
            
    return a, b, c, v
