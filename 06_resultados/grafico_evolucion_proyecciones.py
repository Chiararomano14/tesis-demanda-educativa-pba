
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

print("\n========== ARCHIVOS PARA FIGURA 10 ==========")

# Archivos de proyecciones ARIMA y Prophet
archivos = [
    MODELOS_DIR / "proyecciones_arima_territorial_2026_2035_completas.csv",
    MODELOS_DIR / "proyecciones_prophet_territorial_2026_2035_completas.csv",
    BASE_DIR / "dataset_modelado_features.csv"
]

for archivo in archivos:

    print(f"\nARCHIVO: {archivo.name}")

    if archivo.exists():
        df = pd.read_csv(archivo)
        print("Filas:", len(df))
        print("Columnas:", list(df.columns))
    else:
        print("NO ENCONTRADO")

# Buscar archivos de proyecciones de Random Forest
print("\n========== POSIBLES ARCHIVOS RANDOM FOREST ==========")

for archivo in BASE_DIR.rglob("*.csv"):

    nombre = archivo.name.lower()

    if (
        "proyeccion" in nombre
        or "forecast" in nombre
    ):
        print(archivo.relative_to(BASE_DIR))

print("\nRevision finalizada.")

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELADO_DIR = BASE_DIR / "modelado"

archivos = [
    "proyecciones_provinciales_2026_2035.csv",
    "proyecciones_matricula_2026_2035.csv",
    "proyecciones_por_nivel_2026_2035.csv"
]

print("\n========== REVISION RANDOM FOREST ==========")

for nombre in archivos:

    ruta = MODELADO_DIR / nombre

    print(f"\nARCHIVO: {nombre}")

    if not ruta.exists():
        print("Archivo no encontrado.")
        continue

    df = pd.read_csv(ruta)

    print("Filas:", len(df))
    print("Columnas:", list(df.columns))

    print("\nPrimeras filas:")
    print(df.head(5).to_string(index=False))

    print("\nUltimas filas:")
    print(df.tail(3).to_string(index=False))

print("\nRevision finalizada.")

print("--------------------------------------------------------------------------------")


# ============================================================
# 4. REVISION DE CORRECCIONES Y CASOS ESPECIALES
# ============================================================

print("\n========== CORRECCIONES DE PROYECCIONES ==========")

archivos_revision = {
    "Registro de correcciones Prophet":
        MODELOS_DIR / "registro_correcciones_estabilidad_prophet.csv",

    "Registro de proyecciones ARIMA":
        MODELOS_DIR / "registro_proyecciones_arima.csv",

    "Registro de proyecciones Prophet":
        MODELOS_DIR / "registro_proyecciones_prophet.csv",

    "Fallos de proyecciones ARIMA":
        MODELOS_DIR / "fallos_proyecciones_arima.csv",

    "Fallos de proyecciones Prophet":
        MODELOS_DIR / "fallos_proyecciones_prophet.csv"
}

for nombre, ruta in archivos_revision.items():

    print(f"\n--- {nombre} ---")

    if not ruta.exists():
        print("Archivo no encontrado")
        continue

    try:
        df_revision = pd.read_csv(ruta)

    except pd.errors.EmptyDataError:
        print("Archivo CSV vacio, sin registros para analizar.")
        continue

    print("Filas:", len(df_revision))
    print("Columnas:", df_revision.columns.tolist())

    if not df_revision.empty:
        print("\nPrimeras filas:")
        print(
            df_revision.head(10).to_string(index=False)
        )
    else:
        print("Archivo vacio")

# ------------------------------------------------------------
# 4.1. METODOS UTILIZADOS EN ARIMA DEFINITIVO
# ------------------------------------------------------------

print("\n========== METODOS ARIMA DEFINITIVOS ==========")

arima_final = pd.read_csv(
    MODELOS_DIR /
    "proyecciones_arima_territorial_2026_2035_completas.csv"
)

print("\nDistribucion de metodos:")
print(
    arima_final["metodo"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nSeries por metodo:")
print(
    arima_final.groupby("metodo")[["partido", "nivel"]]
    .apply(
        lambda grupo: grupo.drop_duplicates().shape[0]
    )
    .to_string()
)

# ------------------------------------------------------------
# 4.2. CASOS CON HISTORIAL INCOMPLETO
# ------------------------------------------------------------

print("\n========== SERIES HISTORICAS INCOMPLETAS ==========")

historico_completo = pd.read_csv(
    BASE_DIR / "dataset_modelado_features.csv"
)

historico_completo = historico_completo[
    historico_completo["anio"].between(2012, 2025)
]

conteo_historico = (
    historico_completo.groupby(["partido", "nivel"])
    ["matricula"]
    .count()
)

incompletas = conteo_historico[
    conteo_historico < 14
]

print("Cantidad de series incompletas:", len(incompletas))
print(incompletas.to_string())

print("\n========== REVISION DE CORRECCIONES FINALIZADA ==========")

