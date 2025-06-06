# Электроконвекция в слабопроводящей жидкости в переменном электрическом поле
___


Используется модифицированная модель Лоренца.  
Она представляет собой 5 уравнений и одно дополнительное для расчета среднего по времени теплового потока (Число Нуссельта):

$\dot{X} = Pr(-X+eWcos(2\pi vt)^2)$  
$\dot{Y} = -Y+X+XZ$  
$\dot{Z} = -bZ-XY$  
$\dot{V} = -Pr(dV+eYcos(2\pi vt)^2/d)$  
$\dot{W} = -dW+V$  
$\dot{Nu} = Z$   

## Структура проекта

**interface** Графический интерфейс  (запускается исходником app.py)

**research** основная часть проекта, в нем содержаться 2 файла для численных расчетов и модуль для анализа результатов.

## Файлы

`solution.py`  

`number_Nu.py`

В директории **analisys** файлы для анализа решений.

`fft_analysis.py`

`phase_portrait.py`  
Для отрисовки фазавого портрета.

`plot_2d_nusselt.py`

`plot_3d_nusselt.py`

`nusselt_transition_plot.py`  
Для зависимости числа Нуссельта при одном фиксированном параметре.

`plot.py`  
График для временного ряда.

## Замечания по работе с приложением
При вкл series нужно заполнить через пробел последовательность параметров  
При выкл series заполняется ввиде "p_star p_end p_step", создается последовательность с заданным шагом
