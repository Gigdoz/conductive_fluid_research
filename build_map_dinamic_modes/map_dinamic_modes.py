import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


name_file = "data/puancare/puancare_map e=50-150; v=3-5.csv"
df = pd.read_csv(name_file)

columns = df.columns
matrix = df.pivot(index=columns[0], columns=columns[1], values=columns[2])
e_values = matrix.index.astype(float)
v_values = matrix.columns.astype(float)
map_data = matrix.values

# --- Визуализация карты ---
plt.figure(figsize=(8, 6))
plt.imshow(map_data, origin='lower', extent=(v_values.min(), v_values.max(), e_values.min(), e_values.max()), aspect='auto', cmap='plasma')

label = "Количество уникальных точек Пуанкаре"
plt.colorbar(label=label)
plt.title("Карта динамических режимов")
plt.xlabel("v")
plt.ylabel("e")
plt.show()

# --- Добавление границ ---
# Нахождение контуров с использованием plt.contour()
# contours = plt.contour(
#     P2_range, P1_range, map_data, 
#     levels=[1.0001],  # Можно задать несколько уровней, например, [-0.1, 0, 0.1]
#     colors='black'
# )
# plt.clabel(contours, fontsize=8)
plt.show()