# Script para Procesar y Visualizar Datos
## Recolección de datos por 24 horas.
Este script realiza la carga, procesamiento y visualización de datos desde una base de datos de 24 horas continuas. A continuación se describe el código.

```python
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
        db_path = 'proyecto.db'
        query = "SELECT timestamp, data FROM test_data;"
        script_dir = Path(__file__).parent
        output_path = script_dir / 'grafica_datos.png'

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
```
## Recolección de datos de día
![Texto alternativo](img/grafica_datos.png "Gráfica datos 24 horas")
Los valores muestran una clara disminución de la amplitud (dispersiones más pequeñas) en el periodo central del registro, específicamente alrededor del rango de tiempo equivalente al mediodía hasta la tarde (desde 600 hasta aproximadamente 1600 minutos desde la medianoche). 

Antes y después de este rango central, las variaciones son más amplias, indicando que hay una mayor dispersión o variabilidad al inicio (mañana temprana) y al final (noche/madrugada).

Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante el día. A continuación se describe el código.
```python
import sqlite3
import pandas as pd
from datetime import time
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

        # Filtrar datos entre las 6:00 AM y las 6:00 PM
        df = df[
            (df['timestamp'].dt.time >= time(6, 0)) &
            (df['timestamp'].dt.time <= time(18, 0))
        ]

        # Calcular minutos desde medianoche
        df['minutes'] = (
            df['timestamp'].dt.hour * 60 +
            df['timestamp'].dt.minute
        )

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

        plt.title('Datos Dependientes del Tiempo (6 AM - 6 PM)')
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
        db_path = 'day.db'  # Ruta al archivo cargado
        query = "SELECT timestamp, data FROM test_data;"
        script_dir = Path(__file__).parent
        output_path = script_dir / 'graficadatos_dia.png'

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
```
## Recolección de datos de noche
![Texto alternativo](img/graficadatos_dia.png "Gráfica datos día")
Existe una distribución relativamente más amplia en comparación con la gráfica de los datos nocturnos. Se observan picos significativos en ambas direcciones (positiva y negativa), lo que indica que hay eventos extremos, aunque no son demasiado frecuentes. La dispersión es notable, pero más contenida cerca del mediodía, lo cual podría coincidir con condiciones más estables en este periodo. 

La amplitud de los datos (diferencia entre los valores máximos y mínimos) es mayor durante el día, lo que podría estar relacionado con factores externos más activos. Hay un rango horario específico donde los valores están más estabilizados (probablemente en las horas cercanas al mediodía).

Este script realiza la carga, procesamiento y visualización de datos desde una base de datos durante la noche. A continuación se describe el código.
```python
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
```
![Texto alternativo](img/graficadatos_noche.png "Gráfica datos noche")
Los valores están claramente más concentrados, con menor dispersión general en comparación con el día. Los picos extremos son más pequeños, indicando menos eventos fuera de lo común durante la noche. Los datos parecen estar muy centrados alrededor de la media, lo cual refleja mayor estabilidad. 

La estabilidad de los datos durante la noche podría estar relacionada con una disminución en la influencia de factores externos. La menor dispersión sugiere que los datos nocturnos podrían ser más representativos del comportamiento base del sistema, sin interferencias significativas. El rango de variación es más estrecho, con una menor amplitud de valores extremos. Esto puede indicar que las condiciones nocturnas son menos dinámicas o más constantes.

## Conclusiones
Las gráficas evidencian un comportamiento del sistema con mayor estabilidad durante la noche y mayor variabilidad durante el día. Durante las horas nocturnas (11:00 PM a 6:00 AM), los datos presentan menor amplitud y dispersión, lo que refleja condiciones más constantes y una menor influencia de factores externos. Por otro lado, en el período diurno (6:00 AM a 6:00 PM), la dispersión de los datos es más amplia, especialmente en las horas intermedias, indicando una interacción más activa del sistema con su entorno y la ocurrencia de eventos más extremos.

En general, el sistema muestra patrones claros de menor dinamismo y mayor estabilidad durante la noche, mientras que durante el día se observa una mayor amplitud en los valores, posiblemente vinculada a la influencia de factores externos o condiciones variables. Estos resultados destacan la importancia de considerar los diferentes periodos de tiempo al analizar o optimizar el comportamiento del sistema.