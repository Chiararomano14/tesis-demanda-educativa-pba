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

df = pd.read_csv(BASE_DIR / "dataset_modelado_features.csv")
df = df[df["anio"].between(2012, 2025)].copy()

# Configuraciones de Prophet
configuraciones = [
    (0, 0.05),
    (2, 0.01),
    (2, 0.05)
]

resultados = []
predicciones = []
excluidas = []

series = list(df.groupby(["partido", "nivel"]))
total = len(series)

for numero, ((partido, nivel), grupo) in enumerate(series, 1):

    grupo = grupo.sort_values("anio").copy()

    historico = grupo[
        grupo["anio"].between(2012, 2023)
    ].copy()

    anios_disponibles = set(
        historico.loc[
            historico["matricula"].notna(), "anio"
        ]
    )

    if anios_disponibles != set(range(2012, 2024)):
        excluidas.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "historial_incompleto"
        })
        continue

    train = historico[
        historico["anio"] <= 2019
    ].copy()

    valid = historico[
        historico["anio"].between(2020, 2023)
    ].copy()

    train_prophet = pd.DataFrame({
        "ds": pd.to_datetime(
            train["anio"].astype(str) + "-01-01"
        ),
        "y": train["matricula"].to_numpy(dtype=float)
    })

    futuro = pd.DataFrame({
        "ds": pd.to_datetime(
            [f"{anio}-01-01" for anio in range(2020, 2024)]
        )
    })

    reales = valid["matricula"].to_numpy(dtype=float)

    persistencia = float(
        train["matricula"].iloc[-1]
    )

    mae_persistencia = float(
        np.mean(np.abs(reales - persistencia))
    )

    candidatos = []

    for n_changepoints, prior_scale in configuraciones:

        try:
            modelo = Prophet(
                growth="linear",
                n_changepoints=n_changepoints,
                changepoint_prior_scale=prior_scale,
                yearly_seasonality=False,
                weekly_seasonality=False,
                daily_seasonality=False,
                uncertainty_samples=0
            )

            modelo.fit(train_prophet)

            pred = modelo.predict(futuro)["yhat"].to_numpy(
                dtype=float
            )

            if not np.all(np.isfinite(pred)):
                continue

            pred = np.maximum(pred, 0)

            mae = float(
                np.mean(np.abs(reales - pred))
            )

            candidatos.append({
                "n_changepoints": n_changepoints,
                "changepoint_prior_scale": prior_scale,
                "mae": mae,
                "pred": pred
            })

        except Exception as error:
            print(
                f"Error en {partido} - {nivel}: {error}"
            )

    if not candidatos:
        excluidas.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "sin_configuracion_valida"
        })
        continue

    mejor = min(
        candidatos,
        key=lambda x: x["mae"]
    )

    resultados.append({
        "partido": partido,
        "nivel": nivel,
        "n_changepoints": mejor["n_changepoints"],
        "changepoint_prior_scale": mejor[
            "changepoint_prior_scale"
        ],
        "mae_prophet": mejor["mae"],
        "mae_persistencia": mae_persistencia,
        "prophet_mejora_persistencia": (
            mejor["mae"] < mae_persistencia
        )
    })

    for anio, real, predicha in zip(
        range(2020, 2024),
        reales,
        mejor["pred"]
    ):
        predicciones.append({
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "matricula_real": float(real),
            "prophet": float(predicha),
            "persistencia": persistencia
        })

    if numero % 25 == 0 or numero == total:
        print(
            f"Procesadas {numero} de {total} series"
        )

# Guardar resultados
res = pd.DataFrame(resultados)
pred = pd.DataFrame(predicciones)

res.to_csv(
    MODELOS_DIR / "prophet_territorial_validacion.csv",
    index=False
)

pred.to_csv(
    MODELOS_DIR / "prophet_territorial_predicciones_validacion.csv",
    index=False
)

pd.DataFrame(excluidas).to_csv(
    MODELOS_DIR / "prophet_territorial_series_excluidas.csv",
    index=False
)

print("\n========== VALIDACIÓN PROPHET TERRITORIAL ==========")

print("Series evaluadas:", len(res))
print("Series excluidas:", len(excluidas))

print(
    "Prophet mejor que persistencia:",
    int(res["prophet_mejora_persistencia"].sum())
)

print("\nMAE PROMEDIO POR NIVEL")

print(
    res.groupby("nivel")[
        ["mae_prophet", "mae_persistencia"]
    ].mean().round(2).to_string()
)

print("\nCONFIGURACIONES SELECCIONADAS")

print(
    res.groupby([
        "n_changepoints",
        "changepoint_prior_scale"
    ]).size().to_string()
)

print("\nArchivos guardados correctamente.")