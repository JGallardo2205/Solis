#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import ode

# Parámetros gravitatorios
G = 6.67430e-11  # Constante gravitatoria
m_solar = 1.989e30  # Masa del Sol
m_tierra = 5.972e24  # Masa de la Tierra
m_jupiter = 1.898e27  # Masa de Júpiter

# Condiciones iniciales (posiciones y velocidades)
initial_conditions = np.array([[-147_095_000_000.0, 0, 0],  # Posición inicial de la Tierra (metros)
                                [0, 0, 0],  # Velocidad inicial de la Tierra (metros/segundo)
                                [0, 778_340_821_000.0, 0],  # Posición inicial de Júpiter (metros)
                                [-13_064.8, 0, 0]])  # Velocidad inicial de Júpiter (metros/segundo)

# Función que define el sistema de ecuaciones diferenciales
def gravitation(t, y, G, m1, m2, m3):
    r1 = np.sqrt(y[0]**2 + y[1]**2 + y[2]**2)
    r2 = np.sqrt((y[0] - y[6])**2 + (y[1] - y[7])**2 + (y[2] - y[8])**2)
    r3 = np.sqrt((y[0] - y[12])**2 + (y[1] - y[13])**2 + (y[2] - y[14])**2)

    dydt = np.zeros_like(y)

    dydt[0:3] = y[3:6]  # Derivadas de las posiciones son las velocidades actuales
    dydt[6:9] = y[9:12]  # Derivadas de las posiciones son las velocidades actuales
    dydt[12:15] = y[15:18]  # Derivadas de las posiciones son las velocidades actuales

    # Ecuaciones de movimiento para la Tierra
    dydt[3:6] = -G * m_solar * y[0:3] / r1**3 - G * m_jupiter * (y[0:3] - y[6:9]) / r2**3

    # Ecuaciones de movimiento para Júpiter
    dydt[9:12] = -G * m_solar * (y[6:9] - y[0:3]) / r2**3 - G * m_tierra * (y[6:9] - y[12:15]) / r3**3

    # Ecuaciones de movimiento para el sistema Tierra-Júpiter
    dydt[15:18] = -G * m_solar * (y[12:15] - y[0:3]) / r3**3 - G * m_tierra * (y[12:15] - y[6:9]) / r2**3

    return dydt

# Configuración de la animación
num_frames = 1000
dt = 24 * 3600  # Paso de tiempo en segundos (un día)
solver = ode(gravitation).set_integrator('dopri5')
solver.set_initial_value(initial_conditions.flatten(), 0).set_f_params(G, m_solar, m_tierra, m_jupiter)

# Configuración de la gráfica
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    global solver
    solver.integrate(solver.t + dt)
    positions = solver.y.reshape((-1, 3))
    ax.cla()
    ax.set_xlim([-2e11, 2e11])
    ax.set_ylim([-2e11, 2e11])
    ax.set_zlim([-2e11, 2e11])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Sistema Gravitatorio de 3 Cuerpos')

    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], marker='o', label='Cuerpos')
    return ax

# Crear la animación
ani = FuncAnimation(fig, update, frames=num_frames, blit=False)

# Mostrar la animación
plt.show()
