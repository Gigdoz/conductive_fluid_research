# Электроконвекция в слабопроводящей жидкости в переменном электрическом поле
___

## Структура проекта

**Проект содержит два подпроекта.**

**odeslib**, библиотека на *С* для решения ОДУ, которые уже записаны в ней.
Сборка происходит с помощью *Cmake*, в результате получается динамический линковочный файл, с расширением в зависемости от платформы.
Работает для *Windows* и *Linux* систем.

Команды для сборки:
(Для начала откройте консоль в директории odeslib и запустите команду)
```
mkdir build; cd build; cmake ..; cmake --build .
```
В результате в lib появится нужный файл.

**research**, это *Python* проект для получение решений и их обработка.
1. В **analysis** содержатся скрипты для получения графиков для анализа результатов:
    1. Фурье-преобразование `fft_analysis.py`
    2. Фазовый портрет рисует траекторию в 2 координатах амплитуд `phase_portrait.py`
    2. Получение тепловой карты для числа Нуссельта в зависимости от электрической постоянной и начальной частоты `plot_Nusselt.py`.

    Для наглядности система ОДУ записана в файле `math_functions.py`.
    Результат записывается в **image**.
2. `solution.py` реализуется библиотечная функция `solve_rkf45`.
3. `number_Nu.py` реализуется библиотечная функция `nusselt_number`.
4. В **configs** хранится настройки скриптов записываются в конфигурационный файл `json`.
<br>

## Численные методы

В библиотекае реализуется метод Рунге-Кутты-Фельберга с адаптивным шагом. В ней уже содержуться нужные уравнения с константами.
https://en.wikipedia.org/wiki/List_of_Runge–Kutta_methods

1. Первая функция `solve_rkf45` служит для получения значений амплитуд на каждом шаги и записывает их в файл.
    *Параметры:*
    <em>
    - path_file: путь к csv-файлу
    - const_init: массив с управляющими параметрами и начальным распределением
    - t0: начальное значение независимой переменной (времени)
    - t_end: конечное значение независимой переменной
    - tol: допустимая ошибка на шаге (точность)
    - h_init: начальный шаг
    - h_min: минимально допустимый шаг
    - h_max: максимально допустимый шаг
    - output_step: шаг по времени, с которым результаты записываются в файл
    </em>

<br>

2. Вторая функция `nusselt_number` служит для получения числа Нуссельта на последней итерации, и результат выводится в виде значений `e, v, Nu`.

    *Параметры:*
    <em>
    - Вместо `const_init` передаются параметры в виде массивов `[start, stop, step]` и начальное распределение
    </em>

Все результаты записываются в csv-файлы.
<br>

## Скрипты

Решение записывается в файл `csv` в директорию `datasets` в папку с именем номером или указанным в config.

(Для запуска нужно открыть консоль в **research**)

`solution.py`
Передается имя конфиг файла содержащееся в директории `config`.
В результате получаем файл с числами Нуссельта соответствующим определённому набору параметров `datasets\<имя указанное в конфиге>`.
Для запуска нужно ввести в консоль команду:
`python3 solution.py "<name_config>"`.
<br>
`number_Nu.py`
Передается имя конфиг файла содержащееся в директории `config`.
В результате получаем файлы с временными рядами амплитуд для каждого набора параметров `datasets\<имя указанное в конфиге>`.
Для запуска нужно ввести в консоль команду:
`python3 number_Nu.py "<name_config>"`.
<br>

В директории **analisys** имеются скрипты для анализа решений.

`fft_analysis.py`
Первым аргументом передается имя папки содержащееся в директории `datasets`,
где программа проходится по всем файлам содержащиеся там.
Вторым аргументом передается название величины (столбца из csv-файла).
В результате получаем `image\fft\<имя передаваймой папки>`, где будут все графики.
Для запуска нужно ввести в консоль команду:
`python3 analisys/fft_analysis.py "<name_dir>" "<name_value>"`.
<br>

`phase_portrait.py`
Для отрисовки фазавого портрета.
Передается имя папки содержащееся в директории `datasets`.
В результате получаем `image\phase\<имя передаваймой папки>`.
Для запуска нужно ввести в консоль команду (набор амплитуд может быть любым, этот набор выбран для примера):
`python3 analisys/phase_portrait.py "<name_dir>" "X Y"`.

<br>

`plot_nusselt.py`
Передается 2 аргументом имя директории и 2 имя csv-файла содержащееся в `datasets`, полученный в результате работы `number_Nu.py`.
В итоге получаем `image\<name_dir>\<name_file>`.
Для запуска нужно ввести в консоль команду:
`python3 analisys/plot_nusselt.py "<name_dir>" "<name_file>"`.
<br>

`nusselt_transition_plot.py`
Для зависимости числа Нуссельта при одном фиксированном параметре.
Передается 2 аргументом имя директории и 2 имя csv-файла содержащееся в `datasets`, полученный в результате работы `number_Nu.py`.
В итоге получаем `image\<name_dir>\<name_file>`.
Для запуска нужно ввести в консоль команду:
`python3 analisys/nusselt_transition_plot.py "<name_dir>" "<name_file>"`.
<br>

`plot.py`
График для временного ряда.
Передается 1 аргументом имя директории и 2 имя csv-файла содержащееся в `datasets`, полученный в результате работы `solution.py`.
В итоге получаем `image\<name_dir>`.
Для запуска нужно ввести в консоль команду:
`python3 analisys/plot.py "<name_dir>" "X"`.
<br>

`combine_datasets.py` нужен для объединение датасетов nusselt, так как расчет может производиться кусочно из-за того, что в некоторых зонах нужно увеличивать разрешенность картинки.
<br>

## Конфигурационный файл

- `initial_conditions` - задаются начальные амплитуды
- `control_constants` - управляемые параметры системы (`e` и `v`).
    - `series` - указание формата передачи параметров. Если `True`, то в виде списка. Если `False`, то задается начальное значение, конечное и шаг `[start, stop, step]`.

- `algorithm_settings` - настройки для метода Рунге-Кутты-Фельберга `solve_rk45`.
    - `t0` - начальное значение независимой переменной
    - `t_end` - конечное значение независимой переменной
    - `tol` - допустимая ошибка на шаге (точность)
    - `h_init` - начальный шаг
    - `h_min` - минимально допустимый шаг
    - `h_max` - максимально допустимый шаг
    - `output_step` - шаг по времени, с которым результаты записываются в файл
- `name_solutions` - имя папки куда будут выгружаться файлы с решением.

Для `nusselt_Nu` тоже самое, просто некоторые параметры не будут учитываться.
И `control_constants` нужно передовать в виде `[start, stop, step]`.
<br>

## Примечание

Настройки алгоритма отвечающие за точность могут сильно замедлить его работу или повлиять незаметно, менять их не рекомендуется.
Проверяйти это на небольших интервалах.