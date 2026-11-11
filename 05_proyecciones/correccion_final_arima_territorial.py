
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

historico = pd.read_csv(
    BASE_DIR / "dataset_modelado_features.csv"
)

original = pd.read_csv(
    MODELOS_DIR / "proyecciones_arima_territorial_2026_2035.csv"
)

corregido = original.copy()

casos = [
    ("BRAGADO", "INICIAL"),
    ("BRAGADO", "PRIMARIA"),
    ("GUAMINI", "INICIAL"),
    ("MORON", "PRIMARIA")
]

orden_alternativo = (0, 1, 1)
registro = []

for partido, nivel in casos:

    datos = historico[
        (historico["partido"] == partido) &
        (historico["nivel"] == nivel) &
        (historico["anio"].between(2012, 2025))
    ].sort_values("anio")

    y = datos["matricula"].to_numpy(dtype=float)

    ajuste = ARIMA(
        y,
        order=orden_alternativo,
        trend="n",
        enforce_stationarity=False,
        enforce_invertibility=False
    ).fit()

    if not ajuste.mle_retvals.get("converged", True):
        raise RuntimeError(
            f"El modelo no convergió: {partido} - {nivel}"
        )

    pred = np.asarray(
        ajuste.forecast(steps=10),
        dtype=float
    )

    if not np.all(np.isfinite(pred)) or np.any(pred < 0):
        raise RuntimeError(
            f"Predicciones inválidas: {partido} - {nivel}"
        )

    mascara = (
        (corregido["partido"] == partido) &
        (corregido["nivel"] == nivel) &
        (corregido["anio"].between(2026, 2035))
    )

    if mascara.sum() != 10:
        raise RuntimeError(
            f"Se esperaban 10 filas: {partido} - {nivel}"
        )

    orden_original = corregido.loc[
        mascara, "orden_arima"
    ].iloc[0]

    indices = corregido.loc[mascara].sort_values(
        "anio"
    ).index

    corregido.loc[indices, "matricula_predicha"] = pred
    corregido.loc[indices, "orden_arima"] = str(
        orden_alternativo
    )
    corregido.loc[indices, "metodo"] = (
        "ajuste_estabilidad_arima"
    )

    registro.append({
        "partido": partido,
        "nivel": nivel,
        "orden_original": orden_original,
        "orden_nuevo": str(orden_alternativo),
        "motivo": "Proyeccion negativa a largo plazo"
    })

# Comprobaciones finales
assert len(corregido) == len(original)
assert not corregido["matricula_predicha"].isna().any()
assert (corregido["matricula_predicha"] >= 0).all()

# Guardar proyecciones corregidas
corregido.to_csv(
    MODELOS_DIR /
    "proyecciones_arima_territorial_2026_2035_corregidas.csv",
    index=False
)

pd.DataFrame(registro).to_csv(
    MODELOS_DIR / "registro_correcciones_estabilidad_arima.csv",
    index=False
)

# Recalcular totales
por_nivel = corregido.groupby(
    ["anio", "nivel"], as_index=False
)["matricula_predicha"].sum()

provincial = corregido.groupby(
    "anio", as_index=False
)["matricula_predicha"].sum()

por_nivel.to_csv(
    MODELOS_DIR / "totales_arima_corregidos_por_nivel.csv",
    index=False
)

provincial.to_csv(
    MODELOS_DIR / "totales_arima_corregidos_provincial.csv",
    index=False
)

print("\n========== CORRECCIÓN FINAL ARIMA ==========")
print("Series corregidas:", len(registro))
print("Filas totales:", len(corregido))

print("\nTOTAL PROYECTADO POR AÑO")
print(provincial.round(2).to_string(index=False))

print("\nTOTAL POR NIVEL EN 2035")
print(
    por_nivel[por_nivel["anio"] == 2035]
    .round(2)
    .to_string(index=False)
)

print("\nArchivos corregidos guardados.")
