import tkinter as tk
from tkinter import ttk
import json
import threading

from .frame import create_frames_nu, create_frames_solution
from .util import unpack, Event
from app.research import solution, number_Nu
from app.research.analysis import fft_analysis, phase_portrait, plot, plot_2d_nusselt, plot_3d_nusselt, nusselt_transition_plot


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Главное окно")
        self.geometry("300x200")

        # Создаем меню
        main_menu = tk.Menu()

        # Первый раздел
        solution_menu = tk.Menu(tearoff=0)
        solution_menu.add_command(label="Настройки", command=self.open_input_window_solution)
        solution_menu.add_command(label="Вычислить", command=self.calculate_solution)

        nu_menu = tk.Menu(tearoff=0)
        nu_menu.add_command(label="Настройки", command=self.open_input_window_Nu)
        nu_menu.add_command(label="Вычислить", command=self.calculate_Nu)

        menu = tk.Menu(tearoff=0)
        menu.add_cascade(label="Временной ряд", menu=solution_menu)
        menu.add_cascade(label="Число Нуссельта", menu=nu_menu)

        main_menu.add_cascade(label="Решения", menu=menu)

        # Второй раздел
        solution_menu = tk.Menu(tearoff=0)
        solution_menu.add_command(label="График временного ряда", command=self.create_series_time)
        solution_menu.add_command(label="Фурье преобразование", command=self.create_fft)
        solution_menu.add_command(label="Фазовый портрет", command=self.create_phase)

        nu_menu = tk.Menu(tearoff=0)
        nu_menu.add_command(label="Тепловая карта", command=self.create_heat_map)
        nu_menu.add_command(label="График поверхности", command=self.create_surface)
        nu_menu.add_command(label="График для отдельного значения параметра", command=self.create_section)

        menu = tk.Menu(tearoff=0)
        menu.add_cascade(label="Для временного ряда", menu=solution_menu)
        menu.add_cascade(label="Для числа Нуссельта", menu=nu_menu)

        main_menu.add_cascade(label="Графики", menu=menu)
 
        self.config(menu=main_menu)

    def open_input_window_solution(self):
        input_window = InputSettingsWindow(self)
        input_window.create_frames(create_frames_solution)

    def open_input_window_Nu(self):
        input_window = InputSettingsWindow(self)
        input_window.create_frames(create_frames_nu)

    def calculate_solution(self):
        input_window = SavingResultsWindow(self, solution.solution, create_frames_solution)
        input_window.create_frames()

    def calculate_Nu(self):
        input_window = SavingResultsWindow(self, number_Nu.solution, create_frames_nu)
        input_window.create_frames()

    def create_series_time(self):
        win = PlotWindow(self, "График временного ряда")
        win.create_frames("Выберити гармонику", plot.plot)

    def create_fft(self):
        win = PlotWindow(self, "Фурье преобразование")
        win.create_frames("Выберити гармонику", fft_analysis.plot_fft)

    def create_phase(self):
        win = PlotWindow(self, "Фазовый портрет")
        win.create_frames("", phase_portrait.plot_phase)

    def create_heat_map(self):
        win = PlotWindow(self, "Тепловая карта")
        win.create_frames_heat_map()

    def create_surface(self):
        win = PlotWindow(self, "График поверхности")
        win.create_frames_nu()

    def create_section(self):
        win = PlotWindow(self, "График для отдельного значения параметра")
        win.create_frames_nu_transition()


class InputSettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ввод информации")
        self.geometry("500x500")
        
    def create_frames(self, frames):
        data = frames(self)

        def save_data():
            for key, value in data.items():
                for k, val in value.items():
                    data[key][k] = unpack(val)
            with open(f'configs/{frames.__name__}.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.destroy()

        # Кнопка для сохранения введенной информации
        save_button = tk.Button(self, text="Сохранить", command=save_data)
        save_button.pack(pady=10)


class SavingResultsWindow(tk.Toplevel):
    def __init__(self, parent, fun, frames):
        super().__init__(parent)
        self.title("Сохранение результатов")
        self.geometry("400x300")

        self.fun = fun
        self.frames_name = frames.__name__
        self.create_frames
        
    def create_frames(self):
        # Первый фрэйм
        frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)
        label = tk.Label(frame, text="Укажите путь для сохранения результатов")
        label.grid(row=0, column=0, sticky=tk.W, pady=10)
        path_val = tk.StringVar(self)
        path_entr = ttk.Entry(frame, width=20, textvariable=path_val)
        path_entr.grid(row=1, column=0, pady=10, padx=10)
        data = dict(path_solutions=path_val)

        def save_data():
            with open(f'configs/{self.frames_name}.json', 'r') as f:
                json_file = json.load(f)
            json_file["path_solutions"] = data["path_solutions"].get()
            with open(f'configs/{self.frames_name}.json', 'w') as f:
                json.dump(json_file, f, indent=4)

        # Кнопка для сохранения введенной информации
        save_button = tk.Button(frame, text="Сохранить", command=save_data)
        save_button.grid(row=2, column=0, pady=10, padx=5)
        frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

        # Фрэйм для вычисления
        frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

        # Кнопка для запуска алгоритма
        self.event = True
        sol_button = tk.Button(frame, text="Вычислить", command=self.start_calc)
        sol_button.grid(row=0, column=0, pady=10, padx=10)
        frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    def start_calc(self):
        newthread = threading.Thread(target=self.calculate)
        newthread.start()

    def calculate(self):
        tk.Label(self, text="Вычисляется...").pack()
        self.fun(self.frames_name)
        tk.Label(self, text="Завершенно!").pack()
        



class PlotWindow(tk.Toplevel):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.title(name)
        self.geometry("400x300")
        
    def create_frames(self, entr_text, fun):
        frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

        label = tk.Label(frame, text="Укажите путь к директории")
        label.grid(row=0, column=0, sticky=tk.W, pady=10)
        path_val = tk.StringVar(self)
        path_entr = ttk.Entry(frame, width=20, textvariable=path_val)
        path_entr.grid(row=0, column=1, pady=10, padx=10)

        label = tk.Label(frame, text="Укажите путь для сохранения результатов")
        label.grid(row=1, column=0, sticky=tk.W, pady=10)
        save_path_val = tk.StringVar(self)
        save_path_entr = ttk.Entry(frame, width=20, textvariable=save_path_val)
        save_path_entr.grid(row=1, column=1, pady=10, padx=10)

        label = tk.Label(frame, text=entr_text)
        label.grid(row=2, column=0, sticky=tk.W, pady=10)
        harmonics = tk.StringVar(self)
        harmonics_entr = ttk.Entry(frame, width=20, textvariable=harmonics)
        harmonics_entr.grid(row=2, column=1, pady=10, padx=10)

        def create_plot():
            fun(path_val.get(), save_path_val.get(), harmonics.get())

        button = tk.Button(frame, text="Построить", command=create_plot)
        button.grid(row=3, column=0, pady=10, padx=10)
        frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    def create_frames_heat_map(self):
        frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

        label = tk.Label(frame, text="Укажите путь к файлу")
        label.grid(row=0, column=0, sticky=tk.W, pady=10)
        path_val = tk.StringVar(self)
        path_entr = ttk.Entry(frame, width=20, textvariable=path_val)
        path_entr.grid(row=0, column=1, pady=10, padx=10)

        label = tk.Label(frame, text="Укажите путь и название файла для сохранения результатов")
        label.grid(row=1, column=0, sticky=tk.W, pady=10)
        save_path_val = tk.StringVar(self)
        save_path_entr = ttk.Entry(frame, width=20, textvariable=save_path_val)
        save_path_entr.grid(row=1, column=1, pady=10, padx=10)

        def create_plot():
            plot_2d_nusselt.plot(path_val.get(), save_path_val.get())

        button = tk.Button(frame, text="Построить", command=create_plot)
        button.grid(row=3, column=0, pady=10, padx=10)
        frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    def create_frames_nu(self):
        frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

        label = tk.Label(frame, text="Укажите путь к файлу")
        label.grid(row=0, column=0, sticky=tk.W, pady=10)
        path_val = tk.StringVar(self)
        path_entr = ttk.Entry(frame, width=20, textvariable=path_val)
        path_entr.grid(row=0, column=1, pady=10, padx=10)

        def create_plot():
            plot_3d_nusselt.plot_surf(path_val.get())

        button = tk.Button(frame, text="Построить", command=create_plot)
        button.grid(row=3, column=0, pady=10, padx=10)
        frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    def create_frames_nu_transition(self):
        frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

        label = tk.Label(frame, text="Укажите путь к файлу")
        label.grid(row=0, column=0, sticky=tk.W, pady=10)
        path_val = tk.StringVar(self)
        path_entr = ttk.Entry(frame, width=20, textvariable=path_val)
        path_entr.grid(row=0, column=1, pady=10, padx=10)

        label = tk.Label(frame, text="Укажите путь и название файла для сохранения результатов")
        label.grid(row=1, column=0, sticky=tk.W, pady=10)
        save_path_val = tk.StringVar(self)
        save_path_entr = ttk.Entry(frame, width=20, textvariable=save_path_val)
        save_path_entr.grid(row=1, column=1, pady=10, padx=10)

        label = tk.Label(frame, text="Введите название параметра")
        label.grid(row=2, column=0, sticky=tk.W, pady=10)
        param_name = tk.StringVar(self)
        param_name_entr = ttk.Entry(frame, width=20, textvariable=param_name)
        param_name_entr.grid(row=2, column=1, pady=10, padx=10)

        label = tk.Label(frame, text="Введите значение параметра")
        label.grid(row=3, column=0, sticky=tk.W, pady=10)
        param = tk.StringVar(self)
        param_entr = ttk.Entry(frame, width=20, textvariable=param)
        param_entr.grid(row=3, column=1, pady=10, padx=10)

        def create_plot():
            nusselt_transition_plot.plot(path_val.get(), save_path_val.get(), float(param.get()), param_name.get())

        button = tk.Button(frame, text="Построить", command=create_plot)
        button.grid(row=4, column=0, pady=10, padx=10)
        frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)