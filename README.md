# Análisis y proyección de la matrícula educativa en la provincia de Buenos Aires

## Descripción del proyecto

Este repositorio contiene los datos, scripts de Python, análisis exploratorio y resultados desarrollados para el proyecto final de la Licenciatura en Ciencia de Datos de la Universidad CAECE.

La investigación analiza la evolución de la matrícula educativa en los 135 partidos de la provincia de Buenos Aires, considerando los niveles Inicial, Primario y Secundario.

El período histórico estudiado comprende los años 2012 a 2025, mientras que las proyecciones se extienden desde 2026 hasta 2035.

El objetivo es analizar cómo evolucionó la matrícula, identificar diferencias entre los partidos y evaluar distintas estrategias para estimar su comportamiento futuro.

## Fuentes de datos

Para desarrollar el proyecto se utilizaron datos públicos de organismos oficiales:

- Secretaría de Educación de la Nación: Relevamiento Anual de matrícula educativa, período 2012-2025.
- INDEC: Censo Nacional de Población, Hogares y Viviendas 2022.
- INDEC: estimaciones de población por departamento para el período 2022-2035.
- RENAPER: registros de nacimientos correspondientes al período 2012-2022.

También se analizaron variables demográficas, socioeconómicas y habitacionales para estudiar su relación con la evolución de la matrícula.

Estas variables se utilizaron principalmente durante el análisis exploratorio y no se incorporaron directamente a las proyecciones finales debido a sus limitaciones de cobertura temporal.

## Metodología

El proyecto se desarrolló en distintas etapas:

1. Recolección e inspección de las fuentes de datos.
2. Limpieza y transformación de los archivos originales.
3. Integración de las fuentes en un dataset maestro.
4. Análisis exploratorio de la evolución histórica de la matrícula.
5. Construcción de variables temporales para el modelado predictivo.
6. Entrenamiento y evaluación de modelos de regresión y aprendizaje automático.
7. Incorporación y evaluación de modelos de series temporales.
8. Comparación de los métodos mediante validación cronológica.
9. Generación y revisión de proyecciones de matrícula hasta 2035.

Durante la primera etapa se evaluaron distintos algoritmos de regresión y aprendizaje automático, entre ellos Regresión Lineal, Random Forest, Gradient Boosting y XGBoost. Random Forest presentó el mejor desempeño entre los principales algoritmos de aprendizaje automático evaluados.

Posteriormente, se incorporaron ARIMA y Prophet para ampliar el análisis mediante modelos específicos de series temporales.

La evaluación inicial utilizó la siguiente división cronológica:

- Entrenamiento: 2015-2021.
- Validación: 2022-2023.
- Prueba final: 2024-2025.

Para la comparación final de precisión se utilizaron cuatro métodos: Random Forest, ARIMA, Prophet y persistencia.

La evaluación se realizó sobre 806 observaciones correspondientes a 403 combinaciones de partido y nivel educativo, considerando los años 2024 y 2025. Se utilizaron las métricas MAE, RMSE y MAPE.

Las proyecciones para el período 2026-2035 se generaron mediante cinco estrategias:

- Persistencia.
- Extrapolación de tendencia histórica.
- Random Forest recursivo.
- ARIMA.
- Prophet.

La tendencia histórica se utilizó como un enfoque adicional de proyección, aunque no formó parte de la comparación final de precisión entre los cuatro métodos.

Las estimaciones se realizaron para los 135 partidos y los tres niveles educativos. En los casos con series históricas incompletas o proyecciones poco estables, se aplicaron procedimientos de respaldo y corrección documentados en los archivos del proyecto.

## Estructura del repositorio

### 01_datos

Contiene los principales datasets utilizados en la investigación:

- `dataset_maestro_final.csv`: integración de la información histórica y las variables analizadas.
- `dataset_modelado.csv`: datos organizados para el modelado.
- `dataset_modelado_features.csv`: dataset con variables predictoras temporales.
- `matricula_limpia_final.csv`: información de matrícula después de su procesamiento.

### 02_preparacion

Contiene los scripts utilizados para limpiar y transformar los datos de las distintas fuentes.

Incluye el procesamiento de matrícula, educación, población, nacimientos, fecundidad, economía, hogares y migraciones, además del script de integración del dataset maestro.

### 03_eda

Contiene la notebook de análisis exploratorio:

`RomanoC_Entrega2_EDA_DemandaEducativa.ipynb`

En ella se estudian la evolución histórica de la matrícula, las diferencias entre niveles educativos y partidos, y las relaciones con otras variables demográficas, socioeconómicas y habitacionales.

### 04_modelado

Contiene los scripts correspondientes a la preparación de datos, entrenamiento, validación y evaluación de los modelos.

Incluye tanto los procedimientos originales de aprendizaje automático como los nuevos modelos ARIMA y Prophet.

También reúne los archivos CSV utilizados para comparar las predicciones y los errores de Random Forest, ARIMA, Prophet y persistencia durante la evaluación final.

### 05_proyecciones

Contiene los scripts utilizados para generar las proyecciones de matrícula para el período 2026-2035.

Se incluyen los procedimientos de Random Forest, persistencia, tendencia histórica, ARIMA y Prophet, junto con los archivos definitivos de las proyecciones territoriales.

También se encuentran los procedimientos de revisión, corrección de estabilidad y tratamiento de series históricas incompletas.

### 06_resultados

Contiene los principales resultados finales del proyecto, incluyendo las métricas de evaluación, las proyecciones provinciales, las estimaciones por nivel educativo y las comparaciones territoriales.

También se incluyen las visualizaciones utilizadas para representar la evolución histórica, los errores predictivos, las proyecciones y las diferencias entre modelos.

## Resultados principales

El análisis histórico mostró diferencias entre los niveles educativos. Mientras que la matrícula de Inicial y Primario disminuyó entre 2012 y 2025, la de Secundario aumentó. En conjunto, la matrícula provincial alcanzó los 3.849.256 estudiantes en 2025.

En la evaluación inicial, la persistencia obtuvo menores errores que Random Forest. Sin embargo, la comparación final mostró que el desempeño de los modelos variaba según el nivel educativo.

Random Forest presentó el menor MAE en Inicial, ARIMA obtuvo el menor MAE en Primario y la persistencia registró los menores errores en Secundario. Prophet presentó errores superiores a los demás métodos en los tres niveles.

Las proyecciones provinciales para 2035 también mostraron resultados diferentes:

| Estrategia | Matrícula proyectada para 2035 | Variación respecto de 2025 |
|---|---:|---:|
| Persistencia | 3.849.256 | 0 % |
| Tendencia histórica | 3.233.656 | -15,99 % |
| Random Forest | 3.624.659 | -5,83 % |
| ARIMA | 3.888.584 | +1,02 % |
| Prophet | 3.934.571 | +2,22 % |

A nivel territorial, Random Forest, ARIMA y Prophet coincidieron en proyectar disminuciones en 20 partidos, mientras que en los otros 115 presentaron diferencias en la dirección de los cambios estimados.

Estos resultados muestran que las proyecciones a largo plazo dependen del método utilizado y que las estimaciones provinciales pueden ocultar comportamientos distintos entre territorios y niveles educativos.

## Requisitos técnicos

El proyecto fue desarrollado en Python, utilizando principalmente PyCharm.

Las principales bibliotecas utilizadas incluyen:

- `pandas`
- `numpy`
- `matplotlib`
- `scikit-learn`
- `statsmodels`
- `prophet`
- `pdfplumber`

Las dependencias necesarias para la ejecución del proyecto deben encontrarse especificadas en el archivo `requirements.txt`.

Para instalarlas desde la carpeta principal del proyecto:

`python -m pip install -r requirements.txt`

La instalación de las bibliotecas no garantiza por sí sola la ejecución completa del proyecto. Algunos scripts requieren los archivos originales descargados de las fuentes oficiales y pueden contener rutas que deben adaptarse al equipo donde se ejecuten.

## Cómo consultar los archivos

Para revisar el trabajo se recomienda comenzar por la notebook de `03_eda`, donde se presenta el análisis exploratorio de los datos.

Luego pueden consultarse los scripts de `04_modelado`, que documentan la preparación de variables, el entrenamiento y la evaluación de los modelos.

En `05_proyecciones` se encuentran los procedimientos utilizados para generar las cinco estrategias de proyección hasta 2035 y los archivos correspondientes a ARIMA y Prophet.

Finalmente, en `06_resultados` se presentan las principales tablas, métricas y visualizaciones obtenidas.

## Limitaciones

Las proyecciones representan estimaciones de posibles escenarios futuros y no deben interpretarse como valores definitivos.

La matrícula observada se utiliza como una aproximación a la demanda educativa, pero no representa directamente las necesidades de infraestructura, docentes, establecimientos o vacantes disponibles.

Las series históricas abarcan catorce años y la evaluación final se realizó sobre horizontes más cortos que el período proyectado hasta 2035. Por lo tanto, los resultados de largo plazo presentan incertidumbre.

Además, los modelos no incorporaron directamente posibles cambios futuros en la natalidad, las migraciones, las políticas educativas o las condiciones económicas.

Las diferencias entre los cinco enfoques permiten comparar posibles trayectorias, pero no constituyen un intervalo de confianza sobre la matrícula futura.

## Información académica

Universidad: Universidad CAECE

Carrera: Licenciatura en Ciencia de Datos

Autora: Chiara Camila Romano

Año: 2026
Información académica

Universidad: Universidad CAECE
Carrera: Licenciatura en Ciencia de Datos
Autora: Chiara Camila Romano
Año: 2026
