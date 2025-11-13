# Gráficas

Al haber obtenido todos los datos necesarios estos se creo el siguiente código, con el fin de observar sus resultados.
### Módulos y librerías utilizadas
1.	sqlite3: se utiliza para interactuar con bases de datos SQLite.
2.	pandas: es para análisis y manipulación de datos tabulares.
3.	matplotlib.pyplot: funciona para crear gráficos y visualizaciones de datos.
4.	seaborn: genera gráficos estadísticos atractivos y fáciles de interpretar.
5.	scipy.stats: realiza análisis y pruebas estadísticas.
6.	numpy: facilita la realización de operaciones numéricas y manipulación de arrays.
7.	time: manejar tiempo y medir duraciones en la ejecución de código.

```python title="Código gráficas con el modelo de probabilidad ajustado"
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import time


def load_data():
    """Carga los datos desde la base de datos SQLite."""
    db_path = 'proyecto.db'
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM test_data", conn)
    conn.close()
    return df


def plot_descriptive_graphs(data, variable):
    """Genera gráficas descriptivas para la variable especificada."""
    plt.figure(figsize=(12, 6))
    # Histograma
    plt.subplot(121)
    sns.histplot(data[variable], kde=True, bins=50)
    plt.title(f'Histograma de {variable}')
    # Box plot
    plt.subplot(122)
    sns.boxplot(y=data[variable])
    plt.title(f'Box Plot de {variable}')
    plt.tight_layout()
    plt.savefig(f'{variable}_descriptive_graphs.png')
    plt.close()


def plot_probability_model(data, variable):
    """Genera un histograma con un modelo de probabilidad ajustado."""
    plt.figure(figsize=(10, 6))
    # Crear el histograma
    sns.histplot(data[variable], kde=True,
                 stat="density", bins=50, label='Datos')
    # Ajustar y graficar el modelo de probabilidad
    if variable == 'variable_1':
        # Ajustar una distribución normal para variable_1
        mu, std = stats.norm.fit(data[variable])
        x = np.linspace(data[variable].min(), data[variable].max(), 100)
        p = stats.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2,
                 label='Modelo Normal')
        plt.title(f'Histograma y Modelo '
                  f'de Probabilidad Normal para {variable}')
    elif variable == 'variable_2':
        # Ajustar una distribución exponencial para variable_2
        # Asegurarse de que todos los valores sean positivos
        data_pos = data[variable] - data[variable].min() + 0.01
        param = stats.expon.fit(data_pos)
        x = np.linspace(data_pos.min(), data_pos.max(), 100)
        p = stats.expon.pdf(x, *param)
        plt.plot(x, p, 'k', linewidth=2, label='Modelo Exponencial')
        plt.title(f'Histograma y Modelo '
                  f'de Probabilidad Exponencial para {variable}')
    plt.legend()
    plt.savefig(f'{variable}_probability_model.png')
    plt.close()
```

### Modelo de Probabilidad Normal para variable_1
Este gráfico representa un histograma, donde se muestra la distribución de frecuencia de los datos de variable_1, al presentar la forma de campana, lo que indica que los datos se aproximan a una distribución normal o gaussiana, porque los datos parecen tener una distribución simétrica alrededor de un valor central (cerca de 0), además de que la mayoría de los datos están concentrados en torno a la media, y presentan una dispersión gradual hacia los extremos.
cuencia a medida que aumentan los valores, esto es característico de datos que podrían representar tiempos de espera entre eventos.

![Texto alternativo](img/Histograma_variable1.png)

![Texto alternativo](img/Ajuste_histograma_variable1.png)

###  Modelo de Probabilidad Exponencial para variable_2
Este histograma muestra la distribución de frecuencia de los datos de variable_2, donde los datos tienen un comportamiento asimétrico, con una gran concentración de valores cerca de 0 y una disminución exponencial hacia valores más altos, por lo que se podría decir que es una distribución exponencial, con una rápida caída en la frecuencia a medida que aumentan los valores, esto es característico de datos que podrían representar tiempos de espera entre eventos.

![Texto alternativo](img/Histograma_variable2.png)

![Texto alternativo](img/Ajuste_histograma_variable2.png)
