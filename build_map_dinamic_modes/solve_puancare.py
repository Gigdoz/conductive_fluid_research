import numpy as np
from math import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from tqdm import tqdm

# python build_map_dinamic_modes/solve_puancare.py

# --- Параметры системы ---
T_max = 80     # Время интегрирования
T_transient = 8   # Время для исключения переходного процесса
dt = 0.01        # Шаг дискретизации при регистрации точек Пуанкаре

# --- Диапазоны параметров для карты ---
P1_range = np.linspace(50.0, 150.0, 100)  # Диапазон значений P1
P2_range = np.linspace(5.0, 7.5, 250)  # Диапазон значений P2

# --- Плоскость Пуанкаре (пересечение по x1 = 0) ---
section_value = 0.0
section_index = 0  # Индекс переменной, по которой проверяется пересечение

# --- Уравнения системы (пример) ---

Pr = 100.0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def system(t, state, e, v):
    X, Y, Z, V, W = state

    cos_2 = (cos(2.0*pi*v*t))**2
    dX = Pr*(-X+e*W*cos_2)
    dY = -Y+X+X*Z
    dZ = -b*Z-X*Y
    dV = -Pr*(d*V+e*Y*cos_2/d)
    dW = -d*W+V
    return [dX, dY, dZ, dV, dW]

# --- Функция для численного интегрирования и поиска точек Пуанкаре ---
def poincare_map(P1, P2, state):    
    # Интегрируем систему до T_transient, чтобы исключить переходный процесс
    sol0 = solve_ivp(system, [0, T_transient], state, args=(P1, P2), t_eval=[T_transient])
    state = sol0.y.T[0]
    
    # Интегрируем основную систему и собираем точки Пуанкаре
    times = np.arange(0, T_max, dt)
    sol = solve_ivp(system, [0, T_max], state, args=(P1, P2), t_eval=times)
    
    X = sol.y.T
    poincare_points = []
    
    for i in range(1, len(X)):
        # Поиск пересечения с плоскостью Пуанкаре x1 = section_value
        if (X[i-1][section_index] < section_value and X[i][section_index] >= section_value):
            poincare_points.append(X[i][1:3])  # Сохраняем только x2 и x3 для анализа

    return np.array(poincare_points)


def solution(name_file):
    # Сохранение начальных условий для продолжение вычесления
    X0 = np.random.rand(5) * 2 - 1

    with open(f"data/puancare/{name_file}", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["e", "v", "amounts"])

        for i, P1 in enumerate(tqdm(P1_range, desc="Building Map")):
            for j, P2 in enumerate(P2_range):
                points = poincare_map(P1, P2, X0)
                
                # Если точек мало, считаем режим регулярным
                amount = 0 # Регулярный режим (синий)
                if len(points) >= 20:
                    # Считаем количество уникальных точек (порог P2_max*0.01 для группировки близких точек)
                    unique_points = np.unique(np.round(points, decimals=2), axis=0)
                    amount = len(unique_points)
                writer.writerow([P1, P2, amount])

import sys
solution(sys.argv[1])