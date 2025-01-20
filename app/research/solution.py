from math import *
import numpy as np
import json
import csv
import os
from scipy.integrate import solve_ivp

Pr = 100.0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def sys(t, state, e, v):
    X, Y, Z, V, W, Nu_y = state

    cos_2 = (cos(2.0*pi*v*t))**2
    dX = Pr*(-X+e*W*cos_2)
    dY = -Y+X+X*Z
    dZ = -b*Z-X*Y
    dV = -Pr*(d*V+e*Y*cos_2/d)
    dW = -d*W+V
    dNu = Z
    return [dX, dY, dZ, dV, dW, dNu]


def solution(name_config):
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    path_solutions = config["path_solutions"]
    if not os.path.exists(path_solutions):
        os.makedirs(path_solutions)

    name_columns = ['time']
    initial_conditions = []
    for name in config["initial_conditions"]:
        name_columns.append(name)
        initial_conditions.append(config["initial_conditions"][name])

    E = []
    if not config["control_constants"]["series"]:
        e_start, e_stop, e_step = config["control_constants"]["e"]
        E = np.arange(e_start, e_stop+e_step, e_step)
        v_start, v_stop, v_step = config["control_constants"]["v"]
        V = np.arange(v_start, v_stop+v_step, v_step)
    else:
        E = config["control_constants"]["e"]
        V = config["control_constants"]["v"]
        if isinstance(E, float):
            E = [E]
        if isinstance(V, float):
            V = [V]

    t0 = config["algorithm_settings"]["t0"]
    t_end = config["algorithm_settings"]["t_end"]
    atol = config["algorithm_settings"]["atol"]
    rtol = config["algorithm_settings"]["rtol"]
    continue_by_par = config["algorithm_settings"]["continue_by_par"]
    output_step = config["algorithm_settings"]["output_step"]

    for e in E:
        for v in V:
            name = path_solutions + f'/e={round(e, 3)}; v={round(v, 3)}.csv'
            def f(t, state):
                const = [e, v]
                return sys(const, t, state)
            
            with open(name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(name_columns)
                if output_step == 0:
                    sol = solve_ivp(sys, [t0, t_end], initial_conditions,
                                    args=(e,v), rtol=rtol, atol=atol)
                else:
                    x_pts = np.arange(t0, t_end + output_step, output_step)
                    sol = solve_ivp(sys, (t0, t_end), initial_conditions, t_eval=x_pts,
                                    args=(e,v), rtol=rtol, atol=atol)
                    
                for i in range(len(sol.t)):
                    writer.writerow([sol.t[i], sol.y[0][i],sol.y[1][i],
                            sol.y[2][i],sol.y[3][i],sol.y[4][i], sol.y[5][i]])
                        
                if continue_by_par:
                    initial_conditions = [sol.y[0][-1],sol.y[1][-1],
                                 sol.y[2][-1],sol.y[3][-1],sol.y[4][-1], 0.0]