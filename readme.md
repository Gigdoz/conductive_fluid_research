# Проект на Python для диплома

## Численные методы

В пакете `methods` реализуется метод Рунге-Кутты-Мерсона (RK) четвертого порядка с автоматическим подбором шага для решения обыкновенных дифференциальных уравнений.
Имеется гибкая настройка.
Главный параметр `ese` - extended system of equations.

## Скрипты
В `solution.py` решается система ОДУ записанная в файле `math_functions.py`.
Настройки скрипта записываются в конфигурационный файл `json` (Смотреть пример).
Все конфиги обязательно хранить в директории `configs`.
Решение записывается в файл `csv` в директорию `datasets` в папку с именем номером или указанным в config.

Для запуска нужно ввести в консоль команду `python3 solution.py "<name_config>"`.

В `fft_analysis.py` делается Фурье преобразование и создаются графики.
Первым аргументом передается имя папки содержащееся в директории `datasets`,
где программа проходится по всем файлам содержащиеся там.
Вторым аргументом передается название величины (столбца из csv-файла).
В результате получаем `image\fft\<имя передаваймой папки>`, где будут все графики.

Для запуска нужно ввести в консоль команду `python3 fft_analysis.py "<name_dir>" "<name_value>"`.

## Конфигурационный файл

- `initial_conditions` - задаются начальные амплитуды
- `control_constants` - управляемые параметры системы (`e` и `v`).
Для них задается начальное значение, конечное и шаг `[start, stop, step]`.
Другие константы записанны в `math_functions.py`.
- `algorithm_settings` - настройки для метода Рунге-Кутты-Мерсона `solve_rk4`.
    - `total_time` - общее время.
    - `max_step` - Начальный шаг, а также ограничение.
    - `eps` - управляемая точность алгоритма.
    - `auto_step` - режим подбора шага.
    - `step_reduction` - коэфф. уменьшения шага для контроля точности алгоритма.
- `name_solutions` - имя папки куда будут выгружаться файлы с решением.

## Примечание

Алгоритм решения ОДУ может не сходиться, рекомендуется увеличить `step_reduction` для более плавного изменения шага, а также уменьшение `eps` или увеличения `max_step`.

На примере этой работы модуль `methods` можно адаптировать к любой задачи такого типа, написав системы ОДУ и расширить её начальными условиями и определением констант.