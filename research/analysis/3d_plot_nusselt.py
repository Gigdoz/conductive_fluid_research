import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import os


def plot_surf(path_name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    df = pd.read_csv("./datasets/" + path_name)
    print(df)
    E = df.e.values
    V = df.v.values
    e = np.unique(E)
    v = np.unique(V)
    Nu = df.Nu.values
    Nu = Nu.reshape(len(e), len(v))
    V, E = np.meshgrid(v, e)
    surf = ax.plot_surface(V, E, Nu, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    ax.set_xlabel("e")
    ax.set_ylabel("v")
    ax.set_zlabel("Nu")
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.show()


import sys
plot_surf(sys.argv[1])