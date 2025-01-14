import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import fft, fftfreq
import numpy as np
import os

def plot_fft(data_path, save_path, mag):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for _, __, files in os.walk(data_path):
        for file in files:
            df = pd.read_csv(data_path + f'/{file}')
            dt = df.time[1] - df.time[0]
            n = int(2.0 / dt)
            df = df[n:]

            N = len(df.time)
            n = int(1/(20*dt))
            Xf = 2.0/N * np.abs(fft(df[mag].values))[1:N//n]
            fr = fftfreq(N, dt)[1:N//n]

            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            _, stemlines, baseline = ax.stem(fr, Xf, linefmt ='black', markerfmt ='')
            plt.setp(stemlines, 'linewidth', 0.9)
            plt.setp(baseline, visible=False)
            ax.set_xlabel("v")
            ax.set_ylabel(f'{mag}')
            plt.savefig(save_path+f'/{mag} {file[:-4]}.png')
            plt.close()
