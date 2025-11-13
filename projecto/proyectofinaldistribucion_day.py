import sqlite3
import pandas as pd
from fitter import Fitter
import matplotlib.pyplot as plt

# Conexión a la base de datos SQLite
conn = sqlite3.connect('day.db')

# Cargar los datos desde la tabla "test_data" y la columna "data"
query = "SELECT data FROM test_data"
data = pd.read_sql_query(query, conn)["data"].dropna()

# Cerrar la conexión
conn.close()

# Convertir los datos a tipo numérico si no lo son
data = pd.to_numeric(data, errors='coerce').dropna()

# Definir las distribuciones a evaluar
distribuciones = ['expon', 'gompertz', 'levy', 'logistic', 'norm', 'rayleigh']

# Ajustar las distribuciones con Fitter
f = Fitter(data, distributions=distribuciones)
f.fit()

# Obtener la mejor distribución y sus parámetros
best_fit = f.get_best()

# Imprimir los resultados
print("Mejor distribución encontrada:")
print(best_fit)

# Graficar las distribuciones ajustadas
f.summary()
plt.show()
