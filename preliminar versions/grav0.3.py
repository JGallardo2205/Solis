#!/usr/bin/python3

import numpy as np
import matplotlib
matplotlib.use('Agg')  # O el backend que sea adecuado para tu sistema
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Datos
UA = 1.496e11  # Unidad astronómica en metros
# Constantes del sistema Marte-Tierra-Venus
M1 = 6.4171e23  # Masa de Marte
M2 = 5.972e24   # Masa Tierra
M3 = 4.867e24   # Masa Venus

G = 6.67430e-11  # Constante gravitacional (m^3 kg^−1 s^−2)

# Condiciones iniciales y no dimensionalización
r1 = 1.52*UA  # posición inicial en coordenadas polares (r, θ)
r2 = 1*UA
r3 = 0.072* UA
v1 = np.array([-29.78, 0.001])  # velocidad inicial en coordenadas polares (dr/dt, dθ/dt)
v2 = np.array([24.07, 0.001])
v3 = np.array([-35.02, 0.001])

# Función de ecuaciones diferenciales en coordenadas polares
def ThreeBodyEquations(t, w):
    r1, theta1, r2, theta2, r3, theta3, r_center_x, r_center_y, dr1dt, dtheta1dt, dr2dt, dtheta2dt, dr3dt, dtheta3dt, dr_center_x_dt, dr_center_y_dt = w

    # Distancias entre los cuerpos
    r12 = np.linalg.norm(np.array([r2 - r1, 0.0]))
    r13 = np.linalg.norm(np.array([r3 - r1, 0.0]))
    r23 = np.linalg.norm(np.array([r3 - r2, 0.0]))

    epsilon = 1e-6  # Pequeño valor para evitar divisiones por distancias cercanas a cero

    # Ecuaciones de aceleración en coordenadas polares
    dv1bydt = (G * M2 / (r12 + epsilon)**3) * np.array([r2 - r1, 0.0]) + \
               (G * M3 / (r13 + epsilon)**3) * np.array([r3 - r1, 0.0])
    dv2bydt = (G * M1 / (r12 + epsilon)**3) * np.array([r1 - r2, 0.0]) + \
               (G * M3 / (r23 + epsilon)**3) * np.array([r3 - r2, 0.0])
    dv3bydt = (G * M1 / (r13 + epsilon)**3) * np.array([r1 - r3, 0.0]) + \
               (G * M2 / (r23 + epsilon)**3) * np.array([r2 - r3, 0.0])

    # Ecuaciones de velocidad en coordenadas polares
    dr1bydt = dr1dt
    dtheta1bydt = dtheta1dt
    dr2bydt = dr2dt
    dtheta2bydt = dtheta2dt
    dr3bydt = dr3dt
    dtheta3bydt = dtheta3dt

    # Añadir las ecuaciones para la posición de la estrella central
    dr_center_x_by_dt = dr_center_x_dt
    dr_center_y_by_dt = dr_center_y_dt

    # Corregir el número de valores de retorno
    return [dr1bydt, dtheta1bydt, dr2bydt, dtheta2bydt, dr3bydt, dtheta3bydt, dr_center_x_by_dt, dr_center_y_by_dt, dv1bydt[0], dv1bydt[1], dv2bydt[0], dv2bydt[1], dv3bydt[0], dv3bydt[1], 0, 0]

# Condiciones iniciales y no dimensionalización
w0 = [r1, 0, r2, 0, r3, 0, 0, 0, v1[0], v1[1], v2[0], v2[1], v3[0], v3[1], 0, 0]
t_span = np.linspace(0, 1, 1000) * 365.25 * 24 * 3600  # convertido a segundos

# Resolución de las ecuaciones diferenciales en coordenadas polares
solution = np.zeros((len(t_span), len(w0)))
solution[0] = w0

for i in range(1, len(t_span)):
    dt = t_span[i] - t_span[i - 1]
    k1 = ThreeBodyEquations(t_span[i - 1], solution[i - 1])
    k2 = ThreeBodyEquations(t_span[i - 1] + dt/2, [solution[i - 1][j] + dt/2 * k1[j] for j in range(len(k1))])
    k3 = ThreeBodyEquations(t_span[i - 1] + dt/2, [solution[i - 1][j] + dt/2 * k2[j] for j in range(len(k2))])
    k4 = ThreeBodyEquations(t_span[i - 1] + dt, [solution[i - 1][j] + dt * k3[j] for j in range(len(k3))])
    solution[i] = [solution[i - 1][j] + dt/6 * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j]) for j in range(len(k4))]

# Extraer resultados en coordenadas polares
r1_sol = np.array([[solution[i][0], solution[i][1]] for i in range(len(solution))])
r2_sol = np.array([[solution[i][2], solution[i][3]] for i in range(len(solution))])
r3_sol = np.array([[solution[i][4], solution[i][5]] for i in range(len(solution))])

# Convertir coordenadas polares a cartesianas para la visualización en 3D
x1_sol = r1_sol[:, 0] * np.cos(r1_sol[:, 1])
y1_sol = r1_sol[:, 0] * np.sin(r1_sol[:, 1])
z1_sol = np.zeros_like(x1_sol)

x2_sol = r2_sol[:, 0] * np.cos(r2_sol[:, 1])
y2_sol = r2_sol[:, 0] * np.sin(r2_sol[:, 1])
z2_sol = np.zeros_like(x2_sol)

x3_sol = r3_sol[:, 0] * np.cos(r3_sol[:, 1])
y3_sol = r3_sol[:, 0] * np.sin(r3_sol[:, 1])
z3_sol = np.zeros_like(x3_sol)

# Función para actualizar la animación
def update(frame, ax, x1, y1, z1, x2, y2, z2, x3, y3, z3):
    ax.cla()
    ax.plot(x1[:frame], y1[:frame], z1[:frame], label="Mars")
    ax.plot(x2[:frame], y2[:frame], z2[:frame], label="Earth")
    ax.plot(x3[:frame], y3[:frame], z3[:frame], label="Venus")
    ax.scatter(x1[frame-1], y1[frame-1], z1[frame-1], color="darkblue", marker="o", s=80, label="Mars")
    ax.scatter(x2[frame-1], y2[frame-1], z2[frame-1], color="darkred", marker="o", s=80, label="Earth")
    ax.scatter(x3[frame-1], y3[frame-1], z3[frame-1], color="goldenrod", marker="o", s=80, label="Venus")
    ax.set_xlabel("x-coordinate", fontsize=14)
    ax.set_ylabel("y-coordinate", fontsize=14)
    ax.set_zlabel("z-coordinate", fontsize=14)
    ax.set_title(f"The three-body problem for the Mars-Earth-Venus system (Frame {frame})", fontsize=14)
    ax.legend(fontsize=12)

# Crear la animación
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")
animation = FuncAnimation(fig, update, frames=len(t_span), fargs=(ax, x1_sol, y1_sol, z1_sol, x2_sol, y2_sol, z2_sol, x3_sol, y3_sol, z3_sol))

# Asignar la animación a una variable
anim = animation
# Mostrar la animación en el entorno de IPython/Jupyter Notebook
HTML(animation.to_jshtml())


  


