
# 1. IMPORTAR LIBRERÍAS


from pathlib import Path
import pandas as pd
import numpy as np



# 2. DEFINIR RUTAS


RUTA_MODELADO = Path(__file__).resolve().parent

ruta_proyecciones = (
    RUTA_MODELADO
    / "proyecciones_matricula_2026_2035.csv"
)

ruta_dataset = (
    RUTA_MODELADO.parent
    / "01_datos" / "dataset_maestro_final.csv"
)



# 3. CARGAR DATOS


proyecciones = pd.read_csv(ruta_proyecciones)

historico = pd.read_csv(ruta_dataset)



print("87. TRAYECTORIAS ALTERNATIVAS DE PROYECCIÓN")


print("\nDimensiones de las proyecciones:")
print(proyecciones.shape)

print("\nColumnas disponibles:")
print(proyecciones.columns.tolist())



# 4. RECUPERAR MATRÍCULA REAL DE 2025


matricula_2025 = historico[
    historico["anio"] == 2025
][
    [
        "partido",
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria"
    ]
].copy()


# Convertimos el formato ancho a largo.

matricula_2025 = matricula_2025.melt(

    id_vars="partido",

    value_vars=[
        "matricula_inicial",
        "matricula_primaria",
        "matricula_secundaria"
    ],

    var_name="nivel",
    value_name="matricula_2025"

)


# Igualamos los nombres de los niveles.

matricula_2025["nivel"] = (
    matricula_2025["nivel"]
    .str.replace("matricula_", "", regex=False)
    .str.upper()
)


# Unimos las proyecciones con el valor real de 2025.

escenarios = proyecciones.merge(

    matricula_2025,

    on=["partido", "nivel"],

    how="left",

    validate="many_to_one"

)


assert escenarios["matricula_2025"].notna().all()



# 5. CALCULAR DIFERENCIAS ENTRE ESTRATEGIAS


columnas_estrategias = [

    "prediccion_baseline",

    "prediccion_tendencia",

    "prediccion_random_forest"

]


escenarios["proyeccion_minima"] = (
    escenarios[columnas_estrategias].min(axis=1)
)

escenarios["proyeccion_maxima"] = (
    escenarios[columnas_estrategias].max(axis=1)
)


# Diferencia absoluta entre la mayor y menor proyección.

escenarios["amplitud_estrategias"] = (

    escenarios["proyeccion_maxima"]
    - escenarios["proyeccion_minima"]

)


# Diferencia relativa al valor real de 2025.

escenarios["amplitud_porcentual_2025"] = np.where(

    escenarios["matricula_2025"] > 0,

    (
        escenarios["amplitud_estrategias"]
        / escenarios["matricula_2025"]
    ) * 100,

    np.nan

)



# 6. RESUMEN PROVINCIAL POR AÑO


resumen_provincial = escenarios.groupby(
    "anio",
    as_index=False
)[columnas_estrategias].sum()


resumen_provincial["proyeccion_minima"] = (
    resumen_provincial[columnas_estrategias].min(axis=1)
)

resumen_provincial["proyeccion_maxima"] = (
    resumen_provincial[columnas_estrategias].max(axis=1)
)

resumen_provincial["amplitud_estrategias"] = (

    resumen_provincial["proyeccion_maxima"]
    - resumen_provincial["proyeccion_minima"]

)


print("\n")

print("1. TRAYECTORIAS PROVINCIALES 2026–2035")


print(
    resumen_provincial.round(2).to_string(
        index=False
    )
)



# 7. COMPARAR NIVELES EDUCATIVOS EN 2035


escenarios_2035 = escenarios[
    escenarios["anio"] == 2035
].copy()


resumen_niveles = escenarios_2035.groupby(
    "nivel",
    as_index=False
)[columnas_estrategias].sum()


resumen_niveles["proyeccion_minima"] = (
    resumen_niveles[columnas_estrategias].min(axis=1)
)

resumen_niveles["proyeccion_maxima"] = (
    resumen_niveles[columnas_estrategias].max(axis=1)
)

resumen_niveles["amplitud_estrategias"] = (

    resumen_niveles["proyeccion_maxima"]
    - resumen_niveles["proyeccion_minima"]

)


print("\n")

print("2. DIFERENCIAS POR NIVEL EDUCATIVO EN 2035")


print(
    resumen_niveles.round(2).to_string(
        index=False
    )
)



# 8. COMPARAR PARTIDOS EN 2035


resumen_partidos = escenarios_2035.groupby(
    "partido",
    as_index=False
)[columnas_estrategias].sum()


resumen_partidos["proyeccion_minima"] = (
    resumen_partidos[columnas_estrategias].min(axis=1)
)

resumen_partidos["proyeccion_maxima"] = (
    resumen_partidos[columnas_estrategias].max(axis=1)
)

resumen_partidos["amplitud_estrategias"] = (

    resumen_partidos["proyeccion_maxima"]
    - resumen_partidos["proyeccion_minima"]

)


# Agregamos matrícula total real de 2025.

total_2025 = matricula_2025.groupby(
    "partido",
    as_index=False
)["matricula_2025"].sum()


resumen_partidos = resumen_partidos.merge(

    total_2025,

    on="partido",

    how="left",

    validate="one_to_one"

)


resumen_partidos["amplitud_porcentual_2025"] = np.where(

    resumen_partidos["matricula_2025"] > 0,

    (
        resumen_partidos["amplitud_estrategias"]
        / resumen_partidos["matricula_2025"]
    ) * 100,

    np.nan

)


print("\n")

print("3. PARTIDOS CON MAYOR DIFERENCIA ABSOLUTA")


print(

    resumen_partidos.sort_values(

        "amplitud_estrategias",

        ascending=False

    ).head(15)[

        [
            "partido",
            "matricula_2025",
            "amplitud_estrategias",
            "amplitud_porcentual_2025"
        ]

    ].round(2).to_string(index=False)

)


print("\n")

print("4. PARTIDOS CON MAYOR DIFERENCIA PORCENTUAL")


print(

    resumen_partidos.sort_values(

        "amplitud_porcentual_2025",

        ascending=False

    ).head(15)[

        [
            "partido",
            "matricula_2025",
            "amplitud_estrategias",
            "amplitud_porcentual_2025"
        ]

    ].round(2).to_string(index=False)

)



# 9. CONTROLES DE CALIDAD


print("\n")

print("5. CONTROLES DE CALIDAD")


print("Filas:", len(escenarios))

print(
    "Partidos:",
    escenarios["partido"].nunique()
)

print(
    "Niveles:",
    escenarios["nivel"].nunique()
)

print(
    "Años:",
    escenarios["anio"].nunique()
)


duplicados = escenarios.duplicated(
    subset=["partido", "nivel", "anio"]
).sum()

print("Duplicados:", duplicados)


faltantes = escenarios[
    columnas_estrategias
    + ["matricula_2025"]
].isna().sum().sum()

print("Valores faltantes:", faltantes)


assert len(escenarios) == 4050
assert duplicados == 0
assert faltantes == 0

assert (
    escenarios[columnas_estrategias] >= 0
).all().all()



# 10. GUARDAR RESULTADOS


escenarios.to_csv(

    RUTA_MODELADO
    / "trayectorias_alternativas_2026_2035.csv",

    index=False

)

resumen_provincial.to_csv(

    RUTA_MODELADO
    / "trayectorias_provinciales.csv",

    index=False

)

resumen_niveles.to_csv(

    RUTA_MODELADO
    / "trayectorias_por_nivel_2035.csv",

    index=False

)

resumen_partidos.to_csv(

    RUTA_MODELADO
    / "trayectorias_por_partido_2035.csv",

    index=False

)


print("\n")

print("ANÁLISIS DE TRAYECTORIAS FINALIZADO")


print("\nArchivos generados correctamente.")