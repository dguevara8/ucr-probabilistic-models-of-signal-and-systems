import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ruta del script y configuración para guardar imágenes
script_dir = Path(__file__).parent

# Ruta a la base de datos muestreada
new_db_path = 'estacionalidad_night.db'

# Cargar los datos de la nueva base de datos
conn = sqlite3.connect(new_db_path)
query = "SELECT timestamp, data FROM sampled_data;"
df_sampled = pd.read_sql_query(query, conn)
conn.close()

# Convertir 'timestamp' a tipo datetime
df_sampled['timestamp'] = pd.to_datetime(df_sampled['timestamp'])

# Calcular los minutos desde la medianoche, ajustados para 18:00 a 6:00
df_sampled['minutes_from_midnight'] = (
    df_sampled['timestamp'].dt.hour * 60 +
    df_sampled['timestamp'].dt.minute +
    df_sampled['timestamp'].dt.second / 60
)
df_sampled[
    'minutes_from_midnight'
    ] = df_sampled[
        'minutes_from_midnight'
        ].apply(
    lambda x: (
        x
        if x >= 1080
        else x + 1440
    )
)

# Graficar los datos con minutos desde la medianoche
plt.figure(figsize=(10, 6))
plt.plot(
    df_sampled['minutes_from_midnight'],
    df_sampled['data'],
    marker='o',
    linestyle='-',
    label='Data (Muestreada)'
)
plt.xlabel('Minutos desde la medianoche (ajustados)', fontsize=12)
plt.ylabel('Data', fontsize=12)
plt.title(
    'Gráfica de Data vs Minutos desde Medianoche (18:00-06:00)', fontsize=14
    )

# Ajustar la escala del eje vertical
y_min = df_sampled['data'].min() - 10  # Ajuste inferior
y_max = df_sampled['data'].max() + 10  # Ajuste superior
plt.ylim(y_min, y_max)

plt.grid(True)
plt.legend()
plt.tight_layout()

# Guardar la gráfica
output_path = script_dir / 'grafica_estacionalidad_noche.png'
plt.savefig(output_path, format='png')
print(f"Gráfica guardada en: {output_path}")
plt.close()
