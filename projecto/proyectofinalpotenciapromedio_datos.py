import sqlite3
import pandas as pd

# Cargar los datos de la base de datos original
db_path = 'proyecto.db'
conn = sqlite3.connect(db_path)
query = "SELECT data FROM test_data;"  # Ajustar según tu estructura de tabla
df = pd.read_sql_query(query, conn)
conn.close()

# Calcular la potencia promedio
df['data_squared'] = df['data'] ** 2
average_power = df['data_squared'].mean()

print(f"La potencia promedio es: {average_power}")
