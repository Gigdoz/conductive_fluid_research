import matplotlib.pyplot as plt
import pandas as pd
import os


def plot(name_dir, amp):
    path_dir = f'./datasets/{name_dir}'

    name_dir = f'./image/time_series/{name_dir}'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    for _, __, files in os.walk(path_dir):
        for file in files:
            df = pd.read_csv(path_dir + f'/{file}')
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(df['time'], df[amp], 'k', lw=0.8)
            ax.set_xlabel('time')
            ax.set_ylabel(amp)
            ax.grid()
            plt.savefig(name_dir+f'/{file[:-4]}.png')
            plt.close()


import sys
plot_phase(sys.argv[1], sys.argv[2])