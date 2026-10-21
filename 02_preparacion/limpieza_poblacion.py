import os
import re
import unicodedata
import pandas as pd

# ETAPA 4 - CONSTRUCCIÓN DEL DATASET
# LIMPIEZA DE POBLACIÓN

carpeta_poblacion = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /poblacion"
)


# NORMALIZAR NOMBRES DE PARTIDOS

def normalizar_partido(nombre):

    if pd.isna(nombre):
        return nombre

    nombre = str(nombre)

    nombre = (
        nombre
        .replace("\xa0", " ")
        .replace("\n", " ")
    )

    nombre = " ".join(
        nombre.split()
    )

    nombre = (
        unicodedata
        .normalize(
            "NFD",
            nombre
        )
        .encode(
            "ascii",
            "ignore"
        )
        .decode(
            "utf-8"
        )
    )

    return (
        nombre
        .strip()
        .upper()
    )


# ============================================================
# BLOQUE 1 - POB_01 Y POB_02
# ============================================================

archivo_pob_01 = os.path.join(
    carpeta_poblacion,
    "1.2 – Total población, variación absoluta y relativa por partido, 2010-2022.xlsx"
)

archivo_pob_02 = os.path.join(
    carpeta_poblacion,
    "2.2 – Población y densidad por partido.xlsx"
)


# 1. LEER POB_01

df_pob_01 = pd.read_excel(
    archivo_pob_01,
    sheet_name="Cuadro1.2",
    header=None
)

pob_01 = df_pob_01.iloc[
    5:,
    [1, 2, 3, 4, 5]
].copy()

pob_01.columns = [
    "partido",
    "poblacion_2010",
    "poblacion_2022",
    "variacion_absoluta",
    "variacion_relativa"
]


# 2. NORMALIZAR PARTIDOS POB_01

pob_01 = pob_01[
    pob_01["partido"].notna()
].copy()

pob_01["partido"] = (
    pob_01["partido"]
    .apply(normalizar_partido)
)

pob_01 = pob_01[
    ~pob_01["partido"].str.contains(
        "TOTAL|PARTIDOS DEL GRAN BUENOS AIRES|RESTO DE PARTIDOS",
        case=False,
        na=False
    )
].copy()


# 3. CONVERTIR VARIABLES NUMÉRICAS POB_01

columnas_numericas_pob_01 = [
    "poblacion_2010",
    "poblacion_2022",
    "variacion_absoluta",
    "variacion_relativa"
]

for columna in columnas_numericas_pob_01:

    pob_01[columna] = pd.to_numeric(
        pob_01[columna],
        errors="coerce"
    )


# 4. LEER POB_02

df_pob_02 = pd.read_excel(
    archivo_pob_02,
    sheet_name="Cuadro2.2",
    header=None
)

pob_02 = df_pob_02.iloc[
    6:,
    [1, 2, 3, 4]
].copy()

pob_02.columns = [
    "partido",
    "superficie_km2",
    "poblacion_2022_pob02",
    "densidad_2022"
]


# 5. NORMALIZAR PARTIDOS POB_02

pob_02 = pob_02[
    pob_02["partido"].notna()
].copy()

pob_02["partido"] = (
    pob_02["partido"]
    .apply(normalizar_partido)
)

pob_02 = pob_02[
    ~pob_02["partido"].str.contains(
        "TOTAL|PARTIDOS DEL GRAN BUENOS AIRES|RESTO DE PARTIDOS",
        case=False,
        na=False
    )
].copy()


# 6. CONVERTIR VARIABLES NUMÉRICAS POB_02

columnas_numericas_pob_02 = [
    "superficie_km2",
    "poblacion_2022_pob02",
    "densidad_2022"
]

for columna in columnas_numericas_pob_02:

    pob_02[columna] = pd.to_numeric(
        pob_02[columna],
        errors="coerce"
    )


# 7. UNIR POB_01 Y POB_02

poblacion_base = pob_01.merge(
    pob_02,
    on="partido",
    how="outer"
)


# 8. VALIDAR POBLACIÓN 2022 ENTRE AMBAS FUENTES

poblacion_base["diferencia_poblacion_2022"] = (
    poblacion_base["poblacion_2022"]
    - poblacion_base["poblacion_2022_pob02"]
)

diferencias = poblacion_base[
    poblacion_base[
        "diferencia_poblacion_2022"
    ].fillna(0) != 0
]

print("\nPOB_01 + POB_02")

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_base["partido"].nunique()
)

print("\nFILAS DUPLICADAS:")
print(
    poblacion_base["partido"]
    .duplicated()
    .sum()
)

print("\nDIFERENCIAS DE POBLACIÓN 2022 ENTRE POB_01 Y POB_02:")

if len(diferencias) == 0:

    print(
        "No se encontraron diferencias. "
        "La población 2022 coincide en ambas fuentes."
    )

else:

    print(
        diferencias[
            [
                "partido",
                "poblacion_2022",
                "poblacion_2022_pob02",
                "diferencia_poblacion_2022"
            ]
        ].to_string(index=False)
    )


# 9. REVISAR FALTANTES DE POB_01

faltantes_pob_01 = poblacion_base[
    poblacion_base[
        [
            "poblacion_2010",
            "variacion_absoluta",
            "variacion_relativa"
        ]
    ]
    .isna()
    .any(axis=1)
]

print("\nREGISTROS CON INFORMACIÓN FALTANTE DE POB_01:")

print(
    faltantes_pob_01[
        [
            "partido",
            "poblacion_2010",
            "poblacion_2022",
            "variacion_absoluta",
            "variacion_relativa"
        ]
    ]
    .to_string(index=False)
)


# ============================================================
# BLOQUE 2 - POB_03
# POBLACIÓN POR EDAD
# ============================================================


# 10. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO POB_03

archivo_pob_03 = None

for archivo in os.listdir(carpeta_poblacion):

    if (
        archivo.startswith("4.2")
        and archivo.lower().endswith(".xlsx")
    ):

        archivo_pob_03 = os.path.join(
            carpeta_poblacion,
            archivo
        )

        break

if archivo_pob_03 is None:

    raise FileNotFoundError(
        "No se encontró el archivo POB_03"
    )

print("\nARCHIVO POB_03 ENCONTRADO:")
print(
    archivo_pob_03
)


# 11. IDENTIFICAR LAS 135 HOJAS DE PARTIDOS

excel_pob_03 = pd.ExcelFile(
    archivo_pob_03
)

hojas_partidos = [
    hoja
    for hoja in excel_pob_03.sheet_names
    if re.fullmatch(
        r"Cuadro4\.2\.\d+",
        hoja
    )
    and hoja != "Cuadro4.2.0"
]

print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
print(
    len(hojas_partidos)
)


# 12. RECUPERAR EDADES SIMPLES POR PARTIDO

datos_edades = []

for hoja in hojas_partidos:

    df = pd.read_excel(
        archivo_pob_03,
        sheet_name=hoja,
        header=None
    )

    titulo = str(
        df.iloc[1, 0]
    )

    coincidencia = re.search(
        r"partido\s+(.+?)\.\s*Total",
        titulo,
        flags=re.IGNORECASE
    )

    if coincidencia is None:

        print(
            "No se pudo identificar el partido:",
            hoja
        )

        continue

    partido = normalizar_partido(
        coincidencia.group(1)
    )

    datos = df.iloc[
        4:,
        [0, 1]
    ].copy()

    datos.columns = [
        "edad",
        "poblacion"
    ]

    datos["edad"] = (
        datos["edad"]
        .astype(str)
        .str.strip()
    )

    # Solo se conservan edades simples:
    # 0, 1, 2, 3...
    # Se excluyen intervalos como 0-4, 5-9, etc.

    datos = datos[
        datos["edad"]
        .str.fullmatch(r"\d+")
    ].copy()

    datos["edad"] = pd.to_numeric(
        datos["edad"],
        errors="coerce"
    )

    datos["poblacion"] = pd.to_numeric(
        datos["poblacion"],
        errors="coerce"
    )

    datos["partido"] = partido

    datos_edades.append(
        datos[
            [
                "partido",
                "edad",
                "poblacion"
            ]
        ]
    )


# 13. UNIR LOS 135 PARTIDOS

poblacion_edades = pd.concat(
    datos_edades,
    ignore_index=True
)


# 14. REVISAR FALTANTES DE POBLACIÓN POR EDAD

faltantes_edades = poblacion_edades[
    poblacion_edades["poblacion"].isna()
].copy()

faltantes_edad_escolar = faltantes_edades[
    faltantes_edades["edad"].between(
        0,
        17
    )
]

print("\nPOB_03")

print("\nCANTIDAD DE PARTIDOS RECUPERADOS:")
print(
    poblacion_edades[
        "partido"
    ].nunique()
)

print("\nEDAD MÍNIMA:")
print(
    poblacion_edades[
        "edad"
    ].min()
)

print("\nEDAD MÁXIMA:")
print(
    poblacion_edades[
        "edad"
    ].max()
)

print("\nVALORES FALTANTES DE POBLACIÓN:")
print(
    len(
        faltantes_edades
    )
)

print("\nFALTANTES ENTRE 0 Y 17 AÑOS:")
print(
    len(
        faltantes_edad_escolar
    )
)

print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    poblacion_edades
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)


# 15. CONSTRUIR GRUPOS DE EDAD EDUCATIVA

poblacion_edad_educativa = (
    poblacion_edades[
        poblacion_edades[
            "edad"
        ].between(
            0,
            17
        )
    ]
    .copy()
)


def clasificar_grupo_edad(edad):

    if 0 <= edad <= 5:

        return "poblacion_0_5"

    elif 6 <= edad <= 11:

        return "poblacion_6_11"

    elif 12 <= edad <= 17:

        return "poblacion_12_17"

    return None


poblacion_edad_educativa[
    "grupo_edad"
] = (
    poblacion_edad_educativa[
        "edad"
    ]
    .apply(
        clasificar_grupo_edad
    )
)


# 16. SUMAR POR PARTIDO Y GRUPO DE EDAD

poblacion_grupos = (
    poblacion_edad_educativa
    .groupby(
        [
            "partido",
            "grupo_edad"
        ],
        as_index=False
    )[
        "poblacion"
    ]
    .sum()
)


# 17. PASAR A FORMATO ANCHO

poblacion_grupos = (
    poblacion_grupos
    .pivot(
        index="partido",
        columns="grupo_edad",
        values="poblacion"
    )
    .reset_index()
)

poblacion_grupos.columns.name = None


# 18. ORDENAR COLUMNAS

poblacion_grupos = poblacion_grupos[
    [
        "partido",
        "poblacion_0_5",
        "poblacion_6_11",
        "poblacion_12_17"
    ]
]

print("\nGRUPOS DE EDAD")

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_grupos[
        "partido"
    ].nunique()
)

print("\nVALORES NULOS:")
print(
    poblacion_grupos
    .isna()
    .sum()
)


# 19. INTEGRAR POB_03 CON POB_01 Y POB_02

poblacion_base = poblacion_base.merge(
    poblacion_grupos,
    on="partido",
    how="left"
)


# 20. VALIDACIÓN FINAL DE POB_01 + POB_02 + POB_03

print("\nPOB_01 + POB_02 + POB_03")

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_base[
        "partido"
    ].nunique()
)

print("\nDIMENSIONES:")
print(
    poblacion_base.shape
)

print("\nVALORES NULOS:")
print(
    poblacion_base
    .isna()
    .sum()
)

print("\nCOLUMNAS ACTUALES:")
print(
    poblacion_base.columns.tolist()
)

print("\nPRIMERAS 15 FILAS:")
print(
    poblacion_base
    .head(15)
    .to_string(index=False)
)


# 21. COMPROBAR QUE TODOS LOS PARTIDOS RECIBIERON
# LOS GRUPOS DE EDAD

partidos_sin_edades = poblacion_base[
    poblacion_base[
        [
            "poblacion_0_5",
            "poblacion_6_11",
            "poblacion_12_17"
        ]
    ]
    .isna()
    .any(axis=1)
]

print("\nPARTIDOS SIN INFORMACIÓN DE GRUPOS DE EDAD:")

if len(partidos_sin_edades) == 0:

    print(
        "Todos los partidos tienen información "
        "para los tres grupos de edad."
    )

else:

    print(
        partidos_sin_edades[
            [
                "partido",
                "poblacion_0_5",
                "poblacion_6_11",
                "poblacion_12_17"
            ]
        ]
        .to_string(index=False)
    )
# ============================================================
# BLOQUE 3 - POB_05
# ESTIMACIONES DE POBLACIÓN 2022-2035
# ============================================================

import pdfplumber


# 22. BUSCAR PDF POB_05

archivo_pob_05 = None

for archivo in os.listdir(carpeta_poblacion):

    if (
        archivo.lower().endswith(".pdf")
        and "estimaciones_departamentos" in archivo.lower()
    ):

        archivo_pob_05 = os.path.join(
            carpeta_poblacion,
            archivo
        )

        break


if archivo_pob_05 is None:

    raise FileNotFoundError(
        "No se encontró el archivo POB_05"
    )


print("\nARCHIVO POB_05 ENCONTRADO:")
print(
    archivo_pob_05
)


# 23. DEFINIR AÑOS DE LAS ESTIMACIONES

anios_estimaciones = list(
    range(
        2022,
        2036
    )
)


# 24. EXTRAER FILAS DE BUENOS AIRES - AMBOS SEXOS

datos_estimaciones = []

patron_numeros = (
    r"(\d{1,3}(?:\.\d{3})*"
    r"(?:\s+\d{1,3}(?:\.\d{3})*){13})$"
)


with pdfplumber.open(
    archivo_pob_05
) as pdf:

    for numero_pagina, pagina in enumerate(
        pdf.pages,
        start=1
    ):

        texto = pagina.extract_text()

        if not texto:
            continue

        # Solo nos interesan páginas correspondientes
        # a "Ambos sexos"

        if "Ambos sexos" not in texto:
            continue

        lineas = texto.splitlines()

        for linea in lineas:

            linea = " ".join(
                linea.split()
            )

            # Los códigos de los partidos bonaerenses
            # comienzan con 06

            if not re.match(
                r"^06\d{3}\s+",
                linea
            ):
                continue

            codigo = linea.split()[0]

            resto = linea[
                len(codigo):
            ].strip()

            coincidencia_numeros = re.search(
                patron_numeros,
                resto
            )

            if coincidencia_numeros is None:
                continue

            numeros_texto = (
                coincidencia_numeros
                .group(1)
            )

            valores = (
                numeros_texto
                .split()
            )

            if len(valores) != 14:
                continue

            nombre_partido = resto[
                :coincidencia_numeros.start()
            ].strip()

            # En el PDF este partido aparece
            # dividido en varias líneas

            if codigo == "06182":

                nombre_partido = (
                    "CORONEL DE MARINA "
                    "LEONARDO ROSALES"
                )

            if nombre_partido == "":
                continue

            partido = normalizar_partido(
                nombre_partido
            )

            valores = [
                int(
                    valor.replace(
                        ".",
                        ""
                    )
                )
                for valor in valores
            ]

            for anio, poblacion in zip(
                anios_estimaciones,
                valores
            ):

                datos_estimaciones.append(
                    {
                        "codigo": codigo,
                        "partido": partido,
                        "anio": anio,
                        "poblacion_estimada": poblacion
                    }
                )


# 25. CREAR DATAFRAME POB_05

pob_05 = pd.DataFrame(
    datos_estimaciones
)


# 26. ELIMINAR POSIBLES DUPLICADOS DE EXTRACCIÓN

pob_05 = (
    pob_05
    .drop_duplicates(
        subset=[
            "partido",
            "anio"
        ]
    )
    .sort_values(
        [
            "partido",
            "anio"
        ]
    )
    .reset_index(
        drop=True
    )
)


# 27. VALIDAR COBERTURA DE POB_05

print("\nPOB_05 - ESTIMACIONES 2022-2035")

print("\nCANTIDAD DE PARTIDOS:")
print(
    pob_05[
        "partido"
    ].nunique()
)

print("\nPERÍODO:")
print(
    pob_05["anio"].min(),
    "-",
    pob_05["anio"].max()
)

print("\nCANTIDAD DE AÑOS:")
print(
    pob_05[
        "anio"
    ].nunique()
)

print("\nDIMENSIONES:")
print(
    pob_05.shape
)

print("\nVALORES NULOS:")
print(
    pob_05
    .isna()
    .sum()
)

print("\nFILAS DUPLICADAS PARTIDO-AÑO:")
print(
    pob_05
    .duplicated(
        subset=[
            "partido",
            "anio"
        ]
    )
    .sum()
)


# 28. COMPROBAR COBERTURA TERRITORIAL
# CONTRA POB_01 + POB_02 + POB_03

partidos_base = set(
    poblacion_base[
        "partido"
    ]
)

partidos_estimaciones = set(
    pob_05[
        "partido"
    ]
)


print("\nPARTIDOS DE LA BASE QUE NO APARECEN EN POB_05:")
print(
    partidos_base
    - partidos_estimaciones
)

print("\nPARTIDOS DE POB_05 QUE NO APARECEN EN LA BASE:")
print(
    partidos_estimaciones
    - partidos_base
)


# 29. CANTIDAD DE PARTIDOS POR AÑO

print("\nPARTIDOS POR AÑO:")

print(
    pob_05
    .groupby(
        "anio"
    )[
        "partido"
    ]
    .nunique()
)


# 30. MOSTRAR EJEMPLO

print("\nPRIMERAS 20 FILAS:")

print(
    pob_05
    .head(20)
    .to_string(
        index=False
    )
)


print("\nLA PLATA - ESTIMACIONES:")

print(
    pob_05[
        pob_05[
            "partido"
        ] == "LA PLATA"
    ]
    .to_string(
        index=False
    )
)

# ============================================================
# BLOQUE 4 - GUARDAR DATASETS LIMPIOS DE POBLACIÓN
# ============================================================

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)

os.makedirs(
    carpeta_salida,
    exist_ok=True
)

# 31. PREPARAR BASE CENSAL FINAL

poblacion_base_final = poblacion_base[
    [
        "partido",
        "poblacion_2010",
        "poblacion_2022",
        "variacion_absoluta",
        "variacion_relativa",
        "superficie_km2",
        "densidad_2022",
        "poblacion_0_5",
        "poblacion_6_11",
        "poblacion_12_17"
    ]
].copy()

# Ajustar tipos de datos

columnas_enteras = [
    "poblacion_2010",
    "poblacion_2022",
    "variacion_absoluta",
    "poblacion_0_5",
    "poblacion_6_11",
    "poblacion_12_17"
]

for columna in columnas_enteras:

    poblacion_base_final[columna] = (
        poblacion_base_final[columna]
        .round()
        .astype("Int64")
    )

# 32. PREPARAR ESTIMACIONES FINALES

poblacion_estimaciones_final = pob_05[
    [
        "partido",
        "anio",
        "poblacion_estimada"
    ]
].copy()

poblacion_estimaciones_final["anio"] = (
    poblacion_estimaciones_final["anio"]
    .astype(int)
)

poblacion_estimaciones_final[
    "poblacion_estimada"
] = (
    poblacion_estimaciones_final[
        "poblacion_estimada"
    ]
    .astype("Int64")
)

# 33. VALIDACIÓN FINAL

print("\nBASE CENSAL FINAL")

print("\nDIMENSIONES:")
print(
    poblacion_base_final.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_base_final[
        "partido"
    ].nunique()
)

print("\nVALORES NULOS:")
print(
    poblacion_base_final
    .isna()
    .sum()
)

print("\nESTIMACIONES FINALES")

print("\nDIMENSIONES:")
print(
    poblacion_estimaciones_final.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_estimaciones_final[
        "partido"
    ].nunique()
)

print("\nPERÍODO:")
print(
    poblacion_estimaciones_final[
        "anio"
    ].min(),
    "-",
    poblacion_estimaciones_final[
        "anio"
    ].max()
)

print("\nVALORES NULOS:")
print(
    poblacion_estimaciones_final
    .isna()
    .sum()
)

# 34. GUARDAR ARCHIVOS

archivo_base = os.path.join(
    carpeta_salida,
    "poblacion_base_limpia.csv"
)

archivo_estimaciones = os.path.join(
    carpeta_salida,
    "poblacion_estimaciones_limpia.csv"
)

poblacion_base_final.to_csv(
    archivo_base,
    index=False,
    encoding="utf-8-sig"
)

poblacion_estimaciones_final.to_csv(
    archivo_estimaciones,
    index=False,
    encoding="utf-8-sig"
)

print("\nDATASET BASE GUARDADO EN:")
print(
    archivo_base
)

print("\nDATASET DE ESTIMACIONES GUARDADO EN:")
print(
    archivo_estimaciones
)
