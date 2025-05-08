import numpy as np
from math import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.stats import gaussian_kde
from scipy.fft import fft, fftfreq
from scipy.integrate import solve_ivp

from findpeaks import findpeaks

from system import SolveOptions, SolveSYS, system


def single_plot(data, time):
    dt = time[1] - time[0]
    N = len(time)
    n = int(1/(35*dt))
    Xf = 2.0/N * np.abs(fft(data))[1:N//n]
    fr = fftfreq(N, dt)[1:N//n]
    return Xf, fr


def solve_logic_fun(data, time):
    T = time[-1] - time[0]
    if abs(2 / T * data[5][-1]) < 1e-2:
        return [0]

    # r = np.arctan2(data[0], data[1])
    r = np.linalg.norm(data[[0,4]], axis=0)
    # r = data[0]
    Xf, fr = single_plot(r, time)
    r_peaks, _ = find_peaks(Xf, prominence=0.01, height=Xf.max()*0.01)
    n_peaks = len(r_peaks)
    return [n_peaks]


def num_peaks_ft(path_file, E, V): 
    name_columns = ["e", "v", "peaks"]
    options = SolveOptions(path_file, name_columns, 0, 100, 30, 0.001, False)
    solve_sys = SolveSYS(options, solve_logic_fun)
    solve_sys.solve_mp(E, V, 6)
            

def plot(e, v, i):
    t_end = 120
    t_tr = 50
    T_max = t_end - t_tr
    options = SolveOptions("", "", 0, t_end, t_tr, 0.001, False)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)

    # a = np.linalg.norm(data[[0,3]], axis=0)
    # r = np.arctan2(data[0], data[3])

    a = np.arctan2(data[0], data[4])
    r = np.linalg.norm(data[[0,4]], axis=0)

    r = data[0]
    Xf, fr = single_plot(r, time)

    # fp = findpeaks(lookahead=1)
    # results = fp.fit(Xf)
    # peaks = results['df'].loc[results['df'].peak == True].x

    peaks, _ = find_peaks(Xf, prominence=0.01, height=Xf.max()*0.01)

    plt.subplot(2, 6, 2*i-1)
    n_peaks = len(peaks)
    if abs(2 / T_max * data[5][-1]) < 1e-3:
        n_peaks = 0
    _, stemlines, baseline = plt.stem(fr, Xf, linefmt ='black', markerfmt ='', label=f"e={e}; v={v}\npeaks={n_peaks}")
    plt.plot(fr[peaks], Xf[peaks], "x")
    plt.setp(stemlines, 'linewidth', 0.9)
    plt.setp(baseline, visible=False)
    plt.legend(fontsize='x-small', loc='upper right')
    plt.xlabel("v")
    plt.ylabel("norm(X,V)")

    plt.subplot(2, 6, 2*i)
    plt.plot(data[0], data[3], lw=0.3)
    plt.xlabel("arctan(X,V)")
    plt.ylabel("norm(X,V)")

# e = 160
plt.figure(figsize=(14, 6), layout="constrained")
plot(160, 3.09, 1)
plot(160, 4.1, 2)
plot(160, 5.4, 3)
plot(110, 4.1, 4)
plot(90, 4.1, 5)
plot(160, 6.5, 6)
plt.show()

# if __name__ == '__main__':
#     num_peaks_ft("test_1.csv", np.arange(60, 300, 0.5), np.arange(3.0, 7.5, 0.01))
