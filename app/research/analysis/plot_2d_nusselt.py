import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def plot(path_file, save_path):
    fig = plt.figure()
    ax = fig.add_subplot()

    df = pd.read_csv(path_file)
    df_p = pd.pivot_table(data=df, index='v',columns='e', values='Nu')
    e, v = np.meshgrid(df_p.index.values, df_p.columns.values)
    Nu = df_p.values.T
    pc = ax.pcolormesh(e, v, Nu, shading='nearest')

    ax.set_xlabel("v")
    ax.set_ylabel("e")

    c = fig.colorbar(pc, shrink=0.5, aspect=10)
    c.set_label("Nu")

    list_path = save_path.split(sep='/')
    path_dir = list_path[0]
    for d in list_path[1:-1]:
        path_dir += '/' + d
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    plt.savefig(save_path)
    plt.close()
