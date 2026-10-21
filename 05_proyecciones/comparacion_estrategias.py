# 1. IMPORTAR LIBRERÍAS

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


# 2. DEFINIR RUTAS

RUTA_MODELADO = Path(__file__).resolve().parent

ruta_modelos = (
    RUTA_MODELADO.parent / "04_modelado" / "predicciones_multianuales.csv"
)

ruta_tendencia = (
    RUTA_MODELADO.parent / "04_modelado" / "predicciones_tendencia_historica.csv"
)


# 3. CARGAR RESULTADOS

modelos = pd.read_csv(ruta_modelos)

tendencia = pd.read_csv(ruta_tendencia)

print("COMPARACIÓN FINAL DE ESTRATEGIAS")

print("\nPredicciones anteriores:", modelos.shape)
print("Predicciones de tendencia:", tendencia.shape)


# 4. UNIR LAS TRES ESTRATEGIAS

columnas_clave = [
    "partido",
    "nivel",
    "anio",
    "horizonte"
]

comparacion = modelos.merge(
    tendencia[
        columnas_clave + ["prediccion_tendencia"]
    ],
    on=columnas_clave,
    how="inner",
    validate="one_to_one"
)

print("\nObservaciones después de unir:", len(comparacion))


# 5. CONTROLAR OBSERVACIONES

print("\nObservaciones por horizonte:")

print(
    comparacion.groupby(
        "horizonte"
    ).size()
)

print("\nValores faltantes:")

print(
    comparacion[
        [
            "matricula_real",
            "baseline",
            "random_forest",
            "prediccion_tendencia"
        ]
    ].isna().sum()
)


# 6. CALCULAR MÉTRICAS

def calcular_metricas(
    reales,
    predicciones
):

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

    positivos = reales > 0

    mape = np.mean(
        np.abs(
            (
                reales[positivos]
                - predicciones[positivos]
            )
            / reales[positivos]
        )
    ) * 100

    return mae, rmse, mape


# 7. EVALUAR CADA ESTRATEGIA

resultados = []

estrategias = {
    "Baseline": "baseline",
    "Random Forest": "random_forest",
    "Tendencia": "prediccion_tendencia"
}

for horizonte, grupo in comparacion.groupby(
    "horizonte"
):

    for nombre, columna in estrategias.items():

        mae, rmse, mape = calcular_metricas(
            grupo["matricula_real"],
            grupo[columna]
        )

        resultados.append({

            "horizonte": horizonte,
            "modelo": nombre,
            "observaciones": len(grupo),
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })


metricas = pd.DataFrame(resultados)


# 8. MOSTRAR COMPARACIÓN

print("\n")
print("MÉTRICAS SOBRE LAS MISMAS OBSERVACIONES")

print(
    metricas.sort_values(
        ["horizonte", "MAE"]
    ).to_string(index=False)
)


# 9. IDENTIFICAR MEJOR MAE POR HORIZONTE

mejores = (
    metricas
    .sort_values("MAE")
    .drop_duplicates("horizonte")
    .sort_values("horizonte")
)


print("\n")
print("MEJOR ESTRATEGIA SEGÚN MAE")

print(
    mejores[
        [
            "horizonte",
            "modelo",
            "MAE",
            "RMSE",
            "MAPE"
        ]
    ].to_string(index=False)
)


# 10. GUARDAR RESULTADOS

comparacion.to_csv(
    RUTA_MODELADO
    / "predicciones_comparacion_estrategias.csv",
    index=False
)

metricas.to_csv(
    RUTA_MODELADO
    / "metricas_comparacion_estrategias.csv",
    index=False
)

mejores.to_csv(
    RUTA_MODELADO
    / "mejores_estrategias_por_horizonte.csv",
    index=False
)


print("\nResultados guardados correctamente.")