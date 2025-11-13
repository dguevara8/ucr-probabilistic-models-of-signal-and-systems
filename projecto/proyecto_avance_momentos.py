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
