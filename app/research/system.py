from math import *
import numpy as np
import csv
from scipy.integrate import solve_ivp
import multiprocessing as mp

Pr = 100.0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def system(t, state, e, v):
    X, Y, Z, V, W, Nu = state

    cos_2 = (cos(2.0*pi*v*t))**2
    dX = Pr*(-X+e*W*cos_2)
    dY = -Y+X+X*Z
    dZ = -b*Z-X*Y
    dV = -Pr*(d*V+e*Y*cos_2/d)
    dW = -d*W+V
    dNu = Z
    return [dX, dY, dZ, dV, dW, dNu]


class SolveOptions():
     def __init__(self, path_file, name_columns, t0, t_end, T_transient, dt, final_sol=True, atol=1e-6, rtol=1e-3, offset=0.0):
        self.t0 = t0 + offset
        self.t_end = t_end + offset
        self.dt = dt
        self.T_transient = T_transient
        self.path_file = path_file
        self.name_columns = name_columns

        self.times = None
        if dt is not None:
            self.times = np.array([t0, t_end]) + offset
            if not final_sol:
                self.times = np.arange(t0, t_end, dt) + offset

        self.atol = atol
        self.rtol = rtol
        self.state0 = [1e-5, 5e-6, 0, 12e-6, 0, 41e-6]

class SolveOptionsConfig():
    pass

class SolveSYS():
    def __init__(self, options, solve_logic_fun):
        self.solve_logic_fun = solve_logic_fun
        self.options = options
        self.n_transient = int(self.options.T_transient/self.options.dt)
        self.lock = mp.Lock()

        if self.options.path_file is not None:
            with open(self.options.path_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.options.name_columns)

    def solve(self, state0, e, v):
        sol = solve_ivp(system, (self.options.t0, self.options.t_end), state0, args=(e, v),
                        t_eval=self.options.times, rtol=self.options.rtol, atol=self.options.atol)
        state0 = [sol.y[0][-1], sol.y[1][-1], sol.y[2][-1], sol.y[3][-1], sol.y[4][-1], 0]
        data = sol.y[:, self.n_transient:]
        time = sol.t[self.n_transient:]
        return time, data

    def solves(self, E, V):
        state0 = self.options.state0
        for v in V:
            for e in E:
                time, data = self.solve(state0, e, v)
                vals = self.solve_logic_fun(data, time)
                with self.lock:
                    with open(self.options.path_file, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        for a in vals:
                            writer.writerow([e, v, a])
    def solve_mp(self, E, V, n_processes=4):          
        processes = []
        parts = np.array_split(V, n_processes)
        for part in parts:
            p = mp.Process(target=self.solves, args=(E, part))
            p.start()
            processes.append(p)
        [p.join() for p in processes]