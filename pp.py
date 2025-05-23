import numpy as np
import scienceplots
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

from ssqueezepy import ssq_cwt

from system import SolveOptions, SolveSYS, system

plt.style.use(['science'])
plt.rcParams['axes.labelsize'] = 6  # Размер шрифта для всех осей
plt.rcParams['xtick.labelsize'] = 6  # Размер шрифта для меток по X
plt.rcParams['ytick.labelsize'] = 6  # Размер шрифта для меток по Y
plt.rcParams['axes.titlesize'] = 7  # Размер шрифта заголовка

def fft_fr(data, time):
    dt = time[1] - time[0]
    N = len(time)
    n = int(1/(20*dt))
    Xf = 2.0/N * np.abs(fft(data))[1:N//n]
    fr = fftfreq(N, dt)[1:N//n]
    return Xf, fr

def plots(e, v, signals=(True, False), furie=True, phase=True, wavelet=False):
    key, val = "X", 0

    subplots_list = []
    if signals[0] and not signals[1]:
        subplots_list.append(["signal", "signal"])
    elif signals[0] and signals[1]:
        subplots_list.append(["signal", "cutted_signal"])

    subsubplots = []
    if furie:
        subsubplots.append("magnitude")
    if phase:
        subsubplots.append("phase")
    if furie and not phase:
        subsubplots.append("magnitude")
    if not furie and phase:
        subsubplots.append("phase")
    if subsubplots != []:
        subplots_list.append(subsubplots)
    if wavelet:
        subplots_list.append(["wavelet", "wavelet"])
 
    t_0 = 0
    T_tran = 100
    t_end = T_tran + 200
    dt = 0.01
    time_plot = 100

    options = SolveOptions("", "", t_0, t_end, T_tran, dt, False, atol=1e-7, rtol=1e-4)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)
    Xf, fr = fft_fr(data[val], time)

    fig = plt.figure(figsize=(16, 9), dpi=300, layout='constrained')
    axs = fig.subplot_mosaic(subplots_list)

    list_title = ['a','b','c','d','e']
    if len(subplots_list[0]) == 1 and len(subplots_list) == 1:
        list_title = ['']
    n = 0

    y = -0.15
    c = 0
    if len(subplots_list) == 2:
        y = -0.3
        c = 0.1
    elif len(subplots_list) == 3:
        y = -0.58

    # plot time signal:
    if signals[0]:
        axs["signal"].plot(time[:int(time_plot/dt)], data[0, :int(time_plot/dt)], lw=0.3, color='C0')
        axs["signal"].set_xlabel("t")
        axs["signal"].set_xlim(T_tran, T_tran+time_plot)
        axs["signal"].set_ylabel("X")
        axs["signal"].set_title(f'$\t{list_title[n]}$', y=y)
        n +=1
    
    if signals[1]:
        axs["cutted_signal"].set_title(f'$\t{list_title[n]}$', y=y)
        n +=1
        axs["cutted_signal"].plot(time[:int(time_plot/dt)], data[0, :int(time_plot/dt)], lw=0.3, color='C0')
        axs["cutted_signal"].set_xlabel("t")
        axs["cutted_signal"].set_ylabel("X")

    # plot spectrum:
    if furie:
        axs["magnitude"].set_title(f'$\t{list_title[n]}$', x=0.94, y=0.7+c)
        n +=1
        _, stemlines, baseline = axs["magnitude"].stem(fr, Xf, linefmt ='blue', markerfmt ='')
        plt.setp(stemlines, 'linewidth', 0.5)
        plt.setp(baseline, visible=False)
        axs["magnitude"].set_xlabel("v")
        axs["magnitude"].set_ylabel(f'{key}')
        axs["magnitude"].set_xlim(0, 20)
        axs["magnitude"].set_ylim(-1)


    # plot phase
    if phase:
        axs["phase"].set_title(f'$\t{list_title[n]}$', x=0.94, y=0.7+c)
        n +=1
        axs["phase"].plot(data[0], data[3], '.', ms=0.1, color='black')
        axs["phase"].set_xlabel("X")
        axs["phase"].set_ylabel('V')

    # plot wavelet
    if wavelet:
        Tx, Wx, ssq_freqs, _ = ssq_cwt(data[0], ssq_freqs='linear', fs=1/dt, maprange='energy', wavelet='bump', nv=128)

        axs["wavelet"].set_title(f'$\t{list_title[n]}$', y=y)
        axs["wavelet"].imshow(np.log10(np.abs(Tx)+1), extent=[T_tran, t_end, ssq_freqs[-1], ssq_freqs[0]],
            cmap='Greys', aspect='auto')
        axs["wavelet"].set_ylim(0, 20)
        axs["wavelet"].set_xlim(T_tran+10, T_tran+time_plot)
        axs["wavelet"].set_xlabel("t")
        axs["wavelet"].set_ylabel('v')


plots(160, 4.0, signals=(True, False), furie=True, phase=True, wavelet=False)
plt.show()