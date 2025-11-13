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
