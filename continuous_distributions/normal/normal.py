import numpy as np
import matplotlib.pyplot as plt


def f(x, sigma, mu):
    return (1 / (sigma * np.sqrt(2*np.pi))) * np.exp(-((x - mu)**2) / (2 * sigma**2))

"""
x_ = np.linspace(14, 22, 1000)
y_ = f(x_, 4, 18)
plt.plot(x_, y_)
plt.show()
"""

def f_z(x):
    return (1 / np.sqrt(2*np.pi)) * np.exp(-(x)**2 / 2)
"""
x_ = np.linspace(-5, 5, 1000)
y_ = z(x_)
plt.plot(x_, y_)
plt.show()
"""

def g(x, mu, sigma):
    return (x - mu)/sigma

sigma = 4
mu = 18
x_ = np.linspace(14, 22, 1000)
f_x_def = f(x_, sigma, mu)
f_x_por_z = f_z(g(x_, mu, sigma)) * 1 / sigma

plt.plot(x_, f_x_def)
plt.plot(x_, f_x_por_z)
plt.show()
