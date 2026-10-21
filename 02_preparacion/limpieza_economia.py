import os
import re
import unicodedata
import pandas as pd


# ============================================================
# LIMPIEZA DE ECONOMÍA
# ECO_01 - CONDICIÓN DE ACTIVIDAD ECONÓMICA POR PARTIDO
# ============================================================

print("-" * 70)
print("LIMPIEZA DE ECONOMÍA")
print("ECO_01 - CONDICIÓN DE ACTIVIDAD ECONÓMICA POR PARTIDO")
print("-" * 70)


# ------------------------------------------------------------
# 1. RUTA DE LA CARPETA
# ------------------------------------------------------------

carpeta_economia = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /economia"
)


# ------------------------------------------------------------
# 2. BUSCAR ARCHIVO ECO_01
# ------------------------------------------------------------

archivo_eco_01 = None

for archivo in os.listdir(carpeta_economia):

    if (
        archivo.startswith("1.2")
        and archivo.lower().endswith(".xlsx")
    ):
        archivo_eco_01 = os.path.join(
            carpeta_economia,
            archivo
        )
        break


if archivo_eco_01 is None:
    raise FileNotFoundError(
        "No se encontró el archivo ECO_01"
    )


print("\nARCHIVO ECO_01:")
print(archivo_eco_01)


# ------------------------------------------------------------
# 3. LEER HOJA
# ------------------------------------------------------------

excel_eco_01 = pd.ExcelFile(
    archivo_eco_01
)

hoja_datos = excel_eco_01.sheet_names[0]

print("\nHOJA:")
print(
    repr(hoja_datos)
)


df = pd.read_excel(
    archivo_eco_01,
    sheet_name=hoja_datos,
    header=None
)


# ------------------------------------------------------------
# 4. FUNCIÓN PARA NORMALIZAR NOMBRES DE PARTIDOS
# ------------------------------------------------------------

def normalizar_partido(nombre):

    nombre = str(nombre)

    # Reemplazar espacios especiales
    nombre = nombre.replace("\xa0", " ")

    # Reemplazar saltos de línea
    nombre = nombre.replace("\n", " ")

    # Mayúsculas y espacios
    nombre = nombre.upper().strip()

    # Eliminar tildes
    nombre = unicodedata.normalize(
        "NFD",
        nombre
    )

    nombre = "".join(
        caracter
        for caracter in nombre
        if unicodedata.category(caracter) != "Mn"
    )

    # Unificar espacios múltiples
    nombre = re.sub(
        r"\s+",
        " ",
        nombre
    ).strip()

    # Equivalencias utilizadas en los demás datasets
    equivalencias = {
        "NUEVE DE JULIO": "9 DE JULIO"
    }

    nombre = equivalencias.get(
        nombre,
        nombre
    )

    return nombre


# ------------------------------------------------------------
# 5. EXTRAER FILAS CORRESPONDIENTES A PARTIDOS
# ------------------------------------------------------------

# Las filas de partidos poseen un código INDEC.
# Se excluyen:
# - Total provincial
# - 24 Partidos del Gran Buenos Aires
# - Resto de partidos
# - encabezados
# - notas y fuente

eco_01 = df[
    df[0]
    .astype(str)
    .str.strip()
    .str.fullmatch(r"\d{5}")
].copy()


# ------------------------------------------------------------
# 6. SELECCIONAR VARIABLES
# ------------------------------------------------------------

eco_01 = eco_01[
    [
        1,
        2,
        3,
        4,
        5,
        6
    ]
].copy()


eco_01.columns = [
    "partido",
    "poblacion_14_mas",
    "pea",
    "ocupados",
    "desocupados",
    "poblacion_no_economicamente_activa"
]


# ------------------------------------------------------------
# 7. NORMALIZAR PARTIDOS
# ------------------------------------------------------------

eco_01["partido"] = (
    eco_01["partido"]
    .apply(normalizar_partido)
)


# ------------------------------------------------------------
# 8. CONVERTIR VARIABLES NUMÉRICAS
# ------------------------------------------------------------

columnas_numericas = [
    "poblacion_14_mas",
    "pea",
    "ocupados",
    "desocupados",
    "poblacion_no_economicamente_activa"
]


for columna in columnas_numericas:

    eco_01[columna] = pd.to_numeric(
        eco_01[columna],
        errors="coerce"
    )


# ------------------------------------------------------------
# 9. CONSTRUIR INDICADORES
# ------------------------------------------------------------

eco_01["tasa_actividad"] = (
    eco_01["pea"]
    / eco_01["poblacion_14_mas"]
    * 100
).round(2)


eco_01["tasa_empleo"] = (
    eco_01["ocupados"]
    / eco_01["poblacion_14_mas"]
    * 100
).round(2)


eco_01["tasa_desocupacion"] = (
    eco_01["desocupados"]
    / eco_01["pea"]
    * 100
).round(2)


# ------------------------------------------------------------
# 10. CONTROLES DE CONSISTENCIA
# ------------------------------------------------------------

# PEA = ocupados + desocupados

eco_01["suma_pea"] = (
    eco_01["ocupados"]
    + eco_01["desocupados"]
)


eco_01["diferencia_control_pea"] = (
    eco_01["pea"]
    - eco_01["suma_pea"]
)


# Población 14+ = PEA + población no económicamente activa

eco_01["suma_condicion_actividad"] = (
    eco_01["pea"]
    + eco_01["poblacion_no_economicamente_activa"]
)


eco_01["diferencia_control_poblacion"] = (
    eco_01["poblacion_14_mas"]
    - eco_01["suma_condicion_actividad"]
)


# ------------------------------------------------------------
# 11. VALIDACIÓN PRELIMINAR
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN PRELIMINAR ECO_01")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    eco_01.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    eco_01["partido"].nunique()
)


print("\nPARTIDOS DUPLICADOS:")
print(
    eco_01["partido"].duplicated().sum()
)


print("\nVALORES NULOS:")
print(
    eco_01.isnull().sum()
)


print("\nTIPOS DE DATOS:")
print(
    eco_01.dtypes
)


# ------------------------------------------------------------
# CONTROL PEA
# ------------------------------------------------------------

print(
    "\nREGISTROS DONDE PEA NO COINCIDE "
    "CON OCUPADOS + DESOCUPADOS:"
)


inconsistencias_pea = eco_01[
    eco_01["diferencia_control_pea"] != 0
]


if inconsistencias_pea.empty:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        inconsistencias_pea.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# CONTROL POBLACIÓN 14+
# ------------------------------------------------------------

print(
    "\nREGISTROS DONDE POBLACIÓN 14+ NO COINCIDE "
    "CON PEA + POBLACIÓN NO ECONÓMICAMENTE ACTIVA:"
)


inconsistencias_poblacion = eco_01[
    eco_01["diferencia_control_poblacion"] != 0
]


if inconsistencias_poblacion.empty:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        inconsistencias_poblacion.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 12. RANGOS DE INDICADORES
# ------------------------------------------------------------

print("\nRANGO TASA DE ACTIVIDAD:")

print(
    "Mínimo:",
    eco_01["tasa_actividad"].min()
)

print(
    "Máximo:",
    eco_01["tasa_actividad"].max()
)


print("\nRANGO TASA DE EMPLEO:")

print(
    "Mínimo:",
    eco_01["tasa_empleo"].min()
)

print(
    "Máximo:",
    eco_01["tasa_empleo"].max()
)


print("\nRANGO TASA DE DESOCUPACIÓN:")

print(
    "Mínimo:",
    eco_01["tasa_desocupacion"].min()
)

print(
    "Máximo:",
    eco_01["tasa_desocupacion"].max()
)


# ------------------------------------------------------------
# 13. CONTROL GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\nGENERAL PUEYRREDÓN:")

print(
    eco_01[
        eco_01["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 14. PRIMERAS FILAS
# ------------------------------------------------------------

print("\nPRIMERAS 15 FILAS ECO_01:")

print(
    eco_01.head(15).to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("LIMPIEZA PRELIMINAR ECO_01 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# 15. CONSTRUIR DATASET FINAL
# ============================================================

economia_final = eco_01[
    [
        "partido",
        "poblacion_14_mas",
        "pea",
        "ocupados",
        "desocupados",
        "poblacion_no_economicamente_activa",
        "tasa_actividad",
        "tasa_empleo",
        "tasa_desocupacion"
    ]
].copy()


# Agregar año del Censo
economia_final.insert(
    1,
    "anio",
    2022
)


# ============================================================
# 16. VALIDACIÓN FINAL
# ============================================================

print("\n" + "=" * 70)
print("VALIDACIÓN DEL DATASET FINAL DE ECONOMÍA")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    economia_final.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    economia_final["partido"].nunique()
)


print("\nAÑOS:")
print(
    economia_final["anio"].unique()
)


print("\nVALORES NULOS:")
print(
    economia_final.isnull().sum()
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    economia_final.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


print("\nGENERAL PUEYRREDÓN:")

print(
    economia_final[
        economia_final["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


print("\nPRIMERAS 15 FILAS:")

print(
    economia_final.head(15).to_string(
        index=False
    )
)


# ============================================================
# 17. GUARDAR DATASET FINAL
# ============================================================

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)


os.makedirs(
    carpeta_salida,
    exist_ok=True
)


ruta_salida = os.path.join(
    carpeta_salida,
    "economia_limpio.csv"
)


economia_final.to_csv(
    ruta_salida,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 18. CONTROL DEL ARCHIVO GUARDADO
# ============================================================

print("\n" + "=" * 70)
print("GUARDADO DEL DATASET FINAL DE ECONOMÍA")
print("=" * 70)


print("\nRUTA:")
print(
    ruta_salida
)


print("\nDIMENSIONES:")
print(
    economia_final.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    economia_final["partido"].nunique()
)


print("\nVALORES NULOS TOTALES:")
print(
    economia_final.isnull().sum().sum()
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    economia_final.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


print("\n" + "=" * 70)
print("ARCHIVO DE ECONOMÍA GUARDADO CORRECTAMENTE")
print("=" * 70)