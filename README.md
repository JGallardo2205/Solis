# Solis

Este código tiene como objetivo simular el sistema solar, incluyendo los cuatro gigantes gaseosos y el Sol, mediante el método numérico de Runge-Kutta de cuarto orden. En el proceso de formulación, se han adoptado aproximaciones basadas en condiciones iniciales específicas.

## Configuración inicial

En el instante inicial (t=0), se ha configurado el sistema solar en una disposición alineada, lo que resulta en una velocidad inicial con una componente casi nula. Para corregir este aspecto y obtener una aproximación más precisa a las órbitas reales, se ha ajustado esta velocidad inicial a un valor cercano a cero.

En el contexto de este proyecto de simulación, se implementaron ajustes específicos en las condiciones iniciales del Sol para garantizar que el sistema solar orbite alrededor de un centro de masa común.

### Sol

Para lograr que el sistema de planetas orbite alrededor del centro de masa, se realizaron los siguientes ajustes en las condiciones iniciales del Sol:

#### Posición Inicial

Se eligió una posición inicial para el Sol que desplaza el centro de masa del sistema. En este caso, la posición inicial del Sol se estableció en \(x = -1.5 \times 10^{12}\) metros, \(y = 0\), \(z = 0\). Este ajuste asegura que el centro de masa del sistema no esté ubicado en el centro del Sol, lo que permite el movimiento orbital de los planetas.

#### Velocidad Inicial

Para compensar el cambio en la posición del centro de masa, se asignó una velocidad inicial al Sol en la dirección \(y\). Esta velocidad se ajustó para que el momento lineal del Sol fuera igual y opuesto al momento lineal combinado de los planetas. La velocidad inicial en \(y\) se estableció en \(1 \times 10^{4}\) metros por segundo.

Estos ajustes trabajan en conjunto para mantener el equilibrio dinámico del sistema, permitiendo que los planetas orbiten alrededor del centro de masa ajustado.

La masa del Sol se mantiene en su valor realista de \(1.989 \times 10^{30}\) kilogramos.

### Planetas

Las condiciones iniciales para los planetas (Uranus, Neptune, Saturn, Jupiter) se proporcionaron con valores realistas de posición, velocidad y masa.

## Ecuaciones y Método Numérico

El código utiliza el método de Runge-Kutta de cuarto orden para resolver las ecuaciones diferenciales que describen el movimiento de los planetas. La función `planetary_system` define el sistema de ecuaciones diferenciales, y se considera la masa y la dirección de la fuerza entre los planetas.

## Parámetros de la Simulación

- Duración total de la simulación: 500 años
- Paso de tiempo: (6 horas)

## Dependencias

- NumPy
- Matplotlib
- IPython
- mpl_toolkits
## Ejecución del Código

El código puede ejecutarse en un entorno de Python con las dependencias instaladas. Se recomienda utilizar un entorno virtual para gestionar las dependencias.

```bash
pip install numpy matplotlib
python nombre_del_archivo.py
