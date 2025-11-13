# Densidad de probabilidad
## Densidad de probabilidad de día
### Ecuación de distribución
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante el día para determinar la distribución. A continuación se describe el código.
```python
import sqlite3
import pandas as pd
from fitter import Fitter
import matplotlib.pyplot as plt

# Conexión a la base de datos SQLite
conn = sqlite3.connect('day.db')

# Cargar los datos desde la tabla "test_data" y la columna "data"
query = "SELECT data FROM test_data"
data = pd.read_sql_query(query, conn)["data"].dropna()

# Cerrar la conexión
conn.close()

# Convertir los datos a tipo numérico si no lo son
data = pd.to_numeric(data, errors='coerce').dropna()

# Definir las distribuciones a evaluar
distribuciones = ['expon', 'gompertz', 'levy', 'logistic', 'norm', 'rayleigh']

# Ajustar las distribuciones con Fitter
f = Fitter(data, distributions=distribuciones)
f.fit()

# Obtener la mejor distribución y sus parámetros
best_fit = f.get_best()

# Imprimir los resultados
print("Mejor distribución encontrada:")
print(best_fit)

# Graficar las distribuciones ajustadas
f.summary()
plt.show()
```
![Texto alternativo](img/grafica_mejordistribucion_dia.png "Gráfica de la mejor distribución para el día")
Ecuación de distribución logística:

$$
\frac{e^{-\frac{(t-\mu(t))}{s(t)}}}{s(t)\left(1 + e^{-\frac{(t-\mu(t))}{s(t)}}\right)^2}
$$

### Distribución logística de día
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante el día para determinar los parámetros de scale. A continuación se describe el código.
```python
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ruta del script y configuración para guardar imágenes
script_dir = Path(__file__).parent

# Conectar a la base de datos
database_path = 'parameters_day.db'
connection = sqlite3.connect(database_path)

# Leer los datos desde la base de datos
query = "SELECT * FROM parameters"
data_frame = pd.read_sql_query(query, connection)

# Convertir 'timestamp' a un objeto datetime
data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'])

# Calcular los minutos desde la medianoche
data_frame['minutes_from_midnight'] = (
    data_frame['timestamp'].dt.hour * 60 +
    data_frame['timestamp'].dt.minute +
    data_frame['timestamp'].dt.second / 60
)

# Filtrar los datos en los intervalos de tiempo especificados
morning_data = data_frame[
    (
        data_frame['timestamp'].dt.time >=
        pd.to_datetime('06:00:00').time()
    ) &
    (
        data_frame['timestamp'].dt.time <
        pd.to_datetime('09:42:00').time()
    )
]
day_data = data_frame[
    (
        data_frame['timestamp'].dt.time >=
        pd.to_datetime('09:42:00').time()
    ) &
    (
        data_frame['timestamp'].dt.time <=
        pd.to_datetime('18:00:00').time()
    )
]

# Combinar los datos filtrados
filtered_data = pd.concat([morning_data, day_data])

# Graficar los datos para 'loc'
plt.figure(figsize=(12, 6))
plt.scatter(
    filtered_data['minutes_from_midnight'],
    filtered_data['loc'],
    c='blue',
    alpha=0.7,
    label='Datos (loc)'
)

# Realizar ajuste polinómico de segundo grado para 'loc'
coefficients_loc = np.polyfit(
    filtered_data['minutes_from_midnight'], filtered_data['loc'], 2
    )
polynomial_fit_loc = np.poly1d(coefficients_loc)

# Crear valores ajustados para la curva de 'loc'
x_values = np.linspace(
    filtered_data['minutes_from_midnight'].min(),
    filtered_data['minutes_from_midnight'].max(),
    1000
)
y_values_loc = polynomial_fit_loc(x_values)

# Graficar la curva ajustada para 'loc'
plt.plot(
    x_values,
    y_values_loc,
    'r-',
    label=(
        f"Ajuste polinómico (loc): "
        f"$y = {coefficients_loc[0]:.8f}x^2 + "
        f"{coefficients_loc[1]:.8f}x + "
        f"{coefficients_loc[2]:.8f}$"
    )
)

# Configurar etiquetas y título para 'loc'
plt.xlabel('Minutos desde la medianoche')
plt.ylabel('Valores de la media (loc)')
plt.title('Media de datos (loc) por minuto desde la medianoche')
plt.legend()
plt.grid(True)

# Guardar la gráfica
output_path_loc = script_dir / 'grafica_loc_dia.png'
plt.savefig(output_path_loc, format='png')
print(
    f"Gráfica 'loc' guardada en: {output_path_loc}"
    )
plt.close()

# Graficar los datos para 'scale'
plt.figure(figsize=(12, 6))
plt.scatter(
    filtered_data['minutes_from_midnight'],
    filtered_data['scale'],
    c='green',
    alpha=0.7,
    label='Datos (scale)'
)

# Realizar ajuste polinómico de segundo grado para 'scale'
coefficients_scale = np.polyfit(
    filtered_data['minutes_from_midnight'],
    filtered_data['scale'],
    2
)
polynomial_fit_scale = np.poly1d(coefficients_scale)

# Crear valores ajustados para la curva de 'scale'
y_values_scale = polynomial_fit_scale(x_values)

# Graficar la curva ajustada para 'scale'
plt.plot(
    x_values,
    y_values_scale,
    'r-',
    label=(
        f"Ajuste polinómico (scale): "
        f"$y = {coefficients_scale[0]:.8f}x^2 + "
        f"{coefficients_scale[1]:.8f}x + "
        f"{coefficients_scale[2]:.8f}$"
    )
)

# Configurar etiquetas y título para 'scale'
plt.xlabel('Minutos desde la medianoche')
plt.ylabel('Valores de la desviación estándar (scale)')
plt.title(
    "Desviación estándar de datos (scale) "
    "por minuto desde la medianoche"
)
plt.legend()
plt.grid(True)

# Guardar la gráfica
output_path_scale = script_dir / 'grafica_scale_dia.png'
plt.savefig(output_path_scale, format='png')
print(f"Gráfica 'scale' guardada en: {output_path_scale}")
plt.close()

# Cerrar la conexión a la base de datos
connection.close()
```
![Texto alternativo](img/grafica_loc_dia.png "Gráfica del parámetro loc para el día")
![Texto alternativo](img/grafica_scale_dia.png "Gráfica del parámetro scale para el día")

### Ecuación distribución logística de día

$$
\frac{e^{-\frac{(t-\mu_{day}(t))}{s_{day}(t)}}}{s_{day}(t)\left(1 + e^{-\frac{(t-\mu_{day}(t))}{s_{day}(t)}}\right)^2}
$$

Con una función para $\mu_{day}$(t):

$$
\mu_{day}(t)=-0.00003094t^2 + 0.04453403t - 12.02212940
$$

Con una función para $s_{day}$(t):

$$
s_{day}(t)=-0.00001530t^2+0.02204914t-4.96314783
$$

Mediante el ajuste de la distribución logística para los datos diurnos revela un comportamiento caracterizado por variaciones significativas a lo largo del tiempo. El uso del paquete Fitter permitió determinar que la distribución logística era la mejor para modelar los datos, lo cual sugiere una tendencia a la concentración de valores cercanos al promedio, pero con colas moderadamente largas que reflejan la presencia de eventos extremos. La incorporación de las funciones $\mu_{day}(t)$ y $s_{day}(t)$, que varían con el tiempo, fue esencial para capturar adecuadamente la naturaleza dinámica de los datos diurnos, mostrando cómo la media y la dispersión evolucionan a lo largo del día.

La forma cuadrática de ambas funciones indica que los datos presentan una variabilidad más alta hacia el mediodía, alcanzando un máximo en el rango central del día (entre 6:00 AM y 6:00 PM) antes de decrecer nuevamente. Este comportamiento es consistente con las gráficas previas, donde se observó mayor amplitud y dispersión en este periodo. La parametrización dinámica de la distribución logística proporciona una representación más precisa y permite analizar cómo los factores externos influyen en la estabilidad y concentración de los valores diurnos. Este modelo es útil para predecir patrones o evaluar la relación entre el tiempo y las características del sistema en estudio.

Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante la noche para determinar la distribución. A continuación se describe el código.
```python
import sqlite3
import pandas as pd
from fitter import Fitter
import matplotlib.pyplot as plt

# Conexión a la base de datos SQLite
conn = sqlite3.connect('night.db')

# Cargar los datos desde la tabla "test_data" y la columna "data"
query = "SELECT data FROM test_data"
data = pd.read_sql_query(query, conn)["data"].dropna()

# Cerrar la conexión
conn.close()

# Convertir los datos a tipo numérico si no lo son
data = pd.to_numeric(data, errors='coerce').dropna()

# Definir las distribuciones a evaluar
distribuciones = ['expon', 'gompertz', 'levy', 'logistic', 'norm', 'rayleigh']

# Ajustar las distribuciones con Fitter
f = Fitter(data, distributions=distribuciones)
f.fit()

# Obtener la mejor distribución y sus parámetros
best_fit = f.get_best()

# Imprimir los resultados
print("Mejor distribución encontrada:")
print(best_fit)

# Graficar las distribuciones ajustadas y guardar el gráfico
f.summary()

# Guardar el gráfico en un archivo PNG
plt.savefig("grafica_mejordistribucion_noche.png", dpi=300)

# Mostrar el gráfico en pantalla
plt.show()
```
## Densidad de probabilidad de noche
![Texto alternativo](img/grafica_mejordistribucion_noche.png "Gráfica de la mejor distribución para la noche")

### Distribución logística de noche
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante la noche para determinar los parámetros location y scale. A continuación se describe el código.
```python
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ruta del script y configuración para guardar imágenes
script_dir = Path(__file__).parent

# Conectar a la base de datos
database_path = 'parameters_night.db'
connection = sqlite3.connect(database_path)

# Leer los datos desde la base de datos
query = "SELECT * FROM parameters"
data_frame = pd.read_sql_query(query, connection)

# Convertir 'timestamp' a un objeto datetime
data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'])

data_frame['minutes_from_midnight'] = (
    data_frame['timestamp'].dt.hour * 60 +
    data_frame['timestamp'].dt.minute +
    data_frame['timestamp'].dt.second / 60
)
data_frame[
    'minutes_from_midnight'
    ] = data_frame['minutes_from_midnight'].apply(
    lambda x: x if x >= 1080 else x + 1440
)

# Filtrar los datos en los intervalos de tiempo especificados (18:00 a 6:00)
filtered_data = data_frame[
    (data_frame['minutes_from_midnight'] >= 1080) | (
        data_frame['minutes_from_midnight'] < 360
        )
    ]

# Graficar los datos para 'loc'
plt.figure(figsize=(12, 6))
plt.scatter(
    filtered_data[
        'minutes_from_midnight'
        ], filtered_data[
            'loc'
            ], c='blue', alpha=0.7, label='Datos (loc)'
    )

# Realizar ajuste polinómico de segundo grado para 'loc'
coefficients_loc = np.polyfit(
    filtered_data[
        'minutes_from_midnight'
        ], filtered_data['loc'], 2
    )
polynomial_fit_loc = np.poly1d(coefficients_loc)

# Crear valores ajustados para la curva de 'loc'
x_values = np.linspace(
    filtered_data[
        'minutes_from_midnight'
        ].min(), filtered_data[
            'minutes_from_midnight'
            ].max(), 1000
    )
y_values_loc = polynomial_fit_loc(x_values)

# Graficar la curva ajustada para 'loc'
plt.plot(
    x_values,
    y_values_loc,
    'r-',
    label=(
        f"Ajuste polinómico (loc): "
        f"$y = {coefficients_loc[
            0
            ]:.8f}x^2 + {coefficients_loc[
                1
                ]:.8f}x + {coefficients_loc[
                    2
                    ]:.8f}$"
    )
)


# Configurar etiquetas y título para 'loc'
plt.xlabel('Minutos desde la medianoche (ajustados)')
plt.ylabel('Valores de la media (loc)')
plt.title('Media de datos (loc) por minuto desde la medianoche (18:00-06:00)')
plt.legend()
plt.grid(True)

# Guardar la gráfica
output_path_loc = script_dir / 'grafica_loc_noche.png'
plt.savefig(output_path_loc, format='png')
print(f"Gráfica 'loc' guardada en: {output_path_loc}")
plt.close()

# Graficar los datos para 'scale'
plt.figure(figsize=(12, 6))
plt.scatter(
    filtered_data[
        'minutes_from_midnight'
        ], filtered_data[
            'scale'
            ], c='green', alpha=0.7, label='Datos (scale)'
    )

# Realizar ajuste polinómico de segundo grado para 'scale'
coefficients_scale = np.polyfit(
    filtered_data[
        'minutes_from_midnight'
        ], filtered_data['scale'], 2
    )
polynomial_fit_scale = np.poly1d(coefficients_scale)

# Crear valores ajustados para la curva de 'scale'
y_values_scale = polynomial_fit_scale(x_values)

# Graficar la curva ajustada para 'scale'
plt.plot(
    x_values,
    y_values_scale,
    'r-',
    label=(
        f"Ajuste polinómico (scale): "
        f"$y = {coefficients_scale[0]:.8f}x^2 + "
        f"{coefficients_scale[1]:.8f}x + "
        f"{coefficients_scale[2]:.8f}$"
    )
)

# Configurar etiquetas y título para 'scale'
plt.xlabel('Minutos desde la medianoche (ajustados)')
plt.ylabel('Valores de la desviación estándar (scale)')
plt.title(
    "Desviación estándar de datos (scale) "
    "por minuto desde la medianoche "
    "(18:00-06:00)"
)
plt.legend()
plt.grid(True)

# Guardar la gráfica
output_path_scale = script_dir / 'grafica_scale_noche.png'
plt.savefig(output_path_scale, format='png')
print(f"Gráfica 'scale' guardada en: {output_path_scale}")
plt.close()

# Cerrar la conexión a la base de datos
connection.close()
```
![Texto alternativo](img/grafica_loc_noche.png "Gráfica del parámetro loc para la noche")
![Texto alternativo](img/grafica_scale_noche.png "Gráfica del parámetro scale para la noche")

### Ecuación distribución logística de noche


$$
\frac{e^{-\frac{(t-\mu_{night}(t))}{s_{night}(t)}}}{s_{night}(t)\left(1 + e^{-\frac{(t-\mu_{night}(t))}{s_{night}(t)}}\right)^2}
$$

Con una función para $\mu_{night}$(t):

$$
\mu_{day}(t)=0.00000004t^2 - 0.00013611t + 0.09892365
$$

Con una función para $s_{night}$(t):

$$
s_{day}(t)=-0.00000003t^2 - 0.00008501t + 1.05349743
$$

El análisis de la distribución logística de los datos nocturnos, utilizando el paquete Fitter y ajustando las funciones $\mu_{night}(t)$ y $s_{day}(t)$, destaca una estabilidad notable a lo largo del periodo nocturno (de 6:00 PM a 6:00 AM). La función $\mu_{night}(t)$, que modela la media, muestra cambios mínimos en el tiempo, con una tendencia casi constante alrededor de valores cercanos a cero. Esto sugiere que los datos presentan una menor variabilidad en sus valores promedio, lo que podría reflejar la ausencia de eventos externos significativos que alteren el comportamiento del sistema en este periodo.

Por otro lado, la función $s_{night}(t)$, que representa la desviación estándar, también muestra variaciones muy pequeñas, manteniéndose casi constante en torno a un valor cercano a 1. Esto indica una dispersión reducida y consistente, lo que refuerza la idea de que los datos nocturnos son más estables en comparación con los diurnos. En general, el modelo logístico ajustado refleja adecuadamente la homogeneidad de los datos nocturnos, lo que lo hace ideal para predecir comportamientos y analizar la dinámica base del sistema durante este intervalo de tiempo.

## Conclusiones
El análisis presentado revela comportamientos diferenciados entre los datos diurnos y nocturnos, ajustados mediante distribuciones logísticas. Durante el día, la distribución logística muestra variaciones significativas, con una amplitud máxima hacia el mediodía y una menor dispersión en los extremos. Las funciones de location $\mu_{day}(t)$ y escala $s_{day}(t)$ siguen patrones cuadráticos, reflejando una dinámica activa y la influencia de factores externos, lo que genera una mayor amplitud y dispersión en comparación con el período nocturno.

Por otro lado, durante la noche, los datos presentan una estabilidad notable con una media $\mu_{night}(t)$ casi constante y una dispersión $s_{night}(t)$ homogénea, reflejando la ausencia de eventos externos significativos. Esto sugiere que las condiciones nocturnas son más controladas y menos dinámicas. En conjunto, los modelos logísticos ajustados permiten capturar la evolución temporal y las características diferenciadas del sistema en ambos períodos, proporcionando una herramienta efectiva para analizar la influencia de factores externos y predecir comportamientos futuros.