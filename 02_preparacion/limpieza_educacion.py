import os
import re
import unicodedata
import pandas as pd


# ETAPA 4 - CONSTRUCCIÓN DEL DATASET
# LIMPIEZA DE EDUCACIÓN

carpeta_educacion = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /educacion"
)



# FUNCIÓN PARA NORMALIZAR NOMBRES DE PARTIDOS


def normalizar_partido(texto):

    texto = str(texto)

    texto = texto.replace("\xa0", " ")
    texto = texto.replace("\n", " ")

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    texto = texto.strip().upper()

    # Quitar tildes para evitar problemas en futuros merges
    texto = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )

    return texto



# BLOQUE 1 - EDU_01
# CONDICIÓN DE ASISTENCIA ESCOLAR POR EDAD



# 1. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO EDU_01

archivo_edu_01 = None

for archivo in os.listdir(carpeta_educacion):

    if (
        archivo.startswith("1.2")
        and archivo.lower().endswith(".xlsx")
    ):

        archivo_edu_01 = os.path.join(
            carpeta_educacion,
            archivo
        )

        break


if archivo_edu_01 is None:

    raise FileNotFoundError(
        "No se encontró el archivo EDU_01"
    )


print("\nARCHIVO EDU_01 ENCONTRADO:")
print(archivo_edu_01)


# 2. IDENTIFICAR HOJAS DE LOS PARTIDOS

excel_edu_01 = pd.ExcelFile(
    archivo_edu_01
)

hojas_partidos = [
    hoja
    for hoja in excel_edu_01.sheet_names
    if re.fullmatch(
        r"Cuadro\s*1\.2\.\d+",
        hoja
    )
    and hoja != "Cuadro 1.2.0"
]


print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
print(
    len(hojas_partidos)
)


# 3. RECORRER LAS HOJAS

datos_asistencia = []

for hoja in hojas_partidos:

    df = pd.read_excel(
        archivo_edu_01,
        sheet_name=hoja,
        header=None
    )

    
    # IDENTIFICAR PARTIDO DESDE EL TÍTULO
    

    titulo = str(
        df.iloc[1, 0]
    )

    coincidencia = re.search(
        r"partido\s+(.+?)\s*\.\s*Poblaci[oó]n",
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


    
    # UTILIZAR ÚNICAMENTE EL BLOQUE TOTAL
    

    filas_total = df.index[
        df.iloc[:, 0]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("total")
    ].tolist()

    filas_mujer = df.index[
        df.iloc[:, 0]
        .astype(str)
        .str.contains(
            "Mujer/Femenino",
            case=False,
            na=False
        )
    ].tolist()


    if len(filas_total) == 0 or len(filas_mujer) == 0:

        print(
            "No se pudo identificar el bloque Total:",
            partido
        )

        continue


    inicio = filas_total[0] + 1
    fin = filas_mujer[0]


    
    # EXTRAER EDAD Y CONDICIÓN DE ASISTENCIA
    

    datos = df.iloc[
        inicio:fin,
        [1, 2, 3, 4, 5]
    ].copy()

    datos.columns = [
        "edad",
        "poblacion",
        "asiste",
        "no_asiste_pero_asistio",
        "nunca_asistio"
    ]


    
    # CONSERVAR SOLO EDADES SIMPLES
    

    datos["edad"] = (
        datos["edad"]
        .astype(str)
        .str.strip()
    )

    datos = datos[
        datos["edad"]
        .str.fullmatch(r"\d+")
    ].copy()


    
    # CONVERTIR VARIABLES NUMÉRICAS
    

    datos["edad"] = pd.to_numeric(
        datos["edad"],
        errors="coerce"
    )

    columnas_numericas = [
        "poblacion",
        "asiste",
        "no_asiste_pero_asistio",
        "nunca_asistio"
    ]

    for columna in columnas_numericas:

        datos[columna] = pd.to_numeric(
            datos[columna],
            errors="coerce"
        )


    datos["partido"] = partido


    
    # ORDENAR COLUMNAS
    

    datos = datos[
        [
            "partido",
            "edad",
            "poblacion",
            "asiste",
            "no_asiste_pero_asistio",
            "nunca_asistio"
        ]
    ]


    datos_asistencia.append(
        datos
    )


# 4. UNIR LOS 135 PARTIDOS

edu_01 = pd.concat(
    datos_asistencia,
    ignore_index=True
)



# 5. VALIDACIONES


print("\nEDU_01 - CONDICIÓN DE ASISTENCIA ESCOLAR")


print("\nCANTIDAD DE PARTIDOS:")
print(
    edu_01["partido"].nunique()
)


print("\nDIMENSIONES:")
print(
    edu_01.shape
)


print("\nEDAD MÍNIMA:")
print(
    edu_01["edad"].min()
)


print("\nEDAD MÁXIMA:")
print(
    edu_01["edad"].max()
)


print("\nVALORES NULOS:")
print(
    edu_01
    .isna()
    .sum()
)


print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    edu_01
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)



# 6. VALIDAR QUE LAS CATEGORÍAS SUMEN LA POBLACIÓN
# TRATAMIENTO DE VALORES NULOS EN VARIABLES DE ASISTENCIA
columnas_asistencia = [
    "asiste",
    "no_asiste_pero_asistio",
    "nunca_asistio"
]

edu_01[columnas_asistencia] = edu_01[columnas_asistencia].fillna(0)

edu_01["suma_condiciones"] = (
    edu_01["asiste"]
    + edu_01["no_asiste_pero_asistio"]
    + edu_01["nunca_asistio"]
)

edu_01["diferencia_control"] = (
    edu_01["poblacion"]
    - edu_01["suma_condiciones"]
)


errores_suma = edu_01[
    edu_01["diferencia_control"] != 0
]


print("\nREGISTROS DONDE LAS CONDICIONES NO SUMAN LA POBLACIÓN:")

if len(errores_suma) == 0:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        errores_suma
        .to_string(index=False)
    )



# 7. CALCULAR TASA DE ASISTENCIA


edu_01["tasa_asistencia"] = (
    edu_01["asiste"]
    / edu_01["poblacion"]
    * 100
)



# 8. VALIDACIONES FINALES


print("\nRANGO DE TASA DE ASISTENCIA:")

print(
    edu_01["tasa_asistencia"]
    .describe()
)


print("\nPRIMERAS 20 FILAS:")

print(
    edu_01
    .head(20)
    .to_string(index=False)
)


print("\nEJEMPLO - GENERAL PUEYRREDON:")

print(
    edu_01[
        edu_01["partido"]
        == "GENERAL PUEYRREDON"
    ]
    .head(20)
    .to_string(index=False)
)
# BLOQUE 2 - EDU_02
# POBLACIÓN QUE ASISTE POR NIVEL EDUCATIVO, EDAD Y PARTIDO
print('BLOQUE 2 - EDU_02')
print('POBLACIÓN QUE ASISTE POR NIVEL EDUCATIVO, EDAD Y PARTIDO')
# 1. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO EDU_02

archivo_edu_02 = None

for archivo in os.listdir(carpeta_educacion):

    if (
        archivo.startswith("2.2")
        and archivo.lower().endswith(".xlsx")
    ):
        archivo_edu_02 = os.path.join(
            carpeta_educacion,
            archivo
        )
        break

if archivo_edu_02 is None:
    raise FileNotFoundError(
        "No se encontró el archivo EDU_02"
    )

print("\nARCHIVO EDU_02 ENCONTRADO:")
print(archivo_edu_02)


# 2. IDENTIFICAR LAS 135 HOJAS DE PARTIDOS

excel_edu_02 = pd.ExcelFile(
    archivo_edu_02
)

hojas_partidos_edu_02 = [
    hoja
    for hoja in excel_edu_02.sheet_names
    if re.fullmatch(
        r"Cuadro 2\.2\.\d+",
        hoja
    )
]

print("\nCANTIDAD DE HOJAS DE PARTIDOS EDU_02:")
print(
    len(hojas_partidos_edu_02)
)


# 3. RECUPERAR INFORMACIÓN DE CADA PARTIDO

datos_edu_02 = []

for hoja in hojas_partidos_edu_02:

    df = pd.read_excel(
        archivo_edu_02,
        sheet_name=hoja,
        header=None
    )

    # Recuperar nombre del partido desde el título

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

    
    # RECUPERAR SOLAMENTE EL BLOQUE TOTAL
    
    #
    # El bloque Total comienza en la fila 4.
    # Las edades simples 0-29 aparecen antes del bloque
    # Mujer/Femenino.
    #
    # Filtramos posteriormente las edades simples, por lo que
    # automáticamente se eliminan los grupos 0-4, 5-9, etc.

    # Identificar dónde comienza el bloque Mujer/Femenino

    columna_sexo = (
        df.iloc[:, 0]
        .astype(str)
        .str.strip()
    )

    filas_mujer = df.index[
        columna_sexo.str.contains(
            "Mujer/Femenino",
            case=False,
            na=False
        )
    ].tolist()

    if len(filas_mujer) == 0:
        raise ValueError(
            f"No se encontró el bloque Mujer/Femenino en {hoja}"
        )

    fila_inicio_mujer = filas_mujer[0]

    # Recuperar únicamente el bloque Total.
    # Comienza después de los encabezados y termina
    # antes del bloque Mujer/Femenino.

    datos = df.iloc[
            4:fila_inicio_mujer,
            1:11
            ].copy()

    datos.columns = [
        "edad",
        "poblacion",
        "asiste_edu02",
        "jardin_0_3",
        "sala_4_5",
        "primario",
        "secundario",
        "terciario",
        "universitario",
        "posgrado"
    ]

    # 4. CONSERVAR SOLAMENTE EDADES SIMPLES

    datos["edad"] = (
        datos["edad"]
        .astype(str)
        .str.strip()
    )

    datos = datos[
        datos["edad"]
        .str.fullmatch(r"\d+")
    ].copy()

    datos["edad"] = pd.to_numeric(
        datos["edad"],
        errors="coerce"
    )

    # Seguridad adicional:
    # EDU_02 contiene edades simples entre 0 y 29

    datos = datos[
        datos["edad"].between(
            0,
            29
        )
    ].copy()

    datos["partido"] = partido

    datos_edu_02.append(
        datos[
            [
                "partido",
                "edad",
                "poblacion",
                "asiste_edu02",
                "jardin_0_3",
                "sala_4_5",
                "primario",
                "secundario",
                "terciario",
                "universitario",
                "posgrado"
            ]
        ]
    )


# 5. UNIR LOS 135 PARTIDOS

educacion_nivel = pd.concat(
    datos_edu_02,
    ignore_index=True
)


# 6. TRATAR SÍMBOLOS ESPECIALES DEL INDEC

columnas_niveles = [
    "jardin_0_3",
    "sala_4_5",
    "primario",
    "secundario",
    "terciario",
    "universitario",
    "posgrado"
]

columnas_numericas_edu_02 = [
    "poblacion",
    "asiste_edu02"
] + columnas_niveles


# "-" representa valor cero en la tabla.
#
# "///" indica que el dato no corresponde a esa
# combinación de edad y nivel educativo.
#
# Para los cálculos de suma por nivel lo tratamos como NaN,
# no como cero, para conservar la diferencia conceptual.

for columna in columnas_numericas_edu_02:

    educacion_nivel[columna] = (
        educacion_nivel[columna]
        .replace(
            {
                "-": 0,
                "///": pd.NA
            }
        )
    )

    educacion_nivel[columna] = pd.to_numeric(
        educacion_nivel[columna],
        errors="coerce"
    )


# 7. VALIDAR CANTIDAD DE PARTIDOS Y EDADES

print("\nEDU_02 - POBLACIÓN POR NIVEL EDUCATIVO")

print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_nivel[
        "partido"
    ].nunique()
)

print("\nDIMENSIONES:")
print(
    educacion_nivel.shape
)

print("\nEDAD MÍNIMA:")
print(
    educacion_nivel[
        "edad"
    ].min()
)

print("\nEDAD MÁXIMA:")
print(
    educacion_nivel[
        "edad"
    ].max()
)

print("\nCANTIDAD DE EDADES POR PARTIDO:")

print(
    educacion_nivel
    .groupby("partido")["edad"]
    .nunique()
    .describe()
)


# 8. VALIDAR DUPLICADOS PARTIDO-EDAD

print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    educacion_nivel
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)


# 9. REVISAR VALORES NULOS

print("\nVALORES NULOS:")

print(
    educacion_nivel
    .isna()
    .sum()
)


# 10. COMPROBAR QUE LA SUMA DE NIVELES COINCIDA CON
#     LA POBLACIÓN QUE ASISTE
#
# min_count=1 evita convertir una fila completamente
# no aplicable en un cero artificial.

educacion_nivel[
    "suma_niveles"
] = (
    educacion_nivel[
        columnas_niveles
    ]
    .sum(
        axis=1,
        skipna=True,
        min_count=1
    )
)

educacion_nivel[
    "diferencia_control_niveles"
] = (
    educacion_nivel[
        "asiste_edu02"
    ]
    - educacion_nivel[
        "suma_niveles"
    ]
)

diferencias_niveles = educacion_nivel[
    educacion_nivel[
        "diferencia_control_niveles"
    ].fillna(0) != 0
]

print(
    "\nREGISTROS DONDE LA SUMA DE NIVELES "
    "NO COINCIDE CON LA POBLACIÓN QUE ASISTE:"
)

if len(diferencias_niveles) == 0:

    print(
        "Todos los registros son consistentes."
    )

else:

    print("\nCANTIDAD DE DIFERENCIAS:")
    print(
        len(diferencias_niveles)
    )

    print("\nPRIMERAS 30 DIFERENCIAS:")

    print(
        diferencias_niveles[
            [
                "partido",
                "edad",
                "asiste_edu02",
                "suma_niveles",
                "diferencia_control_niveles"
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


# 11. COMPARAR EDU_01 Y EDU_02
# EN LAS EDADES QUE COMPARTEN: 0-29

comparacion_edu_01_02 = (
    edu_01[
        edu_01["edad"].between(0, 29)
    ][
        [
            "partido",
            "edad",
            "asiste"
        ]
    ]
    .merge(
        educacion_nivel[
            [
                "partido",
                "edad",
                "asiste_edu02"
            ]
        ],
        on=[
            "partido",
            "edad"
        ],
        how="outer"
    )
)

comparacion_edu_01_02["diferencia_asistencia"] = (
    comparacion_edu_01_02["asiste"]
    - comparacion_edu_01_02["asiste_edu02"]
)

diferencias_asistencia = comparacion_edu_01_02[
    comparacion_edu_01_02[
        "diferencia_asistencia"
    ].fillna(0) != 0
]

print(
    "\nCOMPARACIÓN DE ASISTENCIA ENTRE EDU_01 Y EDU_02:"
)

if len(diferencias_asistencia) == 0:

    print(
        "La cantidad de población que asiste "
        "coincide entre EDU_01 y EDU_02."
    )

else:

    print("\nCANTIDAD DE DIFERENCIAS:")
    print(
        len(diferencias_asistencia)
    )

    print("\nPRIMERAS 30 DIFERENCIAS:")

    print(
        diferencias_asistencia
        .head(30)
        .to_string(index=False)
    )


# 12. COMPROBAR PARTIDOS ENTRE EDU_01 Y EDU_02

partidos_edu_01 = set(
    edu_01["partido"].unique()
)

partidos_edu_02 = set(
    educacion_nivel["partido"].unique()
)

print(
    "\nPARTIDOS DE EDU_01 QUE NO APARECEN EN EDU_02:"
)

print(
    partidos_edu_01
    - partidos_edu_02
)

print(
    "\nPARTIDOS DE EDU_02 QUE NO APARECEN EN EDU_01:"
)

print(
    partidos_edu_02
    - partidos_edu_01
)

# 13. MOSTRAR PRIMERAS FILAS

print("\nPRIMERAS 20 FILAS EDU_02:")

print(
    educacion_nivel
    .head(20)
    .to_string(index=False)
)


# 14. EJEMPLO - GENERAL PUEYRREDON

print(
    "\nEJEMPLO EDU_02 - GENERAL PUEYRREDON:"
)

print(
    educacion_nivel[
        educacion_nivel[
            "partido"
        ] == "GENERAL PUEYRREDON"
    ]
    .head(30)
    .to_string(index=False)
)
# --------------------------------------------------------------
print('--------------------------------------------------------------')
# BLOQUE 3 - EDU_03
# MÁXIMO NIVEL EDUCATIVO ALCANZADO

print("\nBLOQUE 3 - EDU_03")
print("MÁXIMO NIVEL EDUCATIVO ALCANZADO")


# 1. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO EDU_03

archivo_edu_03 = None

for archivo in os.listdir(carpeta_educacion):

    if (
        archivo.startswith("3.2")
        and archivo.lower().endswith(".xlsx")
    ):

        archivo_edu_03 = os.path.join(
            carpeta_educacion,
            archivo
        )

        break


if archivo_edu_03 is None:

    raise FileNotFoundError(
        "No se encontró el archivo EDU_03"
    )


print("\nARCHIVO EDU_03 ENCONTRADO:")
print(archivo_edu_03)


# 2. IDENTIFICAR LAS 135 HOJAS DE PARTIDOS

excel_edu_03 = pd.ExcelFile(
    archivo_edu_03
)

hojas_partidos_edu_03 = [
    hoja
    for hoja in excel_edu_03.sheet_names
    if re.fullmatch(
        r"Cuadro 3\.2\.\d+",
        hoja
    )
]


print("\nCANTIDAD DE HOJAS DE PARTIDOS EDU_03:")
print(
    len(hojas_partidos_edu_03)
)


# 3. RECUPERAR LA FILA TOTAL DE CADA PARTIDO

datos_edu_03 = []


for hoja in hojas_partidos_edu_03:

    df = pd.read_excel(
        archivo_edu_03,
        sheet_name=hoja,
        header=None
    )


    # IDENTIFICAR EL PARTIDO DESDE EL TÍTULO

    titulo = str(
        df.iloc[1, 0]
    )

    coincidencia = re.search(
        r"partido\s+(.+?)\.\s*Poblaci[oó]n",
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


    # IDENTIFICAR LA FILA TOTAL

    filas_total = df.index[
        df.iloc[:, 0]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("total")
    ].tolist()


    if len(filas_total) == 0:

        print(
            "No se encontró la fila Total:",
            partido
        )

        continue


    fila_total = filas_total[0]


    # EXTRAER LOS VALORES DE LA FILA TOTAL

    fila = df.iloc[
        fila_total,
        2:27
    ].copy()


    fila.index = [

        "poblacion_5_mas",

        "poblacion_que_asistio",

        "sin_instruccion",

        "primario_total",
        "primario_incompleto",
        "primario_completo",

        "egb_total",
        "egb_incompleto",
        "egb_completo",

        "secundario_total",
        "secundario_incompleto",
        "secundario_completo",

        "polimodal_total",
        "polimodal_incompleto",
        "polimodal_completo",

        "terciario_total",
        "terciario_incompleto",
        "terciario_completo",

        "universitario_total",
        "universitario_incompleto",
        "universitario_completo",

        "posgrado_total",
        "posgrado_incompleto",
        "posgrado_completo",

        "ignorado"
    ]


    registro = fila.to_dict()

    registro["partido"] = partido

    datos_edu_03.append(
        registro
    )


# 4. CREAR DATAFRAME

educacion_maximo_nivel = pd.DataFrame(
    datos_edu_03
)


# 5. ORDENAR COLUMNAS

educacion_maximo_nivel = educacion_maximo_nivel[
    [
        "partido",

        "poblacion_5_mas",
        "poblacion_que_asistio",

        "sin_instruccion",

        "primario_total",
        "primario_incompleto",
        "primario_completo",

        "egb_total",
        "egb_incompleto",
        "egb_completo",

        "secundario_total",
        "secundario_incompleto",
        "secundario_completo",

        "polimodal_total",
        "polimodal_incompleto",
        "polimodal_completo",

        "terciario_total",
        "terciario_incompleto",
        "terciario_completo",

        "universitario_total",
        "universitario_incompleto",
        "universitario_completo",

        "posgrado_total",
        "posgrado_incompleto",
        "posgrado_completo",

        "ignorado"
    ]
]


# 6. CONVERTIR VARIABLES A NUMÉRICAS

columnas_numericas_edu_03 = [
    columna
    for columna in educacion_maximo_nivel.columns
    if columna != "partido"
]


# En las tablas del INDEC:
# "-" representa cero.
# "///" indica que el dato no corresponde.
#
# En la fila Total no deberían aparecer valores "///",
# pero mantenemos el tratamiento por seguridad.

for columna in columnas_numericas_edu_03:

    educacion_maximo_nivel[columna] = (
        educacion_maximo_nivel[columna]
        .replace(
            {
                "-": 0,
                "///": pd.NA
            }
        )
    )

    educacion_maximo_nivel[columna] = pd.to_numeric(
        educacion_maximo_nivel[columna],
        errors="coerce"
    )


# 7. VALIDACIONES GENERALES

print("\nEDU_03 - MÁXIMO NIVEL EDUCATIVO ALCANZADO")


print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_maximo_nivel[
        "partido"
    ].nunique()
)


print("\nDIMENSIONES:")
print(
    educacion_maximo_nivel.shape
)


print("\nFILAS DUPLICADAS POR PARTIDO:")
print(
    educacion_maximo_nivel
    .duplicated(
        subset=["partido"]
    )
    .sum()
)


print("\nVALORES NULOS:")
print(
    educacion_maximo_nivel
    .isna()
    .sum()
)


# 8. VALIDAR TOTAL = INCOMPLETO + COMPLETO

niveles_con_completitud = [
    "primario",
    "egb",
    "secundario",
    "polimodal",
    "terciario",
    "universitario",
    "posgrado"
]


print(
    "\nVALIDACIÓN TOTAL = INCOMPLETO + COMPLETO "
    "POR NIVEL:"
)


for nivel in niveles_con_completitud:

    columna_diferencia = (
        f"diferencia_{nivel}"
    )

    educacion_maximo_nivel[
        columna_diferencia
    ] = (
        educacion_maximo_nivel[
            f"{nivel}_total"
        ]
        - (
            educacion_maximo_nivel[
                f"{nivel}_incompleto"
            ]
            + educacion_maximo_nivel[
                f"{nivel}_completo"
            ]
        )
    )


    errores = educacion_maximo_nivel[
        educacion_maximo_nivel[
            columna_diferencia
        ].fillna(0) != 0
    ]


    print(
        f"\n{nivel.upper()}:"
    )

    if len(errores) == 0:

        print(
            "Todos los registros son consistentes."
        )

    else:

        print(
            "Cantidad de diferencias:",
            len(errores)
        )

        print(
            errores[
                [
                    "partido",
                    f"{nivel}_total",
                    f"{nivel}_incompleto",
                    f"{nivel}_completo",
                    columna_diferencia
                ]
            ]
            .head(20)
            .to_string(index=False)
        )


# 9. VALIDAR SUMA DE NIVELES EDUCATIVOS

columnas_totales_niveles = [
    "sin_instruccion",
    "primario_total",
    "egb_total",
    "secundario_total",
    "polimodal_total",
    "terciario_total",
    "universitario_total",
    "posgrado_total",
    "ignorado"
]


educacion_maximo_nivel[
    "suma_niveles"
] = (
    educacion_maximo_nivel[
        columnas_totales_niveles
    ]
    .sum(
        axis=1,
        skipna=True
    )
)


educacion_maximo_nivel[
    "diferencia_poblacion_que_asistio"
] = (
    educacion_maximo_nivel[
        "poblacion_que_asistio"
    ]
    - educacion_maximo_nivel[
        "suma_niveles"
    ]
)


errores_suma_edu_03 = educacion_maximo_nivel[
    educacion_maximo_nivel[
        "diferencia_poblacion_que_asistio"
    ].fillna(0) != 0
]


print(
    "\nREGISTROS DONDE LA SUMA DE NIVELES "
    "NO COINCIDE CON POBLACIÓN QUE ASISTIÓ:"
)


if len(errores_suma_edu_03) == 0:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        "\nCANTIDAD DE DIFERENCIAS:"
    )

    print(
        len(errores_suma_edu_03)
    )

    print(
        "\nPRIMERAS 20 DIFERENCIAS:"
    )

    print(
        errores_suma_edu_03[
            [
                "partido",
                "poblacion_que_asistio",
                "suma_niveles",
                "diferencia_poblacion_que_asistio"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


# 10. COMPROBAR PARTIDOS CON EDU_01

partidos_edu_01 = set(
    edu_01[
        "partido"
    ].unique()
)

partidos_edu_03 = set(
    educacion_maximo_nivel[
        "partido"
    ].unique()
)


print(
    "\nPARTIDOS DE EDU_01 QUE NO APARECEN EN EDU_03:"
)

print(
    partidos_edu_01
    - partidos_edu_03
)


print(
    "\nPARTIDOS DE EDU_03 QUE NO APARECEN EN EDU_01:"
)

print(
    partidos_edu_03
    - partidos_edu_01
)


# 11. MOSTRAR RESULTADOS

print(
    "\nPRIMERAS 10 FILAS EDU_03:"
)

print(
    educacion_maximo_nivel
    .head(10)
    .to_string(index=False)
)


print(
    "\nEJEMPLO EDU_03 - GENERAL PUEYRREDON:"
)

print(
    educacion_maximo_nivel[
        educacion_maximo_nivel[
            "partido"
        ] == "GENERAL PUEYRREDON"
    ]
    .to_string(index=False)
)
# ============================================================
# INTEGRACIÓN DE EDUCACIÓN
# EDU_01 + EDU_02 + EDU_03
# ============================================================

print("\nINTEGRACIÓN DE EDUCACIÓN")
print("EDU_01 + EDU_02 + EDU_03")


# 1. UNIR EDU_01 CON EDU_02
#
# EDU_01 se utiliza como base porque contiene un rango
# de edades mayor.
#
# De EDU_02 incorporamos únicamente las variables de
# nivel educativo, ya que población y asistencia fueron
# previamente validadas contra EDU_01.


columnas_edu_02_integracion = [
    "partido",
    "edad",
    "jardin_0_3",
    "sala_4_5",
    "primario",
    "secundario",
    "terciario",
    "universitario",
    "posgrado"
]


educacion_censo_2022 = edu_01.merge(
    educacion_nivel[
        columnas_edu_02_integracion
    ],
    on=[
        "partido",
        "edad"
    ],
    how="left",
    validate="one_to_one"
)


# 2. VALIDAR INTEGRACIÓN EDU_01 + EDU_02

print("\nINTEGRACIÓN EDU_01 + EDU_02")


print("\nDIMENSIONES:")
print(
    educacion_censo_2022.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_censo_2022[
        "partido"
    ].nunique()
)


print("\nEDAD MÍNIMA:")
print(
    educacion_censo_2022[
        "edad"
    ].min()
)


print("\nEDAD MÁXIMA:")
print(
    educacion_censo_2022[
        "edad"
    ].max()
)


print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    educacion_censo_2022
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)


print("\nVALORES NULOS:")
print(
    educacion_censo_2022
    .isna()
    .sum()
)


# 3. PREPARAR EDU_03 PARA LA INTEGRACIÓN
#
# EDU_03 contiene una fila por partido.
#
# Las columnas "diferencia_*" y "suma_niveles"
# fueron creadas únicamente para validar la limpieza,
# por lo que no se incorporan al dataset final.


columnas_control_edu_03 = [
    "diferencia_primario",
    "diferencia_egb",
    "diferencia_secundario",
    "diferencia_polimodal",
    "diferencia_terciario",
    "diferencia_universitario",
    "diferencia_posgrado",
    "suma_niveles",
    "diferencia_poblacion_que_asistio"
]


edu_03_integracion = educacion_maximo_nivel.drop(
    columns=columnas_control_edu_03,
    errors="ignore"
)


# 4. UNIR EDU_03
#
# La unión se realiza únicamente por partido.
#
# many_to_one:
# educacion_censo_2022 tiene muchas edades por partido,
# mientras que EDU_03 tiene una sola fila por partido.


educacion_censo_2022 = educacion_censo_2022.merge(
    edu_03_integracion,
    on="partido",
    how="left",
    validate="many_to_one"
)


# 5. VALIDACIONES DE LA INTEGRACIÓN FINAL

print(
    "\nINTEGRACIÓN FINAL EDU_01 + EDU_02 + EDU_03"
)


print("\nDIMENSIONES:")
print(
    educacion_censo_2022.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_censo_2022[
        "partido"
    ].nunique()
)


print("\nCANTIDAD DE FILAS:")
print(
    len(educacion_censo_2022)
)


print("\nEDAD MÍNIMA:")
print(
    educacion_censo_2022[
        "edad"
    ].min()
)


print("\nEDAD MÁXIMA:")
print(
    educacion_censo_2022[
        "edad"
    ].max()
)


print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    educacion_censo_2022
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)


# 6. COMPROBAR QUE TODOS LOS REGISTROS
#    ENCONTRARON INFORMACIÓN DE EDU_03

print("\nREGISTROS SIN INFORMACIÓN DE EDU_03:")

print(
    educacion_censo_2022[
        "poblacion_5_mas"
    ]
    .isna()
    .sum()
)


# 7. MOSTRAR RESULTADOS

print("\nPRIMERAS 10 FILAS:")

print(
    educacion_censo_2022
    .head(10)
    .to_string(index=False)
)


print("\nEJEMPLO - GENERAL PUEYRREDON:")

print(
    educacion_censo_2022[
        educacion_censo_2022[
            "partido"
        ] == "GENERAL PUEYRREDON"
    ]
    .head(10)
    .to_string(index=False)
)
# 8. LIMPIEZA FINAL DEL DATASET INTEGRADO
#
# Eliminamos variables creadas únicamente para controles
# internos durante la limpieza.
#
# Se conserva tasa_asistencia porque constituye una
# variable analítica derivada útil para el proyecto.

columnas_control_final = [
    "suma_condiciones",
    "diferencia_control"
]

educacion_censo_2022 = educacion_censo_2022.drop(
    columns=columnas_control_final,
    errors="ignore"
)


# 9. VALIDACIÓN FINAL

print(
    "\nDATASET FINAL DE EDUCACIÓN - CENSO 2022"
)

print("\nDIMENSIONES:")
print(
    educacion_censo_2022.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_censo_2022["partido"].nunique()
)

print("\nCANTIDAD DE COLUMNAS:")
print(
    len(educacion_censo_2022.columns)
)

print("\nCOLUMNAS FINALES:")

for columna in educacion_censo_2022.columns:
    print(
        "-",
        columna
    )

print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    educacion_censo_2022
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)

# 10. REVISIÓN DE TIPOS DE DATOS ANTES DE EXPORTAR

print(
    "\nTIPOS DE DATOS DEL DATASET FINAL:"
)

print(
    educacion_censo_2022.dtypes
)


# 11. GUARDAR DATASET FINAL DE EDUCACIÓN - CENSO 2022

carpeta_salida_educacion = os.path.join(
    carpeta_educacion,
    "procesados"
)

os.makedirs(
    carpeta_salida_educacion,
    exist_ok=True
)

archivo_salida_educacion = os.path.join(
    carpeta_salida_educacion,
    "educacion_censo_2022.csv"
)

educacion_censo_2022.to_csv(
    archivo_salida_educacion,
    index=False,
    encoding="utf-8-sig"
)


# 12. COMPROBAR QUE EL ARCHIVO SE GUARDÓ CORRECTAMENTE

if os.path.exists(archivo_salida_educacion):

    print(
        "\nDATASET DE EDUCACIÓN GUARDADO CORRECTAMENTE:"
    )

    print(
        archivo_salida_educacion
    )

else:

    raise FileNotFoundError(
        "No se pudo guardar el dataset final de educación."
    )


# 13. VERIFICAR EL CSV GENERADO

educacion_verificacion = pd.read_csv(
    archivo_salida_educacion
)

print(
    "\nVERIFICACIÓN DEL ARCHIVO EXPORTADO"
)

print("\nDIMENSIONES:")
print(
    educacion_verificacion.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_verificacion[
        "partido"
    ].nunique()
)

print("\nDUPLICADOS PARTIDO-EDAD:")
print(
    educacion_verificacion
    .duplicated(
        subset=[
            "partido",
            "edad"
        ]
    )
    .sum()
)

print("\nARCHIVO FINAL:")
print(
    archivo_salida_educacion
)