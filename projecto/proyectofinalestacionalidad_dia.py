import sqlite3
import pandas as pd

# Ruta a la base de datos proporcionada
db_path = 'day.db'

# Cargar los datos desde la base de datos original
conn = sqlite3.connect(db_path)
query = "SELECT timestamp, data FROM test_data;"
df = pd.read_sql_query(query, conn)
conn.close()

# Convertir la columna 'timestamp' a tipo datetime y filtrar valores NULL
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(
    subset=['timestamp', 'data']
)

# Convertir a índice de tiempo y muestrear cada 10 minutos
df.set_index('timestamp', inplace=True)
sampled_df = df.resample('10T').mean().reset_index()

# Calcular la autocorrelación para cada muestra de 10 minutos
autocorrelations = []
for i in range(len(sampled_df)):
    window = sampled_df['data'].iloc[max(0, i - 10):i+1]  # 10 muestras
    if len(window) > 1:
        autocorr = window.autocorr()  # Calcular la autocorrelación
        autocorrelations.append(autocorr)
    else:
        autocorrelations.append(None)

# Agregar autocorrelaciones al DataFrame muestreado
sampled_df['autocorrelation'] = autocorrelations

# Eliminar filas con valores NULL en las columnas calculadas
filtered_df = sampled_df.dropna(subset=['data', 'autocorrelation'])

# Guardar los datos filtrados en una nueva base de datos
new_db_path = 'estacionalidad_day.db'
conn_new = sqlite3.connect(new_db_path)
filtered_df.to_sql('filtered_sampled_data_with_autocorrelation',
                   conn_new, if_exists='replace', index=False)
conn_new.close()

print(f"Datos filtrados y procesados guardados en {new_db_path}")
