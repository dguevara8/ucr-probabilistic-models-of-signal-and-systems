# Momentos de los modelos de probabilidad de los datos

Por otro lado, también se escribió esta otra parte del código para así visualizar los momentos de los modelos, utilizando los mismos módulos y librerías ya mencionadas en el apartado de gráficas.

```python title="Código de momentos (promedio, varianza, desviación estándar, inclinación, kurtosis)"
import sqlite3
import pandas as pd
import time


def load_data():
    """Carga los datos desde la base de datos SQLite."""
    db_path = 'proyecto.db'
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM test_data", conn)
    conn.close()
    return df


def calculate_moments(data, variable):
    """Devuelve los momentos estadísticos de la variable especificada."""
    return {
        "Promedio": data[variable].mean(),
        "Varianza": data[variable].var(),
        "Desviación estándar": data[variable].std(),
        "Asimetría (Skewness)": data[variable].skew(),
        "Curtosis": data[variable].kurtosis()
    }


def main():
    start_time = time.time()
    print("Cargando datos...")
    df = load_data()
    print(f"Datos cargados. Forma del DataFrame: {df.shape}")

    for variable in ['variable_1', 'variable_2']:
        print(f"\nAnalizando {variable}...")
        print("Calculando momentos estadísticos...")
        moments = calculate_moments(df, variable)
        print(f"Momentos estadísticos para {variable}:")
        for k, v in moments.items():
            print(f"{k}: {v:.4f}")

    end_time = time.time()
    print(f"\nTiempo total de ejecución: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
```
###  Momentos estadísticos para variable_1
Primeramente, el promedio tiene un valor cercano a 0, que  sugiere que los datos están bastante centrados alrededor de este valor.  En este caso, la varianza se muestra moderada, lo que significa que los datos tienen cierta variabilidad alrededor de su promedio, la desviación estándar simplemente es la raíz cuadrada de la varianza. La asimetría al tener un valor cercano a 0 indica que los datos están simétricamente distribuidos, lo cual es el caso aquí.  Terminando, se puede decir que la curtosis mide el "apuntamiento" de la distribución, por lo que el valor de la variable 1 indica una distribución más plana.

## Momentos estadísticos para variable_1

| Estadístico             | Valor   |
|-------------------------|---------|
| Promedio                | -0.0062 |
| Varianza                | 3.3064  |
| Desviación estándar     | 1.8183  |
| Asimetría (Skewness)    | 0.0034  |
| Curtosis                | 1.1844  |

###  Momentos estadísticos para variable_2
El promedio en este caso, es positivo y considerablemente mayor que 0, lo que sugiere que los valores están centrados alrededor de 4.3064. Por lo que concierne al valor de la varianza; este es mucho mayor en comparación con variable_1, lo que indica que hay una mayor dispersión en los datos. Los datos de variable_2 están más alejados de su promedio en comparación con los de variable_1, la desviación estándar simplemente es la raíz cuadrada de la varianza. Este valor de asimetría al ser positivo y alto muestra el porque la distribución de los datos está sesgada hacia la derecha. Por último, la curtosis presenta valor extremadamente alto, lo que significa que hay valores extremos que ocurren con mayor frecuencia de lo que se esperaría en una distribución normal.

## Momentos estadísticos para variable_2

| Estadístico             | Valor   |
|-------------------------|---------|
| Promedio                | 4.3064  |
| Varianza                | 34.8117 |
| Desviación estándar     | 5.9001  |
| Asimetría (Skewness)    | 5.0048  |
| Curtosis                | 46.1414 |