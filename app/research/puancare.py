import numpy as np
import json
import os
from .system import SolveOptions, SolveSYS
from .system import SolveOptions, SolveSYS

def solve_logic_fun(data, time):
    poincare_points = []
    
    for i in range(1, len(data[0])):
        # Поиск пересечения с плоскостью Пуанкаре X=0
        if (data[0, i-1] < 0 and data[0, i] >= 0):
            poincare_points.append([data[1, i], data[2, i]])  # Сохраняем только Y и Z для анализа

    # Если точек мало, считаем режим регулярным
    amount = 0 # Регулярный режим (синий)
    if len(poincare_points) >= 20:
     # Считаем количество уникальных точек (порог P2_max*0.01 для группировки близких точек)
        unique_points = np.unique(np.round(poincare_points, decimals=2), axis=0)
        amount = len(unique_points)
    return [amount]


def solution(name_config):
    config = None
    with open(f'configs/{name_config}.json') as f:
        config = json.load(f)

    path_solutions = config["path_solutions"]
    if not os.path.exists(path_solutions):
        os.makedirs(path_solutions)

    e_start, e_stop, e_step = config["control_constants"]["e"]
    E = np.arange(e_start, e_stop+e_step, e_step)
    v_start, v_stop, v_step = config["control_constants"]["v"]
    V = np.arange(v_start, v_stop+v_step, v_step)

    name_columns = ["e", "v", "amt"]
    name = path_solutions + f'/puancare e={E[0]}-{E[-1]}; v={V[0]}-{round(V[-1], 3)}.csv'
    options = SolveOptions(name, name_columns, config['algorithm_settings']['t0'], config['algorithm_settings']['t_end'],
                            config['algorithm_settings']['T_transient'], config['algorithm_settings']['output_step'],
                            False, config['algorithm_settings']['atol'], config['algorithm_settings']['rtol'])
    solve_sys = SolveSYS(options, solve_logic_fun)
    solve_sys.solve_mp(E, V, 4)