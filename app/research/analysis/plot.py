import matplotlib.pyplot as plt
import pandas as pd
import os


def plot(data_path, save_path, amp):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for _, __, files in os.walk(data_path):
        for file in files:
            df = pd.read_csv(data_path + f'/{file}')
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(df['time'], df[amp], 'k', lw=0.8)
            ax.set_xlabel('time')
            ax.set_ylabel(amp)
            ax.grid()
            plt.savefig(save_path+f'/{file[:-4]}.png')
            plt.close()
