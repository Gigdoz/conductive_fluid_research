import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import qr

# Параметры системы
Pr = 100.0
k = 0.962
b = 4/(1+k**2)
d = (4+k**2)/(1+k**2)

def system(t, state, e, v):
    X, Y, Z, V, W = state
    cos_2 = (np.cos(2.0 * np.pi * v * t))**2
    dX = Pr*(-X+e*W*cos_2)
    dY = -Y+X+X*Z
    dZ = -b*Z-X*Y
    dV = -Pr*(d*V+e*Y*cos_2/d)
    dW = -d*W+V
    return [dX, dY, dZ, dV, dW]

def jacobian(t, state, e, v):
    X, Y, Z, V, W = state
    cos_2 = (np.cos(2.0 * np.pi * v * t))**2
    J = np.zeros((5, 5))
    
    J[0, 0] = -Pr
    J[0, 4] = Pr * e * cos_2
    
    J[1, 0] = 1 + Z
    J[1, 1] = -1
    J[1, 2] = X
    
    J[2, 0] = -Y
    J[2, 1] = -X
    J[2, 2] = -b
    
    J[3, 1] = -Pr * e * cos_2 / d
    J[3, 3] = -Pr * d
    
    J[4, 3] = 1
    J[4, 4] = -d
    
    return J

def lyapunov_exponents(t_span, initial_state, e, v, T_transient, dt, lyap_steps=1000):
    dim = len(initial_state)
    state = initial_state.copy()
    t_current = t_span[0]
    
    # 1. Пропускаем переходный процесс
    for _ in range(int(T_transient/dt)):
        sol = solve_ivp(system, (t_current, t_current + dt), state, args=(e, v), rtol=1e-5, atol=1e-8)
        state = sol.y[:, -1]
        t_current += dt
    
    # 2. Теперь вычисляем показатели Ляпунова
    Q = np.eye(dim)
    lyapunovs = np.zeros(dim)
    
    for _ in range(lyap_steps):
        # Интегрируем основную систему
        sol = solve_ivp(system, (t_current, t_current + dt), state, args=(e, v), rtol=1e-5, atol=1e-8)
        state = sol.y[:, -1]
        
        # Интегрируем вариационное уравнение
        Phi = Q.copy()
        for _ in range(5):  # Несколько подшагов для точности
            J = jacobian(t_current, state, e, v)
            dPhi = J @ Phi
            Phi += dPhi * (dt / 5)
            t_current += dt / 5
        
        # QR-разложение и обновление показателей
        Q, R = qr(Phi, mode='economic')
        lyapunovs += np.log(np.abs(np.diag(R)))
    
    # Усредняем
    total_time = lyap_steps * dt
    lyapunovs /= total_time
    initial_state = state
    return lyapunovs

# Пример использования
initial_state = [2, 0, 0, 0, 0]
e = 160
v = 3.1
t_span = (0, 400)

import csv

with open('data/lyp/test2.csv', mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['e', 'v', 'X', 'Y', 'Z', 'V', 'W'])
e = 160
V = np.arange(4.666, 4.667, 0.0001)
for v in V:
    lyapunovs = lyapunov_exponents(t_span, initial_state, e, v, 100, 0.001, 70000)
    with open('data/lyp/test2.csv', mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([e, v, *lyapunovs])