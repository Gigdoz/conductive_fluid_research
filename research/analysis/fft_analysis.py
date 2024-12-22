import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import fft, fftfreq
import numpy as np
import os

def plot_fft(name_dir, mag):
    path_dir = f'./datasets/{name_dir}'

    name_dir = f'./image/fft/{name_dir}'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    for _, __, files in os.walk(path_dir):
        for file in files:
            df = pd.read_csv(path_dir + f'/{file}')
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
            ax.grid()
            plt.savefig(name_dir+f'/{mag} {file[:-4]}.png')
            plt.close()

import sys
plot_fft(sys.argv[1], sys.argv[2])