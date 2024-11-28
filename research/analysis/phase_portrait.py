import matplotlib.pyplot as plt
import pandas as pd
import os
import re

from math_functions import f1


def plot_phase(name_dir):
    path_dir = f'./datasets/{name_dir}'

    name_dir = f'./image/phase/{name_dir}'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    for _, __, files in os.walk(path_dir):
        for file in files:

            numbers = re.findall(r'\d+', file)
            e = 0.0
            v = 0.0
            if numbers:
                e = float(numbers[0]+'.'+numbers[1])
                v = float(numbers[2]+'.'+numbers[3])

            df = pd.read_csv(path_dir + f'/{file}')
            dX = []
            X = []
            t = []
            for i, row in df.iterrows():
                t.append(row.time)
                X.append(row.X)
                dX.append(f1([e, v], row.time, row[1:]))
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            ax.plot(X, dX, t, 'k', lw=0.8)
            ax.set_xlabel("X")
            ax.set_ylabel('dX/dt')
            ax.set_zlabel('time')
            ax.grid()
            plt.savefig(name_dir+f'/{file[:-4]}.png')


import sys
plot_phase(sys.argv[1])
