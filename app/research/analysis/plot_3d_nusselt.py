import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def plot_surf(path_file):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    df = pd.read_csv(path_file)
    E = df.e.values
    V = df.v.values
    e = np.unique(E)
    v = np.unique(V)
    Nu = df.Nu.values
    Nu = Nu.reshape(len(e), len(v))
    V, E = np.meshgrid(v, e)
    surf = ax.plot_trisurf(df.v, df.e, df.Nu, cmap=cm.inferno, linewidth=0.5, antialiased=False)

    ax.set_xlabel("v")
    ax.set_ylabel("e")
    ax.set_zlabel("Nu")

    fig.colorbar(surf, shrink=0.5, aspect=10)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.tight_layout()

    plt.show()
