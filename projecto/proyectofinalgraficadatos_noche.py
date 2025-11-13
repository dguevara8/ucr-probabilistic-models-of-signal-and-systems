import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path


def configure_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def connect_to_database(db_path):
    """
    Establece conexión con la base de datos SQLite.

    Args:
        db_path (str): Ruta al archivo de la base de datos

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos
    """
    try:
        db_path = Path(db_path)
        if not db_path.exists():
            raise FileNotFoundError(
                f"No se encontró la base de datos en: {db_path}"
                )

        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        raise


def load_data(conn, query):
    """
    Carga datos desde la base de datos usando pandas.

    Args:
        conn (sqlite3.Connection): Conexión a la base de datos
        query (str): Consulta SQL para obtener los datos

    Returns:
        pd.DataFrame: DataFrame con los datos cargados
    """
    try:
        return pd.read_sql_query(query, conn)
    except pd.io.sql.DatabaseError as e:
        logging.error(f"Error al cargar datos: {e}")
        raise


def process_data(df):
    """
    Procesa el DataFrame para preparar los datos para la visualización.

    Args:
        df (pd.DataFrame): DataFrame con los datos crudos

    Returns:
        pd.DataFrame: DataFrame procesado
    """
    try:
        # Convertir 'timestamp' a datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Calcular minutos desde medianoche
        start_time = df['timestamp'].iloc[0].normalize()
        df['minutes'] = (df['timestamp'] - start_time).dt.total_seconds() / 60

        return df
    except Exception as e:
        logging.error(f"Error al procesar datos: {e}")
        raise


def create_plot(df, output_path):
    """
    Crea y guarda la gráfica de los datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos procesados
        output_path (Path): Ruta donde se guardará la gráfica
    """
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(df['minutes'], df['data'],
                 marker='o',
                 linestyle='-',
                 color='b',
                 label='Data')

        plt.title('Datos Dependientes del Tiempo')
        plt.xlabel('Tiempo (minutos desde medianoche)')
        plt.ylabel('Valores de Data')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        plt.savefig(output_path, format='png')
        logging.info(f"Gráfica guardada en: {output_path}")
    except Exception as e:
        logging.error(f"Error al crear o guardar la gráfica: {e}")
        raise


def main():
    """Función principal que ejecuta todo el proceso."""
    configure_logging()

    try:
        # Configuración
        db_path = 'night.db'
        query = "SELECT timestamp, data FROM test_data;"
        script_dir = Path(__file__).parent
        output_path = script_dir / 'graficadatos_noche.png'

        # Ejecutar el proceso
        with connect_to_database(db_path) as conn:
            df_raw = load_data(conn, query)
            df_processed = process_data(df_raw)
            create_plot(df_processed, output_path)

    except Exception as e:
        logging.error(f"Error en la ejecución principal: {e}")
        raise


if __name__ == "__main__":
    main()
