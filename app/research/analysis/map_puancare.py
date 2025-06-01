import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
import os

def get_map_data(name_file):
    df = pd.read_csv(name_file)

    columns = df.columns
    matrix = df.pivot(index=columns[0], columns=columns[1], values=columns[2])
    e_values = matrix.index.astype(float).round(0)
    v_values = matrix.columns.astype(float).round(2)
    map_data = matrix.values
    return map_data, e_values, v_values

# def combined(file1, file2):
#     map_data1, e_values1, v_values1 = get_map_data(file1)
#     map_data2, e_values2, v_values2 = get_map_data(file2)

#     scale = map_data1.shape[1] / map_data2.shape[1]
#     bottom_resized = zoom(map_data2, (1, scale))  # (по строкам 1, по столбцам scale)
#     data = np.vstack((map_data1, bottom_resized))
#     return data, (v_values1, v_values2, e_values1, e_values2)


# data, (v_values1, v_values2, e_values1, e_values2) = combined("data/puancare/puancare_map e=50-150; v=3-7.5.csv", "data/puancare/puancare_map e=150-300; v=3-7.5.csv")
# extent = (v_values1.min(), v_values2.max(), e_values1.min(), e_values2.max())



# --- Добавление границ ---
# Нахождение контуров с использованием plt.contour()

# E = np.concatenate([e_values1, e_values2])
# contours_2 = plt.contour(
#     V, E, data,
#     levels=[0, 9, 14],
#     colors='red'
# )


# data, E, V = get_map_data("data/nusselt step_e=1 step_v=0.01/nusselt e=50.0-300.0; v=2.5-7.5.csv")
# contours_1 = plt.contour(
#     V[50:], E, data[:, 50:],
#     levels=[1.001],
#     colors=['black']
# )

# plt.clabel(contours, fontsize=8)


def plot(path_file, save_path):
    data, E, V = get_map_data(path_file)
    extent = (V.min(), V.max(), E.min(), E.max())

    # --- Визуализация карты ---
    plt.figure(figsize=(10, 8))
    plt.imshow(data, origin='lower', extent=extent, aspect='auto', cmap='plasma')

    label = "Количество уникальных точек"
    plt.colorbar(label=label)
    plt.title("Карта динамических режимов")
    plt.xlabel("v")
    plt.ylabel("e")

    list_path = save_path.split(sep='/')
    path_dir = list_path[0]
    for d in list_path[1:-1]:
        path_dir += '/' + d
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    plt.savefig(save_path)
    plt.close()