import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy import signal

from system import SolveOptions, SolveSYS, system


counter_plot = 1

def phase_plotXT(X, e, v, offset):
    options1 = SolveOptions("", "", 0, 120, 50, 0.01, False)
    solve_sys1 = SolveSYS(options1, None)
    state = [2, 0, 0, 0, 0, 0]
    _, data1 = solve_sys1.solve(state, e, v)

    options2 = SolveOptions("", "", 0, 120, 50, 0.01, False, offset=offset)
    solve_sys2 = SolveSYS(options2, None)
    _, data2 = solve_sys2.solve(state, e, v)

    plt.subplot(1, 4, counter_plot)
    plt.plot(data2[X], data1[X], '.', ms=0.3, color='black')
    return 1

def phase_plotXX(X, e, v):
    options = SolveOptions("", "", 0, 120, 50, 0.001, False)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)

    dX = []
    for i in range(len(time)):
        dd = system(time[i], data[:, i], e, v)
        dX.append(dd[X])

    plt.subplot(1, 5, counter_plot)
    plt.plot(data[X], dX, '.', ms=0.3, color='black')
    return 1

def phase_plot2d(amps, e, v):
    options = SolveOptions("", "", 0, 120, 50, 0.001, False)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)

    plt.subplot(1, 4, counter_plot)
    x, y = amps
    plt.plot(data[x], data[y], '.', ms=0.5, color='black')
    return 1

def phase_plot3d(amps, e, v):
    options = SolveOptions("", "", 0, 120, 50, 0.001, False)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)

    plt.subplot(1, 4, counter_plot, projection='3d')
    x, y, z = amps
    plt.plot(data[x], data[y], data[z], lw=0.3)
    return 1


def plot(x, e, v):
    options = SolveOptions("", "", 0, 200, 5, 0.001, False)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)

    plt.subplot(4, 1, counter_plot)
    plt.plot(time, data[x], lw=0.3)
    return 1


def fft_fr(data, time):
    dt = time[1] - time[0]
    N = len(time)
    n = int(1/(20*dt))
    Xf = 2.0/N * np.abs(fft(data))[1:N//n]
    fr = fftfreq(N, dt)[1:N//n]
    return Xf, fr


def plot_fft(X, e, v):
    key, val = X.popitem()
    options = SolveOptions("", "", 0, 300, 100, 0.001, False, atol=1e-6, rtol=1e-3)
    solve_sys = SolveSYS(options, None)
    state = [2, 0, 0, 0, 0, 0]
    time, data = solve_sys.solve(state, e, v)
    Xf, fr = fft_fr(data[val], time)

    fig = plt.figure(figsize=(14, 8), layout='constrained')
    axs = fig.subplot_mosaic([["signal", "signal"],
                          ["magnitude", "phase"] #, ["wavelet", "wavelet"] 
                          ])

    # plot time signal:
    axs["signal"].set_title(f'e={e}; v={v}\nSignal')
    axs["signal"].plot(time[:int(50/0.0001)], data[0, :int(50/0.0001)], lw=0.3, color='C0')
    axs["signal"].set_xlabel("Time")
    axs["signal"].set_ylabel("X")

    # plot different spectrum types:
    axs["magnitude"].set_title("Magnitude Spectrum")
    _, stemlines, baseline = axs["magnitude"].stem(fr, Xf, linefmt ='black', markerfmt ='')
    plt.setp(stemlines, 'linewidth', 0.9)
    plt.setp(baseline, visible=False)
    axs["magnitude"].plot([0, 20], [0, 0], '-', lw=0.2, color='black')
    axs["magnitude"].set_xlabel("frequency")
    axs["magnitude"].set_ylabel(f'{key}')

    axs["phase"].set_title("Phase")
    axs["phase"].plot(data[0], data[3], '.', ms=0.4, color='black')
    axs["phase"].set_xlabel("X")
    axs["phase"].set_ylabel('V')

    # widths = np.arange(0.001, Xf.max())
    # cwtmatr = signal.cwt(data[0], signal.ricker, widths)
    # cwtmatr_yflip = np.flipud(cwtmatr)
    # axs["wavelet"].set_title("Wavelet")
    # axs["wavelet"].imshow(cwtmatr_yflip, extent=[time[0], time[-1], 0.001, Xf.max()],
    #                       cmap='plasma', aspect='auto',
    #                         vmax=abs(cwtmatr).max(),
    #                         vmin=-abs(cwtmatr).min())
    # axs["wavelet"].set_xlabel("Time")
    # axs["wavelet"].set_ylabel('frequency')

# counter_plot += phase_plotXT(0, 170, 5.65, 1)
# counter_plot += phase_plotXT(0, 170, 5.65, 1+1/5.65)
# counter_plot += phase_plotXT(0, 170, 5.65, 1+2/5.65)
# counter_plot += phase_plotXT(0, 170, 5.65, 1+3/(2*5.65))

# counter_plot += phase_plotXX(0, 160, 4.3)
# counter_plot += phase_plotXX(1, 160, 4.3)
# counter_plot += phase_plotXX(2, 160, 4.3)
# counter_plot += phase_plotXX(3, 160, 4.3)
# counter_plot += phase_plotXX(4, 160, 4.3)

# counter_plot += phase_plot2d([0, 1], 160, 3.1)
# counter_plot += phase_plot2d([0, 2], 160, 3.1)
# counter_plot += phase_plot2d([0, 3], 160, 3.1)
# counter_plot += phase_plot2d([0, 4], 160, 3.1)


# counter_plot += phase_plot3d([0, 1, 4], 160, 6.3)
# counter_plot += phase_plot3d([1, 2, 3], 160, 6.3)
# counter_plot += phase_plot3d([1, 2, 4], 160, 6.3)
# counter_plot += phase_plot3d([1, 3, 4], 160, 6.3)

# седло 1 2 4

# counter_plot += plot(0, 295, 4.17)
# counter_plot += plot(0, 295, 4.19)
# counter_plot += plot(0, 295, 4.22)
# counter_plot += plot(0, 295, 4.24)


plot_fft({"X" : 0}, 230, 5.65)
# 7.335

plt.show()