
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



# 3. CARGAR DATASET


df = pd.read_csv(ruta_dataset)

df = df.sort_values(
    ["partido", "nivel", "anio"]
).reset_index(drop=True)


print("EVALUACIÓN FINAL SOBRE TEST 2024-2025")


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
ANIO_FIN_TRAIN = 2023

ANIO_INICIO_TEST = 2024
ANIO_FIN_TEST = 2025

print("\nEntrenamiento: 2015-2023")
print("Test: 2024-2025")



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



# 7. PREPARAR TEST


test = df[
    (df["anio"] >= ANIO_INICIO_TEST)
    & (df["anio"] <= ANIO_FIN_TEST)
].copy()

test_un_anio = test.dropna(
    subset=variables_modelo + ["matricula"]
).copy()

X_test = test_un_anio[variables_modelo]
y_test = test_un_anio["matricula"]

print("Filas de test:", len(test))
print(
    "Filas evaluables a un año:",
    len(test_un_anio)
)



# 8. ENTRENAR RANDOM FOREST


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



# 9. FUNCIÓN PARA CALCULAR MÉTRICAS


def calcular_metricas(reales, predicciones):

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

    reales = np.asarray(reales)
    predicciones = np.asarray(predicciones)

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

    return mae, rmse, mape



# 10. EVALUACIÓN A UN AÑO


print("\n")

print("A. EVALUACIÓN A UN AÑO")


pred_rf_un_anio = modelo.predict(
    X_test
)

pred_rf_un_anio = np.maximum(
    pred_rf_un_anio,
    0
)

pred_baseline_un_anio = (
    test_un_anio["matricula_lag_1"]
    .to_numpy()
)

metricas_un_anio = []

for nombre, predicciones in [
    ("Baseline", pred_baseline_un_anio),
    ("Random Forest", pred_rf_un_anio)
]:

    mae, rmse, mape = calcular_metricas(
        y_test,
        predicciones
    )

    metricas_un_anio.append({
        "modelo": nombre,
        "observaciones": len(y_test),
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    })

metricas_un_anio = pd.DataFrame(
    metricas_un_anio
)

print(
    metricas_un_anio.to_string(
        index=False
    )
)



# 11. PREPARAR HISTORIAL PARA PREDICCIÓN RECURSIVA


historial = df[
    (df["anio"] <= ANIO_FIN_TRAIN)
    & (df["matricula"].notna())
][
    ["partido", "nivel", "anio", "matricula"]
].copy()



# 12. FUNCIÓN PARA CONSTRUIR VARIABLES


def construir_variables(
    partido,
    nivel,
    anio,
    historial_serie
):

    anios_necesarios = [
        anio - 1,
        anio - 2,
        anio - 3
    ]

    datos = historial_serie[
        historial_serie["anio"].isin(
            anios_necesarios
        )
    ]

    if len(datos) != 3:
        return None

    if datos["matricula"].isna().any():
        return None

    matriculas = dict(
        zip(
            datos["anio"],
            datos["matricula"]
        )
    )

    lag_1 = matriculas[anio - 1]
    lag_2 = matriculas[anio - 2]
    lag_3 = matriculas[anio - 3]

    if lag_2 == 0:
        variacion = 0
    else:
        variacion = (
            lag_1 - lag_2
        ) / lag_2

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



# 13. GENERAR PREDICCIONES RECURSIVAS


resultados_recursivos = []

series = historial[
    ["partido", "nivel"]
].drop_duplicates()

for _, serie in series.iterrows():

    partido = serie["partido"]
    nivel = serie["nivel"]

    historial_serie = historial[
        (historial["partido"] == partido)
        & (historial["nivel"] == nivel)
    ].copy()

    # Verificar los tres años anteriores a 2024
    anios_iniciales = [2021, 2022, 2023]

    historial_inicial = historial_serie[
        historial_serie["anio"].isin(
            anios_iniciales
        )
    ]

    if len(historial_inicial) != 3:
        continue

    ultima_matricula_real = (
        historial_serie.loc[
            historial_serie["anio"] == 2023,
            "matricula"
        ].iloc[0]
    )

    for anio in range(
        ANIO_INICIO_TEST,
        ANIO_FIN_TEST + 1
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

        pred_rf = float(
            modelo.predict(X_futuro)[0]
        )

        pred_rf = max(0, pred_rf)

        pred_baseline = ultima_matricula_real

        real = test[
            (test["partido"] == partido)
            & (test["nivel"] == nivel)
            & (test["anio"] == anio)
        ]["matricula"]

        valor_real = (
            real.iloc[0]
            if len(real) > 0
            else np.nan
        )

        resultados_recursivos.append({
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "horizonte": anio - ANIO_FIN_TRAIN,
            "matricula_real": valor_real,
            "baseline": pred_baseline,
            "random_forest": pred_rf
        })

        nueva_fila = pd.DataFrame([{
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "matricula": pred_rf
        }])

        historial_serie = pd.concat(
            [historial_serie, nueva_fila],
            ignore_index=True
        )



# 14. CALCULAR MÉTRICAS RECURSIVAS


resultados_recursivos = pd.DataFrame(
    resultados_recursivos
)

resultados_validos = resultados_recursivos.dropna(
    subset=["matricula_real"]
).copy()

metricas_recursivas = []

for horizonte, grupo in resultados_validos.groupby(
    "horizonte"
):

    reales = grupo["matricula_real"]

    for nombre in [
        "baseline",
        "random_forest"
    ]:

        predicciones = grupo[nombre]

        mae, rmse, mape = calcular_metricas(
            reales,
            predicciones
        )

        metricas_recursivas.append({
            "horizonte": horizonte,
            "modelo": nombre,
            "observaciones": len(grupo),
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

metricas_recursivas = pd.DataFrame(
    metricas_recursivas
)



# 15. MOSTRAR RESULTADOS RECURSIVOS


print("\n")

print("B. EVALUACIÓN RECURSIVA")


print(
    metricas_recursivas.to_string(
        index=False
    )
)



# 16. GUARDAR RESULTADOS


metricas_un_anio.to_csv(
    RUTA_MODELADO / "metricas_test_un_anio.csv",
    index=False
)

metricas_recursivas.to_csv(
    RUTA_MODELADO / "metricas_test_recursivo.csv",
    index=False
)

resultados_recursivos.to_csv(
    RUTA_MODELADO / "predicciones_test_recursivo.csv",
    index=False
)

print("\nResultados guardados correctamente.")

# 17. GUARDAR PREDICCIONES INDIVIDUALES A UN AÑO

predicciones_test_un_anio = test_un_anio[
    [
        "partido",
        "nivel",
        "anio",
        "matricula"
    ]
].copy()

predicciones_test_un_anio[
    "prediccion_baseline"
] = pred_baseline_un_anio

predicciones_test_un_anio[
    "prediccion_random_forest"
] = pred_rf_un_anio


ruta_predicciones_un_anio = (
    RUTA_MODELADO
    / "predicciones_test_un_anio.csv"
)

predicciones_test_un_anio.to_csv(
    ruta_predicciones_un_anio,
    index=False
)

print(
    "\nPredicciones individuales guardadas:",
    ruta_predicciones_un_anio
)