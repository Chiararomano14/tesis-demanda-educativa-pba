
from pathlib import Path
import numpy as np
import pandas as pd

MODELOS_DIR = Path(__file__).resolve().parent

# 1. CARGAR PREDICCIONES COMPARABLES

df = pd.read_csv(
    MODELOS_DIR / "predicciones_test_comparacion_final.csv"
)

modelos = [
    "arima",
    "prophet",
    "random_forest",
    "persistencia"
]

df["horizonte"] = df["anio"].map({
    2024: 1,
    2025: 2
})

if df["horizonte"].isna().any():
    raise ValueError("Se encontraron años inesperados.")

# 2. FUNCION PARA CALCULAR METRICAS

def calcular_metricas(real, predicho):

    real = np.asarray(real, dtype=float)
    predicho = np.asarray(predicho, dtype=float)

    error = real - predicho

    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error ** 2))

    mascara = real != 0

    if mascara.any():
        mape = np.mean(
            np.abs(error[mascara] / real[mascara])
        ) * 100
    else:
        mape = np.nan

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }

# 3. EVALUACION TERRITORIAL

resultados = []

for (nivel, horizonte), grupo in df.groupby(
    ["nivel", "horizonte"]
):

    for modelo in modelos:

        metricas = calcular_metricas(
            grupo["matricula_real"],
            grupo[modelo]
        )

        resultados.append({
            "escala": "territorial",
            "nivel": nivel,
            "horizonte": horizonte,
            "anio": 2023 + horizonte,
            "modelo": modelo,
            "observaciones": len(grupo),
            **metricas
        })

# 4. EVALUACION PROVINCIAL

provincial = df.groupby(
    ["anio", "horizonte", "nivel"],
    as_index=False
)[["matricula_real"] + modelos].sum()

for _, fila in provincial.iterrows():

    for modelo in modelos:

        metricas = calcular_metricas(
            [fila["matricula_real"]],
            [fila[modelo]]
        )

        resultados.append({
            "escala": "provincial",
            "nivel": fila["nivel"],
            "horizonte": int(fila["horizonte"]),
            "anio": int(fila["anio"]),
            "modelo": modelo,
            "observaciones": 1,
            **metricas
        })

resultados = pd.DataFrame(resultados)

# 5. MEJOR MODELO POR HORIZONTE

mejores = (
    resultados.sort_values("MAE")
    .groupby(
        ["escala", "nivel", "horizonte"],
        as_index=False
    )
    .first()
)

# 6. GUARDAR ARCHIVOS

resultados.to_csv(
    MODELOS_DIR / "metricas_comparacion_horizontes.csv",
    index=False
)

mejores.to_csv(
    MODELOS_DIR / "mejores_modelos_por_horizonte.csv",
    index=False
)

# 7. MOSTRAR RESULTADOS

print("\n========== COMPARACION POR HORIZONTE ==========")

print("\nOBSERVACIONES POR AÑO Y NIVEL")
print(
    df.groupby(["anio", "nivel"])
    .size()
    .to_string()
)

print("\nMAE TERRITORIAL POR HORIZONTE")

tabla = resultados[
    resultados["escala"] == "territorial"
].pivot_table(
    index=["nivel", "modelo"],
    columns="horizonte",
    values="MAE"
)

tabla.columns = [
    f"MAE_H{int(h)}" for h in tabla.columns
]

tabla["diferencia_H2_H1"] = (
    tabla["MAE_H2"] - tabla["MAE_H1"]
)

print(tabla.round(2).to_string())

print("\nMEJORES MODELOS POR HORIZONTE")
print(
    mejores[
        ["escala", "nivel", "horizonte", "modelo", "MAE"]
    ].round(2).to_string(index=False)
)

print("\nMETRICAS PROVINCIALES")
print(
    resultados[
        resultados["escala"] == "provincial"
    ][
        ["nivel", "anio", "modelo", "MAE", "MAPE"]
    ].round(2).to_string(index=False)
)

print("\nArchivos guardados correctamente.")
