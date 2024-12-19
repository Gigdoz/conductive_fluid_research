import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def plot(name_dir, name_file):
    fig = plt.figure()
    ax = fig.add_subplot()

    df = pd.read_csv(f"./datasets/{name_dir}/{name_file}")
    df_p = pd.pivot_table(data=df,index='v',columns='e', values='Nu')
    e, v = np.meshgrid(df_p.index.values, df_p.columns.values)
    Nu = df_p.values.T
    pc = ax.pcolormesh(e, v, Nu, shading='nearest')

    ax.set_xlabel("v")
    ax.set_ylabel("e")

    c = fig.colorbar(pc, shrink=0.5, aspect=10)
    c.set_label("Nu")

    name_dir = f'./image/nusselt'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    name = name_dir + f'/{name_file}.png'
    plt.savefig(name)


import sys
plot(sys.argv[1], sys.argv[2])