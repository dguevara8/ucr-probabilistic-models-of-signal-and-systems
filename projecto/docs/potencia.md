# Potencia promedio
## Potencia promedio de día
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante el día para determinar la densidad espectral de potencia. A continuación se describe el código.
```python
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar la base de datos SQLite
db_path = 'day.db'

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
output_path = 'grafica_densidadespectral_day.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

# Mostrar mensaje de éxito
print(f'Gráfica guardada en: {output_path}')
```
![Texto alternativo](img/grafica_densidadespectral_day.png "Gráfica densidad espectral día")
## Potencia promedio de noche
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante la noche para determinar la densidad espectral de potencia. A continuación se describe el código.
```python
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
```
![Texto alternativo](img/grafica_densidadespectral_night.png "Gráfica densidad espectral noche")
## Potencia promedio de día y de noche

| Tiempo | Potencia promedio |
|--------|--------------------|
| Día    | 27.58278500       |
| Noche  | 3.27397432        |

El análisis de la densidad espectral de potencia (PSD) revela diferencias significativas entre los datos diurnos y nocturnos. En la primera gráfica, correspondiente al día, se observa un pico dominante cerca de la frecuencia cero, lo que indica una gran concentración de energía en componentes de muy baja frecuencia, posiblemente relacionadas con tendencias a largo plazo o variaciones lentas en los datos. Además, existen componentes más dispersas en el espectro, lo que sugiere la presencia de oscilaciones o eventos que afectan el sistema durante el día. La potencia promedio calculada para el día (27.58) refleja una actividad energética considerablemente más alta en comparación con la noche.

En contraste, la segunda gráfica, correspondiente a la noche, muestra una PSD mucho más plana y con valores significativamente más bajos. Esto indica que los datos nocturnos tienen menor energía, menor variabilidad y son menos influenciados por eventos de alta amplitud o dinámicas externas. La potencia promedio nocturna (3.27) confirma esta estabilidad y menor actividad. Estas diferencias entre el día y la noche son coherentes con las observaciones previas de mayor estabilidad y menor dispersión en los datos nocturnos, mientras que los datos diurnos presentan mayor dinamismo y oscilaciones más marcadas.

## Conclusiones
El análisis de la densidad espectral de potencia (PSD) destaca diferencias clave entre los períodos diurnos y nocturnos. Durante el día, se observa una mayor concentración de energía en frecuencias bajas, reflejando variaciones lentas y una actividad energética elevada, como lo evidencia la potencia promedio más alta (27.58). Esto sugiere la influencia de dinámicas externas y eventos que afectan al sistema. En contraste, durante la noche, la PSD es más plana, con menor concentración de energía y una potencia promedio significativamente menor (3.27), lo que indica una mayor estabilidad y menor variabilidad en las condiciones nocturnas. Estos resultados confirman que el sistema presenta una actividad más dinámica durante el día y mayor homogeneidad durante la noche.