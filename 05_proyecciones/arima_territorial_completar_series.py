
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

# Archivo ARIMA con las cuatro correcciones de estabilidad
archivo = (
    MODELOS_DIR /
    "proyecciones_arima_territorial_2026_2035_corregidas.csv"
)

proyecciones = pd.read_csv(archivo)

# Series incompletas: métodos de respaldo
series_respaldo = [
    {
        "partido": "CASTELLI",
        "nivel": "SECUNDARIA",
        "matricula": 558.0,
        "orden_arima": "(0, 1, 0)",
        "metodo": "respaldo_historial_corto"
    },
    {
        "partido": "LEZAMA",
        "nivel": "SECUNDARIA",
        "matricula": 65.0,
        "orden_arima": "",
        "metodo": "persistencia_historial_incompleto"
    }
]

nuevas_filas = []

for serie in series_respaldo:
    for anio in range(2026, 2036):
        nuevas_filas.append({
            "partido": serie["partido"],
            "nivel": serie["nivel"],
            "anio": anio,
            "matricula_predicha": serie["matricula"],
            "orden_arima": serie["orden_arima"],
            "metodo": serie["metodo"]
        })

nuevas = pd.DataFrame(nuevas_filas)

# Verificar que no estén incorporadas previamente
claves = ["partido", "nivel", "anio"]

duplicadas = proyecciones.merge(
    nuevas[claves],
    on=claves,
    how="inner"
)

if not duplicadas.empty:
    raise ValueError(
        "Las series de respaldo ya están incorporadas."
    )

# Incorporar las 20 predicciones faltantes
completo = pd.concat(
    [proyecciones, nuevas],
    ignore_index=True
)

completo = completo.sort_values(
    ["partido", "nivel", "anio"]
).reset_index(drop=True)

# Controles
cantidad_series = completo[
    ["partido", "nivel"]
].drop_duplicates().shape[0]

filas_por_serie = completo.groupby(
    ["partido", "nivel"]
).size()

assert cantidad_series == 405
assert len(completo) == 4050
assert (filas_por_serie == 10).all()
assert not completo.duplicated(claves).any()
assert completo["matricula_predicha"].notna().all()
assert np.isfinite(completo["matricula_predicha"]).all()
assert (completo["matricula_predicha"] >= 0).all()

# Guardar archivo completo
completo.to_csv(
    MODELOS_DIR /
    "proyecciones_arima_territorial_2026_2035_completas.csv",
    index=False
)

# Totales por nivel
por_nivel = completo.groupby(
    ["anio", "nivel"], as_index=False
)["matricula_predicha"].sum()

por_nivel.to_csv(
    MODELOS_DIR /
    "totales_arima_territorial_completos_por_nivel.csv",
    index=False
)

# Totales provinciales
provincial = completo.groupby(
    "anio", as_index=False
)["matricula_predicha"].sum()

provincial.to_csv(
    MODELOS_DIR /
    "totales_arima_territorial_completos_provincial.csv",
    index=False
)

# Registro de las dos series incorporadas
pd.DataFrame(series_respaldo).to_csv(
    MODELOS_DIR / "registro_series_respaldo_arima.csv",
    index=False
)

print("\n========== ARIMA TERRITORIAL COMPLETO ==========")
print("Series territoriales:", cantidad_series)
print("Predicciones totales:", len(completo))
print("Series incorporadas:", len(series_respaldo))

print("\nTOTAL PROVINCIAL POR AÑO")
print(provincial.round(2).to_string(index=False))

print("\nTOTAL POR NIVEL EN 2035")
print(
    por_nivel[por_nivel["anio"] == 2035]
    .round(2)
    .to_string(index=False)
)

print("\nArchivo completo guardado correctamente.")
