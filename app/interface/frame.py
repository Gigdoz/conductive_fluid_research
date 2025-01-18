import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import json


def fill_in_frame(self, frame, data, width, row, names_and_amp):
    for (name,amp), i in zip(names_and_amp, range(len(names_and_amp))):
        label = tk.Label(frame, text=name)
        label.grid(row=row, column=2*i, sticky=tk.W, pady=10)
        val = tk.StringVar(self)
        entr = ttk.Entry(frame, width=width, textvariable=val)
        entr.insert(tk.END, amp)
        entr.grid(row=row, column=2*i+1, pady=10, padx=5)
        data[name] = val

def create_frames_solution(self):
    # Словарь для сохранение данных
    data = dict()

    # Первый фрэйм
    tk.Label(self, text="initial_conditions").pack()
    frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)
    
    names_and_amp = [("X",2), ("Y",0), ("Z",0), ("V",0), ("W",0)]
    data["initial_conditions"] = dict()
    fill_in_frame(self, frame, data["initial_conditions"], 8, 0, names_and_amp)
    frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)
    data["initial_conditions"]["Nu_y"] = tk.StringVar(self, value=0)

    # Второй фрэйм
    tk.Label(self, text="control_constants").pack()
    frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

    # def checkbutton_changed():
    #     if enabled.get() == 1:
    #         showinfo(title="Info", message="Включено")
    #     else:
    #         showinfo(title="Info", message="Отключено")

    enabled = tk.IntVar(self)
    enabled_checkbutton = ttk.Checkbutton(frame, text="series", variable=enabled)
    enabled_checkbutton.grid(row=0, column=0, sticky=tk.W, pady=10)

    label = tk.Label(frame, text="e")
    label.grid(row=1, column=0, sticky=tk.W, pady=10)
    e_val = tk.StringVar(self)
    E_entr = ttk.Entry(frame, width=20, textvariable=e_val)
    E_entr.grid(row=1, column=1, pady=10, padx=5)

    label = tk.Label(frame, text="v")
    label.grid(row=2, column=0, sticky=tk.W, pady=10)
    v_val = tk.StringVar(self)
    V_entr = ttk.Entry(frame, width=20, textvariable=v_val)
    V_entr.grid(row=2, column=1, pady=10, padx=5)

    data["control_constants"] = dict(series=enabled, e=e_val, v=v_val)
    frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    # Третий фрэйм
    tk.Label(self, text="algorithm_settings").pack()
    frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

    al_set = [("t0",0), ("t_end",10), ("atol",1e-6), ("rtol",1e-3), ("output_step",0.01)]

    enabled = tk.IntVar(self)
    enabled_checkbutton = ttk.Checkbutton(frame, text="continue_by_par", variable=enabled)
    enabled_checkbutton.grid(row=0, column=0, sticky=tk.W, pady=10)

    data["algorithm_settings"] = dict(continue_by_par=enabled)
    fill_in_frame(self, frame, data["algorithm_settings"], 8, 1, al_set[0:3])
    fill_in_frame(self, frame, data["algorithm_settings"], 8, 2, al_set[3:])
    frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    return data


def create_frames_nu(self):
    # Словарь для сохранение данных
    data = dict()

    # Первый фрэйм
    tk.Label(self, text="initial_conditions").pack()
    frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)
    
    names_and_amp = [("X",2), ("Y",0), ("Z",0), ("V",0), ("W",0)]
    data["initial_conditions"] = dict()
    fill_in_frame(self, frame, data["initial_conditions"], 8, 0, names_and_amp)
    data["initial_conditions"]["Nu_y"] = tk.StringVar(self, value=0)
    frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    # Второй фрэйм
    tk.Label(self, text="control_constants").pack()
    frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

    label = tk.Label(frame, text="e")
    label.grid(row=1, column=0, sticky=tk.W, pady=10)
    e_val = tk.StringVar(self)
    E_entr = ttk.Entry(frame, width=20, textvariable=e_val)
    E_entr.grid(row=1, column=1, pady=10, padx=5)

    label = tk.Label(frame, text="v")
    label.grid(row=2, column=0, sticky=tk.W, pady=10)
    v_val = tk.StringVar(self)
    V_entr = ttk.Entry(frame, width=20, textvariable=v_val)
    V_entr.grid(row=2, column=1, pady=10, padx=5)

    data["control_constants"] = dict(e=e_val, v=v_val)
    frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    # Третий фрэйм
    tk.Label(self, text="algorithm_settings").pack()
    frame = tk.Frame(self, bd=2, relief=tk.SOLID, padx=10, pady=10)

    al_set = [("t0",0), ("t_end",10), ("atol",1e-6), ("rtol",1e-3)]
    enabled = tk.IntVar(self)
    enabled_checkbutton = ttk.Checkbutton(frame, text="continue_by_par", variable=enabled)
    enabled_checkbutton.grid(row=0, column=0, sticky=tk.W, pady=10)

    data["algorithm_settings"] = dict(continue_by_par=enabled)
    fill_in_frame(self, frame, data["algorithm_settings"], 8, 1, al_set)
    frame.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

    return data