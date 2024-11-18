import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import pandas as pd
import os


def plot_surf(path_name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    df = pd.read_csv("./datasets/" + path_name)
    df['t'] = 1.0 / df['v']
    surf = ax.plot_trisurf(df.t, df.e, df.Nu, cmap=cm.inferno, linewidth=0.5, antialiased=False)

    ax.set_xlabel("t")
    ax.set_ylabel("e")
    ax.set_zlabel("Nu")

    fig.colorbar(surf, shrink=0.5, aspect=10)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.tight_layout()

    name_dir = f'image/Nusselt'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    name = name_dir + '/nusselt.png'
    i = 1
    while(os.path.exists(name)):
         name = name_dir + f'/nusselt_{i}.png'
         i += 1
    plt.savefig(name)
    plt.show()


import sys
plot_surf(sys.argv[1])