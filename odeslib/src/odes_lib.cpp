#include "eq_sys.h"

#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

const double A[6] = { 0.0, 1.0 / 4.0, 3.0 / 8.0, 12.0 / 13.0, 1.0, 1.0 / 2.0 };
const double B[6][6] = {
    { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 },
    { 1.0 / 4.0, 0.0, 0.0, 0.0, 0.0, 0.0 },
    { 3.0 / 32.0, 9.0 / 32.0, 0.0, 0.0, 0.0, 0.0 },
    { 1932.0 / 2197.0, -7200.0 / 2197.0, 7296.0 / 2197.0, 0.0, 0.0, 0.0 },
    { 439.0 / 216.0, -8.0, 3680.0 / 513.0, -845.0 / 4104.0, 0.0, 0.0 },
    { -8.0 / 27.0, 2.0, -3544.0 / 2565.0, 1859.0 / 4104.0, -11.0 / 40.0, 0.0 } };
const double C[6] = { 16.0 / 135.0, 0.0, 6656.0 / 12825.0, 28561.0 / 56430.0, -9.0 / 50.0, 2.0 / 55.0 };
const double C_HAT[6] = { 25.0 / 216.0, 0.0, 1408.0 / 2565.0, 2197.0 / 4104.0, -1.0 / 5.0, 0.0 };


void Add(double arr1[], double s, int size) {
    for (int i = 0; i < size; i++) {
        arr1[i] += s;
    }
}

void Init(double arr1[], double s, int size) {
    for (int i = 0; i < size; i++) {
        arr1[i] = s;
    }
}

void Copy(double arr1[], const double arr2[], int size) {
    for (int i = 0; i < size; i++) {
        arr1[i] = arr2[i];
    }
}

double Norm(const double arr1[], const double arr2[], int size) {
    double norm = 0.0;
    for (int i = 0; i < size; i++) {
        double r = arr1[i] - arr2[i];
        norm += r * r;
    }
    return sqrt(norm);
}

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN32
#  define MODULE_API __declspec(dllexport)
#else
#  define MODULE_API
#endif

MODULE_API int solve_rkf45(char* path_file, double consts_init[8], double t0,
    double t_end, double tol = 1e-6, double h_init = 0.1,
    double h_min = 1e-6, double h_max = 1.0, double output_step = 0.01) {

    FILE* fp = fopen(path_file, "a+");
    if (!fp) {
        return -1;
    }

    double t = t0;
    const double e = consts_init[0];
    const double v = consts_init[1];
    double h = h_init;
    double next_output_time = t0; 

    const int num_funs = 6;
    double y[num_funs];
    for (int i = 0; i < num_funs; i++) {
        y[i] = consts_init[i + 2];
    }

    double k[6][num_funs];
    while (t < t_end) {
        if (t + h > t_end) {
            h = t_end - t;
        }

        for (int i = 0; i < 6; i++) {
            double ti = t + A[i] * h;
            for (int p = 0; p < num_funs; p++) {
                double yi[num_funs];
                Copy(yi, y, num_funs);
                double sum = 0.0;
                if (i > 0) {
                    for (int j = 0; j < i; j++) {
                        sum += B[i][j] * k[j][p];
                    }
                    sum *= h;
                    Add(yi, sum, num_funs);
                }
                k[i][p] = sys[p](e, v, ti, yi);
            }
        }

        double y4[num_funs];
        double y5[num_funs];

        double sum1[num_funs];
        double sum2[num_funs];
        Init(sum1, 0.0, num_funs);
        Init(sum2, 0.0, num_funs);
        for (int i = 0; i < num_funs; i++) {
            for (int j = 0; j < 6; j++) {
                sum1[i] += k[j][i] * C_HAT[j];
                sum2[i] += k[j][i] * C[j];
            }
            y4[i] = y[i] + h * sum1[i];
            y5[i] = y[i] + h * sum2[i];
        }

        double error = Norm(y5, y4, num_funs);

        if (error < tol) {
            t += h;
            Copy(y, y5, num_funs);

            if (t >= next_output_time) {
                fprintf(fp, "%lf, ", t);
                for (int i = 0; i < num_funs - 1; i++) {
                    fprintf(fp, "%lf, ", y[i]);
                }
                fprintf(fp, "%lf\n", y[num_funs - 1]);
                next_output_time += output_step;
            }
        }

        if (error > 0.0) {
            h *= fmin(fmax(0.84 * pow(tol / error, 0.25), 0.1), 4.0);
        }
        h = fmax(fmin(h, h_max), h_min);
    }
	
	return 0;
}

MODULE_API int nusselt_number(char* path_file, double E[3], double V[3], double init[6], double t0,
    double t_end, double tol = 1e-6, double h_init = 0.1,
    double h_min = 1e-6, double h_max = 1.0) {

    FILE* fp = fopen(path_file, "a+");
    if (!fp) {
        return -1;
    }

    double h = h_init;

    const int num_funs = 6;
    double k[6][num_funs];
    for (double e = E[0]; e <= E[1]; e += E[2]) {
        for (double v = V[0]; v <= V[1]; v += V[2]) {

            double y[num_funs];
            Copy(y, init, num_funs);
            for (double t = t0; t < t_end;) {
                if (t + h > t_end) {
                    h = t_end - t;
                }

                for (int i = 0; i < 6; i++) {
                    double ti = t + A[i] * h;
                    for (int p = 0; p < num_funs; p++) {
                        double yi[num_funs];
                        Copy(yi, y, num_funs);
                        double sum = 0.0;
                        if (i > 0) {
                            for (int j = 0; j < i; j++) {
                                sum += B[i][j] * k[j][p];
                            }
                            sum *= h;
                            Add(yi, sum, num_funs);
                        }
                        k[i][p] = sys[p](e, v, ti, yi);
                    }
                }

                double y4[num_funs];
                double y5[num_funs];

                double sum1[num_funs];
                double sum2[num_funs];
                Init(sum1, 0.0, num_funs);
                Init(sum2, 0.0, num_funs);
                for (int i = 0; i < num_funs; i++) {
                    for (int j = 0; j < 6; j++) {
                        sum1[i] += k[j][i] * C_HAT[j];
                        sum2[i] += k[j][i] * C[j];
                    }
                    y4[i] = y[i] + h * sum1[i];
                    y5[i] = y[i] + h * sum2[i];
                }

                double error = Norm(y5, y4, num_funs);

                if (error < tol) {
                    t += h;
                    Copy(y, y5, num_funs);
                }

                if (error > 0.0) {
                    h *= fmin(fmax(0.84 * pow(tol / error, 0.25), 0.1), 4.0);
                }
                h = fmax(fmin(h, h_max), h_min);
            }

            fprintf(fp, "%lf, ", e);
            fprintf(fp, "%lf, ", v);
            double nu = 1.0 - 2.0 * y[num_funs - 1] / (t_end - t0);
            fprintf(fp, "%lf\n", nu);
        }
    }
    
    return 0;
} 

#ifdef __cplusplus
}
#endif