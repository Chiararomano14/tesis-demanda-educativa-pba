
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / "dataset_modelado_features.csv")
df = df[df["anio"].between(2012, 2025)].copy()

# Configuraciones ARIMA sencillas
CONFIGURACIONES = [
    (0, 1, 0),
    (1, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 1, 1),
]

resultados = []
predicciones = []
excluidas = []

grupos = df.groupby(["partido", "nivel"])

print("========== VALIDACIÓN ARIMA TERRITORIAL ==========")
print("Series encontradas:", len(grupos))

for numero, ((partido, nivel), grupo) in enumerate(grupos, start=1):

    grupo = grupo.sort_values("anio")

    # Solo series completas
    if len(grupo) != 14 or grupo["matricula"].isna().any():
        excluidas.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "Serie histórica incompleta"
        })
        continue

    entrenamiento = grupo[grupo["anio"].between(2012, 2019)]
    validacion = grupo[grupo["anio"].between(2020, 2023)]

    y_train = entrenamiento["matricula"].to_numpy(dtype=float)
    y_real = validacion["matricula"].to_numpy(dtype=float)

    mejor_mae = np.inf
    mejor_configuracion = None
    mejor_prediccion = None

    for orden in CONFIGURACIONES:
        try:
            modelo = ARIMA(
                y_train,
                order=orden,
                trend="n",
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            ajuste = modelo.fit()

            # Descartar ajustes sin convergencia
            if not ajuste.mle_retvals.get("converged", True):
                continue

            pred = np.asarray(ajuste.forecast(steps=4))

            if not np.isfinite(pred).all():
                continue

            pred = np.maximum(pred, 0)
            mae = np.mean(np.abs(y_real - pred))

            if mae < mejor_mae:
                mejor_mae = mae
                mejor_configuracion = orden
                mejor_prediccion = pred

        except Exception:
            continue

    # Persistencia: matrícula de 2019 durante 2020-2023
    pred_persistencia = np.repeat(y_train[-1], 4)
    mae_persistencia = np.mean(
        np.abs(y_real - pred_persistencia)
    )

    resultados.append({
        "partido": partido,
        "nivel": nivel,
        "arima_orden": str(mejor_configuracion),
        "mae_arima": (
            round(mejor_mae, 2)
            if mejor_configuracion is not None else np.nan
        ),
        "mae_persistencia": round(mae_persistencia, 2),
        "arima_mejora_persistencia": (
            bool(mejor_mae < mae_persistencia)
            if mejor_configuracion is not None else False
        )
    })

    if mejor_prediccion is not None:
        for anio, real, estimado in zip(
            validacion["anio"],
            y_real,
            mejor_prediccion
        ):
            predicciones.append({
                "partido": partido,
                "nivel": nivel,
                "anio": int(anio),
                "matricula_real": real,
                "prediccion_arima": round(float(estimado), 2)
            })

    if numero % 25 == 0:
        print(f"Procesadas {numero} de {len(grupos)} series")

resultados_df = pd.DataFrame(resultados)
predicciones_df = pd.DataFrame(predicciones)
excluidas_df = pd.DataFrame(excluidas)

resultados_df.to_csv(
    MODELOS_DIR / "arima_territorial_validacion.csv",
    index=False
)

predicciones_df.to_csv(
    MODELOS_DIR / "arima_territorial_predicciones_validacion.csv",
    index=False
)

excluidas_df.to_csv(
    MODELOS_DIR / "arima_territorial_series_excluidas.csv",
    index=False
)

validas = resultados_df.dropna(subset=["mae_arima"])

print("\n========== RESULTADOS GENERALES ==========")
print("Series completas evaluadas:", len(resultados_df))
print("Series con ARIMA válido:", len(validas))
print("Series sin ARIMA válido:", len(resultados_df) - len(validas))
print("Series incompletas excluidas:", len(excluidas_df))

if not validas.empty:
    print(
        "ARIMA mejora persistencia en:",
        int(validas["arima_mejora_persistencia"].sum()),
        "series"
    )

    print("\n========== MAE PROMEDIO POR NIVEL ==========")
    print(
        validas.groupby("nivel")[
            ["mae_arima", "mae_persistencia"]
        ].mean().round(2).to_string()
    )

    print("\n========== CONFIGURACIONES SELECCIONADAS ==========")
    print(
        validas["arima_orden"]
        .value_counts()
        .to_string()
    )

print("\nArchivos guardados correctamente.")
