import os
import pandas as pd
import numpy as np

# INSPECCIÓN DE DATASETS LIMPIOS
# PREPARACIÓN PARA DATASET MAESTRO

print("=" * 70)
print("INSPECCIÓN DE DATASETS LIMPIOS")
print("PREPARACIÓN PARA INTEGRACIÓN Y DATASET MAESTRO")
print("=" * 70)



# 1. RUTA DE DATASETS LIMPIOS


carpeta_datos_limpios = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)



# 2. BUSCAR ARCHIVOS CSV


archivos_csv = sorted(
    [
        archivo
        for archivo in os.listdir(carpeta_datos_limpios)
        if archivo.lower().endswith(".csv")
    ]
)


print("\nCANTIDAD DE DATASETS LIMPIOS:")
print(len(archivos_csv))


print("\nARCHIVOS ENCONTRADOS:")

for archivo in archivos_csv:
    print("-", archivo)



# 3. INSPECCIONAR CADA DATASET


resumen = []


for archivo in archivos_csv:

    print("\n" + "=" * 70)
    print("DATASET:", archivo)
    print("=" * 70)

    ruta = os.path.join(
        carpeta_datos_limpios,
        archivo
    )

    df = pd.read_csv(ruta)

    print("\nDIMENSIONES:")
    print(df.shape)

    print("\nCOLUMNAS:")

    for columna in df.columns:
        print("-", columna)

    
    # PARTIDOS
    

    if "partido" in df.columns:

        cantidad_partidos = df["partido"].nunique()

        print("\nCANTIDAD DE PARTIDOS:")
        print(cantidad_partidos)

        print("\nPARTIDOS NULOS:")
        print(df["partido"].isnull().sum())

    else:

        cantidad_partidos = None

        print("\nADVERTENCIA:")
        print("El dataset no contiene la columna 'partido'.")

    
    # AÑOS
    

    if "anio" in df.columns:

        anios = sorted(
            df["anio"]
            .dropna()
            .unique()
            .tolist()
        )

        print("\nAÑOS:")
        print(anios)

    else:

        anios = []

        print("\nAÑOS:")
        print("El dataset no contiene columna 'anio'.")

    
    # NULOS
    

    print("\nVALORES NULOS TOTALES:")
    print(df.isnull().sum().sum())

    
    # DUPLICADOS
    

    if (
        "partido" in df.columns
        and "anio" in df.columns
    ):

        duplicados = df.duplicated(
            subset=["partido", "anio"]
        ).sum()

        print("\nDUPLICADOS PARTIDO-AÑO:")
        print(duplicados)

    elif "partido" in df.columns:

        duplicados = df["partido"].duplicated().sum()

        print("\nDUPLICADOS PARTIDO:")
        print(duplicados)

    else:

        duplicados = None

    
    # GUARDAR RESUMEN
    

    resumen.append(
        {
            "dataset": archivo,
            "filas": df.shape[0],
            "columnas": df.shape[1],
            "partidos": cantidad_partidos,
            "anios": str(anios),
            "nulos": int(
                df.isnull().sum().sum()
            ),
            "duplicados": duplicados
        }
    )



# 4. RESUMEN GENERAL


resumen_df = pd.DataFrame(resumen)


print("\n" + "=" * 70)
print("RESUMEN GENERAL DE DATASETS LIMPIOS")
print("=" * 70)

print(
    resumen_df.to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("INSPECCIÓN FINALIZADA")
print("TODAVÍA NO SE REALIZÓ NINGÚN MERGE")
print("=" * 70)

# 5. INSPECCIÓN DE GRANULARIDADES Y NULOS

print("\n" + "=" * 70)
print("INSPECCIÓN PREVIA A LA INTEGRACIÓN")
print("=" * 70)


# CARGAR DATASETS QUE NECESITAN REVISIÓN

educacion = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "educacion_censo_2022.csv"
    )
)

matricula = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "matricula_limpia.csv"
    )
)

fecundidad_edad = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "fecundidad_por_edad_limpio.csv"
    )
)

poblacion_base = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "poblacion_base_limpia.csv"
    )
)


# 5.1 EDUCACIÓN

print("\n" + "=" * 70)
print("EDUCACIÓN - EDADES")
print("=" * 70)

print("\nVALORES ÚNICOS DE EDAD:")

print(
    sorted(
        educacion["edad"]
        .dropna()
        .unique()
        .tolist()
    )
)

print("\nCANTIDAD DE FILAS POR PARTIDO:")

print(
    educacion.groupby("partido")
    .size()
    .describe()
)


# 5.2 MATRÍCULA

print("\n" + "=" * 70)
print("MATRÍCULA - NIVELES")
print("=" * 70)

print("\nNIVELES ENCONTRADOS:")

for nivel in sorted(
    matricula["nivel"]
    .dropna()
    .unique()
    .tolist()
):
    print("-", nivel)


print("\nCANTIDAD DE NIVELES:")
print(
    matricula["nivel"].nunique()
)


print("\nFILAS CON VALORES NULOS:")

nulos_matricula = matricula[
    matricula.isnull().any(axis=1)
]

if len(nulos_matricula) == 0:
    print("No hay filas con valores nulos.")
else:
    print(
        nulos_matricula.to_string(
            index=False
        )
    )


# 5.3 FECUNDIDAD POR EDAD

print("\n" + "=" * 70)
print("FECUNDIDAD - GRUPOS DE EDAD")
print("=" * 70)

print("\nGRUPOS DE EDAD:")

for grupo in fecundidad_edad[
    "grupo_edad"
].dropna().unique():

    print("-", grupo)


print("\nCANTIDAD DE GRUPOS:")
print(
    fecundidad_edad[
        "grupo_edad"
    ].nunique()
)


print("\nFILAS POR PARTIDO:")

print(
    fecundidad_edad.groupby(
        "partido"
    ).size().describe()
)


# 5.4 POBLACIÓN BASE

print("\n" + "=" * 70)
print("POBLACIÓN BASE - VALORES NULOS")
print("=" * 70)


print("\nNULOS POR COLUMNA:")

print(
    poblacion_base.isnull().sum()
)


print("\nFILAS QUE CONTIENEN NULOS:")

nulos_poblacion = poblacion_base[
    poblacion_base.isnull().any(axis=1)
]

if len(nulos_poblacion) == 0:

    print(
        "No hay filas con valores nulos."
    )

else:

    print(
        nulos_poblacion.to_string(
            index=False
        )
    )


# FINAL

print("\n" + "=" * 70)
print("INSPECCIÓN PREVIA A LA INTEGRACIÓN FINALIZADA")
print("TODAVÍA NO SE REALIZÓ EL DATASET MAESTRO")
print("=" * 70)

# 6. PREPARACIÓN DE MATRÍCULA PARA EL DATASET MAESTRO

print("\n" + "=" * 70)
print("6. PREPARACIÓN DE MATRÍCULA")
print("GRANULARIDAD: PARTIDO + AÑO")
print("=" * 70)


# 6.1 TRANSFORMAR NIVELES EN COLUMNAS

matricula_wide = (
    matricula
    .pivot(
        index=["partido", "anio"],
        columns="nivel",
        values="matricula"
    )
    .reset_index()
)


# Quitar el nombre interno generado por pivot
matricula_wide.columns.name = None

# ============================================================
# CONTROL ESPECIAL LEZAMA - DATOS ORIGINALES DE MATRÍCULA
# ============================================================

print("\n" + "=" * 70)
print("CONTROL LEZAMA - MATRÍCULA ORIGINAL")
print("=" * 70)

control_lezama_original = matricula[
    (matricula["partido"] == "LEZAMA")
    & (matricula["anio"].between(2012, 2022))
]

print(
    control_lezama_original.to_string(index=False)
)
# 6.2 RENOMBRAR COLUMNAS

matricula_wide = matricula_wide.rename(
    columns={
        "Inicial": "matricula_inicial",
        "Primaria": "matricula_primaria",
        "Secundaria": "matricula_secundaria"
    }
)


# 6.3 CALCULAR MATRÍCULA TOTAL

# min_count=3 hace que matricula_total quede NaN
# si falta alguno de los tres niveles.
# Así no confundimos "dato faltante" con matrícula 0.

matricula_wide["matricula_total"] = (
    matricula_wide[
        [
            "matricula_inicial",
            "matricula_primaria",
            "matricula_secundaria"
        ]
    ]
    .sum(
        axis=1,
        min_count=3
    )
)


# 6.4 VALIDACIÓN

print("\nDIMENSIONES:")
print(matricula_wide.shape)


print("\nCANTIDAD DE PARTIDOS:")
print(
    matricula_wide["partido"].nunique()
)


print("\nAÑOS:")
print(
    sorted(
        matricula_wide["anio"]
        .unique()
        .tolist()
    )
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    matricula_wide.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


print("\nNULOS POR COLUMNA:")
print(
    matricula_wide.isnull().sum()
)


# 6.5 CONTROL DE FILAS CON DATOS FALTANTES

print("\nFILAS CON MATRÍCULA FALTANTE:")

filas_matricula_faltante = matricula_wide[
    matricula_wide[
        [
            "matricula_inicial",
            "matricula_primaria",
            "matricula_secundaria"
        ]
    ]
    .isnull()
    .any(axis=1)
]

if filas_matricula_faltante.empty:

    print(
        "No existen filas con matrícula faltante."
    )

else:

    print(
        filas_matricula_faltante.to_string(
            index=False
        )
    )


# 6.6 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)

control_gp_matricula = matricula_wide[
    matricula_wide["partido"]
    == "GENERAL PUEYRREDON"
]

print(
    control_gp_matricula.to_string(
        index=False
    )
)


# 6.7 PRIMERAS FILAS

print("\nPRIMERAS 20 FILAS:")

print(
    matricula_wide
    .head(20)
    .to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("PREPARACIÓN DE MATRÍCULA FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NI SE CREÓ EL DATASET MAESTRO")
print("=" * 70)

# 7. PREPARACIÓN DE EDUCACIÓN CENSO 2022
# GRANULARIDAD: PARTIDO

print("\n" + "=" * 70)
print("PREPARACIÓN DE EDUCACIÓN CENSO 2022")
print("GRANULARIDAD: PARTIDO")
print("=" * 70)


# 7.1 AGREGAR A NIVEL PARTIDO

# El archivo original tiene una fila por partido y edad.
# Para el dataset maestro necesitamos una sola fila por partido.
# Se suman únicamente variables que representan cantidades.

columnas_suma_educacion = [
    "poblacion",
    "asiste",
    "no_asiste_pero_asistio",
    "nunca_asistio",
    "jardin_0_3",
    "sala_4_5",
    "primario",
    "secundario",
    "terciario",
    "universitario",
    "posgrado"
]

educacion_partido = (
    educacion
    .groupby("partido", as_index=False)[columnas_suma_educacion]
    .sum(min_count=1)
)


# 7.2 CALCULAR INDICADORES

educacion_partido["tasa_asistencia_censo_2022"] = (
    educacion_partido["asiste"]
    / educacion_partido["poblacion"]
    * 100
).round(2)

educacion_partido["porcentaje_nunca_asistio_censo_2022"] = (
    educacion_partido["nunca_asistio"]
    / educacion_partido["poblacion"]
    * 100
).round(2)


# 7.3 AGREGAR AÑO

educacion_partido["anio"] = 2022


# 7.4 RENOMBRAR Y ORDENAR COLUMNAS

educacion_partido = educacion_partido.rename(
    columns={
        "poblacion": "poblacion_educacion_censo",
        "asiste": "asiste_censo_2022",
        "no_asiste_pero_asistio": "no_asiste_pero_asistio_censo_2022",
        "nunca_asistio": "nunca_asistio_censo_2022",
        "jardin_0_3": "asiste_jardin_0_3_censo_2022",
        "sala_4_5": "asiste_sala_4_5_censo_2022",
        "primario": "asiste_primario_censo_2022",
        "secundario": "asiste_secundario_censo_2022",
        "terciario": "asiste_terciario_censo_2022",
        "universitario": "asiste_universitario_censo_2022",
        "posgrado": "asiste_posgrado_censo_2022"
    }
)

educacion_partido = educacion_partido[
    [
        "partido",
        "anio",
        "poblacion_educacion_censo",
        "asiste_censo_2022",
        "no_asiste_pero_asistio_censo_2022",
        "nunca_asistio_censo_2022",
        "tasa_asistencia_censo_2022",
        "porcentaje_nunca_asistio_censo_2022",
        "asiste_jardin_0_3_censo_2022",
        "asiste_sala_4_5_censo_2022",
        "asiste_primario_censo_2022",
        "asiste_secundario_censo_2022",
        "asiste_terciario_censo_2022",
        "asiste_universitario_censo_2022",
        "asiste_posgrado_censo_2022"
    ]
]


# 7.5 VALIDACIÓN

print("\nDIMENSIONES:")
print(educacion_partido.shape)

print("\nCANTIDAD DE PARTIDOS:")
print(
    educacion_partido["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        educacion_partido["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    educacion_partido.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    educacion_partido.isnull().sum()
)


# 7.6 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN - EDUCACIÓN")
print("=" * 70)

control_gp_educacion = educacion_partido[
    educacion_partido["partido"]
    == "GENERAL PUEYRREDON"
]

print(
    control_gp_educacion.to_string(
        index=False
    )
)


# 7.7 PRIMERAS FILAS

print("\nPRIMERAS 15 FILAS:")

print(
    educacion_partido
    .head(15)
    .to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("PREPARACIÓN DE EDUCACIÓN FINALIZADA")
print("TODAVÍA NO SE REALIZÓ EL DATASET MAESTRO")
print("=" * 70)

# 8. PREPARACIÓN DE FECUNDIDAD CENSO 2022
# GRANULARIDAD: PARTIDO

print("\n" + "=" * 70)
print("PREPARACIÓN DE FECUNDIDAD CENSO 2022")
print("GRANULARIDAD: PARTIDO")
print("=" * 70)


# 8.1 CARGAR FEC_01

fecundidad = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "fecundidad_fec01_limpio.csv"
    )
)

# 8.2 NORMALIZAR NOMBRES DE PARTIDOS

import unicodedata


def normalizar_partido(nombre):

    if pd.isna(nombre):
        return nombre

    nombre = str(nombre).strip().upper()

    # Eliminar tildes
    nombre = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", nombre)
        if unicodedata.category(caracter) != "Mn"
    )

    # Eliminar espacios duplicados
    nombre = " ".join(nombre.split())

    return nombre


fecundidad["partido"] = (
    fecundidad["partido"]
    .apply(normalizar_partido)
)

# 8.3 SELECCIONAR VARIABLES ÚTILES

# FEC_01 ya tiene una sola fila por partido.
# Eliminamos las columnas utilizadas únicamente como controles
# durante la limpieza.

fecundidad_partido = fecundidad[
    [
        "partido",
        "mujeres_14_49",
        "sin_hijos",
        "con_1_hijo",
        "con_2_hijos",
        "con_3_hijos",
        "con_4_hijos",
        "con_5_mas_hijos",
        "promedio_hijos_por_mujer"
    ]
].copy()


# 8.4 AGREGAR AÑO

fecundidad_partido["anio"] = 2022


# 8.5 RENOMBRAR COLUMNAS

# Se agrega el sufijo censo_2022 para distinguir claramente
# estas variables de otras fuentes que puedan incorporarse
# posteriormente.

fecundidad_partido = fecundidad_partido.rename(
    columns={
        "mujeres_14_49": "mujeres_14_49_censo_2022",
        "sin_hijos": "mujeres_sin_hijos_censo_2022",
        "con_1_hijo": "mujeres_con_1_hijo_censo_2022",
        "con_2_hijos": "mujeres_con_2_hijos_censo_2022",
        "con_3_hijos": "mujeres_con_3_hijos_censo_2022",
        "con_4_hijos": "mujeres_con_4_hijos_censo_2022",
        "con_5_mas_hijos": "mujeres_con_5_mas_hijos_censo_2022",
        "promedio_hijos_por_mujer": "promedio_hijos_por_mujer_censo_2022"
    }
)


# 8.6 ORDENAR COLUMNAS

fecundidad_partido = fecundidad_partido[
    [
        "partido",
        "anio",
        "mujeres_14_49_censo_2022",
        "mujeres_sin_hijos_censo_2022",
        "mujeres_con_1_hijo_censo_2022",
        "mujeres_con_2_hijos_censo_2022",
        "mujeres_con_3_hijos_censo_2022",
        "mujeres_con_4_hijos_censo_2022",
        "mujeres_con_5_mas_hijos_censo_2022",
        "promedio_hijos_por_mujer_censo_2022"
    ]
]


# 8.7 VALIDACIÓN

print("\nDIMENSIONES:")
print(
    fecundidad_partido.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    fecundidad_partido["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        fecundidad_partido["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    fecundidad_partido.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    fecundidad_partido.isnull().sum()
)


# 8.8 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN - FECUNDIDAD")
print("=" * 70)

control_gp_fecundidad = fecundidad_partido[
    fecundidad_partido["partido"]
    == "GENERAL PUEYRREDON"
]

print(
    control_gp_fecundidad.to_string(
        index=False
    )
)


# 8.9 PRIMERAS FILAS

print("\nPRIMERAS 15 FILAS:")

print(
    fecundidad_partido
    .head(15)
    .to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("PREPARACIÓN DE FECUNDIDAD FINALIZADA")
print("TODAVÍA NO SE REALIZÓ EL DATASET MAESTRO")
print("=" * 70)

# 9. PREPARACIÓN DE ECONOMÍA, HOGARES Y MIGRACIONES
# GRANULARIDAD: PARTIDO + AÑO

print("\n" + "=" * 70)
print("PREPARACIÓN DE ECONOMÍA, HOGARES Y MIGRACIONES")
print("GRANULARIDAD: PARTIDO + AÑO")
print("=" * 70)


# 9.1 CARGAR DATASETS

economia = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "economia_limpio.csv"
    )
)

hogares = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "hogares_limpio.csv"
    )
)

migraciones = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "migraciones_limpio.csv"
    )
)


# 9.2 NORMALIZAR NOMBRES DE PARTIDOS

# Utilizamos la misma función normalizar_partido()
# definida anteriormente para fecundidad.

economia["partido"] = (
    economia["partido"]
    .apply(normalizar_partido)
)

hogares["partido"] = (
    hogares["partido"]
    .apply(normalizar_partido)
)

# Corregir nombres de partidos inconsistentes en hogares
hogares["partido"] = hogares["partido"].replace(
    {
        "CORONEL DE MARINA L.ROSALES": "CORONEL DE MARINA LEONARDO ROSALES",
        "LEZANA": "LEZAMA"
    }
)

migraciones["partido"] = (
    migraciones["partido"]
    .apply(normalizar_partido)
)

# 9.3 VALIDAR ECONOMÍA

print("\n" + "=" * 70)
print("ECONOMÍA")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    economia.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    economia["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        economia["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    economia.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    economia.isnull().sum()
)


# 9.4 VALIDAR HOGARES

print("\n" + "=" * 70)
print("HOGARES")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    hogares.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    hogares["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        hogares["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    hogares.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    hogares.isnull().sum()
)


# 9.5 VALIDAR MIGRACIONES

print("\n" + "=" * 70)
print("MIGRACIONES")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    migraciones.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    migraciones["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        migraciones["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    migraciones.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    migraciones.isnull().sum()
)


# 9.6 COMPARAR PARTIDOS ENTRE LOS TRES DATASETS

partidos_economia = set(
    economia["partido"]
)

partidos_hogares = set(
    hogares["partido"]
)

partidos_migraciones = set(
    migraciones["partido"]
)


print("\n" + "=" * 70)
print("COMPARACIÓN DE PARTIDOS")
print("=" * 70)


print("\nPARTIDOS DE ECONOMÍA QUE NO ESTÁN EN HOGARES:")

diferencia = (
    partidos_economia
    - partidos_hogares
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(
        sorted(diferencia)
    )


print("\nPARTIDOS DE HOGARES QUE NO ESTÁN EN ECONOMÍA:")

diferencia = (
    partidos_hogares
    - partidos_economia
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(
        sorted(diferencia)
    )


print("\nPARTIDOS DE ECONOMÍA QUE NO ESTÁN EN MIGRACIONES:")

diferencia = (
    partidos_economia
    - partidos_migraciones
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(
        sorted(diferencia)
    )


print("\nPARTIDOS DE MIGRACIONES QUE NO ESTÁN EN ECONOMÍA:")

diferencia = (
    partidos_migraciones
    - partidos_economia
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(
        sorted(diferencia)
    )


# 9.7 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)


print("\nECONOMÍA:")

print(
    economia[
        economia["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


print("\nHOGARES:")

print(
    hogares[
        hogares["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


print("\nMIGRACIONES:")

print(
    migraciones[
        migraciones["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


# 9.8 VALIDACIÓN FINAL

print("\n" + "=" * 70)
print("RESUMEN DE PREPARACIÓN")
print("=" * 70)

print(
    f"""
ECONOMÍA:
Filas: {len(economia)}
Partidos: {economia["partido"].nunique()}
Duplicados partido-año: {economia.duplicated(subset=["partido", "anio"]).sum()}

HOGARES:
Filas: {len(hogares)}
Partidos: {hogares["partido"].nunique()}
Duplicados partido-año: {hogares.duplicated(subset=["partido", "anio"]).sum()}

MIGRACIONES:
Filas: {len(migraciones)}
Partidos: {migraciones["partido"].nunique()}
Duplicados partido-año: {migraciones.duplicated(subset=["partido", "anio"]).sum()}
"""
)


print("=" * 70)
print("PREPARACIÓN DE ECONOMÍA, HOGARES Y MIGRACIONES FINALIZADA")
print("TODAVÍA NO SE REALIZÓ EL DATASET MAESTRO")
print("=" * 70)

# 10. PREPARACIÓN DE NACIMIENTOS Y POBLACIÓN ESTIMADA
# GRANULARIDAD: PARTIDO + AÑO

print("\n" + "=" * 70)
print("PREPARACIÓN DE NACIMIENTOS Y POBLACIÓN ESTIMADA")
print("GRANULARIDAD: PARTIDO + AÑO")
print("=" * 70)


# 10.1 CARGAR DATASETS

nacimientos = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "nacimientos_limpios.csv"
    )
)

poblacion_estimaciones = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "poblacion_estimaciones_limpia.csv"
    )
)


# 10.2 NORMALIZAR NOMBRES DE PARTIDOS

nacimientos["partido"] = (
    nacimientos["partido"]
    .apply(normalizar_partido)
)

poblacion_estimaciones["partido"] = (
    poblacion_estimaciones["partido"]
    .apply(normalizar_partido)
)


# 10.3 VALIDAR NACIMIENTOS

print("\n" + "=" * 70)
print("NACIMIENTOS")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    nacimientos.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    nacimientos["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        nacimientos["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    nacimientos.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    nacimientos.isnull().sum()
)


# 10.4 VALIDAR POBLACIÓN ESTIMADA

print("\n" + "=" * 70)
print("POBLACIÓN ESTIMADA")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    poblacion_estimaciones.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_estimaciones["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        poblacion_estimaciones["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    poblacion_estimaciones.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    poblacion_estimaciones.isnull().sum()
)


# 10.5 COMPARAR PARTIDOS

partidos_nacimientos = set(
    nacimientos["partido"]
)

partidos_poblacion_estimada = set(
    poblacion_estimaciones["partido"]
)


print("\n" + "=" * 70)
print("COMPARACIÓN DE PARTIDOS")
print("=" * 70)


print(
    "\nPARTIDOS DE NACIMIENTOS "
    "QUE NO ESTÁN EN POBLACIÓN ESTIMADA:"
)

diferencia = (
    partidos_nacimientos
    - partidos_poblacion_estimada
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(
        sorted(diferencia)
    )


print(
    "\nPARTIDOS DE POBLACIÓN ESTIMADA "
    "QUE NO ESTÁN EN NACIMIENTOS:"
)

diferencia = (
    partidos_poblacion_estimada
    - partidos_nacimientos
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(
        sorted(diferencia)
    )


# 10.6 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)


print("\nNACIMIENTOS:")

print(
    nacimientos[
        nacimientos["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


print("\nPOBLACIÓN ESTIMADA:")

print(
    poblacion_estimaciones[
        poblacion_estimaciones["partido"]
        == "GENERAL PUEYRREDON"
    ].to_string(
        index=False
    )
)


# 10.7 RESUMEN DE PREPARACIÓN

print("\n" + "=" * 70)
print("RESUMEN DE PREPARACIÓN")
print("=" * 70)

print(
    f"""
NACIMIENTOS:
Filas: {len(nacimientos)}
Partidos: {nacimientos["partido"].nunique()}
Duplicados partido-año: {nacimientos.duplicated(subset=["partido", "anio"]).sum()}

POBLACIÓN ESTIMADA:
Filas: {len(poblacion_estimaciones)}
Partidos: {poblacion_estimaciones["partido"].nunique()}
Duplicados partido-año: {poblacion_estimaciones.duplicated(subset=["partido", "anio"]).sum()}
"""
)


print("=" * 70)
print("PREPARACIÓN DE NACIMIENTOS Y POBLACIÓN ESTIMADA FINALIZADA")
print("TODAVÍA NO SE REALIZÓ EL DATASET MAESTRO")
print("=" * 70)

# 11. PREPARACIÓN DE POBLACIÓN BASE
# GRANULARIDAD: PARTIDO

print("\n" + "=" * 70)
print("PREPARACIÓN DE POBLACIÓN BASE")
print("GRANULARIDAD: PARTIDO")
print("=" * 70)


# 11.1 CARGAR DATASET

poblacion_base = pd.read_csv(
    os.path.join(
        carpeta_datos_limpios,
        "poblacion_base_limpia.csv"
    )
)


# 11.2 NORMALIZAR NOMBRES DE PARTIDOS

# Utilizamos la misma función normalizar_partido()
# definida anteriormente.

poblacion_base["partido"] = (
    poblacion_base["partido"]
    .apply(normalizar_partido)
)


# 11.3 AGREGAR AÑO DE REFERENCIA

# Las principales variables de este dataset corresponden
# al Censo 2022.
# Las variables poblacion_2010 y variación se mantienen
# identificadas por su propio nombre.

poblacion_base["anio"] = 2022


# 11.4 ORDENAR COLUMNAS

poblacion_base = poblacion_base[
    [
        "partido",
        "anio",
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
]


# 11.5 VALIDACIÓN GENERAL

print("\nDIMENSIONES:")
print(
    poblacion_base.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    poblacion_base["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        poblacion_base["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    poblacion_base.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print("\nNULOS POR COLUMNA:")
print(
    poblacion_base.isnull().sum()
)


# 11.6 IDENTIFICAR FILAS CON VALORES FALTANTES

print("\nFILAS CON VALORES NULOS:")

filas_nulas_poblacion = poblacion_base[
    poblacion_base.isnull().any(axis=1)
]

if filas_nulas_poblacion.empty:

    print(
        "No existen filas con valores nulos."
    )

else:

    print(
        filas_nulas_poblacion.to_string(
            index=False
        )
    )


# 11.7 CONTROL LEZAMA

print("\n" + "=" * 70)
print("CONTROL LEZAMA")
print("=" * 70)

control_lezama = poblacion_base[
    poblacion_base["partido"]
    == "LEZAMA"
]

print(
    control_lezama.to_string(
        index=False
    )
)


# 11.8 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)

control_gp_poblacion = poblacion_base[
    poblacion_base["partido"]
    == "GENERAL PUEYRREDON"
]

print(
    control_gp_poblacion.to_string(
        index=False
    )
)


# 11.9 COMPARAR PARTIDOS CON DATASETS YA PREPARADOS

print("\n" + "=" * 70)
print("COMPARACIÓN DE PARTIDOS")
print("=" * 70)

partidos_poblacion_base = set(
    poblacion_base["partido"]
)

partidos_economia = set(
    economia["partido"]
)


print("\nPARTIDOS DE POBLACIÓN BASE QUE NO ESTÁN EN ECONOMÍA:")

diferencia = (
    partidos_poblacion_base
    - partidos_economia
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(sorted(diferencia))


print("\nPARTIDOS DE ECONOMÍA QUE NO ESTÁN EN POBLACIÓN BASE:")

diferencia = (
    partidos_economia
    - partidos_poblacion_base
)

if len(diferencia) == 0:
    print("Ninguno.")
else:
    print(sorted(diferencia))


# 11.10 PRIMERAS FILAS

print("\nPRIMERAS 15 FILAS:")

print(
    poblacion_base
    .head(15)
    .to_string(
        index=False
    )
)


# 11.11 RESUMEN FINAL

print("\n" + "=" * 70)
print("RESUMEN DE PREPARACIÓN")
print("=" * 70)

print(
    f"""
POBLACIÓN BASE:
Filas: {len(poblacion_base)}
Partidos: {poblacion_base["partido"].nunique()}
Duplicados partido-año: {poblacion_base.duplicated(subset=["partido", "anio"]).sum()}
Valores nulos: {poblacion_base.isnull().sum().sum()}
"""
)


print("=" * 70)
print("PREPARACIÓN DE POBLACIÓN BASE FINALIZADA")
print("TODAVÍA NO SE REALIZÓ EL DATASET MAESTRO")
print("=" * 70)

# 12. CONSTRUCCIÓN DE LA BASE TEMPORAL DEL DATASET MAESTRO
# GRANULARIDAD: PARTIDO + AÑO

print("\n" + "=" * 70)
print("CONSTRUCCIÓN DE LA BASE TEMPORAL DEL DATASET MAESTRO")
print("GRANULARIDAD: PARTIDO + AÑO")
print("=" * 70)


# 12.1 NORMALIZAR PARTIDOS EN DATASETS TEMPORALES

# Aplicamos la misma normalización territorial utilizada
# anteriormente para asegurar que los joins coincidan.

matricula_wide["partido"] = (
    matricula_wide["partido"]
    .apply(normalizar_partido)
)

nacimientos["partido"] = (
    nacimientos["partido"]
    .apply(normalizar_partido)
)

poblacion_estimaciones["partido"] = (
    poblacion_estimaciones["partido"]
    .apply(normalizar_partido)
)

educacion_partido["partido"] = (
    educacion_partido["partido"]
    .apply(normalizar_partido)
)

fecundidad_partido["partido"] = (
    fecundidad_partido["partido"]
    .apply(normalizar_partido)
)

poblacion_base["partido"] = (
    poblacion_base["partido"]
    .apply(normalizar_partido)
)


# 12.2 DEFINIR PARTIDOS Y AÑOS DEL DATASET MAESTRO

# Utilizamos los 135 partidos ya validados.
# El período maestro será 2012-2035 porque reúne:
#
# - Nacimientos: 2012-2022
# - Matrícula: 2012-2025
# - Población estimada: 2022-2035
#
# Los datos censales aparecerán únicamente en 2022.

partidos_maestro = sorted(
    economia["partido"]
    .dropna()
    .unique()
    .tolist()
)

anios_maestro = list(
    range(2012, 2036)
)


# 12.3 CREAR TODAS LAS COMBINACIONES PARTIDO + AÑO

indice_maestro = pd.MultiIndex.from_product(
    [
        partidos_maestro,
        anios_maestro
    ],
    names=[
        "partido",
        "anio"
    ]
)

dataset_maestro = (
    indice_maestro
    .to_frame(index=False)
)


print("\nBASE TEMPORAL CREADA")

print("\nDIMENSIONES:")
print(
    dataset_maestro.shape
)

print("\nCANTIDAD DE PARTIDOS:")
print(
    dataset_maestro["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        dataset_maestro["anio"]
        .unique()
        .tolist()
    )
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    dataset_maestro.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


# 12.4 INTEGRAR NACIMIENTOS

dataset_maestro = dataset_maestro.merge(
    nacimientos,
    on=["partido", "anio"],
    how="left"
)


print("\n" + "=" * 70)
print("MERGE 1 - NACIMIENTOS")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    dataset_maestro.shape
)

print("\nREGISTROS CON NACIMIENTOS:")
print(
    dataset_maestro["nacimientos"]
    .notna()
    .sum()
)


# 12.5 INTEGRAR MATRÍCULA

dataset_maestro = dataset_maestro.merge(
    matricula_wide,
    on=["partido", "anio"],
    how="left"
)


print("\n" + "=" * 70)
print("MERGE 2 - MATRÍCULA")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    dataset_maestro.shape
)

print("\nREGISTROS CON MATRÍCULA INICIAL:")
print(
    dataset_maestro["matricula_inicial"]
    .notna()
    .sum()
)

print("\nREGISTROS CON MATRÍCULA PRIMARIA:")
print(
    dataset_maestro["matricula_primaria"]
    .notna()
    .sum()
)

print("\nREGISTROS CON MATRÍCULA SECUNDARIA:")
print(
    dataset_maestro["matricula_secundaria"]
    .notna()
    .sum()
)

print("\nREGISTROS CON MATRÍCULA TOTAL:")
print(
    dataset_maestro["matricula_total"]
    .notna()
    .sum()
)


# 12.6 INTEGRAR POBLACIÓN ESTIMADA

dataset_maestro = dataset_maestro.merge(
    poblacion_estimaciones,
    on=["partido", "anio"],
    how="left"
)


print("\n" + "=" * 70)
print("MERGE 3 - POBLACIÓN ESTIMADA")
print("=" * 70)

print("\nDIMENSIONES:")
print(
    dataset_maestro.shape
)

print("\nREGISTROS CON POBLACIÓN ESTIMADA:")
print(
    dataset_maestro["poblacion_estimada"]
    .notna()
    .sum()
)


# 12.7 VALIDACIÓN DE LA BASE TEMPORAL

print("\n" + "=" * 70)
print("VALIDACIÓN DE LA BASE TEMPORAL")
print("=" * 70)


print("\nDIMENSIONES ACTUALES:")
print(
    dataset_maestro.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    dataset_maestro["partido"].nunique()
)


print("\nCANTIDAD DE AÑOS:")
print(
    dataset_maestro["anio"].nunique()
)


print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    dataset_maestro.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


print("\nFILAS ESPERADAS:")
print(
    len(partidos_maestro)
    * len(anios_maestro)
)


print("\nFILAS OBTENIDAS:")
print(
    len(dataset_maestro)
)


# 12.8 COBERTURA TEMPORAL DE VARIABLES

print("\n" + "=" * 70)
print("COBERTURA TEMPORAL")
print("=" * 70)


columnas_control = [
    "nacimientos",
    "matricula_total",
    "poblacion_estimada"
]


for columna in columnas_control:

    print(
        f"\nAÑOS CON DATOS DE {columna.upper()}:"
    )

    anios_con_datos = (
        dataset_maestro.loc[
            dataset_maestro[columna].notna(),
            "anio"
        ]
        .unique()
        .tolist()
    )

    print(
        sorted(anios_con_datos)
    )


# 12.9 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)


control_gp_maestro = dataset_maestro[
    dataset_maestro["partido"]
    == "GENERAL PUEYRREDON"
]


print(
    control_gp_maestro.to_string(
        index=False
    )
)


# 12.10 CONTROL AÑO 2022

print("\n" + "=" * 70)
print("CONTROL AÑO 2022")
print("=" * 70)


control_2022 = dataset_maestro[
    dataset_maestro["anio"]
    == 2022
]


print("\nFILAS EN 2022:")
print(
    len(control_2022)
)


print("\nPARTIDOS EN 2022:")
print(
    control_2022["partido"].nunique()
)


print("\nNULOS EN VARIABLES PRINCIPALES - 2022:")

print(
    control_2022[
        [
            "nacimientos",
            "matricula_inicial",
            "matricula_primaria",
            "matricula_secundaria",
            "matricula_total",
            "poblacion_estimada"
        ]
    ]
    .isnull()
    .sum()
)


# 12.11 RESUMEN

print("\n" + "=" * 70)
print("RESUMEN DE LA BASE TEMPORAL")
print("=" * 70)

print(
    f"""
Filas: {len(dataset_maestro)}
Partidos: {dataset_maestro["partido"].nunique()}
Años: {dataset_maestro["anio"].nunique()}
Período: {dataset_maestro["anio"].min()} - {dataset_maestro["anio"].max()}
Duplicados partido-año: {dataset_maestro.duplicated(subset=["partido", "anio"]).sum()}
"""
)


print("=" * 70)
print("BASE TEMPORAL DEL DATASET MAESTRO CREADA")
print("SE INTEGRARON NACIMIENTOS, MATRÍCULA Y POBLACIÓN ESTIMADA")
print("TODAVÍA NO SE GUARDÓ EL DATASET MAESTRO")
print("=" * 70)

# 13. INTEGRACIÓN DE VARIABLES CENSALES 2022
# GRANULARIDAD: PARTIDO + AÑO

print("\n" + "=" * 70)
print("INTEGRACIÓN DE VARIABLES CENSALES 2022")
print("GRANULARIDAD: PARTIDO + AÑO")
print("=" * 70)


# 13.1 INTEGRAR EDUCACIÓN

dataset_maestro = dataset_maestro.merge(
    educacion_partido,
    on=["partido", "anio"],
    how="left"
)

print("\nMERGE 4 - EDUCACIÓN CENSO 2022")
print("DIMENSIONES:", dataset_maestro.shape)

print(
    "REGISTROS CON EDUCACIÓN:",
    dataset_maestro["poblacion_educacion_censo"].notna().sum()
)


# 13.2 INTEGRAR FECUNDIDAD

dataset_maestro = dataset_maestro.merge(
    fecundidad_partido,
    on=["partido", "anio"],
    how="left"
)

print("\nMERGE 5 - FECUNDIDAD CENSO 2022")
print("DIMENSIONES:", dataset_maestro.shape)

print(
    "REGISTROS CON FECUNDIDAD:",
    dataset_maestro["mujeres_14_49_censo_2022"].notna().sum()
)


# 13.3 INTEGRAR ECONOMÍA

dataset_maestro = dataset_maestro.merge(
    economia,
    on=["partido", "anio"],
    how="left"
)

print("\nMERGE 6 - ECONOMÍA")
print("DIMENSIONES:", dataset_maestro.shape)

print(
    "REGISTROS CON ECONOMÍA:",
    dataset_maestro["poblacion_14_mas"].notna().sum()
)


# 13.4 INTEGRAR HOGARES

dataset_maestro = dataset_maestro.merge(
    hogares,
    on=["partido", "anio"],
    how="left"
)

print("\nMERGE 7 - HOGARES")
print("DIMENSIONES:", dataset_maestro.shape)

print(
    "REGISTROS CON HOGARES:",
    dataset_maestro["hogares_total"].notna().sum()
)


# 13.5 INTEGRAR MIGRACIONES

dataset_maestro = dataset_maestro.merge(
    migraciones,
    on=["partido", "anio"],
    how="left"
)

print("\nMERGE 8 - MIGRACIONES")
print("DIMENSIONES:", dataset_maestro.shape)

print(
    "REGISTROS CON MIGRACIONES:",
    dataset_maestro["poblacion_5_mas"].notna().sum()
)


# 13.6 INTEGRAR POBLACIÓN BASE

dataset_maestro = dataset_maestro.merge(
    poblacion_base,
    on=["partido", "anio"],
    how="left"
)

print("\nMERGE 9 - POBLACIÓN BASE")
print("DIMENSIONES:", dataset_maestro.shape)

print(
    "REGISTROS CON POBLACIÓN BASE:",
    dataset_maestro["poblacion_2022"].notna().sum()
)


# 13.7 VALIDACIÓN GENERAL

print("\n" + "=" * 70)
print("VALIDACIÓN DESPUÉS DE INTEGRAR VARIABLES CENSALES")
print("=" * 70)

print("\nDIMENSIONES:")
print(dataset_maestro.shape)

print("\nFILAS:")
print(len(dataset_maestro))

print("\nPARTIDOS:")
print(
    dataset_maestro["partido"].nunique()
)

print("\nAÑOS:")
print(
    dataset_maestro["anio"].nunique()
)

print("\nDUPLICADOS PARTIDO-AÑO:")
print(
    dataset_maestro.duplicated(
        subset=["partido", "anio"]
    ).sum()
)


# 13.8 CONTROL DE COBERTURA CENSAL EN 2022

control_2022_completo = dataset_maestro[
    dataset_maestro["anio"] == 2022
]

columnas_control_censo = [
    "poblacion_educacion_censo",
    "mujeres_14_49_censo_2022",
    "poblacion_14_mas",
    "hogares_total",
    "poblacion_5_mas",
    "poblacion_2022"
]

print("\n" + "=" * 70)
print("CONTROL DE COBERTURA CENSAL - AÑO 2022")
print("=" * 70)

print("\nFILAS EN 2022:")
print(
    len(control_2022_completo)
)

print("\nNULOS EN VARIABLES CENSALES PRINCIPALES:")

print(
    control_2022_completo[
        columnas_control_censo
    ]
    .isnull()
    .sum()
)


# 13.9 VERIFICAR QUE LOS DATOS CENSALES NO APAREZCAN EN OTROS AÑOS

print("\nREGISTROS CENSALES FUERA DE 2022:")

for columna in columnas_control_censo:

    cantidad = dataset_maestro.loc[
        dataset_maestro["anio"] != 2022,
        columna
    ].notna().sum()

    print(
        f"{columna}: {cantidad}"
    )


# 13.10 CONTROL GENERAL PUEYRREDÓN 2022

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN - 2022")
print("=" * 70)

control_gp_2022 = dataset_maestro[
    (dataset_maestro["partido"] == "GENERAL PUEYRREDON")
    & (dataset_maestro["anio"] == 2022)
]

print(
    control_gp_2022.to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("INTEGRACIÓN DE VARIABLES CENSALES FINALIZADA")
print("TODAVÍA NO SE GUARDÓ EL DATASET MAESTRO")
print("=" * 70)

# 14. VALIDACIÓN FINAL DEL DATASET MAESTRO

print("\n" + "=" * 70)
print("14. VALIDACIÓN FINAL DEL DATASET MAESTRO")
print("=" * 70)


# 14.1 DIMENSIONES GENERALES

print("\nDIMENSIONES:")
print(dataset_maestro.shape)

print("\nFILAS:")
print(len(dataset_maestro))

print("\nCOLUMNAS:")
print(len(dataset_maestro.columns))

print("\nPARTIDOS:")
print(dataset_maestro["partido"].nunique())

print("\nAÑOS:")
print(dataset_maestro["anio"].nunique())

print("\nPERÍODO:")
print(
    dataset_maestro["anio"].min(),
    "-",
    dataset_maestro["anio"].max()
)


# 14.2 DUPLICADOS

print("\n" + "=" * 70)
print("CONTROL DE DUPLICADOS")
print("=" * 70)

duplicados_maestro = dataset_maestro.duplicated(
    subset=["partido", "anio"]
).sum()

print("\nDUPLICADOS PARTIDO-AÑO:")
print(duplicados_maestro)


# 14.3 NULOS POR COLUMNA

print("\n" + "=" * 70)
print("VALORES NULOS POR COLUMNA")
print("=" * 70)

nulos_maestro = dataset_maestro.isnull().sum()

print(
    nulos_maestro.to_string()
)


# 14.4 COBERTURA TEMPORAL DE TODAS LAS VARIABLES

print("\n" + "=" * 70)
print("COBERTURA TEMPORAL POR VARIABLE")
print("=" * 70)

for columna in dataset_maestro.columns:

    if columna not in ["partido", "anio"]:

        anios_con_datos = sorted(
            dataset_maestro.loc[
                dataset_maestro[columna].notna(),
                "anio"
            ]
            .unique()
            .tolist()
        )

        print(
            f"\n{columna}:"
        )

        print(
            anios_con_datos
        )


# 14.5 CANTIDAD DE DATOS DISPONIBLES POR AÑO

print("\n" + "=" * 70)
print("CANTIDAD DE DATOS DISPONIBLES POR AÑO")
print("=" * 70)

columnas_variables = [
    columna
    for columna in dataset_maestro.columns
    if columna not in ["partido", "anio"]
]

cobertura_por_anio = (
    dataset_maestro
    .groupby("anio")[columnas_variables]
    .count()
)

print(
    cobertura_por_anio.to_string()
)


# 14.6 CONTROL DE PARTIDOS POR AÑO

print("\n" + "=" * 70)
print("CONTROL DE PARTIDOS POR AÑO")
print("=" * 70)

partidos_por_anio = (
    dataset_maestro
    .groupby("anio")["partido"]
    .nunique()
)

print(
    partidos_por_anio.to_string()
)


# 14.7 VERIFICAR AÑOS CON MENOS DE 135 PARTIDOS

print("\n" + "=" * 70)
print("AÑOS CON MENOS DE 135 PARTIDOS")
print("=" * 70)

anios_incompletos = partidos_por_anio[
    partidos_por_anio != 135
]

if anios_incompletos.empty:

    print(
        "Todos los años contienen los 135 partidos."
    )

else:

    print(
        anios_incompletos.to_string()
    )


# 14.8 CONTROL DE VARIABLES TEMPORALES PRINCIPALES

print("\n" + "=" * 70)
print("CONTROL DE VARIABLES TEMPORALES PRINCIPALES")
print("=" * 70)

variables_temporales = [
    "nacimientos",
    "tbn",
    "matricula_inicial",
    "matricula_primaria",
    "matricula_secundaria",
    "matricula_total",
    "poblacion_estimada"
]

for columna in variables_temporales:

    print(
        f"\n{columna.upper()}:"
    )

    print(
        "Registros con datos:",
        dataset_maestro[columna]
        .notna()
        .sum()
    )

    print(
        "Años:",
        sorted(
            dataset_maestro.loc[
                dataset_maestro[columna].notna(),
                "anio"
            ]
            .unique()
            .tolist()
        )
    )


# 14.9 CONTROL DE VARIABLES CENSALES

print("\n" + "=" * 70)
print("CONTROL DE VARIABLES CENSALES")
print("=" * 70)

variables_censales = [
    "poblacion_educacion_censo",
    "mujeres_14_49_censo_2022",
    "poblacion_14_mas",
    "hogares_total",
    "poblacion_5_mas",
    "poblacion_2022"
]

for columna in variables_censales:

    registros_2022 = dataset_maestro.loc[
        dataset_maestro["anio"] == 2022,
        columna
    ].notna().sum()

    registros_fuera_2022 = dataset_maestro.loc[
        dataset_maestro["anio"] != 2022,
        columna
    ].notna().sum()

    print(
        f"\n{columna}:"
    )

    print(
        "Registros en 2022:",
        registros_2022
    )

    print(
        "Registros fuera de 2022:",
        registros_fuera_2022
    )


# 14.10 CONTROL DE LEZAMA

print("\n" + "=" * 70)
print("CONTROL LEZAMA - 2022")
print("=" * 70)

control_lezama_maestro = dataset_maestro[
    (dataset_maestro["partido"] == "LEZAMA")
    & (dataset_maestro["anio"] == 2022)
]

print(
    control_lezama_maestro.to_string(
        index=False
    )
)


# 14.11 CONTROL GENERAL PUEYRREDÓN

print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")
print("=" * 70)

control_gp_final = dataset_maestro[
    dataset_maestro["partido"]
    == "GENERAL PUEYRREDON"
]

print(
    control_gp_final.to_string(
        index=False
    )
)


# 14.12 RESUMEN FINAL

print("\n" + "=" * 70)
print("RESUMEN FINAL DEL DATASET MAESTRO")
print("=" * 70)

print(
    f"""
Filas: {len(dataset_maestro)}
Columnas: {len(dataset_maestro.columns)}
Partidos: {dataset_maestro["partido"].nunique()}
Años: {dataset_maestro["anio"].nunique()}
Período: {dataset_maestro["anio"].min()} - {dataset_maestro["anio"].max()}
Duplicados partido-año: {dataset_maestro.duplicated(subset=["partido", "anio"]).sum()}
"""
)

# ============================================================
# TRATAMIENTO DEL FALTANTE CENSAL DE LEZAMA
# ============================================================

# Lezama no posee un valor comparable de población 2010
# dentro de esta fuente.
# Por lo tanto, poblacion_2010 se conserva como NaN.
#
# Como no existe una base 2010 comparable, también se mantienen
# como NaN:
# - variacion_absoluta
# - variacion_relativa
#
# No se realiza imputación para evitar introducir datos
# artificiales en variables censales.
# ============================================================
# CONTROL DE FALTANTES CENSALES 2022
# ============================================================

print("\n" + "=" * 70)
print("CONTROL DE FALTANTES CENSALES 2022")
print("=" * 70)

faltantes_censo = dataset_maestro[
    (dataset_maestro["anio"] == 2022) &
    (
        dataset_maestro["poblacion_2010"].isna() |
        dataset_maestro["poblacion_2022"].isna()
    )
][
    [
        "partido",
        "anio",
        "poblacion_2010",
        "poblacion_2022",
        "variacion_absoluta",
        "variacion_relativa"
    ]
]

print(faltantes_censo.to_string(index=False))


# ============================================================
# FIN DE LA VALIDACIÓN
# ============================================================

print("\n" + "=" * 70)
print("VALIDACIÓN FINALIZADA")
print("EL DATASET MAESTRO TODAVÍA NO FUE GUARDADO")
print("=" * 70)

# ============================================================
# 15. IDENTIFICACIÓN DE FALTANTES REALES DE MATRÍCULA
# ============================================================

print("\n" + "=" * 70)
print("15. IDENTIFICACIÓN DE FALTANTES REALES DE MATRÍCULA")
print("PERÍODO CON DATOS DE MATRÍCULA: 2012-2025")
print("=" * 70)


# 15.1 FILTRAR ÚNICAMENTE EL PERÍODO REAL DE MATRÍCULA

matricula_periodo = dataset_maestro[
    dataset_maestro["anio"].between(2012, 2025)
].copy()


# 15.2 IDENTIFICAR FILAS CON ALGÚN NIVEL FALTANTE

faltantes_matricula = matricula_periodo[
    matricula_periodo[
        [
            "matricula_inicial",
            "matricula_primaria",
            "matricula_secundaria"
        ]
    ]
    .isnull()
    .any(axis=1)
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "matricula_total"
    ]
].sort_values(
    ["partido", "anio"]
)


# 15.3 MOSTRAR LOS CASOS

print("\nFILAS CON ALGÚN NIVEL DE MATRÍCULA FALTANTE:")
print("-" * 70)

if faltantes_matricula.empty:

    print("No existen faltantes de matrícula entre 2012 y 2025.")

else:

    print(
        faltantes_matricula.to_string(
            index=False
        )
    )


# 15.4 CANTIDAD DE FALTANTES POR VARIABLE

print("\n" + "=" * 70)
print("CANTIDAD DE FALTANTES REALES POR VARIABLE")
print("=" * 70)

for columna in [
    "matricula_inicial",
    "matricula_primaria",
    "matricula_secundaria",
    "matricula_total"
]:

    cantidad = matricula_periodo[columna].isna().sum()

    print(
        f"{columna}: {cantidad}"
    )


# 15.5 CANTIDAD DE CASOS POR PARTIDO

print("\n" + "=" * 70)
print("FALTANTES POR PARTIDO")
print("=" * 70)

if faltantes_matricula.empty:

    print("Ninguno.")

else:

    faltantes_por_partido = (
        faltantes_matricula
        .groupby("partido")
        .size()
        .sort_values(ascending=False)
    )

    print(
        faltantes_por_partido.to_string()
    )


# 15.6 RESUMEN

print("\n" + "=" * 70)
print("RESUMEN DEL CONTROL")
print("=" * 70)

print(
    f"""
Período analizado: 2012-2025
Filas analizadas: {len(matricula_periodo)}
Filas con algún faltante de matrícula: {len(faltantes_matricula)}

Faltantes matrícula inicial: {matricula_periodo["matricula_inicial"].isna().sum()}
Faltantes matrícula primaria: {matricula_periodo["matricula_primaria"].isna().sum()}
Faltantes matrícula secundaria: {matricula_periodo["matricula_secundaria"].isna().sum()}
Faltantes matrícula total: {matricula_periodo["matricula_total"].isna().sum()}
"""
)

print("=" * 70)
print("CONTROL FINALIZADO")
print("NO SE REALIZÓ NINGUNA MODIFICACIÓN")
print("=" * 70)


# ============================================================
# 16. DIAGNÓSTICO DE FALTANTES DE MATRÍCULA SECUNDARIA
# ============================================================

print("\n" + "=" * 70)
print("16. DIAGNÓSTICO DE FALTANTES DE MATRÍCULA SECUNDARIA")
print("=" * 70)

# Revisamos las series completas de Castelli y Lezama
# para determinar cómo se comportan los faltantes de secundaria.
# Este punto es únicamente de diagnóstico.
# NO se modifica ni se imputa ningún dato.

control_castelli_lezama = dataset_maestro[
    dataset_maestro["partido"].isin(["CASTELLI", "LEZAMA"])
    & dataset_maestro["anio"].between(2012, 2025)
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "matricula_total"
    ]
].sort_values(
    ["partido", "anio"]
)


# 16.1 MOSTRAR SERIES COMPLETAS

print("\nSERIES COMPLETAS DE CASTELLI Y LEZAMA:")
print("-" * 70)

print(
    control_castelli_lezama.to_string(
        index=False
    )
)


# 16.2 IDENTIFICAR PRIMER Y ÚLTIMO AÑO CON SECUNDARIA

print("\n" + "=" * 70)
print("PRIMER Y ÚLTIMO AÑO CON MATRÍCULA SECUNDARIA")
print("=" * 70)

for partido in ["CASTELLI", "LEZAMA"]:

    serie = control_castelli_lezama[
        control_castelli_lezama["partido"] == partido
    ]

    anios_con_secundaria = serie.loc[
        serie["matricula_secundaria"].notna(),
        "anio"
    ].tolist()

    print(f"\n{partido}:")

    if anios_con_secundaria:

        print(
            "Primer año con secundaria:",
            min(anios_con_secundaria)
        )

        print(
            "Último año con secundaria:",
            max(anios_con_secundaria)
        )

        print(
            "Años con secundaria:",
            anios_con_secundaria
        )

    else:

        print(
            "No posee datos de matrícula secundaria "
            "en el período 2012-2025."
        )


# 16.3 FINALIZAR DIAGNÓSTICO

print("\n" + "=" * 70)
print("DIAGNÓSTICO FINALIZADO")
print("NO SE REALIZÓ NINGUNA IMPUTACIÓN")
print("=" * 70)

# ============================================================
# 17. INVESTIGACIÓN DEL ORIGEN DE LOS FALTANTES
# CASTELLI Y LEZAMA
# ============================================================

print("\n" + "=" * 70)
print("17. INVESTIGACIÓN DEL ORIGEN DE LOS FALTANTES")
print("CASTELLI Y LEZAMA")
print("=" * 70)

# Este punto vuelve al dataset limpio oficial de matrícula
# para revisar los registros originales disponibles.
#
# NO se modifica matricula_limpia.csv.
# NO se modifica dataset_maestro.
# NO se realiza ninguna imputación.


# ------------------------------------------------------------
# 17.1 CARGAR MATRÍCULA LIMPIA
# ------------------------------------------------------------

ruta_matricula_limpia = os.path.join(
    carpeta_datos_limpios,
    "matricula_limpia.csv"
)

matricula_revision = pd.read_csv(
    ruta_matricula_limpia
)

print("\nARCHIVO ANALIZADO:")
print(ruta_matricula_limpia)

print("\nDIMENSIONES:")
print(matricula_revision.shape)

print("\nCOLUMNAS:")
print(
    matricula_revision.columns.tolist()
)


# ------------------------------------------------------------
# 17.2 NORMALIZAR PARTIDOS
# ------------------------------------------------------------

matricula_revision["partido"] = (
    matricula_revision["partido"]
    .apply(normalizar_partido)
)


# ------------------------------------------------------------
# 17.3 EXTRAER CASTELLI Y LEZAMA
# ------------------------------------------------------------

revision_castelli_lezama = matricula_revision[
    matricula_revision["partido"].isin(
        ["CASTELLI", "LEZAMA"]
    )
    & matricula_revision["anio"].between(2012, 2025)
].copy()

revision_castelli_lezama = (
    revision_castelli_lezama
    .sort_values(
        ["partido", "anio", "nivel"]
    )
)


print("\n" + "=" * 70)
print("REGISTROS ORIGINALES EN MATRICULA_LIMPIA.CSV")
print("=" * 70)

print(
    revision_castelli_lezama.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 17.4 TABLA PARTIDO-AÑO-NIVEL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MATRÍCULA POR NIVEL")
print("=" * 70)

tabla_revision = (
    revision_castelli_lezama
    .pivot_table(
        index=["partido", "anio"],
        columns="nivel",
        values="matricula",
        aggfunc="sum"
    )
    .reset_index()
)

tabla_revision.columns.name = None

print(
    tabla_revision.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 17.5 CANTIDAD DE NIVELES DISPONIBLES POR AÑO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CANTIDAD DE NIVELES DISPONIBLES POR PARTIDO Y AÑO")
print("=" * 70)

niveles_por_anio = (
    revision_castelli_lezama
    .groupby(
        ["partido", "anio"]
    )["nivel"]
    .nunique()
    .reset_index(
        name="cantidad_niveles"
    )
)

print(
    niveles_por_anio.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 17.6 IDENTIFICAR AÑOS SIN SECUNDARIA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AÑOS SIN REGISTRO DE SECUNDARIA")
print("=" * 70)

for partido in ["CASTELLI", "LEZAMA"]:

    datos_partido = revision_castelli_lezama[
        revision_castelli_lezama["partido"]
        == partido
    ]

    anios_secundaria = set(
        datos_partido.loc[
            datos_partido["nivel"]
            .str.lower()
            .eq("secundaria"),
            "anio"
        ]
    )

    anios_esperados = set(
        range(2012, 2026)
    )

    anios_sin_secundaria = sorted(
        anios_esperados
        - anios_secundaria
    )

    print(f"\n{partido}:")
    print(
        "Años sin secundaria:",
        anios_sin_secundaria
    )


# ------------------------------------------------------------
# 17.7 COMPARAR DATASET LIMPIO CON DATASET MAESTRO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COMPARACIÓN CON EL DATASET MAESTRO")
print("=" * 70)

comparacion_maestro = dataset_maestro[
    dataset_maestro["partido"].isin(
        ["CASTELLI", "LEZAMA"]
    )
    & dataset_maestro["anio"].between(
        2012, 2025
    )
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "matricula_total"
    ]
].copy()

print(
    comparacion_maestro
    .sort_values(
        ["partido", "anio"]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 17.8 RESUMEN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DEL DIAGNÓSTICO")
print("=" * 70)

print(
    f"""
Registros revisados en matricula_limpia.csv:
{len(revision_castelli_lezama)}

Partidos analizados:
{revision_castelli_lezama["partido"].nunique()}

Período analizado:
2012-2025

Objetivo:
Determinar si los faltantes de matrícula secundaria de
Castelli y Lezama ya están presentes en matricula_limpia.csv
o si fueron generados durante la integración.

IMPORTANTE:
En este punto NO se realizó ninguna modificación ni imputación.
"""
)

print("=" * 70)
print("INVESTIGACIÓN FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 18. DIAGNÓSTICO DE COHERENCIA DE LOS FALTANTES DE MATRÍCULA
# CASTELLI Y LEZAMA
# ============================================================

print("\n" + "=" * 70)
print("18. DIAGNÓSTICO DE COHERENCIA DE LOS FALTANTES DE MATRÍCULA")
print("CASTELLI Y LEZAMA")
print("=" * 70)

# Objetivo:
# Analizar si los 12 faltantes de matrícula secundaria pueden
# considerarse faltantes aislados o si forman parte de cambios
# estructurales en las series de matrícula.
#
# Se revisan:
# - evolución anual de los tres niveles;
# - variaciones interanuales;
# - relación entre los niveles;
# - años con cambios especialmente grandes.
#
# IMPORTANTE:
# NO se modifica matricula_limpia.csv.
# NO se modifica dataset_maestro.
# NO se realiza ninguna imputación.


# ------------------------------------------------------------
# 18.1 EXTRAER SERIES DE CASTELLI Y LEZAMA
# ------------------------------------------------------------

series_diagnostico = dataset_maestro[
    dataset_maestro["partido"].isin(
        ["CASTELLI", "LEZAMA"]
    )
    & dataset_maestro["anio"].between(
        2012, 2025
    )
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "matricula_total"
    ]
].copy()

series_diagnostico = (
    series_diagnostico
    .sort_values(
        ["partido", "anio"]
    )
)


print("\n" + "=" * 70)
print("SERIES ORIGINALES")
print("=" * 70)

print(
    series_diagnostico.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 18.2 CALCULAR VARIACIONES INTERANUALES ABSOLUTAS
# ------------------------------------------------------------

columnas_matricula = [
    "matricula_inicial",
    "matricula_primaria",
    "matricula_secundaria"
]

for columna in columnas_matricula:

    series_diagnostico[
        f"variacion_{columna}"
    ] = (
        series_diagnostico
        .groupby("partido")[columna]
        .diff()
    )


print("\n" + "=" * 70)
print("VARIACIONES INTERANUALES ABSOLUTAS")
print("=" * 70)

columnas_variaciones = [
    "partido",
    "anio",
    "variacion_matricula_inicial",
    "variacion_matricula_primaria",
    "variacion_matricula_secundaria"
]

print(
    series_diagnostico[
        columnas_variaciones
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 18.3 CALCULAR VARIACIONES INTERANUALES PORCENTUALES
# ------------------------------------------------------------

for columna in columnas_matricula:

    series_diagnostico[
        f"variacion_pct_{columna}"
    ] = (
        series_diagnostico
        .groupby("partido")[columna]
        .pct_change(
            fill_method=None
        )
        * 100
    )


print("\n" + "=" * 70)
print("VARIACIONES INTERANUALES PORCENTUALES")
print("=" * 70)

columnas_porcentajes = [
    "partido",
    "anio",
    "variacion_pct_matricula_inicial",
    "variacion_pct_matricula_primaria",
    "variacion_pct_matricula_secundaria"
]

print(
    series_diagnostico[
        columnas_porcentajes
    ]
    .round(2)
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 18.4 IDENTIFICAR CAMBIOS INTERANUALES MUY GRANDES
# ------------------------------------------------------------

# Utilizamos únicamente como señal de diagnóstico un cambio
# superior al 100 % respecto del año anterior.
#
# Esto NO significa automáticamente que exista un error.
# Sirve para identificar años que requieren revisión.

print("\n" + "=" * 70)
print("CAMBIOS INTERANUALES SUPERIORES AL 100 %")
print("=" * 70)

columnas_pct = [
    "variacion_pct_matricula_inicial",
    "variacion_pct_matricula_primaria",
    "variacion_pct_matricula_secundaria"
]

cambios_grandes = series_diagnostico[
    series_diagnostico[
        columnas_pct
    ]
    .abs()
    .gt(100)
    .any(axis=1)
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "variacion_pct_matricula_inicial",
        "variacion_pct_matricula_primaria",
        "variacion_pct_matricula_secundaria"
    ]
]


if cambios_grandes.empty:

    print(
        "No se detectaron cambios superiores al 100 %."
    )

else:

    print(
        cambios_grandes
        .round(2)
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 18.5 IDENTIFICAR AÑOS CON SECUNDARIA FALTANTE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AÑOS CON MATRÍCULA SECUNDARIA FALTANTE")
print("=" * 70)

faltantes_secundaria_diagnostico = (
    series_diagnostico[
        series_diagnostico[
            "matricula_secundaria"
        ].isna()
    ][
        [
            "partido",
            "anio",
            "matricula_inicial",
            "matricula_primaria",
            "matricula_secundaria"
        ]
    ]
)


print(
    faltantes_secundaria_diagnostico
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 18.6 ANALIZAR AÑOS ANTERIOR Y POSTERIOR A CADA BLOQUE
# DE FALTANTES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CONTEXTO TEMPORAL DE LOS BLOQUES DE FALTANTES")
print("=" * 70)


# CASTELLI:
# faltantes de secundaria entre 2012 y 2016.
# Revisamos especialmente 2016 y 2017.

print("\nCASTELLI - TRANSICIÓN 2016 / 2017")
print("-" * 70)

castelli_transicion = series_diagnostico[
    (series_diagnostico["partido"] == "CASTELLI")
    & series_diagnostico["anio"].between(
        2015, 2018
    )
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "matricula_total"
    ]
]

print(
    castelli_transicion.to_string(
        index=False
    )
)


# LEZAMA:
# faltantes de secundaria entre 2015 y 2021.
# Revisamos los años inmediatamente anteriores y posteriores.

print("\nLEZAMA - TRANSICIONES 2014 / 2015 Y 2021 / 2022")
print("-" * 70)

lezama_transicion = series_diagnostico[
    (series_diagnostico["partido"] == "LEZAMA")
    & (
        series_diagnostico["anio"].between(
            2013, 2016
        )
        |
        series_diagnostico["anio"].between(
            2020, 2023
        )
    )
][
    [
        "partido",
        "anio",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria",
        "matricula_total"
    ]
]

print(
    lezama_transicion.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 18.7 COMPARAR ESCALA ENTRE NIVELES
# ------------------------------------------------------------

# Calculamos la relación entre secundaria y primaria únicamente
# cuando ambas variables tienen datos.
#
# El objetivo es observar si la escala de secundaria es
# razonablemente comparable con primaria en los años disponibles.

series_diagnostico[
    "ratio_secundaria_primaria"
] = (
    series_diagnostico[
        "matricula_secundaria"
    ]
    /
    series_diagnostico[
        "matricula_primaria"
    ]
)


print("\n" + "=" * 70)
print("RELACIÓN MATRÍCULA SECUNDARIA / PRIMARIA")
print("=" * 70)

print(
    series_diagnostico[
        [
            "partido",
            "anio",
            "matricula_primaria",
            "matricula_secundaria",
            "ratio_secundaria_primaria"
        ]
    ]
    .round(3)
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 18.8 RESUMEN AUTOMÁTICO POR PARTIDO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN POR PARTIDO")
print("=" * 70)

for partido in [
    "CASTELLI",
    "LEZAMA"
]:

    serie_partido = series_diagnostico[
        series_diagnostico["partido"]
        == partido
    ]

    faltantes = (
        serie_partido[
            "matricula_secundaria"
        ]
        .isna()
        .sum()
    )

    anios_faltantes = (
        serie_partido.loc[
            serie_partido[
                "matricula_secundaria"
            ].isna(),
            "anio"
        ]
        .tolist()
    )

    print(f"\n{partido}")

    print(
        "Cantidad de años analizados:",
        len(serie_partido)
    )

    print(
        "Faltantes de secundaria:",
        faltantes
    )

    print(
        "Años faltantes:",
        anios_faltantes
    )

    print(
        "Primer año con secundaria:",
        serie_partido.loc[
            serie_partido[
                "matricula_secundaria"
            ].notna(),
            "anio"
        ].min()
    )

    print(
        "Último año con secundaria:",
        serie_partido.loc[
            serie_partido[
                "matricula_secundaria"
            ].notna(),
            "anio"
        ].max()
    )


# ------------------------------------------------------------
# 18.9 CONCLUSIÓN DEL DIAGNÓSTICO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CONCLUSIÓN DEL DIAGNÓSTICO")
print("=" * 70)

print(
    """
Los faltantes de matrícula secundaria analizados no fueron
generados durante la integración del dataset maestro.

Los valores ya se encuentran como NaN en matricula_limpia.csv.

Además, los faltantes aparecen agrupados en bloques temporales:

- CASTELLI: 2012-2016
- LEZAMA: 2015-2021

Por este motivo, antes de realizar cualquier imputación es
necesario determinar si estos bloques responden a:

1. ausencia real de información en la fuente;
2. cambios de cobertura o metodología;
3. problemas en los datos originales;
4. cambios en la clasificación territorial o educativa.

Las variaciones interanuales calculadas en este diagnóstico
son únicamente señales de control y no demuestran por sí
mismas la existencia de errores.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
"""
)


print("=" * 70)
print("DIAGNÓSTICO DE COHERENCIA FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 19. INVESTIGACIÓN DE ANOMALÍAS EN LAS SERIES DE MATRÍCULA
# CASTELLI Y LEZAMA
# ============================================================

print("\n" + "=" * 70)
print("19. INVESTIGACIÓN DE ANOMALÍAS EN LAS SERIES DE MATRÍCULA")
print("CASTELLI Y LEZAMA")
print("=" * 70)

# Objetivo:
# Analizar con mayor detalle los períodos donde aparecen
# faltantes o cambios bruscos en las series de matrícula.
#
# CASTELLI:
# - faltantes de secundaria: 2012-2016
# - cambio muy grande entre 2016 y 2017
#
# LEZAMA:
# - comportamiento atípico en 2014
# - faltantes de secundaria: 2015-2021
# - reaparición de secundaria en 2022
#
# IMPORTANTE:
# Este punto es únicamente de investigación.
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.


# ------------------------------------------------------------
# 19.1 PREPARAR MATRÍCULA LIMPIA PARA EL ANÁLISIS
# ------------------------------------------------------------

matricula_investigacion = matricula_revision.copy()

matricula_investigacion["partido"] = (
    matricula_investigacion["partido"]
    .apply(normalizar_partido)
)

matricula_investigacion = matricula_investigacion[
    matricula_investigacion["anio"].between(2012, 2025)
].copy()


print("\nDIMENSIONES DE MATRÍCULA ANALIZADA:")
print(matricula_investigacion.shape)

print("\nPARTIDOS:")
print(
    matricula_investigacion["partido"].nunique()
)

print("\nAÑOS:")
print(
    sorted(
        matricula_investigacion["anio"]
        .unique()
        .tolist()
    )
)


# ------------------------------------------------------------
# 19.2 CREAR TABLA WIDE SIN CONVERTIR NaN EN CERO
# ------------------------------------------------------------

# Usamos pivot en lugar de pivot_table con sum para evitar
# que un NaN pueda mostrarse incorrectamente como 0.

matricula_investigacion_wide = (
    matricula_investigacion
    .pivot(
        index=["partido", "anio"],
        columns="nivel",
        values="matricula"
    )
    .reset_index()
)

matricula_investigacion_wide.columns.name = None


print("\n" + "=" * 70)
print("CONTROL DE NaN EN CASTELLI Y LEZAMA")
print("=" * 70)

print(
    matricula_investigacion_wide[
        matricula_investigacion_wide["partido"]
        .isin(["CASTELLI", "LEZAMA"])
    ]
    .sort_values(["partido", "anio"])
    .to_string(index=False)
)


# ------------------------------------------------------------
# 19.3 COMPARAR CASTELLI CON PARTIDOS CERCANOS EN ESCALA
# ------------------------------------------------------------

# Para saber si el salto de Castelli en 2017 es un fenómeno
# particular, buscamos partidos cuya matrícula primaria en
# 2016 estuviera relativamente cerca de la de Castelli.

print("\n" + "=" * 70)
print("CASTELLI - COMPARACIÓN DEL CAMBIO 2016 / 2017")
print("=" * 70)

comparacion_2016_2017 = (
    matricula_investigacion_wide[
        matricula_investigacion_wide["anio"]
        .isin([2016, 2017])
    ]
    .pivot(
        index="partido",
        columns="anio",
        values=[
            "Inicial",
            "Primaria",
            "Secundaria"
        ]
    )
)

comparacion_2016_2017.columns = [
    f"{nivel}_{anio}"
    for nivel, anio
    in comparacion_2016_2017.columns
]

comparacion_2016_2017 = (
    comparacion_2016_2017
    .reset_index()
)


# Valores de Castelli en 2016

castelli_2016 = matricula_investigacion_wide[
    (matricula_investigacion_wide["partido"] == "CASTELLI")
    & (matricula_investigacion_wide["anio"] == 2016)
]

if not castelli_2016.empty:

    primaria_castelli_2016 = (
        castelli_2016["Primaria"].iloc[0]
    )

    partidos_similares_castelli = (
        matricula_investigacion_wide[
            (matricula_investigacion_wide["anio"] == 2016)
            & (
                matricula_investigacion_wide["Primaria"]
                .between(
                    primaria_castelli_2016 * 0.5,
                    primaria_castelli_2016 * 1.5
                )
            )
        ]["partido"]
        .unique()
        .tolist()
    )

    comparacion_castelli = (
        comparacion_2016_2017[
            comparacion_2016_2017["partido"]
            .isin(partidos_similares_castelli)
        ]
    )

    print(
        comparacion_castelli
        .sort_values("partido")
        .to_string(index=False)
    )

else:

    print(
        "No se encontró Castelli 2016."
    )


# ------------------------------------------------------------
# 19.4 MEDIR CAMBIO 2016-2017 EN TODOS LOS PARTIDOS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CAMBIO DE MATRÍCULA PRIMARIA 2016 / 2017 - TODOS LOS PARTIDOS")
print("=" * 70)

cambio_primaria_16_17 = (
    matricula_investigacion_wide[
        matricula_investigacion_wide["anio"]
        .isin([2016, 2017])
    ]
    .pivot(
        index="partido",
        columns="anio",
        values="Primaria"
    )
    .reset_index()
)

if (
    2016 in cambio_primaria_16_17.columns
    and 2017 in cambio_primaria_16_17.columns
):

    cambio_primaria_16_17[
        "variacion_pct"
    ] = (
        (
            cambio_primaria_16_17[2017]
            - cambio_primaria_16_17[2016]
        )
        /
        cambio_primaria_16_17[2016]
        * 100
    )

    print(
        cambio_primaria_16_17[
            [
                "partido",
                2016,
                2017,
                "variacion_pct"
            ]
        ]
        .sort_values(
            "variacion_pct",
            ascending=False
        )
        .head(20)
        .round(2)
        .to_string(index=False)
    )


# ------------------------------------------------------------
# 19.5 POSICIÓN DE CASTELLI EN EL CAMBIO 2016-2017
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("POSICIÓN DE CASTELLI - CAMBIO PRIMARIA 2016 / 2017")
print("=" * 70)

control_castelli_cambio = (
    cambio_primaria_16_17[
        cambio_primaria_16_17["partido"]
        == "CASTELLI"
    ]
)

print(
    control_castelli_cambio
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 19.6 INVESTIGAR LEZAMA 2014
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LEZAMA - INVESTIGACIÓN DEL AÑO 2014")
print("=" * 70)

lezama_2012_2016 = (
    matricula_investigacion_wide[
        (matricula_investigacion_wide["partido"] == "LEZAMA")
        & matricula_investigacion_wide["anio"]
        .between(2012, 2016)
    ]
)

print(
    lezama_2012_2016
    .to_string(index=False)
)


# ------------------------------------------------------------
# 19.7 COMPARAR LEZAMA 2014 CON RESTO DE LOS AÑOS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LEZAMA - RELACIÓN 2014 CON AÑOS ADYACENTES")
print("=" * 70)

for nivel in [
    "Inicial",
    "Primaria",
    "Secundaria"
]:

    valor_2014 = lezama_2012_2016.loc[
        lezama_2012_2016["anio"] == 2014,
        nivel
    ]

    valor_2013 = lezama_2012_2016.loc[
        lezama_2012_2016["anio"] == 2013,
        nivel
    ]

    valor_2015 = lezama_2012_2016.loc[
        lezama_2012_2016["anio"] == 2015,
        nivel
    ]

    print(f"\n{nivel.upper()}:")

    if (
        not valor_2014.empty
        and not valor_2013.empty
        and not valor_2015.empty
    ):

        print(
            "2013:",
            valor_2013.iloc[0]
        )

        print(
            "2014:",
            valor_2014.iloc[0]
        )

        print(
            "2015:",
            valor_2015.iloc[0]
        )


# ------------------------------------------------------------
# 19.8 BUSCAR OTROS PARTIDOS CON CAMBIOS EXTREMOS EN 2014
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CAMBIOS EXTREMOS 2013 / 2014 - TODOS LOS PARTIDOS")
print("=" * 70)

cambio_2013_2014 = (
    matricula_investigacion_wide[
        matricula_investigacion_wide["anio"]
        .isin([2013, 2014])
    ]
    .pivot(
        index="partido",
        columns="anio",
        values=[
            "Inicial",
            "Primaria",
            "Secundaria"
        ]
    )
)

cambio_2013_2014.columns = [
    f"{nivel}_{anio}"
    for nivel, anio
    in cambio_2013_2014.columns
]

cambio_2013_2014 = (
    cambio_2013_2014
    .reset_index()
)


for nivel in [
    "Inicial",
    "Primaria",
    "Secundaria"
]:

    col_2013 = f"{nivel}_2013"
    col_2014 = f"{nivel}_2014"

    cambio_2013_2014[
        f"variacion_pct_{nivel}"
    ] = (
        (
            cambio_2013_2014[col_2014]
            - cambio_2013_2014[col_2013]
        )
        /
        cambio_2013_2014[col_2013]
        * 100
    )


columnas_cambio_2014 = [
    "partido",
    "Inicial_2013",
    "Inicial_2014",
    "variacion_pct_Inicial",
    "Primaria_2013",
    "Primaria_2014",
    "variacion_pct_Primaria",
    "Secundaria_2013",
    "Secundaria_2014",
    "variacion_pct_Secundaria"
]


print(
    cambio_2013_2014[
        columnas_cambio_2014
    ]
    .sort_values(
        "variacion_pct_Primaria",
        ascending=False
    )
    .head(20)
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 19.9 POSICIÓN ESPECÍFICA DE LEZAMA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("POSICIÓN DE LEZAMA - CAMBIO 2013 / 2014")
print("=" * 70)

print(
    cambio_2013_2014[
        cambio_2013_2014["partido"]
        == "LEZAMA"
    ][
        columnas_cambio_2014
    ]
    .round(2)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 19.10 ANALIZAR REAPARICIÓN DE SECUNDARIA EN LEZAMA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LEZAMA - REAPARICIÓN DE SECUNDARIA EN 2022")
print("=" * 70)

lezama_2019_2025 = (
    matricula_investigacion_wide[
        (matricula_investigacion_wide["partido"] == "LEZAMA")
        & matricula_investigacion_wide["anio"]
        .between(2019, 2025)
    ]
)

print(
    lezama_2019_2025
    .to_string(index=False)
)


# ------------------------------------------------------------
# 19.11 DETECTAR NaN DE SECUNDARIA EN TODO EL DATASET
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FALTANTES DE SECUNDARIA EN TODOS LOS PARTIDOS")
print("=" * 70)

faltantes_secundaria_global = (
    matricula_investigacion_wide[
        matricula_investigacion_wide[
            "Secundaria"
        ].isna()
    ][
        [
            "partido",
            "anio",
            "Inicial",
            "Primaria",
            "Secundaria"
        ]
    ]
    .sort_values(
        ["partido", "anio"]
    )
)

print(
    faltantes_secundaria_global
    .to_string(index=False)
)

print(
    "\nCantidad total:",
    len(faltantes_secundaria_global)
)


# ------------------------------------------------------------
# 19.12 RESUMEN DE FALTANTES DE SECUNDARIA POR PARTIDO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FALTANTES DE SECUNDARIA POR PARTIDO")
print("=" * 70)

resumen_faltantes_global = (
    faltantes_secundaria_global
    .groupby("partido")
    .agg(
        cantidad_faltantes=("anio", "count"),
        primer_anio=("anio", "min"),
        ultimo_anio=("anio", "max")
    )
    .sort_values(
        "cantidad_faltantes",
        ascending=False
    )
)

if resumen_faltantes_global.empty:

    print(
        "No existen faltantes de secundaria."
    )

else:

    print(
        resumen_faltantes_global
        .to_string()
    )


# ------------------------------------------------------------
# 19.13 CONCLUSIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DE LA INVESTIGACIÓN")
print("=" * 70)

print(
    """
Este análisis permite determinar si las anomalías observadas
en Castelli y Lezama son casos aislados o si existen cambios
similares en otros partidos.

Puntos principales revisados:

1. Castelli presenta un cambio muy grande entre 2016 y 2017.

2. Lezama presenta un comportamiento extremadamente atípico
   en 2014 respecto de 2013 y 2015.

3. Los faltantes de secundaria se analizan también contra
   todos los demás partidos para determinar si el fenómeno
   aparece únicamente en Castelli y Lezama.

4. Los NaN se conservan como NaN durante todo el análisis.
   No se interpretan automáticamente como matrícula igual a 0.

IMPORTANTE:
Los resultados de este punto todavía NO justifican una
imputación automática.

NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)

print("=" * 70)
print("INVESTIGACIÓN DE ANOMALÍAS FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 20. LOCALIZACIÓN DE LAS FUENTES ORIGINALES DE MATRÍCULA
# ============================================================

print("\n" + "=" * 70)
print("20. LOCALIZACIÓN DE LAS FUENTES ORIGINALES DE MATRÍCULA")
print("=" * 70)

# Objetivo:
# Localizar los archivos relacionados con matrícula que existen
# dentro de la carpeta general de datos de la tesis.
#
# Esto permitirá identificar qué archivos fueron utilizados
# antes de generar matricula_limpia.csv y, posteriormente,
# verificar directamente los valores de Castelli y Lezama.
#
# IMPORTANTE:
# Este punto es únicamente de exploración.
# NO se modifica ningún archivo.
# NO se modifica dataset_maestro.
# NO se realiza ninguna imputación.


# ------------------------------------------------------------
# 20.1 DEFINIR CARPETA GENERAL DE DATOS
# ------------------------------------------------------------

# carpeta_datos_limpios apunta actualmente a:
# .../datos tesis/datos_limpios
#
# Por lo tanto, subimos un nivel para revisar toda la carpeta
# "datos tesis".

carpeta_datos_tesis = os.path.dirname(
    carpeta_datos_limpios
)

print("\nCARPETA GENERAL ANALIZADA:")
print(carpeta_datos_tesis)


# ------------------------------------------------------------
# 20.2 BUSCAR ARCHIVOS RELACIONADOS CON MATRÍCULA
# ------------------------------------------------------------

archivos_matricula_encontrados = []

for raiz, carpetas, archivos in os.walk(
    carpeta_datos_tesis
):

    for archivo in archivos:

        nombre_minuscula = archivo.lower()

        if (
            "matricula" in nombre_minuscula
            or "matrícula" in nombre_minuscula
        ):

            ruta_completa = os.path.join(
                raiz,
                archivo
            )

            archivos_matricula_encontrados.append(
                ruta_completa
            )


# ------------------------------------------------------------
# 20.3 MOSTRAR ARCHIVOS ENCONTRADOS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ARCHIVOS RELACIONADOS CON MATRÍCULA")
print("=" * 70)

if not archivos_matricula_encontrados:

    print(
        "No se encontraron archivos cuyo nombre "
        "contenga 'matricula'."
    )

else:

    archivos_matricula_encontrados = sorted(
        archivos_matricula_encontrados
    )

    print(
        "\nCantidad encontrada:",
        len(archivos_matricula_encontrados)
    )

    for numero, ruta in enumerate(
        archivos_matricula_encontrados,
        start=1
    ):

        print(
            f"\n{numero}. {ruta}"
        )


# ------------------------------------------------------------
# 20.4 MOSTRAR TIPO Y TAMAÑO DE CADA ARCHIVO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INFORMACIÓN DE LOS ARCHIVOS")
print("=" * 70)

for numero, ruta in enumerate(
    archivos_matricula_encontrados,
    start=1
):

    nombre = os.path.basename(
        ruta
    )

    extension = os.path.splitext(
        nombre
    )[1].lower()

    tamanio_bytes = os.path.getsize(
        ruta
    )

    tamanio_kb = (
        tamanio_bytes / 1024
    )

    print(
        f"""
ARCHIVO {numero}
Nombre: {nombre}
Extensión: {extension}
Tamaño: {tamanio_kb:.2f} KB
Ruta: {ruta}
"""
    )


# ------------------------------------------------------------
# 20.5 IDENTIFICAR ARCHIVOS QUE NO SEAN MATRICULA_LIMPIA
# ------------------------------------------------------------

posibles_fuentes_originales = [
    ruta
    for ruta in archivos_matricula_encontrados
    if os.path.basename(ruta).lower()
    != "matricula_limpia.csv"
]


print("\n" + "=" * 70)
print("POSIBLES FUENTES ANTERIORES A MATRICULA_LIMPIA.CSV")
print("=" * 70)

if not posibles_fuentes_originales:

    print(
        "No se encontró otro archivo con 'matricula' "
        "en el nombre además de matricula_limpia.csv."
    )

else:

    print(
        "\nCantidad de posibles fuentes:",
        len(posibles_fuentes_originales)
    )

    for numero, ruta in enumerate(
        posibles_fuentes_originales,
        start=1
    ):

        print(
            f"\n{numero}. {ruta}"
        )


# ------------------------------------------------------------
# 20.6 BUSCAR TAMBIÉN ARCHIVOS EXCEL, CSV Y ODS
# EN CARPETAS CUYO NOMBRE HAGA REFERENCIA A EDUCACIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ARCHIVOS EN CARPETAS RELACIONADAS CON EDUCACIÓN")
print("=" * 70)

archivos_educacion = []

palabras_educacion = [
    "educacion",
    "educación",
    "escuela",
    "matricula",
    "matrícula"
]

extensiones_validas = [
    ".csv",
    ".xlsx",
    ".xls",
    ".ods"
]

for raiz, carpetas, archivos in os.walk(
    carpeta_datos_tesis
):

    raiz_minuscula = raiz.lower()

    carpeta_relacionada = any(
        palabra in raiz_minuscula
        for palabra in palabras_educacion
    )

    if carpeta_relacionada:

        for archivo in archivos:

            extension = os.path.splitext(
                archivo
            )[1].lower()

            if extension in extensiones_validas:

                archivos_educacion.append(
                    os.path.join(
                        raiz,
                        archivo
                    )
                )


archivos_educacion = sorted(
    set(archivos_educacion)
)

if not archivos_educacion:

    print(
        "No se encontraron archivos adicionales "
        "en carpetas relacionadas con educación."
    )

else:

    print(
        "\nCantidad encontrada:",
        len(archivos_educacion)
    )

    for numero, ruta in enumerate(
        archivos_educacion,
        start=1
    ):

        print(
            f"\n{numero}. {ruta}"
        )


# ------------------------------------------------------------
# 20.7 RESUMEN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DE LA BÚSQUEDA")
print("=" * 70)

print(
    f"""
Archivos con 'matricula' en el nombre:
{len(archivos_matricula_encontrados)}

Posibles fuentes anteriores a matricula_limpia.csv:
{len(posibles_fuentes_originales)}

Archivos encontrados en carpetas relacionadas con educación:
{len(archivos_educacion)}

Objetivo del próximo paso:
Identificar cuál de estos archivos contiene los datos originales
utilizados para construir matricula_limpia.csv y revisar allí:

- CASTELLI: 2012-2017
- LEZAMA: 2012-2022

IMPORTANTE:
En este punto NO se modificó ningún dato.
NO se realizó ninguna imputación.
NO se guardó ningún archivo.
"""
)

print("=" * 70)
print("LOCALIZACIÓN DE FUENTES FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 21. VERIFICACIÓN DIRECTA EN LAS FUENTES ANUALES DE MATRÍCULA
# CASTELLI Y LEZAMA
# ============================================================

print("\n" + "=" * 70)
print("21. VERIFICACIÓN DIRECTA EN LAS FUENTES ANUALES DE MATRÍCULA")
print("CASTELLI Y LEZAMA")
print("=" * 70)

# Objetivo:
# Revisar directamente los CSV anuales que constituyen las
# fuentes previas a matricula_limpia.csv para comprobar si las
# anomalías de Castelli y Lezama ya existen en los archivos fuente.
#
# Casos de interés:
# - CASTELLI: 2012-2017
# - LEZAMA: 2012-2022
#
# Este punto es únicamente de diagnóstico.
# NO se modifica ningún archivo.


# ------------------------------------------------------------
# 21.1 DEFINIR CARPETA DE FUENTES ANUALES
# ------------------------------------------------------------

carpeta_fuentes_matricula = os.path.join(
    carpeta_datos_tesis,
    "necesarios ",
    "educacion",
    "Matriculas 2011 - 2025"
)


# ------------------------------------------------------------
# 21.2 DEFINIR CASOS A REVISAR
# ------------------------------------------------------------

casos_revision = {
    "CASTELLI": range(2012, 2018),
    "LEZAMA": range(2012, 2023)
}


# ------------------------------------------------------------
# 21.3 REVISAR DIRECTAMENTE CADA ARCHIVO ANUAL
# ------------------------------------------------------------

for partido_objetivo, anios_objetivo in casos_revision.items():

    print("\n" + "=" * 70)
    print(f"FUENTE ORIGINAL - {partido_objetivo}")
    print("=" * 70)

    for anio_objetivo in anios_objetivo:

        ruta_fuente = os.path.join(
            carpeta_fuentes_matricula,
            f"{anio_objetivo} Matricula - agregada(in).csv"
        )

        print(f"\n{partido_objetivo} - {anio_objetivo}")
        print("-" * 70)

        print(
            "Archivo:",
            ruta_fuente
        )

        # ----------------------------------------------------
        # CONTROLAR QUE EL ARCHIVO EXISTA
        # ----------------------------------------------------

        if not os.path.exists(
            ruta_fuente
        ):

            print(
                "ARCHIVO NO ENCONTRADO"
            )

            continue


        # ----------------------------------------------------
        # CARGAR ARCHIVO
        # ----------------------------------------------------

        try:

            fuente_anual = pd.read_csv(
                ruta_fuente,
                low_memory=False
            )

        except UnicodeDecodeError:

            fuente_anual = pd.read_csv(
                ruta_fuente,
                encoding="latin1",
                low_memory=False
            )


        print(
            "Dimensiones:",
            fuente_anual.shape
        )

        print(
            "Columnas:",
            fuente_anual.columns.tolist()
        )


        # ----------------------------------------------------
        # BUSCAR COLUMNAS DONDE APARECE EL PARTIDO
        # ----------------------------------------------------

        columnas_con_partido = []

        for columna in fuente_anual.columns:

            serie_texto = (
                fuente_anual[columna]
                .astype(str)
                .str.upper()
                .str.strip()
            )

            if serie_texto.str.contains(
                partido_objetivo,
                regex=False,
                na=False
            ).any():

                columnas_con_partido.append(
                    columna
                )


        if not columnas_con_partido:

            print(
                "No se encontró ninguna columna que contenga "
                f"el texto {partido_objetivo}."
            )

            continue


        print(
            "Columnas donde aparece el partido:",
            columnas_con_partido
        )


        # ----------------------------------------------------
        # IDENTIFICAR TODAS LAS FILAS DEL PARTIDO
        # ----------------------------------------------------

        mascara_partido = pd.Series(
            False,
            index=fuente_anual.index
        )

        for columna in columnas_con_partido:

            mascara_partido = (
                mascara_partido
                |
                fuente_anual[columna]
                .astype(str)
                .str.upper()
                .str.strip()
                .str.contains(
                    partido_objetivo,
                    regex=False,
                    na=False
                )
            )


        filas_partido = fuente_anual[
            mascara_partido
        ].copy()


        print(
            "Cantidad de filas encontradas:",
            len(filas_partido)
        )


        # ----------------------------------------------------
        # MOSTRAR REGISTROS ORIGINALES
        # ----------------------------------------------------

        if filas_partido.empty:

            print(
                "No se encontraron registros."
            )

        else:

            print(
                filas_partido.to_string(
                    index=False
                )
            )


# ------------------------------------------------------------
# 21.4 RESUMEN DE LA VERIFICACIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DE LA VERIFICACIÓN DIRECTA")
print("=" * 70)

print(
    """
Se revisaron directamente los archivos anuales originales para
los períodos donde se detectaron anomalías en matricula_limpia.csv.

La salida anterior permite comprobar, sin modificar los datos:

- si Castelli ya presenta en las fuentes 2012-2016 una cobertura
  distinta de la observada desde 2017;

- si el salto de Castelli en 2017 ya está presente en la fuente;

- si los valores extraordinarios de Lezama en 2014 ya aparecen
  en el archivo anual original;

- si la ausencia de secundaria de Lezama entre 2015 y 2021 ya
  está presente en las fuentes;

- y si secundaria reaparece efectivamente en la fuente de 2022.

IMPORTANTE:
Todavía NO se realiza ninguna imputación ni corrección automática.

NO se modifica matricula_limpia.csv.
NO se modifica dataset_maestro.
NO se guarda ningún archivo.
"""
)

print("=" * 70)
print("VERIFICACIÓN DE FUENTES FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

import pandas as pd
import os

# ============================================================
# 22. AUDITORÍA ESTRUCTURADA DE MATRÍCULA
# CASTELLI Y LEZAMA
# ============================================================
print('22. AUDITORÍA ESTRUCTURADA DE MATRÍCULA')
print('CASTELLI Y LEZAMA')
carpeta = "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/necesarios /educacion/Matriculas 2011 - 2025"

partidos = ["CASTELLI", "LEZAMA"]
anios = range(2012, 2023)

resultados = []

for anio in anios:

    archivo = os.path.join(
        carpeta,
        f"{anio} Matricula - agregada(in).csv"
    )

    if not os.path.exists(archivo):
        print(f"⚠️ No se encontró el archivo de {anio}")
        continue

    # IMPORTANTE: los archivos están separados por ;
    # Algunos años no están codificados en UTF-8.
    # Primero intentamos UTF-8 y, si falla, usamos latin1.

    try:
        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

    except UnicodeDecodeError:
        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="latin1",
            low_memory=False
        )

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # Normalizar departamento para buscar correctamente
    df["departamento"] = (
        df["departamento"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    for partido in partidos:

        temp = df[df["departamento"] == partido].copy()

        if temp.empty:
            resultados.append({
                "anio": anio,
                "partido": partido,
                "filas": 0,
                "sector": None,
                "ambito": None
            })

        else:

            for _, fila in temp.iterrows():

                resultados.append({
                    "anio": anio,
                    "partido": partido,
                    "filas": len(temp),
                    "sector": fila.get("sector"),
                    "ambito": fila.get("ambito")
                })


# ============================================================
# RESULTADO
# ============================================================

auditoria = pd.DataFrame(resultados)

print("\n" + "=" * 70)
print("AUDITORÍA DE COBERTURA - CASTELLI Y LEZAMA")
print("=" * 70)

print(
    auditoria.to_string(index=False)
)

print("\n" + "=" * 70)
print("RESUMEN POR PARTIDO Y AÑO")
print("=" * 70)

resumen = (
    auditoria
    .groupby(["partido", "anio"], dropna=False)
    .agg(
        cantidad_filas=("filas", "max"),
        sectores=("sector", lambda x: " | ".join(
            sorted(set(str(v) for v in x if pd.notna(v)))
        )),
        ambitos=("ambito", lambda x: " | ".join(
            sorted(set(str(v) for v in x if pd.notna(v)))
        ))
    )
    .reset_index()
)

print(resumen.to_string(index=False))


# ============================================================
# CONTROL
# ============================================================

print("\n" + "=" * 70)
print("AUDITORÍA FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# 23. CUANTIFICACIÓN DEL CAMBIO DE COBERTURA DE MATRÍCULA
# CASTELLI Y LEZAMA
# ============================================================

print("\n" + "=" * 70)
print("23. CUANTIFICACIÓN DEL CAMBIO DE COBERTURA DE MATRÍCULA")
print("CASTELLI Y LEZAMA")
print("=" * 70)

# Objetivo:
# Comprobar si las anomalías observadas en las series de
# matrícula coinciden con la aparición o desaparición de
# registros urbanos en las fuentes originales.
#
# Casos principales:
#
# CASTELLI:
# 2016 -> solamente Rural
# 2017 -> Rural + Urbano
#
# LEZAMA:
# 2013 -> solamente Rural
# 2014 -> Rural + Urbano
# 2015 -> solamente Rural
#
# Se calculará la matrícula correspondiente a:
# - Inicial
# - Primaria
# - Secundaria
#
# separando Rural y Urbano.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.


# ------------------------------------------------------------
# 23.1 DEFINIR CASOS A ANALIZAR
# ------------------------------------------------------------

casos_cobertura = {
    "CASTELLI": [2016, 2017],
    "LEZAMA": [2013, 2014, 2015]
}

resultados_cobertura = []


# ------------------------------------------------------------
# 23.2 DEFINIR COLUMNAS POR NIVEL
# ------------------------------------------------------------

# Inicial:
# lactantes, deambulantes, sala de 2, 3, 4 y 5 años

columnas_inicial = [
    "lactantes",
    "deambulantes",
    "s2",
    "s3",
    "s4",
    "s5"
]

# Primaria:
# grados/años 1 a 6

columnas_primaria = [
    "_1",
    "_2",
    "_3",
    "_4",
    "_5",
    "_6"
]

# Secundaria:
# años 7 a 12 y agrupación 13/14

columnas_secundaria = [
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12",
    "_1314"
]


# ------------------------------------------------------------
# 23.3 LEER FUENTES ORIGINALES
# ------------------------------------------------------------

for partido, lista_anios in casos_cobertura.items():

    for anio in lista_anios:

        archivo = os.path.join(
            carpeta,
            f"{anio} Matricula - agregada(in).csv"
        )

        print("\n" + "-" * 70)
        print(f"{partido} - {anio}")
        print("-" * 70)

        if not os.path.exists(archivo):

            print("Archivo no encontrado.")
            continue

        # Algunos archivos utilizan UTF-8 y otros latin1.

        try:

            df = pd.read_csv(
                archivo,
                sep=";",
                encoding="utf-8",
                low_memory=False
            )

        except UnicodeDecodeError:

            df = pd.read_csv(
                archivo,
                sep=";",
                encoding="latin1",
                low_memory=False
            )

        df.columns = (
            df.columns
            .str.strip()
        )

        df["departamento"] = (
            df["departamento"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df["ambito"] = (
            df["ambito"]
            .astype(str)
            .str.strip()
            .str.upper()
        )


        # ----------------------------------------------------
        # 23.4 FILTRAR PARTIDO
        # ----------------------------------------------------

        temp = df[
            df["departamento"] == partido
        ].copy()

        if temp.empty:

            print(
                "No existen registros para este partido."
            )

            continue


        # ----------------------------------------------------
        # 23.5 CONVERTIR COLUMNAS DE MATRÍCULA A NUMÉRICAS
        # ----------------------------------------------------

        columnas_necesarias = (
            columnas_inicial
            + columnas_primaria
            + columnas_secundaria
        )

        for columna in columnas_necesarias:

            if columna in temp.columns:

                temp[columna] = pd.to_numeric(
                    temp[columna],
                    errors="coerce"
                )


        # ----------------------------------------------------
        # 23.6 CALCULAR MATRÍCULA POR NIVEL
        # ----------------------------------------------------

        columnas_inicial_existentes = [
            c for c in columnas_inicial
            if c in temp.columns
        ]

        columnas_primaria_existentes = [
            c for c in columnas_primaria
            if c in temp.columns
        ]

        columnas_secundaria_existentes = [
            c for c in columnas_secundaria
            if c in temp.columns
        ]

        temp["matricula_inicial_calculada"] = (
            temp[
                columnas_inicial_existentes
            ]
            .sum(
                axis=1,
                min_count=1
            )
        )

        temp["matricula_primaria_calculada"] = (
            temp[
                columnas_primaria_existentes
            ]
            .sum(
                axis=1,
                min_count=1
            )
        )

        temp["matricula_secundaria_calculada"] = (
            temp[
                columnas_secundaria_existentes
            ]
            .sum(
                axis=1,
                min_count=1
            )
        )


        # ----------------------------------------------------
        # 23.7 GUARDAR RESULTADOS POR ÁMBITO
        # ----------------------------------------------------

        for _, fila in temp.iterrows():

            resultados_cobertura.append({
                "partido": partido,
                "anio": anio,
                "ambito": fila["ambito"],
                "matricula_inicial":
                    fila["matricula_inicial_calculada"],
                "matricula_primaria":
                    fila["matricula_primaria_calculada"],
                "matricula_secundaria":
                    fila["matricula_secundaria_calculada"]
            })


# ------------------------------------------------------------
# 23.8 CREAR TABLA DE RESULTADOS
# ------------------------------------------------------------

cobertura_matricula = pd.DataFrame(
    resultados_cobertura
)

print("\n" + "=" * 70)
print("MATRÍCULA CALCULADA POR ÁMBITO")
print("=" * 70)

print(
    cobertura_matricula
    .sort_values(
        ["partido", "anio", "ambito"]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 23.9 CALCULAR TOTAL POR PARTIDO Y AÑO
# ------------------------------------------------------------
totales_cobertura = (
    cobertura_matricula
    .groupby(
        ["partido", "anio"],
        as_index=False
    )
    .agg(
        matricula_inicial_total=(
            "matricula_inicial",
            lambda x: x.sum(min_count=1)
        ),
        matricula_primaria_total=(
            "matricula_primaria",
            lambda x: x.sum(min_count=1)
        ),
        matricula_secundaria_total=(
            "matricula_secundaria",
            lambda x: x.sum(min_count=1)
        ),
        cantidad_ambitos=(
            "ambito",
            "nunique"
        )
    )
)


print("\n" + "=" * 70)
print("TOTALES SEGÚN COBERTURA DISPONIBLE")
print("=" * 70)

print(
    totales_cobertura
    .sort_values(
        ["partido", "anio"]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 23.10 MOSTRAR APORTE URBANO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("APORTE DE LOS REGISTROS URBANOS")
print("=" * 70)

registros_urbanos = (
    cobertura_matricula[
        cobertura_matricula["ambito"]
        == "URBANO"
    ]
)

if registros_urbanos.empty:

    print(
        "No se encontraron registros urbanos "
        "en los casos analizados."
    )

else:

    print(
        registros_urbanos
        .sort_values(
            ["partido", "anio"]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 23.11 CONCLUSIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CONCLUSIÓN DEL ANÁLISIS DE COBERTURA")
print("=" * 70)

print(
    """
Este análisis cuantifica por separado la matrícula Rural y
Urbana presente en las fuentes originales.

El objetivo es comprobar si los cambios extraordinarios
observados en las series temporales coinciden con cambios
en la cobertura territorial de los archivos fuente.

En particular:

- Castelli pasa de disponer solamente de registros rurales
  en 2016 a disponer de registros rurales y urbanos en 2017.

- Lezama dispone de registros rurales y urbanos en 2014,
  mientras que en 2013 y 2015 solamente aparecen registros
  rurales.

Por lo tanto, cualquier salto entre estos años debe analizarse
teniendo en cuenta el cambio de cobertura antes de interpretarlo
como un crecimiento o caída real de matrícula.

IMPORTANTE:
Este análisis todavía no determina cómo deben corregirse los
datos. Primero debe verificarse la consistencia de los valores
calculados con matricula_limpia.csv.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)

print("=" * 70)
print("ANÁLISIS DE COBERTURA FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 24. COMPARACIÓN ENTRE FUENTES ORIGINALES Y MATRICULA_LIMPIA
# ============================================================

print("\n" + "=" * 70)
print("24. COMPARACIÓN FUENTES ORIGINALES VS MATRICULA_LIMPIA")
print("=" * 70)

# Objetivo:
# Comparar los valores calculados directamente desde las fuentes
# originales con los valores presentes en matricula_limpia.csv.
#
# Esto permite determinar si las anomalías:
#
# 1. ya estaban presentes en las fuentes originales;
# 2. o fueron introducidas durante el proceso de limpieza.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.


# ------------------------------------------------------------
# 24.1 PREPARAR TOTALES DE LAS FUENTES ORIGINALES
# ------------------------------------------------------------

fuente_comparacion = (
    totales_cobertura[
        [
            "partido",
            "anio",
            "matricula_inicial_total",
            "matricula_primaria_total",
            "matricula_secundaria_total"
        ]
    ]
    .copy()
)

fuente_comparacion = fuente_comparacion.rename(
    columns={
        "matricula_inicial_total":
            "fuente_inicial",
        "matricula_primaria_total":
            "fuente_primaria",
        "matricula_secundaria_total":
            "fuente_secundaria"
    }
)


# ------------------------------------------------------------
# 24.2 PREPARAR MATRICULA_LIMPIA
# ------------------------------------------------------------

matricula_limpia_comparacion = (
    matricula_revision.copy()
)

matricula_limpia_comparacion["partido"] = (
    matricula_limpia_comparacion["partido"]
    .apply(normalizar_partido)
)

# Nos quedamos únicamente con los casos que acabamos
# de verificar directamente en las fuentes.

casos_comparacion = {
    "CASTELLI": [2016, 2017],
    "LEZAMA": [2013, 2014, 2015]
}

mascara_casos = pd.Series(
    False,
    index=matricula_limpia_comparacion.index
)

for partido, lista_anios in casos_comparacion.items():

    mascara_casos = (
        mascara_casos
        |
        (
            (
                matricula_limpia_comparacion["partido"]
                == partido
            )
            &
            (
                matricula_limpia_comparacion["anio"]
                .isin(lista_anios)
            )
        )
    )


matricula_casos = (
    matricula_limpia_comparacion[
        mascara_casos
    ]
    .copy()
)


print("\n" + "=" * 70)
print("REGISTROS EN MATRICULA_LIMPIA")
print("=" * 70)

print(
    matricula_casos
    .sort_values(
        ["partido", "anio", "nivel"]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 24.3 PASAR MATRICULA_LIMPIA A FORMATO WIDE
# ------------------------------------------------------------

# Utilizamos pivot y no sum para conservar correctamente
# los NaN.

matricula_casos_wide = (
    matricula_casos
    .pivot(
        index=["partido", "anio"],
        columns="nivel",
        values="matricula"
    )
    .reset_index()
)

matricula_casos_wide.columns.name = None


# ------------------------------------------------------------
# 24.4 NORMALIZAR NOMBRES DE LOS NIVELES
# ------------------------------------------------------------

renombrar_niveles = {}

if "Inicial" in matricula_casos_wide.columns:
    renombrar_niveles["Inicial"] = "limpia_inicial"

if "Primaria" in matricula_casos_wide.columns:
    renombrar_niveles["Primaria"] = "limpia_primaria"

if "Secundaria" in matricula_casos_wide.columns:
    renombrar_niveles["Secundaria"] = "limpia_secundaria"


matricula_casos_wide = (
    matricula_casos_wide.rename(
        columns=renombrar_niveles
    )
)


# ------------------------------------------------------------
# 24.5 UNIR FUENTES ORIGINALES Y MATRICULA_LIMPIA
# ------------------------------------------------------------

comparacion_fuente_limpia = (
    fuente_comparacion
    .merge(
        matricula_casos_wide,
        on=["partido", "anio"],
        how="outer"
    )
)


# ------------------------------------------------------------
# 24.6 FUNCIÓN PARA COMPARAR INCLUYENDO NaN
# ------------------------------------------------------------

def valores_iguales(a, b):

    # Dos NaN se consideran iguales para esta auditoría.
    if pd.isna(a) and pd.isna(b):
        return True

    # Si solamente uno es NaN, son diferentes.
    if pd.isna(a) or pd.isna(b):
        return False

    # Para valores numéricos usamos isclose.
    return bool(
        np.isclose(
            float(a),
            float(b)
        )
    )


# ------------------------------------------------------------
# 24.7 COMPARAR CADA NIVEL
# ------------------------------------------------------------

comparacion_fuente_limpia[
    "coincide_inicial"
] = comparacion_fuente_limpia.apply(
    lambda fila: valores_iguales(
        fila["fuente_inicial"],
        fila["limpia_inicial"]
    ),
    axis=1
)

comparacion_fuente_limpia[
    "coincide_primaria"
] = comparacion_fuente_limpia.apply(
    lambda fila: valores_iguales(
        fila["fuente_primaria"],
        fila["limpia_primaria"]
    ),
    axis=1
)

comparacion_fuente_limpia[
    "coincide_secundaria"
] = comparacion_fuente_limpia.apply(
    lambda fila: valores_iguales(
        fila["fuente_secundaria"],
        fila["limpia_secundaria"]
    ),
    axis=1
)


# ------------------------------------------------------------
# 24.8 RESULTADO GENERAL
# ------------------------------------------------------------

comparacion_fuente_limpia[
    "coincide_todo"
] = (
    comparacion_fuente_limpia[
        [
            "coincide_inicial",
            "coincide_primaria",
            "coincide_secundaria"
        ]
    ]
    .all(axis=1)
)


print("\n" + "=" * 70)
print("COMPARACIÓN DETALLADA")
print("=" * 70)

columnas_resultado = [
    "partido",
    "anio",
    "fuente_inicial",
    "limpia_inicial",
    "coincide_inicial",
    "fuente_primaria",
    "limpia_primaria",
    "coincide_primaria",
    "fuente_secundaria",
    "limpia_secundaria",
    "coincide_secundaria",
    "coincide_todo"
]

print(
    comparacion_fuente_limpia[
        columnas_resultado
    ]
    .sort_values(
        ["partido", "anio"]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 24.9 MOSTRAR ÚNICAMENTE DIFERENCIAS
# ------------------------------------------------------------

diferencias_fuente_limpia = (
    comparacion_fuente_limpia[
        ~comparacion_fuente_limpia[
            "coincide_todo"
        ]
    ]
)


print("\n" + "=" * 70)
print("DIFERENCIAS DETECTADAS")
print("=" * 70)

if diferencias_fuente_limpia.empty:

    print(
        "No se detectaron diferencias entre las fuentes "
        "originales y matricula_limpia.csv para los casos "
        "analizados."
    )

else:

    print(
        diferencias_fuente_limpia[
            columnas_resultado
        ]
        .sort_values(
            ["partido", "anio"]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 24.10 RESUMEN AUTOMÁTICO
# ------------------------------------------------------------

cantidad_casos = len(
    comparacion_fuente_limpia
)

cantidad_coincidentes = (
    comparacion_fuente_limpia[
        "coincide_todo"
    ]
    .sum()
)

cantidad_diferencias = (
    ~comparacion_fuente_limpia[
        "coincide_todo"
    ]
).sum()


print("\n" + "=" * 70)
print("RESUMEN DE LA COMPARACIÓN")
print("=" * 70)

print(
    f"""
Casos comparados:
{cantidad_casos}

Casos con coincidencia completa:
{cantidad_coincidentes}

Casos con alguna diferencia:
{cantidad_diferencias}
"""
)


# ------------------------------------------------------------
# 24.11 CONCLUSIÓN
# ------------------------------------------------------------

print("=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

if cantidad_diferencias == 0:

    print(
        """
Para todos los casos analizados, los valores de
matricula_limpia.csv coinciden con los valores calculados
directamente desde las fuentes originales.

Esto indica que las anomalías observadas no fueron introducidas
durante la limpieza de matrícula.

Los cambios detectados en Castelli y Lezama ya se encuentran
en las fuentes originales y están asociados a diferencias en
la cobertura Rural/Urbana entre años.

Por lo tanto, no corresponde corregir matricula_limpia.csv
asumiendo que existe un error del proceso de limpieza.
"""
    )

else:

    print(
        """
Se detectaron diferencias entre las fuentes originales y
matricula_limpia.csv.

Antes de tomar una decisión sobre los faltantes o cambios de
cobertura, será necesario identificar en qué nivel y año se
produce cada diferencia y revisar el proceso de limpieza.
"""
    )


print(
    """
IMPORTANTE:
NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)

print("=" * 70)
print("COMPARACIÓN FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 25. AUDITORÍA GLOBAL DE COBERTURA RURAL / URBANA
# ============================================================

print("\n" + "=" * 70)
print("25. AUDITORÍA GLOBAL DE COBERTURA RURAL / URBANA")
print("=" * 70)

# Objetivo:
# Analizar la cobertura territorial de las fuentes originales
# de matrícula para todos los partidos y años disponibles.
#
# Queremos determinar:
#
# 1. qué partidos tienen registros Rural y Urbano;
# 2. qué partidos tienen solamente Rural;
# 3. qué partidos tienen solamente Urbano;
# 4. qué partidos cambian de cobertura entre años;
# 5. si Castelli y Lezama son casos aislados o forman parte
#    de un problema más general de las fuentes.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 25.1 DEFINIR PERÍODO DE ANÁLISIS
# ------------------------------------------------------------

anios_auditoria_global = range(2012, 2026)

registros_cobertura_global = []

columnas_esperadas = {
    "provincia",
    "departamento",
    "sector",
    "ambito"
}


# ------------------------------------------------------------
# 25.2 LEER TODAS LAS FUENTES ANUALES
# ------------------------------------------------------------

for anio in anios_auditoria_global:

    archivo = os.path.join(
        carpeta,
        f"{anio} Matricula - agregada(in).csv"
    )

    print(f"\nAnalizando año {anio}...")

    if not os.path.exists(archivo):

        print(
            f"⚠️ No se encontró el archivo correspondiente a {anio}."
        )

        continue


    # --------------------------------------------------------
    # PRIMER INTENTO:
    # separador ;, que utilizan los archivos históricos
    # --------------------------------------------------------

    try:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

    except UnicodeDecodeError:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="latin1",
            low_memory=False
        )


    # --------------------------------------------------------
    # CONTROLAR SI SE LEYERON CORRECTAMENTE LAS COLUMNAS
    # --------------------------------------------------------

    columnas_detectadas = {
        str(columna).strip().lower()
        for columna in df.columns
    }


    # Desde 2024 algunos archivos pueden tener una estructura
    # o separador diferente.
    #
    # Si no aparecen las columnas esperadas, dejamos que
    # pandas detecte automáticamente el separador.

    if not columnas_esperadas.issubset(
        columnas_detectadas
    ):

        print(
            f"⚠️ {anio}: estructura diferente detectada. "
            "Se intentará detectar automáticamente el separador."
        )

        try:

            df = pd.read_csv(
                archivo,
                sep=None,
                engine="python",
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            df = pd.read_csv(
                archivo,
                sep=None,
                engine="python",
                encoding="latin1"
            )


    # --------------------------------------------------------
    # 25.3 NORMALIZAR NOMBRES DE COLUMNAS
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # --------------------------------------------------------
    # CONTROLAR COLUMNAS OBLIGATORIAS
    # --------------------------------------------------------

    columnas_faltantes = (
        columnas_esperadas
        -
        set(df.columns)
    )

    if columnas_faltantes:

        print(
            f"⚠️ {anio}: no se pudieron identificar "
            f"las columnas {sorted(columnas_faltantes)}."
        )

        print(
            "Columnas disponibles:"
        )

        print(
            df.columns.tolist()
        )

        print(
            f"⚠️ El año {anio} será omitido de esta auditoría."
        )

        continue


    # --------------------------------------------------------
    # NORMALIZAR COLUMNAS PRINCIPALES
    # --------------------------------------------------------

    df["departamento"] = (
        df["departamento"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["ambito"] = (
        df["ambito"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["sector"] = (
        df["sector"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    # --------------------------------------------------------
    # 25.4 LIMITAR EL ANÁLISIS A BUENOS AIRES
    # --------------------------------------------------------

    df["provincia_normalizada"] = (
        df["provincia"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df_buenos_aires = df[
        df["provincia_normalizada"]
        == "BUENOS AIRES"
    ].copy()


    print(
        "Registros de Buenos Aires:",
        len(df_buenos_aires)
    )


    # --------------------------------------------------------
    # 25.5 RESUMIR COBERTURA POR PARTIDO
    # --------------------------------------------------------

    for partido, grupo in df_buenos_aires.groupby(
        "departamento"
    ):

        ambitos = sorted(
            set(
                valor
                for valor in grupo["ambito"]
                if valor not in [
                    "",
                    "NAN",
                    "NONE"
                ]
            )
        )

        sectores = sorted(
            set(
                valor
                for valor in grupo["sector"]
                if valor not in [
                    "",
                    "NAN",
                    "NONE"
                ]
            )
        )


        # ----------------------------------------------------
        # 25.6 CLASIFICAR COBERTURA
        # ----------------------------------------------------

        tiene_rural = (
            "RURAL" in ambitos
        )

        tiene_urbano = (
            "URBANO" in ambitos
        )

        if tiene_rural and tiene_urbano:

            tipo_cobertura = (
                "RURAL + URBANO"
            )

        elif tiene_rural:

            tipo_cobertura = (
                "SOLO RURAL"
            )

        elif tiene_urbano:

            tipo_cobertura = (
                "SOLO URBANO"
            )

        else:

            tipo_cobertura = (
                "OTRA / SIN CLASIFICAR"
            )


        registros_cobertura_global.append({

            "partido":
                partido,

            "anio":
                anio,

            "cantidad_filas":
                len(grupo),

            "cantidad_ambitos":
                len(ambitos),

            "ambitos":
                " | ".join(ambitos),

            "sectores":
                " | ".join(sectores),

            "tiene_rural":
                tiene_rural,

            "tiene_urbano":
                tiene_urbano,

            "tipo_cobertura":
                tipo_cobertura
        })


# ------------------------------------------------------------
# 25.7 CREAR DATAFRAME GLOBAL
# ------------------------------------------------------------

cobertura_global = pd.DataFrame(
    registros_cobertura_global
)


# Control por si no se pudo procesar ningún año.

if cobertura_global.empty:

    print("\n" + "=" * 70)
    print("NO SE GENERARON REGISTROS PARA LA AUDITORÍA")
    print("=" * 70)

    print(
        """
No fue posible construir la auditoría global.

Es necesario revisar la estructura de los archivos anuales
antes de continuar.
"""
    )

else:

    print("\n" + "=" * 70)
    print("DIMENSIONES DE LA AUDITORÍA")
    print("=" * 70)

    print(
        "Registros partido-año:",
        len(cobertura_global)
    )

    print(
        "Partidos diferentes:",
        cobertura_global[
            "partido"
        ].nunique()
    )

    print(
        "Años analizados:",
        cobertura_global[
            "anio"
        ].nunique()
    )


    # --------------------------------------------------------
    # 25.8 DISTRIBUCIÓN DE TIPOS DE COBERTURA
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DISTRIBUCIÓN DE COBERTURA")
    print("=" * 70)

    distribucion_cobertura = (
        cobertura_global[
            "tipo_cobertura"
        ]
        .value_counts()
    )

    print(
        distribucion_cobertura
        .to_string()
    )


    # --------------------------------------------------------
    # 25.9 DISTRIBUCIÓN DE COBERTURA POR AÑO
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("COBERTURA POR AÑO")
    print("=" * 70)

    cobertura_por_anio = (
        cobertura_global
        .groupby(
            [
                "anio",
                "tipo_cobertura"
            ]
        )
        .size()
        .unstack(
            fill_value=0
        )
    )

    print(
        cobertura_por_anio
        .to_string()
    )


    # --------------------------------------------------------
    # 25.10 DETECTAR CAMBIOS DE COBERTURA ENTRE AÑOS
    # --------------------------------------------------------

    cobertura_global = (
        cobertura_global
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


    cobertura_global[
        "cobertura_anterior"
    ] = (
        cobertura_global
        .groupby(
            "partido"
        )[
            "tipo_cobertura"
        ]
        .shift(1)
    )


    cobertura_global[
        "anio_anterior"
    ] = (
        cobertura_global
        .groupby(
            "partido"
        )[
            "anio"
        ]
        .shift(1)
    )


    # Solamente consideramos cambios entre años consecutivos.

    cobertura_global[
        "anios_consecutivos"
    ] = (
        cobertura_global[
            "anio"
        ]
        -
        cobertura_global[
            "anio_anterior"
        ]
        == 1
    )


    cobertura_global[
        "cambio_cobertura"
    ] = (
        cobertura_global[
            "cobertura_anterior"
        ].notna()
        &
        cobertura_global[
            "anios_consecutivos"
        ]
        &
        (
            cobertura_global[
                "tipo_cobertura"
            ]
            !=
            cobertura_global[
                "cobertura_anterior"
            ]
        )
    )


    cambios_cobertura = (
        cobertura_global[
            cobertura_global[
                "cambio_cobertura"
            ]
        ]
        .copy()
    )


    print("\n" + "=" * 70)
    print("CAMBIOS DE COBERTURA ENTRE AÑOS CONSECUTIVOS")
    print("=" * 70)

    if cambios_cobertura.empty:

        print(
            "No se detectaron cambios de cobertura."
        )

    else:

        print(
            cambios_cobertura[
                [
                    "partido",
                    "anio_anterior",
                    "anio",
                    "cobertura_anterior",
                    "tipo_cobertura"
                ]
            ]
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 25.11 CANTIDAD DE CAMBIOS POR PARTIDO
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PARTIDOS CON CAMBIOS DE COBERTURA")
    print("=" * 70)

    resumen_cambios_partido = (
        cambios_cobertura
        .groupby(
            "partido"
        )
        .size()
        .reset_index(
            name="cantidad_cambios"
        )
        .sort_values(
            "cantidad_cambios",
            ascending=False
        )
    )


    if resumen_cambios_partido.empty:

        print(
            "Ningún partido presenta cambios."
        )

    else:

        print(
            resumen_cambios_partido
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 25.12 RESUMEN GENERAL DE CAMBIOS
    # --------------------------------------------------------

    cantidad_partidos_cambios = (
        cambios_cobertura[
            "partido"
        ]
        .nunique()
    )

    cantidad_cambios_total = (
        len(
            cambios_cobertura
        )
    )

    cantidad_partidos_total = (
        cobertura_global[
            "partido"
        ]
        .nunique()
    )


    print("\n" + "=" * 70)
    print("RESUMEN GLOBAL DE CAMBIOS")
    print("=" * 70)

    print(
        "Partidos analizados:",
        cantidad_partidos_total
    )

    print(
        "Partidos con al menos un cambio de cobertura:",
        cantidad_partidos_cambios
    )

    print(
        "Cantidad total de cambios interanuales:",
        cantidad_cambios_total
    )


    if cantidad_partidos_total > 0:

        porcentaje_partidos_cambios = (
            cantidad_partidos_cambios
            /
            cantidad_partidos_total
            * 100
        )

        print(
            "Porcentaje de partidos con cambios:",
            round(
                porcentaje_partidos_cambios,
                2
            ),
            "%"
        )


    # --------------------------------------------------------
    # 25.13 CASTELLI Y LEZAMA EN EL CONTEXTO GLOBAL
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CASTELLI Y LEZAMA EN EL CONTEXTO GLOBAL")
    print("=" * 70)

    control_castelli_lezama_global = (
        cobertura_global[
            cobertura_global[
                "partido"
            ].isin(
                [
                    "CASTELLI",
                    "LEZAMA"
                ]
            )
        ][
            [
                "partido",
                "anio",
                "cantidad_filas",
                "ambitos",
                "tipo_cobertura",
                "cobertura_anterior",
                "cambio_cobertura"
            ]
        ]
    )

    print(
        control_castelli_lezama_global
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 25.14 COBERTURA TEMPORAL POR PARTIDO
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("COBERTURA TEMPORAL POR PARTIDO")
    print("=" * 70)

    resumen_anios_partido = (
        cobertura_global
        .groupby(
            "partido"
        )
        .agg(
            cantidad_anios=(
                "anio",
                "nunique"
            ),
            primer_anio=(
                "anio",
                "min"
            ),
            ultimo_anio=(
                "anio",
                "max"
            )
        )
        .reset_index()
    )


    # La cantidad esperada se calcula según los años
    # que efectivamente pudieron procesarse.

    anios_procesados = sorted(
        cobertura_global[
            "anio"
        ].unique()
    )

    cantidad_anios_esperados = (
        len(
            anios_procesados
        )
    )


    partidos_cobertura_incompleta = (
        resumen_anios_partido[
            resumen_anios_partido[
                "cantidad_anios"
            ]
            < cantidad_anios_esperados
        ]
    )


    print(
        "Años efectivamente procesados:",
        anios_procesados
    )

    print(
        "Cantidad de años procesados:",
        cantidad_anios_esperados
    )

    print(
        "Partidos con cobertura temporal incompleta:",
        len(
            partidos_cobertura_incompleta
        )
    )


    if not partidos_cobertura_incompleta.empty:

        print(
            partidos_cobertura_incompleta
            .sort_values(
                "cantidad_anios"
            )
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 25.15 CONCLUSIÓN AUTOMÁTICA
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CONCLUSIÓN DE LA AUDITORÍA GLOBAL")
    print("=" * 70)


    if cantidad_partidos_cambios == 0:

        print(
            """
No se detectaron cambios interanuales de cobertura Rural/Urbana
en los partidos analizados.

En este escenario, los casos observados previamente deberían
revisarse individualmente.
"""
        )

    elif cantidad_partidos_cambios <= 2:

        print(
            """
Los cambios de cobertura Rural/Urbana aparecen en una cantidad
muy reducida de partidos.

Esto sugiere que Castelli y/o Lezama podrían representar casos
particulares de cobertura en las fuentes originales.
"""
        )

    else:

        print(
            """
Los cambios de cobertura Rural/Urbana no se limitan únicamente
a Castelli y Lezama.

Existen otros partidos con cambios entre años, por lo que la
comparabilidad temporal de las fuentes de matrícula debe
evaluarse como una característica general del dataset y no
solamente como un problema de dos partidos particulares.
"""
        )


    print(
        """
IMPORTANTE:
La existencia de un cambio de cobertura no demuestra por sí sola
que exista un error en la fuente.

Este punto identifica cambios estructurales que deben ser
considerados antes de decidir cómo tratar las series de matrícula.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
    )


    print("=" * 70)
    print("AUDITORÍA GLOBAL FINALIZADA")
    print("NO SE MODIFICÓ NINGÚN DATASET")
    print("=" * 70)

# ============================================================
# 26. IMPACTO DE LOS CAMBIOS DE COBERTURA EN LA MATRÍCULA
# ============================================================

print("\n" + "=" * 70)
print("26. IMPACTO DE LOS CAMBIOS DE COBERTURA EN LA MATRÍCULA")
print("=" * 70)

# Objetivo:
# Cuantificar si los cambios de cobertura Rural/Urbana
# detectados en el punto 25 coinciden con cambios importantes
# en los valores de matrícula.
#
# Se analizarán únicamente los partidos que presentan cambios:
#
# - CASTELLI
# - CHASCOMUS
# - EZEIZA
# - LEZAMA
# - PUNTA INDIO
#
# Para cada transición se comparará:
#
# - matrícula del año anterior
# - matrícula del año del cambio
# - diferencia absoluta
# - variación porcentual
#
# para:
#
# - Inicial
# - Primaria
# - Secundaria
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 26.1 OBTENER LOS CAMBIOS DETECTADOS EN EL PUNTO 25
# ------------------------------------------------------------

transiciones_cobertura = (
    cambios_cobertura[
        [
            "partido",
            "anio_anterior",
            "anio",
            "cobertura_anterior",
            "tipo_cobertura"
        ]
    ]
    .copy()
)

transiciones_cobertura[
    "anio_anterior"
] = (
    transiciones_cobertura[
        "anio_anterior"
    ]
    .astype(int)
)

transiciones_cobertura[
    "anio"
] = (
    transiciones_cobertura[
        "anio"
    ]
    .astype(int)
)


print("\n" + "=" * 70)
print("TRANSICIONES A ANALIZAR")
print("=" * 70)

print(
    transiciones_cobertura
    .sort_values(
        ["partido", "anio"]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 26.2 PREPARAR MATRICULA_LIMPIA
# ------------------------------------------------------------

matricula_impacto = (
    matricula_revision.copy()
)

matricula_impacto[
    "partido"
] = (
    matricula_impacto[
        "partido"
    ]
    .apply(
        normalizar_partido
    )
)

matricula_impacto[
    "anio"
] = pd.to_numeric(
    matricula_impacto[
        "anio"
    ],
    errors="coerce"
)

matricula_impacto[
    "matricula"
] = pd.to_numeric(
    matricula_impacto[
        "matricula"
    ],
    errors="coerce"
)


# ------------------------------------------------------------
# 26.3 CONTROLAR DUPLICADOS PARTIDO-AÑO-NIVEL
# ------------------------------------------------------------

duplicados_impacto = (
    matricula_impacto
    .duplicated(
        subset=[
            "partido",
            "anio",
            "nivel"
        ],
        keep=False
    )
)

cantidad_duplicados_impacto = (
    duplicados_impacto.sum()
)

print("\n" + "=" * 70)
print("CONTROL DE DUPLICADOS")
print("=" * 70)

print(
    "Filas duplicadas partido-año-nivel:",
    cantidad_duplicados_impacto
)

if cantidad_duplicados_impacto > 0:

    print(
        matricula_impacto[
            duplicados_impacto
        ]
        .sort_values(
            [
                "partido",
                "anio",
                "nivel"
            ]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 26.4 PASAR MATRÍCULA A FORMATO WIDE
# ------------------------------------------------------------

matricula_impacto_wide = (
    matricula_impacto
    .pivot(
        index=[
            "partido",
            "anio"
        ],
        columns="nivel",
        values="matricula"
    )
    .reset_index()
)

matricula_impacto_wide.columns.name = None


# Normalizar nombres de niveles

renombrar_impacto = {}

if "Inicial" in matricula_impacto_wide.columns:
    renombrar_impacto[
        "Inicial"
    ] = "matricula_inicial"

if "Primaria" in matricula_impacto_wide.columns:
    renombrar_impacto[
        "Primaria"
    ] = "matricula_primaria"

if "Secundaria" in matricula_impacto_wide.columns:
    renombrar_impacto[
        "Secundaria"
    ] = "matricula_secundaria"


matricula_impacto_wide = (
    matricula_impacto_wide.rename(
        columns=renombrar_impacto
    )
)


# ------------------------------------------------------------
# 26.5 FUNCIÓN PARA CALCULAR VARIACIÓN
# ------------------------------------------------------------

def calcular_variacion(valor_anterior, valor_actual):

    # Si falta alguno de los dos valores,
    # no puede calcularse una variación válida.

    if (
        pd.isna(valor_anterior)
        or
        pd.isna(valor_actual)
    ):

        return (
            np.nan,
            np.nan
        )


    diferencia = (
        valor_actual
        -
        valor_anterior
    )


    # Evitar división por cero.

    if valor_anterior == 0:

        porcentaje = np.nan

    else:

        porcentaje = (
            diferencia
            /
            valor_anterior
            *
            100
        )


    return (
        diferencia,
        porcentaje
    )


# ------------------------------------------------------------
# 26.6 COMPARAR CADA TRANSICIÓN
# ------------------------------------------------------------

resultados_impacto = []

niveles_impacto = [
    "inicial",
    "primaria",
    "secundaria"
]


for _, cambio in transiciones_cobertura.iterrows():

    partido = cambio[
        "partido"
    ]

    anio_anterior = cambio[
        "anio_anterior"
    ]

    anio_actual = cambio[
        "anio"
    ]


    fila_anterior = (
        matricula_impacto_wide[
            (
                matricula_impacto_wide[
                    "partido"
                ]
                == partido
            )
            &
            (
                matricula_impacto_wide[
                    "anio"
                ]
                == anio_anterior
            )
        ]
    )


    fila_actual = (
        matricula_impacto_wide[
            (
                matricula_impacto_wide[
                    "partido"
                ]
                == partido
            )
            &
            (
                matricula_impacto_wide[
                    "anio"
                ]
                == anio_actual
            )
        ]
    )


    # Si falta alguno de los años completos,
    # dejamos constancia y continuamos.

    if (
        fila_anterior.empty
        or
        fila_actual.empty
    ):

        print(
            f"⚠️ No se pudo comparar "
            f"{partido}: "
            f"{anio_anterior} -> {anio_actual}"
        )

        continue


    resultado = {

        "partido":
            partido,

        "anio_anterior":
            anio_anterior,

        "anio_actual":
            anio_actual,

        "cobertura_anterior":
            cambio[
                "cobertura_anterior"
            ],

        "cobertura_actual":
            cambio[
                "tipo_cobertura"
            ]
    }


    for nivel in niveles_impacto:

        columna = (
            f"matricula_{nivel}"
        )


        valor_anterior = (
            fila_anterior[
                columna
            ]
            .iloc[0]
            if columna
            in fila_anterior.columns
            else np.nan
        )


        valor_actual = (
            fila_actual[
                columna
            ]
            .iloc[0]
            if columna
            in fila_actual.columns
            else np.nan
        )


        diferencia, porcentaje = (
            calcular_variacion(
                valor_anterior,
                valor_actual
            )
        )


        resultado[
            f"{nivel}_anterior"
        ] = valor_anterior

        resultado[
            f"{nivel}_actual"
        ] = valor_actual

        resultado[
            f"{nivel}_diferencia"
        ] = diferencia

        resultado[
            f"{nivel}_variacion_pct"
        ] = porcentaje


    resultados_impacto.append(
        resultado
    )


# ------------------------------------------------------------
# 26.7 CREAR TABLA DE IMPACTO
# ------------------------------------------------------------

impacto_cobertura = pd.DataFrame(
    resultados_impacto
)


print("\n" + "=" * 70)
print("IMPACTO DE LOS CAMBIOS DE COBERTURA")
print("=" * 70)


if impacto_cobertura.empty:

    print(
        "No fue posible calcular ninguna transición."
    )

else:

    print(
        impacto_cobertura
        .sort_values(
            [
                "partido",
                "anio_actual"
            ]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 26.8 MOSTRAR RESULTADO POR NIVEL
# ------------------------------------------------------------

if not impacto_cobertura.empty:

    for nivel in niveles_impacto:

        print("\n" + "=" * 70)
        print(
            f"IMPACTO EN {nivel.upper()}"
        )
        print("=" * 70)

        columnas_nivel = [

            "partido",
            "anio_anterior",
            "anio_actual",

            "cobertura_anterior",
            "cobertura_actual",

            f"{nivel}_anterior",
            f"{nivel}_actual",
            f"{nivel}_diferencia",
            f"{nivel}_variacion_pct"
        ]


        print(
            impacto_cobertura[
                columnas_nivel
            ]
            .sort_values(
                [
                    "partido",
                    "anio_actual"
                ]
            )
            .to_string(
                index=False
            )
        )


# ------------------------------------------------------------
# 26.9 IDENTIFICAR VARIACIONES EXTRAORDINARIAS
# ------------------------------------------------------------

# Este umbral NO implica que el dato sea incorrecto.
#
# Se utiliza únicamente como herramienta descriptiva para
# identificar transiciones que merecen una revisión especial.

umbral_variacion = 50


variaciones_extraordinarias = []


if not impacto_cobertura.empty:

    for _, fila in impacto_cobertura.iterrows():

        for nivel in niveles_impacto:

            porcentaje = fila[
                f"{nivel}_variacion_pct"
            ]


            if (
                pd.notna(porcentaje)
                and
                abs(porcentaje)
                >= umbral_variacion
            ):

                variaciones_extraordinarias.append({

                    "partido":
                        fila["partido"],

                    "anio_anterior":
                        fila["anio_anterior"],

                    "anio_actual":
                        fila["anio_actual"],

                    "cobertura_anterior":
                        fila[
                            "cobertura_anterior"
                        ],

                    "cobertura_actual":
                        fila[
                            "cobertura_actual"
                        ],

                    "nivel":
                        nivel.capitalize(),

                    "valor_anterior":
                        fila[
                            f"{nivel}_anterior"
                        ],

                    "valor_actual":
                        fila[
                            f"{nivel}_actual"
                        ],

                    "diferencia":
                        fila[
                            f"{nivel}_diferencia"
                        ],

                    "variacion_pct":
                        porcentaje
                })


variaciones_extraordinarias_df = (
    pd.DataFrame(
        variaciones_extraordinarias
    )
)


print("\n" + "=" * 70)
print(
    f"VARIACIONES >= {umbral_variacion}% "
    "EN AÑOS CON CAMBIO DE COBERTURA"
)
print("=" * 70)


if variaciones_extraordinarias_df.empty:

    print(
        "No se detectaron variaciones iguales o "
        f"superiores al {umbral_variacion}%."
    )

else:

    print(
        variaciones_extraordinarias_df
        .sort_values(
            [
                "partido",
                "anio_actual",
                "nivel"
            ]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 26.10 RESUMEN DE TRANSICIONES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DEL IMPACTO")
print("=" * 70)


cantidad_transiciones = (
    len(
        impacto_cobertura
    )
)


if variaciones_extraordinarias_df.empty:

    cantidad_transiciones_extraordinarias = 0

else:

    cantidad_transiciones_extraordinarias = (
        variaciones_extraordinarias_df[
            [
                "partido",
                "anio_anterior",
                "anio_actual"
            ]
        ]
        .drop_duplicates()
        .shape[0]
    )


print(
    "Transiciones de cobertura analizadas:",
    cantidad_transiciones
)

print(
    "Transiciones con al menos una variación >= "
    f"{umbral_variacion}%:",
    cantidad_transiciones_extraordinarias
)


# ------------------------------------------------------------
# 26.11 DETALLE DE LOS CASOS CON MAYOR IMPACTO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CASOS QUE REQUIEREN REVISIÓN ESPECIAL")
print("=" * 70)


if variaciones_extraordinarias_df.empty:

    print(
        "No se identificaron casos mediante "
        "el criterio descriptivo utilizado."
    )

else:

    casos_revision = (
        variaciones_extraordinarias_df[
            [
                "partido",
                "anio_anterior",
                "anio_actual",
                "cobertura_anterior",
                "cobertura_actual"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "partido",
                "anio_actual"
            ]
        )
    )

    print(
        casos_revision.to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 26.12 INTERPRETACIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

print(
    """
Este análisis compara los valores de matrícula antes y después
de cada cambio de cobertura Rural/Urbana detectado en las
fuentes originales.

Una variación elevada que coincide temporalmente con la
aparición o desaparición de un ámbito constituye evidencia de
que la serie puede no ser directamente comparable entre ambos
años.

Sin embargo, la coincidencia temporal no demuestra por sí sola
que toda la variación haya sido causada por el cambio de
cobertura.

El umbral del 50% utilizado en este punto es únicamente un
criterio descriptivo para priorizar casos de revisión. No se
utiliza para modificar ni clasificar automáticamente los datos
como erróneos.

Los resultados deberán utilizarse junto con la auditoría de las
fuentes originales antes de definir el tratamiento metodológico
final de matrícula.
"""
)


print(
    """
IMPORTANTE:
NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)


print("=" * 70)
print("ANÁLISIS DE IMPACTO FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 27. VERIFICACIÓN DEL EFECTO RURAL / URBANO EN PUNTA INDIO
# ============================================================

print("\n" + "=" * 70)
print("27. VERIFICACIÓN DEL EFECTO RURAL / URBANO EN PUNTA INDIO")
print("=" * 70)

# Objetivo:
#
# Analizar directamente las fuentes originales de Punta Indio
# en los años donde el punto 26 detectó cambios extraordinarios:
#
# 2014 -> Rural + Urbano
# 2015 -> Solo Rural
#
# 2021 -> Solo Rural
# 2022 -> Rural + Urbano
#
# Queremos comprobar:
#
# 1. cuánto aporta cada ámbito a la matrícula;
# 2. si el componente Rural se mantiene relativamente estable;
# 3. si los saltos observados se explican principalmente por
#    la aparición o desaparición del componente Urbano;
# 4. si los totales calculados desde las fuentes coinciden con
#    matricula_limpia.csv.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 27.1 DEFINIR CASO
# ------------------------------------------------------------

partido_punta_indio = "PUNTA INDIO"

anios_punta_indio = [
    2014,
    2015,
    2021,
    2022
]

resultados_punta_indio = []


# ------------------------------------------------------------
# 27.2 COLUMNAS DE MATRÍCULA POR NIVEL
# ------------------------------------------------------------

columnas_inicial_pi = [
    "lactantes",
    "deambulantes",
    "s2",
    "s3",
    "s4",
    "s5"
]

columnas_primaria_pi = [
    "_1",
    "_2",
    "_3",
    "_4",
    "_5",
    "_6"
]

columnas_secundaria_pi = [
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12",
    "_1314"
]


# ------------------------------------------------------------
# 27.3 LEER FUENTES ORIGINALES
# ------------------------------------------------------------

for anio in anios_punta_indio:

    archivo = os.path.join(
        carpeta,
        f"{anio} Matricula - agregada(in).csv"
    )

    print("\n" + "-" * 70)
    print(f"PUNTA INDIO - {anio}")
    print("-" * 70)

    if not os.path.exists(archivo):

        print(
            f"⚠️ No se encontró el archivo de {anio}."
        )

        continue


    # --------------------------------------------------------
    # LEER ARCHIVO
    # --------------------------------------------------------

    try:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

    except UnicodeDecodeError:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="latin1",
            low_memory=False
        )


    # --------------------------------------------------------
    # NORMALIZAR COLUMNAS
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # --------------------------------------------------------
    # CONTROL DE ESTRUCTURA
    # --------------------------------------------------------

    columnas_obligatorias_pi = {
        "departamento",
        "ambito"
    }

    faltantes_pi = (
        columnas_obligatorias_pi
        -
        set(df.columns)
    )

    if faltantes_pi:

        print(
            f"⚠️ Faltan columnas obligatorias: "
            f"{sorted(faltantes_pi)}"
        )

        print(
            "Columnas disponibles:"
        )

        print(
            df.columns.tolist()
        )

        continue


    # --------------------------------------------------------
    # NORMALIZAR PARTIDO Y ÁMBITO
    # --------------------------------------------------------

    df["departamento"] = (
        df["departamento"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["ambito"] = (
        df["ambito"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    # --------------------------------------------------------
    # 27.4 FILTRAR PUNTA INDIO
    # --------------------------------------------------------

    temp = df[
        df["departamento"]
        == partido_punta_indio
    ].copy()


    if temp.empty:

        print(
            "⚠️ No se encontraron registros "
            "para Punta Indio."
        )

        continue


    print(
        "Cantidad de registros encontrados:",
        len(temp)
    )

    print(
        "Ámbitos encontrados:",
        sorted(
            temp["ambito"]
            .dropna()
            .unique()
            .tolist()
        )
    )


    # --------------------------------------------------------
    # 27.5 CONVERTIR MATRÍCULA A NUMÉRICA
    # --------------------------------------------------------

    todas_columnas_pi = (
        columnas_inicial_pi
        +
        columnas_primaria_pi
        +
        columnas_secundaria_pi
    )

    for columna in todas_columnas_pi:

        if columna in temp.columns:

            temp[columna] = pd.to_numeric(
                temp[columna],
                errors="coerce"
            )


    # --------------------------------------------------------
    # 27.6 IDENTIFICAR COLUMNAS EXISTENTES
    # --------------------------------------------------------

    inicial_existentes_pi = [
        columna
        for columna in columnas_inicial_pi
        if columna in temp.columns
    ]

    primaria_existentes_pi = [
        columna
        for columna in columnas_primaria_pi
        if columna in temp.columns
    ]

    secundaria_existentes_pi = [
        columna
        for columna in columnas_secundaria_pi
        if columna in temp.columns
    ]


    # --------------------------------------------------------
    # 27.7 CALCULAR MATRÍCULA POR FILA / ÁMBITO
    # --------------------------------------------------------

    temp["matricula_inicial"] = (
        temp[
            inicial_existentes_pi
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )

    temp["matricula_primaria"] = (
        temp[
            primaria_existentes_pi
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )

    temp["matricula_secundaria"] = (
        temp[
            secundaria_existentes_pi
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )


    # --------------------------------------------------------
    # 27.8 GUARDAR RESULTADOS
    # --------------------------------------------------------

    for _, fila in temp.iterrows():

        resultados_punta_indio.append({

            "partido":
                partido_punta_indio,

            "anio":
                anio,

            "ambito":
                fila["ambito"],

            "matricula_inicial":
                fila["matricula_inicial"],

            "matricula_primaria":
                fila["matricula_primaria"],

            "matricula_secundaria":
                fila["matricula_secundaria"]
        })


# ------------------------------------------------------------
# 27.9 CREAR DATAFRAME
# ------------------------------------------------------------

punta_indio_ambito = pd.DataFrame(
    resultados_punta_indio
)


print("\n" + "=" * 70)
print("MATRÍCULA DE PUNTA INDIO POR ÁMBITO")
print("=" * 70)


if punta_indio_ambito.empty:

    print(
        "No fue posible calcular resultados."
    )

else:

    print(
        punta_indio_ambito
        .sort_values(
            [
                "anio",
                "ambito"
            ]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 27.10 CALCULAR TOTALES POR AÑO
# ------------------------------------------------------------

if not punta_indio_ambito.empty:

    punta_indio_totales = (
        punta_indio_ambito
        .groupby(
            "anio",
            as_index=False
        )
        .agg(

            matricula_inicial_fuente=(
                "matricula_inicial",
                lambda x: x.sum(
                    min_count=1
                )
            ),

            matricula_primaria_fuente=(
                "matricula_primaria",
                lambda x: x.sum(
                    min_count=1
                )
            ),

            matricula_secundaria_fuente=(
                "matricula_secundaria",
                lambda x: x.sum(
                    min_count=1
                )
            ),

            cantidad_ambitos=(
                "ambito",
                "nunique"
            )
        )
    )


    print("\n" + "=" * 70)
    print("TOTALES CALCULADOS DESDE LAS FUENTES")
    print("=" * 70)

    print(
        punta_indio_totales
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 27.11 EXTRAER COMPONENTE RURAL
# ------------------------------------------------------------

if not punta_indio_ambito.empty:

    punta_indio_rural = (
        punta_indio_ambito[
            punta_indio_ambito[
                "ambito"
            ]
            == "RURAL"
        ]
        .copy()
    )


    print("\n" + "=" * 70)
    print("COMPONENTE RURAL")
    print("=" * 70)

    print(
        punta_indio_rural[
            [
                "anio",
                "matricula_inicial",
                "matricula_primaria",
                "matricula_secundaria"
            ]
        ]
        .sort_values(
            "anio"
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 27.12 EXTRAER COMPONENTE URBANO
# ------------------------------------------------------------

if not punta_indio_ambito.empty:

    punta_indio_urbano = (
        punta_indio_ambito[
            punta_indio_ambito[
                "ambito"
            ]
            == "URBANO"
        ]
        .copy()
    )


    print("\n" + "=" * 70)
    print("COMPONENTE URBANO")
    print("=" * 70)


    if punta_indio_urbano.empty:

        print(
            "No se encontraron registros urbanos."
        )

    else:

        print(
            punta_indio_urbano[
                [
                    "anio",
                    "matricula_inicial",
                    "matricula_primaria",
                    "matricula_secundaria"
                ]
            ]
            .sort_values(
                "anio"
            )
            .to_string(
                index=False
            )
        )


# ------------------------------------------------------------
# 27.13 COMPARAR COMPONENTE RURAL ENTRE AÑOS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VARIACIÓN DEL COMPONENTE RURAL")
print("=" * 70)


if not punta_indio_ambito.empty:

    rural_comparacion = (
        punta_indio_rural[
            [
                "anio",
                "matricula_inicial",
                "matricula_primaria",
                "matricula_secundaria"
            ]
        ]
        .sort_values(
            "anio"
        )
        .copy()
    )


    for nivel in [
        "inicial",
        "primaria",
        "secundaria"
    ]:

        columna = (
            f"matricula_{nivel}"
        )

        rural_comparacion[
            f"{nivel}_rural_anterior"
        ] = (
            rural_comparacion[
                columna
            ]
            .shift(1)
        )

        rural_comparacion[
            f"{nivel}_rural_variacion_pct"
        ] = (
            (
                rural_comparacion[
                    columna
                ]
                -
                rural_comparacion[
                    f"{nivel}_rural_anterior"
                ]
            )
            /
            rural_comparacion[
                f"{nivel}_rural_anterior"
            ]
            *
            100
        )


    print(
        rural_comparacion
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 27.14 PREPARAR MATRICULA_LIMPIA
# ------------------------------------------------------------

matricula_pi_limpia = (
    matricula_revision.copy()
)

matricula_pi_limpia[
    "partido"
] = (
    matricula_pi_limpia[
        "partido"
    ]
    .apply(
        normalizar_partido
    )
)


matricula_pi_limpia = (
    matricula_pi_limpia[
        (
            matricula_pi_limpia[
                "partido"
            ]
            == partido_punta_indio
        )
        &
        (
            matricula_pi_limpia[
                "anio"
            ]
            .isin(
                anios_punta_indio
            )
        )
    ]
    .copy()
)


print("\n" + "=" * 70)
print("REGISTROS EN MATRICULA_LIMPIA")
print("=" * 70)

print(
    matricula_pi_limpia
    .sort_values(
        [
            "anio",
            "nivel"
        ]
    )
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 27.15 PASAR MATRICULA_LIMPIA A WIDE
# ------------------------------------------------------------

matricula_pi_wide = (
    matricula_pi_limpia
    .pivot(
        index="anio",
        columns="nivel",
        values="matricula"
    )
    .reset_index()
)

matricula_pi_wide.columns.name = None


renombrar_pi = {}

if "Inicial" in matricula_pi_wide.columns:

    renombrar_pi[
        "Inicial"
    ] = "matricula_inicial_limpia"

if "Primaria" in matricula_pi_wide.columns:

    renombrar_pi[
        "Primaria"
    ] = "matricula_primaria_limpia"

if "Secundaria" in matricula_pi_wide.columns:

    renombrar_pi[
        "Secundaria"
    ] = "matricula_secundaria_limpia"


matricula_pi_wide = (
    matricula_pi_wide.rename(
        columns=renombrar_pi
    )
)


# ------------------------------------------------------------
# 27.16 COMPARAR FUENTE VS MATRICULA_LIMPIA
# ------------------------------------------------------------

if not punta_indio_ambito.empty:

    comparacion_pi = (
        punta_indio_totales
        .merge(
            matricula_pi_wide,
            on="anio",
            how="outer"
        )
        .sort_values(
            "anio"
        )
    )


    for nivel in [
        "inicial",
        "primaria",
        "secundaria"
    ]:

        fuente = (
            f"matricula_{nivel}_fuente"
        )

        limpia = (
            f"matricula_{nivel}_limpia"
        )


        comparacion_pi[
            f"coincide_{nivel}"
        ] = (
            comparacion_pi.apply(
                lambda fila:
                    valores_iguales(
                        fila[fuente],
                        fila[limpia]
                    ),
                axis=1
            )
        )


    comparacion_pi[
        "coincide_todo"
    ] = (
        comparacion_pi[
            [
                "coincide_inicial",
                "coincide_primaria",
                "coincide_secundaria"
            ]
        ]
        .all(
            axis=1
        )
    )


    print("\n" + "=" * 70)
    print("COMPARACIÓN FUENTE ORIGINAL VS MATRICULA_LIMPIA")
    print("=" * 70)

    print(
        comparacion_pi
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 27.17 APORTE DEL COMPONENTE URBANO AL TOTAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("APORTE DEL COMPONENTE URBANO")
print("=" * 70)


if (
    not punta_indio_ambito.empty
    and
    not punta_indio_urbano.empty
):

    aporte_urbano_pi = (
        punta_indio_urbano
        .merge(
            punta_indio_totales,
            on="anio",
            how="left"
        )
    )


    for nivel in [
        "inicial",
        "primaria",
        "secundaria"
    ]:

        aporte_urbano_pi[
            f"aporte_urbano_{nivel}_pct"
        ] = (
            aporte_urbano_pi[
                f"matricula_{nivel}"
            ]
            /
            aporte_urbano_pi[
                f"matricula_{nivel}_fuente"
            ]
            *
            100
        )


    columnas_aporte_pi = [

        "anio",

        "matricula_inicial",
        "matricula_inicial_fuente",
        "aporte_urbano_inicial_pct",

        "matricula_primaria",
        "matricula_primaria_fuente",
        "aporte_urbano_primaria_pct",

        "matricula_secundaria",
        "matricula_secundaria_fuente",
        "aporte_urbano_secundaria_pct"
    ]


    print(
        aporte_urbano_pi[
            columnas_aporte_pi
        ]
        .sort_values(
            "anio"
        )
        .to_string(
            index=False
        )
    )

else:

    print(
        "No existen registros urbanos para calcular el aporte."
    )


# ------------------------------------------------------------
# 27.18 RESUMEN AUTOMÁTICO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DE LA VERIFICACIÓN")
print("=" * 70)


if not punta_indio_ambito.empty:

    print(
        "Años analizados:",
        sorted(
            punta_indio_ambito[
                "anio"
            ]
            .unique()
            .tolist()
        )
    )

    print(
        "Años con componente Rural:",
        sorted(
            punta_indio_rural[
                "anio"
            ]
            .unique()
            .tolist()
        )
    )

    print(
        "Años con componente Urbano:",
        sorted(
            punta_indio_urbano[
                "anio"
            ]
            .unique()
            .tolist()
        )
    )


    if "comparacion_pi" in locals():

        print(
            "Años donde fuente y matricula_limpia "
            "coinciden completamente:",
            int(
                comparacion_pi[
                    "coincide_todo"
                ]
                .sum()
            ),
            "de",
            len(
                comparacion_pi
            )
        )


# ------------------------------------------------------------
# 27.19 INTERPRETACIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

print(
    """
Este análisis descompone la matrícula de Punta Indio según
el ámbito Rural y Urbano directamente desde las fuentes
originales.

El objetivo es determinar si las variaciones extraordinarias
detectadas en 2014-2015 y 2021-2022 coinciden con la
desaparición o aparición del componente Urbano.

La comparación del componente Rural entre años permite evaluar
si existe una continuidad aproximada de esa parte de la serie,
mientras que el cálculo del aporte Urbano permite cuantificar
cuánto representa ese ámbito sobre la matrícula total.

La comparación con matricula_limpia.csv permite además verificar
si los valores extraordinarios fueron introducidos durante la
limpieza o si ya estaban presentes en las fuentes originales.

IMPORTANTE:
Los resultados de este análisis todavía no justifican por sí
solos una imputación.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)


print("=" * 70)
print("VERIFICACIÓN DE PUNTA INDIO FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)
# ============================================================
# 28. AUDITORÍA DE LA COMPOSICIÓN DE SECUNDARIA
# PUNTA INDIO
# ============================================================

print("\n" + "=" * 70)
print("28. AUDITORÍA DE LA COMPOSICIÓN DE SECUNDARIA")
print("PUNTA INDIO")
print("=" * 70)

# Objetivo:
# Investigar por qué la matrícula secundaria calculada
# directamente desde las fuentes originales no coincide con
# matricula_limpia.csv en Punta Indio para algunos años.
#
# Se compararán:
#
# 1. las columnas _7 a _12;
# 2. la columna _1314 por separado;
# 3. la suma _7 a _12;
# 4. la suma _7 a _12 + _1314;
# 5. el valor existente en matricula_limpia.csv.
#
# IMPORTANTE:
# Este análisis es únicamente diagnóstico.
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 28.1 DEFINIR CASOS
# ------------------------------------------------------------

partido_auditoria_secundaria = "PUNTA INDIO"

anios_auditoria_secundaria = [
    2014,
    2015,
    2021,
    2022
]

columnas_secundaria_base = [
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12"
]

columna_1314 = "_1314"

resultados_secundaria_detalle = []


# ------------------------------------------------------------
# 28.2 LEER FUENTES ORIGINALES
# ------------------------------------------------------------

for anio in anios_auditoria_secundaria:

    archivo = os.path.join(
        carpeta,
        f"{anio} Matricula - agregada(in).csv"
    )

    print("\n" + "-" * 70)
    print(f"{partido_auditoria_secundaria} - {anio}")
    print("-" * 70)

    if not os.path.exists(archivo):

        print("⚠️ Archivo no encontrado.")
        continue

    try:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

    except UnicodeDecodeError:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="latin1",
            low_memory=False
        )

    # Normalizar nombres de columnas

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Controlar columnas necesarias

    columnas_control = {
        "departamento",
        "ambito"
    }

    if not columnas_control.issubset(
        set(df.columns)
    ):

        print(
            "⚠️ No se encontraron las columnas necesarias."
        )

        print(
            "Columnas disponibles:",
            df.columns.tolist()
        )

        continue


    # --------------------------------------------------------
    # 28.3 NORMALIZAR PARTIDO Y ÁMBITO
    # --------------------------------------------------------

    df["departamento"] = (
        df["departamento"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["ambito"] = (
        df["ambito"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    # --------------------------------------------------------
    # 28.4 FILTRAR PUNTA INDIO
    # --------------------------------------------------------

    temp = df[
        df["departamento"]
        == partido_auditoria_secundaria
    ].copy()

    print(
        "Registros encontrados:",
        len(temp)
    )

    if temp.empty:

        continue


    # --------------------------------------------------------
    # 28.5 CONVERTIR COLUMNAS A NUMÉRICAS
    # --------------------------------------------------------

    columnas_a_convertir = (
        columnas_secundaria_base
        + [columna_1314]
    )

    for columna in columnas_a_convertir:

        if columna in temp.columns:

            temp[columna] = pd.to_numeric(
                temp[columna],
                errors="coerce"
            )

        else:

            # Si la columna no existe, la dejamos como NaN
            # para que quede explícito en la auditoría.

            temp[columna] = np.nan


    # --------------------------------------------------------
    # 28.6 CALCULAR SECUNDARIA CON DOS DEFINICIONES
    # --------------------------------------------------------

    # Definición A:
    # solamente _7 a _12

    temp["secundaria_7_12"] = (
        temp[
            columnas_secundaria_base
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )

    # Definición B:
    # _7 a _12 + _1314

    temp["secundaria_7_1314"] = (
        temp[
            columnas_secundaria_base
            + [columna_1314]
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )


    # --------------------------------------------------------
    # 28.7 GUARDAR DETALLE POR ÁMBITO
    # --------------------------------------------------------

    for _, fila in temp.iterrows():

        resultados_secundaria_detalle.append({

            "partido":
                partido_auditoria_secundaria,

            "anio":
                anio,

            "ambito":
                fila["ambito"],

            "_7":
                fila["_7"],

            "_8":
                fila["_8"],

            "_9":
                fila["_9"],

            "_10":
                fila["_10"],

            "_11":
                fila["_11"],

            "_12":
                fila["_12"],

            "_1314":
                fila["_1314"],

            "secundaria_7_12":
                fila["secundaria_7_12"],

            "secundaria_7_1314":
                fila["secundaria_7_1314"]
        })


# ------------------------------------------------------------
# 28.8 CREAR TABLA DETALLADA
# ------------------------------------------------------------

detalle_secundaria = pd.DataFrame(
    resultados_secundaria_detalle
)

print("\n" + "=" * 70)
print("COMPOSICIÓN DE SECUNDARIA POR ÁMBITO")
print("=" * 70)

if detalle_secundaria.empty:

    print(
        "No se pudieron generar resultados."
    )

else:

    print(
        detalle_secundaria
        .sort_values(
            ["anio", "ambito"]
        )
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 28.9 CALCULAR TOTALES POR AÑO
# ------------------------------------------------------------

if not detalle_secundaria.empty:

    totales_secundaria = (
        detalle_secundaria
        .groupby(
            "anio",
            as_index=False
        )
        .agg(
            total_7=(
                "_7",
                lambda x: x.sum(min_count=1)
            ),

            total_8=(
                "_8",
                lambda x: x.sum(min_count=1)
            ),

            total_9=(
                "_9",
                lambda x: x.sum(min_count=1)
            ),

            total_10=(
                "_10",
                lambda x: x.sum(min_count=1)
            ),

            total_11=(
                "_11",
                lambda x: x.sum(min_count=1)
            ),

            total_12=(
                "_12",
                lambda x: x.sum(min_count=1)
            ),

            total_1314=(
                "_1314",
                lambda x: x.sum(min_count=1)
            ),

            secundaria_7_12=(
                "secundaria_7_12",
                lambda x: x.sum(min_count=1)
            ),

            secundaria_7_1314=(
                "secundaria_7_1314",
                lambda x: x.sum(min_count=1)
            )
        )
    )


    print("\n" + "=" * 70)
    print("TOTALES DE SECUNDARIA POR AÑO")
    print("=" * 70)

    print(
        totales_secundaria
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 28.10 OBTENER SECUNDARIA DE MATRICULA_LIMPIA
    # --------------------------------------------------------

    secundaria_limpia_punta_indio = (
        matricula_revision[
            (
                matricula_revision[
                    "partido"
                ].apply(
                    normalizar_partido
                )
                ==
                partido_auditoria_secundaria
            )
            &
            (
                matricula_revision[
                    "anio"
                ].isin(
                    anios_auditoria_secundaria
                )
            )
            &
            (
                matricula_revision[
                    "nivel"
                ]
                ==
                "Secundaria"
            )
        ][
            [
                "anio",
                "matricula"
            ]
        ]
        .copy()
    )

    secundaria_limpia_punta_indio = (
        secundaria_limpia_punta_indio
        .rename(
            columns={
                "matricula":
                    "secundaria_matricula_limpia"
            }
        )
    )


    # --------------------------------------------------------
    # 28.11 COMPARAR LAS DOS DEFINICIONES
    # --------------------------------------------------------

    comparacion_definicion_secundaria = (
        totales_secundaria
        .merge(
            secundaria_limpia_punta_indio,
            on="anio",
            how="left"
        )
    )


    comparacion_definicion_secundaria[
        "diferencia_7_12"
    ] = (
        comparacion_definicion_secundaria[
            "secundaria_7_12"
        ]
        -
        comparacion_definicion_secundaria[
            "secundaria_matricula_limpia"
        ]
    )


    comparacion_definicion_secundaria[
        "diferencia_7_1314"
    ] = (
        comparacion_definicion_secundaria[
            "secundaria_7_1314"
        ]
        -
        comparacion_definicion_secundaria[
            "secundaria_matricula_limpia"
        ]
    )


    comparacion_definicion_secundaria[
        "coincide_7_12"
    ] = comparacion_definicion_secundaria.apply(

        lambda fila: valores_iguales(

            fila[
                "secundaria_7_12"
            ],

            fila[
                "secundaria_matricula_limpia"
            ]

        ),

        axis=1
    )


    comparacion_definicion_secundaria[
        "coincide_7_1314"
    ] = comparacion_definicion_secundaria.apply(

        lambda fila: valores_iguales(

            fila[
                "secundaria_7_1314"
            ],

            fila[
                "secundaria_matricula_limpia"
            ]

        ),

        axis=1
    )


    print("\n" + "=" * 70)
    print("COMPARACIÓN DE DEFINICIONES DE SECUNDARIA")
    print("=" * 70)

    columnas_comparacion = [

        "anio",

        "secundaria_7_12",

        "total_1314",

        "secundaria_7_1314",

        "secundaria_matricula_limpia",

        "diferencia_7_12",

        "diferencia_7_1314",

        "coincide_7_12",

        "coincide_7_1314"
    ]

    print(
        comparacion_definicion_secundaria[
            columnas_comparacion
        ]
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 28.12 IDENTIFICAR QUÉ DEFINICIÓN COINCIDE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESULTADO POR AÑO")
    print("=" * 70)

    for _, fila in (
        comparacion_definicion_secundaria
        .sort_values("anio")
        .iterrows()
    ):

        anio = int(
            fila["anio"]
        )

        coincide_base = (
            fila["coincide_7_12"]
        )

        coincide_ampliada = (
            fila["coincide_7_1314"]
        )

        if coincide_base and not coincide_ampliada:

            resultado = (
                "matricula_limpia coincide con _7 a _12 "
                "y NO incluye _1314"
            )

        elif coincide_ampliada and not coincide_base:

            resultado = (
                "matricula_limpia coincide con _7 a _12 + _1314"
            )

        elif coincide_base and coincide_ampliada:

            resultado = (
                "ambas definiciones coinciden; "
                "_1314 es 0 o no aporta matrícula"
            )

        else:

            resultado = (
                "ninguna de las dos definiciones coincide; "
                "se requiere revisar otras columnas o la "
                "construcción de matricula_limpia"
            )

        print(
            f"{anio}: {resultado}"
        )


    # --------------------------------------------------------
    # 28.13 RESUMEN AUTOMÁTICO
    # --------------------------------------------------------

    cantidad_coincide_base = (
        comparacion_definicion_secundaria[
            "coincide_7_12"
        ]
        .sum()
    )

    cantidad_coincide_ampliada = (
        comparacion_definicion_secundaria[
            "coincide_7_1314"
        ]
        .sum()
    )


    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)

    print(
        "Años analizados:",
        len(
            comparacion_definicion_secundaria
        )
    )

    print(
        "Años donde coincide _7 a _12:",
        cantidad_coincide_base
    )

    print(
        "Años donde coincide _7 a _12 + _1314:",
        cantidad_coincide_ampliada
    )


    # --------------------------------------------------------
    # 28.14 INTERPRETACIÓN
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("INTERPRETACIÓN")
    print("=" * 70)

    print(
        """
Este análisis verifica qué columnas de las fuentes originales
explican el valor de matrícula secundaria utilizado en
matricula_limpia.csv para Punta Indio.

Se comparan dos definiciones:

A) suma de _7 a _12;

B) suma de _7 a _12 más _1314.

El objetivo es determinar si las diferencias detectadas en el
punto anterior se deben específicamente a la inclusión de la
columna _1314 o si existe otra diferencia en la construcción
del indicador de matrícula secundaria.

Todavía no se asume cuál definición es metodológicamente
correcta. La coincidencia con matricula_limpia.csv permite
reconstruir cómo fue calculado el indicador, pero la decisión
sobre qué columnas deben formar Secundaria deberá mantenerse
consistente con el criterio utilizado para construir la serie
completa.

IMPORTANTE:
NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
    )


print("=" * 70)
print("AUDITORÍA DE SECUNDARIA FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 29. VALIDACIÓN GLOBAL DE LA DEFINICIÓN DE SECUNDARIA
# ============================================================

print("\n" + "=" * 70)
print("29. VALIDACIÓN GLOBAL DE LA DEFINICIÓN DE SECUNDARIA")
print("=" * 70)

# Objetivo:
# Verificar globalmente qué definición de Secundaria reproduce
# los valores existentes en matricula_limpia.csv.
#
# Se compararán:
#
# A) _7 + _8 + _9 + _10 + _11 + _12
#
# B) _7 + _8 + _9 + _10 + _11 + _12 + _1314
#
# Esto permitirá confirmar si la diferencia detectada en
# Punta Indio se debe exclusivamente a la inclusión de _1314
# en los cálculos diagnósticos posteriores.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 29.1 DEFINIR PERÍODO Y COLUMNAS
# ------------------------------------------------------------

anios_validacion_secundaria = range(2012, 2026)

columnas_secundaria_base = [
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12"
]

columna_secundaria_1314 = "_1314"

resultados_validacion_secundaria = []


# ------------------------------------------------------------
# 29.2 LEER TODAS LAS FUENTES ORIGINALES
# ------------------------------------------------------------

for anio in anios_validacion_secundaria:

    archivo = os.path.join(
        carpeta,
        f"{anio} Matricula - agregada(in).csv"
    )

    print(f"\nAnalizando Secundaria - {anio}...")

    if not os.path.exists(archivo):

        print(
            f"⚠️ No se encontró el archivo de {anio}."
        )

        continue


    # --------------------------------------------------------
    # LEER ARCHIVO
    # --------------------------------------------------------

    try:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

    except UnicodeDecodeError:

        df = pd.read_csv(
            archivo,
            sep=";",
            encoding="latin1",
            low_memory=False
        )


    # --------------------------------------------------------
    # NORMALIZAR COLUMNAS
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # --------------------------------------------------------
    # CONTROLAR ESTRUCTURA
    # --------------------------------------------------------

    if "departamento" not in df.columns:

        print(
            f"⚠️ {anio}: no se encontró la columna departamento."
        )

        print(
            "Columnas disponibles:",
            df.columns.tolist()
        )

        continue


    # --------------------------------------------------------
    # NORMALIZAR PARTIDO
    # --------------------------------------------------------

    df["departamento"] = (
        df["departamento"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    # --------------------------------------------------------
    # CONVERTIR COLUMNAS DE SECUNDARIA
    # --------------------------------------------------------

    columnas_a_convertir = (
        columnas_secundaria_base
        + [columna_secundaria_1314]
    )

    for columna in columnas_a_convertir:

        if columna in df.columns:

            df[columna] = pd.to_numeric(
                df[columna],
                errors="coerce"
            )

        else:

            # Dejamos explícitamente NaN si la columna
            # no existe en un determinado archivo.

            df[columna] = np.nan


    # --------------------------------------------------------
    # 29.3 CALCULAR SECUNDARIA POR FILA
    # --------------------------------------------------------

    # Definición A: _7 a _12

    df["secundaria_7_12"] = (
        df[
            columnas_secundaria_base
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )


    # Definición B: _7 a _12 + _1314

    df["secundaria_7_1314"] = (
        df[
            columnas_secundaria_base
            + [columna_secundaria_1314]
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )


    # --------------------------------------------------------
    # 29.4 SUMAR POR PARTIDO
    # --------------------------------------------------------

    secundaria_anual = (
        df
        .groupby(
            "departamento",
            as_index=False
        )
        .agg(
            secundaria_7_12=(
                "secundaria_7_12",
                lambda x: x.sum(min_count=1)
            ),

            secundaria_7_1314=(
                "secundaria_7_1314",
                lambda x: x.sum(min_count=1)
            ),

            total_1314=(
                columna_secundaria_1314,
                lambda x: x.sum(min_count=1)
            )
        )
    )


    secundaria_anual["anio"] = anio

    secundaria_anual = (
        secundaria_anual.rename(
            columns={
                "departamento":
                    "partido"
            }
        )
    )


    resultados_validacion_secundaria.append(
        secundaria_anual
    )


# ------------------------------------------------------------
# 29.5 UNIR TODOS LOS AÑOS
# ------------------------------------------------------------

if not resultados_validacion_secundaria:

    print("\n" + "=" * 70)
    print("NO SE GENERARON RESULTADOS")
    print("=" * 70)

else:

    secundaria_fuentes_global = pd.concat(
        resultados_validacion_secundaria,
        ignore_index=True
    )


    # --------------------------------------------------------
    # 29.6 NORMALIZAR PARTIDOS DE LAS FUENTES
    # --------------------------------------------------------

    secundaria_fuentes_global[
        "partido"
    ] = (
        secundaria_fuentes_global[
            "partido"
        ]
        .apply(
            normalizar_partido
        )
    )


    # --------------------------------------------------------
    # 29.7 PREPARAR MATRICULA_LIMPIA
    # --------------------------------------------------------

    secundaria_limpia_global = (
        matricula_revision[
            matricula_revision[
                "nivel"
            ]
            ==
            "Secundaria"
        ][
            [
                "partido",
                "anio",
                "matricula"
            ]
        ]
        .copy()
    )


    secundaria_limpia_global[
        "partido"
    ] = (
        secundaria_limpia_global[
            "partido"
        ]
        .apply(
            normalizar_partido
        )
    )


    secundaria_limpia_global = (
        secundaria_limpia_global.rename(
            columns={
                "matricula":
                    "secundaria_matricula_limpia"
            }
        )
    )


    # --------------------------------------------------------
    # 29.8 CONTROL DE DUPLICADOS
    # --------------------------------------------------------

    duplicados_fuente = (
        secundaria_fuentes_global
        .duplicated(
            subset=[
                "partido",
                "anio"
            ]
        )
        .sum()
    )

    duplicados_limpia = (
        secundaria_limpia_global
        .duplicated(
            subset=[
                "partido",
                "anio"
            ]
        )
        .sum()
    )


    print("\n" + "=" * 70)
    print("CONTROL DE DUPLICADOS")
    print("=" * 70)

    print(
        "Duplicados partido-año en fuentes:",
        duplicados_fuente
    )

    print(
        "Duplicados partido-año en matricula_limpia:",
        duplicados_limpia
    )


    # --------------------------------------------------------
    # 29.9 UNIR FUENTES Y MATRICULA_LIMPIA
    # --------------------------------------------------------

    comparacion_secundaria_global = (
        secundaria_fuentes_global
        .merge(
            secundaria_limpia_global,
            on=[
                "partido",
                "anio"
            ],
            how="outer",
            indicator=True
        )
    )


    # --------------------------------------------------------
    # 29.10 COMPARAR VALORES INCLUYENDO NaN
    # --------------------------------------------------------

    comparacion_secundaria_global[
        "coincide_7_12"
    ] = comparacion_secundaria_global.apply(

        lambda fila: valores_iguales(

            fila[
                "secundaria_7_12"
            ],

            fila[
                "secundaria_matricula_limpia"
            ]

        ),

        axis=1
    )


    comparacion_secundaria_global[
        "coincide_7_1314"
    ] = comparacion_secundaria_global.apply(

        lambda fila: valores_iguales(

            fila[
                "secundaria_7_1314"
            ],

            fila[
                "secundaria_matricula_limpia"
            ]

        ),

        axis=1
    )


    # --------------------------------------------------------
    # 29.11 CALCULAR DIFERENCIAS
    # --------------------------------------------------------

    comparacion_secundaria_global[
        "diferencia_7_12"
    ] = (
        comparacion_secundaria_global[
            "secundaria_7_12"
        ]
        -
        comparacion_secundaria_global[
            "secundaria_matricula_limpia"
        ]
    )


    comparacion_secundaria_global[
        "diferencia_7_1314"
    ] = (
        comparacion_secundaria_global[
            "secundaria_7_1314"
        ]
        -
        comparacion_secundaria_global[
            "secundaria_matricula_limpia"
        ]
    )


    # --------------------------------------------------------
    # 29.12 RESUMEN GENERAL
    # --------------------------------------------------------

    cantidad_comparaciones = len(
        comparacion_secundaria_global
    )

    cantidad_coincide_7_12 = (
        comparacion_secundaria_global[
            "coincide_7_12"
        ]
        .sum()
    )

    cantidad_coincide_7_1314 = (
        comparacion_secundaria_global[
            "coincide_7_1314"
        ]
        .sum()
    )


    print("\n" + "=" * 70)
    print("RESUMEN GLOBAL")
    print("=" * 70)

    print(
        "Registros partido-año comparados:",
        cantidad_comparaciones
    )

    print(
        "Coincidencias usando _7 a _12:",
        cantidad_coincide_7_12
    )

    print(
        "Coincidencias usando _7 a _12 + _1314:",
        cantidad_coincide_7_1314
    )


    if cantidad_comparaciones > 0:

        porcentaje_7_12 = (
            cantidad_coincide_7_12
            /
            cantidad_comparaciones
            * 100
        )

        porcentaje_7_1314 = (
            cantidad_coincide_7_1314
            /
            cantidad_comparaciones
            * 100
        )

        print(
            "Porcentaje coincidencia _7 a _12:",
            round(
                porcentaje_7_12,
                2
            ),
            "%"
        )

        print(
            "Porcentaje coincidencia _7 a _12 + _1314:",
            round(
                porcentaje_7_1314,
                2
            ),
            "%"
        )


    # --------------------------------------------------------
    # 29.13 CONTROL DE PRESENCIA EN AMBAS FUENTES
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PRESENCIA DE REGISTROS")
    print("=" * 70)

    print(
        comparacion_secundaria_global[
            "_merge"
        ]
        .value_counts()
        .to_string()
    )


    # --------------------------------------------------------
    # 29.14 MOSTRAR DIFERENCIAS PARA _7 A _12
    # --------------------------------------------------------

    diferencias_7_12 = (
        comparacion_secundaria_global[
            ~comparacion_secundaria_global[
                "coincide_7_12"
            ]
        ]
        .copy()
    )


    print("\n" + "=" * 70)
    print("DIFERENCIAS USANDO _7 A _12")
    print("=" * 70)

    if diferencias_7_12.empty:

        print(
            "No se detectaron diferencias."
        )

    else:

        columnas_diferencias = [

            "partido",
            "anio",

            "secundaria_7_12",

            "secundaria_matricula_limpia",

            "diferencia_7_12",

            "total_1314",

            "_merge"
        ]

        print(
            diferencias_7_12[
                columnas_diferencias
            ]
            .sort_values(
                [
                    "partido",
                    "anio"
                ]
            )
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 29.15 CASOS DONDE _1314 CAMBIA EL RESULTADO
    # --------------------------------------------------------

    casos_1314_relevante = (
        comparacion_secundaria_global[
            (
                comparacion_secundaria_global[
                    "coincide_7_12"
                ]
            )
            &
            (
                ~comparacion_secundaria_global[
                    "coincide_7_1314"
                ]
            )
        ]
        .copy()
    )


    print("\n" + "=" * 70)
    print("CASOS DONDE _1314 GENERA DIFERENCIA")
    print("=" * 70)

    print(
        "Cantidad de casos:",
        len(
            casos_1314_relevante
        )
    )


    if not casos_1314_relevante.empty:

        print(
            casos_1314_relevante[
                [
                    "partido",
                    "anio",
                    "secundaria_7_12",
                    "total_1314",
                    "secundaria_7_1314",
                    "secundaria_matricula_limpia"
                ]
            ]
            .sort_values(
                [
                    "partido",
                    "anio"
                ]
            )
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 29.16 RESUMEN POR AÑO
    # --------------------------------------------------------

    resumen_secundaria_anio = (
        comparacion_secundaria_global
        .groupby(
            "anio"
        )
        .agg(
            registros=(
                "partido",
                "size"
            ),

            coincidencias_7_12=(
                "coincide_7_12",
                "sum"
            ),

            coincidencias_7_1314=(
                "coincide_7_1314",
                "sum"
            )
        )
        .reset_index()
    )


    resumen_secundaria_anio[
        "pct_7_12"
    ] = (
        resumen_secundaria_anio[
            "coincidencias_7_12"
        ]
        /
        resumen_secundaria_anio[
            "registros"
        ]
        * 100
    )


    resumen_secundaria_anio[
        "pct_7_1314"
    ] = (
        resumen_secundaria_anio[
            "coincidencias_7_1314"
        ]
        /
        resumen_secundaria_anio[
            "registros"
        ]
        * 100
    )


    print("\n" + "=" * 70)
    print("COINCIDENCIA POR AÑO")
    print("=" * 70)

    print(
        resumen_secundaria_anio
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 29.17 CONCLUSIÓN AUTOMÁTICA
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("INTERPRETACIÓN")
    print("=" * 70)


    if (
        cantidad_coincide_7_12
        ==
        cantidad_comparaciones
    ):

        print(
            """
La definición de Secundaria basada en la suma de las columnas
_7 a _12 reproduce completamente los valores presentes en
matricula_limpia.csv para todos los registros partido-año
comparados.

Esto confirma que _1314 no forma parte del indicador de
matrícula secundaria utilizado para construir
matricula_limpia.csv.

Las diferencias detectadas previamente al incluir _1314
corresponden, por lo tanto, al cálculo realizado durante las
auditorías posteriores y no a un error de matricula_limpia.csv.
"""
        )

    else:

        print(
            """
La suma de _7 a _12 no reproduce completamente los valores
presentes en matricula_limpia.csv.

Existen casos que requieren una revisión adicional antes de
confirmar globalmente la definición de matrícula secundaria.

Las diferencias se muestran en la sección anterior y deberán
analizarse antes de modificar cualquier cálculo.
"""
        )


    print(
        """
IMPORTANTE:
Este análisis solamente valida la consistencia entre las
fuentes originales y matricula_limpia.csv.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
    )


print("=" * 70)
print("VALIDACIÓN GLOBAL DE SECUNDARIA FINALIZADA")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)
# ============================================================
# 30. DIAGNÓSTICO: RECONSTRUIR CÓMO SE OBTUVO MATRICULA_LIMPIA
# ============================================================

print("\n" + "=" * 70)
print("30. DIAGNÓSTICO: RECONSTRUIR CÓMO SE OBTUVO MATRICULA_LIMPIA")
print("=" * 70)

# Objetivo:
# Analizar un caso concreto donde el cálculo realizado
# directamente desde la fuente original no coincide con
# matricula_limpia.csv.
#
# Caso seleccionado:
# 25 DE MAYO - 2012
#
# Este punto es únicamente diagnóstico.
# NO modifica ningún dataset.
# NO realiza imputaciones.
# NO guarda archivos.


# ------------------------------------------------------------
# 30.1 DEFINIR CASO DE PRUEBA
# ------------------------------------------------------------

PARTIDO_PRUEBA = "25 DE MAYO"
ANIO_PRUEBA = 2012


# ------------------------------------------------------------
# 30.2 LOCALIZAR ARCHIVO ORIGINAL
# ------------------------------------------------------------

archivo_prueba = os.path.join(
    carpeta,
    f"{ANIO_PRUEBA} Matricula - agregada(in).csv"
)

print("\nArchivo esperado:")
print(archivo_prueba)

if not os.path.exists(archivo_prueba):

    raise FileNotFoundError(
        f"No se encontró el archivo original correspondiente "
        f"a {ANIO_PRUEBA} dentro de la carpeta:\n{carpeta}"
    )

print("\nArchivo encontrado correctamente.")


# ------------------------------------------------------------
# 30.3 LEER ARCHIVO ORIGINAL
# ------------------------------------------------------------

try:

    df_original = pd.read_csv(
        archivo_prueba,
        sep=";",
        encoding="utf-8",
        low_memory=False
    )

except UnicodeDecodeError:

    df_original = pd.read_csv(
        archivo_prueba,
        sep=";",
        encoding="latin1",
        low_memory=False
    )


print("\nDimensiones del archivo original:")
print(df_original.shape)


# ------------------------------------------------------------
# 30.4 NORMALIZAR NOMBRES DE COLUMNAS
# ------------------------------------------------------------

df_original.columns = (
    df_original.columns
    .astype(str)
    .str.strip()
    .str.lower()
)

print("\nColumnas disponibles:")
print(df_original.columns.tolist())


# ------------------------------------------------------------
# 30.5 DETECTAR COLUMNA TERRITORIAL
# ------------------------------------------------------------

if "departamento" in df_original.columns:

    col_partido = "departamento"

elif "partido" in df_original.columns:

    col_partido = "partido"

else:

    raise ValueError(
        "No se encontró una columna 'departamento' ni 'partido'."
    )


print("\nColumna territorial utilizada:")
print(col_partido)


# ------------------------------------------------------------
# 30.6 NORMALIZAR PARTIDOS
# ------------------------------------------------------------

df_original["_partido_norm"] = (
    df_original[col_partido]
    .apply(normalizar_partido)
)


# ------------------------------------------------------------
# 30.7 FILTRAR 25 DE MAYO
# ------------------------------------------------------------

caso = df_original[
    df_original["_partido_norm"]
    ==
    normalizar_partido(PARTIDO_PRUEBA)
].copy()


print(
    f"\nFilas encontradas para "
    f"{PARTIDO_PRUEBA} - {ANIO_PRUEBA}:",
    len(caso)
)


if caso.empty:

    print("\n⚠️ No se encontraron registros para el partido.")

else:

    # --------------------------------------------------------
    # 30.8 IDENTIFICAR COLUMNAS RELEVANTES
    # --------------------------------------------------------

    columnas_secundaria = [
        "_7",
        "_8",
        "_9",
        "_10",
        "_11",
        "_12"
    ]

    columnas_extra = [
        "_1314"
    ]

    columnas_numericas = (
        columnas_secundaria
        +
        columnas_extra
    )


    for columna in columnas_numericas:

        if columna in caso.columns:

            caso[columna] = pd.to_numeric(
                caso[columna],
                errors="coerce"
            )

        else:

            caso[columna] = np.nan


    # --------------------------------------------------------
    # 30.9 MOSTRAR VARIABLES CATEGÓRICAS
    # --------------------------------------------------------

    posibles_categoricas = [

        "ambito",
        "sector",
        "gestion",
        "dependencia",
        "nivel",
        "modalidad",
        "rama",
        "tipo"
    ]

    columnas_categoricas = [

        columna
        for columna in posibles_categoricas
        if columna in caso.columns
    ]


    print("\n" + "=" * 70)
    print("FILAS ORIGINALES DE 25 DE MAYO")
    print("=" * 70)


    columnas_mostrar = (
        [col_partido]
        +
        columnas_categoricas
        +
        columnas_secundaria
        +
        columnas_extra
    )


    print(
        caso[
            columnas_mostrar
        ]
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 30.10 CALCULAR SECUNDARIA POR FILA
    # --------------------------------------------------------

    caso["secundaria_7_12"] = (
        caso[
            columnas_secundaria
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )


    caso["secundaria_7_1314"] = (
        caso[
            columnas_secundaria
            +
            columnas_extra
        ]
        .sum(
            axis=1,
            min_count=1
        )
    )


    print("\n" + "=" * 70)
    print("SECUNDARIA CALCULADA POR FILA")
    print("=" * 70)


    columnas_detalle = (
        [col_partido]
        +
        columnas_categoricas
        +
        [
            "secundaria_7_12",
            "secundaria_7_1314"
        ]
    )


    print(
        caso[
            columnas_detalle
        ]
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 30.11 TOTALES GENERALES
    # --------------------------------------------------------

    total_7_12 = (
        caso[
            "secundaria_7_12"
        ]
        .sum(
            min_count=1
        )
    )


    total_7_1314 = (
        caso[
            "secundaria_7_1314"
        ]
        .sum(
            min_count=1
        )
    )


    total_1314 = (
        caso[
            "_1314"
        ]
        .sum(
            min_count=1
        )
    )


    print("\n" + "=" * 70)
    print("TOTALES CALCULADOS DESDE LA FUENTE")
    print("=" * 70)

    print(
        "Total secundaria _7 a _12:",
        total_7_12
    )

    print(
        "Total _1314:",
        total_1314
    )

    print(
        "Total secundaria _7 a _12 + _1314:",
        total_7_1314
    )


    # --------------------------------------------------------
    # 30.12 OBTENER VALOR DE MATRICULA_LIMPIA
    # --------------------------------------------------------

    valor_limpio = (
        matricula_revision[
            (
                matricula_revision[
                    "partido"
                ].apply(
                    normalizar_partido
                )
                ==
                normalizar_partido(
                    PARTIDO_PRUEBA
                )
            )
            &
            (
                matricula_revision[
                    "anio"
                ]
                ==
                ANIO_PRUEBA
            )
            &
            (
                matricula_revision[
                    "nivel"
                ]
                ==
                "Secundaria"
            )
        ][
            "matricula"
        ]
    )


    if valor_limpio.empty:

        valor_matricula_limpia = np.nan

    else:

        valor_matricula_limpia = (
            valor_limpio.iloc[0]
        )


    print("\n" + "=" * 70)
    print("VALOR EN MATRICULA_LIMPIA")
    print("=" * 70)

    print(
        f"{PARTIDO_PRUEBA} - "
        f"{ANIO_PRUEBA} - Secundaria:",
        valor_matricula_limpia
    )


    # --------------------------------------------------------
    # 30.13 BUSCAR FILAS QUE EXPLIQUEN EL VALOR LIMPIO
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("BÚSQUEDA DE LA CONSTRUCCIÓN DEL VALOR")
    print("=" * 70)


    coincidencias_individuales = caso[
        caso[
            "secundaria_7_12"
        ]
        ==
        valor_matricula_limpia
    ]


    print(
        "\nFilas individuales que coinciden exactamente "
        "con matricula_limpia:"
    )


    if coincidencias_individuales.empty:

        print(
            "Ninguna fila individual coincide exactamente."
        )

    else:

        print(
            coincidencias_individuales[
                columnas_detalle
            ]
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 30.14 ANALIZAR POR ÁMBITO
    # --------------------------------------------------------

    if "ambito" in caso.columns:

        resumen_ambito = (
            caso
            .groupby(
                "ambito",
                dropna=False,
                as_index=False
            )
            .agg(
                secundaria_7_12=(
                    "secundaria_7_12",
                    lambda x: x.sum(
                        min_count=1
                    )
                ),

                secundaria_7_1314=(
                    "secundaria_7_1314",
                    lambda x: x.sum(
                        min_count=1
                    )
                )
            )
        )


        print("\n" + "=" * 70)
        print("SECUNDARIA POR ÁMBITO")
        print("=" * 70)

        print(
            resumen_ambito
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 30.15 ANALIZAR OTRAS VARIABLES CATEGÓRICAS
    # --------------------------------------------------------

    for variable in columnas_categoricas:

        if variable == "ambito":
            continue

        print("\n" + "=" * 70)
        print(
            f"SECUNDARIA AGRUPADA POR {variable.upper()}"
        )
        print("=" * 70)

        resumen_variable = (
            caso
            .groupby(
                variable,
                dropna=False,
                as_index=False
            )
            .agg(
                cantidad_filas=(
                    "secundaria_7_12",
                    "size"
                ),

                secundaria_7_12=(
                    "secundaria_7_12",
                    lambda x: x.sum(
                        min_count=1
                    )
                )
            )
        )

        print(
            resumen_variable
            .to_string(
                index=False
            )
        )


    # --------------------------------------------------------
    # 30.16 COMPARACIÓN FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("COMPARACIÓN FINAL")
    print("=" * 70)

    print(
        "Fuente completa (_7 a _12):",
        total_7_12
    )

    print(
        "matricula_limpia:",
        valor_matricula_limpia
    )

    if (
        pd.notna(total_7_12)
        and
        pd.notna(valor_matricula_limpia)
    ):

        diferencia = (
            total_7_12
            -
            valor_matricula_limpia
        )

        print(
            "Diferencia:",
            diferencia
        )


# ------------------------------------------------------------
# 30.17 INTERPRETACIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

print(
    """
Este diagnóstico analiza directamente las filas originales de
25 DE MAYO para el año 2012.

El objetivo es identificar por qué la suma global de las
columnas _7 a _12 obtenida directamente desde la fuente no
coincide con el valor existente en matricula_limpia.csv.

Se muestran las filas originales y se desagregan los resultados
según las variables categóricas disponibles, como ámbito,
sector, gestión, dependencia, nivel o modalidad.

Esto permitirá determinar si matricula_limpia fue construido
utilizando solamente un subconjunto específico de los registros
originales.

IMPORTANTE:
NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)


print("=" * 70)
print("DIAGNÓSTICO 30 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 31. IDENTIFICAR QUÉ FILAS REPRODUCEN MATRICULA_LIMPIA
# ============================================================

print("\n" + "=" * 70)
print("31. IDENTIFICAR QUÉ FILAS REPRODUCEN MATRICULA_LIMPIA")
print("=" * 70)

# Objetivo:
# Determinar qué subconjunto de las filas originales de
# 25 DE MAYO - 2012 reproduce exactamente el valor de
# Secundaria presente en matricula_limpia.csv.
#
# En el punto 30 obtuvimos:
#
# Fuente completa (_7 a _12): 11.501
# matricula_limpia:             3.133
#
# Observamos además que:
#
# 659 + 1845 + 629 = 3133
#
# Este punto verifica sistemáticamente esa coincidencia y
# analiza qué características distinguen esas filas del resto.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 31.1 CONTROLES PREVIOS
# ------------------------------------------------------------

if "caso" not in globals():

    raise ValueError(
        "No existe el DataFrame 'caso'. "
        "Ejecutá primero el punto 30."
    )

if caso.empty:

    raise ValueError(
        "El DataFrame del caso está vacío."
    )

if "secundaria_7_12" not in caso.columns:

    raise ValueError(
        "No existe la columna secundaria_7_12. "
        "Ejecutá primero el punto 30."
    )


objetivo_secundaria = valor_matricula_limpia

print("\nValor objetivo de matricula_limpia:")
print(objetivo_secundaria)

print("\nCantidad de filas disponibles:")
print(len(caso))


# ------------------------------------------------------------
# 31.2 ASIGNAR IDENTIFICADOR A CADA FILA
# ------------------------------------------------------------

caso_31 = caso.copy().reset_index(drop=True)

caso_31["id_fila"] = (
    caso_31.index + 1
)


# ------------------------------------------------------------
# 31.3 MOSTRAR FILAS DISPONIBLES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FILAS DISPONIBLES")
print("=" * 70)

columnas_identificacion = [
    "id_fila",
    col_partido
]

for columna in [
    "sector",
    "ambito",
    "multi_ini",
    "multi_pri",
    "multi_sec",
    "multinivel"
]:

    if columna in caso_31.columns:

        columnas_identificacion.append(
            columna
        )

columnas_identificacion.append(
    "secundaria_7_12"
)

print(
    caso_31[
        columnas_identificacion
    ]
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 31.4 BUSCAR TODAS LAS COMBINACIONES POSIBLES
# ------------------------------------------------------------

from itertools import combinations

coincidencias = []

cantidad_filas = len(caso_31)

for cantidad in range(
    1,
    cantidad_filas + 1
):

    for indices in combinations(
        range(cantidad_filas),
        cantidad
    ):

        valores = (
            caso_31
            .iloc[
                list(indices)
            ][
                "secundaria_7_12"
            ]
        )

        total = valores.sum(
            min_count=1
        )

        if (
            pd.notna(total)
            and
            pd.notna(objetivo_secundaria)
            and
            np.isclose(
                total,
                objetivo_secundaria
            )
        ):

            ids = (
                caso_31
                .iloc[
                    list(indices)
                ][
                    "id_fila"
                ]
                .tolist()
            )

            coincidencias.append({
                "cantidad_filas":
                    cantidad,

                "ids_filas":
                    ids,

                "total":
                    total
            })


# ------------------------------------------------------------
# 31.5 MOSTRAR RESULTADOS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COMBINACIONES QUE REPRODUCEN MATRICULA_LIMPIA")
print("=" * 70)

print(
    "Cantidad de combinaciones exactas encontradas:",
    len(coincidencias)
)


if len(coincidencias) == 0:

    print(
        "\nNo se encontró ninguna combinación exacta."
    )

else:

    coincidencias_df = pd.DataFrame(
        coincidencias
    )

    coincidencias_df = (
        coincidencias_df
        .sort_values(
            [
                "cantidad_filas"
            ]
        )
        .reset_index(
            drop=True
        )
    )

    print(
        "\nResumen de combinaciones:"
    )

    print(
        coincidencias_df
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 31.6 ANALIZAR LA COMBINACIÓN MÁS SIMPLE
# ------------------------------------------------------------

if len(coincidencias) > 0:

    cantidad_minima = (
        coincidencias_df[
            "cantidad_filas"
        ]
        .min()
    )

    combinaciones_minimas = (
        coincidencias_df[
            coincidencias_df[
                "cantidad_filas"
            ]
            ==
            cantidad_minima
        ]
        .copy()
    )


    print("\n" + "=" * 70)
    print("COMBINACIONES CON MENOR CANTIDAD DE FILAS")
    print("=" * 70)

    print(
        combinaciones_minimas
        .to_string(
            index=False
        )
    )


    # --------------------------------------------------------
    # 31.7 DETALLE DE CADA COMBINACIÓN MÍNIMA
    # --------------------------------------------------------

    for numero, (_, combinacion) in enumerate(
        combinaciones_minimas.iterrows(),
        start=1
    ):

        ids = combinacion[
            "ids_filas"
        ]

        seleccion = (
            caso_31[
                caso_31[
                    "id_fila"
                ].isin(
                    ids
                )
            ]
            .copy()
        )


        print("\n" + "-" * 70)
        print(
            f"COMBINACIÓN MÍNIMA {numero}"
        )
        print("-" * 70)

        print(
            "Filas:",
            ids
        )

        print(
            "Total:",
            seleccion[
                "secundaria_7_12"
            ].sum(
                min_count=1
            )
        )


        columnas_detalle_31 = [
            "id_fila",
            col_partido
        ]

        # Mostrar todas las variables que podrían
        # explicar por qué esas filas fueron utilizadas.

        for columna in [
            "sector",
            "ambito",
            "multi_ini",
            "multi_pri",
            "multi_sec",
            "multinivel"
        ]:

            if columna in seleccion.columns:

                columnas_detalle_31.append(
                    columna
                )


        columnas_detalle_31 += [
            "_7",
            "_8",
            "_9",
            "_10",
            "_11",
            "_12",
            "_1314",
            "secundaria_7_12"
        ]


        print(
            seleccion[
                columnas_detalle_31
            ]
            .to_string(
                index=False
            )
        )


# ------------------------------------------------------------
# 31.8 COMPROBAR ESPECÍFICAMENTE FILAS 1, 2 Y 3
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COMPROBACIÓN DE FILAS 1 + 2 + 3")
print("=" * 70)

primeras_tres = (
    caso_31[
        caso_31[
            "id_fila"
        ]
        .isin(
            [1, 2, 3]
        )
    ]
    .copy()
)

total_primeras_tres = (
    primeras_tres[
        "secundaria_7_12"
    ]
    .sum(
        min_count=1
    )
)

print(
    primeras_tres[
        columnas_identificacion
    ]
    .to_string(
        index=False
    )
)

print(
    "\nTotal filas 1 + 2 + 3:",
    total_primeras_tres
)

print(
    "matricula_limpia:",
    objetivo_secundaria
)

print(
    "¿Coinciden?:",
    valores_iguales(
        total_primeras_tres,
        objetivo_secundaria
    )
)


# ------------------------------------------------------------
# 31.9 COMPARAR FILAS SELECCIONADAS VS NO SELECCIONADAS
# ------------------------------------------------------------

if len(coincidencias) > 0:

    primera_combinacion = (
        combinaciones_minimas
        .iloc[0][
            "ids_filas"
        ]
    )

    caso_31[
        "seleccionada"
    ] = (
        caso_31[
            "id_fila"
        ]
        .isin(
            primera_combinacion
        )
    )


    print("\n" + "=" * 70)
    print("SELECCIONADAS VS NO SELECCIONADAS")
    print("=" * 70)

    columnas_comparacion_31 = [
        "id_fila",
        "seleccionada",
        col_partido
    ]

    for columna in [
        "sector",
        "ambito",
        "multi_ini",
        "multi_pri",
        "multi_sec",
        "multinivel"
    ]:

        if columna in caso_31.columns:

            columnas_comparacion_31.append(
                columna
            )

    columnas_comparacion_31.append(
        "secundaria_7_12"
    )


    print(
        caso_31[
            columnas_comparacion_31
        ]
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 31.10 INSPECCIONAR COLUMNAS QUE CAMBIAN ENTRE LAS FILAS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COLUMNAS POTENCIALMENTE EXPLICATIVAS")
print("=" * 70)

# Buscamos columnas no numéricas o indicadores especiales
# que tengan más de un valor dentro de las 11 filas.

columnas_explicativas = []

for columna in caso_31.columns:

    if columna.startswith("_partido"):
        continue

    if columna in [
        "id_fila",
        "secundaria_7_12",
        "secundaria_7_1314",
        "seleccionada"
    ]:
        continue

    valores_unicos = (
        caso_31[
            columna
        ]
        .dropna()
        .astype(str)
        .unique()
    )

    if len(valores_unicos) > 1:

        columnas_explicativas.append(
            columna
        )


print(
    "Cantidad de columnas que varían entre las filas:",
    len(columnas_explicativas)
)

print(
    "Columnas:",
    columnas_explicativas
)


# ------------------------------------------------------------
# 31.11 MOSTRAR INDICADORES MULTINIVEL
# ------------------------------------------------------------

columnas_multi = [
    columna
    for columna in [
        "multi_ini",
        "multi_pri",
        "multi_sec",
        "multinivel"
    ]
    if columna in caso_31.columns
]


if columnas_multi:

    print("\n" + "=" * 70)
    print("INDICADORES MULTINIVEL")
    print("=" * 70)

    columnas_multi_mostrar = (
        [
            "id_fila",
            "seleccionada"
        ]
        +
        columnas_multi
        +
        [
            "secundaria_7_12"
        ]
    )

    print(
        caso_31[
            columnas_multi_mostrar
        ]
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 31.12 INTERPRETACIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

print(
    """
Este análisis busca qué combinación de las filas originales de
25 DE MAYO - 2012 reproduce exactamente el valor de matrícula
secundaria presente en matricula_limpia.csv.

Encontrar una combinación exacta permite identificar qué
registros de la fuente podrían haber sido utilizados para
construir el indicador.

Sin embargo, una coincidencia matemática no demuestra todavía
que esa sea la regla metodológica correcta.

El siguiente paso será analizar qué característica estructural
distingue a las filas seleccionadas de las restantes y comprobar
si esa misma regla reproduce matricula_limpia en otros partidos
y años.

Solo después de validar esa regla globalmente se podrá determinar
si existe algún problema real en matricula_limpia o si las
diferencias anteriores fueron generadas por una agregación
incorrecta durante la auditoría.

IMPORTANTE:
NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)


print("=" * 70)
print("DIAGNÓSTICO 31 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 32. IDENTIFICAR LA ESTRUCTURA DE LAS FILAS QUE EXPLICAN
#     MATRICULA_LIMPIA
# ============================================================

print("\n" + "=" * 70)
print("32. ESTRUCTURA DE LAS FILAS QUE EXPLICAN MATRICULA_LIMPIA")
print("=" * 70)

# Objetivo:
# En el punto 31 se comprobó que, para 25 DE MAYO - 2012,
# solamente las filas 1 + 2 + 3 reproducen exactamente la
# matrícula secundaria de matricula_limpia:
#
# 659 + 1845 + 629 = 3133
#
# Ahora queremos identificar qué característica estructural
# diferencia esas filas de las filas 4 a 11.
#
# Se analizarán especialmente las familias:
#
# - columnas generales: _*
# - v_*
# - r_*
# - s_*
# - _sec*
# - indicadores multi_*
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 32.1 CONTROLES
# ------------------------------------------------------------

if "caso_31" not in globals():
    raise ValueError(
        "No existe caso_31. Ejecutá primero el punto 31."
    )

caso_32 = caso_31.copy()

if "seleccionada" not in caso_32.columns:
    caso_32["seleccionada"] = (
        caso_32["id_fila"].isin([1, 2, 3])
    )


# ------------------------------------------------------------
# 32.2 FUNCIÓN AUXILIAR PARA CONVERTIR VALORES
# ------------------------------------------------------------

def convertir_numerico_32(serie):

    return pd.to_numeric(
        serie.astype(str)
        .str.strip()
        .replace({
            "": np.nan,
            "nan": np.nan,
            "None": np.nan
        }),
        errors="coerce"
    )


# ------------------------------------------------------------
# 32.3 IDENTIFICAR FAMILIAS DE COLUMNAS
# ------------------------------------------------------------

columnas_v = [
    c for c in caso_32.columns
    if c.startswith("v_")
]

columnas_r = [
    c for c in caso_32.columns
    if c.startswith("r_")
]

columnas_s = [
    c for c in caso_32.columns
    if c.startswith("s_")
]

columnas_sec = [
    c for c in caso_32.columns
    if c.startswith("_sec")
]

columnas_multi_32 = [
    c for c in [
        "multi_ini",
        "multi_pri",
        "multi_sec",
        "multinivel"
    ]
    if c in caso_32.columns
]


print("\n" + "=" * 70)
print("FAMILIAS DE COLUMNAS DETECTADAS")
print("=" * 70)

print("Columnas v_*:", len(columnas_v))
print("Columnas r_*:", len(columnas_r))
print("Columnas s_*:", len(columnas_s))
print("Columnas _sec*:", len(columnas_sec))
print("Columnas multi_*:", len(columnas_multi_32))


# ------------------------------------------------------------
# 32.4 CALCULAR TOTALES POR FAMILIA PARA CADA FILA
# ------------------------------------------------------------

familias = {
    "v": columnas_v,
    "r": columnas_r,
    "s": columnas_s,
    "sec": columnas_sec
}

for nombre_familia, columnas in familias.items():

    columnas_validas = []

    for columna in columnas:

        caso_32[columna] = convertir_numerico_32(
            caso_32[columna]
        )

        columnas_validas.append(columna)

    if columnas_validas:

        caso_32[
            f"total_{nombre_familia}"
        ] = (
            caso_32[
                columnas_validas
            ]
            .sum(
                axis=1,
                min_count=1
            )
        )

        caso_32[
            f"cantidad_{nombre_familia}_con_datos"
        ] = (
            caso_32[
                columnas_validas
            ]
            .notna()
            .sum(axis=1)
        )

    else:

        caso_32[
            f"total_{nombre_familia}"
        ] = np.nan

        caso_32[
            f"cantidad_{nombre_familia}_con_datos"
        ] = 0


# ------------------------------------------------------------
# 32.5 RESUMEN GENERAL POR FILA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN ESTRUCTURAL POR FILA")
print("=" * 70)

columnas_resumen_32 = [
    "id_fila",
    "seleccionada",
    col_partido
]

for columna in [
    "sector",
    "ambito"
]:
    if columna in caso_32.columns:
        columnas_resumen_32.append(columna)

columnas_resumen_32 += [
    "secundaria_7_12",
    "total_v",
    "cantidad_v_con_datos",
    "total_r",
    "cantidad_r_con_datos",
    "total_s",
    "cantidad_s_con_datos",
    "total_sec",
    "cantidad_sec_con_datos"
]

columnas_resumen_32 += columnas_multi_32

print(
    caso_32[
        columnas_resumen_32
    ]
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 32.6 ANALIZAR ESPECÍFICAMENTE EDADES 7 A 12
#      EN CADA FAMILIA
# ------------------------------------------------------------

edades_secundaria_32 = [
    "7", "8", "9", "10", "11", "12"
]

familias_edades = {
    "general": [
        f"_{edad}"
        for edad in edades_secundaria_32
    ],

    "v": [
        f"v_{edad}"
        for edad in edades_secundaria_32
    ],

    "r": [
        f"r_{edad}"
        for edad in edades_secundaria_32
    ],

    "s": [
        f"s_{edad}"
        for edad in edades_secundaria_32
    ],

    "sec": [
        f"_sec{edad}"
        for edad in edades_secundaria_32
    ]
}


for familia, columnas in familias_edades.items():

    columnas_existentes = [
        c for c in columnas
        if c in caso_32.columns
    ]

    for columna in columnas_existentes:

        caso_32[columna] = convertir_numerico_32(
            caso_32[columna]
        )

    if columnas_existentes:

        caso_32[
            f"secundaria_familia_{familia}"
        ] = (
            caso_32[
                columnas_existentes
            ]
            .sum(
                axis=1,
                min_count=1
            )
        )

    else:

        caso_32[
            f"secundaria_familia_{familia}"
        ] = np.nan


print("\n" + "=" * 70)
print("EDADES 7 A 12 SEGÚN FAMILIA DE COLUMNAS")
print("=" * 70)

columnas_familias_32 = [
    "id_fila",
    "seleccionada"
]

for columna in [
    "sector",
    "ambito"
]:
    if columna in caso_32.columns:
        columnas_familias_32.append(columna)

columnas_familias_32 += [
    "secundaria_familia_general",
    "secundaria_familia_v",
    "secundaria_familia_r",
    "secundaria_familia_s",
    "secundaria_familia_sec"
]

print(
    caso_32[
        columnas_familias_32
    ]
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 32.7 MOSTRAR DETALLE DE LAS FILAS 1, 2 Y 3
# ------------------------------------------------------------

seleccionadas_32 = (
    caso_32[
        caso_32["seleccionada"]
    ]
    .copy()
)

no_seleccionadas_32 = (
    caso_32[
        ~caso_32["seleccionada"]
    ]
    .copy()
)


print("\n" + "=" * 70)
print("FILAS QUE REPRODUCEN MATRICULA_LIMPIA")
print("=" * 70)

print(
    seleccionadas_32[
        columnas_resumen_32
    ]
    .to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("FILAS QUE NO FORMAN PARTE DEL VALOR DE MATRICULA_LIMPIA")
print("=" * 70)

print(
    no_seleccionadas_32[
        columnas_resumen_32
    ]
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 32.8 COMPARAR PATRONES DE DATOS PRESENTES / AUSENTES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PATRONES DE PRESENCIA DE DATOS")
print("=" * 70)

columnas_estructura = (
    columnas_v
    + columnas_r
    + columnas_s
    + columnas_sec
)

patrones = []

for _, fila in caso_32.iterrows():

    registro = {
        "id_fila": fila["id_fila"],
        "seleccionada": fila["seleccionada"]
    }

    for familia, columnas in familias.items():

        columnas_existentes = [
            c for c in columnas
            if c in caso_32.columns
        ]

        if columnas_existentes:

            valores = fila[
                columnas_existentes
            ]

            valores_num = pd.to_numeric(
                valores,
                errors="coerce"
            )

            registro[
                f"{familia}_tiene_datos"
            ] = bool(
                valores_num.notna().any()
            )

            registro[
                f"{familia}_tiene_valores_positivos"
            ] = bool(
                (valores_num.fillna(0) != 0).any()
            )

        else:

            registro[
                f"{familia}_tiene_datos"
            ] = False

            registro[
                f"{familia}_tiene_valores_positivos"
            ] = False

    patrones.append(registro)


patrones_32 = pd.DataFrame(
    patrones
)

print(
    patrones_32
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 32.9 BUSCAR COLUMNAS CON PATRÓN PERFECTO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COLUMNAS QUE PODRÍAN EXPLICAR LA SELECCIÓN")
print("=" * 70)

# Buscamos columnas cuya presencia/ausencia pueda separar
# perfectamente las filas 1-3 de las filas 4-11.

columnas_patron_perfecto = []

for columna in caso_32.columns:

    if columna in [
        "id_fila",
        "seleccionada",
        "_partido_norm",
        "secundaria_7_12",
        "secundaria_7_1314"
    ]:
        continue

    serie = caso_32[columna]

    # Patrón de presencia
    presencia = (
        serie
        .replace("", np.nan)
        .notna()
    )

    seleccion = caso_32[
        "seleccionada"
    ]

    # Presente únicamente en seleccionadas
    if (
        presencia[seleccion].all()
        and
        (~presencia[~seleccion]).all()
    ):

        columnas_patron_perfecto.append({
            "columna": columna,
            "patron":
                "PRESENTE SOLO EN SELECCIONADAS"
        })

    # Ausente únicamente en seleccionadas
    elif (
        (~presencia[seleccion]).all()
        and
        presencia[~seleccion].all()
    ):

        columnas_patron_perfecto.append({
            "columna": columna,
            "patron":
                "AUSENTE SOLO EN SELECCIONADAS"
        })


patron_perfecto_32 = pd.DataFrame(
    columnas_patron_perfecto
)

if patron_perfecto_32.empty:

    print(
        "No se encontró una columna cuya simple presencia o "
        "ausencia separe perfectamente ambos grupos."
    )

else:

    print(
        patron_perfecto_32
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 32.10 BUSCAR COLUMNAS NUMÉRICAS QUE SEAN CERO
#       EN UN GRUPO Y NO EN EL OTRO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PATRONES NUMÉRICOS CERO / NO CERO")
print("=" * 70)

resultados_cero_32 = []

for columna in caso_32.columns:

    serie_num = pd.to_numeric(
        caso_32[columna],
        errors="coerce"
    )

    if serie_num.notna().sum() == 0:
        continue

    seleccion = caso_32[
        "seleccionada"
    ]

    sel = (
        serie_num[
            seleccion
        ]
        .fillna(0)
    )

    no_sel = (
        serie_num[
            ~seleccion
        ]
        .fillna(0)
    )

    # Seleccionadas todas cero, resto tiene algún valor
    if (
        (sel == 0).all()
        and
        (no_sel != 0).any()
    ):

        resultados_cero_32.append({
            "columna": columna,
            "patron":
                "SELECCIONADAS = 0; RESTO TIENE VALORES"
        })

    # Seleccionadas tienen algún valor y resto todo cero
    elif (
        (sel != 0).any()
        and
        (no_sel == 0).all()
    ):

        resultados_cero_32.append({
            "columna": columna,
            "patron":
                "SELECCIONADAS TIENEN VALORES; RESTO = 0"
        })


patrones_cero_df_32 = pd.DataFrame(
    resultados_cero_32
)

if patrones_cero_df_32.empty:

    print(
        "No se encontraron patrones simples cero/no cero."
    )

else:

    print(
        patrones_cero_df_32
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 32.11 DETALLE DE COLUMNAS _SEC PARA 7 A 12
# ------------------------------------------------------------

columnas_sec_7_12 = [
    f"_sec{edad}"
    for edad in edades_secundaria_32
    if f"_sec{edad}" in caso_32.columns
]

if columnas_sec_7_12:

    print("\n" + "=" * 70)
    print("DETALLE DE COLUMNAS _SEC7 A _SEC12")
    print("=" * 70)

    columnas_detalle_sec = [
        "id_fila",
        "seleccionada"
    ]

    if "sector" in caso_32.columns:
        columnas_detalle_sec.append("sector")

    if "ambito" in caso_32.columns:
        columnas_detalle_sec.append("ambito")

    columnas_detalle_sec += (
        columnas_sec_7_12
        +
        [
            "secundaria_familia_sec",
            "secundaria_7_12"
        ]
    )

    print(
        caso_32[
            columnas_detalle_sec
        ]
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 32.12 DETALLE DE COLUMNAS V, R Y S PARA 7 A 12
# ------------------------------------------------------------

for familia in ["v", "r", "s"]:

    columnas_detalle = [
        f"{familia}_{edad}"
        for edad in edades_secundaria_32
        if f"{familia}_{edad}" in caso_32.columns
    ]

    if not columnas_detalle:
        continue

    print("\n" + "=" * 70)
    print(
        f"DETALLE DE COLUMNAS {familia.upper()}_7 A "
        f"{familia.upper()}_12"
    )
    print("=" * 70)

    columnas_mostrar = [
        "id_fila",
        "seleccionada"
    ]

    if "sector" in caso_32.columns:
        columnas_mostrar.append("sector")

    if "ambito" in caso_32.columns:
        columnas_mostrar.append("ambito")

    columnas_mostrar += columnas_detalle

    columnas_mostrar.append(
        f"secundaria_familia_{familia}"
    )

    print(
        caso_32[
            columnas_mostrar
        ]
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 32.13 CONCLUSIÓN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

print(
    """
El punto 31 confirmó que existe una única combinación de filas
que reproduce exactamente la matrícula secundaria de
25 DE MAYO - 2012: las filas 1, 2 y 3.

Este punto analiza la estructura interna de esas filas y la
compara con las restantes.

El objetivo no es asumir que las filas 1 a 3 son correctas
simplemente porque su suma coincide, sino identificar una regla
estructural presente en las variables originales que explique
por qué esas filas forman parte del indicador y las restantes no.

Las familias v_*, r_*, s_* y _sec* se analizan por separado
porque pueden representar componentes distintos de la fuente
original y explicar el exceso observado cuando se sumaron todas
las filas indiscriminadamente en el punto 29.

La regla que surja de este diagnóstico todavía deberá validarse
en otros partidos y años antes de considerarla una regla general
de construcción de matricula_limpia.

IMPORTANTE:
NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)

print("=" * 70)
print("DIAGNÓSTICO 32 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ============================================================
# 33. IDENTIFICAR LA ESTRUCTURA DE BLOQUES DEL ARCHIVO ORIGINAL
# ============================================================

print("\n" + "=" * 70)
print("33. IDENTIFICAR LA ESTRUCTURA DE BLOQUES DEL ARCHIVO ORIGINAL")
print("=" * 70)

# Objetivo:
# El punto 31 mostró que, para 25 DE MAYO - 2012,
# matricula_limpia = 3133 se reproduce exactamente con
# las primeras tres filas del partido:
#
#   fila 1 = Estatal - Rural  = 659
#   fila 2 = Estatal - Urbano = 1845
#   fila 3 = Privado - Urbano = 629
#
# Sin embargo, después aparecen otras filas con combinaciones
# similares de sector y ámbito.
#
# El objetivo de este punto es investigar si el archivo original
# está organizado en BLOQUES de registros y si existe alguna
# característica estructural que permita identificar qué bloque
# fue utilizado para construir matricula_limpia.
#
# IMPORTANTE:
# NO se modifica ningún dataset.
# NO se realiza ninguna imputación.
# NO se guarda ningún archivo.


# ------------------------------------------------------------
# 33.1 PARTIR DEL CASO YA CARGADO EN LOS PUNTOS ANTERIORES
# ------------------------------------------------------------

caso_33 = caso.copy()

# Conservamos explícitamente el orden original de las filas
caso_33 = caso_33.reset_index().rename(
    columns={
        "index": "indice_archivo_original"
    }
)

caso_33["id_fila_33"] = range(
    1,
    len(caso_33) + 1
)


# ------------------------------------------------------------
# 33.2 COLUMNAS GENERALES DE MATRÍCULA
# ------------------------------------------------------------

columnas_generales = [
    "lactantes",
    "deambulantes",
    "s2",
    "s3",
    "s4",
    "s5",
    "_1",
    "_2",
    "_3",
    "_4",
    "_5",
    "_6",
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12",
    "_1314",
    "_snu"
]

columnas_generales = [
    c for c in columnas_generales
    if c in caso_33.columns
]


# ------------------------------------------------------------
# 33.3 FAMILIAS DE COLUMNAS
# ------------------------------------------------------------

columnas_v_33 = [
    c for c in caso_33.columns
    if str(c).startswith("v_")
]

columnas_r_33 = [
    c for c in caso_33.columns
    if str(c).startswith("r_")
]

columnas_s_33 = [
    c for c in caso_33.columns
    if str(c).startswith("s_")
]

columnas_sec_33 = [
    c for c in caso_33.columns
    if str(c).startswith("_sec")
]

columnas_multi_33 = [
    c for c in [
        "multi_ini",
        "multi_pri",
        "multi_sec",
        "multinivel"
    ]
    if c in caso_33.columns
]


# ------------------------------------------------------------
# 33.4 CONVERTIR A NUMÉRICO
# ------------------------------------------------------------

columnas_numericas_33 = list(
    dict.fromkeys(
        columnas_generales
        + columnas_v_33
        + columnas_r_33
        + columnas_s_33
        + columnas_sec_33
        + columnas_multi_33
    )
)

for col in columnas_numericas_33:

    caso_33[col] = pd.to_numeric(
        caso_33[col],
        errors="coerce"
    )


# ------------------------------------------------------------
# 33.5 CALCULAR TOTALES POR FAMILIA
# ------------------------------------------------------------

def suma_familia_33(df, columnas):

    if not columnas:
        return pd.Series(
            np.nan,
            index=df.index
        )

    return df[columnas].sum(
        axis=1,
        min_count=1
    )


caso_33["total_general"] = suma_familia_33(
    caso_33,
    columnas_generales
)

caso_33["total_v"] = suma_familia_33(
    caso_33,
    columnas_v_33
)

caso_33["total_r"] = suma_familia_33(
    caso_33,
    columnas_r_33
)

caso_33["total_s"] = suma_familia_33(
    caso_33,
    columnas_s_33
)

caso_33["total_sec"] = suma_familia_33(
    caso_33,
    columnas_sec_33
)


# ------------------------------------------------------------
# 33.6 SECUNDARIA GENERAL
# ------------------------------------------------------------

cols_secundaria_33 = [
    c for c in [
        "_7",
        "_8",
        "_9",
        "_10",
        "_11",
        "_12"
    ]
    if c in caso_33.columns
]

caso_33["secundaria_7_12_33"] = (
    caso_33[
        cols_secundaria_33
    ]
    .sum(
        axis=1,
        min_count=1
    )
)


# ------------------------------------------------------------
# 33.7 MARCAR LAS FILAS QUE REPRODUCEN MATRICULA_LIMPIA
# ------------------------------------------------------------

caso_33["seleccionada_3133"] = (
    caso_33["id_fila_33"].isin(
        [1, 2, 3]
    )
)


# ------------------------------------------------------------
# 33.8 MOSTRAR ORDEN ORIGINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ORDEN ORIGINAL DE LAS FILAS")
print("=" * 70)

columnas_orden_33 = [
    "id_fila_33",
    "indice_archivo_original",
    "departamento",
    "sector",
    "ambito",
    "seleccionada_3133",
    "secundaria_7_12_33"
]

for c in columnas_multi_33:

    if c not in columnas_orden_33:
        columnas_orden_33.append(c)

print(
    caso_33[
        columnas_orden_33
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 33.9 DETECTAR REPETICIONES SECTOR + ÁMBITO
# ------------------------------------------------------------

caso_33[
    "numero_repeticion_sector_ambito"
] = (
    caso_33
    .groupby(
        [
            "sector",
            "ambito"
        ]
    )
    .cumcount()
    + 1
)


print("\n" + "=" * 70)
print("REPETICIONES DE SECTOR + ÁMBITO")
print("=" * 70)

columnas_repeticion_33 = [
    "id_fila_33",
    "sector",
    "ambito",
    "numero_repeticion_sector_ambito",
    "seleccionada_3133",
    "secundaria_7_12_33"
]

print(
    caso_33[
        columnas_repeticion_33
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 33.10 RESUMEN DE COMBINACIONES
# ------------------------------------------------------------

resumen_combinaciones_33 = (
    caso_33
    .groupby(
        [
            "sector",
            "ambito"
        ],
        dropna=False
    )
    .agg(
        cantidad_filas=(
            "id_fila_33",
            "size"
        ),

        cantidad_seleccionadas=(
            "seleccionada_3133",
            "sum"
        ),

        secundaria_total=(
            "secundaria_7_12_33",
            "sum"
        )
    )
    .reset_index()
)


print("\n" + "=" * 70)
print("RESUMEN POR SECTOR Y ÁMBITO")
print("=" * 70)

print(
    resumen_combinaciones_33
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 33.11 COMPARAR PRIMERA APARICIÓN VS RESTO
# ------------------------------------------------------------

caso_33[
    "primera_aparicion_sector_ambito"
] = (
    caso_33[
        "numero_repeticion_sector_ambito"
    ]
    ==
    1
)


print("\n" + "=" * 70)
print("¿LAS FILAS SELECCIONADAS SON PRIMERAS APARICIONES?")
print("=" * 70)

print(
    caso_33[
        [
            "id_fila_33",
            "sector",
            "ambito",
            "numero_repeticion_sector_ambito",
            "primera_aparicion_sector_ambito",
            "seleccionada_3133",
            "secundaria_7_12_33"
        ]
    ]
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 33.12 SUMAR LAS PRIMERAS APARICIONES
# ------------------------------------------------------------

primeras_apariciones_33 = (
    caso_33[
        caso_33[
            "primera_aparicion_sector_ambito"
        ]
    ]
    .copy()
)

total_primeras_apariciones_33 = (
    primeras_apariciones_33[
        "secundaria_7_12_33"
    ]
    .sum()
)


print("\n" + "=" * 70)
print("SUMA DE PRIMERAS APARICIONES SECTOR + ÁMBITO")
print("=" * 70)

print(
    primeras_apariciones_33[
        [
            "id_fila_33",
            "sector",
            "ambito",
            "secundaria_7_12_33"
        ]
    ]
    .to_string(
        index=False
    )
)

print(
    "\nTotal primeras apariciones:",
    total_primeras_apariciones_33
)
# Valor observado en matricula_limpia para 25 DE MAYO - 2012
valor_objetivo = 3133.0
print(
    "Valor matricula_limpia:",
    valor_objetivo
)

print(
    "¿Coinciden?:",
    np.isclose(
        total_primeras_apariciones_33,
        valor_objetivo
    )
)


# ------------------------------------------------------------
# 33.13 COMPARAR TOTALES DE FAMILIAS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COMPARACIÓN DE FAMILIAS POR FILA")
print("=" * 70)

columnas_familias_33 = [
    "id_fila_33",
    "seleccionada_3133",
    "sector",
    "ambito",
    "numero_repeticion_sector_ambito",
    "secundaria_7_12_33",
    "total_general",
    "total_v",
    "total_r",
    "total_s",
    "total_sec"
]

print(
    caso_33[
        columnas_familias_33
    ]
    .to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 33.14 ANALIZAR CAMBIOS ENTRE FILAS CON MISMO SECTOR/ÁMBITO
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SECUENCIA DE REPETICIONES POR SECTOR Y ÁMBITO")
print("=" * 70)

for (
    sector_33,
    ambito_33
), grupo_33 in caso_33.groupby(
    [
        "sector",
        "ambito"
    ],
    dropna=False
):

    print("\n" + "-" * 70)

    print(
        f"SECTOR: {sector_33} | "
        f"ÁMBITO: {ambito_33}"
    )

    print("-" * 70)

    print(
        grupo_33[
            [
                "id_fila_33",
                "numero_repeticion_sector_ambito",
                "seleccionada_3133",
                "secundaria_7_12_33",
                "total_v",
                "total_r",
                "total_s",
                "total_sec"
            ]
        ]
        .to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 33.15 BUSCAR COLUMNAS QUE CAMBIEN ENTRE REPETICIONES
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COLUMNAS CON POSIBLE INFORMACIÓN DE BLOQUE")
print("=" * 70)

# Excluimos columnas puramente numéricas de matrícula porque
# sabemos que naturalmente cambian entre las filas.
#
# Buscamos especialmente columnas categóricas adicionales
# que pudieran explicar la existencia de varios bloques.

columnas_excluir_33 = set(
    columnas_numericas_33
    + [
        "_partido_norm",
        "_total_7_12",
        "secundaria_7_12",
        "secundaria_7_12_33",
        "total_general",
        "total_v",
        "total_r",
        "total_s",
        "total_sec",
        "id_fila_33",
        "indice_archivo_original",
        "seleccionada_3133",
        "numero_repeticion_sector_ambito",
        "primera_aparicion_sector_ambito"
    ]
)

columnas_categoricas_extra_33 = [
    c for c in caso_33.columns
    if c not in columnas_excluir_33
]


if columnas_categoricas_extra_33:

    print(
        "Columnas categóricas/no numéricas disponibles:"
    )

    for col in columnas_categoricas_extra_33:

        valores = (
            caso_33[col]
            .astype(str)
            .replace(
                {
                    "nan": "<NA>",
                    "None": "<NA>"
                }
            )
            .unique()
            .tolist()
        )

        print(
            f"\n{col}:"
        )

        print(
            valores
        )

else:

    print(
        "No se detectaron columnas categóricas adicionales."
    )


# ------------------------------------------------------------
# 33.16 COMPROBAR HIPÓTESIS DE PRIMERA APARICIÓN
# ------------------------------------------------------------

coincide_hipotesis_33 = np.isclose(
    total_primeras_apariciones_33,
    valor_objetivo
)


print("\n" + "=" * 70)
print("RESULTADO DE LA HIPÓTESIS")
print("=" * 70)


if coincide_hipotesis_33:

    print(
        """
En 25 DE MAYO - 2012, tomar solamente la primera aparición
de cada combinación sector-ámbito reproduce exactamente el
valor de matrícula secundaria presente en matricula_limpia.csv.

Esto constituye una pista importante sobre la estructura del
archivo original.

Sin embargo, NO demuestra todavía que "primera aparición" sea
la regla metodológica real.

Es posible que el orden de las filas esté reflejando bloques
correspondientes a otra clasificación que no aparece de forma
explícita en las columnas actualmente analizadas.

Por eso, esta hipótesis deberá probarse en otros partidos y años
antes de utilizarla para reconstruir la serie.
"""
    )

else:

    print(
        """
La hipótesis de tomar solamente la primera aparición de cada
combinación sector-ámbito NO reproduce matricula_limpia.

Por lo tanto, las filas 1, 2 y 3 deben estar siendo distinguidas
por otra característica estructural del archivo original.

Será necesario continuar investigando la organización de los
registros antes de establecer una regla general.
"""
    )


# ------------------------------------------------------------
# 33.17 INTERPRETACIÓN FINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

print(
    """
Este diagnóstico estudia el orden y la repetición de las filas
originales de 25 DE MAYO - 2012.

El análisis anterior demostró que las filas 1, 2 y 3 suman
exactamente 3.133, que es el valor presente en
matricula_limpia.csv.

Ahora se analiza si esas filas corresponden a la primera
aparición de cada combinación sector-ámbito y si las filas
posteriores pertenecen a bloques diferentes de información.

El objetivo es encontrar una regla estructural reproducible,
no simplemente una combinación matemática que coincida por
casualidad.

IMPORTANTE:
Todavía NO se considera validada ninguna regla general.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.csv.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
"""
)


print("=" * 70)
print("DIAGNÓSTICO 33 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)
# =============================================================================
# 34. VALIDAR HIPÓTESIS DE PRIMERA APARICIÓN EN TODO 2012
# =============================================================================

print("\n" + "=" * 70)
print("34. VALIDAR HIPÓTESIS DE PRIMERA APARICIÓN EN TODO 2012")
print("=" * 70)

# -------------------------------------------------------------------------
# 34.1 CARGAR FUENTE ORIGINAL 2012
# -------------------------------------------------------------------------

ruta_2012_34 = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/necesarios "
    "/educacion/Matriculas 2011 - 2025/2012 Matricula - agregada(in).csv"
)

if not os.path.exists(ruta_2012_34):
    raise FileNotFoundError(
        f"No se encontró el archivo original 2012:\n{ruta_2012_34}"
    )

# El archivo 2012 no está separado por comas.
# Detectamos automáticamente el separador correcto.
fuente_2012_34 = pd.read_csv(
    ruta_2012_34,
    encoding="latin1",
    sep=None,
    engine="python"
)

# Limpiar posibles espacios o caracteres extraños
# en los nombres de las columnas.
fuente_2012_34.columns = (
    fuente_2012_34.columns
    .astype(str)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

print("\nArchivo 2012 cargado correctamente.")
print("Dimensiones:", fuente_2012_34.shape)

print("\nColumnas originales detectadas:")
print(fuente_2012_34.columns.tolist())


# -------------------------------------------------------------------------
# 34.2 NORMALIZAR DEPARTAMENTO, SECTOR Y ÁMBITO
# -------------------------------------------------------------------------

fuente_2012_34 = fuente_2012_34.copy()


# Normalizar nombres de columnas para poder encontrarlas
# aunque tengan mayúsculas, espacios o tildes.
def normalizar_nombre_columna_34(nombre):

    nombre = str(nombre).strip().lower()

    nombre = (
        nombre
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )

    return nombre


mapa_columnas_34 = {
    normalizar_nombre_columna_34(c): c
    for c in fuente_2012_34.columns
}


col_departamento_fuente_34 = (
    mapa_columnas_34.get("departamento")
)

col_sector_fuente_34 = (
    mapa_columnas_34.get("sector")
)

col_ambito_fuente_34 = (
    mapa_columnas_34.get("ambito")
)


print("\nColumnas territoriales detectadas en fuente 2012:")

print(
    "Departamento:",
    col_departamento_fuente_34
)

print(
    "Sector:",
    col_sector_fuente_34
)

print(
    "Ámbito:",
    col_ambito_fuente_34
)


if col_departamento_fuente_34 is None:

    raise KeyError(
        "No se encontró la columna departamento. "
        f"Columnas disponibles: "
        f"{fuente_2012_34.columns.tolist()}"
    )


if col_sector_fuente_34 is None:

    raise KeyError(
        "No se encontró la columna sector. "
        f"Columnas disponibles: "
        f"{fuente_2012_34.columns.tolist()}"
    )


if col_ambito_fuente_34 is None:

    raise KeyError(
        "No se encontró la columna ambito. "
        f"Columnas disponibles: "
        f"{fuente_2012_34.columns.tolist()}"
    )


# Renombramos estas columnas para que el resto del
# punto 34 pueda seguir trabajando normalmente.
fuente_2012_34 = fuente_2012_34.rename(
    columns={
        col_departamento_fuente_34:
            "departamento",

        col_sector_fuente_34:
            "sector",

        col_ambito_fuente_34:
            "ambito"
    }
)


for col in [
    "departamento",
    "sector",
    "ambito"
]:

    fuente_2012_34[col] = (
        fuente_2012_34[col]
        .astype(str)
        .str.strip()
        .str.upper()
    )

# Guardamos el orden real del archivo.
fuente_2012_34["indice_original_34"] = fuente_2012_34.index


# -------------------------------------------------------------------------
# 34.3 CALCULAR MATRÍCULA SECUNDARIA _7 A _12
# -------------------------------------------------------------------------

columnas_secundaria_34 = [
    "_7", "_8", "_9", "_10", "_11", "_12"
]

for col in columnas_secundaria_34:
    fuente_2012_34[col] = pd.to_numeric(
        fuente_2012_34[col],
        errors="coerce"
    )

fuente_2012_34["secundaria_7_12_34"] = (
    fuente_2012_34[columnas_secundaria_34]
    .fillna(0)
    .sum(axis=1)
)


# -------------------------------------------------------------------------
# 34.4 IDENTIFICAR PRIMERA APARICIÓN DE SECTOR + ÁMBITO
#      DENTRO DE CADA DEPARTAMENTO
# -------------------------------------------------------------------------

fuente_2012_34["numero_repeticion_34"] = (
    fuente_2012_34
    .groupby(
        ["departamento", "sector", "ambito"],
        dropna=False
    )
    .cumcount()
    + 1
)

fuente_2012_34["primera_aparicion_34"] = (
    fuente_2012_34["numero_repeticion_34"] == 1
)

primeras_34 = fuente_2012_34[
    fuente_2012_34["primera_aparicion_34"]
].copy()


# -------------------------------------------------------------------------
# 34.5 SUMAR LAS PRIMERAS APARICIONES POR DEPARTAMENTO
# -------------------------------------------------------------------------

hipotesis_2012_34 = (
    primeras_34
    .groupby(
        "departamento",
        as_index=False
    )["secundaria_7_12_34"]
    .sum()
    .rename(
        columns={
            "secundaria_7_12_34":
                "secundaria_hipotesis_primera_aparicion"
        }
    )
)

print("\n" + "=" * 70)
print("RESULTADO DE LA HIPÓTESIS POR DEPARTAMENTO")
print("=" * 70)

print(
    hipotesis_2012_34
    .sort_values("departamento")
    .to_string(index=False)
)


# -------------------------------------------------------------------------
# 34.6 OBTENER LOS VALORES REALES DE MATRICULA_LIMPIA PARA 2012
# -------------------------------------------------------------------------
print('34.6 OBTENER LOS VALORES REALES DE MATRICULA_LIMPIA PARA 2012')
ruta_matricula_limpia_34 = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios/matricula_limpia.csv"
)

if not os.path.exists(ruta_matricula_limpia_34):
    raise FileNotFoundError(
        f"No se encontró matricula_limpia.csv:\n"
        f"{ruta_matricula_limpia_34}"
    )

try:
    matricula_limpia = pd.read_csv(
        ruta_matricula_limpia_34,
        encoding="utf-8"
    )
except UnicodeDecodeError:
    matricula_limpia = pd.read_csv(
        ruta_matricula_limpia_34,
        encoding="latin1"
    )

matricula_limpia.columns = (
    matricula_limpia.columns
    .astype(str)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

print("\nmatricula_limpia.csv cargado correctamente.")
print("Dimensiones:", matricula_limpia.shape)


print("\n" + "=" * 70)
print("LOCALIZAR COLUMNAS EN MATRICULA_LIMPIA")
print("=" * 70)

print("Columnas disponibles:")
print(matricula_limpia.columns.tolist())

def buscar_columna_34(df, candidatos):
    """
    Busca una columna sin depender de mayúsculas/minúsculas.
    """
    mapa = {
        str(c).strip().lower(): c
        for c in df.columns
    }

    for candidato in candidatos:
        clave = candidato.strip().lower()

        if clave in mapa:
            return mapa[clave]

    return None


col_anio_34 = buscar_columna_34(
    matricula_limpia,
    ["anio", "año", "year"]
)

col_partido_34 = buscar_columna_34(
    matricula_limpia,
    [
        "partido",
        "departamento",
        "municipio"
    ]
)

col_nivel_34 = buscar_columna_34(
    matricula_limpia,
    [
        "nivel",
        "nivel_educativo",
        "nivel educativo"
    ]
)

col_matricula_34 = buscar_columna_34(
    matricula_limpia,
    [
        "matricula",
        "matrícula",
        "valor",
        "cantidad"
    ]
)

print("\nColumnas detectadas:")
print("Año:", col_anio_34)
print("Partido/departamento:", col_partido_34)
print("Nivel:", col_nivel_34)
print("Matrícula:", col_matricula_34)

if col_anio_34 is None:
    raise KeyError(
        "No se pudo identificar la columna de año en matricula_limpia."
    )

if col_partido_34 is None:
    raise KeyError(
        "No se pudo identificar la columna territorial en matricula_limpia."
    )

if col_matricula_34 is None:
    raise KeyError(
        "No se pudo identificar la columna de matrícula en matricula_limpia."
    )


# -------------------------------------------------------------------------
# 34.7 FILTRAR 2012 Y SECUNDARIA
# -------------------------------------------------------------------------

matricula_2012_34 = matricula_limpia.copy()

matricula_2012_34[col_anio_34] = pd.to_numeric(
    matricula_2012_34[col_anio_34],
    errors="coerce"
)

matricula_2012_34 = matricula_2012_34[
    matricula_2012_34[col_anio_34] == 2012
].copy()

matricula_2012_34[col_partido_34] = (
    matricula_2012_34[col_partido_34]
    .astype(str)
    .str.strip()
    .str.upper()
)

if col_nivel_34 is not None:

    matricula_2012_34[col_nivel_34] = (
        matricula_2012_34[col_nivel_34]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    matricula_2012_34 = matricula_2012_34[
        matricula_2012_34[col_nivel_34]
        .str.contains(
            "SECUND",
            case=False,
            na=False
        )
    ].copy()

matricula_2012_34[col_matricula_34] = pd.to_numeric(
    matricula_2012_34[col_matricula_34],
    errors="coerce"
)


# -------------------------------------------------------------------------
# 34.8 AGRUPAR MATRICULA_LIMPIA POR PARTIDO
# -------------------------------------------------------------------------

real_2012_34 = (
    matricula_2012_34
    .groupby(
        col_partido_34,
        as_index=False
    )[col_matricula_34]
    .sum(min_count=1)
    .rename(
        columns={
            col_partido_34: "departamento",
            col_matricula_34: "secundaria_matricula_limpia"
        }
    )
)

print("\n" + "=" * 70)
print("VALORES DE MATRICULA_LIMPIA - 2012")
print("=" * 70)

print(
    real_2012_34
    .sort_values("departamento")
    .to_string(index=False)
)


# -------------------------------------------------------------------------
# 34.9 COMPARAR HIPÓTESIS VS MATRICULA_LIMPIA
# -------------------------------------------------------------------------

comparacion_34 = hipotesis_2012_34.merge(
    real_2012_34,
    on="departamento",
    how="outer",
    indicator=True
)

comparacion_34["diferencia"] = (
    comparacion_34["secundaria_hipotesis_primera_aparicion"]
    -
    comparacion_34["secundaria_matricula_limpia"]
)

comparacion_34["coincide"] = np.isclose(
    comparacion_34[
        "secundaria_hipotesis_primera_aparicion"
    ],
    comparacion_34[
        "secundaria_matricula_limpia"
    ],
    equal_nan=False
)


# -------------------------------------------------------------------------
# 34.10 RESULTADO GENERAL
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("COMPARACIÓN: HIPÓTESIS VS MATRICULA_LIMPIA")
print("=" * 70)

columnas_mostrar_34 = [
    "departamento",
    "secundaria_hipotesis_primera_aparicion",
    "secundaria_matricula_limpia",
    "diferencia",
    "coincide",
    "_merge"
]

print(
    comparacion_34[
        columnas_mostrar_34
    ]
    .sort_values("departamento")
    .to_string(index=False)
)


# -------------------------------------------------------------------------
# 34.11 ESTADÍSTICAS DE VALIDACIÓN
# -------------------------------------------------------------------------

comparables_34 = comparacion_34[
    comparacion_34["_merge"] == "both"
].copy()

cantidad_comparables_34 = len(comparables_34)

cantidad_coinciden_34 = int(
    comparables_34["coincide"].sum()
)

cantidad_no_coinciden_34 = (
    cantidad_comparables_34
    -
    cantidad_coinciden_34
)

if cantidad_comparables_34 > 0:
    porcentaje_coincidencia_34 = (
        cantidad_coinciden_34
        / cantidad_comparables_34
        * 100
    )
else:
    porcentaje_coincidencia_34 = np.nan


print("\n" + "=" * 70)
print("RESUMEN DE VALIDACIÓN")
print("=" * 70)

print(
    "Departamentos comparables:",
    cantidad_comparables_34
)

print(
    "Coincidencias exactas:",
    cantidad_coinciden_34
)

print(
    "No coincidencias:",
    cantidad_no_coinciden_34
)

print(
    "Porcentaje de coincidencia:",
    round(porcentaje_coincidencia_34, 2)
    if pd.notna(porcentaje_coincidencia_34)
    else "No calculable"
)


# -------------------------------------------------------------------------
# 34.12 MOSTRAR SOLAMENTE LAS COINCIDENCIAS
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("DEPARTAMENTOS DONDE LA HIPÓTESIS COINCIDE")
print("=" * 70)

coincidencias_34 = comparables_34[
    comparables_34["coincide"]
].copy()

if len(coincidencias_34) == 0:
    print("No se encontraron coincidencias.")
else:
    print(
        coincidencias_34[
            columnas_mostrar_34[:-1]
        ]
        .sort_values("departamento")
        .to_string(index=False)
    )


# -------------------------------------------------------------------------
# 34.13 MOSTRAR SOLAMENTE LAS DIFERENCIAS
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("DEPARTAMENTOS DONDE LA HIPÓTESIS NO COINCIDE")
print("=" * 70)

diferencias_34 = comparables_34[
    ~comparables_34["coincide"]
].copy()

if len(diferencias_34) == 0:
    print("TODOS los departamentos comparables coinciden.")
else:
    print(
        diferencias_34[
            columnas_mostrar_34[:-1]
        ]
        .sort_values(
            "diferencia",
            key=lambda x: x.abs(),
            ascending=False
        )
        .to_string(index=False)
    )


# -------------------------------------------------------------------------
# 34.14 TERRITORIOS PRESENTES SOLO EN UNA DE LAS DOS FUENTES
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("TERRITORIOS PRESENTES SOLO EN UNA FUENTE")
print("=" * 70)

solo_fuente_34 = comparacion_34[
    comparacion_34["_merge"] == "left_only"
]

solo_limpia_34 = comparacion_34[
    comparacion_34["_merge"] == "right_only"
]

print("\nSolo en fuente original:")
if len(solo_fuente_34) == 0:
    print("Ninguno.")
else:
    print(
        solo_fuente_34[
            ["departamento"]
        ].to_string(index=False)
    )

print("\nSolo en matricula_limpia:")
if len(solo_limpia_34) == 0:
    print("Ninguno.")
else:
    print(
        solo_limpia_34[
            ["departamento"]
        ].to_string(index=False)
    )


# -------------------------------------------------------------------------
# 34.15 CONTROL ESPECÍFICO DE 25 DE MAYO
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("CONTROL: 25 DE MAYO")
print("=" * 70)

control_25_34 = comparacion_34[
    comparacion_34["departamento"] == "25 DE MAYO"
]

if len(control_25_34) == 0:
    print("25 DE MAYO no apareció en la comparación.")
else:
    print(
        control_25_34[
            columnas_mostrar_34
        ].to_string(index=False)
    )


# -------------------------------------------------------------------------
# 34.16 INTERPRETACIÓN AUTOMÁTICA
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("INTERPRETACIÓN")
print("=" * 70)

if (
    cantidad_comparables_34 > 0
    and cantidad_coinciden_34 == cantidad_comparables_34
):

    print("""
La hipótesis de tomar únicamente la primera aparición de cada
combinación sector-ámbito reproduce el 100% de los valores
comparables de matrícula secundaria de 2012 presentes en
matricula_limpia.

Este resultado sería una evidencia muy fuerte de que el orden
del archivo original contiene una estructura de bloques que fue
utilizada durante la construcción de matricula_limpia.

Sin embargo, antes de considerar esta regla como definitiva,
deberá comprobarse en otros años.
""")

elif cantidad_coinciden_34 > 0:

    print(f"""
La hipótesis reproduce algunos, pero no todos, los valores de
matricula_limpia.

Coincidencias:
{cantidad_coinciden_34} de {cantidad_comparables_34}
({porcentaje_coincidencia_34:.2f}%).

Esto indica que la primera aparición de sector-ámbito puede
estar capturando parte de la estructura real del archivo, pero
todavía no constituye una regla general.

Será necesario estudiar los departamentos donde no coincide
para identificar qué característica adicional distingue los
bloques.
""")

else:

    print("""
La hipótesis de primera aparición no reproduce de forma general
los valores de matricula_limpia.

La coincidencia observada en 25 DE MAYO podría deberse a una
estructura particular de ese caso o a otra variable implícita
en el orden del archivo.

Será necesario buscar otra regla de selección.
""")


# -------------------------------------------------------------------------
# 34.17 ACLARACIÓN DE SEGURIDAD
# -------------------------------------------------------------------------

print("\nIMPORTANTE:")
print("NO se realizó ninguna imputación.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 70)
print("DIAGNÓSTICO 34 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# =============================================================================
# 35. DIAGNOSTICAR EXCEPCIONES DE LA HIPÓTESIS DE PRIMERA APARICIÓN
# =============================================================================

print("\n" + "=" * 70)
print("35. DIAGNOSTICAR EXCEPCIONES DE LA HIPÓTESIS DE PRIMERA APARICIÓN")
print("=" * 70)

# IMPORTANTE:
# Este punto es exclusivamente diagnóstico.
# NO modifica fuente_2012_34.
# NO modifica matricula_limpia.
# NO modifica dataset_maestro.
# NO guarda ningún archivo.


# -------------------------------------------------------------------------
# 35.1 IDENTIFICAR PARTIDOS CON DIFERENCIA NUMÉRICA
# -------------------------------------------------------------------------

excepciones_35 = diferencias_34[
    diferencias_34[
        "secundaria_hipotesis_primera_aparicion"
    ].notna()
    &
    diferencias_34[
        "secundaria_matricula_limpia"
    ].notna()
].copy()

partidos_excepcion_35 = (
    excepciones_35["departamento"]
    .dropna()
    .unique()
    .tolist()
)

print("\nPartidos con diferencia numérica:")
print(partidos_excepcion_35)

print(
    "\nCantidad de partidos a estudiar:",
    len(partidos_excepcion_35)
)


# -------------------------------------------------------------------------
# 35.2 EXTRAER TODAS LAS FILAS ORIGINALES DE ESOS PARTIDOS
# -------------------------------------------------------------------------

detalle_excepciones_35 = fuente_2012_34[
    fuente_2012_34["departamento"].isin(
        partidos_excepcion_35
    )
].copy()

print("\nCantidad de filas originales involucradas:")
print(len(detalle_excepciones_35))


# -------------------------------------------------------------------------
# 35.3 MOSTRAR ESTRUCTURA COMPLETA DE CADA PARTIDO
# -------------------------------------------------------------------------

columnas_detalle_35 = [
    "indice_original_34",
    "departamento",
    "sector",
    "ambito",
    "numero_repeticion_34",
    "primera_aparicion_34",
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12",
    "secundaria_7_12_34"
]

# Agregar columnas potencialmente explicativas
# solamente si existen en el archivo.
columnas_extra_35 = [
    "multi_sec",
    "multinivel",
    "multi_ini",
    "multi_pri",
    "_1314",
    "_snu",
    "v_7",
    "v_8",
    "v_9",
    "v_10",
    "v_11",
    "v_12",
    "v_1314",
    "v_snu",
    "r_7",
    "r_8",
    "r_9",
    "r_10",
    "r_11",
    "r_12",
    "r_1314",
    "s_7",
    "s_8",
    "s_9",
    "s_10",
    "s_11",
    "s_12",
    "s_1314"
]

for col in columnas_extra_35:
    if col in detalle_excepciones_35.columns:
        columnas_detalle_35.append(col)


for partido_35 in partidos_excepcion_35:

    print("\n" + "=" * 100)
    print("PARTIDO:", partido_35)
    print("=" * 100)

    bloque_35 = detalle_excepciones_35[
        detalle_excepciones_35["departamento"]
        == partido_35
    ].copy()

    bloque_35 = bloque_35.sort_values(
        "indice_original_34"
    )

    print(
        bloque_35[
            columnas_detalle_35
        ].to_string(index=False)
    )


# -------------------------------------------------------------------------
# 35.4 RESUMEN POR SECTOR + ÁMBITO
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("35.4 RESUMEN POR SECTOR + ÁMBITO")
print("=" * 70)

resumen_sector_ambito_35 = (
    detalle_excepciones_35
    .groupby(
        [
            "departamento",
            "sector",
            "ambito"
        ],
        dropna=False
    )
    .agg(
        cantidad_filas=(
            "indice_original_34",
            "size"
        ),
        suma_todas_filas=(
            "secundaria_7_12_34",
            "sum"
        ),
        valor_primera_aparicion=(
            "secundaria_7_12_34",
            "first"
        ),
        minimo=(
            "secundaria_7_12_34",
            "min"
        ),
        maximo=(
            "secundaria_7_12_34",
            "max"
        )
    )
    .reset_index()
)

print(
    resumen_sector_ambito_35
    .sort_values(
        [
            "departamento",
            "sector",
            "ambito"
        ]
    )
    .to_string(index=False)
)


# -------------------------------------------------------------------------
# 35.5 COMPARAR TODAS LAS REPETICIONES DE CADA SECTOR + ÁMBITO
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("35.5 VALORES SEGÚN NÚMERO DE REPETICIÓN")
print("=" * 70)

tabla_repeticiones_35 = (
    detalle_excepciones_35
    .pivot_table(
        index=[
            "departamento",
            "sector",
            "ambito"
        ],
        columns="numero_repeticion_34",
        values="secundaria_7_12_34",
        aggfunc="first"
    )
    .reset_index()
)

tabla_repeticiones_35.columns = [
    (
        f"repeticion_{c}"
        if isinstance(c, (int, np.integer))
        else c
    )
    for c in tabla_repeticiones_35.columns
]

print(
    tabla_repeticiones_35
    .sort_values(
        [
            "departamento",
            "sector",
            "ambito"
        ]
    )
    .to_string(index=False)
)


# -------------------------------------------------------------------------
# 35.6 BUSCAR SI ALGUNA REPETICIÓN INDIVIDUAL EXPLICA LA DIFERENCIA
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("35.6 BUSCAR VALORES IGUALES A LA DIFERENCIA")
print("=" * 70)

hallazgos_diferencia_35 = []

for _, fila_exc_35 in excepciones_35.iterrows():

    partido_35 = fila_exc_35["departamento"]
    diferencia_35 = fila_exc_35["diferencia"]

    filas_partido_35 = detalle_excepciones_35[
        detalle_excepciones_35["departamento"]
        == partido_35
    ]

    for _, fila_original_35 in filas_partido_35.iterrows():

        valor_35 = fila_original_35[
            "secundaria_7_12_34"
        ]

        if (
            pd.notna(valor_35)
            and pd.notna(diferencia_35)
            and np.isclose(
                valor_35,
                diferencia_35
            )
        ):

            hallazgos_diferencia_35.append(
                {
                    "departamento":
                        partido_35,

                    "diferencia":
                        diferencia_35,

                    "indice_original":
                        fila_original_35[
                            "indice_original_34"
                        ],

                    "sector":
                        fila_original_35["sector"],

                    "ambito":
                        fila_original_35["ambito"],

                    "numero_repeticion":
                        fila_original_35[
                            "numero_repeticion_34"
                        ],

                    "primera_aparicion":
                        fila_original_35[
                            "primera_aparicion_34"
                        ],

                    "secundaria_fila":
                        valor_35
                }
            )


hallazgos_diferencia_35 = pd.DataFrame(
    hallazgos_diferencia_35
)

if len(hallazgos_diferencia_35) == 0:

    print(
        "Ninguna diferencia coincide exactamente "
        "con una fila individual."
    )

else:

    print(
        hallazgos_diferencia_35
        .sort_values(
            [
                "departamento",
                "indice_original"
            ]
        )
        .to_string(index=False)
    )


# -------------------------------------------------------------------------
# 35.7 ANALIZAR ESPECÍFICAMENTE LAS PRIMERAS APARICIONES
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("35.7 PRIMERAS APARICIONES QUE FORMAN LA HIPÓTESIS")
print("=" * 70)

primeras_excepciones_35 = detalle_excepciones_35[
    detalle_excepciones_35[
        "primera_aparicion_34"
    ]
].copy()

for partido_35 in partidos_excepcion_35:

    print("\n" + "-" * 90)
    print("PARTIDO:", partido_35)
    print("-" * 90)

    primeras_partido_35 = primeras_excepciones_35[
        primeras_excepciones_35["departamento"]
        == partido_35
    ].copy()

    print(
        primeras_partido_35[
            [
                "indice_original_34",
                "sector",
                "ambito",
                "_7",
                "_8",
                "_9",
                "_10",
                "_11",
                "_12",
                "secundaria_7_12_34"
            ]
        ]
        .to_string(index=False)
    )

    suma_35 = (
        primeras_partido_35[
            "secundaria_7_12_34"
        ].sum()
    )

    real_partido_35 = excepciones_35.loc[
        excepciones_35["departamento"]
        == partido_35,
        "secundaria_matricula_limpia"
    ]

    if len(real_partido_35) > 0:
        real_partido_35 = real_partido_35.iloc[0]
    else:
        real_partido_35 = np.nan

    print("\nSuma primeras apariciones:", suma_35)
    print("Valor matricula_limpia:", real_partido_35)

    if pd.notna(real_partido_35):
        print(
            "Exceso:",
            suma_35 - real_partido_35
        )


# -------------------------------------------------------------------------
# 35.8 BUSCAR SI EL VALOR REAL SE PUEDE OBTENER EXCLUYENDO
#      UNA DE LAS PRIMERAS APARICIONES
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("35.8 PROBAR EXCLUSIÓN DE UNA PRIMERA APARICIÓN")
print("=" * 70)

resultados_exclusion_35 = []

for partido_35 in partidos_excepcion_35:

    primeras_partido_35 = primeras_excepciones_35[
        primeras_excepciones_35["departamento"]
        == partido_35
    ].copy()

    real_35 = excepciones_35.loc[
        excepciones_35["departamento"]
        == partido_35,
        "secundaria_matricula_limpia"
    ]

    if len(real_35) == 0:
        continue

    real_35 = real_35.iloc[0]

    suma_total_35 = primeras_partido_35[
        "secundaria_7_12_34"
    ].sum()

    for _, fila_35 in primeras_partido_35.iterrows():

        suma_sin_fila_35 = (
            suma_total_35
            -
            fila_35["secundaria_7_12_34"]
        )

        coincide_sin_fila_35 = np.isclose(
            suma_sin_fila_35,
            real_35
        )

        if coincide_sin_fila_35:

            resultados_exclusion_35.append(
                {
                    "departamento":
                        partido_35,

                    "matricula_limpia":
                        real_35,

                    "hipotesis_original":
                        suma_total_35,

                    "indice_excluido":
                        fila_35[
                            "indice_original_34"
                        ],

                    "sector_excluido":
                        fila_35["sector"],

                    "ambito_excluido":
                        fila_35["ambito"],

                    "valor_excluido":
                        fila_35[
                            "secundaria_7_12_34"
                        ],

                    "resultado_sin_fila":
                        suma_sin_fila_35
                }
            )


resultados_exclusion_35 = pd.DataFrame(
    resultados_exclusion_35
)

if len(resultados_exclusion_35) == 0:

    print(
        "No hay casos donde excluir una única "
        "primera aparición reproduzca exactamente "
        "matricula_limpia."
    )

else:

    print(
        resultados_exclusion_35
        .sort_values("departamento")
        .to_string(index=False)
    )


# -------------------------------------------------------------------------
# 35.9 CONTROL ESPECIAL DE LOS CASOS MÁS INFORMATIVOS
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("35.9 CASOS PRIORITARIOS")
print("=" * 70)

casos_prioritarios_35 = [
    "MAIPU",
    "GENERAL ALVEAR",
    "LEANDRO N. ALEM",
    "GENERAL SAN MARTIN",
    "MORENO"
]

for partido_35 in casos_prioritarios_35:

    if partido_35 not in partidos_excepcion_35:
        continue

    print("\n" + "#" * 100)
    print("CASO PRIORITARIO:", partido_35)
    print("#" * 100)

    caso_35 = detalle_excepciones_35[
        detalle_excepciones_35["departamento"]
        == partido_35
    ].copy()

    print(
        caso_35[
            columnas_detalle_35
        ]
        .sort_values("indice_original_34")
        .to_string(index=False)
    )


# -------------------------------------------------------------------------
# 35.10 RESUMEN FINAL
# -------------------------------------------------------------------------

print("\n" + "=" * 70)
print("RESUMEN DEL DIAGNÓSTICO 35")
print("=" * 70)

print(
    "Partidos analizados:",
    len(partidos_excepcion_35)
)

print(
    "Filas originales analizadas:",
    len(detalle_excepciones_35)
)

print(
    "Casos donde una fila individual coincide "
    "con la diferencia:",
    len(hallazgos_diferencia_35)
)

print(
    "Casos donde excluir una primera aparición "
    "reproduce matricula_limpia:",
    len(resultados_exclusion_35)
)

print("""
Objetivo del diagnóstico:
determinar qué característica distingue las primeras
apariciones que parecen haber sido excluidas durante la
construcción de matricula_limpia.

Todavía NO se adopta ninguna nueva regla.
Primero deben inspeccionarse los patrones encontrados.
""")

print("IMPORTANTE:")
print("NO se realizó ninguna imputación.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 70)
print("DIAGNÓSTICO 35 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 70)

# ======================================================================
# 36. DIAGNOSTICAR LA REGLA REAL DE EXCLUSIÓN
# ======================================================================

import pandas as pd
import numpy as np
from itertools import combinations

print("\n" + "=" * 100)
print("36. DIAGNOSTICAR LA REGLA REAL DE EXCLUSIÓN")
print("=" * 100)


# ======================================================================
# 36.0 LOCALIZAR AUTOMÁTICAMENTE LOS DATAFRAMES NECESARIOS
# ======================================================================

# ----------------------------------------------------------
# A) Buscar el DataFrame que contiene las filas originales
#    utilizadas en el diagnóstico 34/35.
# ----------------------------------------------------------

columnas_necesarias_filas_36 = {
    "departamento",
    "sector",
    "ambito",
    "numero_repeticion_34",
    "primera_aparicion_34",
    "secundaria_7_12_34"
}

candidatos_filas_36 = []

for nombre, objeto in list(globals().items()):

    if isinstance(objeto, pd.DataFrame):

        if columnas_necesarias_filas_36.issubset(
            set(objeto.columns)
        ):
            candidatos_filas_36.append(
                (nombre, objeto)
            )


if len(candidatos_filas_36) == 0:

    raise ValueError(
        "\nNo encontré ningún DataFrame que tenga estas columnas:\n"
        + str(columnas_necesarias_filas_36)
    )


# Si hay varios candidatos, elegimos el que tenga más filas.
candidatos_filas_36.sort(
    key=lambda x: len(x[1]),
    reverse=True
)

nombre_filas_36, datos_filas_36 = candidatos_filas_36[0]

print("\nDataFrame de filas encontrado automáticamente:")
print("Nombre:", nombre_filas_36)
print("Filas:", len(datos_filas_36))
print("Columnas:", len(datos_filas_36.columns))


# ----------------------------------------------------------
# B) Buscar el DataFrame de comparación con matricula_limpia
# ----------------------------------------------------------

candidatos_comparacion_36 = []

for nombre, objeto in list(globals().items()):

    if not isinstance(objeto, pd.DataFrame):
        continue

    columnas_lower = [
        str(c).lower()
        for c in objeto.columns
    ]

    tiene_departamento = (
        "departamento" in objeto.columns
    )

    tiene_diferencia = any(
        "difer" in c
        for c in columnas_lower
    )

    tiene_matricula = any(
        "matricula_limpia" in c
        for c in columnas_lower
    )

    if (
        tiene_departamento
        and tiene_diferencia
        and tiene_matricula
    ):
        candidatos_comparacion_36.append(
            (nombre, objeto)
        )


if len(candidatos_comparacion_36) == 0:

    raise ValueError(
        "\nNo encontré el DataFrame que contiene "
        "departamento, diferencia y matricula_limpia."
    )


# Si comparacion_34 existe y cumple las condiciones,
# lo priorizamos.
comparacion_encontrada_36 = None
nombre_comparacion_36 = None

for nombre, objeto in candidatos_comparacion_36:

    if nombre == "comparacion_34":
        nombre_comparacion_36 = nombre
        comparacion_encontrada_36 = objeto
        break


# Si no existe comparacion_34, usamos el candidato
# con menor cantidad de filas, porque normalmente
# la comparación tiene una fila por partido.
if comparacion_encontrada_36 is None:

    candidatos_comparacion_36.sort(
        key=lambda x: len(x[1])
    )

    nombre_comparacion_36, comparacion_encontrada_36 = (
        candidatos_comparacion_36[0]
    )


print("\nDataFrame de comparación encontrado automáticamente:")
print("Nombre:", nombre_comparacion_36)
print("Filas:", len(comparacion_encontrada_36))
print("Columnas:", len(comparacion_encontrada_36.columns))


# ======================================================================
# 36.1 IDENTIFICAR PARTIDOS CON DIFERENCIA
# ======================================================================

columnas_diferencia = [
    c for c in comparacion_encontrada_36.columns
    if "difer" in str(c).lower()
]

if len(columnas_diferencia) == 0:
    raise ValueError(
        "No se encontró una columna de diferencia."
    )

col_diferencia = columnas_diferencia[0]


columnas_matricula = [
    c for c in comparacion_encontrada_36.columns
    if "matricula_limpia" in str(c).lower()
]

if len(columnas_matricula) == 0:
    raise ValueError(
        "No se encontró una columna de matricula_limpia."
    )

col_matricula = columnas_matricula[0]


print("\nColumna de diferencia utilizada:")
print(col_diferencia)

print("\nColumna de matrícula utilizada:")
print(col_matricula)


casos_36 = comparacion_encontrada_36[
    pd.to_numeric(
        comparacion_encontrada_36[col_diferencia],
        errors="coerce"
    ).fillna(0) != 0
].copy()


partidos_36 = (
    casos_36["departamento"]
    .dropna()
    .unique()
    .tolist()
)


print("\nPartidos con diferencia:")
print(partidos_36)

print(
    "\nCantidad de partidos a estudiar:",
    len(partidos_36)
)


# ======================================================================
# 36.2 PREPARAR PRIMERAS APARICIONES
# ======================================================================

# IMPORTANTE:
# Acá ya NO usamos df_34.
# Usamos el DataFrame encontrado automáticamente.

primeras_36 = datos_filas_36[
    (
        datos_filas_36["departamento"]
        .isin(partidos_36)
    )
    &
    (
        datos_filas_36["primera_aparicion_34"]
        == True
    )
].copy()


print(
    "\nCantidad total de primeras apariciones involucradas:"
)

print(len(primeras_36))


# Control
print("\nPrimeras apariciones por partido:")

print(
    primeras_36
    .groupby("departamento")
    .size()
    .reset_index(name="cantidad")
    .to_string(index=False)
)
# ======================================================================
# 36.3 BUSCAR COMBINACIONES QUE EXPLIQUEN LA DIFERENCIA
# ======================================================================

print("\n" + "=" * 100)
print("36.3 BUSCAR COMBINACIONES DE PRIMERAS APARICIONES")
print("=" * 100)

resultados_combinaciones_36 = []

for partido in partidos_36:

    filas_partido = primeras_36[
        primeras_36["departamento"] == partido
    ].copy()

    fila_comp = casos_36[
        casos_36["departamento"] == partido
    ]

    if fila_comp.empty:
        continue

    diferencia = float(fila_comp.iloc[0][col_diferencia])

    indices = filas_partido.index.tolist()

    combinaciones_encontradas = []

    # Probamos exclusión de 1, 2 y 3 primeras apariciones.
    max_r = min(3, len(indices))

    for r in range(1, max_r + 1):

        for combo in combinations(indices, r):

            filas_combo = filas_partido.loc[list(combo)]

            suma_combo = filas_combo[
                "secundaria_7_12_34"
            ].fillna(0).sum()

            if np.isclose(suma_combo, diferencia):

                combinaciones_encontradas.append(
                    {
                        "cantidad_filas": r,
                        "indices_dataframe": list(combo),
                        "indices_originales": (
                            filas_combo["indice_original_34"].tolist()
                            if "indice_original_34" in filas_combo.columns
                            else list(combo)
                        ),
                        "sectores": filas_combo["sector"].tolist(),
                        "ambitos": filas_combo["ambito"].tolist(),
                        "valores": filas_combo[
                            "secundaria_7_12_34"
                        ].tolist(),
                        "suma": suma_combo
                    }
                )

    print("\n" + "-" * 90)
    print("PARTIDO:", partido)
    print("-" * 90)
    print("Diferencia a explicar:", diferencia)

    if combinaciones_encontradas:

        # Priorizamos la combinación con menor cantidad de filas.
        minimo = min(
            x["cantidad_filas"]
            for x in combinaciones_encontradas
        )

        mejores = [
            x for x in combinaciones_encontradas
            if x["cantidad_filas"] == minimo
        ]

        print(
            f"Combinaciones encontradas con {minimo} fila(s): "
            f"{len(mejores)}"
        )

        for n, resultado in enumerate(mejores, start=1):

            print(f"\nCombinación {n}:")
            print(
                "Índices originales:",
                resultado["indices_originales"]
            )
            print("Sectores:", resultado["sectores"])
            print("Ámbitos:", resultado["ambitos"])
            print("Valores:", resultado["valores"])
            print("Suma:", resultado["suma"])

            resultados_combinaciones_36.append(
                {
                    "departamento": partido,
                    "diferencia": diferencia,
                    "cantidad_excluidas": minimo,
                    "indices_originales": resultado[
                        "indices_originales"
                    ],
                    "sectores": resultado["sectores"],
                    "ambitos": resultado["ambitos"],
                    "valores": resultado["valores"],
                    "suma_excluida": resultado["suma"]
                }
            )

    else:
        print(
            "NO se encontró combinación de hasta 3 "
            "primeras apariciones."
        )


df_combinaciones_36 = pd.DataFrame(
    resultados_combinaciones_36
)
# ======================================================================
# 36.4 CONSTRUIR GRUPO EXCLUIDO E INCLUIDO
# ======================================================================

print("\n" + "=" * 100)
print("36.4 CONSTRUIR GRUPOS EXCLUIDOS E INCLUIDOS")
print("=" * 100)

# Reunimos los índices originales de las filas que, según 36.3,
# explican exactamente las diferencias.
indices_excluidos_originales_36 = set()

for _, fila in df_combinaciones_36.iterrows():

    for idx in fila["indices_originales"]:
        indices_excluidos_originales_36.add(idx)

if "indice_original_34" not in primeras_36.columns:
    raise ValueError(
        "No existe la columna 'indice_original_34' "
        "en el DataFrame utilizado."
    )

# Clasificamos cada primera aparición.
primeras_36["clasificacion_36"] = np.where(
    primeras_36["indice_original_34"].isin(
        indices_excluidos_originales_36
    ),
    "EXCLUIDA",
    "INCLUIDA"
)

excluidas_36 = primeras_36[
    primeras_36["clasificacion_36"] == "EXCLUIDA"
].copy()

incluidas_36 = primeras_36[
    primeras_36["clasificacion_36"] == "INCLUIDA"
].copy()

print("\nÍndices originales clasificados como EXCLUIDOS:")
print(sorted(indices_excluidos_originales_36))

print("\nCantidad de primeras apariciones EXCLUIDAS:")
print(len(excluidas_36))

print("\nCantidad de primeras apariciones INCLUIDAS:")
print(len(incluidas_36))


# ======================================================================
# 36.5 MOSTRAR FILAS EXCLUIDAS
# ======================================================================

print("\n" + "=" * 100)
print("36.5 PRIMERAS APARICIONES EXCLUIDAS")
print("=" * 100)

columnas_base_36 = [
    "indice_original_34",
    "departamento",
    "sector",
    "ambito",
    "numero_repeticion_34",
    "secundaria_7_12_34",
    "multi_sec",
    "multinivel",
    "multi_ini",
    "multi_pri",
    "_1314",
    "_snu"
]

columnas_base_36 = [
    c for c in columnas_base_36
    if c in primeras_36.columns
]

print(
    excluidas_36[columnas_base_36]
    .sort_values(
        ["departamento", "indice_original_34"]
    )
    .to_string(index=False)
)


# ======================================================================
# 36.6 MOSTRAR FILAS INCLUIDAS
# ======================================================================

print("\n" + "=" * 100)
print("36.6 PRIMERAS APARICIONES INCLUIDAS")
print("=" * 100)

print(
    incluidas_36[columnas_base_36]
    .sort_values(
        ["departamento", "indice_original_34"]
    )
    .to_string(index=False)
)


# ======================================================================
# 36.7 COMPARAR SECTOR + ÁMBITO
# ======================================================================

print("\n" + "=" * 100)
print("36.7 COMPARACIÓN POR SECTOR + ÁMBITO")
print("=" * 100)

comparacion_sector_ambito_36 = (
    primeras_36
    .groupby(
        ["clasificacion_36", "sector", "ambito"],
        dropna=False
    )
    .size()
    .reset_index(name="cantidad")
)

print(
    comparacion_sector_ambito_36
    .sort_values(
        ["clasificacion_36", "sector", "ambito"]
    )
    .to_string(index=False)
)


# ======================================================================
# 36.8 COMPARAR VARIABLES MULTI*
# ======================================================================

print("\n" + "=" * 100)
print("36.8 COMPARACIÓN DE VARIABLES MULTI*")
print("=" * 100)

columnas_multi_36 = [
    "multi_sec",
    "multinivel",
    "multi_ini",
    "multi_pri"
]

columnas_multi_36 = [
    c for c in columnas_multi_36
    if c in primeras_36.columns
]

resumen_multi_36 = []

for columna in columnas_multi_36:

    for grupo, df_grupo in [
        ("EXCLUIDA", excluidas_36),
        ("INCLUIDA", incluidas_36)
    ]:

        serie = pd.to_numeric(
            df_grupo[columna],
            errors="coerce"
        )

        resumen_multi_36.append(
            {
                "variable": columna,
                "grupo": grupo,
                "cantidad_filas": len(df_grupo),
                "cantidad_no_nula": int(
                    serie.notna().sum()
                ),
                "cantidad_mayor_0": int(
                    (serie.fillna(0) > 0).sum()
                ),
                "suma": serie.fillna(0).sum(),
                "media": serie.mean()
            }
        )

df_resumen_multi_36 = pd.DataFrame(
    resumen_multi_36
)

print(
    df_resumen_multi_36.to_string(index=False)
)


# ======================================================================
# 36.9 COMPARAR _1314 Y _SNU
# ======================================================================

print("\n" + "=" * 100)
print("36.9 COMPARACIÓN DE _1314 Y _SNU")
print("=" * 100)

columnas_extra_36 = [
    c for c in ["_1314", "_snu"]
    if c in primeras_36.columns
]

resumen_extra_36 = []

for columna in columnas_extra_36:

    for grupo, df_grupo in [
        ("EXCLUIDA", excluidas_36),
        ("INCLUIDA", incluidas_36)
    ]:

        serie = pd.to_numeric(
            df_grupo[columna],
            errors="coerce"
        )

        resumen_extra_36.append(
            {
                "variable": columna,
                "grupo": grupo,
                "cantidad_filas": len(df_grupo),
                "cantidad_no_nula": int(
                    serie.notna().sum()
                ),
                "cantidad_mayor_0": int(
                    (serie.fillna(0) > 0).sum()
                ),
                "suma": serie.fillna(0).sum(),
                "media": serie.mean()
            }
        )

df_resumen_extra_36 = pd.DataFrame(
    resumen_extra_36
)

print(
    df_resumen_extra_36.to_string(index=False)
)


# ======================================================================
# 36.10 COMPARAR BLOQUES V, R Y S
# ======================================================================

print("\n" + "=" * 100)
print("36.10 COMPARACIÓN DE BLOQUES V_*, R_* Y S_*")
print("=" * 100)

bloques_36 = {
    "V": [
        c for c in primeras_36.columns
        if str(c).startswith("v_")
    ],
    "R": [
        c for c in primeras_36.columns
        if str(c).startswith("r_")
    ],
    "S": [
        c for c in primeras_36.columns
        if str(c).startswith("s_")
    ]
}

resumen_bloques_36 = []

for nombre_bloque, columnas in bloques_36.items():

    for grupo, df_grupo in [
        ("EXCLUIDA", excluidas_36),
        ("INCLUIDA", incluidas_36)
    ]:

        if len(columnas) == 0:
            continue

        numerico = df_grupo[columnas].apply(
            pd.to_numeric,
            errors="coerce"
        )

        suma_por_fila = (
            numerico
            .fillna(0)
            .sum(axis=1)
        )

        resumen_bloques_36.append(
            {
                "bloque": nombre_bloque,
                "grupo": grupo,
                "cantidad_filas": len(df_grupo),
                "filas_con_valores": int(
                    (suma_por_fila > 0).sum()
                ),
                "filas_sin_valores": int(
                    (suma_por_fila == 0).sum()
                ),
                "suma_total": suma_por_fila.sum(),
                "media_por_fila": suma_por_fila.mean()
            }
        )

df_resumen_bloques_36 = pd.DataFrame(
    resumen_bloques_36
)

print(
    df_resumen_bloques_36.to_string(index=False)
)


# ======================================================================
# 36.11 CREAR INDICADORES DETALLADOS POR FILA
# ======================================================================

print("\n" + "=" * 100)
print("36.11 INDICADORES DETALLADOS POR PRIMERA APARICIÓN")
print("=" * 100)

detalle_36 = primeras_36.copy()

# Indicadores de variables multi*
for columna in columnas_multi_36:

    detalle_36[f"{columna}_positivo"] = (
        pd.to_numeric(
            detalle_36[columna],
            errors="coerce"
        )
        .fillna(0)
        .gt(0)
    )

# Indicadores de bloques V/R/S
for nombre_bloque, columnas in bloques_36.items():

    if len(columnas) == 0:
        continue

    datos = (
        detalle_36[columnas]
        .apply(
            pd.to_numeric,
            errors="coerce"
        )
        .fillna(0)
    )

    suma = datos.sum(axis=1)

    detalle_36[
        f"suma_{nombre_bloque.lower()}"
    ] = suma

    detalle_36[
        f"tiene_{nombre_bloque.lower()}"
    ] = suma > 0


columnas_detalle_36 = [
    "indice_original_34",
    "departamento",
    "sector",
    "ambito",
    "secundaria_7_12_34",
    "clasificacion_36"
]

columnas_detalle_36 += [
    c for c in detalle_36.columns
    if c.endswith("_positivo")
]

columnas_detalle_36 += [
    c for c in [
        "suma_v",
        "tiene_v",
        "suma_r",
        "tiene_r",
        "suma_s",
        "tiene_s"
    ]
    if c in detalle_36.columns
]

print(
    detalle_36[columnas_detalle_36]
    .sort_values(
        [
            "clasificacion_36",
            "departamento",
            "indice_original_34"
        ]
    )
    .to_string(index=False)
)


# ======================================================================
# 36.12 BUSCAR CARACTERÍSTICAS BINARIAS
# ======================================================================

print("\n" + "=" * 100)
print("36.12 BUSCAR PATRONES BINARIOS")
print("=" * 100)

# Sector y ámbito
detalle_36["es_rural"] = (
    detalle_36["ambito"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("RURAL")
)

detalle_36["es_urbano"] = (
    detalle_36["ambito"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("URBANO")
)

detalle_36["es_estatal"] = (
    detalle_36["sector"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("ESTATAL")
)

detalle_36["es_privado"] = (
    detalle_36["sector"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("PRIVADO")
)

variables_binarias_36 = [
    "es_rural",
    "es_urbano",
    "es_estatal",
    "es_privado"
]

# Agregamos indicadores multi*
variables_binarias_36 += [
    c for c in detalle_36.columns
    if c.endswith("_positivo")
]

# Agregamos indicadores V/R/S
variables_binarias_36 += [
    c for c in [
        "tiene_v",
        "tiene_r",
        "tiene_s"
    ]
    if c in detalle_36.columns
]

patrones_binarios_36 = []

for variable in variables_binarias_36:

    excl = detalle_36.loc[
        detalle_36["clasificacion_36"] == "EXCLUIDA",
        variable
    ].astype(bool)

    incl = detalle_36.loc[
        detalle_36["clasificacion_36"] == "INCLUIDA",
        variable
    ].astype(bool)

    patrones_binarios_36.append(
        {
            "variable": variable,

            "excluidas_true": int(excl.sum()),
            "excluidas_total": len(excl),

            "pct_excluidas": (
                excl.mean() * 100
                if len(excl) > 0
                else np.nan
            ),

            "incluidas_true": int(incl.sum()),
            "incluidas_total": len(incl),

            "pct_incluidas": (
                incl.mean() * 100
                if len(incl) > 0
                else np.nan
            )
        }
    )

df_patrones_binarios_36 = pd.DataFrame(
    patrones_binarios_36
)

df_patrones_binarios_36["diferencia_pct"] = (
    df_patrones_binarios_36["pct_excluidas"]
    - df_patrones_binarios_36["pct_incluidas"]
).abs()

df_patrones_binarios_36 = (
    df_patrones_binarios_36
    .sort_values(
        "diferencia_pct",
        ascending=False
    )
)

print(
    df_patrones_binarios_36.to_string(index=False)
)


# ======================================================================
# 36.13 BUSCAR REGLAS SIMPLES PERFECTAS
# ======================================================================

print("\n" + "=" * 100)
print("36.13 REGLAS SIMPLES QUE SEPARAN PERFECTAMENTE LOS GRUPOS")
print("=" * 100)

reglas_perfectas_36 = []

for variable in variables_binarias_36:

    excl = detalle_36.loc[
        detalle_36["clasificacion_36"] == "EXCLUIDA",
        variable
    ].astype(bool)

    incl = detalle_36.loc[
        detalle_36["clasificacion_36"] == "INCLUIDA",
        variable
    ].astype(bool)

    # Todas las excluidas = True
    # Todas las incluidas = False
    if (
        len(excl) > 0
        and len(incl) > 0
        and excl.all()
        and (~incl).all()
    ):
        reglas_perfectas_36.append(
            f"{variable} == True"
        )

    # Todas las excluidas = False
    # Todas las incluidas = True
    if (
        len(excl) > 0
        and len(incl) > 0
        and (~excl).all()
        and incl.all()
    ):
        reglas_perfectas_36.append(
            f"{variable} == False"
        )

if len(reglas_perfectas_36) > 0:

    print(
        "\nSe encontraron reglas simples "
        "con separación perfecta:"
    )

    for regla in reglas_perfectas_36:
        print(" -", regla)

else:

    print(
        "\nNO se encontró una única variable binaria "
        "que separe perfectamente las filas "
        "EXCLUIDAS de las INCLUIDAS."
    )


# ======================================================================
# 36.14 RESUMEN DE EXCLUSIONES
# ======================================================================

print("\n" + "=" * 100)
print("36.14 RESUMEN DE EXCLUSIONES QUE REPRODUCEN LA DIFERENCIA")
print("=" * 100)

if not df_combinaciones_36.empty:

    print(
        df_combinaciones_36
        .sort_values("departamento")
        .to_string(index=False)
    )

else:

    print("No se encontraron combinaciones.")


# ======================================================================
# 36.15 CONTROL ESPECIAL: GENERAL SAN MARTIN
# ======================================================================

print("\n" + "=" * 100)
print("36.15 CONTROL ESPECIAL DE GENERAL SAN MARTIN")
print("=" * 100)

gsm_36 = df_combinaciones_36[
    df_combinaciones_36["departamento"]
    == "GENERAL SAN MARTIN"
]

if not gsm_36.empty:

    print(gsm_36.to_string(index=False))

else:

    print(
        "No se encontró una combinación para "
        "GENERAL SAN MARTIN."
    )


# ======================================================================
# 36.16 RESUMEN FINAL
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL DIAGNÓSTICO 36")
print("=" * 100)

print(
    "Partidos analizados:",
    len(partidos_36)
)

print(
    "Primeras apariciones analizadas:",
    len(primeras_36)
)

print(
    "Primeras apariciones clasificadas como EXCLUIDAS:",
    len(excluidas_36)
)

print(
    "Primeras apariciones clasificadas como INCLUIDAS:",
    len(incluidas_36)
)

print(
    "Partidos cuya diferencia fue reproducida:",
    (
        df_combinaciones_36["departamento"].nunique()
        if not df_combinaciones_36.empty
        else 0
    ),
    "de",
    len(partidos_36)
)

print(
    "Reglas binarias simples con separación perfecta:",
    len(reglas_perfectas_36)
)

print("\nObjetivo del diagnóstico:")
print(
    "identificar qué características distinguen las "
    "primeras apariciones que parecen haber sido "
    "excluidas en matricula_limpia."
)

print("\nIMPORTANTE:")
print("NO se adoptó ninguna nueva regla.")
print("NO se realizó ninguna imputación.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("DIAGNÓSTICO 36 FINALIZADO")
print("NO SE MODIFICÓ NINGÚN DATASET")
print("=" * 100)

# ======================================================================
# 37. BUSCAR AUTOMÁTICAMENTE QUÉ VARIABLES DISTINGUEN
#     LAS PRIMERAS APARICIONES EXCLUIDAS DE LAS INCLUIDAS
# ======================================================================

print("\n" + "=" * 100)
print("37. BUSCAR VARIABLES QUE DISTINGUEN EXCLUIDAS E INCLUIDAS")
print("=" * 100)


# ======================================================================
# 37.1 CONTROL INICIAL
# ======================================================================

print("\nCantidad de filas analizadas:", len(detalle_36))
print(
    "EXCLUIDAS:",
    (detalle_36["clasificacion_36"] == "EXCLUIDA").sum()
)
print(
    "INCLUIDAS:",
    (detalle_36["clasificacion_36"] == "INCLUIDA").sum()
)


# ======================================================================
# 37.2 IDENTIFICAR COLUMNAS ORIGINALES DISPONIBLES
# ======================================================================

# Trabajamos con primeras_36 porque conserva las columnas originales
# de fuente_2012_34.

columnas_analizar_37 = []

columnas_excluir_37 = {
    "clasificacion_36",
    "primera_aparicion_34",
    "numero_repeticion_34",
    "indice_original_34",
    "departamento"
}

for columna in primeras_36.columns:

    if columna not in columnas_excluir_37:
        columnas_analizar_37.append(columna)

print("\nColumnas originales disponibles para analizar:")
print(len(columnas_analizar_37))


# ======================================================================
# 37.3 ANALIZAR COLUMNAS NUMÉRICAS
# ======================================================================

print("\n" + "=" * 100)
print("37.3 DIFERENCIAS EN VARIABLES NUMÉRICAS")
print("=" * 100)

resultados_numericos_37 = []

for columna in columnas_analizar_37:

    serie_total = pd.to_numeric(
        primeras_36[columna],
        errors="coerce"
    )

    # Solo analizamos como numérica si existe al menos algún dato
    # convertible a número.
    if serie_total.notna().sum() == 0:
        continue

    excl = pd.to_numeric(
        excluidas_36[columna],
        errors="coerce"
    )

    incl = pd.to_numeric(
        incluidas_36[columna],
        errors="coerce"
    )

    excl_no_nulos = excl.dropna()
    incl_no_nulos = incl.dropna()

    if len(excl_no_nulos) == 0 and len(incl_no_nulos) == 0:
        continue

    media_excl = (
        excl_no_nulos.mean()
        if len(excl_no_nulos) > 0
        else np.nan
    )

    media_incl = (
        incl_no_nulos.mean()
        if len(incl_no_nulos) > 0
        else np.nan
    )

    mediana_excl = (
        excl_no_nulos.median()
        if len(excl_no_nulos) > 0
        else np.nan
    )

    mediana_incl = (
        incl_no_nulos.median()
        if len(incl_no_nulos) > 0
        else np.nan
    )

    positivos_excl = int(
        (excl.fillna(0) > 0).sum()
    )

    positivos_incl = int(
        (incl.fillna(0) > 0).sum()
    )

    pct_pos_excl = (
        positivos_excl / len(excl) * 100
        if len(excl) > 0
        else np.nan
    )

    pct_pos_incl = (
        positivos_incl / len(incl) * 100
        if len(incl) > 0
        else np.nan
    )

    resultados_numericos_37.append(
        {
            "variable": columna,

            "excl_no_nulos": len(excl_no_nulos),
            "incl_no_nulos": len(incl_no_nulos),

            "media_excl": media_excl,
            "media_incl": media_incl,

            "mediana_excl": mediana_excl,
            "mediana_incl": mediana_incl,

            "positivos_excl": positivos_excl,
            "positivos_incl": positivos_incl,

            "pct_pos_excl": pct_pos_excl,
            "pct_pos_incl": pct_pos_incl,

            "dif_pct_positivo": abs(
                pct_pos_excl - pct_pos_incl
            )
        }
    )


df_numericas_37 = pd.DataFrame(
    resultados_numericos_37
)

if not df_numericas_37.empty:

    df_numericas_37 = (
        df_numericas_37
        .sort_values(
            "dif_pct_positivo",
            ascending=False
        )
    )

    print(
        df_numericas_37.head(40)
        .to_string(index=False)
    )

else:
    print("No se detectaron variables numéricas.")


# ======================================================================
# 37.4 BUSCAR PRESENCIA / AUSENCIA PERFECTA
# ======================================================================

print("\n" + "=" * 100)
print("37.4 VARIABLES CON PATRÓN DE PRESENCIA/AUSENCIA")
print("=" * 100)

patrones_presencia_37 = []

for columna in columnas_analizar_37:

    serie_total = pd.to_numeric(
        primeras_36[columna],
        errors="coerce"
    )

    if serie_total.notna().sum() == 0:
        continue

    excl = pd.to_numeric(
        excluidas_36[columna],
        errors="coerce"
    ).fillna(0)

    incl = pd.to_numeric(
        incluidas_36[columna],
        errors="coerce"
    ).fillna(0)

    excl_pos = excl > 0
    incl_pos = incl > 0

    pct_excl = excl_pos.mean() * 100
    pct_incl = incl_pos.mean() * 100

    diferencia = abs(pct_excl - pct_incl)

    if diferencia >= 40:

        patrones_presencia_37.append(
            {
                "variable": columna,
                "excluidas_con_valor": int(excl_pos.sum()),
                "excluidas_total": len(excl_pos),
                "pct_excluidas": pct_excl,
                "incluidas_con_valor": int(incl_pos.sum()),
                "incluidas_total": len(incl_pos),
                "pct_incluidas": pct_incl,
                "diferencia_pct": diferencia
            }
        )


df_presencia_37 = pd.DataFrame(
    patrones_presencia_37
)

if not df_presencia_37.empty:

    df_presencia_37 = (
        df_presencia_37
        .sort_values(
            "diferencia_pct",
            ascending=False
        )
    )

    print(
        df_presencia_37.to_string(index=False)
    )

else:

    print(
        "No se encontraron variables con una diferencia "
        "de presencia >= 40 puntos porcentuales."
    )


# ======================================================================
# 37.5 BUSCAR SEPARACIÓN PERFECTA POR UMBRAL NUMÉRICO
# ======================================================================

print("\n" + "=" * 100)
print("37.5 BUSCAR UMBRALES NUMÉRICOS PERFECTOS")
print("=" * 100)

umbrales_perfectos_37 = []

for columna in columnas_analizar_37:

    serie = pd.to_numeric(
        primeras_36[columna],
        errors="coerce"
    )

    if serie.notna().sum() < 2:
        continue

    temp = pd.DataFrame({
        "valor": serie,
        "grupo": primeras_36["clasificacion_36"]
    }).dropna()

    if temp["grupo"].nunique() < 2:
        continue

    valores_unicos = sorted(
        temp["valor"].unique()
    )

    if len(valores_unicos) < 2:
        continue

    # Puntos medios entre valores consecutivos.
    thresholds = [
        (valores_unicos[i] + valores_unicos[i + 1]) / 2
        for i in range(len(valores_unicos) - 1)
    ]

    for threshold in thresholds:

        excl = temp[
            temp["grupo"] == "EXCLUIDA"
        ]["valor"]

        incl = temp[
            temp["grupo"] == "INCLUIDA"
        ]["valor"]

        # Regla 1:
        # excluidas <= umbral
        # incluidas > umbral

        if (
            len(excl) > 0
            and len(incl) > 0
            and (excl <= threshold).all()
            and (incl > threshold).all()
        ):

            umbrales_perfectos_37.append(
                {
                    "variable": columna,
                    "regla": "<=",
                    "umbral": threshold,
                    "max_excluida": excl.max(),
                    "min_incluida": incl.min()
                }
            )

            break

        # Regla 2:
        # excluidas > umbral
        # incluidas <= umbral

        if (
            len(excl) > 0
            and len(incl) > 0
            and (excl > threshold).all()
            and (incl <= threshold).all()
        ):

            umbrales_perfectos_37.append(
                {
                    "variable": columna,
                    "regla": ">",
                    "umbral": threshold,
                    "min_excluida": excl.min(),
                    "max_incluida": incl.max()
                }
            )

            break


df_umbrales_37 = pd.DataFrame(
    umbrales_perfectos_37
)

if not df_umbrales_37.empty:

    print(
        df_umbrales_37.to_string(index=False)
    )

else:

    print(
        "NO se encontró una variable numérica "
        "con un umbral que separe perfectamente "
        "EXCLUIDAS e INCLUIDAS."
    )


# ======================================================================
# 37.6 ANALIZAR VARIABLES DE TEXTO / CATEGÓRICAS
# ======================================================================

print("\n" + "=" * 100)
print("37.6 VARIABLES CATEGÓRICAS")
print("=" * 100)

resultados_categoricos_37 = []

for columna in columnas_analizar_37:

    # Si la columna es claramente numérica, no la repetimos.
    convertida = pd.to_numeric(
        primeras_36[columna],
        errors="coerce"
    )

    proporcion_numerica = (
        convertida.notna().mean()
    )

    if proporcion_numerica > 0.8:
        continue

    excl = (
        excluidas_36[columna]
        .fillna("<<NA>>")
        .astype(str)
        .str.strip()
    )

    incl = (
        incluidas_36[columna]
        .fillna("<<NA>>")
        .astype(str)
        .str.strip()
    )

    valores_excl = set(excl.unique())
    valores_incl = set(incl.unique())

    solo_excl = valores_excl - valores_incl
    solo_incl = valores_incl - valores_excl

    if solo_excl or solo_incl:

        resultados_categoricos_37.append(
            {
                "variable": columna,
                "solo_excluidas": sorted(
                    list(solo_excl)
                )[:10],
                "solo_incluidas": sorted(
                    list(solo_incl)
                )[:10]
            }
        )


df_categoricas_37 = pd.DataFrame(
    resultados_categoricos_37
)

if not df_categoricas_37.empty:

    print(
        df_categoricas_37.head(40)
        .to_string(index=False)
    )

else:

    print(
        "No aparecieron categorías exclusivas relevantes."
    )


# ======================================================================
# 37.7 MIRAR PARTICULARMENTE LAS 10 FILAS EXCLUIDAS
# ======================================================================

print("\n" + "=" * 100)
print("37.7 PERFIL COMPLETO DE LAS 10 FILAS EXCLUIDAS")
print("=" * 100)

columnas_interes_37 = [
    "indice_original_34",
    "departamento",
    "sector",
    "ambito",
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12",
    "secundaria_7_12_34",
    "multi_sec",
    "multinivel",
    "multi_ini",
    "multi_pri",
    "_1314",
    "_snu"
]

# Agregamos automáticamente columnas cuyo nombre pueda
# contener información estructural importante.
palabras_interes_37 = [
    "nivel",
    "modal",
    "tipo",
    "oferta",
    "servicio",
    "depend",
    "sector",
    "ambito",
    "rural",
    "urbano",
    "estable",
    "escuela"
]

for columna in primeras_36.columns:

    nombre = str(columna).lower()

    if any(
        palabra in nombre
        for palabra in palabras_interes_37
    ):

        if columna not in columnas_interes_37:
            columnas_interes_37.append(columna)

columnas_interes_37 = [
    c for c in columnas_interes_37
    if c in primeras_36.columns
]

print(
    excluidas_36[columnas_interes_37]
    .sort_values(
        ["departamento", "indice_original_34"]
    )
    .to_string(index=False)
)


# ======================================================================
# 37.8 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL DIAGNÓSTICO 37")
print("=" * 100)

print(
    "Variables originales analizadas:",
    len(columnas_analizar_37)
)

print(
    "Variables numéricas analizadas:",
    len(df_numericas_37)
)

print(
    "Variables con diferencia de presencia >= 40 puntos:",
    len(df_presencia_37)
)

print(
    "Variables con umbral perfecto:",
    len(df_umbrales_37)
)

print(
    "Variables categóricas con categorías exclusivas:",
    len(df_categoricas_37)
)

print("\nIMPORTANTE:")
print("Este diagnóstico solamente busca patrones.")
print("NO se adoptó ninguna regla nueva.")
print("NO se realizó ninguna imputación.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("DIAGNÓSTICO 37 FINALIZADO")
print("=" * 100)
# ======================================================================
# 38. DIAGNOSTICAR SI LAS "EXCLUSIONES" SON REGISTROS
#     DE OTRAS PROVINCIAS CON EL MISMO NOMBRE DE DEPARTAMENTO
# ======================================================================

print("\n" + "=" * 100)
print("38. DIAGNOSTICAR COINCIDENCIAS DE DEPARTAMENTO ENTRE PROVINCIAS")
print("=" * 100)


# ======================================================================
# 38.1 CONTROLAR COLUMNA PROVINCIA
# ======================================================================

if "provincia" not in primeras_36.columns:
    raise ValueError(
        "No se encontró la columna 'provincia' en primeras_36."
    )

control_provincia_38 = primeras_36[
    [
        "indice_original_34",
        "provincia",
        "departamento",
        "sector",
        "ambito",
        "secundaria_7_12_34",
        "clasificacion_36"
    ]
].copy()

print("\nFilas involucradas con provincia:")
print(
    control_provincia_38
    .sort_values(
        ["departamento", "provincia", "sector", "ambito"]
    )
    .to_string(index=False)
)


# ======================================================================
# 38.2 PROVINCIAS DE LAS FILAS EXCLUIDAS
# ======================================================================

print("\n" + "=" * 100)
print("38.2 PROVINCIAS DE LAS FILAS CLASIFICADAS COMO EXCLUIDAS")
print("=" * 100)

print(
    control_provincia_38[
        control_provincia_38["clasificacion_36"] == "EXCLUIDA"
    ]
    .sort_values(["provincia", "departamento"])
    .to_string(index=False)
)


print("\nConteo por provincia:")

print(
    control_provincia_38[
        control_provincia_38["clasificacion_36"] == "EXCLUIDA"
    ]
    .groupby("provincia", dropna=False)
    .size()
    .reset_index(name="cantidad")
    .sort_values("cantidad", ascending=False)
    .to_string(index=False)
)


# ======================================================================
# 38.3 PROVINCIAS DE LAS FILAS INCLUIDAS
# ======================================================================

print("\n" + "=" * 100)
print("38.3 PROVINCIAS DE LAS FILAS CLASIFICADAS COMO INCLUIDAS")
print("=" * 100)

print(
    control_provincia_38[
        control_provincia_38["clasificacion_36"] == "INCLUIDA"
    ]
    .sort_values(["provincia", "departamento"])
    .to_string(index=False)
)


print("\nConteo por provincia:")

print(
    control_provincia_38[
        control_provincia_38["clasificacion_36"] == "INCLUIDA"
    ]
    .groupby("provincia", dropna=False)
    .size()
    .reset_index(name="cantidad")
    .sort_values("cantidad", ascending=False)
    .to_string(index=False)
)


# ======================================================================
# 38.4 COMPROBAR SEPARACIÓN PROVINCIA
# ======================================================================

print("\n" + "=" * 100)
print("38.4 COMPROBAR HIPÓTESIS PROVINCIA")
print("=" * 100)

provincia_normalizada_38 = (
    primeras_36["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
)

es_buenos_aires_38 = provincia_normalizada_38.isin(
    [
        "BUENOS AIRES",
        "PROVINCIA DE BUENOS AIRES"
    ]
)

clasificacion_38 = primeras_36["clasificacion_36"]

tabla_38 = pd.crosstab(
    clasificacion_38,
    es_buenos_aires_38,
    rownames=["clasificacion"],
    colnames=["es_buenos_aires"]
)

print("\nTabla clasificación vs provincia:")
print(tabla_38)


excluidas_ba_38 = (
    (clasificacion_38 == "EXCLUIDA") &
    es_buenos_aires_38
).sum()

incluidas_fuera_ba_38 = (
    (clasificacion_38 == "INCLUIDA") &
    (~es_buenos_aires_38)
).sum()

print(
    "\nFilas EXCLUIDAS que pertenecen a Buenos Aires:",
    excluidas_ba_38
)

print(
    "Filas INCLUIDAS que NO pertenecen a Buenos Aires:",
    incluidas_fuera_ba_38
)


if (
    excluidas_ba_38 == 0
    and incluidas_fuera_ba_38 == 0
):
    print(
        "\n>>> PATRÓN PERFECTO EN LAS 28 FILAS:"
    )
    print(
        "Todas las INCLUIDAS pertenecen a Buenos Aires "
        "y todas las EXCLUIDAS pertenecen a otra provincia."
    )
else:
    print(
        "\nLa provincia NO separa perfectamente los grupos."
    )


# ======================================================================
# 38.5 COMPROBAR MATEMÁTICAMENTE CONTRA MATRICULA_LIMPIA
# ======================================================================

print("\n" + "=" * 100)
print("38.5 COMPROBAR SUMA DE BUENOS AIRES CONTRA MATRICULA_LIMPIA")
print("=" * 100)

filas_ba_38 = primeras_36[
    provincia_normalizada_38.isin(
        [
            "BUENOS AIRES",
            "PROVINCIA DE BUENOS AIRES"
        ]
    )
].copy()

suma_ba_38 = (
    filas_ba_38
    .groupby("departamento")["secundaria_7_12_34"]
    .sum()
    .reset_index(
        name="suma_primeras_apariciones_buenos_aires"
    )
)

control_matricula_38 = casos_36[
    ["departamento", col_matricula]
].copy()

control_matricula_38 = control_matricula_38.merge(
    suma_ba_38,
    on="departamento",
    how="left"
)

control_matricula_38[
    "diferencia_control"
] = (
    control_matricula_38[
        "suma_primeras_apariciones_buenos_aires"
    ]
    -
    control_matricula_38[col_matricula]
)

control_matricula_38[
    "coincide"
] = np.isclose(
    control_matricula_38[
        "suma_primeras_apariciones_buenos_aires"
    ],
    control_matricula_38[col_matricula],
    equal_nan=False
)

print(
    control_matricula_38
    .to_string(index=False)
)


# ======================================================================
# 38.6 RESUMEN FINAL
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL DIAGNÓSTICO 38")
print("=" * 100)

coincidencias_38 = int(
    control_matricula_38["coincide"].sum()
)

total_38 = len(control_matricula_38)

print(
    "Partidos donde sumar únicamente registros de Buenos Aires "
    "reproduce matricula_limpia:",
    f"{coincidencias_38} de {total_38}"
)

if coincidencias_38 == total_38:

    print("\n>>> HIPÓTESIS FUERTEMENTE CONFIRMADA.")
    print(
        "Las diferencias parecen provenir de mezclar "
        "departamentos homónimos de distintas provincias."
    )

    print(
        "\nLa clave territorial no debería ser solamente "
        "'departamento'."
    )

    print(
        "Debería incorporarse 'provincia' para evitar "
        "unir territorios diferentes con el mismo nombre."
    )

else:

    print(
        "\nLa hipótesis de provincia explica algunos casos, "
        "pero todavía existen excepciones."
    )


print("\nIMPORTANTE:")
print("NO se modificó ningún dataset.")
print("NO se realizó ninguna imputación.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("DIAGNÓSTICO 38 FINALIZADO")
print("=" * 100)

# ======================================================================
# 39. VALIDAR CORRECCIÓN TERRITORIAL DEFINITIVA
#     FILTRAR PROVINCIA DE BUENOS AIRES
# ======================================================================

print("\n" + "=" * 100)
print("39. VALIDAR CORRECCIÓN TERRITORIAL DEFINITIVA")
print("=" * 100)


# ======================================================================
# 39.1 IDENTIFICAR DATAFRAME FUENTE
# ======================================================================

# En el diagnóstico 36 detectamos que la fuente utilizada es:
# fuente_2012_34

if "fuente_2012_34" not in globals():
    raise NameError(
        "No existe fuente_2012_34. "
        "Debe ejecutarse primero el bloque donde se construye esa fuente."
    )

fuente_39 = fuente_2012_34.copy()

print("\nFuente analizada:")
print("fuente_2012_34")

print("Filas totales:", len(fuente_39))
print("Columnas:", len(fuente_39.columns))


# ======================================================================
# 39.2 CONTROLAR COLUMNAS TERRITORIALES
# ======================================================================

columnas_necesarias_39 = [
    "provincia",
    "departamento"
]

faltantes_39 = [
    c for c in columnas_necesarias_39
    if c not in fuente_39.columns
]

if faltantes_39:
    raise ValueError(
        f"Faltan columnas necesarias: {faltantes_39}"
    )

print("\nColumnas territoriales encontradas correctamente.")


# ======================================================================
# 39.3 NORMALIZAR PROVINCIA SOLO PARA EL DIAGNÓSTICO
# ======================================================================

fuente_39["_provincia_normalizada_39"] = (
    fuente_39["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print("\nProvincias presentes en la fuente:")

print(
    fuente_39[
        ["provincia", "_provincia_normalizada_39"]
    ]
    .drop_duplicates()
    .sort_values("provincia")
    .to_string(index=False)
)


# ======================================================================
# 39.4 CREAR VERSIÓN FILTRADA DE BUENOS AIRES
#     TODAVÍA NO MODIFICA LA FUENTE ORIGINAL
# ======================================================================

fuente_ba_39 = fuente_39[
    fuente_39["_provincia_normalizada_39"].isin(
        [
            "BUENOS AIRES",
            "PROVINCIA DE BUENOS AIRES"
        ]
    )
].copy()

print("\n" + "=" * 100)
print("39.4 FILTRO BUENOS AIRES")
print("=" * 100)

print("Filas antes del filtro:", len(fuente_39))
print("Filas después del filtro:", len(fuente_ba_39))
print(
    "Filas de otras provincias eliminadas:",
    len(fuente_39) - len(fuente_ba_39)
)


# ======================================================================
# 39.5 CONTROLAR DEPARTAMENTOS HOMÓNIMOS
# ======================================================================

print("\n" + "=" * 100)
print("39.5 DEPARTAMENTOS QUE APARECEN EN MÁS DE UNA PROVINCIA")
print("=" * 100)

control_homonimos_39 = (
    fuente_39
    .groupby("departamento")["provincia"]
    .nunique()
    .reset_index(name="cantidad_provincias")
)

homonimos_39 = control_homonimos_39[
    control_homonimos_39["cantidad_provincias"] > 1
].copy()

print(
    "Cantidad de nombres de departamento presentes "
    "en más de una provincia:",
    len(homonimos_39)
)

if not homonimos_39.empty:

    detalle_homonimos_39 = (
        fuente_39[
            fuente_39["departamento"].isin(
                homonimos_39["departamento"]
            )
        ]
        [["provincia", "departamento"]]
        .drop_duplicates()
        .sort_values(
            ["departamento", "provincia"]
        )
    )

    print("\nDetalle:")
    print(
        detalle_homonimos_39.to_string(index=False)
    )


# ======================================================================
# 39.6 VERIFICAR LOS 9 CASOS PROBLEMÁTICOS
# ======================================================================

print("\n" + "=" * 100)
print("39.6 CONTROL DE LOS 9 CASOS PROBLEMÁTICOS")
print("=" * 100)

partidos_problema_39 = [
    "ALMIRANTE BROWN",
    "AVELLANEDA",
    "GENERAL ALVEAR",
    "GENERAL SAN MARTIN",
    "ITUZAINGO",
    "LEANDRO N. ALEM",
    "MAIPU",
    "MORENO",
    "SAN MIGUEL"
]

control_problemas_39 = (
    fuente_39[
        fuente_39["departamento"].isin(
            partidos_problema_39
        )
    ]
    .groupby(
        ["departamento", "provincia"],
        dropna=False
    )
    .size()
    .reset_index(name="cantidad_filas")
)

print(
    control_problemas_39
    .sort_values(
        ["departamento", "provincia"]
    )
    .to_string(index=False)
)


# ======================================================================
# 39.7 COMPROBAR QUE DESPUÉS DEL FILTRO CADA CASO
#     PERTENEZCA SOLO A BUENOS AIRES
# ======================================================================

print("\n" + "=" * 100)
print("39.7 CONTROL DESPUÉS DEL FILTRO")
print("=" * 100)

control_ba_39 = (
    fuente_ba_39[
        fuente_ba_39["departamento"].isin(
            partidos_problema_39
        )
    ]
    .groupby("departamento")
    .agg(
        cantidad_filas=("departamento", "size"),
        cantidad_provincias=("provincia", "nunique"),
        provincia=("provincia", "first")
    )
    .reset_index()
)

print(
    control_ba_39
    .sort_values("departamento")
    .to_string(index=False)
)


# ======================================================================
# 39.8 COMPROBAR NUEVAMENTE MATRÍCULA SECUNDARIA
# ======================================================================

print("\n" + "=" * 100)
print("39.8 VALIDACIÓN CONTRA MATRICULA_LIMPIA")
print("=" * 100)

# Usamos la misma lógica que ya comprobamos en el diagnóstico 38:
# primeras apariciones + Buenos Aires.

primeras_ba_39 = primeras_36[
    primeras_36["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
    .isin(
        [
            "BUENOS AIRES",
            "PROVINCIA DE BUENOS AIRES"
        ]
    )
].copy()

suma_secundaria_ba_39 = (
    primeras_ba_39
    .groupby("departamento")[
        "secundaria_7_12_34"
    ]
    .sum()
    .reset_index(
        name="secundaria_reconstruida_39"
    )
)

validacion_39 = casos_36[
    ["departamento", col_matricula]
].copy()

validacion_39 = validacion_39.merge(
    suma_secundaria_ba_39,
    on="departamento",
    how="left"
)

validacion_39["diferencia_39"] = (
    validacion_39["secundaria_reconstruida_39"]
    -
    validacion_39[col_matricula]
)

validacion_39["coincide_39"] = np.isclose(
    validacion_39["secundaria_reconstruida_39"],
    validacion_39[col_matricula],
    equal_nan=False
)

print(
    validacion_39.to_string(index=False)
)


# ======================================================================
# 39.9 CONTROL DE COBERTURA TERRITORIAL
# ======================================================================

print("\n" + "=" * 100)
print("39.9 COBERTURA TERRITORIAL DE BUENOS AIRES")
print("=" * 100)

departamentos_ba_39 = sorted(
    fuente_ba_39["departamento"]
    .dropna()
    .unique()
)

print(
    "Cantidad de departamentos/partidos únicos "
    "en la fuente filtrada:",
    len(departamentos_ba_39)
)

print("\nPrimeros 30:")
print(departamentos_ba_39[:30])


# ======================================================================
# 39.10 DETECTAR SI QUEDAN DUPLICADOS TERRITORIALES
# ======================================================================

print("\n" + "=" * 100)
print("39.10 CONTROL DE CLAVE PROVINCIA + DEPARTAMENTO")
print("=" * 100)

claves_39 = (
    fuente_ba_39[
        ["provincia", "departamento"]
    ]
    .drop_duplicates()
)

print(
    "Cantidad de combinaciones únicas "
    "provincia + departamento:",
    len(claves_39)
)

print(
    "Cantidad de departamentos únicos:",
    fuente_ba_39["departamento"].nunique()
)

if (
    len(claves_39)
    ==
    fuente_ba_39["departamento"].nunique()
):
    print(
        "\nOK: dentro de Buenos Aires cada nombre de "
        "departamento pertenece a una única provincia."
    )
else:
    print(
        "\nATENCIÓN: todavía existen inconsistencias "
        "en la clave territorial."
    )


# ======================================================================
# 39.11 DECISIÓN AUTOMÁTICA
# ======================================================================

print("\n" + "=" * 100)
print("39.11 RESULTADO DE LA VALIDACIÓN")
print("=" * 100)

coincidencias_39 = int(
    validacion_39["coincide_39"].sum()
)

total_validaciones_39 = len(validacion_39)

print(
    "Casos corregidos:",
    f"{coincidencias_39} de {total_validaciones_39}"
)

if coincidencias_39 == total_validaciones_39:

    print("\n>>> VALIDACIÓN EXITOSA.")

    print(
        "El filtro por Provincia de Buenos Aires "
        "corrige los 9 casos problemáticos."
    )

    print(
        "La causa del error queda identificada como "
        "colisión de nombres de departamento entre provincias."
    )

    print(
        "\nSIGUIENTE PASO:"
    )

    print(
        "Aplicar el filtro de Buenos Aires en el punto "
        "correcto del pipeline y reconstruir la variable."
    )

else:

    print("\n>>> TODAVÍA HAY DIFERENCIAS.")

    print(
        "No debe modificarse el pipeline hasta "
        "investigar los casos restantes."
    )


# ======================================================================
# 39.12 RESUMEN FINAL
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL DIAGNÓSTICO 39")
print("=" * 100)

print("Filas fuente original:", len(fuente_39))
print("Filas fuente Buenos Aires:", len(fuente_ba_39))

print(
    "Filas de otras provincias:",
    len(fuente_39) - len(fuente_ba_39)
)

print(
    "Departamentos homónimos entre provincias:",
    len(homonimos_39)
)

print(
    "Validaciones de matrícula correctas:",
    f"{coincidencias_39}/{total_validaciones_39}"
)

print("\nIMPORTANTE:")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("DIAGNÓSTICO 39 FINALIZADO")
print("=" * 100)

# ======================================================================
# 40. LOCALIZAR EL PUNTO CORRECTO PARA APLICAR EL FILTRO TERRITORIAL
# ======================================================================

print("\n" + "=" * 100)
print("40. LOCALIZAR EL PUNTO CORRECTO PARA APLICAR EL FILTRO TERRITORIAL")
print("=" * 100)

# ----------------------------------------------------------------------
# 40.1 CONTROLAR LA FUENTE ACTUAL
# ----------------------------------------------------------------------

if "fuente_2012_34" not in globals():
    raise NameError(
        "No existe fuente_2012_34. "
        "Ejecutá primero los bloques anteriores."
    )

print("\nFuente actual: fuente_2012_34")
print("Filas:", len(fuente_2012_34))
print("Columnas:", len(fuente_2012_34.columns))

print("\nProvincias presentes actualmente:")

print(
    fuente_2012_34["provincia"]
    .value_counts(dropna=False)
    .to_string()
)


# ----------------------------------------------------------------------
# 40.2 CREAR COPIA CORREGIDA SOLO EN MEMORIA
# ----------------------------------------------------------------------

fuente_2012_ba_40 = fuente_2012_34[
    fuente_2012_34["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("BUENOS AIRES")
].copy()

print("\n" + "-" * 80)
print("COPIA FILTRADA PARA BUENOS AIRES")
print("-" * 80)

print("Filas originales:", len(fuente_2012_34))
print("Filas Buenos Aires:", len(fuente_2012_ba_40))

print(
    "Filas descartadas:",
    len(fuente_2012_34) - len(fuente_2012_ba_40)
)


# ----------------------------------------------------------------------
# 40.3 COMPROBAR QUE SOLO QUEDE BUENOS AIRES
# ----------------------------------------------------------------------

provincias_restantes_40 = (
    fuente_2012_ba_40["provincia"]
    .dropna()
    .unique()
    .tolist()
)

print("\nProvincias restantes:")
print(provincias_restantes_40)

if len(provincias_restantes_40) == 1:

    print("\n>>> OK: la copia contiene únicamente Buenos Aires.")

else:

    print(
        "\n>>> ATENCIÓN: quedó más de una provincia."
    )


# ----------------------------------------------------------------------
# 40.4 CONTROLAR PARTIDOS
# ----------------------------------------------------------------------

cantidad_partidos_40 = (
    fuente_2012_ba_40["departamento"]
    .nunique()
)

print(
    "\nCantidad de partidos/departamentos únicos:",
    cantidad_partidos_40
)


# ----------------------------------------------------------------------
# 40.5 MOSTRAR INFORMACIÓN NECESARIA PARA EL SIGUIENTE PASO
# ----------------------------------------------------------------------

print("\n" + "=" * 100)
print("RESULTADO DEL PASO 40")
print("=" * 100)

print(
    "La fuente nacional puede transformarse correctamente "
    "en una fuente exclusiva de Provincia de Buenos Aires."
)

print(
    "\nEl próximo paso será aplicar esta condición "
    "en la construcción original de fuente_2012_34, "
    "ANTES de cualquier agrupación por departamento."
)

print("\nIMPORTANTE:")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("PASO 40 FINALIZADO")
print("=" * 100)

# ======================================================================
# 41. CONTROLAR LOS 136 DEPARTAMENTOS DE BUENOS AIRES
# ======================================================================

print("\n" + "=" * 100)
print("41. CONTROLAR LOS 136 DEPARTAMENTOS DE BUENOS AIRES")
print("=" * 100)

# Lista de departamentos presentes en la fuente filtrada
departamentos_41 = sorted(
    fuente_2012_ba_40["departamento"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

print("\nCantidad de departamentos encontrados:")
print(len(departamentos_41))

print("\nListado completo:")
for i, departamento in enumerate(departamentos_41, start=1):
    print(f"{i:03d}. {departamento}")


# ======================================================================
# 41.2 BUSCAR NOMBRES SOSPECHOSOS O CATEGORÍAS ESPECIALES
# ======================================================================

print("\n" + "=" * 100)
print("41.2 POSIBLES CATEGORÍAS ESPECIALES")
print("=" * 100)

palabras_sospechosas_41 = [
    "ENMASCARADO",
    "SIN",
    "IGNORADO",
    "DESCONOCIDO",
    "TOTAL",
    "OTRO",
    "NO ESPECIFICADO"
]

sospechosos_41 = fuente_2012_ba_40[
    fuente_2012_ba_40["departamento"]
    .astype(str)
    .str.upper()
    .apply(
        lambda x: any(
            palabra in x
            for palabra in palabras_sospechosas_41
        )
    )
].copy()

if sospechosos_41.empty:

    print("\nNo se encontraron categorías sospechosas automáticamente.")

else:

    columnas_mostrar_41 = [
        c for c in [
            "provincia",
            "departamento",
            "sector",
            "ambito"
        ]
        if c in sospechosos_41.columns
    ]

    print("\nFilas con nombres potencialmente especiales:")

    print(
        sospechosos_41[columnas_mostrar_41]
        .drop_duplicates()
        .to_string(index=False)
    )


# ======================================================================
# 41.3 FRECUENCIA POR DEPARTAMENTO
# ======================================================================

print("\n" + "=" * 100)
print("41.3 FRECUENCIA DE FILAS POR DEPARTAMENTO")
print("=" * 100)

frecuencia_41 = (
    fuente_2012_ba_40
    .groupby("departamento", dropna=False)
    .size()
    .reset_index(name="cantidad_filas")
    .sort_values(
        ["cantidad_filas", "departamento"],
        ascending=[True, True]
    )
)

print(frecuencia_41.to_string(index=False))


# ======================================================================
# 41.4 DEPARTAMENTOS CON MUY POCAS FILAS
# ======================================================================

print("\n" + "=" * 100)
print("41.4 DEPARTAMENTOS CON 1 SOLA FILA")
print("=" * 100)

una_fila_41 = frecuencia_41[
    frecuencia_41["cantidad_filas"] == 1
]

if una_fila_41.empty:
    print("\nNo hay departamentos con una sola fila.")
else:
    print(una_fila_41.to_string(index=False))


# ======================================================================
# 41.5 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL CONTROL 41")
print("=" * 100)

print("Departamentos únicos:", len(departamentos_41))
print("Filas Buenos Aires:", len(fuente_2012_ba_40))
print("Categorías sospechosas encontradas:", len(sospechosos_41))

print("\nIMPORTANTE:")
print("Este paso es únicamente diagnóstico.")
print("NO se eliminó ningún departamento.")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("CONTROL 41 FINALIZADO")
print("=" * 100)

# ======================================================================
# 42. DIAGNOSTICAR LA CATEGORÍA ENMASCARADO
# ======================================================================

print("\n" + "=" * 100)
print("42. DIAGNOSTICAR LA CATEGORÍA ENMASCARADO")
print("=" * 100)


# ======================================================================
# 42.1 EXTRAER FILAS ENMASCARADAS DE BUENOS AIRES
# ======================================================================

enmascarado_42 = fuente_2012_ba_40[
    fuente_2012_ba_40["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("ENMASCARADO")
].copy()

print("\nCantidad de filas ENMASCARADO:")
print(len(enmascarado_42))


# ======================================================================
# 42.2 MOSTRAR TODA LA INFORMACIÓN TERRITORIAL Y EDUCATIVA RELEVANTE
# ======================================================================

columnas_42 = [
    "provincia",
    "departamento",
    "sector",
    "ambito",
    "_7",
    "_8",
    "_9",
    "_10",
    "_11",
    "_12",
    "secundaria_7_12_34",
    "multi_sec",
    "multinivel",
    "multi_ini",
    "multi_pri",
    "_1314",
    "_snu"
]

columnas_42 = [
    c for c in columnas_42
    if c in enmascarado_42.columns
]

print("\nFilas ENMASCARADO:")

print(
    enmascarado_42[columnas_42]
    .to_string(index=False)
)


# ======================================================================
# 42.3 SUMA DE MATRÍCULA SECUNDARIA
# ======================================================================

if "secundaria_7_12_34" in enmascarado_42.columns:

    secundaria_enmascarado_42 = pd.to_numeric(
        enmascarado_42["secundaria_7_12_34"],
        errors="coerce"
    ).fillna(0).sum()

    print("\nMatrícula secundaria total de ENMASCARADO:")
    print(secundaria_enmascarado_42)

else:

    secundaria_enmascarado_42 = np.nan

    print(
        "\nNo existe secundaria_7_12_34 "
        "en la fuente."
    )


# ======================================================================
# 42.4 BUSCAR ENMASCARADO EN COMPARACION_34
# ======================================================================

print("\n" + "=" * 100)
print("42.4 BUSCAR ENMASCARADO EN COMPARACION_34")
print("=" * 100)

if "comparacion_34" in globals():

    if "departamento" in comparacion_34.columns:

        comp_enmascarado_42 = comparacion_34[
            comparacion_34["departamento"]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("ENMASCARADO")
        ].copy()

        if comp_enmascarado_42.empty:

            print(
                "\nENMASCARADO NO aparece en comparacion_34."
            )

        else:

            print(
                "\nENMASCARADO aparece en comparacion_34:"
            )

            print(
                comp_enmascarado_42
                .to_string(index=False)
            )

    else:

        print(
            "\ncomparacion_34 no tiene columna departamento."
        )

else:

    print("\ncomparacion_34 no está disponible.")


# ======================================================================
# 42.5 BUSCAR ENMASCARADO EN DATASET_MAESTRO
# ======================================================================

print("\n" + "=" * 100)
print("42.5 BUSCAR ENMASCARADO EN DATASET_MAESTRO")
print("=" * 100)

if "dataset_maestro" in globals():

    posibles_columnas_territoriales_42 = [
        c for c in dataset_maestro.columns
        if (
            "depart" in str(c).lower()
            or "partido" in str(c).lower()
        )
    ]

    print("\nColumnas territoriales candidatas:")
    print(posibles_columnas_territoriales_42)

    encontrado_maestro_42 = False

    for columna in posibles_columnas_territoriales_42:

        mascara = (
            dataset_maestro[columna]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("ENMASCARADO")
        )

        if mascara.any():

            encontrado_maestro_42 = True

            print(
                f"\nENMASCARADO encontrado en "
                f"dataset_maestro['{columna}']"
            )

            print(
                dataset_maestro.loc[mascara]
                .to_string(index=False)
            )

    if not encontrado_maestro_42:

        print(
            "\nENMASCARADO NO aparece en dataset_maestro."
        )

else:

    print(
        "\ndataset_maestro no está disponible en memoria."
    )


# ======================================================================
# 42.6 BUSCAR ENMASCARADO EN TODOS LOS DATAFRAMES EN MEMORIA
# ======================================================================

print("\n" + "=" * 100)
print("42.6 BUSCAR ENMASCARADO EN DATAFRAMES RELEVANTES")
print("=" * 100)

apariciones_42 = []

for nombre_objeto, objeto in list(globals().items()):

    if not isinstance(objeto, pd.DataFrame):
        continue

    for columna in objeto.columns:

        if (
            "depart" not in str(columna).lower()
            and "partido" not in str(columna).lower()
        ):
            continue

        try:

            mascara = (
                objeto[columna]
                .astype(str)
                .str.strip()
                .str.upper()
                .eq("ENMASCARADO")
            )

            cantidad = int(mascara.sum())

            if cantidad > 0:

                apariciones_42.append(
                    {
                        "dataframe": nombre_objeto,
                        "columna": columna,
                        "cantidad": cantidad
                    }
                )

        except Exception:
            pass


df_apariciones_42 = pd.DataFrame(apariciones_42)

if df_apariciones_42.empty:

    print(
        "\nNo se encontró ENMASCARADO "
        "en otros DataFrames."
    )

else:

    print(
        df_apariciones_42
        .drop_duplicates()
        .sort_values(
            ["dataframe", "columna"]
        )
        .to_string(index=False)
    )


# ======================================================================
# 42.7 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL DIAGNÓSTICO 42")
print("=" * 100)

print(
    "Filas ENMASCARADO en la fuente Buenos Aires:",
    len(enmascarado_42)
)

print(
    "Matrícula secundaria asociada:",
    secundaria_enmascarado_42
)

print("\nObjetivo:")
print(
    "determinar si ENMASCARADO forma parte del universo "
    "territorial final o si es una categoría que debe "
    "quedar fuera del análisis por partido."
)

print("\nIMPORTANTE:")
print("NO se eliminó ENMASCARADO.")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("DIAGNÓSTICO 42 FINALIZADO")
print("=" * 100)
# ======================================================================
# 43. VALIDACIÓN FINAL DEL UNIVERSO TERRITORIAL
#     BUENOS AIRES + EXCLUSIÓN DE ENMASCARADO
# ======================================================================

print("\n" + "=" * 100)
print("43. VALIDACIÓN FINAL DEL UNIVERSO TERRITORIAL")
print("=" * 100)


# ======================================================================
# 43.1 CONSTRUIR UNIVERSO TERRITORIAL DEFINITIVO
# ======================================================================

fuente_ba_final_43 = fuente_2012_34.copy()

# Normalizamos provincia y departamento SOLO para realizar el filtro.
provincia_norm_43 = (
    fuente_ba_final_43["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
)

departamento_norm_43 = (
    fuente_ba_final_43["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Condición territorial definitiva.
mascara_43 = (
    provincia_norm_43.eq("BUENOS AIRES")
    &
    ~departamento_norm_43.eq("ENMASCARADO")
)

fuente_ba_final_43 = (
    fuente_ba_final_43[mascara_43]
    .copy()
)


print("\nFilas fuente nacional:")
print(len(fuente_2012_34))

print("\nFilas después de aplicar:")
print("provincia == Buenos Aires")
print("departamento != ENMASCARADO")
print(len(fuente_ba_final_43))


# ======================================================================
# 43.2 CONTROL DE PROVINCIAS
# ======================================================================

print("\n" + "=" * 100)
print("43.2 CONTROL DE PROVINCIAS")
print("=" * 100)

print(
    fuente_ba_final_43["provincia"]
    .value_counts(dropna=False)
    .to_string()
)

provincias_43 = (
    fuente_ba_final_43["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
    .unique()
    .tolist()
)

if provincias_43 == ["BUENOS AIRES"]:
    print("\nOK: solamente quedó Provincia de Buenos Aires.")
else:
    print("\nATENCIÓN: quedaron provincias inesperadas:")
    print(provincias_43)


# ======================================================================
# 43.3 CONTROL DE ENMASCARADO
# ======================================================================

print("\n" + "=" * 100)
print("43.3 CONTROL DE ENMASCARADO")
print("=" * 100)

cantidad_enmascarado_43 = (
    fuente_ba_final_43["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("ENMASCARADO")
    .sum()
)

print(
    "Filas ENMASCARADO restantes:",
    cantidad_enmascarado_43
)

if cantidad_enmascarado_43 == 0:
    print("OK: ENMASCARADO quedó fuera del universo final.")
else:
    print("ERROR: todavía existen filas ENMASCARADO.")


# ======================================================================
# 43.4 CONTROL DE LOS 135 PARTIDOS
# ======================================================================

print("\n" + "=" * 100)
print("43.4 CONTROL DE PARTIDOS")
print("=" * 100)

partidos_43 = sorted(
    fuente_ba_final_43["departamento"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .unique()
)

print("\nCantidad de partidos:")
print(len(partidos_43))

if len(partidos_43) == 135:
    print("\nOK: se obtuvieron exactamente 135 partidos.")
else:
    print(
        "\nATENCIÓN: se esperaban 135 partidos "
        f"y se obtuvieron {len(partidos_43)}."
    )


# ======================================================================
# 43.5 RECONSTRUIR MATRÍCULA SECUNDARIA
# ======================================================================

print("\n" + "=" * 100)
print("43.5 RECONSTRUIR MATRÍCULA SECUNDARIA")
print("=" * 100)

fuente_ba_final_43[
    "secundaria_7_12_43"
] = (
    fuente_ba_final_43[
        ["_7", "_8", "_9", "_10", "_11", "_12"]
    ]
    .apply(pd.to_numeric, errors="coerce")
    .fillna(0)
    .sum(axis=1)
)

secundaria_reconstruida_43 = (
    fuente_ba_final_43
    .groupby(
        "departamento",
        as_index=False
    )["secundaria_7_12_43"]
    .sum()
    .rename(
        columns={
            "secundaria_7_12_43":
            "secundaria_reconstruida_43"
        }
    )
)

print(
    secundaria_reconstruida_43
    .head(20)
    .to_string(index=False)
)


# ======================================================================
# 43.6 COMPARAR CONTRA MATRICULA_LIMPIA
# ======================================================================

print("\n" + "=" * 100)
print("43.6 COMPARACIÓN GLOBAL CONTRA MATRICULA_LIMPIA")
print("=" * 100)

# Tomamos del diagnóstico anterior la matrícula limpia
# disponible en comparacion_34.
matricula_control_43 = (
    comparacion_34[
        [
            "departamento",
            "secundaria_matricula_limpia"
        ]
    ]
    .dropna(
        subset=["secundaria_matricula_limpia"]
    )
    .drop_duplicates(
        subset=["departamento"]
    )
    .copy()
)

control_final_43 = (
    secundaria_reconstruida_43
    .merge(
        matricula_control_43,
        on="departamento",
        how="outer",
        indicator=True
    )
)

control_final_43[
    "diferencia_43"
] = (
    control_final_43[
        "secundaria_reconstruida_43"
    ]
    -
    control_final_43[
        "secundaria_matricula_limpia"
    ]
)

control_final_43[
    "coincide_43"
] = np.isclose(
    control_final_43[
        "secundaria_reconstruida_43"
    ],
    control_final_43[
        "secundaria_matricula_limpia"
    ],
    equal_nan=False
)


# ======================================================================
# 43.7 RESUMEN DE COINCIDENCIAS
# ======================================================================

print("\n" + "=" * 100)
print("43.7 RESULTADOS")
print("=" * 100)

ambos_43 = control_final_43[
    control_final_43["_merge"] == "both"
].copy()

cantidad_comparables_43 = len(ambos_43)

cantidad_coinciden_43 = int(
    ambos_43["coincide_43"].sum()
)

cantidad_no_coinciden_43 = (
    cantidad_comparables_43
    - cantidad_coinciden_43
)

print(
    "\nPartidos comparables:",
    cantidad_comparables_43
)

print(
    "Partidos que coinciden:",
    cantidad_coinciden_43
)

print(
    "Partidos que NO coinciden:",
    cantidad_no_coinciden_43
)


# ======================================================================
# 43.8 MOSTRAR DIFERENCIAS RESTANTES
# ======================================================================

diferencias_43 = ambos_43[
    ~ambos_43["coincide_43"]
].copy()

print("\n" + "=" * 100)
print("43.8 DIFERENCIAS RESTANTES")
print("=" * 100)

if diferencias_43.empty:

    print(
        "\n>>> NO QUEDAN DIFERENCIAS."
    )

    print(
        "La reconstrucción territorial coincide "
        "con matricula_limpia para todos los "
        "partidos comparables."
    )

else:

    print(
        diferencias_43[
            [
                "departamento",
                "secundaria_reconstruida_43",
                "secundaria_matricula_limpia",
                "diferencia_43"
            ]
        ]
        .sort_values(
            "diferencia_43",
            key=lambda x: abs(x),
            ascending=False
        )
        .to_string(index=False)
    )


# ======================================================================
# 43.9 ELEMENTOS PRESENTES SOLO EN UNA FUENTE
# ======================================================================

print("\n" + "=" * 100)
print("43.9 COBERTURA ENTRE FUENTES")
print("=" * 100)

solo_reconstruida_43 = control_final_43[
    control_final_43["_merge"] == "left_only"
]

solo_matricula_43 = control_final_43[
    control_final_43["_merge"] == "right_only"
]

print(
    "\nPartidos solo en reconstrucción:",
    len(solo_reconstruida_43)
)

if not solo_reconstruida_43.empty:
    print(
        solo_reconstruida_43[
            ["departamento"]
        ].to_string(index=False)
    )

print(
    "\nPartidos solo en matricula_limpia:",
    len(solo_matricula_43)
)

if not solo_matricula_43.empty:
    print(
        solo_matricula_43[
            ["departamento"]
        ].to_string(index=False)
    )


# ======================================================================
# 43.10 RESUMEN FINAL
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL CONTROL 43")
print("=" * 100)

print(
    "Partidos territoriales finales:",
    len(partidos_43)
)

print(
    "Filas ENMASCARADO:",
    cantidad_enmascarado_43
)

print(
    "Partidos comparables con matricula_limpia:",
    cantidad_comparables_43
)

print(
    "Coincidencias:",
    cantidad_coinciden_43
)

print(
    "Diferencias:",
    cantidad_no_coinciden_43
)

if (
    len(partidos_43) == 135
    and cantidad_enmascarado_43 == 0
    and cantidad_no_coinciden_43 == 0
):

    print("\n>>> VALIDACIÓN TERRITORIAL COMPLETA.")

    print(
        "El universo correcto es Provincia de Buenos Aires "
        "excluyendo la categoría ENMASCARADO."
    )

else:

    print(
        "\nTodavía existe alguna diferencia que debe "
        "revisarse antes de modificar el pipeline."
    )


print("\nIMPORTANTE:")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("CONTROL 43 FINALIZADO")
print("=" * 100)
# ======================================================================
# 44. RESOLVER ÚLTIMAS DIFERENCIAS DE COBERTURA TERRITORIAL
# ======================================================================

print("\n" + "=" * 100)
print("44. RESOLVER ÚLTIMAS DIFERENCIAS DE COBERTURA TERRITORIAL")
print("=" * 100)


# ======================================================================
# 44.1 RECONSTRUIR FUENTE FINAL VALIDADA EN EL PASO 43
# ======================================================================

if "fuente_2012_34" not in globals():
    raise NameError(
        "No existe fuente_2012_34. "
        "Ejecutá el script desde los pasos anteriores."
    )

# Creamos la fuente que validamos conceptualmente en el Paso 43:
# 1. solamente Provincia de Buenos Aires
# 2. excluyendo ENMASCARADO

fuente_final_43 = fuente_2012_34.copy()

# Normalización auxiliar para hacer el filtro de forma segura.
provincia_normalizada_44 = (
    fuente_final_43["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
)

departamento_normalizado_44 = (
    fuente_final_43["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
)

fuente_final_43 = fuente_final_43[
    (provincia_normalizada_44 == "BUENOS AIRES")
    &
    (departamento_normalizado_44 != "ENMASCARADO")
].copy()

print("\nFuente territorial reconstruida correctamente.")
print("Filas:", len(fuente_final_43))
print(
    "Partidos:",
    fuente_final_43["departamento"].nunique()
)

print("\nProvincias presentes:")
print(
    fuente_final_43["provincia"]
    .value_counts(dropna=False)
    .to_string()
)

# Controles de seguridad.
if len(fuente_final_43) != 320:
    print(
        "\nADVERTENCIA: se esperaban 320 filas "
        "según el resultado del Paso 43."
    )

if fuente_final_43["departamento"].nunique() != 135:
    print(
        "\nADVERTENCIA: se esperaban 135 partidos "
        "según el resultado del Paso 43."
    )

print("\n>>> Fuente lista para continuar el diagnóstico 44.")
# ======================================================================
# 44.2 INSPECCIONAR CASTELLI EN LA FUENTE ORIGINAL
# ======================================================================

print("\n" + "=" * 100)
print("44.2 ANALIZAR CASTELLI")
print("=" * 100)

castelli_44 = fuente_final_43[
    fuente_final_43["departamento"]
    .astype(str)
    .str.upper()
    .str.strip()
    == "CASTELLI"
].copy()

print("\nFilas de CASTELLI en la fuente final:")
print("Cantidad:", len(castelli_44))

if not castelli_44.empty:

    columnas_castelli_44 = [
        "provincia",
        "departamento",
        "sector",
        "ambito",
        "_7",
        "_8",
        "_9",
        "_10",
        "_11",
        "_12",
        "secundaria_7_12_34"
    ]

    columnas_castelli_44 = [
        c for c in columnas_castelli_44
        if c in castelli_44.columns
    ]

    print(
        castelli_44[columnas_castelli_44]
        .to_string(index=False)
    )

    if "secundaria_7_12_34" in castelli_44.columns:

        total_castelli_44 = (
            pd.to_numeric(
                castelli_44["secundaria_7_12_34"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

        print(
            "\nMatrícula secundaria reconstruida de CASTELLI:",
            total_castelli_44
        )


# ======================================================================
# 44.3 BUSCAR CASTELLI EN TODOS LOS DATAFRAMES DISPONIBLES
# ======================================================================

print("\n" + "=" * 100)
print("44.3 BUSCAR CASTELLI EN DATAFRAMES")
print("=" * 100)

resultados_castelli_44 = []

for nombre, objeto in list(globals().items()):

    if not isinstance(objeto, pd.DataFrame):
        continue

    for columna in objeto.columns:

        nombre_col = str(columna).lower()

        if (
            "partido" not in nombre_col
            and "departamento" not in nombre_col
        ):
            continue

        try:

            serie = (
                objeto[columna]
                .astype(str)
                .str.upper()
                .str.strip()
            )

            cantidad = (
                serie == "CASTELLI"
            ).sum()

            if cantidad > 0:

                resultados_castelli_44.append(
                    {
                        "dataframe": nombre,
                        "columna": columna,
                        "cantidad": int(cantidad)
                    }
                )

        except Exception:
            pass

df_castelli_busqueda_44 = pd.DataFrame(
    resultados_castelli_44
)

if not df_castelli_busqueda_44.empty:

    print(
        df_castelli_busqueda_44
        .sort_values(["dataframe", "columna"])
        .to_string(index=False)
    )

else:
    print("CASTELLI no fue encontrado en otros DataFrames.")


# ======================================================================
# 44.4 ANALIZAR CORONEL ROSALES
# ======================================================================

print("\n" + "=" * 100)
print("44.4 ANALIZAR CORONEL ROSALES")
print("=" * 100)

patron_rosales_44 = "ROSALES"

resultados_rosales_44 = []

for nombre, objeto in list(globals().items()):

    if not isinstance(objeto, pd.DataFrame):
        continue

    for columna in objeto.columns:

        nombre_col = str(columna).lower()

        if (
            "partido" not in nombre_col
            and "departamento" not in nombre_col
        ):
            continue

        try:

            serie = (
                objeto[columna]
                .astype(str)
                .str.upper()
                .str.strip()
            )

            mascara = serie.str.contains(
                patron_rosales_44,
                na=False
            )

            if mascara.any():

                valores = (
                    objeto.loc[mascara, columna]
                    .astype(str)
                    .drop_duplicates()
                    .tolist()
                )

                resultados_rosales_44.append(
                    {
                        "dataframe": nombre,
                        "columna": columna,
                        "cantidad": int(mascara.sum()),
                        "valores": valores
                    }
                )

        except Exception:
            pass

df_rosales_busqueda_44 = pd.DataFrame(
    resultados_rosales_44
)

if not df_rosales_busqueda_44.empty:

    print(
        df_rosales_busqueda_44
        .to_string(index=False)
    )

else:
    print("No se encontraron variantes de ROSALES.")


# ======================================================================
# 44.5 MOSTRAR REGISTROS DE ROSALES EN LA FUENTE FINAL
# ======================================================================

rosales_fuente_44 = fuente_final_43[
    fuente_final_43["departamento"]
    .astype(str)
    .str.upper()
    .str.contains(
        "ROSALES",
        na=False
    )
].copy()

print("\nFilas de ROSALES en fuente_final_43:")

if not rosales_fuente_44.empty:

    columnas_rosales_44 = [
        "provincia",
        "departamento",
        "sector",
        "ambito",
        "_7",
        "_8",
        "_9",
        "_10",
        "_11",
        "_12",
        "secundaria_7_12_34"
    ]

    columnas_rosales_44 = [
        c for c in columnas_rosales_44
        if c in rosales_fuente_44.columns
    ]

    print(
        rosales_fuente_44[columnas_rosales_44]
        .to_string(index=False)
    )

    if "secundaria_7_12_34" in rosales_fuente_44.columns:

        total_rosales_44 = (
            pd.to_numeric(
                rosales_fuente_44[
                    "secundaria_7_12_34"
                ],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

        print(
            "\nMatrícula secundaria reconstruida de ROSALES:",
            total_rosales_44
        )

else:
    print("No se encontró ROSALES en fuente_final_43.")


# ======================================================================
# 44.6 COMPARAR VARIANTES DE NOMBRE
# ======================================================================

print("\n" + "=" * 100)
print("44.6 COMPARAR VARIANTES DEL NOMBRE CORONEL ROSALES")
print("=" * 100)

variantes_rosales_44 = set()

for resultado in resultados_rosales_44:

    for valor in resultado["valores"]:
        variantes_rosales_44.add(valor)

print("\nVariantes encontradas:")

for valor in sorted(variantes_rosales_44):
    print("-", valor)

if len(variantes_rosales_44) > 1:

    print(
        "\n>>> Se encontraron distintas formas de escribir "
        "el mismo territorio."
    )

    print(
        "Esto es compatible con un problema de normalización "
        "del nombre del partido."
    )

else:

    print(
        "\nNo se detectaron múltiples variantes automáticamente."
    )


# ======================================================================
# 44.7 BUSCAR CASTELLI Y ROSALES EN DATASET_MAESTRO
# ======================================================================

print("\n" + "=" * 100)
print("44.7 CONTROL EN DATASET_MAESTRO")
print("=" * 100)

if "dataset_maestro" in globals():

    columnas_territoriales_44 = [
        c for c in dataset_maestro.columns
        if (
            "partido" in str(c).lower()
            or "departamento" in str(c).lower()
        )
    ]

    print(
        "\nColumnas territoriales encontradas:",
        columnas_territoriales_44
    )

    for columna in columnas_territoriales_44:

        serie = (
            dataset_maestro[columna]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        mascara = (
            serie.eq("CASTELLI")
            | serie.str.contains(
                "ROSALES",
                na=False
            )
        )

        if mascara.any():

            print(
                f"\nRegistros encontrados usando '{columna}':"
            )

            columnas_mostrar = [
                columna
            ] + [
                c for c in dataset_maestro.columns
                if "matricula" in str(c).lower()
            ]

            columnas_mostrar = list(
                dict.fromkeys(columnas_mostrar)
            )

            print(
                dataset_maestro.loc[
                    mascara,
                    columnas_mostrar
                ].to_string(index=False)
            )

else:

    print(
        "dataset_maestro no está disponible actualmente."
    )


# ======================================================================
# 44.8 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL DIAGNÓSTICO 44")
print("=" * 100)

print(
    "Filas CASTELLI en fuente final:",
    len(castelli_44)
)

print(
    "Filas ROSALES en fuente final:",
    len(rosales_fuente_44)
)

print(
    "Variantes territoriales de ROSALES encontradas:",
    len(variantes_rosales_44)
)

print("\nObjetivo:")
print(
    "determinar por qué CASTELLI no aparece en matricula_limpia "
    "y confirmar si las dos denominaciones de CORONEL ROSALES "
    "corresponden al mismo partido."
)

print("\nIMPORTANTE:")
print("NO se modificó ningún nombre.")
print("NO se eliminó CASTELLI.")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.csv.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("DIAGNÓSTICO 44 FINALIZADO")
print("=" * 100)

# ======================================================================
# 45. APLICAR Y VALIDAR CORRECCIONES TERRITORIALES DEFINITIVAS
# ======================================================================

import pandas as pd
import numpy as np

print("\n" + "=" * 100)
print("45. APLICAR Y VALIDAR CORRECCIONES TERRITORIALES DEFINITIVAS")
print("=" * 100)


# ======================================================================
# 45.1 PARTIR DE LA FUENTE TERRITORIAL YA VALIDADA
# ======================================================================

if "fuente_final_43" not in globals():
    raise NameError(
        "No existe fuente_final_43. Ejecutá primero el Paso 44."
    )

fuente_corregida_45 = fuente_final_43.copy()

print("\nFilas iniciales:", len(fuente_corregida_45))
print(
    "Partidos iniciales:",
    fuente_corregida_45["departamento"].nunique()
)


# ======================================================================
# 45.2 NORMALIZAR CORONEL ROSALES
# ======================================================================

fuente_corregida_45["departamento"] = (
    fuente_corregida_45["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
)

mapa_nombres_45 = {
    "CORONEL DE MARINA L ROSALES":
        "CORONEL DE MARINA LEONARDO ROSALES"
}

fuente_corregida_45["departamento"] = (
    fuente_corregida_45["departamento"]
    .replace(mapa_nombres_45)
)

print("\n" + "=" * 100)
print("45.2 CONTROL DE CORONEL ROSALES")
print("=" * 100)

rosales_45 = fuente_corregida_45[
    fuente_corregida_45["departamento"]
    .str.contains("ROSALES", na=False)
]

print(rosales_45[
    [
        "provincia",
        "departamento",
        "sector",
        "ambito",
        "secundaria_7_12_34"
    ]
].to_string(index=False))

print(
    "\nMatrícula secundaria reconstruida:",
    rosales_45["secundaria_7_12_34"].sum()
)

variantes_rosales_45 = (
    fuente_corregida_45.loc[
        fuente_corregida_45["departamento"]
        .str.contains("ROSALES", na=False),
        "departamento"
    ]
    .unique()
)

print("\nVariantes restantes:")
print(variantes_rosales_45)


# ======================================================================
# 45.3 CONTROLAR CASTELLI
# ======================================================================

print("\n" + "=" * 100)
print("45.3 CONTROL DE CASTELLI")
print("=" * 100)

castelli_45 = fuente_corregida_45[
    fuente_corregida_45["departamento"] == "CASTELLI"
].copy()

print("\nFilas de CASTELLI:")
print(
    castelli_45[
        [
            "provincia",
            "departamento",
            "sector",
            "ambito",
            "_7",
            "_8",
            "_9",
            "_10",
            "_11",
            "_12",
            "secundaria_7_12_34"
        ]
    ].to_string(index=False)
)

print(
    "\nMatrícula secundaria reconstruida:",
    castelli_45["secundaria_7_12_34"].sum()
)

print(
    "\nCASTELLI se conserva como partido."
)
print(
    "No se elimina ni se imputa matrícula en este paso."
)


# ======================================================================
# 45.4 RECONSTRUIR SECUNDARIA POR PARTIDO
# ======================================================================

secundaria_corregida_45 = (
    fuente_corregida_45
    .groupby("departamento", as_index=False)[
        "secundaria_7_12_34"
    ]
    .sum(min_count=1)
    .rename(
        columns={
            "secundaria_7_12_34":
                "secundaria_reconstruida_45"
        }
    )
)

print("\n" + "=" * 100)
print("45.4 COBERTURA TERRITORIAL FINAL")
print("=" * 100)

print(
    "\nCantidad de partidos:",
    secundaria_corregida_45["departamento"].nunique()
)

if secundaria_corregida_45["departamento"].nunique() == 135:
    print(">>> OK: quedaron exactamente 135 partidos.")
else:
    print(
        ">>> ADVERTENCIA: no quedaron exactamente 135 partidos."
    )


# ======================================================================
# 45.5 BUSCAR DUPLICADOS TERRITORIALES
# ======================================================================

conteo_45 = (
    secundaria_corregida_45["departamento"]
    .value_counts()
)

duplicados_45 = conteo_45[
    conteo_45 > 1
]

print("\n" + "=" * 100)
print("45.5 CONTROL DE DUPLICADOS")
print("=" * 100)

if len(duplicados_45) == 0:
    print("\n>>> OK: no hay partidos duplicados.")
else:
    print("\nPartidos duplicados:")
    print(duplicados_45.to_string())


# ======================================================================
# 45.6 COMPARAR CONTRA MATRICULA_LIMPIA
# ======================================================================

print("\n" + "=" * 100)
print("45.6 COMPARACIÓN CONTRA MATRICULA_LIMPIA")
print("=" * 100)

if "matricula_limpia" in globals():

    ml_45 = matricula_limpia.copy()

    ml_45["partido"] = (
        ml_45["partido"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace(mapa_nombres_45)
    )

    # Detectar automáticamente la columna secundaria 2012
    columnas_sec_45 = [
        c for c in ml_45.columns
        if "secund" in str(c).lower()
    ]

    print(
        "\nColumnas candidatas de secundaria:",
        columnas_sec_45
    )

    # Usamos el mismo valor previamente identificado si existe.
    candidatos_2012_45 = [
        c for c in columnas_sec_45
        if "2012" in str(c)
    ]

    if len(candidatos_2012_45) > 0:
        columna_ml_45 = candidatos_2012_45[0]
    elif "matricula_secundaria" in ml_45.columns:
        columna_ml_45 = "matricula_secundaria"
    else:
        columna_ml_45 = None

    if columna_ml_45 is not None:

        print(
            "Columna utilizada:",
            columna_ml_45
        )

        control_45 = secundaria_corregida_45.merge(
            ml_45[
                ["partido", columna_ml_45]
            ],
            left_on="departamento",
            right_on="partido",
            how="outer",
            indicator=True
        )

        control_45["diferencia_45"] = (
            control_45["secundaria_reconstruida_45"]
            -
            pd.to_numeric(
                control_45[columna_ml_45],
                errors="coerce"
            )
        )

        print("\nCobertura del merge:")
        print(
            control_45["_merge"]
            .value_counts(dropna=False)
            .to_string()
        )

        solo_reconstruida_45 = control_45[
            control_45["_merge"] == "left_only"
        ]

        solo_limpia_45 = control_45[
            control_45["_merge"] == "right_only"
        ]

        print("\nSolo en reconstrucción:")
        if len(solo_reconstruida_45) == 0:
            print("Ninguno.")
        else:
            print(
                solo_reconstruida_45[
                    [
                        "departamento",
                        "secundaria_reconstruida_45"
                    ]
                ].to_string(index=False)
            )

        print("\nSolo en matricula_limpia:")
        if len(solo_limpia_45) == 0:
            print("Ninguno.")
        else:
            print(
                solo_limpia_45[
                    [
                        "partido",
                        columna_ml_45
                    ]
                ].to_string(index=False)
            )

    else:
        print(
            "\nNo se pudo identificar automáticamente "
            "la columna secundaria de matricula_limpia."
        )

else:
    print("\nNo existe matricula_limpia en memoria.")


# ======================================================================
# 45.7 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL PASO 45")
print("=" * 100)

print(
    "Filas territoriales:",
    len(fuente_corregida_45)
)

print(
    "Partidos únicos:",
    fuente_corregida_45["departamento"].nunique()
)

print(
    "Variantes de Coronel Rosales restantes:",
    len(variantes_rosales_45)
)

print(
    "Filas de Castelli:",
    len(castelli_45)
)

print("\nCorrecciones aplicadas EN COPIA:")
print(
    "- Provincia: únicamente Buenos Aires."
)
print(
    "- ENMASCARADO: excluido."
)
print(
    "- CORONEL DE MARINA L ROSALES -> "
    "CORONEL DE MARINA LEONARDO ROSALES."
)
print(
    "- CASTELLI: conservado como partido."
)

print("\nIMPORTANTE:")
print("NO se realizó ninguna imputación.")
print("NO se modificó fuente_2012_34.")
print("NO se modificó matricula_limpia.")
print("NO se modificó dataset_maestro.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("PASO 45 FINALIZADO")
print("=" * 100)

# ======================================================================
# 46. PREPARAR APLICACIÓN DEFINITIVA AL PIPELINE
# ======================================================================

import pandas as pd
import numpy as np

print("\n" + "=" * 100)
print("46. PREPARAR APLICACIÓN DEFINITIVA AL PIPELINE")
print("=" * 100)


# ======================================================================
# 46.1 CONTROLAR OBJETOS NECESARIOS
# ======================================================================

objetos_necesarios_46 = [
    "fuente_2012_34",
    "fuente_corregida_45",
    "matricula_limpia",
    "dataset_maestro"
]

for nombre in objetos_necesarios_46:
    if nombre in globals():
        obj = globals()[nombre]

        if isinstance(obj, pd.DataFrame):
            print(
                f"{nombre}: OK | "
                f"filas={len(obj)} | columnas={len(obj.columns)}"
            )
        else:
            print(f"{nombre}: existe pero no es DataFrame")
    else:
        print(f"{nombre}: NO EXISTE")


# ======================================================================
# 46.2 ESTRUCTURA REAL DE MATRICULA_LIMPIA
# ======================================================================

print("\n" + "=" * 100)
print("46.2 ESTRUCTURA DE MATRICULA_LIMPIA")
print("=" * 100)

if "matricula_limpia" not in globals():
    raise NameError("No existe matricula_limpia.")

print("\nColumnas:")
for i, col in enumerate(matricula_limpia.columns, start=1):
    print(f"{i:03d}. {col}")

print("\nPrimeras 10 filas:")
print(
    matricula_limpia
    .head(10)
    .to_string(index=False)
)

print("\nTipos de datos:")
print(
    matricula_limpia
    .dtypes
    .to_string()
)


# ======================================================================
# 46.3 IDENTIFICAR ESTRUCTURA TEMPORAL
# ======================================================================

print("\n" + "=" * 100)
print("46.3 IDENTIFICAR AÑO Y NIVEL")
print("=" * 100)

columnas_anio_46 = [
    c for c in matricula_limpia.columns
    if (
        "anio" in str(c).lower()
        or "año" in str(c).lower()
        or "year" in str(c).lower()
    )
]

columnas_nivel_46 = [
    c for c in matricula_limpia.columns
    if (
        "nivel" in str(c).lower()
        or "tipo" in str(c).lower()
    )
]

columnas_valor_46 = [
    c for c in matricula_limpia.columns
    if pd.api.types.is_numeric_dtype(matricula_limpia[c])
]

print("Columnas candidatas de año:")
print(columnas_anio_46)

print("\nColumnas candidatas de nivel:")
print(columnas_nivel_46)

print("\nColumnas numéricas:")
print(columnas_valor_46)


# ======================================================================
# 46.4 INSPECCIONAR CASTELLI Y CORONEL ROSALES
# ======================================================================

print("\n" + "=" * 100)
print("46.4 CASTELLI Y CORONEL ROSALES EN MATRICULA_LIMPIA")
print("=" * 100)

if "partido" in matricula_limpia.columns:

    partidos_norm_46 = (
        matricula_limpia["partido"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    casos_46 = matricula_limpia[
        partidos_norm_46.str.contains(
            "CASTELLI|ROSALES",
            regex=True,
            na=False
        )
    ].copy()

    print(
        casos_46.to_string(index=False)
        if len(casos_46) > 0
        else "No se encontraron registros."
    )

else:
    print("No existe columna 'partido'.")


# ======================================================================
# 46.5 INSPECCIONAR DATASET_MAESTRO
# ======================================================================

print("\n" + "=" * 100)
print("46.5 ESTRUCTURA TERRITORIAL/TEMPORAL DEL DATASET_MAESTRO")
print("=" * 100)

if "dataset_maestro" not in globals():
    raise NameError("No existe dataset_maestro.")

columnas_clave_46 = []

for col in dataset_maestro.columns:
    texto = str(col).lower()

    if any(
        palabra in texto
        for palabra in [
            "partido",
            "provincia",
            "anio",
            "año",
            "matricula"
        ]
    ):
        columnas_clave_46.append(col)

print("\nColumnas relevantes:")
for col in columnas_clave_46:
    print("-", col)

print("\nDimensión actual:")
print("Filas:", len(dataset_maestro))

if "partido" in dataset_maestro.columns:
    print(
        "Partidos únicos:",
        dataset_maestro["partido"].nunique()
    )


# ======================================================================
# 46.6 VERIFICAR NORMALIZACIÓN DE ROSALES EN EL MAESTRO
# ======================================================================

print("\n" + "=" * 100)
print("46.6 CONTROL DE ROSALES EN DATASET_MAESTRO")
print("=" * 100)

if "partido" in dataset_maestro.columns:

    rosales_maestro_46 = dataset_maestro[
        dataset_maestro["partido"]
        .astype(str)
        .str.upper()
        .str.contains("ROSALES", na=False)
    ]

    print(
        rosales_maestro_46[
            columnas_clave_46
        ].head(30).to_string(index=False)
        if len(rosales_maestro_46) > 0
        else "No se encontró ROSALES."
    )


# ======================================================================
# 46.7 CONTROL DE LOS 135 PARTIDOS CONTRA EL MAESTRO
# ======================================================================

print("\n" + "=" * 100)
print("46.7 COBERTURA DE LOS 135 PARTIDOS")
print("=" * 100)

partidos_correctos_46 = set(
    fuente_corregida_45["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
)

partidos_maestro_46 = set(
    dataset_maestro["partido"]
    .astype(str)
    .str.strip()
    .str.upper()
)

solo_fuente_46 = sorted(
    partidos_correctos_46 - partidos_maestro_46
)

solo_maestro_46 = sorted(
    partidos_maestro_46 - partidos_correctos_46
)

print(
    "Partidos territoriales correctos:",
    len(partidos_correctos_46)
)

print(
    "Partidos únicos en dataset_maestro:",
    len(partidos_maestro_46)
)

print("\nPartidos correctos ausentes del maestro:")
print(
    solo_fuente_46
    if solo_fuente_46
    else "Ninguno."
)

print("\nPartidos del maestro fuera del universo correcto:")
print(
    solo_maestro_46
    if solo_maestro_46
    else "Ninguno."
)


# ======================================================================
# 46.8 REGLAS DEFINITIVAS IDENTIFICADAS
# ======================================================================

print("\n" + "=" * 100)
print("46.8 REGLAS TERRITORIALES DEFINITIVAS")
print("=" * 100)

print("""
REGLA 1
Conservar únicamente:
provincia == 'Buenos Aires'

REGLA 2
Excluir:
departamento == 'ENMASCARADO'

REGLA 3
Normalizar:
'CORONEL DE MARINA L ROSALES'
->
'CORONEL DE MARINA LEONARDO ROSALES'

REGLA 4
CASTELLI se conserva como partido.
No imputar automáticamente secundaria cuando la fuente
original no informa _7 a _12.

REGLA 5
El filtro territorial debe ejecutarse ANTES de agrupar
por departamento.
""")


# ======================================================================
# 46.9 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL PASO 46")
print("=" * 100)

print("""
Este paso NO modifica todavía el pipeline.

Su objetivo es mostrar la estructura exacta de
matricula_limpia y dataset_maestro antes de aplicar
la corrección definitiva.

NO se realizó ninguna imputación.
NO se modificó matricula_limpia.
NO se modificó dataset_maestro.
NO se guardó ningún archivo.
""")

print("=" * 100)
print("PASO 46 FINALIZADO")
print("=" * 100)
# ======================================================================
# 47. CONTROL FINAL DE NORMALIZACIÓN DE LOS 135 PARTIDOS
# ======================================================================

import pandas as pd
import numpy as np
import unicodedata
import re
from difflib import SequenceMatcher

print("\n" + "=" * 100)
print("47. CONTROL FINAL DE NORMALIZACIÓN DE LOS 135 PARTIDOS")
print("=" * 100)


# ======================================================================
# 47.1 FUNCIÓN DE NORMALIZACIÓN SOLO PARA COMPARAR
# ======================================================================

def normalizar_nombre_47(texto):
    if pd.isna(texto):
        return ""

    texto = str(texto).strip().upper()

    # Quitar tildes solamente para detectar equivalencias
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    # Dejar letras, números y espacios
    texto = re.sub(r"[^A-Z0-9 ]", " ", texto)

    # Unificar espacios
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


# ======================================================================
# 47.2 OBTENER LOS DOS UNIVERSOS DE 135 PARTIDOS
# ======================================================================

partidos_fuente_47 = sorted(
    fuente_corregida_45["departamento"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .unique()
)

partidos_maestro_47 = sorted(
    dataset_maestro["partido"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .unique()
)

print("\nPartidos en fuente territorial:", len(partidos_fuente_47))
print("Partidos en dataset_maestro:", len(partidos_maestro_47))


# ======================================================================
# 47.3 COMPARACIÓN EXACTA
# ======================================================================

set_fuente_47 = set(partidos_fuente_47)
set_maestro_47 = set(partidos_maestro_47)

solo_fuente_47 = sorted(
    set_fuente_47 - set_maestro_47
)

solo_maestro_47 = sorted(
    set_maestro_47 - set_fuente_47
)

print("\n" + "=" * 100)
print("47.3 DIFERENCIAS EXACTAS")
print("=" * 100)

print("\nSolo en fuente:")
print(
    solo_fuente_47
    if solo_fuente_47
    else "Ninguno."
)

print("\nSolo en maestro:")
print(
    solo_maestro_47
    if solo_maestro_47
    else "Ninguno."
)


# ======================================================================
# 47.4 COMPARACIÓN SIN TILDES
# ======================================================================

print("\n" + "=" * 100)
print("47.4 COMPARACIÓN NORMALIZADA SIN TILDES")
print("=" * 100)

mapa_fuente_47 = {
    normalizar_nombre_47(p): p
    for p in partidos_fuente_47
}

mapa_maestro_47 = {
    normalizar_nombre_47(p): p
    for p in partidos_maestro_47
}

claves_fuente_47 = set(mapa_fuente_47)
claves_maestro_47 = set(mapa_maestro_47)

equivalencias_47 = []

for clave in sorted(
    claves_fuente_47.intersection(claves_maestro_47)
):
    nombre_fuente = mapa_fuente_47[clave]
    nombre_maestro = mapa_maestro_47[clave]

    if nombre_fuente != nombre_maestro:
        equivalencias_47.append(
            {
                "fuente": nombre_fuente,
                "maestro": nombre_maestro,
                "normalizado": clave
            }
        )

if equivalencias_47:
    equivalencias_df_47 = pd.DataFrame(equivalencias_47)

    print("\nNombres distintos pero equivalentes al quitar tildes:")
    print(
        equivalencias_df_47.to_string(index=False)
    )
else:
    equivalencias_df_47 = pd.DataFrame()

    print(
        "\nNo se encontraron diferencias explicadas "
        "únicamente por tildes."
    )


# ======================================================================
# 47.5 DIFERENCIAS QUE SIGUEN SIN EXPLICARSE
# ======================================================================

faltan_fuente_norm_47 = sorted(
    claves_fuente_47 - claves_maestro_47
)

faltan_maestro_norm_47 = sorted(
    claves_maestro_47 - claves_fuente_47
)

print("\n" + "=" * 100)
print("47.5 DIFERENCIAS DESPUÉS DE NORMALIZAR")
print("=" * 100)

print("\nSolo fuente después de normalizar:")
print(
    [
        mapa_fuente_47[x]
        for x in faltan_fuente_norm_47
    ]
    if faltan_fuente_norm_47
    else "Ninguno."
)

print("\nSolo maestro después de normalizar:")
print(
    [
        mapa_maestro_47[x]
        for x in faltan_maestro_norm_47
    ]
    if faltan_maestro_norm_47
    else "Ninguno."
)


# ======================================================================
# 47.6 BUSCAR NOMBRES MUY PARECIDOS
# ======================================================================

print("\n" + "=" * 100)
print("47.6 POSIBLES EQUIVALENCIAS POR SIMILITUD")
print("=" * 100)

candidatos_47 = []

for clave_fuente in faltan_fuente_norm_47:

    mejor_nombre = None
    mejor_ratio = 0

    for clave_maestro in faltan_maestro_norm_47:

        ratio = SequenceMatcher(
            None,
            clave_fuente,
            clave_maestro
        ).ratio()

        if ratio > mejor_ratio:
            mejor_ratio = ratio
            mejor_nombre = clave_maestro

    if mejor_nombre is not None:

        candidatos_47.append(
            {
                "fuente":
                    mapa_fuente_47[clave_fuente],

                "posible_maestro":
                    mapa_maestro_47[mejor_nombre],

                "similitud":
                    round(mejor_ratio, 4)
            }
        )


if candidatos_47:

    candidatos_df_47 = pd.DataFrame(
        candidatos_47
    ).sort_values(
        "similitud",
        ascending=False
    )

    print(
        candidatos_df_47.to_string(index=False)
    )

else:
    candidatos_df_47 = pd.DataFrame()

    print(
        "No quedaron nombres para comparar."
    )


# ======================================================================
# 47.7 CONTROL ESPECÍFICO DE CAÑUELAS
# ======================================================================

print("\n" + "=" * 100)
print("47.7 CONTROL ESPECÍFICO DE CAÑUELAS")
print("=" * 100)

print(
    "CAÑUELAS en fuente:",
    "CAÑUELAS" in set_fuente_47
)

print(
    "CANUELAS en maestro:",
    "CANUELAS" in set_maestro_47
)

print(
    "CAÑUELAS en maestro:",
    "CAÑUELAS" in set_maestro_47
)


# ======================================================================
# 47.8 SIMULAR NORMALIZACIONES CONOCIDAS
# ======================================================================

print("\n" + "=" * 100)
print("47.8 SIMULAR NORMALIZACIONES DEFINITIVAS")
print("=" * 100)

mapa_definitivo_47 = {

    "CORONEL DE MARINA L ROSALES":
        "CORONEL DE MARINA LEONARDO ROSALES",

    "CANUELAS":
        "CAÑUELAS"
}


fuente_simulada_47 = fuente_corregida_45.copy()

fuente_simulada_47["departamento"] = (
    fuente_simulada_47["departamento"]
    .replace(mapa_definitivo_47)
)


maestro_simulado_47 = dataset_maestro.copy()

maestro_simulado_47["partido"] = (
    maestro_simulado_47["partido"]
    .astype(str)
    .str.strip()
    .str.upper()
    .replace(mapa_definitivo_47)
)


partidos_fuente_sim_47 = set(
    fuente_simulada_47["departamento"].unique()
)

partidos_maestro_sim_47 = set(
    maestro_simulado_47["partido"].unique()
)


print(
    "\nPartidos fuente después de simulación:",
    len(partidos_fuente_sim_47)
)

print(
    "Partidos maestro después de simulación:",
    len(partidos_maestro_sim_47)
)

print(
    "\nSolo fuente después de simulación:",
    sorted(
        partidos_fuente_sim_47 -
        partidos_maestro_sim_47
    )
)

print(
    "\nSolo maestro después de simulación:",
    sorted(
        partidos_maestro_sim_47 -
        partidos_fuente_sim_47
    )
)


if (
    len(partidos_fuente_sim_47) == 135
    and
    len(partidos_maestro_sim_47) == 135
    and
    partidos_fuente_sim_47 == partidos_maestro_sim_47
):

    print(
        "\n>>> VALIDACIÓN PERFECTA:"
    )

    print(
        "Los dos universos contienen exactamente "
        "los mismos 135 partidos."
    )

else:

    print(
        "\n>>> Todavía quedan diferencias de nombres."
    )


# ======================================================================
# 47.9 RESUMEN
# ======================================================================

print("\n" + "=" * 100)
print("RESUMEN DEL PASO 47")
print("=" * 100)

print(
    "Partidos fuente:",
    len(partidos_fuente_47)
)

print(
    "Partidos maestro:",
    len(partidos_maestro_47)
)

print(
    "Diferencias exactas fuente:",
    len(solo_fuente_47)
)

print(
    "Diferencias exactas maestro:",
    len(solo_maestro_47)
)

print(
    "Equivalencias detectadas por normalización:",
    len(equivalencias_df_47)
)

print(
    "Diferencias restantes después de quitar tildes:",
    len(faltan_fuente_norm_47),
    "/",
    len(faltan_maestro_norm_47)
)

print("\nIMPORTANTE:")
print("Este paso es solamente de validación.")
print("NO se modificó dataset_maestro.")
print("NO se modificó matricula_limpia.")
print("NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("PASO 47 FINALIZADO")
print("=" * 100)

# ============================================================
# PASO 48 - APLICAR CORRECCIONES TERRITORIALES DEFINITIVAS
# ============================================================

print("\n" + "=" * 100)
print("48. APLICAR CORRECCIONES TERRITORIALES DEFINITIVAS")
print("=" * 100)

# ------------------------------------------------------------
# 48.1 NORMALIZAR NOMBRES EN MATRICULA_LIMPIA
# ------------------------------------------------------------

matricula_limpia["partido"] = (
    matricula_limpia["partido"]
    .astype(str)
    .str.strip()
    .str.upper()
)

matricula_limpia["partido"] = matricula_limpia["partido"].replace({
    "CAÑUELAS": "CANUELAS",
    "CORONEL DE MARINA L ROSALES": "CORONEL DE MARINA LEONARDO ROSALES"
})

print("\nNormalización aplicada en matricula_limpia.")


# ------------------------------------------------------------
# 48.2 NORMALIZAR NOMBRES EN DATASET_MAESTRO
# ------------------------------------------------------------

dataset_maestro["partido"] = (
    dataset_maestro["partido"]
    .astype(str)
    .str.strip()
    .str.upper()
)

dataset_maestro["partido"] = dataset_maestro["partido"].replace({
    "CAÑUELAS": "CANUELAS",
    "CORONEL DE MARINA L ROSALES": "CORONEL DE MARINA LEONARDO ROSALES"
})

print("Normalización aplicada en dataset_maestro.")


# ------------------------------------------------------------
# 48.3 CONSTRUIR UNIVERSO TERRITORIAL CORRECTO
# ------------------------------------------------------------

fuente_final_48 = fuente_2012_34.copy()

fuente_final_48["_provincia_norm_48"] = (
    fuente_final_48["provincia"]
    .astype(str)
    .str.strip()
    .str.upper()
)

fuente_final_48["departamento"] = (
    fuente_final_48["departamento"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Solo Provincia de Buenos Aires
fuente_final_48 = fuente_final_48[
    fuente_final_48["_provincia_norm_48"] == "BUENOS AIRES"
].copy()

# Excluir categoría ENMASCARADO
fuente_final_48 = fuente_final_48[
    fuente_final_48["departamento"] != "ENMASCARADO"
].copy()

# Normalizaciones territoriales
fuente_final_48["departamento"] = fuente_final_48["departamento"].replace({
    "CAÑUELAS": "CANUELAS",
    "CORONEL DE MARINA L ROSALES": "CORONEL DE MARINA LEONARDO ROSALES"
})

print("\nFuente territorial corregida.")
print("Filas:", len(fuente_final_48))
print(
    "Partidos:",
    fuente_final_48["departamento"].nunique()
)


# ------------------------------------------------------------
# 48.4 CONTROL DE UNIVERSO TERRITORIAL
# ------------------------------------------------------------

partidos_fuente_48 = set(
    fuente_final_48["departamento"].dropna().unique()
)

partidos_maestro_48 = set(
    dataset_maestro["partido"].dropna().unique()
)

solo_fuente_48 = sorted(
    partidos_fuente_48 - partidos_maestro_48
)

solo_maestro_48 = sorted(
    partidos_maestro_48 - partidos_fuente_48
)

print("\n" + "=" * 100)
print("48.4 CONTROL DE LOS 135 PARTIDOS")
print("=" * 100)

print("\nPartidos fuente:", len(partidos_fuente_48))
print("Partidos maestro:", len(partidos_maestro_48))

print("\nSolo en fuente:")
print(solo_fuente_48 if solo_fuente_48 else "Ninguno")

print("\nSolo en maestro:")
print(solo_maestro_48 if solo_maestro_48 else "Ninguno")


# ------------------------------------------------------------
# 48.5 CONTROL DE PROVINCIA
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("48.5 CONTROL DE PROVINCIA")
print("=" * 100)

print(
    fuente_final_48["provincia"]
    .value_counts(dropna=False)
    .to_string()
)


# ------------------------------------------------------------
# 48.6 CONTROL ENMASCARADO
# ------------------------------------------------------------

cantidad_enmascarado_48 = (
    fuente_final_48["departamento"] == "ENMASCARADO"
).sum()

print("\n" + "=" * 100)
print("48.6 CONTROL DE ENMASCARADO")
print("=" * 100)

print(
    "Filas ENMASCARADO restantes:",
    cantidad_enmascarado_48
)


# ------------------------------------------------------------
# 48.7 CONTROL CORONEL ROSALES
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("48.7 CONTROL CORONEL ROSALES")
print("=" * 100)

rosales_48 = sorted([
    x for x in partidos_fuente_48
    if "ROSALES" in str(x)
])

print("Variantes encontradas:")
print(rosales_48)


# ------------------------------------------------------------
# 48.8 CONTROL CAÑUELAS / CANUELAS
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("48.8 CONTROL CAÑUELAS / CANUELAS")
print("=" * 100)

print(
    "CANUELAS en fuente:",
    "CANUELAS" in partidos_fuente_48
)

print(
    "CANUELAS en maestro:",
    "CANUELAS" in partidos_maestro_48
)

print(
    "CAÑUELAS en fuente:",
    "CAÑUELAS" in partidos_fuente_48
)

print(
    "CAÑUELAS en maestro:",
    "CAÑUELAS" in partidos_maestro_48
)


# ------------------------------------------------------------
# 48.9 VALIDACIÓN FINAL
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("48.9 VALIDACIÓN FINAL")
print("=" * 100)

condiciones_48 = {
    "135 partidos en fuente":
        len(partidos_fuente_48) == 135,

    "135 partidos en maestro":
        len(partidos_maestro_48) == 135,

    "Universos idénticos":
        partidos_fuente_48 == partidos_maestro_48,

    "Sin ENMASCARADO":
        cantidad_enmascarado_48 == 0,

    "Una sola variante de Rosales":
        rosales_48 == [
            "CORONEL DE MARINA LEONARDO ROSALES"
        ],

    "CANUELAS normalizado":
        (
            "CANUELAS" in partidos_fuente_48
            and "CANUELAS" in partidos_maestro_48
            and "CAÑUELAS" not in partidos_fuente_48
            and "CAÑUELAS" not in partidos_maestro_48
        )
}

for nombre, resultado in condiciones_48.items():
    print(
        f"{nombre}:",
        "OK" if resultado else "ERROR"
    )


todo_ok_48 = all(condiciones_48.values())

print("\n" + "=" * 100)

if todo_ok_48:
    print(">>> VALIDACIÓN TERRITORIAL FINAL EXITOSA.")
    print(">>> LOS 135 PARTIDOS COINCIDEN PERFECTAMENTE.")
else:
    print(">>> QUEDAN PROBLEMAS POR REVISAR.")

print("=" * 100)

print("\nIMPORTANTE:")
print("Las correcciones fueron aplicadas en memoria.")
print("Todavía NO se guardó ningún archivo.")

print("\n" + "=" * 100)
print("PASO 48 FINALIZADO")
print("=" * 100)
# ============================================================
# PASO 49 - GUARDAR Y VALIDAR DATASETS DEFINITIVOS
# ============================================================

import os
import pandas as pd

print("\n" + "=" * 100)
print("49. GUARDAR Y VALIDAR DATASETS DEFINITIVOS")
print("=" * 100)


# ------------------------------------------------------------
# 49.1 DEFINIR ARCHIVOS DE SALIDA
# ------------------------------------------------------------

archivo_matricula_49 = "matricula_limpia_final.csv"
archivo_maestro_49 = "dataset_maestro_final.csv"

print("\nArchivos que se van a generar:")
print("-", archivo_matricula_49)
print("-", archivo_maestro_49)


# ------------------------------------------------------------
# 49.2 CONTROLES ANTES DE GUARDAR
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("49.2 CONTROLES PREVIOS")
print("=" * 100)

partidos_matricula_49 = set(
    matricula_limpia["partido"].dropna().unique()
)

partidos_maestro_49 = set(
    dataset_maestro["partido"].dropna().unique()
)

print("Filas matricula_limpia:", len(matricula_limpia))
print("Filas dataset_maestro:", len(dataset_maestro))

print(
    "Partidos matricula_limpia:",
    len(partidos_matricula_49)
)

print(
    "Partidos dataset_maestro:",
    len(partidos_maestro_49)
)

print(
    "Universos iguales:",
    partidos_matricula_49 == partidos_maestro_49
)


# ------------------------------------------------------------
# 49.3 CONTROL DE CLAVES
# ------------------------------------------------------------

duplicados_matricula_49 = matricula_limpia.duplicated(
    subset=["partido", "anio", "nivel"]
).sum()

duplicados_maestro_49 = dataset_maestro.duplicated(
    subset=["partido", "anio"]
).sum()

print("\nDuplicados matricula [partido, anio, nivel]:",
      duplicados_matricula_49)

print("Duplicados maestro [partido, anio]:",
      duplicados_maestro_49)


# ------------------------------------------------------------
# 49.4 CONTROL TERRITORIAL
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("49.4 CONTROL TERRITORIAL")
print("=" * 100)

controles_territoriales_49 = {
    "135 partidos en matricula":
        len(partidos_matricula_49) == 135,

    "135 partidos en maestro":
        len(partidos_maestro_49) == 135,

    "Universos idénticos":
        partidos_matricula_49 == partidos_maestro_49,

    "Sin CAÑUELAS en matricula":
        "CAÑUELAS" not in partidos_matricula_49,

    "Sin CAÑUELAS en maestro":
        "CAÑUELAS" not in partidos_maestro_49,

    "CANUELAS en matricula":
        "CANUELAS" in partidos_matricula_49,

    "CANUELAS en maestro":
        "CANUELAS" in partidos_maestro_49,

    "Rosales normalizado en matricula":
        "CORONEL DE MARINA LEONARDO ROSALES"
        in partidos_matricula_49,

    "Rosales normalizado en maestro":
        "CORONEL DE MARINA LEONARDO ROSALES"
        in partidos_maestro_49,

    "Sin ENMASCARADO en matricula":
        "ENMASCARADO" not in partidos_matricula_49,

    "Sin ENMASCARADO en maestro":
        "ENMASCARADO" not in partidos_maestro_49,

    "Sin duplicados en matricula":
        duplicados_matricula_49 == 0,

    "Sin duplicados en maestro":
        duplicados_maestro_49 == 0,
}

for nombre, resultado in controles_territoriales_49.items():
    print(
        f"{nombre}:",
        "OK" if resultado else "ERROR"
    )


# ------------------------------------------------------------
# 49.5 NO GUARDAR SI HAY ALGÚN ERROR
# ------------------------------------------------------------

todo_previo_ok_49 = all(
    controles_territoriales_49.values()
)

if not todo_previo_ok_49:
    raise ValueError(
        "PASO 49 DETENIDO: existe al menos un error "
        "en los controles previos. NO se guardó ningún archivo."
    )

print("\n>>> Todos los controles previos dieron OK.")


# ------------------------------------------------------------
# 49.6 GUARDAR COPIAS DEFINITIVAS
# ------------------------------------------------------------

matricula_limpia.to_csv(
    archivo_matricula_49,
    index=False,
    encoding="utf-8-sig"
)

dataset_maestro.to_csv(
    archivo_maestro_49,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 100)
print("49.6 ARCHIVOS GUARDADOS")
print("=" * 100)

print(
    archivo_matricula_49,
    "| existe:",
    os.path.exists(archivo_matricula_49)
)

print(
    archivo_maestro_49,
    "| existe:",
    os.path.exists(archivo_maestro_49)
)


# ------------------------------------------------------------
# 49.7 RECARGAR LOS ARCHIVOS DESDE DISCO
# ------------------------------------------------------------

matricula_recargada_49 = pd.read_csv(
    archivo_matricula_49
)

maestro_recargado_49 = pd.read_csv(
    archivo_maestro_49
)

print("\n" + "=" * 100)
print("49.7 RECARGA DESDE DISCO")
print("=" * 100)

print(
    "matricula recargada:",
    matricula_recargada_49.shape
)

print(
    "maestro recargado:",
    maestro_recargado_49.shape
)


# ------------------------------------------------------------
# 49.8 COMPARAR DIMENSIONES
# ------------------------------------------------------------

mismas_dimensiones_matricula_49 = (
    matricula_recargada_49.shape
    == matricula_limpia.shape
)

mismas_dimensiones_maestro_49 = (
    maestro_recargado_49.shape
    == dataset_maestro.shape
)

print("\nDimensiones matrícula:",
      "OK" if mismas_dimensiones_matricula_49 else "ERROR")

print("Dimensiones maestro:",
      "OK" if mismas_dimensiones_maestro_49 else "ERROR")


# ------------------------------------------------------------
# 49.9 CONTROL DE PARTIDOS DESPUÉS DE RECARGAR
# ------------------------------------------------------------

partidos_matricula_recargada_49 = set(
    matricula_recargada_49["partido"]
    .dropna()
    .unique()
)

partidos_maestro_recargado_49 = set(
    maestro_recargado_49["partido"]
    .dropna()
    .unique()
)

print("\n" + "=" * 100)
print("49.9 CONTROL POST-GUARDADO")
print("=" * 100)

print(
    "Partidos matrícula:",
    len(partidos_matricula_recargada_49)
)

print(
    "Partidos maestro:",
    len(partidos_maestro_recargado_49)
)

print(
    "Universos idénticos:",
    partidos_matricula_recargada_49
    == partidos_maestro_recargado_49
)


# ------------------------------------------------------------
# 49.10 CONTROL DE DUPLICADOS POST-GUARDADO
# ------------------------------------------------------------

duplicados_matricula_post_49 = (
    matricula_recargada_49.duplicated(
        subset=["partido", "anio", "nivel"]
    ).sum()
)

duplicados_maestro_post_49 = (
    maestro_recargado_49.duplicated(
        subset=["partido", "anio"]
    ).sum()
)

print(
    "Duplicados matrícula:",
    duplicados_matricula_post_49
)

print(
    "Duplicados maestro:",
    duplicados_maestro_post_49
)


# ------------------------------------------------------------
# 49.11 VALIDACIÓN DE INTEGRIDAD
# ------------------------------------------------------------

controles_finales_49 = {
    "Dimensión matrícula conservada":
        mismas_dimensiones_matricula_49,

    "Dimensión maestro conservada":
        mismas_dimensiones_maestro_49,

    "135 partidos matrícula":
        len(partidos_matricula_recargada_49) == 135,

    "135 partidos maestro":
        len(partidos_maestro_recargado_49) == 135,

    "Universos idénticos":
        partidos_matricula_recargada_49
        == partidos_maestro_recargado_49,

    "Sin duplicados matrícula":
        duplicados_matricula_post_49 == 0,

    "Sin duplicados maestro":
        duplicados_maestro_post_49 == 0,

    "CANUELAS presente":
        (
            "CANUELAS"
            in partidos_matricula_recargada_49
            and
            "CANUELAS"
            in partidos_maestro_recargado_49
        ),

    "CAÑUELAS ausente":
        (
            "CAÑUELAS"
            not in partidos_matricula_recargada_49
            and
            "CAÑUELAS"
            not in partidos_maestro_recargado_49
        ),

    "Rosales normalizado":
        (
            "CORONEL DE MARINA LEONARDO ROSALES"
            in partidos_matricula_recargada_49
            and
            "CORONEL DE MARINA LEONARDO ROSALES"
            in partidos_maestro_recargado_49
        )
}

print("\n" + "=" * 100)
print("49.11 VALIDACIÓN FINAL DE INTEGRIDAD")
print("=" * 100)

for nombre, resultado in controles_finales_49.items():
    print(
        f"{nombre}:",
        "OK" if resultado else "ERROR"
    )


todo_final_ok_49 = all(
    controles_finales_49.values()
)


# ------------------------------------------------------------
# 49.12 RESULTADO DEFINITIVO
# ------------------------------------------------------------

print("\n" + "=" * 100)
print("49.12 RESULTADO DEFINITIVO")
print("=" * 100)

if todo_final_ok_49:

    print(
        ">>> VALIDACIÓN FINAL EXITOSA."
    )

    print(
        ">>> LOS ARCHIVOS FUERON GUARDADOS "
        "Y RECARGADOS CORRECTAMENTE."
    )

    print(
        ">>> EL UNIVERSO TERRITORIAL CONTIENE "
        "LOS 135 PARTIDOS."
    )

    print(
        ">>> NO SE DETECTARON DUPLICADOS "
        "EN LAS CLAVES PRINCIPALES."
    )

    print(
        ">>> CORRECCIÓN TERRITORIAL FINALIZADA."
    )

else:

    print(
        ">>> ATENCIÓN: ALGÚN CONTROL FINAL FALLÓ."
    )

    print(
        ">>> NO CONSIDERAR TODAVÍA LOS ARCHIVOS "
        "COMO DEFINITIVOS."
    )


print("\nArchivos generados:")
print("-", os.path.abspath(archivo_matricula_49))
print("-", os.path.abspath(archivo_maestro_49))

print("\n" + "=" * 100)
print("PASO 49 FINALIZADO")
print("=" * 100)