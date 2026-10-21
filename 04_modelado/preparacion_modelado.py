import pandas as pd
from pathlib import Path



# 1. CARGAR DATASET MAESTRO

RUTA_PROYECTO = Path(__file__).resolve().parent.parent

ruta_maestro = RUTA_PROYECTO / "01_datos" / "dataset_maestro_final.csv"

df = pd.read_csv(ruta_maestro)

print("\n=== DATASET MAESTRO ===")
print("Filas:", df.shape[0])
print("Columnas:", df.shape[1])
print("Partidos:", df["partido"].nunique())
print("Años:", df["anio"].min(), "-", df["anio"].max())



# 2. TRANSFORMAR MATRÍCULA DE FORMATO ANCHO A FORMATO LARGO

columnas_matricula = [
    "matricula_inicial",
    "matricula_primaria",
    "matricula_secundaria"
]

df_modelado = df.melt(
    id_vars=[
        columna
        for columna in df.columns
        if columna not in columnas_matricula
    ],
    value_vars=columnas_matricula,
    var_name="nivel",
    value_name="matricula"
)



# 3. LIMPIAR NOMBRE DEL NIVEL

df_modelado["nivel"] = (
    df_modelado["nivel"]
    .str.replace("matricula_", "", regex=False)
    .str.upper()
)

print("\n=== NIVELES EDUCATIVOS ===")
print(df_modelado["nivel"].value_counts())



# 4. ORDENAR DATASET

df_modelado = df_modelado.sort_values(
    by=["partido", "anio", "nivel"]
).reset_index(drop=True)



# 5. CONTROLES ESTRUCTURALES

print("\n=== DATASET DE MODELADO ===")
print("Filas:", df_modelado.shape[0])
print("Columnas:", df_modelado.shape[1])

print("\nPartidos:", df_modelado["partido"].nunique())
print("Años:", df_modelado["anio"].min(), "-", df_modelado["anio"].max())
print("Cantidad de niveles:", df_modelado["nivel"].nunique())

print("\nNiveles:")
print(df_modelado["nivel"].unique())



# 6. CONTROLAR CLAVE PARTIDO + AÑO + NIVEL

duplicados = df_modelado.duplicated(
    subset=["partido", "anio", "nivel"]
).sum()

print("\n=== CONTROL DE DUPLICADOS ===")
print("Duplicados partido-año-nivel:", duplicados)



# 7. REVISAR MATRÍCULA HISTÓRICA Y FUTURA

print("\n=== MATRÍCULA DISPONIBLE POR AÑO ===")

resumen_matricula = (
    df_modelado
    .groupby("anio")["matricula"]
    .agg(
        registros="size",
        disponibles="count"
    )
)

resumen_matricula["faltantes"] = (
    resumen_matricula["registros"]
    - resumen_matricula["disponibles"]
)

print(resumen_matricula)



# 8. MOSTRAR EJEMPLO DE LA NUEVA ESTRUCTURA

print("\n=== EJEMPLO DEL DATASET ===")

print(
    df_modelado[
        ["partido", "anio", "nivel", "matricula"]
    ].head(15)
)



# 9. GUARDAR DATASET DE MODELADO

ruta_salida = RUTA_PROYECTO / "01_datos" / "dataset_modelado.csv"

df_modelado.to_csv(
    ruta_salida,
    index=False
)

print("\nDataset guardado correctamente:")
print(ruta_salida)
# 10. AUDITORÍA DE DISPONIBILIDAD TEMPORAL DE VARIABLES

print("\n")
print("AUDITORÍA DE DISPONIBILIDAD TEMPORAL DE VARIABLES")

# Variables que no necesitamos auditar como predictoras
columnas_excluir = [
    "partido",
    "anio",
    "nivel",
    "matricula"
]

variables_candidatas = [
    columna
    for columna in df_modelado.columns
    if columna not in columnas_excluir
]

resultados_disponibilidad = []

for variable in variables_candidatas:

    datos_variable = df_modelado[
        df_modelado[variable].notna()
    ]

    if len(datos_variable) > 0:

        anio_min = datos_variable["anio"].min()
        anio_max = datos_variable["anio"].max()

        cantidad_anios = datos_variable["anio"].nunique()

        anios_disponibles = sorted(
            datos_variable["anio"].unique()
        )

        cantidad_datos = datos_variable[variable].count()

    else:

        anio_min = None
        anio_max = None
        cantidad_anios = 0
        anios_disponibles = []
        cantidad_datos = 0

    resultados_disponibilidad.append({
        "variable": variable,
        "anio_min": anio_min,
        "anio_max": anio_max,
        "cantidad_anios": cantidad_anios,
        "cantidad_datos": cantidad_datos,
        "anios_disponibles": anios_disponibles
    })


disponibilidad = pd.DataFrame(resultados_disponibilidad)


# 11. MOSTRAR RESUMEN

print("\n=== RESUMEN DE DISPONIBILIDAD ===")

print(
    disponibilidad[
        [
            "variable",
            "anio_min",
            "anio_max",
            "cantidad_anios",
            "cantidad_datos"
        ]
    ].to_string(index=False)
)


# 12. VARIABLES DISPONIBLES HASTA 2035

variables_futuras = disponibilidad[
    disponibilidad["anio_max"] == 2035
]

print("\n=== VARIABLES CON INFORMACIÓN HASTA 2035 ===")

print(
    variables_futuras[
        [
            "variable",
            "anio_min",
            "anio_max",
            "cantidad_anios"
        ]
    ].to_string(index=False)
)


# 13. VARIABLES DISPONIBLES SOLO EN 2022

variables_2022 = disponibilidad[
    (disponibilidad["anio_min"] == 2022)
    &
    (disponibilidad["anio_max"] == 2022)
]

print("\n=== VARIABLES DISPONIBLES SOLO EN 2022 ===")

print(
    variables_2022[
        ["variable", "cantidad_datos"]
    ].to_string(index=False)
)


# 14. VARIABLES CON INFORMACIÓN HISTÓRICA

variables_historicas = disponibilidad[
    disponibilidad["cantidad_anios"] > 1
]

print("\n=== VARIABLES CON MÁS DE UN AÑO DE INFORMACIÓN ===")

print(
    variables_historicas[
        [
            "variable",
            "anio_min",
            "anio_max",
            "cantidad_anios"
        ]
    ].to_string(index=False)
)


# 15. GUARDAR AUDITORÍA

ruta_disponibilidad = (
    RUTA_PROYECTO
    / "04_modelado"
    / "disponibilidad_variables.csv"
)

disponibilidad.to_csv(
    ruta_disponibilidad,
    index=False
)

print("\nAuditoría guardada correctamente:")
print(ruta_disponibilidad)


# 16. CREAR CARACTERÍSTICAS TEMPORALES DE MATRÍCULA


print("\n")
print("CREACIÓN DE CARACTERÍSTICAS TEMPORALES")

# Es fundamental ordenar antes de crear variables temporales
df_modelado = df_modelado.sort_values(
    by=["partido", "nivel", "anio"]
).reset_index(drop=True)



# 17. LAGS DE MATRÍCULA


df_modelado["matricula_lag_1"] = (
    df_modelado
    .groupby(["partido", "nivel"])["matricula"]
    .shift(1)
)

df_modelado["matricula_lag_2"] = (
    df_modelado
    .groupby(["partido", "nivel"])["matricula"]
    .shift(2)
)

df_modelado["matricula_lag_3"] = (
    df_modelado
    .groupby(["partido", "nivel"])["matricula"]
    .shift(3)
)



# 18. VARIACIÓN ANUAL DE MATRÍCULA


df_modelado["variacion_anual_matricula"] = (
    (
        df_modelado["matricula_lag_1"]
        - df_modelado["matricula_lag_2"]
    )
    / df_modelado["matricula_lag_2"]
)



# 19. TENDENCIA RECIENTE DE 3 AÑOS


# Calculamos el cambio promedio anual de los últimos
# tres valores conocidos anteriores al año a predecir.

df_modelado["tendencia_3_anios"] = (
    (
        df_modelado["matricula_lag_1"]
        - df_modelado["matricula_lag_3"]
    )
    / 2
)



# 20. CONTROLES


print("\n=== CARACTERÍSTICAS CREADAS ===")

nuevas_caracteristicas = [
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]

for variable in nuevas_caracteristicas:

    print(
        variable,
        "- datos disponibles:",
        df_modelado[variable].notna().sum()
    )



# 21. EJEMPLO PARA UN PARTIDO Y NIVEL


ejemplo = df_modelado[
    (df_modelado["partido"] == "PILAR")
    &
    (df_modelado["nivel"] == "INICIAL")
][
    [
        "partido",
        "anio",
        "nivel",
        "matricula",
        "matricula_lag_1",
        "matricula_lag_2",
        "matricula_lag_3",
        "variacion_anual_matricula",
        "tendencia_3_anios"
    ]
]

print("\n=== EJEMPLO: PILAR - INICIAL ===")
print(ejemplo.to_string(index=False))



# 22. GUARDAR DATASET CON NUEVAS CARACTERÍSTICAS


ruta_salida_features = (
    RUTA_PROYECTO
    / "01_datos" / "dataset_modelado_features.csv"
)

df_modelado.to_csv(
    ruta_salida_features,
    index=False
)

print("\nDataset con características guardado correctamente:")
print(ruta_salida_features)


# 23. CONTROL BÁSICO DE DATA LEAKAGE


print("\n")
print("CONTROL BÁSICO DE DATA LEAKAGE")


# Variables que NO deben utilizarse directamente
# como predictoras del mismo año

variables_excluidas_leakage = [
    "matricula",
    "matricula_total"
]

print("\n=== VARIABLES EXCLUIDAS COMO PREDICTORAS DIRECTAS ===")

for variable in variables_excluidas_leakage:
    print("-", variable)



# 24. COMPROBAR LAGS


df_historico = df_modelado[
    df_modelado["matricula"].notna()
].copy()

control_lag_1 = (
    df_historico["matricula_lag_1"]
    == df_historico
        .groupby(["partido", "nivel"])["matricula"]
        .shift(1)
)

errores_lag_1 = (
    control_lag_1[
        df_historico["matricula_lag_1"].notna()
    ]
    == False
).sum()

print("\n=== CONTROL TEMPORAL DE LAG 1 ===")
print("Errores detectados:", errores_lag_1)



# 25. RESUMEN DE REGLAS TEMPORALES


print("\n=== REGLAS PARA EL MODELADO ===")

print("1. La matrícula del año objetivo NO puede utilizarse como predictor.")
print("2. matricula_total del mismo año queda excluida.")
print("3. Los lags utilizan únicamente años anteriores.")
print("4. Las variables del Censo 2022 no se copiarán hacia años anteriores.")
print("5. Las variables futuras solo podrán utilizarse si son proyecciones conocidas.")
print("6. La división train/validación/test deberá respetar el orden temporal.")


# 26. DEFINIR DIVISIÓN TEMPORAL


print("\n")
print("=" * 70)
print("DIVISIÓN TEMPORAL: TRAIN / VALIDACIÓN / TEST")
print("=" * 70)


# Trabajamos únicamente con años donde conocemos
# la variable objetivo.

df_modelado_historico = df_modelado[
    df_modelado["matricula"].notna()
].copy()



# 27. ASIGNAR CONJUNTO SEGÚN EL AÑO


def asignar_conjunto(anio):

    if 2015 <= anio <= 2021:
        return "TRAIN"

    elif 2022 <= anio <= 2023:
        return "VALIDACION"

    elif 2024 <= anio <= 2025:
        return "TEST"

    else:
        return "FUERA"


df_modelado_historico["conjunto"] = (
    df_modelado_historico["anio"]
    .apply(asignar_conjunto)
)



# 28. FILTRAR PERÍODO UTILIZADO


df_modelado_historico = df_modelado_historico[
    df_modelado_historico["conjunto"] != "FUERA"
].copy()



# 29. CREAR TRAIN, VALIDACIÓN Y TEST


train = df_modelado_historico[
    df_modelado_historico["conjunto"] == "TRAIN"
].copy()

validacion = df_modelado_historico[
    df_modelado_historico["conjunto"] == "VALIDACION"
].copy()

test = df_modelado_historico[
    df_modelado_historico["conjunto"] == "TEST"
].copy()



# 30. CONTROLES


print("\n=== TRAIN ===")
print("Años:", train["anio"].min(), "-", train["anio"].max())
print("Filas:", len(train))

print("\n=== VALIDACIÓN ===")
print(
    "Años:",
    validacion["anio"].min(),
    "-",
    validacion["anio"].max()
)
print("Filas:", len(validacion))

print("\n=== TEST ===")
print("Años:", test["anio"].min(), "-", test["anio"].max())
print("Filas:", len(test))



# 31. CONTROLAR ORDEN TEMPORAL


orden_temporal_correcto = (
    train["anio"].max()
    < validacion["anio"].min()
    < test["anio"].min()
)

print("\n=== CONTROL TEMPORAL ===")
print("Orden temporal correcto:", orden_temporal_correcto)



# 32. CONTROL DE LAGS COMPLETOS


variables_lag = [
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3"
]

print("\n=== FALTANTES EN LAGS ===")

for nombre, datos in [
    ("TRAIN", train),
    ("VALIDACION", validacion),
    ("TEST", test)
]:

    print(f"\n{nombre}")

    print(
        datos[variables_lag]
        .isna()
        .sum()
    )



# 33. GUARDAR CONJUNTOS


ruta_train = RUTA_PROYECTO / "04_modelado" / "train.csv"
ruta_validacion = RUTA_PROYECTO / "04_modelado" / "validacion.csv"
ruta_test = RUTA_PROYECTO / "04_modelado" / "test.csv"

train.to_csv(ruta_train, index=False)
validacion.to_csv(ruta_validacion, index=False)
test.to_csv(ruta_test, index=False)

print("\nConjuntos guardados correctamente:")
print(ruta_train)
print(ruta_validacion)
print(ruta_test)