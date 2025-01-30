from cx_Freeze import setup, Executable

setup(
    name="Conductive Fluid Research",
    version="1.0",
    description="Расчетная программа с возможностью создания графиков разного вида.",
    options = {"build_exe": {"packages": ["pandas", "os", "numpy", "math",
                                           "json", "csv", "scipy", "matplotlib",
                                             "threading"],
                              "excludes": ["tkinter"]}},
    executables=[Executable("app.py", base = "Win32GUI")]
    )
