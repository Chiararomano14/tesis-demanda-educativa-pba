import pandas as pd
import numpy as np
from pathlib import Path



# 1. RUTAS


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_MODELADO = RUTA_PROYECTO / "04_modelado"

ruta_train = RUTA_MODELADO / "train.csv"
ruta_validacion = RUTA_MODELADO / "validacion.csv"
ruta_test = RUTA_MODELADO / "test.csv"



# 2. CARGAR DATOS


train = pd.read_csv(ruta_train)
validacion = pd.read_csv(ruta_validacion)
test = pd.read_csv(ruta_test)

print("\n")

print("VALIDACIÓN FINAL DEL DATASET DE MODELADO")




# 3. ESTRUCTURA GENERAL


print("\n=== ESTRUCTURA GENERAL ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:
    print(f"\n{nombre}")
    print("Filas:", len(datos))
    print("Columnas:", len(datos.columns))
    print("Partidos:", datos["partido"].nunique())
    print("Niveles:", datos["nivel"].nunique())
    print(
        "Años:",
        datos["anio"].min(),
        "-",
        datos["anio"].max()
    )



# 4. CONTROL DE DUPLICADOS


print("\n=== DUPLICADOS EN CLAVE PARTIDO + AÑO + NIVEL ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:

    duplicados = datos.duplicated(
        subset=["partido", "anio", "nivel"]
    ).sum()

    print(nombre, ":", duplicados)



# 5. CONTROL DE VARIABLE OBJETIVO


print("\n=== FALTANTES EN VARIABLE OBJETIVO ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:

    faltantes = datos["matricula"].isna().sum()

    print(nombre, ":", faltantes)



# 6. CONTROL DE NIVELES EDUCATIVOS


print("\n=== NIVELES EDUCATIVOS ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:

    niveles = sorted(
        datos["nivel"].dropna().unique()
    )

    print(nombre, ":", niveles)



# 7. CONTROL DE LAGS


variables_lag = [
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3"
]

print("\n=== FALTANTES EN LAGS ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:

    print(f"\n{nombre}")

    print(
        datos[variables_lag]
        .isna()
        .sum()
    )



# 8. CONTROL DE VALORES INFINITOS


print("\n=== VALORES INFINITOS ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:

    columnas_numericas = datos.select_dtypes(
        include=[np.number]
    )

    cantidad_infinitos = np.isinf(
        columnas_numericas
    ).sum().sum()

    print(nombre, ":", cantidad_infinitos)



# 9. CONTROL DE MATRÍCULAS NEGATIVAS


print("\n=== MATRÍCULAS NEGATIVAS ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACIÓN", validacion),
    ("TEST", test)
]:

    negativas = (
        datos["matricula"] < 0
    ).sum()

    print(nombre, ":", negativas)



# 10. CONTROL DEL ORDEN TEMPORAL


orden_temporal = (
    train["anio"].max()
    < validacion["anio"].min()
    < test["anio"].min()
)

print("\n=== ORDEN TEMPORAL ===")
print("Correcto:", orden_temporal)



# 11. CONTROL DE SUPERPOSICIÓN DE AÑOS


anios_train = set(train["anio"].unique())
anios_validacion = set(validacion["anio"].unique())
anios_test = set(test["anio"].unique())

superposicion = (
    (anios_train & anios_validacion)
    | (anios_train & anios_test)
    | (anios_validacion & anios_test)
)

print("\n=== SUPERPOSICIÓN DE AÑOS ===")
print("Años repetidos entre conjuntos:", superposicion)



# 12. RESUMEN AUTOMÁTICO


duplicados_totales = (
    train.duplicated(
        subset=["partido", "anio", "nivel"]
    ).sum()
    +
    validacion.duplicated(
        subset=["partido", "anio", "nivel"]
    ).sum()
    +
    test.duplicated(
        subset=["partido", "anio", "nivel"]
    ).sum()
)

objetivos_faltantes = (
    train["matricula"].isna().sum()
    +
    validacion["matricula"].isna().sum()
    +
    test["matricula"].isna().sum()
)

matriculas_negativas = (
    (train["matricula"] < 0).sum()
    +
    (validacion["matricula"] < 0).sum()
    +
    (test["matricula"] < 0).sum()
)


validacion_general = (
    duplicados_totales == 0
    and objetivos_faltantes == 0
    and matriculas_negativas == 0
    and orden_temporal
    and len(superposicion) == 0
)


print("\n")
print("RESULTADO FINAL")
print(
    "Dataset apto para comenzar modelado:",
    validacion_general
)

