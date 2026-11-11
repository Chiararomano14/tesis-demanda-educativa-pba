
from pathlib import Path
import logging
import warnings

import numpy as np
import pandas as pd
from prophet import Prophet

warnings.filterwarnings("ignore")
logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
logging.getLogger("prophet").setLevel(logging.ERROR)

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

DATASET = BASE_DIR / "dataset_modelado_features.csv"
VALIDACION = MODELOS_DIR / "prophet_territorial_validacion.csv"

SALIDA_PREDICCIONES = MODELOS_DIR / "predicciones_test_prophet_territorial.csv"
SALIDA_RESUMEN = MODELOS_DIR / "resultados_test_prophet_territorial.csv"
SALIDA_FALLOS = MODELOS_DIR / "fallos_test_prophet_territorial.csv"

df = pd.read_csv(DATASET)
validacion = pd.read_csv(VALIDACION)

columnas = {"partido", "nivel", "anio", "matricula"}
assert columnas.issubset(df.columns), "Faltan columnas en el dataset."

# Solo usamos datos históricos reales.
df = df[df["anio"].between(2012, 2025)].copy()
df = df.dropna(subset=["matricula"])

config_cols = {"partido", "nivel", "n_changepoints", "changepoint_prior_scale"}
assert config_cols.issubset(validacion.columns), (
    f"Faltan columnas en la validación: {config_cols - set(validacion.columns)}"
)

assert not validacion.duplicated(["partido", "nivel"]).any(), (
    "Hay configuraciones duplicadas."
)

predicciones = []
resumen = []
fallos = []

configuraciones = validacion[
    ["partido", "nivel", "n_changepoints", "changepoint_prior_scale"]
].drop_duplicates()

total = len(configuraciones)

for i, config in enumerate(configuraciones.itertuples(index=False), start=1):
    partido = config.partido
    nivel = config.nivel

    serie = df[
        (df["partido"] == partido) &
        (df["nivel"] == nivel)
    ].sort_values("anio")

    train = serie[serie["anio"].between(2012, 2023)]
    test = serie[serie["anio"].between(2024, 2025)]

    if (
        len(train) != 12
        or len(test) != 2
        or train["anio"].tolist() != list(range(2012, 2024))
        or test["anio"].tolist() != [2024, 2025]
    ):
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "Historial incompleto para entrenamiento o test"
        })
        continue

    try:
        datos_prophet = pd.DataFrame({
            "ds": pd.to_datetime(train["anio"].astype(str) + "-01-01"),
            "y": train["matricula"].to_numpy(dtype=float)
        })

        modelo = Prophet(
            growth="linear",
            n_changepoints=int(config.n_changepoints),
            changepoint_prior_scale=float(config.changepoint_prior_scale),
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False,
            uncertainty_samples=0
        )

        modelo.fit(datos_prophet)

        futuro = pd.DataFrame({
            "ds": pd.to_datetime(["2024-01-01", "2025-01-01"])
        })

        pronostico = modelo.predict(futuro)
        estimaciones = np.maximum(
            pronostico["yhat"].to_numpy(dtype=float),
            0
        )

        if not np.isfinite(estimaciones).all():
            raise ValueError("Prophet produjo predicciones no finitas.")

        reales = test["matricula"].to_numpy(dtype=float)
        persistencia = float(train.iloc[-1]["matricula"])

        for anio, real, estimado in zip(
            [2024, 2025], reales, estimaciones
        ):
            predicciones.append({
                "partido": partido,
                "nivel": nivel,
                "anio": anio,
                "matricula_real": float(real),
                "prophet": float(estimado),
                "persistencia": persistencia
            })

        resumen.append({
            "partido": partido,
            "nivel": nivel,
            "n_changepoints": int(config.n_changepoints),
            "changepoint_prior_scale": float(config.changepoint_prior_scale),
            "mae_prophet": float(np.mean(np.abs(reales - estimaciones))),
            "mae_persistencia": float(np.mean(np.abs(reales - persistencia)))
        })

    except Exception as e:
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": str(e)
        })

    if i % 25 == 0 or i == total:
        print(f"Procesadas {i} de {total} series", flush=True)

pred_df = pd.DataFrame(predicciones)
resumen_df = pd.DataFrame(resumen)
fallos_df = pd.DataFrame(
    fallos, columns=["partido", "nivel", "motivo"]
)

pred_df.to_csv(SALIDA_PREDICCIONES, index=False)
resumen_df.to_csv(SALIDA_RESUMEN, index=False)
fallos_df.to_csv(SALIDA_FALLOS, index=False)

print("\n========== TEST PROPHET TERRITORIAL ==========")
print(f"Series evaluadas: {len(resumen_df)}")
print(f"Series con fallos: {len(fallos_df)}")
print(f"Predicciones generadas: {len(pred_df)}")

if not resumen_df.empty:
    print("\nMAE PROMEDIO POR NIVEL")
    print(
        resumen_df.groupby("nivel")[
            ["mae_prophet", "mae_persistencia"]
        ].mean().round(2)
    )

    print("\nPROPHET MEJOR QUE PERSISTENCIA")
    print(
        int(
            (resumen_df["mae_prophet"] <
             resumen_df["mae_persistencia"]).sum()
        )
    )

if not fallos_df.empty:
    print("\nSERIES CON FALLOS")
    print(fallos_df.to_string(index=False))

print("\nArchivos guardados correctamente.")
