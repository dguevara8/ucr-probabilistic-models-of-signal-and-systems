from scipy import stats
import pandas as pd
import sqlite3

# Conectar a la base de datos original
db_path = 'night.db'  # Reemplaza con la ruta correcta
conn = sqlite3.connect(db_path)

# Cargar los datos necesarios de la tabla test_data
query = "SELECT timestamp, data FROM test_data"
data_df = pd.read_sql_query(query, conn)
conn.close()

# Verificar que la columna "data" no contenga valores nulos
if data_df['data'].isnull().any():
    raise ValueError(
        "La columna 'data' contiene valores nulos. "
        "Elimina o imputa los datos "
        "antes de continuar."
    )

# Agrupar por timestamp y calcular loc y scale
results = []
for timestamp, group in data_df.groupby('timestamp'):
    data_values = group['data'].values
    loc, scale = stats.logistic.fit(data_values)
    results.append((timestamp, loc, scale))

# Crear un DataFrame con los resultados
results_df = pd.DataFrame(results, columns=['timestamp', 'loc', 'scale'])

# Conectar a la nueva base de datos para guardar resultados
new_db_path = 'parameters_night.db'  # Reemplaza con la ruta donde guardar
conn = sqlite3.connect(new_db_path)

# Crear tabla si no existe
conn.execute('''
CREATE TABLE IF NOT EXISTS parameters (
    timestamp TEXT,
    loc REAL,
    scale REAL
)
''')

# Insertar los datos en la tabla
results_df.to_sql('parameters', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.commit()
conn.close()

print(f"Parámetros 'loc' y 'scale' calculados y guardados en '{new_db_path}'.")
