import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def plot_surf(path_name):
    fig = plt.figure()
    ax = fig.add_subplot()

    df = pd.read_csv("./datasets/" + path_name)
    df['t'] = 1.0 / df['v']
    df_p = pd.pivot_table(data=df,index='t',columns='e', values='Nu')
    e, t = np.meshgrid(df_p.index.values, df_p.columns.values)
    Nu = df_p.values.T
    pc = ax.pcolormesh(e, t, Nu, shading='nearest')

    ax.set_xlabel("t")
    ax.set_ylabel("e")

    c = fig.colorbar(pc, shrink=0.5, aspect=10)
    c.set_label("Nu")

    name_dir = f'image/nusselt'
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