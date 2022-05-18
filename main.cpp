#include <iostream>
#include <cmath>
#include <fstream>

#define PI 3.1415926535

int main(int argc, char** argv) {
    const int n = 200;
    const int m = 2;
    double y[n + 1][m];
    for (int i = 0; i <= n; i++) {
        y[i][0] = cos(6.0 * PI * (double)i / (double)n);
        y[i][1] = sin(8.0 * PI * (double)i / (double)n);
    }

    double x[n + 1];
    for (int i = 0; i <= n; i++) {
        x[i] = i;
    }

    // Step 1
    double a[n + 1][m];
    for (int i = 0; i <= n; i++) {
        for (int k = 0; k < m; k++) {
            a[i][k] = y[i][k];
        }
    }

    // Step 2
    double b[n][m];
    double d[n][m];

    // Step 3
    double h[n];
    for (int i = 0; i < n; i++) {
        h[i] = x[i + 1] - x[i];
    }

    // Step 4
    double alpha[n][m];
    for (int i = 1; i < n; i++) {
        for (int k = 0; k < m; k++) {
            alpha[i][k] = (3 / h[i]) * (a[i + 1][k] - a[i][k]) - (3 / h[i - 1]) * (a[i][k] - a[i - 1][k]);
        }
    }

    // Step 5
    double c[n + 1][m];
    double l[n + 1];
    double mu[n + 1];
    double z[n + 1][m];

    // Step 6
    l[0] = 1;
    mu[0] = 0;
    for (int k = 0; k < m; k++) {
        z[0][k] = 0;
    }

    // Step 7
    for (int i = 1; i < n; i++) {
        for (int k = 0; k < m; k++) {
            l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1];
            mu[i] = h[i] / l[i];
            z[i][k] = (alpha[i][k] - h[i - 1] * z[i - 1][k]) / l[i];
        }
    }

    // Step 8
    l[n] = 1;
    for (int k = 0; k < m; k++) {
        z[n][k] = 0;
        c[n][k] = 0;
    }

    // Step 9
    for (int j = n - 1; j >= 0; j--) {
        for (int k = 0; k < m; k++) {
            c[j][k] = z[j][k] - mu[j] * c[j + 1][k];
            b[j][k] = (a[j + 1][k] - a[j][k]) / h[j] - (h[j] * (c[j + 1][k] + 2 * c[j][k])) / 3;
            d[j][k] = (c[j + 1][k] - c[j][j]) / (3 * h[j]);
        }
    }
    const int res = 100;
    double curve[n * res][m];
    double tau[res * n];
    for (int i = 0; i < res * n; i++) {
        tau[i] = (double)i / (double)(res);
    }
    for (int j = 0; j < n; j++) {
        for (int k = 0; k < m; k++) {
            for (int r = 0; r < res; r++) {
                curve[j * res + r][k] =
                          a[j][k]
                        + b[j][k] * (tau[j * res + r] - x[j])
                        + c[j][k] * (tau[j * res + r] - x[j]) * (tau[j * res + r] - x[j])
                        + d[j][k] * (tau[j * res + r] - x[j]) * (tau[j * res + r] - x[j]) * (tau[j * res + r] - x[j]);
            }
        }
    }
    std::ofstream fout;
    fout.open("data.csv");
    for (int j = 0; j < n; j++) {
        for (int r = 0; r < res; r++) {
            char str[256];
            sprintf(str, "%f, %f\n", curve[j * res + r][0], curve[j * res + r][1]);
            fout << str;
        }
    }
}