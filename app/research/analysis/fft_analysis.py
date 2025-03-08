import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import fft, fftfreq
import numpy as np
import os

def single_plot(dir_path, file, save_dir, mag, save_fft_data=None):
    df = pd.read_csv(dir_path + f'/{file}')
    dt = df.time[1] - df.time[0]
    # Примерной интервал сходимости алгоритма 4-6 ед.времени
    n = int(4.0 / dt)
    df = df[n:]
    N = len(df.time)
    n = int(1/(20*dt))
    Xf = 2.0/N * np.abs(fft(df[mag].values))[1:N//n]
    fr = fftfreq(N, dt)[1:N//n]

    if save_fft_data:
        df = pd.DataFrame(data={'amp' : Xf, 'freq' : fr}).sort_values(ascending=False, by='amp')
        df.to_csv(f'data/fft/{save_fft_data}/{file}', index=False)
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    _, stemlines, baseline = ax.stem(fr, Xf, linefmt ='black', markerfmt ='')
    plt.setp(stemlines, 'linewidth', 0.9)
    plt.setp(baseline, visible=False)
    ax.set_xlabel("v")
    ax.set_ylabel(f'{mag}')
    plt.savefig(save_dir+f'/{mag} {file[:-4]}.png')
    plt.close()

def plot_fft(dir_path, save_dir, mag, save_fft_data=True):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    dirs = dir_path.split('/')
    if save_fft_data:
        if not os.path.exists(f'data/fft/{dirs[-1]}'):
            os.makedirs(f'data/fft/{dirs[-1]}')
            
    for _, __, files in os.walk(dir_path):
        for file in files:
            single_plot(dir_path, file, save_dir, mag, dirs[-1])
