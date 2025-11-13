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


def main():
    start_time = time.time()
    print("Cargando datos...")
    df = load_data()
    print(f"Datos cargados. Forma del DataFrame: {df.shape}")

    for variable in ['variable_1', 'variable_2']:
        print(f"\nAnalizando {variable}...")
        print("Generando gráficas descriptivas...")
        plot_descriptive_graphs(df, variable)
        print("Generando modelo de probabilidad...")
        plot_probability_model(df, variable)

    end_time = time.time()
    print(f"\nTiempo total de ejecución: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
