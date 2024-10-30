from methods.odes import solve_rk4
import numpy as np
import pandas as pd
from math_functions import *
import json
import os


def solution(path_config):
    with open(path_config) as f:
        config = json.load(f)

    name_columns = ['time']
    initial_conditions = []
    for name in config["initial_conditions"]:
        name_columns.append(name)
        initial_conditions.append(config["initial_conditions"][name])
    initial_conditions = np.array(initial_conditions)

    e_start, e_stop, e_step = config["control_constants"]["e"]
    v_start, v_stop, v_step = config["control_constants"]["v"]

    total_time = config["algorithm_settings"]["total_time"]
    max_step = config["algorithm_settings"]["max_step"]
    eps = config["algorithm_settings"]["eps"]
    auto_step = config["algorithm_settings"]["auto_step"]
    step_reduction = config["algorithm_settings"]["step_reduction"]

    name_solutions = ""
    if config["name_solutions"] == "None":
        i = 1
        while True:
            if os.path.exists(f'daraset/1.csv'):
                i += 1
            else:
                name_solutions = str(i)
                break
    else:
        name_solutions = config["name_solutions"]

    name_dir = 'datasets/' + name_solutions
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    E = []
    if e_step == 0.0:
        E.append(e_start)
    else:
        E = np.arange(e_start, e_stop, e_step)

    V = []
    if v_step == 0.0:
        V.append(v_start)
    else:
        V = np.arange(v_start, v_stop, v_step)

    for e in E:
        for v in V:
            solution = solve_rk4(([e, v], initial_conditions, sys_equations),
                                    total_time, max_step, eps, auto_step, step_reduction)
            
            name = name_dir + f'/e={e}; v={v}.csv'
            pd.DataFrame(data=solution, columns=name_columns).to_csv(name, index=False)


import sys
solution(sys.argv[1])