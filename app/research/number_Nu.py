import json
import csv
import numpy as np
import os
from math import *
from scipy.integrate import solve_ivp

Pr = 100.0
r = .0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def sys(const, t, state):
    e, v = const
    X, Y, Z, V, W, Nu_y = state
    dX = Pr*(-X+e*W*(cos(2.0*pi*v*t))**2)
    dY = -Y+X+X*Z
    dZ = -b*Z-X*Y
    dV = Pr*(-d*V+(-e*Y*(cos(2.0*pi*v*t))**2)/d)
    dW = -d*W+V
    dNu = Z
    return [dX, dY, dZ, dV, dW, dNu]


def solution(name_config):
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    path_solutions = config["path_solutions"]

    if not os.path.exists(path_solutions):
        os.makedirs(path_solutions)

    e_start, e_stop, e_step = config["control_constants"]["e"]
    E = np.arange(e_start, e_stop+e_step, e_step)
    v_start, v_stop, v_step = config["control_constants"]["v"]
    V = np.arange(v_start, v_stop+v_step, v_step)

    t0 = config["algorithm_settings"]["t0"]
    t_end = config["algorithm_settings"]["t_end"]
    atol = config["algorithm_settings"]["atol"]
    rtol = config["algorithm_settings"]["rtol"]
    continue_by_par = config["algorithm_settings"]["continue_by_par"]

    initial_conditions = []
    for name in config["initial_conditions"]:
        initial_conditions.append(config["initial_conditions"][name])

    name = path_solutions + f'/nusselt e={E[0]}-{E[-1]}; v={V[0]}-{V[-1]}.csv'
         
    name_columns = ['e', 'v', 'Nu']
    with open(name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(name_columns)
        for e in E:
            for v in V:
                def f(t, state):
                    const = [e, v]
                    return sys(const, t, state)
                
                sol = solve_ivp(f, (t0, t_end), initial_conditions, t_eval=[t0, t_end],
                                rtol=rtol, atol=atol)
                Nu = 1 - 2 / (t_end - t0) * sol.y[5][-1]
                writer.writerow([e, v, Nu])
                if continue_by_par:
                    initial_conditions = [sol.y[0][-1],sol.y[1][-1],
                                 sol.y[2][-1],sol.y[3][-1],sol.y[4][-1], 0.0]
            
