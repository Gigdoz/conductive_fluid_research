import numpy as np
import json
import csv
import os
import platform

os_name = platform.system()

from ctypes import *

n = ""
if os_name == "Windows":
    n = "odeslib.dll"
elif os_name == "Linux":
    n = "libodeslib.so"
else:
     print("Неизвестная ОС")
lib = CDLL(f"../odeslib/lib/{n}")


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

    E = []
    if not config["control_constants"]["series"]:
        e_start, e_stop, e_step = config["control_constants"]["e"]
        E = np.arange(e_start, e_stop, e_step)
        v_start, v_stop, v_step = config["control_constants"]["v"]
        V = np.arange(v_start, v_stop, v_step)
    else:
        E = config["control_constants"]["e"]
        V = config["control_constants"]["v"]

    t0 = config["algorithm_settings"]["t0"]
    t_end = config["algorithm_settings"]["t_end"]
    tol = config["algorithm_settings"]["tol"]
    h_init = config["algorithm_settings"]["h_init"]
    h_min = config["algorithm_settings"]["h_min"]
    h_max = config["algorithm_settings"]["h_max"]
    output_step = config["algorithm_settings"]["output_step"]

    consts_init = [0.0, 0.0] + initial_conditions
    seq = c_double * len(consts_init)
    consts_init = seq(*consts_init)

    for e in E:
        consts_init[0] = c_double(e)
        for v in V:
            name = name_dir + f'/e={e}; v={v}.csv'
            with open(name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(name_columns)  # Заголовки столбцов
            
            consts_init[1] = c_double(v)
            lib.solve_rkf45(name.encode('utf-8'), consts_init, c_double(t0),
                            c_double(t_end), c_double(tol), c_double(h_init),
                            c_double(h_min), c_double(h_max), c_double(output_step))


import sys
solution(sys.argv[1])