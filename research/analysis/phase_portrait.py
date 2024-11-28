import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_phase(name_dir, list_amp):
    x, y, z = list_amp.split(sep=' ')
    path_dir = f'./datasets/{name_dir}'

    name_dir = f'./image/phase/{name_dir}'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    for _, __, files in os.walk(path_dir):
        for file in files:
            df = pd.read_csv(path_dir + f'/{file}')
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            ax.plot(df[x], df[y], df[z], 'k', lw=0.8)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_zlabel(z)
            ax.grid()
            plt.savefig(name_dir+f'/{file[:-4]}.png')


import sys
plot_phase(sys.argv[1], sys.argv[2])
