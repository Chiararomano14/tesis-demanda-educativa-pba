
from pathlib import Path
import ast
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / "dataset_modelado_features.csv")

configuraciones = pd.read_csv(
    MODELOS_DIR / "arima_territorial_validacion.csv"
)

predicciones = []
fallos = []

print("========== TEST ARIMA TERRITORIAL ==========")

for numero, fila in enumerate(
    configuraciones.itertuples(index=False), start=1
):
    partido = fila.partido
    nivel = fila.nivel

    if pd.isna(fila.arima_orden):
        continue

    orden = tuple(ast.literal_eval(fila.arima_orden))

    grupo = df[
        (df["partido"] == partido) &
        (df["nivel"] == nivel)
    ].sort_values("anio")

    train = grupo[grupo["anio"].between(2012, 2023)]
    test = grupo[grupo["anio"].between(2024, 2025)]

    if (
        len(train) != 12 or
        len(test) != 2 or
        train["matricula"].isna().any()
    ):
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "Datos insuficientes"
        })
        continue

    try:
        modelo = ARIMA(
            train["matricula"].to_numpy(dtype=float),
            order=orden,
            trend="n",
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        ajuste = modelo.fit()

        if not ajuste.mle_retvals.get("converged", True):
            raise ValueError("El modelo no convergió")

        pred = np.asarray(ajuste.forecast(steps=2))
        if not np.isfinite(pred).all():
            raise ValueError("Predicción no finita")

        pred = np.maximum(pred, 0)

        persistencia = float(train["matricula"].iloc[-1])

        for anio, real, estimado in zip(
            test["anio"],
            test["matricula"],
            pred
        ):
            predicciones.append({
                "partido": partido,
                "nivel": nivel,
                "anio": int(anio),
                "matricula_real": float(real),
                "arima": float(estimado),
                "persistencia": persistencia
            })

    except Exception as error:
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": str(error)
        })

    if numero % 50 == 0:
        print(f"Procesadas {numero} de {len(configuraciones)}")

pred_df = pd.DataFrame(predicciones)
fallos_df = pd.DataFrame(fallos)

pred_df.to_csv(
    MODELOS_DIR / "predicciones_test_arima_territorial.csv",
    index=False
)

fallos_df.to_csv(
    MODELOS_DIR / "fallos_test_arima_territorial.csv",
    index=False
)

print("\n========== RESULTADOS ==========")
print("Series con predicciones:", len(pred_df) // 2)
print("Series con fallos:", len(fallos_df))

if not pred_df.empty:
    print("\n========== MAE TERRITORIAL POR NIVEL ==========")

    for nivel, grupo in pred_df.groupby("nivel"):
        mae_arima = np.mean(
            np.abs(grupo["matricula_real"] - grupo["arima"])
        )
        mae_persistencia = np.mean(
            np.abs(
                grupo["matricula_real"] - grupo["persistencia"]
            )
        )

        print(
            f"{nivel}: "
            f"ARIMA={mae_arima:.2f} | "
            f"Persistencia={mae_persistencia:.2f}"
        )

    print("\n========== MAE PROVINCIAL POR NIVEL ==========")

    provincial = pred_df.groupby(
        ["nivel", "anio"], as_index=False
    )[["matricula_real", "arima", "persistencia"]].sum()

    for nivel, grupo in provincial.groupby("nivel"):
        mae_arima = np.mean(
            np.abs(grupo["matricula_real"] - grupo["arima"])
        )
        mae_persistencia = np.mean(
            np.abs(
                grupo["matricula_real"] - grupo["persistencia"]
            )
        )

        print(
            f"{nivel}: "
            f"ARIMA={mae_arima:.2f} | "
            f"Persistencia={mae_persistencia:.2f}"
        )

print("\nArchivos guardados correctamente.")
