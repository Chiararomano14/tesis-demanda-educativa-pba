
# 1. IMPORTAR LIBRERÍAS


from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)



# 2. DEFINIR RUTAS


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_MODELADO = Path(__file__).resolve().parent

ruta_dataset = (
    RUTA_PROYECTO / "01_datos" / "dataset_modelado_features.csv"
)

ruta_comparacion = (
    RUTA_MODELADO / "predicciones_multianuales.csv"
)



# 3. CARGAR DATOS


df = pd.read_csv(ruta_dataset)

comparacion = pd.read_csv(ruta_comparacion)


print("EVALUACIÓN HISTÓRICA DE TENDENCIA")


print("\nDataset:", df.shape)
print("Predicciones anteriores:", comparacion.shape)



# 4. DEFINIR PERÍODO DE EVALUACIÓN


ANIO_ORIGEN = 2019

ANIOS_HISTORICOS = [
    2017,
    2018,
    2019
]

ANIOS_EVALUACION = [
    2020,
    2021,
    2022,
    2023
]



# 5. PREPARAR HISTORIA


historico = df[
    df["anio"].isin(ANIOS_HISTORICOS)
][
    [
        "partido",
        "nivel",
        "anio",
        "matricula"
    ]
].copy()

historico = historico.pivot(
    index=["partido", "nivel"],
    columns="anio",
    values="matricula"
)

historico = historico.dropna(
    subset=ANIOS_HISTORICOS
)



# 6. CALCULAR TENDENCIA HISTÓRICA


# Cambio anual promedio entre 2017 y 2019.

historico["cambio_anual"] = (
    historico[2019] - historico[2017]
) / 2

# Cambio relativo anual respecto de 2019.

historico["tasa_anual"] = (
    historico["cambio_anual"]
    / historico[2019]
)



# 7. CONTROLAR TENDENCIAS EXTREMAS


# Limitamos la variación anual al rango -10 % / +10 %.
# Es un supuesto exploratorio, no una tasa oficial.

LIMITE_INFERIOR = -0.10
LIMITE_SUPERIOR = 0.10

historico["tasa_controlada"] = (
    historico["tasa_anual"]
    .clip(
        lower=LIMITE_INFERIOR,
        upper=LIMITE_SUPERIOR
    )
)



# 8. GENERAR PROYECCIONES


resultados = []

for (partido, nivel), fila in historico.iterrows():

    matricula_base = fila[2019]
    tasa = fila["tasa_controlada"]

    for anio in ANIOS_EVALUACION:

        horizonte = anio - ANIO_ORIGEN

        prediccion = (
            matricula_base
            * (1 + tasa) ** horizonte
        )

        resultados.append({

            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "horizonte": horizonte,
            "prediccion_tendencia": max(
                0,
                prediccion
            )
        })


predicciones_tendencia = pd.DataFrame(
    resultados
)



# 9. INCORPORAR MATRÍCULA REAL


reales = df[
    df["anio"].isin(ANIOS_EVALUACION)
][
    [
        "partido",
        "nivel",
        "anio",
        "matricula"
    ]
].copy()

predicciones_tendencia = (
    predicciones_tendencia
    .merge(
        reales,
        on=["partido", "nivel", "anio"],
        how="inner",
        validate="one_to_one"
    )
)

predicciones_tendencia = (
    predicciones_tendencia
    .dropna(
        subset=[
            "matricula",
            "prediccion_tendencia"
        ]
    )
)



# 10. CALCULAR MÉTRICAS


def calcular_metricas(datos):

    y_real = datos["matricula"]

    y_pred = datos["prediccion_tendencia"]

    mae = mean_absolute_error(
        y_real,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_real,
            y_pred
        )
    )

    positivos = y_real > 0

    mape = (
        np.mean(
            np.abs(
                (
                    y_real[positivos]
                    - y_pred[positivos]
                )
                / y_real[positivos]
            )
        ) * 100
    )

    return pd.Series({

        "observaciones": len(datos),
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    })


metricas_tendencia = (
    predicciones_tendencia
    .groupby("horizonte")
    .apply(
        calcular_metricas,
        include_groups=False
    )
    .reset_index()
)

metricas_tendencia["modelo"] = "tendencia"



# 11. MOSTRAR RESULTADOS


print("\n")

print("RESULTADOS DE TENDENCIA")


print(
    metricas_tendencia[
        [
            "horizonte",
            "modelo",
            "observaciones",
            "MAE",
            "RMSE",
            "MAPE"
        ]
    ].to_string(index=False)
)



# 12. GUARDAR RESULTADOS


predicciones_tendencia.to_csv(
    RUTA_MODELADO
    / "predicciones_tendencia_historica.csv",
    index=False
)

metricas_tendencia.to_csv(
    RUTA_MODELADO
    / "metricas_tendencia_historica.csv",
    index=False
)



# 13. COMPARAR CON MODELOS ANTERIORES


# Revisamos primero las columnas del archivo anterior.

print("\n")

print("COLUMNAS DE PREDICCIONES ANTERIORES")


print(comparacion.columns.tolist())


print("\n")

print("ARCHIVOS GUARDADOS CORRECTAMENTE")
