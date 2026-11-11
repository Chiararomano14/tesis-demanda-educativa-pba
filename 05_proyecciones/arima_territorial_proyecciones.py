
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

correcciones = pd.read_csv(
    MODELOS_DIR / "registro_correcciones_arima.csv"
)

# Configuraciones alternativas definidas previamente
ordenes_corregidos = {
    (fila["partido"], fila["nivel"]): tuple(
        ast.literal_eval(fila["orden_utilizado"])
    )
    for _, fila in correcciones.iterrows()
    if pd.notna(fila["orden_utilizado"])
}

proyecciones = []
registro = []
fallos = []

ANIOS_FUTUROS = list(range(2026, 2036))

print("========== PROYECCIONES ARIMA TERRITORIAL ==========")

for numero, fila in enumerate(
    configuraciones.itertuples(index=False), start=1
):
    partido = fila.partido
    nivel = fila.nivel

    if pd.isna(fila.arima_orden):
        continue

    orden_validacion = tuple(
        ast.literal_eval(fila.arima_orden)
    )

    grupo = df[
        (df["partido"] == partido) &
        (df["nivel"] == nivel) &
        (df["anio"].between(2012, 2025))
    ].sort_values("anio")

    # Por ahora trabajamos con las 403 series completas
    if len(grupo) != 14 or grupo["matricula"].isna().any():
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "Serie histórica incompleta"
        })
        continue

    y = grupo["matricula"].to_numpy(dtype=float)

    # Usar primero el orden que funcionó en el test
    orden_preferido = ordenes_corregidos.get(
        (partido, nivel),
        orden_validacion
    )

    opciones = list(dict.fromkeys([
        orden_preferido,
        (1, 1, 0),
        (0, 1, 0)
    ]))

    prediccion = None
    orden_utilizado = None

    for orden in opciones:
        try:
            modelo = ARIMA(
                y,
                order=orden,
                trend="n",
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            ajuste = modelo.fit()

            if not ajuste.mle_retvals.get("converged", True):
                continue

            valores = np.asarray(
                ajuste.forecast(steps=10),
                dtype=float
            )

            if not np.isfinite(valores).all():
                continue

            prediccion = np.maximum(valores, 0)
            orden_utilizado = orden
            break

        except Exception:
            continue

    if prediccion is None:
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "Ninguna configuración ARIMA convergió"
        })
        continue

    for anio, estimado in zip(ANIOS_FUTUROS, prediccion):
        proyecciones.append({
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "matricula_predicha": round(float(estimado), 2),
            "orden_arima": str(orden_utilizado),
            "metodo": "ARIMA"
        })

    registro.append({
        "partido": partido,
        "nivel": nivel,
        "orden_validacion": str(orden_validacion),
        "orden_utilizado": str(orden_utilizado),
        "cambio_configuracion": orden_utilizado != orden_validacion
    })

    if numero % 50 == 0:
        print(f"Procesadas {numero} de {len(configuraciones)} series")

proyecciones_df = pd.DataFrame(proyecciones)
registro_df = pd.DataFrame(registro)
fallos_df = pd.DataFrame(fallos)

proyecciones_df.to_csv(
    MODELOS_DIR / "proyecciones_arima_territorial_2026_2035.csv",
    index=False
)

registro_df.to_csv(
    MODELOS_DIR / "registro_proyecciones_arima.csv",
    index=False
)

fallos_df.to_csv(
    MODELOS_DIR / "fallos_proyecciones_arima.csv",
    index=False
)

print("\n========== RESULTADOS GENERALES ==========")
print("Series proyectadas:", len(registro_df))
print("Series con fallos:", len(fallos_df))
print("Filas de proyecciones:", len(proyecciones_df))

if not registro_df.empty:
    print(
        "Series con cambio de configuración:",
        int(registro_df["cambio_configuracion"].sum())
    )

if not proyecciones_df.empty:
    # Totales por año y nivel
    totales_nivel = (
        proyecciones_df.groupby(
            ["anio", "nivel"], as_index=False
        )["matricula_predicha"]
        .sum()
    )

    totales_nivel.to_csv(
        MODELOS_DIR / "totales_arima_territorial_por_nivel.csv",
        index=False
    )

    # Totales provinciales por año
    totales_provinciales = (
        proyecciones_df.groupby(
            "anio", as_index=False
        )["matricula_predicha"]
        .sum()
    )

    totales_provinciales.to_csv(
        MODELOS_DIR / "totales_arima_territorial_provincial.csv",
        index=False
    )

    print("\n========== PROYECCIÓN PROVINCIAL ==========")
    print(totales_provinciales.to_string(index=False))

    print("\n========== PROYECCIÓN 2035 POR NIVEL ==========")
    print(
        totales_nivel[
            totales_nivel["anio"] == 2035
        ].to_string(index=False)
    )

print("\n========== FALLOS ==========")
if fallos_df.empty:
    print("Ninguno.")
else:
    print(fallos_df.to_string(index=False))

print("\nArchivos guardados correctamente.")
