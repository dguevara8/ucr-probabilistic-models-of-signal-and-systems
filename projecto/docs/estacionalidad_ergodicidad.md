# Estacionalidad en sentido amplio y ergodicidad
## Estacionalidad en sentido amplio
### Estacionalidad en sentido amplio de día
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante el día para determinar la estacionalidad en sentido amplio. A continuación se describe el código.
```python
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
```
![Texto alternativo](img/grafica_estacionalidad_dia.png "Gráfica estacionalidad día")

### Estacionalidad en sentido amplio de noche
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante la noche para determinar la estacionalidad en sentido amplio. A continuación se describe el código.
```python
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
```
![Texto alternativo](img/grafica_estacionalidad_noche.png "Gráfica estacionalidad noche")

En la gráfica del día, la autocorrelación muestra una marcada dependencia temporal que no es constante, evidenciada por su forma en "campana". Este comportamiento sugiere que las relaciones entre los valores en diferentes momentos varían a lo largo del día. Esto indica que el proceso diurno no es estacionario en sentido amplio, ya que la autocorrelación depende del tiempo absoluto. Este resultado es coherente con un sistema afectado por factores externos dinámicos, como cambios ambientales o actividades humanas, que introducen variaciones en las dependencias temporales.

Por otro lado, la gráfica de la noche muestra una autocorrelación constante y estable a lo largo del tiempo, con valores cercanos a cero. Este comportamiento indica que las relaciones entre los valores nocturnos son homogéneas y no dependen del tiempo absoluto. Esto cumple con el requisito de estacionalidad en sentido amplio, ya que las propiedades estadísticas, incluyendo la autocorrelación, permanecen invariables en el tiempo durante este periodo. Este resultado refleja una mayor estabilidad y ausencia de dinámicas externas significativas durante la noche.

## Ergodicidad

Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante el día para determinar la ergodicidad. A continuación se describe el código.
```python
import sqlite3
import pandas as pd

# Ruta a las bases de datos
original_db_path = 'day.db'
new_db_path = 'ergodicidad_day.db'

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
```

Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante la noche para determinar la ergodicidad. A continuación se describe el código.
```python
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
```
| Tiempo | Promedio datos completos | Promedio muestra de datos | Diferencia |
|--------|---------------------------|----------------------------|------------|
| Día    | 2.662737567645559         | 2.5908736339321745         | 0.0718639337133844 |
| Noche  | -0.002244522427234939     | -0.014919608419609596      | 0.012675085992374657 |

El análisis de ergodicidad se centra en comparar si las estadísticas temporales (promedio de datos completos) coinciden con las estadísticas espaciales (promedio de una muestra representativa). En este caso, los resultados muestran que para el día, la diferencia entre ambos promedios es de aproximadamente 0.0719, lo cual es relativamente pequeño, pero no insignificante. Esto indica que los datos diurnos no son completamente ergódicos, ya que la muestra de datos no refleja perfectamente el promedio global. Este resultado puede deberse a la naturaleza no estacionaria de los datos diurnos, como se observó previamente en su comportamiento dinámico y dependiente del tiempo.

Por el contrario, en el periodo nocturno, la diferencia entre el promedio de los datos completos y el promedio de la muestra es de aproximadamente 0.0127, mucho menor que la diferencia observada durante el día. Este resultado respalda que los datos nocturnos son más ergódicos, ya que la muestra seleccionada representa de manera más precisa el comportamiento global. Esto coincide con las observaciones previas sobre la mayor estabilidad y estacionariedad en sentido amplio de los datos nocturnos, lo que facilita que las propiedades estadísticas temporales se alineen con las estadísticas espaciales del sistema.

## Conclusiones
Las gráficas muestran un comportamiento contrastante en la autocorrelación de los datos entre el día y la noche. Durante el día, la autocorrelación presenta una dependencia temporal no constante con una forma de "campana", indicando un proceso no estacionario influenciado por factores externos dinámicos como cambios ambientales o actividades humanas. En contraste, durante la noche, la autocorrelación es constante y estable, con valores cercanos a cero, lo que refleja un comportamiento estacionario con propiedades estadísticas invariables y la ausencia de dinámicas externas significativas. Esto evidencia una mayor estabilidad y homogeneidad en las condiciones nocturnas frente a la variabilidad del día.

El análisis de ergodicidad revela que los datos diurnos no son completamente ergódicos, dado que existe una diferencia notable entre el promedio de los datos completos y el de la muestra representativa, lo cual se asocia a la naturaleza no estacionaria y dinámica de este período. En contraste, durante la noche, la diferencia entre ambos promedios es significativamente menor, lo que sugiere que los datos nocturnos son más ergódicos y representan con mayor precisión el comportamiento global del sistema. Esto refuerza la observación de que las condiciones nocturnas son más estables y homogéneas, alineándose mejor con las propiedades estadísticas esperadas del sistema.