import sqlite3
import pandas as pd

# Ruta a las bases de datos
original_db_path = 'night.db'
new_db_path = 'ergodicidad_night.db'

# Cargar la base de datos original y calcular el promedio
conn_original = sqlite3.connect(original_db_path)
query_original = "SELECT data FROM test_data;"
df_original = pd.read_sql_query(query_original, conn_original)
conn_original.close()

# Calcular el promedio de la base de datos original
average_original = df_original['data'].mean()

# Cargar la base de datos nueva y calcular el promedio
conn_new = sqlite3.connect(new_db_path)
query_new = "SELECT data FROM selected_data;"
df_new = pd.read_sql_query(query_new, conn_new)
conn_new.close()

# Calcular el promedio de la base de datos nueva
average_new = df_new['data'].mean()

# Comparar los promedios
difference = abs(average_original - average_new)
similar = difference < 0.1  # Umbral para determinar si son similares

# Resultados
comparison_result = {
    "Average Original (night.db)": average_original,
    "Average New (ergodicidad_night.db)": average_new,
    "Difference": difference,
    "Similar": similar
}

print(comparison_result)
