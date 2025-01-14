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
lib = CDLL(f"app/extensions/{n}")

def solution(name_config):
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    path_solutions = config["path_solutions"]

    if not os.path.exists(path_solutions):
        os.makedirs(path_solutions)

    E = config["control_constants"]["e"]
    V = config["control_constants"]["v"]

    t0 = config["algorithm_settings"]["t0"]
    t_end = config["algorithm_settings"]["t_end"]
    tol = config["algorithm_settings"]["tol"]
    h_init = config["algorithm_settings"]["h_init"]
    h_min = config["algorithm_settings"]["h_min"]
    h_max = config["algorithm_settings"]["h_max"]
    # continue_by_par = config["algorithm_settings"]["continue_by_par"]

    initial_conditions = []
    for name in config["initial_conditions"]:
        initial_conditions.append(config["initial_conditions"][name])

    seq = c_longdouble * len(initial_conditions)
    init = seq(*initial_conditions)

    name = path_solutions + f'/nusselt e={E[0]}-{E[1]}; v={V[0]}-{V[1]}.csv'

    seq = c_longdouble * len(E)
    E = seq(*E)
    V = seq(*V)
         
    name_columns = ['e', 'v', 'Nu']
    with open(name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(name_columns)

    lib.nusselt_number(name.encode('utf-8'), E, V, init, c_double(t0),
                    c_double(t_end), c_double(tol), c_double(h_init),
                    c_double(h_min), c_double(h_max))
            
