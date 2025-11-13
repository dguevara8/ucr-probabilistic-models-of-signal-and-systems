import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar la base de datos SQLite
db_path = 'night.db'

# Leer los datos de la tabla 'test_data'
with sqlite3.connect(db_path) as conn:
    df = pd.read_sql_query("SELECT * FROM test_data;", conn)

# Crear una nueva columna que representa los minutos desde la medianoche
df['minutes_since_midnight'] = (
                                    pd.to_datetime(
                                        df['timestamp']
                                        ).dt.hour * 60 +
                                    pd.to_datetime(
                                        df['timestamp']
                                        ).dt.minute
                                )
# Calcular el cuadrado de la variable para la potencia promedio
df['data_squared'] = df['data'] ** 2

# Calcular la potencia promedio
average_power = np.mean(df['data_squared'])
print(f"Potencia promedio: {average_power:.8f}")

# Número de puntos de la señal
N = len(df)

# Calcular el intervalo de tiempo (dT) en segundos
df['time_diff'] = df['minutes_since_midnight'].diff()
df_filtered = df[df['time_diff'] > 0]  # Filtrar valores únicos
df_filtered = df_filtered.drop(columns='time_diff')
dT = (
    df_filtered['minutes_since_midnight'].iloc[1] -
    df_filtered['minutes_since_midnight'].iloc[0]
) * 60

# Variable de interés
variable = df_filtered['data'].values

# Transformada de Fourier
fft_result = np.fft.fft(variable)
n = len(df_filtered)
frequencies = np.fft.fftfreq(n, d=dT)

# Densidad espectral de potencia (PSD)
psd = np.abs(fft_result)**2 / (n * dT)

plt.figure(figsize=(10, 6))
plt.plot(frequencies[:n//2], psd[:n//2])  # Solo mostrar frecuencias positivas
plt.ylim(0, 50)  # Límite máximo del eje vertical
plt.title('Densidad Espectral de Potencia (PSD)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Potencia')
plt.grid(True)

# Guardar la gráfica como un archivo de imagen
output_path = 'grafica_densidadespectral_night.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

# Mostrar mensaje de éxito
print(f'Gráfica guardada en: {output_path}')
