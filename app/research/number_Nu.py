import json
import csv
import numpy as np
import os
from math import *
from scipy.integrate import solve_ivp
import multiprocessing
import time

Pr = 100.0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def sys(t, state, e, v):
    X, Y, Z, V, W, _ = state

    cos_2 = (cos(2.0*pi*v*t))**2
    dX = Pr*(-X+e*W*cos_2)
    dY = -Y+X+X*Z
    dZ = -b*Z-X*Y
    dV = -Pr*(d*V+e*Y*cos_2/d)
    dW = -d*W+V
    dNu = Z
    return [dX, dY, dZ, dV, dW, dNu]

class SolveOptions():
     def __init__(self, config):
        self.t0 = config["algorithm_settings"]["t0"]
        self.t_end = config["algorithm_settings"]["t_end"]
        self.atol = config["algorithm_settings"]["atol"]
        self.rtol = config["algorithm_settings"]["rtol"]

        self.initial_conditions = []
        for name in config["initial_conditions"]:
            self.initial_conditions.append(config["initial_conditions"][name])

class SolveSYS():
    def __init__(self, solve_options):
        self.solve_options = solve_options

    def update(self, v, E, queue):
        for e in E:
            sol = solve_ivp(sys, (self.solve_options.t0, self.solve_options.t_end),
                            self.solve_options.initial_conditions,
                            t_eval=[self.solve_options.t0, self.solve_options.t_end], args=(e, v),
                            rtol=self.solve_options.rtol, atol=self.solve_options.atol)
            Nu = 1 - 2 / (self.solve_options.t_end - self.solve_options.t0) * sol.y[5][-1]

            queue.put([e, v, Nu])
            self.solve_options.initial_conditions = [sol.y[0][-1],sol.y[1][-1],
                                                    sol.y[2][-1],sol.y[3][-1],sol.y[4][-1], 0.0]

def solution(name_config):
    config = None
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    path_solutions = config["path_solutions"]
    if not os.path.exists(path_solutions):
        os.makedirs(path_solutions)

    e_start, e_stop, e_step = config["control_constants"]["e"]
    E = np.arange(e_start, e_stop+e_step, e_step)
    v_start, v_stop, v_step = config["control_constants"]["v"]
    V = np.arange(v_start, v_stop+v_step, v_step)

    solve_sys = SolveSYS(SolveOptions(config))

    manager = multiprocessing.Manager()
    queue = manager.Queue()

    start_time = time.time()

    processes = []
    for v in V:
        p = multiprocessing.Process(target=solve_sys.update, args=(v, E, queue))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()


    name = path_solutions + f'/nusselt e={E[0]}-{E[-1]}; v={V[0]}-{round(V[-1], 3)}.csv'
    name_columns = ['e', 'v', 'Nu']
    with open(name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(name_columns)
        while not queue.empty():
            result = queue.get()
            writer.writerow(result)

    mp_time = time.time() - start_time
    print(f"Multiprocessing execution time: {mp_time:.4f} seconds")