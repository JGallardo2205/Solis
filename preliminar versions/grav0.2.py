#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

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
m1 = 2.0e10  # Masa del primer cuerpo en kg
m2 = 1.0e10  # Masa del segundo cuerpo en kg
m3 = 9.0e10  # Masa del tercer cuerpo en kg

# Condiciones iniciales
y0 = [1, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, -1]  # [x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3]

# Tiempo de integración
tiempo = np.linspace(0, 10, 1000)

# Configuración de la figura
fig, ax = plt.subplots(figsize=(8, 8))
cuerpo1, = ax.plot([], [], 'bo', markersize=10)
cuerpo2, = ax.plot([], [], 'go', markersize=10)
cuerpo3, = ax.plot([], [], 'ro', markersize=10)

ax.set_xlim(-2, 2)  # Ajusta los límites según tus necesidades
ax.set_ylim(-2, 2)

# Función de inicialización para la animación
def init():
    cuerpo1.set_data([], [])
    cuerpo2.set_data([], [])
    cuerpo3.set_data([], [])
    return cuerpo1, cuerpo2, cuerpo3

# Función de actualización para la animación
def update(frame):
    # Resolver ecuaciones diferenciales usando odeint
    solucion_frame = odeint(sistema_gravitatorio, y0, [0, frame])

    # Actualizar posiciones de los cuerpos
    cuerpo1.set_data(solucion_frame[:, 0], solucion_frame[:, 1])
    cuerpo2.set_data(solucion_frame[:, 4], solucion_frame[:, 5])
    cuerpo3.set_data(solucion_frame[:, 8], solucion_frame[:, 9])

    return cuerpo1, cuerpo2, cuerpo3

# Crear la animación
ani = FuncAnimation(fig, update, frames=tiempo, init_func=init, blit=True)

plt.title('Simulación Gravitatoria de Tres Cuerpos')
plt.xlabel('Posición en x (m)')
plt.ylabel('Posición en y (m)')
plt.show()
