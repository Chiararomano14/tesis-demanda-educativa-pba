
from pathlib import Path
import ast
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

proyecciones = pd.read_csv(
    MODELOS_DIR / "proyecciones_arima_territorial_2026_2035.csv"
)

casos = [
    ("BRAGADO", "INICIAL"),
    ("BRAGADO", "PRIMARIA"),
    ("GUAMINI", "INICIAL"),
    ("MORON", "PRIMARIA")
]

# Normalizar nombres para evitar problemas con tildes
import unicodedata

def normalizar(texto):
    texto = str(texto).upper().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

historico["partido_normalizado"] = (
    historico["partido"].apply(normalizar)
)

proyecciones["partido_normalizado"] = (
    proyecciones["partido"].apply(normalizar)
)

for partido, nivel in casos:

    datos = historico[
        (historico["partido_normalizado"] == partido) &
        (historico["nivel"] == nivel)
    ].sort_values("anio")

    futuro = proyecciones[
        (proyecciones["partido_normalizado"] == partido) &
        (proyecciones["nivel"] == nivel)
    ].sort_values("anio")

    print(f"\n========== {partido} - {nivel} ==========")

    if datos.empty or futuro.empty:
        print("No se encontraron datos para esta serie.")
        continue

    print("\nMATRÍCULA HISTÓRICA")
    print(
        datos[["anio", "matricula"]]
        .to_string(index=False)
    )

    print("\nPROYECCIONES GUARDADAS")
    print(
        futuro[["anio", "matricula_predicha", "orden_arima"]]
        .to_string(index=False)
    )

    orden = tuple(
        ast.literal_eval(futuro["orden_arima"].iloc[0])
    )

    datos = datos[datos["anio"].between(2012, 2025)].copy()
    y = datos["matricula"].to_numpy(dtype=float)

    try:
        modelo = ARIMA(
            y,
            order=orden,
            trend="n",
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        ajuste = modelo.fit()

        pred_original = np.asarray(
            ajuste.forecast(steps=10),
            dtype=float
        )

        print("\nPREDICCIONES ANTES DE CORREGIR NEGATIVOS")

        comparacion = pd.DataFrame({
            "anio": range(2026, 2036),
            "prediccion_original": pred_original,
            "prediccion_guardada": futuro[
                "matricula_predicha"
            ].to_numpy()
        })

        print(
            comparacion.round(2).to_string(index=False)
        )

        print("\n¿Convergió?:",
              ajuste.mle_retvals.get("converged", True))

    except Exception as error:
        print("Error al ajustar:", error)

    print("\nPERSISTENCIA COMO REFERENCIA")
    print("Matrícula 2025:", y[-1])

print("\nRevisión finalizada.")
