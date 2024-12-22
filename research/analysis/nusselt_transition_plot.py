import matplotlib.pyplot as plt
import pandas as pd
import os


def plot(name_dir, name_file):
    fig = plt.figure()
    ax = fig.add_subplot()

    df = pd.read_csv(f"./datasets/{name_dir}/{name_file}")
    ax.plot(df['e'], df['Nu'], 'k', lw=0.8)
    ax.set_xlabel("e")
    ax.set_ylabel("Nu")

    name_dir = f'./image/nusselt'
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

    name = name_dir + f'/{name_file[:-4]}.png'
    plt.savefig(name)


import sys
plot(sys.argv[1], sys.argv[2])