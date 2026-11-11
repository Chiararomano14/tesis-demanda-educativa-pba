
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
validacion = pd.read_csv(
    MODELOS_DIR / "prophet_territorial_validacion.csv"
)

# Datos históricos reales
df = df[df["anio"].between(2012, 2025)].copy()

proyecciones = []
registro = []
fallos = []

total = len(validacion)

for numero, config in enumerate(validacion.itertuples(index=False), 1):

    partido = config.partido
    nivel = config.nivel

    grupo = df[
        (df["partido"] == partido) &
        (df["nivel"] == nivel)
    ].sort_values("anio")

    # Verificar que estén los 14 años históricos
    if (
        len(grupo) != 14
        or grupo["anio"].tolist() != list(range(2012, 2026))
        or grupo["matricula"].isna().any()
    ):
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": "historial_incompleto"
        })
        continue

    datos_prophet = pd.DataFrame({
        "ds": pd.to_datetime(
            grupo["anio"].astype(str) + "-01-01"
        ),
        "y": grupo["matricula"].to_numpy(dtype=float)
    })

    futuro = pd.DataFrame({
        "ds": pd.to_datetime(
            [f"{anio}-01-01" for anio in range(2026, 2036)]
        )
    })

    try:
        modelo = Prophet(
            growth="linear",
            n_changepoints=int(config.n_changepoints),
            changepoint_prior_scale=float(
                config.changepoint_prior_scale
            ),
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False,
            uncertainty_samples=0
        )

        modelo.fit(datos_prophet)

        estimaciones_originales = modelo.predict(futuro)[
            "yhat"
        ].to_numpy(dtype=float)

        if not np.isfinite(estimaciones_originales).all():
            raise ValueError("Predicciones no finitas")

        # La matrícula no puede ser negativa
        estimaciones = np.maximum(estimaciones_originales, 0)

        for anio, estimado, original in zip(
            range(2026, 2036),
            estimaciones,
            estimaciones_originales
        ):
            proyecciones.append({
                "partido": partido,
                "nivel": nivel,
                "anio": anio,
                "prophet": float(estimado),
                "prediccion_original": float(original)
            })

        registro.append({
            "partido": partido,
            "nivel": nivel,
            "n_changepoints": int(config.n_changepoints),
            "changepoint_prior_scale": float(
                config.changepoint_prior_scale
            ),
            "matricula_2025": float(
                grupo.loc[grupo["anio"] == 2025, "matricula"].iloc[0]
            ),
            "proyeccion_2035": float(estimaciones[-1]),
            "predicciones_negativas": int(
                (estimaciones_originales < 0).sum()
            ),
            "metodo": "prophet"
        })

    except Exception as error:
        fallos.append({
            "partido": partido,
            "nivel": nivel,
            "motivo": str(error)
        })

    if numero % 25 == 0 or numero == total:
        print(
            f"Procesadas {numero} de {total} series",
            flush=True
        )

pred = pd.DataFrame(proyecciones)
reg = pd.DataFrame(registro)
errores = pd.DataFrame(
    fallos, columns=["partido", "nivel", "motivo"]
)

pred.to_csv(
    MODELOS_DIR / "proyecciones_prophet_territorial_2026_2035.csv",
    index=False
)

reg.to_csv(
    MODELOS_DIR / "registro_proyecciones_prophet.csv",
    index=False
)

errores.to_csv(
    MODELOS_DIR / "fallos_proyecciones_prophet.csv",
    index=False
)

print("\n========== PROYECCIONES PROPHET TERRITORIAL ==========")
print("Series proyectadas:", len(reg))
print("Predicciones generadas:", len(pred))
print("Series con fallos:", len(errores))

if not reg.empty:
    print(
        "Series con predicciones negativas originales:",
        int((reg["predicciones_negativas"] > 0).sum())
    )

if not pred.empty:
    por_nivel = (
        pred.groupby(["anio", "nivel"], as_index=False)["prophet"]
        .sum()
    )

    provincial = (
        pred.groupby("anio", as_index=False)["prophet"]
        .sum()
    )

    por_nivel.to_csv(
        MODELOS_DIR / "totales_prophet_territorial_por_nivel.csv",
        index=False
    )

    provincial.to_csv(
        MODELOS_DIR / "totales_prophet_territorial_provincial.csv",
        index=False
    )

    print("\nTOTAL PROVINCIAL POR AÑO")
    print(provincial.round(2).to_string(index=False))

    print("\nTOTAL POR NIVEL EN 2035")
    print(
        por_nivel[por_nivel["anio"] == 2035]
        .round(2)
        .to_string(index=False)
    )

print("\nArchivos guardados correctamente.")
