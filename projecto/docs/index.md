# Proyecto de programación

### Integrantes:
1. Danna Guevara Quesada C23562
2. Jean Carlo Chinchilla Mora C02276
3. Josué Rodríguez Salamanca C26692

Esta es la documentación del proyecto de programación de IE0405 - Modelos Probabilísticos de Señales y Sistemas.
Inicialmente, este proyecto se llevo acabo por medio de las instrucciones brindadas en (https://mpss-eie.github.io/proyecto/instrucciones/), donde se ejecutaron paso a paso las instrucciones para la realización de este proyecto, desde su nueva recolección de datos hasta las recomendaciones obtenidas de (https://github.com/fabianabarca/python/blob/main/Py5.ipynb) para los códigos, donde se instalaron todos los paquetes faltantes necesarios para el funcionamiento de estos. Todo esto, para finalmente realizar un respectivo análisis de todo lo obtenido en el mkdocs.
## Conceptos importantes

!!! note "Función de densidad de probabilidad"
    Describe cómo se distribuyen los valores de una variable aleatoria, indicando la probabilidad relativa de que tome un valor específico, aunque no proporciona probabilidades absolutas.

!!! note "Estacionaridad en sentido amplio"
    Una señal es estacionaria en este sentido si su media, varianza y función de autocorrelación no cambian con el tiempo, lo que facilita el análisis de señales aleatorias.

!!! note "Promedios temporales de funciones muestra"
    Representan los valores promedio calculados a lo largo del tiempo para una realización específica de un proceso aleatorio, utilizados como estimaciones de sus características estadísticas.

!!! note "Ergodicidad"
    Un proceso aleatorio es ergódico si los promedios temporales coinciden con los promedios esperados (probabilísticos), lo que permite caracterizar el proceso completo a partir de una única muestra.

!!! note "Correlación y covarianza"
    - **Correlación**: Mide cómo dos señales (o una consigo misma) están relacionadas en el tiempo o espacio.
    - **Covarianza**: Evalúa la relación lineal entre dos señales, considerando sus valores centrados respecto a las medias.

!!! note "Potencia promedio"
    Representa la energía promedio transferida por una señal en un intervalo de tiempo, un concepto clave en el análisis de señales periódicas y aleatorias.

!!! note "Densidad espectral de potencia"
    Describe cómo se distribuye la potencia de una señal en el dominio de la frecuencia, proporcionando información sobre su contenido espectral.

!!! note "Análisis de ruido"
    Estudia las características estadísticas y espectrales del ruido en un sistema, ayudando a entender su impacto y diseñar estrategias para mitigar sus efectos.

### Tipos de modelos de distribución de probabilidad.
1.	Distribución normal (o gaussiana): es la distribución continua más común. Tiene forma de campana simétrica y describe muchas variables naturales como la altura o el peso.
2.	Distribución exponencial: modela el tiempo entre eventos en un proceso de Poisson (eventos que ocurren a una tasa constante e independiente).
3.	Distribución uniforme continua: todos los valores en un intervalo tienen la misma probabilidad.
4.	Distribución de Bernoulli: se usa para modelar experimentos que tienen solo dos resultados posibles: éxito o fracaso.
5.	Distribución de Rayleigh: es útil para modelar fenómenos en los que la magnitud de un vector aleatorio bidimensional, cuyas componentes son variables aleatorias independientes y normalmente distribuidas.
6.	Distribución de Boltzmann: suele utilizarse para modelar la distribución de energías en sistemas físicos en equilibrio térmico, como gases a diferentes temperaturas.

### Recolección de datos.
1.	Primeramente, en el directorio raíz se debe de crear un archivo proyecto.cfg, rellenándolo con el contenido respectivo según el grupo, donde se modificar según las necesidades de su implementación. 
2.	En una nueva terminal se debe de activar Redis y dejar esta terminal abierta, porque esta funcionará como la base de datos en memoria, de código abierto y extremadamente rápida, que se utiliza principalmente como almacenamiento clave-valor. A diferencia de otras bases de datos tradicionales, Redis almacena los datos directamente en la memoria RAM, lo que le permite acceder a ellos de manera muy eficiente, siendo ideal para aplicaciones que requieren baja latencia y alto rendimiento.
3.	En una nueva terminal ejecutar el siguiente comando para activar Celery Worker y Celery Beat; con el fin de que se estén importando y guardando datos en la base de datos, según está detallado en models.py y tasks.py.
4.	Finalmente, deben de dejarse todas estas terminales abiertas por un transcurso de 24 horas; con el fin de que recopile la mayor cantidad de datos posibles.

### Documentación.
1.	Tras la exhaustiva espera de la recopilación de datos, se debe de realizar un análisis exploratorio de los datos obtenidos.
2.	Con los respetivos datos; se determina la función de densidad de probabilidad, la estacionaridad en sentido amplio y ergodicidad y por último la determinación de la potencia promedio.
3.  Al finalizar la escritura de todos los codigos repectivos a los analisis de las funciones se verifica que cumplan con PEP 8.
3.	Luego, se realiza el respectivo análisis de resultados con todas las gráficas obtenidas anteriormente y sus conclusiones.
5.	Finalmente, se almacenan todos los datos obtenidos por medio de la documentación de mkdocs serve.