import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_phase(data_path, save_path, list_amp):
    x, y = list_amp.split(sep=' ')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for _, __, files in os.walk(data_path):
        for file in files:
            df = pd.read_csv(data_path + f'/{file}')
            df = df.loc[df['time'] > 8]
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(df[x], df[y], 'k', lw=0.8)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.grid()
            plt.savefig(save_path+f'/{file[:-4]}.png')
            plt.close('all')
