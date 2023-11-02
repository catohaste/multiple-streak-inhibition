params = {
    "c_threshold": 0.01,        # calcium act. above threshold -> BMP production (alpha in paper)
    "c_b_threshold": 1,         # BMP below threshold -> streak (beta_C in paper)
    'v_b_threshold': 1.22,      # BMP below threshold -> Vg1 production (beta_V in paper)
    "rho": 1,                   # rate of BMP production (k_B in paper)
    "gamma_0": 0.3,             # BMP decay (base)
    "gamma_c": 0.1,             # BMP decay (calcium act. dependent)
    "gamma_v": 0.1,             # BMP decay (Vg1 dependent)
    "k": 500,                   # calcium act. production rate, when streak on (k_C in paper)
    "k_v": 5,                   # Vg1 production rate
    "mu": 50,                   # diffusion rate (D in paper)
    "lambda_const": 5,          # calcium act. decay (lambda in paper)
    "lambda_const_v_0": 4,      # Vg1 decay (mu in paper)
    "lambda_const_v_b": 0       # Vg1 decay dependent on BMP level (not used in paper, set to 0)
}

# params_save_2022_04_18 = {
#     "c_threshold": 0.01,
#     "c_b_threshold": 1,
#     'v_b_threshold': 1.22,
#     "rho": 1,
#     "gamma_0": 0.3,
#     "gamma_c": 0.1,
#     "gamma_v": 0.1,
#     "k": 500,
#     "k_v": 5,
#     "mu": 50,
#     "lambda_const": 5,
#     "lambda_const_v_0": 4,
#     "lambda_const_v_b": 0
# }

# params_save = {
#     "c_threshold": 0.01,
#     "c_b_threshold": 1,
#     'v_b_threshold': 1.35,
#     "rho": 1,
#     "gamma_0": 0.3,
#     "gamma_c": 0.1,
#     "gamma_v": 0,
#     "k": 500,
#     "k_v": 5,
#     "mu": 50,
#     "lambda_const": 5,
#     "lambda_const_v_0": 4,
#     "lambda_const_v_b": 0
# }

karen_params = {
    "number_of_cells": 100,
    "c_threshold": 0.01,
    "c_b_threshold": 1,
    'v_b_threshold': 1.5,
    "rho": 1,
    "gamma_0": 0.1,
    "gamma_c": 0.1,
    "gamma_v": 0,
    "k": 500,
    "k_v": 5,
    "mu": 50,
    "lambda_const": 2,
    "lambda_const_v_0": 2,
    "lambda_const_v_b": 0
}

# params_unknown = {
#     "c_threshold": 0.01,
#     "c_b_threshold": 1,
#     'v_b_threshold': 1.22,
#     "rho": 1,
#     "gamma_0": 0.3,
#     "gamma_c": 0.1,
#     "gamma_v": 0.1,
#     "k": 100, # calcium production
#     "k_v": 5,
#     "mu": 4, # diffusion constant D
#     "lambda_const": 2, # calcium decay
#     "lambda_const_v_0": 4,
#     "lambda_const_v_b": 0
# }