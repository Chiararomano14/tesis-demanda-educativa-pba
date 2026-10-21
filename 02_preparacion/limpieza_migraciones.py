import os
import re
import unicodedata
import pandas as pd


# ============================================================
# LIMPIEZA DE MIGRACIONES
# MIG_01 - LUGAR DE RESIDENCIA HABITUAL EN 2017
# ============================================================

print("-" * 70)
print("LIMPIEZA DE MIGRACIONES")
print("MIG_01 - LUGAR DE RESIDENCIA HABITUAL EN 2017")
print("-" * 70)


# ------------------------------------------------------------
# 1. RUTA DE LA CARPETA
# ------------------------------------------------------------

carpeta_migraciones = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /migraciones"
)


# ------------------------------------------------------------
# 2. BUSCAR ARCHIVO MIG_01
# ------------------------------------------------------------

archivo_mig_01 = None

for archivo in os.listdir(carpeta_migraciones):

    if (
        archivo.startswith("4.2")
        and archivo.lower().endswith(".xlsx")
    ):
        archivo_mig_01 = os.path.join(
            carpeta_migraciones,
            archivo
        )
        break


if archivo_mig_01 is None:
    raise FileNotFoundError(
        "No se encontró el archivo MIG_01"
    )


print("\nARCHIVO MIG_01:")
print(archivo_mig_01)


# ------------------------------------------------------------
# 3. LEER HOJAS
# ------------------------------------------------------------

excel_mig_01 = pd.ExcelFile(
    archivo_mig_01
)


# Solo hojas correspondientes a partidos.
# Se excluye "Cuadro 4.2", que corresponde al total provincial.

hojas_partidos = []

for hoja in excel_mig_01.sheet_names:

    nombre_normalizado = (
        hoja
        .replace("\xa0", " ")
        .strip()
    )

    if re.fullmatch(
        r"Cuadro 4\.2\.\d+",
        nombre_normalizado
    ):
        hojas_partidos.append(hoja)


print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
print(
    len(hojas_partidos)
)


# ------------------------------------------------------------
# 4. FUNCIÓN PARA NORMALIZAR NOMBRES DE PARTIDOS
# ------------------------------------------------------------

def normalizar_partido(nombre):

    nombre = str(nombre)

    # Reemplazar espacios especiales del Excel por espacios normales
    nombre = nombre.replace("\xa0", " ")

    # Mayúsculas y espacios iniciales/finales
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

    # Equivalencias para mantener los mismos nombres
    # utilizados en los demás datasets
    equivalencias = {
        "NUEVE DE JULIO": "9 DE JULIO"
    }

    nombre = equivalencias.get(
        nombre,
        nombre
    )

    return nombre

# ------------------------------------------------------------
# 5. EXTRAER INFORMACIÓN DE CADA PARTIDO
# ------------------------------------------------------------

registros = []


for hoja in hojas_partidos:

    df = pd.read_excel(
        archivo_mig_01,
        sheet_name=hoja,
        header=None
    )


    # --------------------------------------------------------
    # EXTRAER NOMBRE DEL PARTIDO DESDE EL TÍTULO
    # --------------------------------------------------------

    titulo = str(
        df.iloc[1, 0]
    )

    coincidencia = re.search(
        r"[Pp]artido\s+(.+?)\.\s*Población",
        titulo
    )


    if coincidencia is None:

        print(
            "\nNO SE PUDO EXTRAER EL PARTIDO DE:"
        )

        print(
            repr(hoja)
        )

        continue


    partido = normalizar_partido(
        coincidencia.group(1)
    )


    # --------------------------------------------------------
    # EXTRAER FILA TOTAL
    # --------------------------------------------------------

    poblacion_total = df.iloc[4, 2]
    misma_localidad = df.iloc[4, 3]
    otra_localidad_pba = df.iloc[4, 4]
    otra_provincia = df.iloc[4, 5]
    otro_pais = df.iloc[4, 6]


    # --------------------------------------------------------
    # CONVERTIR VALORES
    # --------------------------------------------------------

    valores = [
        poblacion_total,
        misma_localidad,
        otra_localidad_pba,
        otra_provincia,
        otro_pais
    ]


    valores_limpios = []

    for valor in valores:

        if valor == "-" or pd.isna(valor):
            valor = 0

        valor = int(valor)

        valores_limpios.append(
            valor
        )


    (
        poblacion_total,
        misma_localidad,
        otra_localidad_pba,
        otra_provincia,
        otro_pais
    ) = valores_limpios


    # --------------------------------------------------------
    # AGREGAR REGISTRO
    # --------------------------------------------------------

    registros.append(
        {
            "partido": partido,
            "poblacion_5_mas": poblacion_total,
            "residencia_2017_misma_localidad": misma_localidad,
            "residencia_2017_otra_localidad_pba": otra_localidad_pba,
            "residencia_2017_otra_provincia": otra_provincia,
            "residencia_2017_otro_pais": otro_pais
        }
    )


# ------------------------------------------------------------
# 6. CREAR DATAFRAME
# ------------------------------------------------------------

mig_01 = pd.DataFrame(
    registros
)


# ------------------------------------------------------------
# 7. INDICADORES PRELIMINARES
# ------------------------------------------------------------

mig_01["poblacion_residia_fuera_localidad_2017"] = (
    mig_01["residencia_2017_otra_localidad_pba"]
    + mig_01["residencia_2017_otra_provincia"]
    + mig_01["residencia_2017_otro_pais"]
)


mig_01["porcentaje_residia_fuera_localidad_2017"] = (
    mig_01["poblacion_residia_fuera_localidad_2017"]
    / mig_01["poblacion_5_mas"]
    * 100
).round(2)


# ------------------------------------------------------------
# 8. CONTROL DE CONSISTENCIA
# ------------------------------------------------------------

mig_01["suma_residencia_2017"] = (
    mig_01["residencia_2017_misma_localidad"]
    + mig_01["residencia_2017_otra_localidad_pba"]
    + mig_01["residencia_2017_otra_provincia"]
    + mig_01["residencia_2017_otro_pais"]
)


mig_01["diferencia_control_residencia"] = (
    mig_01["poblacion_5_mas"]
    - mig_01["suma_residencia_2017"]
)


# ------------------------------------------------------------
# 9. VALIDACIÓN PRELIMINAR
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN PRELIMINAR MIG_01")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    mig_01.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    mig_01["partido"].nunique()
)


print("\nPARTIDOS DUPLICADOS:")
print(
    mig_01["partido"].duplicated().sum()
)


print("\nVALORES NULOS:")
print(
    mig_01.isnull().sum()
)


print("\nTIPOS DE DATOS:")
print(
    mig_01.dtypes
)


print(
    "\nREGISTROS DONDE LA SUMA DE LAS CATEGORÍAS "
    "DE RESIDENCIA NO COINCIDE CON EL TOTAL:"
)

inconsistencias = mig_01[
    mig_01["diferencia_control_residencia"] != 0
]


if inconsistencias.empty:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        inconsistencias.to_string(
            index=False
        )
    )


print(
    "\nRANGO % DE POBLACIÓN QUE RESIDÍA "
    "FUERA DE LA LOCALIDAD EN 2017:"
)

print(
    "Mínimo:",
    mig_01[
        "porcentaje_residia_fuera_localidad_2017"
    ].min()
)

print(
    "Máximo:",
    mig_01[
        "porcentaje_residia_fuera_localidad_2017"
    ].max()
)


# ------------------------------------------------------------
# 10. CONTROL GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\nGENERAL PUEYRREDÓN:")

print(
    mig_01[
        mig_01["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 11. MOSTRAR PRIMERAS FILAS
# ------------------------------------------------------------

print("\nPRIMERAS 15 FILAS MIG_01:")

print(
    mig_01.head(15).to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("LIMPIEZA PRELIMINAR MIG_01 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# PREPARAR DATASET FINAL DE MIGRACIONES
# ============================================================

migraciones_final = mig_01[
    [
        "partido",
        "poblacion_5_mas",
        "residencia_2017_misma_localidad",
        "residencia_2017_otra_localidad_pba",
        "residencia_2017_otra_provincia",
        "residencia_2017_otro_pais",
        "poblacion_residia_fuera_localidad_2017",
        "porcentaje_residia_fuera_localidad_2017"
    ]
].copy()


# El relevamiento corresponde al Censo 2022.
# Las variables de residencia indican dónde vivía
# la población cinco años antes, es decir, en 2017.

migraciones_final.insert(
    1,
    "anio",
    2022
)


# ============================================================
# VALIDACIÓN FINAL
# ============================================================

print("\n" + "=" * 70)
print("VALIDACIÓN DEL DATASET FINAL DE MIGRACIONES")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    migraciones_final.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    migraciones_final["partido"].nunique()
)


print("\nAÑOS:")
print(
    sorted(
        migraciones_final["anio"].unique()
    )
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    migraciones_final.duplicated(
        subset=[
            "partido",
            "anio"
        ]
    ).sum()
)


print("\nVALORES NULOS:")
print(
    migraciones_final.isnull().sum()
)


print("\nTIPOS DE DATOS:")
print(
    migraciones_final.dtypes
)


# ============================================================
# CONTROL DEL INDICADOR DE MOVILIDAD
# ============================================================

print(
    "\nRANGO DEL PORCENTAJE DE POBLACIÓN "
    "QUE RESIDÍA FUERA DE LA LOCALIDAD EN 2017:"
)

print(
    "Mínimo:",
    migraciones_final[
        "porcentaje_residia_fuera_localidad_2017"
    ].min()
)

print(
    "Máximo:",
    migraciones_final[
        "porcentaje_residia_fuera_localidad_2017"
    ].max()
)


porcentajes_invalidos = migraciones_final[
    ~migraciones_final[
        "porcentaje_residia_fuera_localidad_2017"
    ].between(
        0,
        100
    )
]


print("\nPORCENTAJES FUERA DEL RANGO 0-100:")


if porcentajes_invalidos.empty:

    print(
        "Todos los porcentajes son válidos."
    )

else:

    print(
        porcentajes_invalidos.to_string(
            index=False
        )
    )


# ============================================================
# CONTROL GENERAL PUEYRREDÓN
# ============================================================

print("\nGENERAL PUEYRREDÓN:")

print(
    migraciones_final[
        migraciones_final["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


# ============================================================
# GUARDAR DATASET FINAL
# ============================================================

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)


os.makedirs(
    carpeta_salida,
    exist_ok=True
)


ruta_salida_migraciones = os.path.join(
    carpeta_salida,
    "migraciones_limpio.csv"
)


migraciones_final.to_csv(
    ruta_salida_migraciones,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# CONTROL DEL ARCHIVO GUARDADO
# ============================================================

print("\n" + "=" * 70)
print("GUARDADO DEL DATASET FINAL DE MIGRACIONES")
print("=" * 70)


print("\nRUTA:")
print(
    ruta_salida_migraciones
)


print("\nDIMENSIONES:")
print(
    migraciones_final.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    migraciones_final["partido"].nunique()
)


print("\nVALORES NULOS TOTALES:")
print(
    migraciones_final
    .isnull()
    .sum()
    .sum()
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    migraciones_final.duplicated(
        subset=[
            "partido",
            "anio"
        ]
    ).sum()
)


print("\n" + "=" * 70)
print("ARCHIVO DE MIGRACIONES GUARDADO CORRECTAMENTE")
print("=" * 70)