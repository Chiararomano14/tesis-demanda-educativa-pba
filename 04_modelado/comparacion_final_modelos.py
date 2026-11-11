
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

# 1. CARGAR PREDICCIONES DEL TEST

arima = pd.read_csv(
    MODELOS_DIR / "predicciones_test_arima_territorial_completo.csv"
)

prophet = pd.read_csv(
    MODELOS_DIR / "predicciones_test_prophet_territorial.csv"
)

rf = pd.read_csv(
    BASE_DIR / "modelado" / "predicciones_test_recursivo.csv"
)

claves = ["partido", "nivel", "anio"]

# Normalizar nombres de columnas
arima = arima[
    claves + ["matricula_real", "arima"]
].rename(
    columns={"matricula_real": "real_arima"}
)

prophet = prophet[
    claves + ["matricula_real", "prophet"]
].rename(
    columns={"matricula_real": "real_prophet"}
)

rf = rf[
    claves + ["matricula_real", "random_forest", "baseline"]
].rename(
    columns={
        "matricula_real": "real_rf",
        "baseline": "persistencia"
    }
)

# 2. UNIFICAR LOS MODELOS

for nombre, datos in [
    ("ARIMA", arima),
    ("Prophet", prophet),
    ("Random Forest", rf)
]:
    if datos.duplicated(claves).any():
        raise ValueError(
            f"Hay observaciones duplicadas en {nombre}"
        )

comparacion = arima.merge(
    prophet,
    on=claves,
    how="inner",
    validate="one_to_one"
).merge(
    rf,
    on=claves,
    how="inner",
    validate="one_to_one"
)

comparacion = comparacion[
    comparacion["anio"].isin([2024, 2025])
].copy()

# Verificar que los valores reales coincidan
for columna in ["real_prophet", "real_rf"]:
    if not np.allclose(
        comparacion["real_arima"],
        comparacion[columna],
        rtol=0,
        atol=0.001
    ):
        raise ValueError(
            f"Los valores reales no coinciden: {columna}"
        )

comparacion = comparacion.rename(
    columns={"real_arima": "matricula_real"}
).drop(
    columns=["real_prophet", "real_rf"]
)

modelos = [
    "arima",
    "prophet",
    "random_forest",
    "persistencia"
]

comparacion = comparacion.dropna(
    subset=["matricula_real"] + modelos
).copy()

# 3. CALCULAR METRICAS

def calcular_metricas(real, predicho):
    real = np.asarray(real, dtype=float)
    predicho = np.asarray(predicho, dtype=float)

    errores = real - predicho

    mae = np.mean(np.abs(errores))
    rmse = np.sqrt(np.mean(errores ** 2))

    mascara = real != 0

    if mascara.any():
        mape = np.mean(
            np.abs(
                errores[mascara] / real[mascara]
            )
        ) * 100
    else:
        mape = np.nan

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }


resultados = []

# 4. EVALUACION TERRITORIAL

for nivel, grupo in comparacion.groupby("nivel"):

    for modelo in modelos:

        metricas = calcular_metricas(
            grupo["matricula_real"],
            grupo[modelo]
        )

        resultados.append({
            "escala": "territorial",
            "nivel": nivel,
            "modelo": modelo,
            "observaciones": len(grupo),
            **metricas
        })

# 5. EVALUACION PROVINCIAL

provincial = comparacion.groupby(
    ["anio", "nivel"],
    as_index=False
)[["matricula_real"] + modelos].sum()

for nivel, grupo in provincial.groupby("nivel"):

    for modelo in modelos:

        metricas = calcular_metricas(
            grupo["matricula_real"],
            grupo[modelo]
        )

        resultados.append({
            "escala": "provincial",
            "nivel": nivel,
            "modelo": modelo,
            "observaciones": len(grupo),
            **metricas
        })

resultados = pd.DataFrame(resultados)

# 6. GUARDAR ARCHIVOS

comparacion.to_csv(
    MODELOS_DIR / "predicciones_test_comparacion_final.csv",
    index=False
)

provincial.to_csv(
    MODELOS_DIR / "predicciones_provinciales_comparacion_final.csv",
    index=False
)

resultados.to_csv(
    MODELOS_DIR / "metricas_comparacion_final.csv",
    index=False
)

# 7. MOSTRAR RESULTADOS

print("\n========== COMPARACION FINAL DE MODELOS ==========")

print("\nOBSERVACIONES COMPARABLES")
print("Total:", len(comparacion))

print("\nOBSERVACIONES POR NIVEL")
print(
    comparacion.groupby("nivel").size().to_string()
)

print("\nMETRICAS TERRITORIALES")
print(
    resultados[
        resultados["escala"] == "territorial"
    ].round(2).to_string(index=False)
)

print("\nMETRICAS PROVINCIALES")
print(
    resultados[
        resultados["escala"] == "provincial"
    ].round(2).to_string(index=False)
)

print("\nMEJOR MODELO POR NIVEL SEGUN MAE")

mejores = (
    resultados.sort_values("MAE")
    .groupby(["escala", "nivel"], as_index=False)
    .first()
)

print(
    mejores[
        ["escala", "nivel", "modelo", "MAE"]
    ].round(2).to_string(index=False)
)

print("\nArchivos guardados correctamente.")
