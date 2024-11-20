#pragma once

#define _USE_MATH_DEFINES
#include <math.h>

const double Pr = 100.0;
const double r = 0.0;
const double k = 0.962;
const double b = 4.0 / (1.0 + k * k);
const double d = (4.0 + k * k) / (1.0 + k * k);

double X(double e, double v, double t, const double y[]) {
	double c = cos(2.0 * M_PI * v * t);
	return Pr * (-y[0] + r * y[1] + e * y[4] * c * c);
}

double Y(double e, double v, double t, const double y[]) {
	return -y[1] + y[0] + y[0] * y[2];
}

double Z(double e, double v, double t, const double y[]) {
	return -b * y[2] - y[0] * y[1];
}

double V(double e, double v, double t, const double y[]) {
	double c = cos(2.0 * M_PI * v * t);
	return Pr * (-d * y[3] + (r * y[4] - e * y[1] * c * c) / d);
}

double W(double e, double v, double t, const double y[]) {
	return -d * y[4] + y[3];
}

double Nu(double e, double v, double t, const double y[]) {
	return y[2];
}

double (*sys[6])(double, double, double, const double*) = {X, Y, Z, V, W, Nu};