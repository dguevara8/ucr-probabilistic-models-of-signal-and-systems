import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ruta a la base de datos proporcionada
db_path = 'estacionalidad_day.db'

# Cargar los datos de la base de datos
conn = sqlite3.connect(db_path)
query = (
    "SELECT timestamp, data FROM filtered_sampled_data_with_autocorrelation;"
)
df_sampled = pd.read_sql_query(query, conn)
conn.close()

# Convertir 'timestamp' a tipo datetime
df_sampled['timestamp'] = pd.to_datetime(df_sampled['timestamp'])

# Calcular los minutos desde la medianoche
df_sampled['minutes_from_midnight'] = (
    df_sampled['timestamp'].dt.hour * 60 +
    df_sampled['timestamp'].dt.minute +
    df_sampled['timestamp'].dt.second / 60
)

# Ordenar los datos por minutos desde la medianoche
df_sampled = df_sampled.sort_values(by='minutes_from_midnight')

# Determinar los límites del eje X
x_min = df_sampled['minutes_from_midnight'].min() - 50
x_max = df_sampled['minutes_from_midnight'].max() + 50

# Graficar los datos
plt.figure(figsize=(12, 6))
plt.plot(
    df_sampled['minutes_from_midnight'], df_sampled['data'],
    marker='o', linestyle='-', label='Data (Muestreada)'
)
plt.xlabel('Tiempo (minutos desde la medianoche)', fontsize=12)
plt.ylabel('Data', fontsize=12)
plt.title(
    'Gráfica de Data vs Tiempo en Minutos (Desde las 9:42 AM)', fontsize=14
    )

# Ajustar los límites del eje X
plt.xlim(x_min, x_max)

# Ajustar la escala del eje Y
y_min = df_sampled['data'].min() - 3
y_max = df_sampled['data'].max() + 3
plt.ylim(y_min, y_max)

# Etiquetas personalizadas del eje X en minutos desde la medianoche
tick_positions = range(int(x_min), int(x_max) + 1, 120)
tick_labels = [f"{int(tick)}" for tick in tick_positions]
plt.xticks(tick_positions, tick_labels)

plt.grid(True)
plt.legend()
plt.tight_layout()

# Guardar la gráfica en un archivo
output_path = Path('grafica_estacionalidad_dia.png')
plt.savefig(output_path, format='png')
plt.close()

print(f"Gráfica guardada en: {output_path}")
