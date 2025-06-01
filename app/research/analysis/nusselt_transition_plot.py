import matplotlib.pyplot as plt
import pandas as pd
import os


def plot(path_file, save_path, val, col):
    fig = plt.figure()
    ax = fig.add_subplot()

    df = pd.read_csv(path_file)
    if col == "e":
        df = df.loc[df[col] == val]
        ax.plot(df['v'], df['Nu'], 'k', lw=0.8)
        ax.set_xlabel("v")
        ax.set_ylabel("Nu")
    else:
        df = df.loc[df[col] == val]
        ax.plot(df['e'], df['Nu'], 'k', lw=0.8)
        ax.set_xlabel("e")
        ax.set_ylabel("Nu")

    list_path = save_path.split(sep='/')
    path_dir = list_path[0]
    for d in list_path[1:-1]:
        path_dir += '/' + d
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    plt.savefig(save_path)
    plt.close()
