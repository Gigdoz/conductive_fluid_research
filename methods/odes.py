import numpy as np

def solve_rk4(ese, total_time, max_step=0.1, eps=0.01, auto_step=True, step_reduction=0.6):
    consts, yi0, funs = ese
    step = max_step

    size = len(funs)
    ki1 = np.zeros(size)
    ki2 = np.zeros(size)
    ki3 = np.zeros(size)
    ki4 = np.zeros(size)
    ki5 = np.zeros(size)

    t = 0
    solution = np.array([np.concatenate(([t], yi0), axis=0)])

    while t < total_time:
        step_3 = step/3
        for i in range(size):
            ki1[i] = step_3 * (funs[i](consts, t, yi0))
        
        for i in range(size):
            ki2[i] = step_3 * (funs[i](consts, t+step_3, yi0+ki1))

        for i in range(size):
            ki3[i] = step * (funs[i](consts, t+step_3, yi0+0.5*(ki1+ki2)))

        for i in range(size):
            ki4[i] = ki1[i] + 4*step_3 * (funs[i](consts, t+step/2, yi0+0.375*(ki1+ki3)))

        for i in range(size):
            ki5[i] = step_3 * (funs[i](consts, t+step, yi0+1.5*(ki4-ki3)))

        if auto_step:
            R = abs(np.sum(2*ki4 - 3*ki3 - ki5))/10
            if step < 0.0001:
                raise Exception('Алгоритм не сходится')
            if R > eps:
                step *= step_reduction
                continue
            elif 32*R < eps and step < max_step:
                step /= step_reduction
                continue

        yi0 += 0.5*(ki4 + ki5)
        t += step
        solution = np.concatenate((solution, [np.concatenate(([t], yi0), axis=0)]), axis=0)

    return solution
    