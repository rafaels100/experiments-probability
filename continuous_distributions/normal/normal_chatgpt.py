import numpy as np
import matplotlib.pyplot as plt

# Distribución normal con media mu y desviación sigma
def f(x, sigma, mu):
    return (1 / (sigma * np.sqrt(2*np.pi))) * np.exp(-((x - mu)**2) / (2 * sigma**2))

# Distribución normal estándar N(0, 1)
def f_z(x):
    return (1 / np.sqrt(2*np.pi)) * np.exp(-x**2 / 2)

# Parámetros
sigma = 4
mu = 18
x_vals = np.linspace(14, 22, 1000)

# Evaluación directa con fórmula general
f_x_def = f(x_vals, sigma, mu)

# Usar normal estándar, ajustada con cambio de variable z = (x - mu) / sigma
f_x_por_z = f_z((x_vals - mu) / sigma) / sigma  # IMPORTANTE: dividir por sigma para escalar correctamente

# Visualización
plt.plot(x_vals, f_x_def, label="f(x) directa")
plt.plot(x_vals, f_x_por_z, '--', label="f(x) por normal estándar")
plt.legend()
plt.show()

