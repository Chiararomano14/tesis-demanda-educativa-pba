import os
import pandas as pd


# ============================================================
# LIMPIEZA DE HOGARES
# HOG_01 - PROVISIÓN Y PROCEDENCIA DEL AGUA
# ============================================================

print("--------------------------------------------------------------")
print("LIMPIEZA DE HOGARES")
print("HOG_01 - PROVISIÓN Y PROCEDENCIA DEL AGUA")


# 1. RUTAS

carpeta_hogares = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /hogares"
)

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)


# 2. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO HOG_01

archivo_hog_01 = None

for archivo in os.listdir(carpeta_hogares):

    if (
        archivo.startswith("2.2")
        and archivo.lower().endswith(".xlsx")
    ):
        archivo_hog_01 = os.path.join(
            carpeta_hogares,
            archivo
        )
        break


if archivo_hog_01 is None:
    raise FileNotFoundError(
        "No se encontró el archivo HOG_01"
    )


print("\nARCHIVO HOG_01:")
print(archivo_hog_01)


# 3. LEER LAS HOJAS DEL EXCEL

excel_hog_01 = pd.ExcelFile(
    archivo_hog_01
)


# Seleccionar solamente las 135 hojas correspondientes
# a los partidos.
# Quedan afuera:
# - Carátula
# - Índice
# - Cuadro2.2 (total provincial)

hojas_partidos = []

for hoja in excel_hog_01.sheet_names:

    if hoja.startswith("Cuadro2.2."):

        numero = hoja.replace(
            "Cuadro2.2.",
            ""
        )

        if numero.isdigit():
            hojas_partidos.append(hoja)


print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
print(len(hojas_partidos))


# 4. EXTRAER INFORMACIÓN DE CADA PARTIDO

registros = []


for hoja in hojas_partidos:

    df = pd.read_excel(
        archivo_hog_01,
        sheet_name=hoja,
        header=None
    )


    # --------------------------------------------------------
    # OBTENER NOMBRE DEL PARTIDO DESDE EL TÍTULO
    # --------------------------------------------------------

    titulo = None

    for i in range(min(5, len(df))):

        texto = str(df.iloc[i, 0])

        texto = texto.replace(
            "\xa0",
            " "
        )

        texto = " ".join(
            texto.split()
        )

        if "partido " in texto.lower():
            titulo = texto
            break


    if titulo is None:

        print("\nERROR EN LA HOJA:")
        print(repr(hoja))

        print("\nPRIMERAS 5 FILAS:")
        print(
            df.iloc[:5, 0].to_string()
        )

        raise ValueError(
            f"No se pudo identificar el partido en {hoja}"
        )


    # Extraer el nombre ubicado después de "Partido"

    posicion_partido = titulo.lower().find(
        "partido "
    )

    partido = titulo[
        posicion_partido + len("partido "):
    ]

    # En este archivo el nombre termina antes de
    # ". Total de hogares"

    partido = partido.split(
        ". Total de hogares"
    )[0]

    partido = partido.strip().upper()


    # --------------------------------------------------------
    # EXTRAER FILAS IMPORTANTES
    # --------------------------------------------------------

    fila_total = None
    fila_red_publica = None


    for _, fila in df.iterrows():

        categoria = str(
            fila.iloc[0]
        ).strip()

        categoria_normalizada = (
            categoria
            .replace("\xa0", " ")
            .lower()
        )


        if categoria_normalizada == "total":
            fila_total = fila


        elif "red pública" in categoria_normalizada:
            fila_red_publica = fila


    if fila_total is None:
        raise ValueError(
            f"No se encontró la fila Total en {hoja}"
        )


    if fila_red_publica is None:
        raise ValueError(
            f"No se encontró Red pública en {hoja}"
        )


    # --------------------------------------------------------
    # GUARDAR VARIABLES
    # --------------------------------------------------------

    registros.append({

        "partido":
            partido,

        "hogares_total":
            fila_total.iloc[1],

        "hogares_agua_red":
            fila_red_publica.iloc[1],

        "hogares_agua_dentro_vivienda":
            fila_total.iloc[2],

        "hogares_agua_fuera_vivienda_dentro_terreno":
            fila_total.iloc[3],

        "hogares_agua_fuera_terreno":
            fila_total.iloc[4]
    })


# 5. CREAR DATAFRAME

hog_01 = pd.DataFrame(
    registros
)


# 6. MOSTRAR RESULTADO PRELIMINAR

print("\n" + "=" * 70)
print("EXTRACCIÓN PRELIMINAR HOG_01")
print("=" * 70)


print("\nDIMENSIONES:")
print(hog_01.shape)


print("\nCANTIDAD DE PARTIDOS:")
print(
    hog_01["partido"].nunique()
)


print("\nPRIMERAS 15 FILAS:")

print(
    hog_01
    .head(15)
    .to_string(index=False)
)


# 7. CONTROL DE GENERAL PUEYRREDÓN

print("\nGENERAL PUEYRREDÓN:")

control_pueyrredon = hog_01[
    hog_01["partido"]
    .str.contains(
        "PUEYRRED",
        case=False,
        na=False
    )
]

print(
    control_pueyrredon.to_string(
        index=False
    )
)


# 8. BUSCAR DUPLICADOS

print("\nPARTIDOS DUPLICADOS:")

duplicados = hog_01.duplicated(
    subset=["partido"]
)

print(
    duplicados.sum()
)


if duplicados.any():

    print(
        hog_01[
            duplicados
        ].to_string(index=False)
    )


# 9. VALORES NULOS

print("\nVALORES NULOS:")

print(
    hog_01.isnull().sum()
)


# 10. FIN DE LA EXTRACCIÓN PRELIMINAR

print("\n" + "=" * 70)
print("EXTRACCIÓN PRELIMINAR HOG_01 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# VALIDACIÓN DEFINITIVA HOG_01
# ============================================================

print("\n" + "=" * 70)
print("VALIDACIÓN DEFINITIVA HOG_01")
print("=" * 70)


# ------------------------------------------------------------
# 1. ASEGURAR TIPOS NUMÉRICOS
# ------------------------------------------------------------

columnas_numericas = [
    "hogares_total",
    "hogares_agua_red",
    "hogares_agua_dentro_vivienda",
    "hogares_agua_fuera_vivienda_dentro_terreno",
    "hogares_agua_fuera_terreno"
]


for columna in columnas_numericas:

    hog_01[columna] = pd.to_numeric(
        hog_01[columna],
        errors="raise"
    ).astype(int)


# ------------------------------------------------------------
# 2. CONTROL DE UBICACIÓN DE LA PROVISIÓN DE AGUA
# ------------------------------------------------------------

# Estas tres categorías deberían sumar el total de hogares:
#
# - agua dentro de la vivienda
# - agua fuera de la vivienda pero dentro del terreno
# - agua fuera del terreno

hog_01["suma_ubicacion_agua"] = (
    hog_01["hogares_agua_dentro_vivienda"]
    + hog_01["hogares_agua_fuera_vivienda_dentro_terreno"]
    + hog_01["hogares_agua_fuera_terreno"]
)


hog_01["diferencia_control_ubicacion"] = (
    hog_01["hogares_total"]
    - hog_01["suma_ubicacion_agua"]
)


# ------------------------------------------------------------
# 3. CONTROL DE HOGARES CON AGUA DE RED
# ------------------------------------------------------------

# La cantidad de hogares con agua de red pública
# nunca debería superar el total de hogares.

errores_agua_red = hog_01[
    hog_01["hogares_agua_red"]
    > hog_01["hogares_total"]
]


# ------------------------------------------------------------
# 4. CREAR INDICADOR: % DE HOGARES CON AGUA DE RED
# ------------------------------------------------------------

hog_01["porcentaje_hogares_agua_red"] = (
    hog_01["hogares_agua_red"]
    / hog_01["hogares_total"]
    * 100
)


# Redondeamos a 2 decimales

hog_01["porcentaje_hogares_agua_red"] = (
    hog_01["porcentaje_hogares_agua_red"]
    .round(2)
)


# ------------------------------------------------------------
# 5. VALIDAR CONSISTENCIA DE UBICACIÓN
# ------------------------------------------------------------

errores_ubicacion = hog_01[
    hog_01["diferencia_control_ubicacion"] != 0
]


print(
    "\nREGISTROS DONDE LA SUMA DE LAS CATEGORÍAS "
    "DE UBICACIÓN NO COINCIDE CON EL TOTAL:"
)


if errores_ubicacion.empty:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        errores_ubicacion.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 6. VALIDAR AGUA DE RED
# ------------------------------------------------------------

print(
    "\nREGISTROS DONDE HOGARES CON AGUA DE RED "
    "SUPERA EL TOTAL DE HOGARES:"
)


if errores_agua_red.empty:

    print(
        "No se encontraron inconsistencias."
    )

else:

    print(
        errores_agua_red.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 7. VALORES NULOS
# ------------------------------------------------------------

print("\nVALORES NULOS:")

print(
    hog_01.isnull().sum()
)


# ------------------------------------------------------------
# 8. TIPOS DE DATOS
# ------------------------------------------------------------

print("\nTIPOS DE DATOS:")

print(
    hog_01.dtypes
)


# ------------------------------------------------------------
# 9. CONTROL DE PORCENTAJES
# ------------------------------------------------------------

print("\nRANGO DEL PORCENTAJE DE HOGARES CON AGUA DE RED:")

print(
    "Mínimo:",
    hog_01["porcentaje_hogares_agua_red"].min()
)

print(
    "Máximo:",
    hog_01["porcentaje_hogares_agua_red"].max()
)


porcentajes_invalidos = hog_01[
    (hog_01["porcentaje_hogares_agua_red"] < 0)
    |
    (hog_01["porcentaje_hogares_agua_red"] > 100)
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


# ------------------------------------------------------------
# 10. CONTROL DE GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\nGENERAL PUEYRREDÓN:")

print(
    hog_01[
        hog_01["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 11. MOSTRAR PRIMERAS FILAS
# ------------------------------------------------------------

print("\nPRIMERAS 15 FILAS HOG_01:")

print(
    hog_01
    .head(15)
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 12. RESUMEN FINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN DEFINITIVA HOG_01 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# LIMPIEZA DE HOGARES
# HOG_02 - BAÑO/LETRINA, DESAGÜE Y DESCARGA DE AGUA
# ============================================================

print("--------------------------------------------------------------")
print("LIMPIEZA DE HOGARES")
print("HOG_02 - BAÑO/LETRINA, DESAGÜE Y DESCARGA DE AGUA")


# ------------------------------------------------------------
# 1. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO HOG_02
# ------------------------------------------------------------

archivo_hog_02 = None

for archivo in os.listdir(carpeta_hogares):

    if (
        archivo.startswith("3.2")
        and archivo.lower().endswith(".xlsx")
    ):
        archivo_hog_02 = os.path.join(
            carpeta_hogares,
            archivo
        )
        break


if archivo_hog_02 is None:
    raise FileNotFoundError(
        "No se encontró el archivo HOG_02"
    )


print("\nARCHIVO HOG_02:")
print(archivo_hog_02)


# ------------------------------------------------------------
# 2. LEER LAS HOJAS
# ------------------------------------------------------------

excel_hog_02 = pd.ExcelFile(
    archivo_hog_02
)


# Seleccionar únicamente las 135 hojas correspondientes
# a partidos.
#
# Quedan afuera:
# - Carátula
# - Índice
# - Cuadro3.2 (total provincial)

hojas_partidos = []

for hoja in excel_hog_02.sheet_names:

    if hoja.startswith("Cuadro3.2."):

        numero = hoja.replace(
            "Cuadro3.2.",
            ""
        )

        if numero.isdigit():
            hojas_partidos.append(hoja)


print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
print(len(hojas_partidos))


# ------------------------------------------------------------
# 3. EXTRAER INFORMACIÓN DE CADA PARTIDO
# ------------------------------------------------------------

registros = []


for hoja in hojas_partidos:

    df = pd.read_excel(
        archivo_hog_02,
        sheet_name=hoja,
        header=None
    )


    # --------------------------------------------------------
    # OBTENER NOMBRE DEL PARTIDO
    # --------------------------------------------------------

    titulo = None

    for i in range(min(5, len(df))):

        texto = str(
            df.iloc[i, 0]
        )

        texto = texto.replace(
            "\xa0",
            " "
        )

        texto = " ".join(
            texto.split()
        )

        if "partido " in texto.lower():
            titulo = texto
            break


    if titulo is None:

        print("\nERROR EN LA HOJA:")
        print(repr(hoja))

        print("\nPRIMERAS 5 FILAS:")
        print(
            df.iloc[:5, 0].to_string()
        )

        raise ValueError(
            f"No se pudo identificar el partido en {hoja}"
        )


    posicion_partido = titulo.lower().find(
        "partido "
    )

    partido = titulo[
        posicion_partido + len("partido "):
    ]


    # El nombre termina antes de:
    # ". Total de hogares"

    partido = partido.split(
        ". Total de hogares"
    )[0]

    partido = (
        partido
        .strip()
        .upper()
    )


    # --------------------------------------------------------
    # 4. EXTRAER VARIABLES
    # --------------------------------------------------------
    #
    # Según la estructura observada durante la inspección:
    #
    # fila 4  -> Total de hogares
    # fila 5  -> Red pública (cloaca)
    # fila 10 -> Cámara séptica y pozo ciego
    # fila 15 -> Solo pozo ciego
    # fila 20 -> Hoyo/excavación
    # fila 25 -> No tiene baño/letrina
    #
    # columnas:
    # 2 -> total
    # 3 -> baño dentro de vivienda
    # 4 -> baño fuera de vivienda pero dentro del terreno
    # 5 -> no tiene


    registros.append({

        "partido":
            partido,

        "hogares_total":
            df.iloc[4, 2],

        "hogares_con_cloaca":
            df.iloc[5, 2],

        "hogares_camara_septica":
            df.iloc[10, 2],

        "hogares_solo_pozo_ciego":
            df.iloc[15, 2],

        "hogares_hoyo_excavacion":
            df.iloc[20, 2],

        "hogares_sin_banio":
            df.iloc[25, 2],

        "hogares_banio_dentro_vivienda":
            df.iloc[4, 3],

        "hogares_banio_fuera_vivienda":
            df.iloc[4, 4]
    })


# ------------------------------------------------------------
# 5. CREAR DATAFRAME
# ------------------------------------------------------------

hog_02 = pd.DataFrame(
    registros
)


# ------------------------------------------------------------
# 6. CONVERTIR VARIABLES A NUMÉRICAS
# ------------------------------------------------------------

columnas_numericas = [
    "hogares_total",
    "hogares_con_cloaca",
    "hogares_camara_septica",
    "hogares_solo_pozo_ciego",
    "hogares_hoyo_excavacion",
    "hogares_sin_banio",
    "hogares_banio_dentro_vivienda",
    "hogares_banio_fuera_vivienda"
]


for columna in columnas_numericas:

    hog_02[columna] = (
        hog_02[columna]
        .astype(str)
        .str.strip()
        .replace("-", "0")
    )

    hog_02[columna] = pd.to_numeric(
        hog_02[columna],
        errors="raise"
    ).astype(int)


# ------------------------------------------------------------
# 7. CONTROL DE TIPOS DE DESAGÜE
# ------------------------------------------------------------

hog_02["suma_tipo_saneamiento"] = (
    hog_02["hogares_con_cloaca"]
    + hog_02["hogares_camara_septica"]
    + hog_02["hogares_solo_pozo_ciego"]
    + hog_02["hogares_hoyo_excavacion"]
    + hog_02["hogares_sin_banio"]
)


hog_02["diferencia_control_saneamiento"] = (
    hog_02["hogares_total"]
    - hog_02["suma_tipo_saneamiento"]
)


# ------------------------------------------------------------
# 8. CONTROL DE UBICACIÓN DEL BAÑO
# ------------------------------------------------------------

hog_02["suma_ubicacion_banio"] = (
    hog_02["hogares_banio_dentro_vivienda"]
    + hog_02["hogares_banio_fuera_vivienda"]
    + hog_02["hogares_sin_banio"]
)


hog_02["diferencia_control_ubicacion"] = (
    hog_02["hogares_total"]
    - hog_02["suma_ubicacion_banio"]
)


# ------------------------------------------------------------
# 9. CREAR INDICADORES
# ------------------------------------------------------------

hog_02["porcentaje_hogares_cloaca"] = (
    hog_02["hogares_con_cloaca"]
    / hog_02["hogares_total"]
    * 100
).round(2)


hog_02["porcentaje_hogares_sin_banio"] = (
    hog_02["hogares_sin_banio"]
    / hog_02["hogares_total"]
    * 100
).round(2)


# ------------------------------------------------------------
# 10. VALIDACIÓN ESTRUCTURAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN PRELIMINAR HOG_02")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    hog_02.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    hog_02["partido"].nunique()
)


print("\nPARTIDOS DUPLICADOS:")

duplicados = hog_02.duplicated(
    subset=["partido"]
)

print(
    duplicados.sum()
)


print("\nVALORES NULOS:")

print(
    hog_02.isnull().sum()
)


print("\nTIPOS DE DATOS:")

print(
    hog_02.dtypes
)


# ------------------------------------------------------------
# 11. VALIDAR SANEAMIENTO
# ------------------------------------------------------------

errores_saneamiento = hog_02[
    hog_02["diferencia_control_saneamiento"] != 0
]


print(
    "\nREGISTROS DONDE LA SUMA DE LOS TIPOS DE "
    "SANEAMIENTO NO COINCIDE CON EL TOTAL:"
)


if errores_saneamiento.empty:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        errores_saneamiento.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 12. VALIDAR UBICACIÓN DEL BAÑO
# ------------------------------------------------------------

errores_ubicacion = hog_02[
    hog_02["diferencia_control_ubicacion"] != 0
]


print(
    "\nREGISTROS DONDE LA UBICACIÓN DEL BAÑO "
    "NO COINCIDE CON EL TOTAL:"
)


if errores_ubicacion.empty:

    print(
        "Todos los registros son consistentes."
    )

else:

    print(
        errores_ubicacion.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 13. CONTROL DE PORCENTAJES
# ------------------------------------------------------------

print("\nRANGO % HOGARES CON CLOACA:")

print(
    "Mínimo:",
    hog_02["porcentaje_hogares_cloaca"].min()
)

print(
    "Máximo:",
    hog_02["porcentaje_hogares_cloaca"].max()
)


print("\nRANGO % HOGARES SIN BAÑO:")

print(
    "Mínimo:",
    hog_02["porcentaje_hogares_sin_banio"].min()
)

print(
    "Máximo:",
    hog_02["porcentaje_hogares_sin_banio"].max()
)


# ------------------------------------------------------------
# 14. GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\nGENERAL PUEYRREDÓN:")

print(
    hog_02[
        hog_02["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 15. PRIMERAS FILAS
# ------------------------------------------------------------

print("\nPRIMERAS 15 FILAS HOG_02:")

print(
    hog_02
    .head(15)
    .to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("LIMPIEZA PRELIMINAR HOG_02 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)
# ============================================================
# NORMALIZACIÓN DE NOMBRES DE PARTIDOS
# ============================================================

print("\n" + "=" * 70)
print("NORMALIZACIÓN DE NOMBRES DE PARTIDOS")
print("=" * 70)


# ------------------------------------------------------------
# 1. DICCIONARIO DE NOMBRES ESTANDARIZADOS
# ------------------------------------------------------------

correcciones_partidos = {

    "CAPITAN SARMIENTO":
        "CAPITÁN SARMIENTO",

    "CHASCOMUS":
        "CHASCOMÚS",

    "COLON":
        "COLÓN",

    "EXALTACION DE LA CRUZ":
        "EXALTACIÓN DE LA CRUZ",

    "NUEVE DE JULIO":
        "9 DE JULIO"
}


# ------------------------------------------------------------
# 2. APLICAR CORRECCIONES
# ------------------------------------------------------------

hog_01["partido"] = (
    hog_01["partido"]
    .replace(correcciones_partidos)
)

hog_02["partido"] = (
    hog_02["partido"]
    .replace(correcciones_partidos)
)


# ------------------------------------------------------------
# 3. VERIFICAR RESULTADO
# ------------------------------------------------------------

partidos_hog_01 = set(
    hog_01["partido"]
)

partidos_hog_02 = set(
    hog_02["partido"]
)


print("\nPARTIDOS EN HOG_01 PERO NO EN HOG_02:")

print(
    sorted(
        partidos_hog_01 - partidos_hog_02
    )
)


print("\nPARTIDOS EN HOG_02 PERO NO EN HOG_01:")

print(
    sorted(
        partidos_hog_02 - partidos_hog_01
    )
)


if partidos_hog_01 == partidos_hog_02:

    print(
        "\nOK - HOG_01 y HOG_02 contienen "
        "exactamente los mismos 135 partidos."
    )

else:

    print(
        "\nATENCIÓN - Todavía existen diferencias "
        "entre los nombres de los partidos."
    )
# ============================================================
# VALIDACIÓN CRUZADA HOG_01 VS HOG_02
# ============================================================

print("\n" + "=" * 70)
print("VALIDACIÓN CRUZADA DE HOGARES")
print("HOG_01 - HOG_02")
print("=" * 70)


# ------------------------------------------------------------
# 1. COMPARAR CANTIDAD DE PARTIDOS
# ------------------------------------------------------------

print("\nCANTIDAD DE PARTIDOS:")

print(
    "HOG_01:",
    hog_01["partido"].nunique()
)

print(
    "HOG_02:",
    hog_02["partido"].nunique()
)


# ------------------------------------------------------------
# 2. COMPARAR NOMBRES DE PARTIDOS
# ------------------------------------------------------------

partidos_hog_01 = set(
    hog_01["partido"]
)

partidos_hog_02 = set(
    hog_02["partido"]
)


print("\nPARTIDOS EN HOG_01 PERO NO EN HOG_02:")

print(
    sorted(
        partidos_hog_01 - partidos_hog_02
    )
)


print("\nPARTIDOS EN HOG_02 PERO NO EN HOG_01:")

print(
    sorted(
        partidos_hog_02 - partidos_hog_01
    )
)


# ------------------------------------------------------------
# 3. COMPARAR TOTAL DE HOGARES
# ------------------------------------------------------------

comparacion_hogares = hog_01[
    [
        "partido",
        "hogares_total"
    ]
].merge(

    hog_02[
        [
            "partido",
            "hogares_total"
        ]
    ],

    on="partido",

    how="outer",

    suffixes=(
        "_hog01",
        "_hog02"
    ),

    indicator=True
)


print("\n" + "=" * 70)
print("COMPARACIÓN DE HOGARES TOTALES")
print("=" * 70)


print("\nRESULTADO DEL MERGE:")

print(
    comparacion_hogares["_merge"]
    .value_counts()
)


# ------------------------------------------------------------
# 4. CALCULAR DIFERENCIA DE HOGARES
# ------------------------------------------------------------

comparacion_hogares[
    "diferencia_hogares"
] = (

    comparacion_hogares[
        "hogares_total_hog01"
    ]

    -

    comparacion_hogares[
        "hogares_total_hog02"
    ]
)


diferencias = comparacion_hogares[

    (
        comparacion_hogares[
            "diferencia_hogares"
        ] != 0
    )

    |

    (
        comparacion_hogares[
            "_merge"
        ] != "both"
    )

]


print(
    "\nPARTIDOS DONDE EL TOTAL DE HOGARES "
    "NO COINCIDE:"
)


if diferencias.empty:

    print(
        "HOG_01 y HOG_02 coinciden "
        "en los 135 partidos."
    )

else:

    print(
        diferencias.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 5. CONTROL GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)


print("\nHOG_01:")

print(
    hog_01[
        hog_01["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ][
        [
            "partido",
            "hogares_total",
            "hogares_agua_red",
            "porcentaje_hogares_agua_red"
        ]
    ].to_string(
        index=False
    )
)


print("\nHOG_02:")

print(
    hog_02[
        hog_02["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ][
        [
            "partido",
            "hogares_total",
            "hogares_con_cloaca",
            "hogares_sin_banio",
            "porcentaje_hogares_cloaca",
            "porcentaje_hogares_sin_banio"
        ]
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 6. RESULTADO FINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN CRUZADA HOG_01 VS HOG_02 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)



# ============================================================
# INTEGRACIÓN FINAL HOG_01 + HOG_02
# ============================================================

print("\n" + "=" * 70)
print("INTEGRACIÓN HOG_01 + HOG_02")
print("=" * 70)


# ------------------------------------------------------------
# 1. SELECCIONAR VARIABLES NECESARIAS DE HOG_01
# ------------------------------------------------------------

hog_01_integracion = hog_01[
    [
        "partido",
        "hogares_total",
        "hogares_agua_red",
        "porcentaje_hogares_agua_red"
    ]
].copy()


# ------------------------------------------------------------
# 2. SELECCIONAR VARIABLES NECESARIAS DE HOG_02
# ------------------------------------------------------------

hog_02_integracion = hog_02[
    [
        "partido",
        "hogares_total",
        "hogares_con_cloaca",
        "porcentaje_hogares_cloaca",
        "hogares_sin_banio",
        "porcentaje_hogares_sin_banio"
    ]
].copy()


# ------------------------------------------------------------
# 3. UNIR HOG_01 Y HOG_02
# ------------------------------------------------------------

hogares = hog_01_integracion.merge(
    hog_02_integracion,
    on="partido",
    how="outer",
    suffixes=(
        "_hog01",
        "_hog02"
    ),
    indicator=True
)


print("\nRESULTADO DEL MERGE:")

print(
    hogares["_merge"]
    .value_counts()
)


print("\nDIMENSIONES DESPUÉS DEL MERGE:")
print(
    hogares.shape
)


# ------------------------------------------------------------
# 4. VERIFICAR QUE HOGARES_TOTAL COINCIDA
# ------------------------------------------------------------

diferencias_total = hogares[
    hogares["hogares_total_hog01"]
    != hogares["hogares_total_hog02"]
]


print("\nREGISTROS CON DIFERENCIAS EN HOGARES TOTALES:")


if diferencias_total.empty:

    print(
        "HOG_01 y HOG_02 coinciden "
        "en todos los registros."
    )

else:

    print(
        diferencias_total.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 5. CREAR UNA ÚNICA VARIABLE HOGARES_TOTAL
# ------------------------------------------------------------

hogares["hogares_total"] = (
    hogares["hogares_total_hog01"]
)


# ------------------------------------------------------------
# 6. AGREGAR AÑO
# ------------------------------------------------------------

hogares["anio"] = 2022


# ------------------------------------------------------------
# 7. SELECCIONAR ESTRUCTURA FINAL
# ------------------------------------------------------------

hogares_limpio = hogares[
    [
        "partido",
        "anio",
        "hogares_total",
        "hogares_agua_red",
        "porcentaje_hogares_agua_red",
        "hogares_con_cloaca",
        "porcentaje_hogares_cloaca",
        "hogares_sin_banio",
        "porcentaje_hogares_sin_banio"
    ]
].copy()


# ------------------------------------------------------------
# 8. ORDENAR DATASET
# ------------------------------------------------------------

hogares_limpio = (
    hogares_limpio
    .sort_values(
        by="partido"
    )
    .reset_index(
        drop=True
    )
)


# ------------------------------------------------------------
# 9. VALIDACIÓN FINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN DEL DATASET FINAL DE HOGARES")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    hogares_limpio.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    hogares_limpio["partido"].nunique()
)


print("\nAÑOS:")
print(
    sorted(
        hogares_limpio["anio"].unique()
    )
)


print("\nPARTIDOS DUPLICADOS:")
print(
    hogares_limpio.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


print("\nVALORES NULOS:")

print(
    hogares_limpio.isnull().sum()
)


print("\nTIPOS DE DATOS:")

print(
    hogares_limpio.dtypes
)


# ------------------------------------------------------------
# 10. CONTROL DE PORCENTAJES
# ------------------------------------------------------------

columnas_porcentajes = [
    "porcentaje_hogares_agua_red",
    "porcentaje_hogares_cloaca",
    "porcentaje_hogares_sin_banio"
]


print("\nRANGOS DE PORCENTAJES:")


for columna in columnas_porcentajes:

    print(
        f"\n{columna}:"
    )

    print(
        "Mínimo:",
        hogares_limpio[columna].min()
    )

    print(
        "Máximo:",
        hogares_limpio[columna].max()
    )


# ------------------------------------------------------------
# 11. CONTROL GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\nGENERAL PUEYRREDÓN:")

print(
    hogares_limpio[
        hogares_limpio["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 12. MOSTRAR PRIMERAS FILAS
# ------------------------------------------------------------

print("\nPRIMERAS 15 FILAS:")

print(
    hogares_limpio
    .head(15)
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 13. FIN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTEGRACIÓN HOG_01 + HOG_02 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# GUARDAR DATASET FINAL DE HOGARES
# ============================================================

print("\n" + "=" * 70)
print("GUARDADO DEL DATASET FINAL DE HOGARES")
print("=" * 70)


# ------------------------------------------------------------
# 1. DEFINIR RUTA DE SALIDA
# ------------------------------------------------------------

ruta_salida_hogares = os.path.join(
    carpeta_salida,
    "hogares_limpio.csv"
)


# ------------------------------------------------------------
# 2. GUARDAR ARCHIVO
# ------------------------------------------------------------

hogares_limpio.to_csv(
    ruta_salida_hogares,
    index=False,
    encoding="utf-8-sig"
)


# ------------------------------------------------------------
# 3. CONFIRMAR GUARDADO
# ------------------------------------------------------------

print("\nRUTA:")
print(
    ruta_salida_hogares
)


print("\nDIMENSIONES:")
print(
    hogares_limpio.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    hogares_limpio["partido"].nunique()
)


print("\nVALORES NULOS TOTALES:")
print(
    hogares_limpio.isnull().sum().sum()
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    hogares_limpio.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


print("\n" + "=" * 70)
print("ARCHIVO DE HOGARES GUARDADO CORRECTAMENTE")
print("=" * 70)