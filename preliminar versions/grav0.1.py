#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sympy as sp

# Definir constantes gravitatorias
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Definir ecuaciones diferenciales del sistema gravitatorio de tres cuerpos
def sistema_gravitatorio(y, t):
    # Desempaquetar posiciones y velocidades
    x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3 = y

    # Calcular distancias entre los cuerpos
    r12 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    r13 = np.sqrt((x3 - x1)**2 + (y3 - y1)**2)
    r23 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2)

    # Calcular aceleraciones
    ax1 = G * (m2 * (x2 - x1) / r12**3 + m3 * (x3 - x1) / r13**3)
    ay1 = G * (m2 * (y2 - y1) / r12**3 + m3 * (y3 - y1) / r13**3)

    ax2 = G * (m1 * (x1 - x2) / r12**3 + m3 * (x3 - x2) / r23**3)
    ay2 = G * (m1 * (y1 - y2) / r12**3 + m3 * (y3 - y2) / r23**3)

    ax3 = G * (m1 * (x1 - x3) / r13**3 + m2 * (x2 - x3) / r23**3)
    ay3 = G * (m1 * (y1 - y3) / r13**3 + m2 * (y2 - y3) / r23**3)

    return [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2, vx3, vy3, ax3, ay3]

# Parámetros del sistema
m1 = 1.0e10  # Masa del primer cuerpo en kg
m2 = 1.0e10  # Masa del segundo cuerpo en kg
m3 = 1.0e10  # Masa del tercer cuerpo en kg

# Condiciones iniciales
y0 = [1, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, -1]  # [x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3]

# Tiempo de integración
tiempo = np.linspace(0, 10, 1000)

# Resolver ecuaciones diferenciales usando odeint
solucion = odeint(sistema_gravitatorio, y0, tiempo)

# Graficar la trayectoria de los cuerpos
plt.figure(figsize=(8, 8))
plt.plot(solucion[:, 0], solucion[:, 1], label='Cuerpo 1')
plt.plot(solucion[:, 4], solucion[:, 5], label='Cuerpo 2')
plt.plot(solucion[:, 8], solucion[:, 9], label='Cuerpo 3')
plt.title('Simulación Gravitatoria de Tres Cuerpos')
plt.xlabel('Posición en x (m)')
plt.ylabel('Posición en y (m)')
plt.legend()
plt.show()
