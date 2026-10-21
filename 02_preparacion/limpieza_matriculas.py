import os
import pandas as pd

# ETAPA 4 - CONSTRUCCIÓN DEL DATASET
# LIMPIEZA DE MATRÍCULA 2012-2025

carpeta_matriculas = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /educacion/Matriculas 2011 - 2025"
)

columnas_inicial = [
    "lactantes",
    "deambulantes",
    "s2",
    "s3",
    "s4",
    "s5"
]

columnas_primaria = [
    "_1",
    "_2",
    "_3",
    "_4",
    "_5",
    "_6"
]

columnas_secundaria = [
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12"
]

datos_matricula = []

# 1. LEER Y LIMPIAR CADA AÑO

for anio in range(2012, 2026):

    archivo_anio = None

    for archivo in os.listdir(carpeta_matriculas):

        if (
            str(anio) in archivo
            and archivo.lower().endswith(".csv")
        ):
            archivo_anio = os.path.join(
                carpeta_matriculas,
                archivo
            )
            break

    if archivo_anio is None:
        print("No se encontró:", anio)
        continue

    df = pd.read_csv(
        archivo_anio,
        sep=";",
        encoding="latin1",
        low_memory=False
    )

    df.columns = df.columns.str.strip()

    if "Departamento" in df.columns:
        df = df.rename(
            columns={
                "Departamento": "departamento"
            }
        )

    df = df[
        df["provincia"]
        .astype(str)
        .str.strip()
        == "Buenos Aires"
    ].copy()

    df = df[
        df["departamento"]
        .astype(str)
        .str.strip()
        .str.upper()
        != "ENMASCARADO"
    ].copy()

    columnas_numericas = (
        columnas_inicial
        + columnas_primaria
        + columnas_secundaria
    )

    for columna in columnas_numericas:

        if columna not in df.columns:
            df[columna] = pd.NA

        df[columna] = pd.to_numeric(
            df[columna],
            errors="coerce"
        )

    # Si todas las columnas de un nivel están vacías,
    # el resultado queda como NaN y no se convierte en 0.

    df["matricula_inicial"] = (
        df[columnas_inicial]
        .sum(
            axis=1,
            min_count=1
        )
    )

    df["matricula_primaria"] = (
        df[columnas_primaria]
        .sum(
            axis=1,
            min_count=1
        )
    )

    df["matricula_secundaria"] = (
        df[columnas_secundaria]
        .sum(
            axis=1,
            min_count=1
        )
    )

    df["anio"] = anio

    datos_matricula.append(
        df[
            [
                "departamento",
                "anio",
                "sector",
                "ambito",
                "matricula_inicial",
                "matricula_primaria",
                "matricula_secundaria"
            ]
        ]
    )

# 2. UNIR TODOS LOS AÑOS

matricula_historica = pd.concat(
    datos_matricula,
    ignore_index=True
)

# 3. PASAR A FORMATO LARGO

matricula_larga = matricula_historica.melt(
    id_vars=[
        "departamento",
        "anio",
        "sector",
        "ambito"
    ],
    value_vars=[
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria"
    ],
    var_name="nivel",
    value_name="matricula"
)

matricula_larga["nivel"] = (
    matricula_larga["nivel"]
    .str.replace(
        "matricula_",
        "",
        regex=False
    )
    .str.capitalize()
)

# 4. MATRÍCULA TOTAL POR PARTIDO, AÑO Y NIVEL

matricula_partido = (
    matricula_larga
    .groupby(
        [
            "departamento",
            "anio",
            "nivel"
        ],
        as_index=False
    )["matricula"]
    .sum(min_count=1)
)

# 5. REVISAR RESULTADO

print("\nPERÍODO:")
print(
    matricula_partido["anio"].min(),
    "-",
    matricula_partido["anio"].max()
)

print("\nCANTIDAD DE AÑOS:")
print(
    matricula_partido["anio"].nunique()
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    matricula_partido["departamento"].nunique()
)

print("\nNIVELES:")
print(
    matricula_partido["nivel"].unique()
)

print("\nDIMENSIONES:")
print(
    matricula_partido.shape
)

print("\nPARTIDOS POR AÑO:")
print(
    matricula_partido
    .groupby("anio")["departamento"]
    .nunique()
)

# 6. VALIDAR CALIDAD DEL DATASET LIMPIO

print("\nVALORES NULOS:")
print(
    matricula_partido
    .isna()
    .sum()
)

print("\nFILAS DUPLICADAS:")
print(
    matricula_partido
    .duplicated(
        subset=[
            "departamento",
            "anio",
            "nivel"
        ]
    )
    .sum()
)

print("\nVALORES NEGATIVOS DE MATRÍCULA:")
print(
    (
        matricula_partido["matricula"] < 0
    ).sum()
)

print("\nVALORES DE MATRÍCULA IGUALES A CERO:")
print(
    (
        matricula_partido["matricula"] == 0
    ).sum()
)

print("\nTIPOS DE DATOS:")
print(
    matricula_partido.dtypes
)

print("\nRESUMEN DE MATRÍCULA:")
print(
    matricula_partido["matricula"]
    .describe()
)

# 7. REVISAR REGISTROS CON MATRÍCULA FALTANTE

matriculas_faltantes = matricula_partido[
    matricula_partido["matricula"].isna()
]

print("\nREGISTROS CON MATRÍCULA FALTANTE:")
print(
    matriculas_faltantes
    .to_string(index=False)
)
# --------------------------------------------------------------
print('--------------------------------------------------------------')

# 8. NORMALIZAR NOMBRES TERRITORIALES

matricula_partido["departamento"] = (
    matricula_partido["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Corregir diferencias de nomenclatura conocidas

matricula_partido["departamento"] = (
    matricula_partido["departamento"]
    .replace({
        "CORONEL DE MARINA L ROSALES":
        "CORONEL DE MARINA LEONARDO ROSALES"
    })
)

# Renombrar departamento como partido

matricula_partido = matricula_partido.rename(
    columns={
        "departamento": "partido"
    }
)

# 9. AJUSTAR TIPOS DE DATOS

matricula_partido["anio"] = (
    matricula_partido["anio"]
    .astype(int)
)

matricula_partido["matricula"] = (
    matricula_partido["matricula"]
    .astype("Int64")
)

# 10. VALIDAR NORMALIZACIÓN

print("\nCANTIDAD DE PARTIDOS DESPUÉS DE NORMALIZAR:")
print(
    matricula_partido["partido"]
    .nunique()
)

print("\nCOLUMNAS FINALES:")
print(
    matricula_partido.columns.tolist()
)

print("\nTIPOS DE DATOS FINALES:")
print(
    matricula_partido.dtypes
)

print("\nPRIMERAS 15 FILAS DEL DATASET LIMPIO:")
print(
    matricula_partido
    .head(15)
    .to_string(index=False)
)

print("\nVALORES FALTANTES FINALES:")
print(
    matricula_partido
    .isna()
    .sum()
)

# 11. GUARDAR DATASET LIMPIO

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)

os.makedirs(
    carpeta_salida,
    exist_ok=True
)

archivo_salida = os.path.join(
    carpeta_salida,
    "matricula_limpia.csv"
)

matricula_partido.to_csv(
    archivo_salida,
    index=False,
    encoding="utf-8-sig"
)

print("\nDATASET GUARDADO EN:")
print(archivo_salida)
