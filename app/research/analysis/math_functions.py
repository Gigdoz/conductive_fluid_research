from math import *


Pr = 100.0
r = .0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def f1(const, t, y):
    e, v = const
    X, Y, Z, V, W, Nu_y = y
    return Pr*(-X+r*Y+e*W*(cos(2.0*pi*v*t))**2)

def f2(const, t, y):
    e, v = const
    X, Y, Z, V, W, Nu_y = y
    return -Y+X+X*Z

def f3(const, t, y):
    e, v = const
    X, Y, Z, V, W, Nu_y = y
    return -b*Z-X*Y

def f4(const, t, y):
    e, v = const
    X, Y, Z, V, W, Nu_y = y
    return Pr*(-d*V+(r*W-e*Y*(cos(2.0*pi*v*t))**2)/d)

def f5(const, t, y):
    e, v = const
    X, Y, Z, V, W, Nu_y = y
    return -d*W+V

def f6(const, t, y):
    X, Y, Z, V, W, Nu_y = y
    return Z

sys_equations = [f1, f2, f3, f4, f5, f6]