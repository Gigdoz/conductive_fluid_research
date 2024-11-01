from methods.odes import solve_rk4
import numpy as np
import pandas as pd
from math_functions import *
import json
import os


def solution(name_config):
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    name_solutions = ""
    if config["name_solutions"] == "":
        i = 1
        while True:
            if os.path.exists(f'daraset/{i}'):
                i += 1
            else:
                name_solutions = str(i)
                break
    else:
        name_solutions = config["name_solutions"]

    name_dir = 'datasets/' + name_solutions
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    name_columns = ['time']
    initial_conditions = []
    for name in config["initial_conditions"]:
        name_columns.append(name)
        initial_conditions.append(config["initial_conditions"][name])
    initial_conditions = np.array(initial_conditions)

    E = []
    if not config["control_constants"]["series"]:
        e_start, e_stop, e_step = config["control_constants"]["e"]
        E = np.arange(e_start, e_stop, e_step)
        v_start, v_stop, v_step = config["control_constants"]["v"]
        V = np.arange(v_start, v_stop, v_step)
    else:
        E = config["control_constants"]["e"]
        V = config["control_constants"]["v"]

    total_time = config["algorithm_settings"]["total_time"]
    max_step = config["algorithm_settings"]["max_step"]
    eps = config["algorithm_settings"]["eps"]
    auto_step = config["algorithm_settings"]["auto_step"]
    step_reduction = config["algorithm_settings"]["step_reduction"]

    for e in E:
        for v in V:
            solution = solve_rk4(([e, v], initial_conditions, sys_equations),
                                    total_time, max_step, eps, auto_step, step_reduction)
            
            name = name_dir + f'/e={e}; v={v}.csv'
            pd.DataFrame(data=solution, columns=name_columns).to_csv(name, index=False)


import sys
solution(sys.argv[1])