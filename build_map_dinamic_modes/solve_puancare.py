import numpy as np
from system import SolveOptions, SolveSYS, system
from system import SolveOptions, SolveSYS

def solve_logic_fun(data, time):
    poincare_points = []
    
    for i in range(1, len(data)):
        # Поиск пересечения с плоскостью Пуанкаре x1 = section_value
        if (data[i-1][0] < 0 and data[i][0] >= 0):
            poincare_points.append([X[i][2], X[i][3]])  # Сохраняем только Z и V для анализа

    # Если точек мало, считаем режим регулярным
    amount = 0 # Регулярный режим (синий)
    if len(poincare_points) >= 20:
     # Считаем количество уникальных точек (порог P2_max*0.01 для группировки близких точек)
        unique_points = np.unique(np.round(poincare_points, decimals=2), axis=0)
        amount = len(unique_points)
    return [amount]


def solution(path_file, E, V):
    name_columns = ["e", "v", "amt"]
    options = SolveOptions(f'data/puancare{path_file}', name_columns, 0, 60, 10, 0.001, False)
    solve_sys = SolveSYS(options, solve_logic_fun)
    solve_sys.solve_mp(E, V, 6)


if __name__ == '__main__':
    solution(sys.argv[1], np.arange(60, 300, 1), np.arange(3.0, 7.5, 0.01))