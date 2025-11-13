import sqlite3
import pandas as pd

# Ruta a la base de datos original
db_path = 'night.db'

# Cargar los datos desde la base de datos original
conn = sqlite3.connect(db_path)
query = "SELECT timestamp, data FROM test_data;"
df = pd.read_sql_query(query, conn)
conn.close()

# Convertir la columna 'timestamp' a tipo datetime y muestrear cada 10 minutos
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
sampled_df = df.resample('10T').mean().reset_index()

# Guardar los datos muestreados en una nueva base de datos
new_db_path = 'estacionalidad_night.db'
conn_new = sqlite3.connect(new_db_path)
sampled_df.to_sql('sampled_data', conn_new, if_exists='replace', index=False)
conn_new.close()

print(f"Datos muestreados guardados en {new_db_path}")
