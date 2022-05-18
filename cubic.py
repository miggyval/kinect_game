from numba import njit
import numba as nb
import matplotlib.pyplot as plt
import numpy as np
import math
from perlin_noise import PerlinNoise

@njit(parallel=True)
def call(n, m, a, b, c, d, x):
    res = 100
    curve = np.zeros((n * res, m))
    tau = np.zeros((n * res, m))
    for i in range(n * res):
        tau[i] = i / (res * n)

    for j in nb.prange(n):
        for r in range(res):
            val = a[j, :] \
                + b[j, :] * (tau[j * res + r] - x[j]) \
                + c[j, :] * (tau[j * res + r] - x[j]) ** 2 \
                + d[j, :] * (tau[j * res + r] - x[j]) ** 3
            curve[j * res + r] = val
    return (tau, curve)

class MyCubicSpline:
    def __init__(self, y):
        
        # Number of Points
        n = y.shape[0] - 1
        m = y.shape[1]
        
        x = np.linspace(0, 1, n + 1)
        
        # Step 1
        a = np.zeros((n + 1, m))
        for i in range(0, n + 1):
            a[i, :] = y[i, :]
        
        # Step 2
        b = np.zeros((n, m))
        d = np.zeros((n, m))
        
        # Step 3
        h = np.zeros((n,))
        for i in range(0, n):
            h[i] = x[i + 1] - x[i]
            
        # Step 4
        alpha = np.zeros((n, m))
        for i in range(1, n):
            alpha[i, :] = (3 / h[i]) * (a[i + 1, :] - a[i, :]) - (3 / h[i - 1]) * (a[i, :] - a[i - 1, :])
        
        # Step 5
        c = np.zeros((n + 1, m))
        l = np.zeros((n + 1,))
        mu = np.zeros((n + 1,))
        z = np.zeros((n + 1, m))
        
        # Step 6
        l[0] = 1
        mu[0] = 0
        z[0, :] = 0
        
        # Step 7
        for i in range(1, n):
            l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
            mu[i] = h[i] / l[i]
            z[i, :] = (alpha[i, :] - h[i - 1] * z[i - 1, :]) / l[i]
        
        # Step 8
        l[n] = 1
        z[n, :] = 0
        c[n, :] = 0
        
        # Step 9
        for j in range(n - 1, -1, -1):
            c[j, :] = z[j, :] - mu[j] * c[j + 1, :]
            b[j, :] = (a[j + 1, :] - a[j, :]) / h[j] - (h[j] * (c[j + 1, :] + 2 * c[j, :])) / 3
            d[j, :] = (c[j + 1, :] - c[j, :]) / (3 * h[j])
        
        # Step 10
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
        self.x = x
        self.y = y 
        
    
    def __call__(self):
        n = self.y.shape[0]
        m = self.y.shape[1]
        return call(n, m, self.a, self.b, self.c, self.d, self.x)
        
            
        
        
        
if __name__ == "__main__":
    N = 200
    y = np.zeros((N + 1, 2))
    for i in range(N + 1):
        y[i, :] = np.array([np.cos(6 * np.pi * i / N), np.sin(8 * np.pi * i / N)])
    MCS = MyCubicSpline(y)
    tau, curve = MCS()
    plt.plot(curve[:, 0], curve[:, 1])
    
    #plt.plot(B[:, 0], B[:, 1])
    plt.scatter(y[:, 0], y[:, 1], 5, color='r')

    plt.figure()

    plt.plot(tau, curve[:, 0])
    plt.plot(tau, curve[:, 1])
    plt.show()