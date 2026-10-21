import os
import pandas as pd

# ETAPA 4 - CONSTRUCCIÓN DEL DATASET
# LIMPIEZA DE NACIMIENTOS 2012-2022

archivo_nacimientos = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /nacimientos/"
    "nacimientos_por_departamento_y_anio_2012_2022.csv"
)

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)

# 1. LEER DATASET

df = pd.read_csv(
    archivo_nacimientos,
    encoding="utf-8",
    low_memory=False
)

# 2. FILTRAR PROVINCIA DE BUENOS AIRES

nacimientos_pba = df[
    df["provincia_nombre"]
    .astype(str)
    .str.strip()
    == "Buenos Aires"
].copy()

# 3. SELECCIONAR VARIABLES NECESARIAS

nacimientos_limpio = nacimientos_pba[
    [
        "departamento_nombre",
        "anio",
        "nacimientos_cantidad",
        "poblacion_total",
        "tbn"
    ]
].copy()

# 4. NORMALIZAR NOMBRE DE VARIABLES

nacimientos_limpio = nacimientos_limpio.rename(
    columns={
        "departamento_nombre": "partido",
        "nacimientos_cantidad": "nacimientos"
    }
)

# 5. NORMALIZAR NOMBRES DE PARTIDOS

nacimientos_limpio["partido"] = (
    nacimientos_limpio["partido"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# 6. NORMALIZAR TIPOS DE DATOS

nacimientos_limpio["anio"] = pd.to_numeric(
    nacimientos_limpio["anio"],
    errors="coerce"
).astype("Int64")

nacimientos_limpio["nacimientos"] = pd.to_numeric(
    nacimientos_limpio["nacimientos"],
    errors="coerce"
).astype("Int64")

nacimientos_limpio["poblacion_total"] = pd.to_numeric(
    nacimientos_limpio["poblacion_total"],
    errors="coerce"
).astype("Int64")

nacimientos_limpio["tbn"] = pd.to_numeric(
    nacimientos_limpio["tbn"],
    errors="coerce"
)

# 7. ORDENAR DATASET

nacimientos_limpio = (
    nacimientos_limpio
    .sort_values(
        [
            "partido",
            "anio"
        ]
    )
    .reset_index(drop=True)
)

# 8. VALIDAR RESULTADO FINAL

print("\nPERÍODO:")
print(
    nacimientos_limpio["anio"].min(),
    "-",
    nacimientos_limpio["anio"].max()
)

print("\nCANTIDAD DE AÑOS:")
print(
    nacimientos_limpio["anio"].nunique()
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    nacimientos_limpio["partido"].nunique()
)

print("\nDIMENSIONES:")
print(
    nacimientos_limpio.shape
)

print("\nCOLUMNAS FINALES:")
print(
    nacimientos_limpio.columns.tolist()
)

print("\nTIPOS DE DATOS:")
print(
    nacimientos_limpio.dtypes
)

print("\nVALORES NULOS:")
print(
    nacimientos_limpio
    .isna()
    .sum()
)

print("\nFILAS DUPLICADAS:")
print(
    nacimientos_limpio
    .duplicated(
        subset=[
            "partido",
            "anio"
        ]
    )
    .sum()
)

print("\nPRIMERAS 15 FILAS:")
print(
    nacimientos_limpio
    .head(15)
    .to_string(index=False)
)

# 9. GUARDAR DATASET LIMPIO

os.makedirs(
    carpeta_salida,
    exist_ok=True
)

archivo_salida = os.path.join(
    carpeta_salida,
    "nacimientos_limpios.csv"
)

nacimientos_limpio.to_csv(
    archivo_salida,
    index=False,
    encoding="utf-8-sig"
)

print("\nDATASET GUARDADO EN:")
print(archivo_salida)