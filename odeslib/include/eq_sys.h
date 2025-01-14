#pragma once


#include <math.h>

const long double PI = 3.14159265358979323851;
const long double Pr = 100.0;
const long double k = 0.962;
const long double b = 4.0 / (1.0 + k * k);
const long double d = (4.0 + k * k) / (1.0 + k * k);

long double X(long double e, long double v, long double t, const long double y[]) {
	long double c = cos(2.0 * PI * v * t);
	return Pr * (-y[0] + e * y[4] * c * c);
}

long double Y(long double e, long double v, long double t, const long double y[]) {
	return -y[1] + y[0] + y[0] * y[2];
}

long double Z(long double e, long double v, long double t, const long double y[]) {
	return -b * y[2] - y[0] * y[1];
}

long double V(long double e, long double v, long double t, const long double y[]) {
	long double c = cos(2.0 * PI * v * t);
	return - Pr * (d * y[3] + e * y[1] * c * c / d);
}

long double W(long double e, long double v, long double t, const long double y[]) {
	return -d * y[4] + y[3];
}

long double Nu(long double e, long double v, long double t, const long double y[]) {
	return y[2];
}

long double (*sys[6])(long double, long double, long double, const long double*) = {X, Y, Z, V, W, Nu};
