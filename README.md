Análisis y proyección de la matrícula educativa en la provincia de Buenos Aires

Descripción del proyecto

Este repositorio contiene los datos, scripts de Python, análisis exploratorio y resultados desarrollados para el trabajo final de la Licenciatura en Ciencia de Datos de la Universidad CAECE.

La investigación analiza la evolución de la matrícula educativa en los 135 partidos de la provincia de Buenos Aires, considerando los niveles Inicial, Primario y Secundario.

El período histórico estudiado comprende los años 2012 a 2025, mientras que las proyecciones se extienden desde 2026 hasta 2035.

El objetivo es analizar cómo evolucionó la matrícula, identificar diferencias entre los partidos y evaluar distintas estrategias para proyectar su comportamiento futuro.

Fuentes de datos

Para desarrollar el proyecto se utilizaron datos públicos de organismos oficiales:

* Secretaría de Educación de la Nación: Relevamiento Anual de matrícula educativa, período 2012–2025.
* INDEC: Censo Nacional de Población, Hogares y Viviendas 2022.
* INDEC: estimaciones de población por departamento para el período 2022–2035.
* RENAPER: registros de nacimientos correspondientes al período 2012–2022.

También se analizaron variables demográficas, socioeconómicas y habitacionales para estudiar su relación con la evolución de la matrícula.

Estas variables se utilizaron principalmente en el análisis exploratorio y no se incorporaron como predictores en el modelo final debido a las limitaciones de disponibilidad temporal.

Metodología

El proyecto se desarrolló en distintas etapas:

1. Recolección e inspección de las fuentes de datos.
2. Limpieza y transformación de los archivos originales.
3. Integración de las fuentes en un dataset maestro.
4. Análisis exploratorio de la evolución histórica de la matrícula.
5. Construcción de variables para el modelado predictivo.
6. Entrenamiento y evaluación de modelos.
7. Comparación con un modelo de referencia basado en persistencia.
8. Evaluación temporal y análisis de errores.
9. Elaboración de proyecciones de matrícula hasta 2035.

Para el modelado se utilizó Random Forest, comparando sus resultados con una estrategia de persistencia.

Los datos se dividieron cronológicamente en tres conjuntos:
    Entrenamiento: 2015–2021
    Validación: 2022–2023
    Prueba: 2024–2025

Las proyecciones futuras se realizaron mediante tres estrategias: persistencia, tendencia reciente y Random Forest.

Estructura del repositorio

01_datos

Contiene los principales datasets utilizados en la investigación:

* dataset_maestro_final.csv: integración de la información histórica y las variables analizadas.
* dataset_modelado.csv: datos organizados para el modelado.
* dataset_modelado_features.csv: dataset con las variables predictoras.
* matricula_limpia_final.csv: información de matrícula después de su procesamiento.

02_preparacion

Contiene los scripts utilizados para limpiar y transformar los datos de las distintas fuentes.

Incluye el procesamiento de matrícula, educación, población, nacimientos, fecundidad, economía, hogares y migraciones, además del script de integración del dataset maestro.

03_eda

Contiene la notebook de análisis exploratorio:

RomanoC_Entrega2_EDA_DemandaEducativa.ipynb

En ella se estudian la evolución histórica de la matrícula, las diferencias entre niveles educativos y partidos, y las relaciones con otras variables.

04_modelado

Contiene los scripts correspondientes a la preparación de datos, entrenamiento, validación y evaluación de los modelos.

También incluye archivos CSV con las divisiones temporales, predicciones, métricas y resultados intermedios.

05_proyecciones

Contiene los scripts utilizados para generar las proyecciones hasta 2035, construir escenarios alternativos y comparar los resultados de las estrategias.

06_resultados

Contiene los principales resultados finales del proyecto, incluyendo las proyecciones provinciales, por nivel educativo y las métricas de evaluación.

La subcarpeta graficos reúne las visualizaciones de la evolución histórica, las proyecciones y las diferencias territoriales.

Resultados principales

El análisis histórico mostró diferencias entre los niveles educativos. Mientras que la matrícula de Inicial y Primario disminuyó entre 2012 y 2025, la de Secundario aumentó.

En la evaluación sobre el conjunto de prueba, el modelo de persistencia obtuvo menores errores que Random Forest para la predicción a un año.

Las proyecciones provinciales para 2035 mostraron resultados diferentes según la estrategia utilizada:
    Persistencia: 3.849.256
    Tendencia reciente: 3.233.656
    Random Forest: 3.624.659
Estas diferencias muestran la importancia de considerar más de una estrategia al analizar la evolución futura de la matrícula.

Requisitos técnicos

El proyecto fue desarrollado en Python utilizando PyCharm.

Las principales bibliotecas utilizadas son:

* pandas
* numpy
* matplotlib
* scikit-learn
* pdfplumber

Las versiones utilizadas se encuentran especificadas en requirements.txt.

Para instalar las dependencias desde la carpeta principal del proyecto: "python -m pip install -r requirements.txt"
La instalación de las dependencias no garantiza por sí sola la ejecución completa del proyecto. Los scripts de limpieza pueden requerir los archivos originales descargados de las fuentes oficiales y algunas rutas deben verificarse al utilizar el proyecto en otro equipo.

Cómo consultar los archivos

Para revisar el trabajo se recomienda comenzar por la notebook de 03_eda, donde se presenta el análisis exploratorio.

Luego pueden consultarse los scripts de 04_modelado, que documentan la preparación de variables, el entrenamiento y la evaluación.

Los scripts de 05_proyecciones permiten revisar las estrategias utilizadas para proyectar la matrícula hasta 2035.

Finalmente, en 06_resultados se encuentran las principales tablas y visualizaciones obtenidas.

Limitaciones

Las proyecciones representan estimaciones de posibles escenarios futuros y no deben interpretarse como valores definitivos.

La matrícula observada se utiliza como una aproximación a la demanda educativa, pero no representa directamente las necesidades de infraestructura, docentes o establecimientos.

Además, las evaluaciones multianuales se realizaron sobre horizontes más cortos que el período proyectado hasta 2035, por lo que la incertidumbre aumenta a medida que se extiende el horizonte.

Información académica

Universidad: Universidad CAECE
Carrera: Licenciatura en Ciencia de Datos
Autora: Chiara Camila Romano
Año: 2026