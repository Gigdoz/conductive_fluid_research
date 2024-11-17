import numpy as np
import json
import os
import csv

from ctypes import *
lib = CDLL("./lib/odeslib.dll")

import matplotlib.pyplot as plt
from matplotlib import cm


def plot_surf(res):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    E = res[:, 0]
    V = res[:, 1]
    e = np.unique(E)
    v = np.unique(V)
    Nu = res[:, 2].reshape(len(e), len(v))
    V, E = np.meshgrid(v, e)
    surf = ax.plot_surface(V, E, Nu, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    ax.set_xlabel("e")
    ax.set_ylabel("v")
    ax.set_zlabel("Nu")
    fig.colorbar(surf, shrink=0.5, aspect=10)

    name_dir = f'image/Nusselt'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)
    plt.savefig(name_dir+'/Nu_V_E.png')
    plt.show()


def solution(name_config):
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    name_solutions = ""
    if config["name_solutions"] == "":
        i = 1
        while True:
            if os.path.exists(f'datasets/{i}'):
                i += 1
            else:
                name_solutions = str(i)
                break
    else:
        name_solutions = config["name_solutions"]

    name_dir = 'datasets/' + name_solutions
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    E = config["control_constants"]["e"]
    V = config["control_constants"]["v"]

    t0 = config["algorithm_settings"]["t0"]
    t_end = config["algorithm_settings"]["t_end"]
    tol = config["algorithm_settings"]["tol"]
    h_init = config["algorithm_settings"]["h_init"]
    h_min = config["algorithm_settings"]["h_min"]
    h_max = config["algorithm_settings"]["h_max"]

    initial_conditions = []
    for name in config["initial_conditions"]:
        initial_conditions.append(config["initial_conditions"][name])

    seq = c_double * len(initial_conditions)
    init = seq(*initial_conditions)

    seq = c_double * len(E)
    E = seq(*E)
    V = seq(*V)

    name = name_dir + '/nusselt.csv'
    name_columns = ['e', 'v', 'Nu']
    with open(name, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(name_columns)  # Заголовки столбцов

    lib.nusselt_number(name.encode('utf-8'), E, V, init, c_double(t0),
                    c_double(t_end), c_double(tol), c_double(h_init),
                    c_double(h_min), c_double(h_max))
            

import sys
solution(sys.argv[1])