
# 1. IMPORTAR LIBRERÍAS


from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error



# 2. DEFINIR RUTAS


RUTA_MODELADO = Path(__file__).resolve().parent
RUTA_PROYECTO = RUTA_MODELADO.parent

ruta_dataset = (
    RUTA_PROYECTO
    / "01_datos" / "dataset_modelado_features.csv"
)



# 3. CARGAR DATOS


df = pd.read_csv(ruta_dataset)

df = df.sort_values(
    ["partido", "nivel", "anio"]
).reset_index(drop=True)


print("EVALUACIÓN MULTIANUAL")


print("\nDataset cargado:", df.shape)



# 4. DEFINIR VARIABLES


variables_modelo = [
    "partido",
    "nivel",
    "anio",
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]

categoricas = [
    "partido",
    "nivel"
]

numericas = [
    "anio",
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]



# 5. DEFINIR PERÍODOS


ANIO_INICIO_TRAIN = 2015
ANIO_FIN_TRAIN = 2019

ANIO_INICIO_PREDICCION = 2020
ANIO_FIN_PREDICCION = 2023

print("\nEntrenamiento:")
print(
    ANIO_INICIO_TRAIN,
    "-",
    ANIO_FIN_TRAIN
)

print("\nPredicción:")
print(
    ANIO_INICIO_PREDICCION,
    "-",
    ANIO_FIN_PREDICCION
)



# 6. PREPARAR ENTRENAMIENTO


train = df[
    (df["anio"] >= ANIO_INICIO_TRAIN)
    & (df["anio"] <= ANIO_FIN_TRAIN)
].copy()

train = train.dropna(
    subset=variables_modelo + ["matricula"]
)

X_train = train[variables_modelo]
y_train = train["matricula"]

print("\nFilas de entrenamiento:", len(train))



# 7. CREAR RANDOM FOREST


preprocesamiento = ColumnTransformer(
    transformers=[
        (
            "categoricas",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categoricas
        ),
        (
            "numericas",
            "passthrough",
            numericas
        )
    ]
)

modelo = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
        (
            "modelo",
            RandomForestRegressor(
                n_estimators=300,
                max_depth=None,
                min_samples_leaf=2,
                max_features=0.7,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

modelo.fit(X_train, y_train)

print("\nRandom Forest entrenado correctamente.")



# 8. CREAR HISTORIAL HASTA 2019


historial = df[
    (df["anio"] <= ANIO_FIN_TRAIN)
    & (df["matricula"].notna())
][
    ["partido", "nivel", "anio", "matricula"]
].copy()

historial = historial.sort_values(
    ["partido", "nivel", "anio"]
)



# 9. FUNCIÓN PARA GENERAR VARIABLES

def construir_variables(
    partido,
    nivel,
    anio,
    historial_serie
):

    # Ordenar historial
    historial_serie = historial_serie.sort_values(
        "anio"
    )

    # Años que necesitamos para predecir
    anios_necesarios = [
        anio - 1,
        anio - 2,
        anio - 3
    ]

    # Buscar las matrículas correspondientes
    datos_necesarios = historial_serie[
        historial_serie["anio"].isin(
            anios_necesarios
        )
    ]

    # Verificar que estén los tres años
    if len(datos_necesarios) != 3:
        return None

    # Verificar que no haya matrículas faltantes
    if datos_necesarios["matricula"].isna().any():
        return None

    # Crear diccionario año -> matrícula
    matriculas_por_anio = dict(
        zip(
            datos_necesarios["anio"],
            datos_necesarios["matricula"]
        )
    )

    # Obtener rezagos exactos
    lag_1 = matriculas_por_anio[anio - 1]
    lag_2 = matriculas_por_anio[anio - 2]
    lag_3 = matriculas_por_anio[anio - 3]

    # Calcular variación anual
    if lag_2 == 0:
        variacion = 0
    else:
        variacion = (
            lag_1 - lag_2
        ) / lag_2

    # Calcular tendencia de tres años
    tendencia = (
        lag_1 - lag_3
    ) / 2

    return {
        "partido": partido,
        "nivel": nivel,
        "anio": anio,
        "matricula_lag_1": lag_1,
        "matricula_lag_2": lag_2,
        "matricula_lag_3": lag_3,
        "variacion_anual_matricula": variacion,
        "tendencia_3_anios": tendencia
    }



# 10. GENERAR PREDICCIONES RECURSIVAS


resultados = []

series = (
    historial[
        ["partido", "nivel"]
    ]
    .drop_duplicates()
)

for _, serie in series.iterrows():

    partido = serie["partido"]
    nivel = serie["nivel"]

    historial_serie = historial[
        (historial["partido"] == partido)
        & (historial["nivel"] == nivel)
    ].copy()

    # Verificar que existan los tres años anteriores
    # al inicio de las predicciones

    anios_iniciales = [
        ANIO_FIN_TRAIN,
        ANIO_FIN_TRAIN - 1,
        ANIO_FIN_TRAIN - 2
    ]

    historial_inicial = historial_serie[
        historial_serie["anio"].isin(
            anios_iniciales
        )
    ]

    if len(historial_inicial) != 3:
        continue

    ultima_matricula_real = (
        historial_serie
        .sort_values("anio")["matricula"]
        .iloc[-1]
    )

    for anio in range(
        ANIO_INICIO_PREDICCION,
        ANIO_FIN_PREDICCION + 1
    ):

        variables = construir_variables(
            partido,
            nivel,
            anio,
            historial_serie
        )

        if variables is None:
            continue

        X_futuro = pd.DataFrame([variables])

        prediccion_rf = float(
            modelo.predict(X_futuro)[0]
        )

        prediccion_rf = max(
            0,
            prediccion_rf
        )

        prediccion_baseline = (
            ultima_matricula_real
        )

        real = df[
            (df["partido"] == partido)
            & (df["nivel"] == nivel)
            & (df["anio"] == anio)
        ]["matricula"]

        valor_real = (
            real.iloc[0]
            if len(real) > 0
            else np.nan
        )

        resultados.append({
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "horizonte": (
                anio - ANIO_FIN_TRAIN
            ),
            "matricula_real": valor_real,
            "baseline": prediccion_baseline,
            "random_forest": prediccion_rf
        })

        nueva_fila = pd.DataFrame([{
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "matricula": prediccion_rf
        }])

        historial_serie = pd.concat(
            [historial_serie, nueva_fila],
            ignore_index=True
        )



# 11. CREAR RESULTADOS


resultados = pd.DataFrame(resultados)

resultados_validos = resultados.dropna(
    subset=["matricula_real"]
).copy()

print("\nPredicciones generadas:", len(resultados))
print("Predicciones evaluables:", len(resultados_validos))



# 12. CALCULAR MÉTRICAS POR HORIZONTE


metricas = []

for horizonte, grupo in resultados_validos.groupby(
    "horizonte"
):

    reales = grupo["matricula_real"]

    for nombre_modelo in [
        "baseline",
        "random_forest"
    ]:

        predicciones = grupo[nombre_modelo]

        mae = mean_absolute_error(
            reales,
            predicciones
        )

        rmse = np.sqrt(
            mean_squared_error(
                reales,
                predicciones
            )
        )

        mascara = reales != 0

        mape = np.mean(
            np.abs(
                (
                    reales[mascara]
                    - predicciones[mascara]
                )
                / reales[mascara]
            )
        ) * 100

        metricas.append({
            "horizonte": horizonte,
            "modelo": nombre_modelo,
            "observaciones": len(grupo),
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })


metricas = pd.DataFrame(metricas)



# 13. MOSTRAR RESULTADOS


print("\n")

print("RESULTADOS MULTIANUALES")


print(
    metricas.to_string(
        index=False
    )
)



# 14. GUARDAR ARCHIVOS


ruta_predicciones = (
    RUTA_MODELADO
    / "predicciones_multianuales.csv"
)

ruta_metricas = (
    RUTA_MODELADO
    / "metricas_multianuales.csv"
)

resultados.to_csv(
    ruta_predicciones,
    index=False
)

metricas.to_csv(
    ruta_metricas,
    index=False
)

print("\nArchivos guardados correctamente:")
print(ruta_predicciones)
print(ruta_metricas)