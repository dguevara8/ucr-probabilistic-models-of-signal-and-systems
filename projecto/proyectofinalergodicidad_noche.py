import sqlite3
import pandas as pd

# Ruta de la base de datos original
uploaded_db_path = 'night.db'

# Cargar los datos desde la base de datos original
conn = sqlite3.connect(uploaded_db_path)
query = "SELECT * FROM test_data;"
df = pd.read_sql_query(query, conn)
conn.close()

# Agrupar por 'timestamp' y seleccionar el quinto valor (si existe)
selected_data = (
                    df.groupby('timestamp')
                    .apply(
                        lambda x: x.iloc[4] if len(x) > 4 else None
                    )
                    .dropna()
                    .reset_index(drop=True)
                )

# Guardar los datos seleccionados en una nueva base de datos
new_db_path = 'ergodicidad_night.db'
conn_new = sqlite3.connect(new_db_path)
selected_data[['timestamp', 'data']].to_sql(
    'selected_data',
    conn_new,
    if_exists='replace',
    index=False
)
conn_new.close()

print(f"Datos guardados en {new_db_path}")
