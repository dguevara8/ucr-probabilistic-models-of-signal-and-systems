import sqlite3

# Rutas de las bases de datos
input_db_path = 'proyecto.db'  # Base de datos original
night_db_path = 'night.db'    # Base de datos para sunlight = 0
day_db_path = 'day.db'        # Base de datos para sunlight = 1

# Conectar a la base de datos original
conn_input = sqlite3.connect(input_db_path)
cursor_input = conn_input.cursor()

# Crear conexiones a las nuevas bases de datos
conn_night = sqlite3.connect(night_db_path)
cursor_night = conn_night.cursor()
conn_day = sqlite3.connect(day_db_path)
cursor_day = conn_day.cursor()

# Obtener todas las tablas de la base de datos original
cursor_input.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_input.fetchall()

# Procesar cada tabla
for table_name in tables:
    table_name = table_name[0]  # Nombre de la tabla
    # Obtener los datos de la tabla
    cursor_input.execute(f"SELECT * FROM '{table_name}'")
    rows = cursor_input.fetchall()

    # Obtener la estructura de la tabla
    cursor_input.execute(f"PRAGMA table_info('{table_name}')")
    columns_info = cursor_input.fetchall()
    columns = [col[1] for col in columns_info]
    columns_def = ", ".join([f'"{col[1]}" {col[2]}' for col in columns_info])

    # Crear las tablas en las nuevas bases de datos
    cursor_night.execute(
        f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_def})'
        )
    cursor_day.execute(
        f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_def})'
        )

    # Identificar la columna 'sunlight'
    sunlight_column_index = None
    for idx, col in enumerate(columns_info):
        if col[1].lower() == 'sunlight':
            sunlight_column_index = idx
            break

    if sunlight_column_index is None:
        print(f"La tabla '{table_name}' no tiene una columna 'sunlight'.")
        continue

    # Dividir los datos según el valor de 'sunlight'
    night_rows = [
        row for row in rows if row[sunlight_column_index] == 0
        ]
    day_rows = [
        row for row in rows if row[sunlight_column_index] == 1
        ]

    # Insertar los datos en las bases de datos correspondientes
    placeholders = ", ".join(["?" for _ in columns])
    cursor_night.executemany(
        f'INSERT INTO "{table_name}" VALUES ({placeholders})', night_rows
        )
    cursor_day.executemany(
        f'INSERT INTO "{table_name}" VALUES ({placeholders})', day_rows
        )

# Confirmar cambios y cerrar conexiones
conn_night.commit()
conn_day.commit()
conn_input.close()
conn_night.close()
conn_day.close()

print("Bases de datos creadas: 'night.db' y 'day.db'.")
