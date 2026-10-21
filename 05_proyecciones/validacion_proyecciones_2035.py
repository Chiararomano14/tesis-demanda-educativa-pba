
# 1. IMPORTAR LIBRERÍAS


from pathlib import Path

import numpy as np
import pandas as pd



# 2. DEFINIR RUTAS


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_MODELADO = Path(__file__).resolve().parent

ruta_proyecciones = (
    RUTA_MODELADO
    / "proyecciones_matricula_2026_2035.csv"
)

ruta_dataset = (
    RUTA_PROYECTO
    / "01_datos" / "dataset_modelado_features.csv"
)



# 3. CARGAR DATOS


proyecciones = pd.read_csv(ruta_proyecciones)

dataset = pd.read_csv(ruta_dataset)


print("VALIDACIÓN DE PROYECCIONES 2026–2035")


print("\nProyecciones:", proyecciones.shape)
print("Dataset histórico:", dataset.shape)



# 4. DEFINIR ESTRATEGIAS


estrategias = {
    "Baseline": "prediccion_baseline",
    "Tendencia": "prediccion_tendencia",
    "Random Forest": "prediccion_random_forest"
}

columnas_predicciones = list(estrategias.values())



# 5. RECUPERAR MATRÍCULA REAL DE 2025


matricula_2025 = dataset[
    dataset["anio"] == 2025
][
    ["partido", "nivel", "matricula"]
].copy()

matricula_2025 = matricula_2025.rename(
    columns={
        "matricula": "matricula_2025"
    }
)

# Verificamos que exista una única matrícula
# por partido y nivel.

assert not matricula_2025.duplicated(
    ["partido", "nivel"]
).any(), "Hay claves duplicadas en 2025."

assert matricula_2025["matricula_2025"].notna().all(), (
    "Hay matrículas faltantes en 2025."
)

proyecciones = proyecciones.merge(
    matricula_2025,
    on=["partido", "nivel"],
    how="left",
    validate="many_to_one"
)

assert proyecciones["matricula_2025"].notna().all(), (
    "Hay proyecciones sin matrícula de referencia."
)



# 6. PREPARAR CAMBIOS ANUALES


# Para calcular la variación de 2026 necesitamos
# compararla con la matrícula real de 2025.

base_2025 = matricula_2025.copy()

base_2025["anio"] = 2025

for columna in columnas_predicciones:
    base_2025[columna] = base_2025["matricula_2025"]

base_2025 = base_2025[
    ["partido", "nivel", "anio"]
    + columnas_predicciones
]

serie_completa = pd.concat(
    [
        base_2025,
        proyecciones[
            ["partido", "nivel", "anio"]
            + columnas_predicciones
        ]
    ],
    ignore_index=True
)

serie_completa = serie_completa.sort_values(
    ["partido", "nivel", "anio"]
)



# 7. CALCULAR VARIACIONES ANUALES


for nombre, columna in estrategias.items():

    columna_anterior = f"anterior_{columna}"
    columna_variacion = f"variacion_{columna}"

    serie_completa[columna_anterior] = (
        serie_completa.groupby(
            ["partido", "nivel"]
        )[columna].shift(1)
    )

    serie_completa[columna_variacion] = np.where(
        serie_completa[columna_anterior] > 0,

        (
            (
                serie_completa[columna]
                - serie_completa[columna_anterior]
            )
            / serie_completa[columna_anterior]
        ) * 100,

        np.nan
    )



# 8. IDENTIFICAR CAMBIOS ANUALES EXTREMOS


UMBRAL_ANUAL = 20

cambios_anuales = []

for nombre, columna in estrategias.items():

    columna_variacion = f"variacion_{columna}"

    datos = serie_completa[
        serie_completa["anio"] >= 2026
    ].copy()

    datos["estrategia"] = nombre

    datos["variacion_anual_pct"] = (
        datos[columna_variacion]
    )

    datos["magnitud_cambio"] = (
        datos["variacion_anual_pct"].abs()
    )

    cambios_anuales.append(
        datos[
            datos["magnitud_cambio"] > UMBRAL_ANUAL
        ][
            [
                "partido",
                "nivel",
                "anio",
                "estrategia",
                "variacion_anual_pct",
                "magnitud_cambio"
            ]
        ]
    )


cambios_extremos = pd.concat(
    cambios_anuales,
    ignore_index=True
)

cambios_extremos = cambios_extremos.sort_values(
    "magnitud_cambio",
    ascending=False
)


print("\n")

print("1. CAMBIOS ANUALES SUPERIORES AL 20 %")


print("\nCantidad total:", len(cambios_extremos))

print("\nPor estrategia:")

print(
    cambios_extremos["estrategia"]
    .value_counts()
    .reindex(
        estrategias.keys(),
        fill_value=0
    )
)

print("\nLos 15 cambios más grandes:")

print(
    cambios_extremos.head(15).to_string(index=False)
)



# 9. CALCULAR CAMBIO ACUMULADO 2025–2035


proyecciones_2035 = proyecciones[
    proyecciones["anio"] == 2035
].copy()

for nombre, columna in estrategias.items():

    columna_variacion = f"cambio_2035_{columna}"

    proyecciones_2035[columna_variacion] = np.where(
        proyecciones_2035["matricula_2025"] > 0,

        (
            (
                proyecciones_2035[columna]
                - proyecciones_2035["matricula_2025"]
            )
            / proyecciones_2035["matricula_2025"]
        ) * 100,

        np.nan
    )



# 10. IDENTIFICAR CAMBIOS ACUMULADOS EXTREMOS


UMBRAL_ACUMULADO = 50

cambios_acumulados = []

for nombre, columna in estrategias.items():

    columna_variacion = f"cambio_2035_{columna}"

    datos = proyecciones_2035[
        [
            "partido",
            "nivel",
            "matricula_2025",
            columna,
            columna_variacion
        ]
    ].copy()

    datos = datos.rename(
        columns={
            columna: "matricula_2035",
            columna_variacion: "variacion_2025_2035_pct"
        }
    )

    datos["estrategia"] = nombre

    datos["magnitud_cambio"] = (
        datos["variacion_2025_2035_pct"].abs()
    )

    cambios_acumulados.append(
        datos[
            datos["magnitud_cambio"] > UMBRAL_ACUMULADO
        ]
    )


cambios_acumulados = pd.concat(
    cambios_acumulados,
    ignore_index=True
)

cambios_acumulados = cambios_acumulados.sort_values(
    "magnitud_cambio",
    ascending=False
)


print("\n")

print("2. CAMBIOS ACUMULADOS SUPERIORES AL 50 %")


print("\nCantidad total:", len(cambios_acumulados))

print("\nPor estrategia:")

print(
    cambios_acumulados["estrategia"]
    .value_counts()
    .reindex(
        estrategias.keys(),
        fill_value=0
    )
)

print("\nLos 15 cambios más grandes:")

print(
    cambios_acumulados.head(15).to_string(index=False)
)



# 11. COMPARAR ESTRATEGIAS EN 2035


proyecciones_2035["prediccion_minima"] = (
    proyecciones_2035[columnas_predicciones].min(axis=1)
)

proyecciones_2035["prediccion_maxima"] = (
    proyecciones_2035[columnas_predicciones].max(axis=1)
)

proyecciones_2035["diferencia_absoluta"] = (
    proyecciones_2035["prediccion_maxima"]
    - proyecciones_2035["prediccion_minima"]
)

proyecciones_2035["diferencia_pct_2025"] = np.where(
    proyecciones_2035["matricula_2025"] > 0,

    (
        proyecciones_2035["diferencia_absoluta"]
        / proyecciones_2035["matricula_2025"]
    ) * 100,

    np.nan
)

diferencias_estrategias = (
    proyecciones_2035.sort_values(
        "diferencia_pct_2025",
        ascending=False
    )
)


print("\n")

print("3. MAYORES DIFERENCIAS ENTRE ESTRATEGIAS")


print(
    diferencias_estrategias[
        [
            "partido",
            "nivel",
            "matricula_2025",
            "prediccion_baseline",
            "prediccion_tendencia",
            "prediccion_random_forest",
            "diferencia_pct_2025"
        ]
    ].head(15).to_string(index=False)
)



# 12. EVOLUCIÓN POR NIVEL EDUCATIVO


niveles_2025 = matricula_2025.groupby(
    "nivel"
)["matricula_2025"].sum()

niveles_2035 = proyecciones_2035.groupby(
    "nivel"
)[columnas_predicciones].sum()

resumen_niveles = niveles_2035.copy()

resumen_niveles["matricula_2025"] = niveles_2025

for columna in columnas_predicciones:

    resumen_niveles[f"variacion_{columna}_pct"] = (
        (
            resumen_niveles[columna]
            - resumen_niveles["matricula_2025"]
        )
        / resumen_niveles["matricula_2025"]
    ) * 100


print("\n")

print("4. EVOLUCIÓN POR NIVEL EDUCATIVO")


print(
    resumen_niveles.to_string()
)



# 13. EVOLUCIÓN TERRITORIAL


partidos_2025 = matricula_2025.groupby(
    "partido"
)["matricula_2025"].sum()

partidos_2035 = proyecciones_2035.groupby(
    "partido"
)[columnas_predicciones].sum()

resumen_partidos = partidos_2035.copy()

resumen_partidos["matricula_2025"] = partidos_2025

for columna in columnas_predicciones:

    resumen_partidos[f"variacion_{columna}_pct"] = (
        (
            resumen_partidos[columna]
            - resumen_partidos["matricula_2025"]
        )
        / resumen_partidos["matricula_2025"]
    ) * 100



# 14. MOSTRAR PARTIDOS CON MAYORES CAMBIOS


print("\n")

print("5. MAYORES DISMINUCIONES TERRITORIALES")


print("\nSegún Random Forest:")

print(
    resumen_partidos.sort_values(
        "variacion_prediccion_random_forest_pct"
    )[
        [
            "matricula_2025",
            "prediccion_random_forest",
            "variacion_prediccion_random_forest_pct"
        ]
    ].head(10).to_string()
)


print("\n")

print("6. MAYORES AUMENTOS TERRITORIALES")


print("\nSegún Random Forest:")

print(
    resumen_partidos.sort_values(
        "variacion_prediccion_random_forest_pct",
        ascending=False
    )[
        [
            "matricula_2025",
            "prediccion_random_forest",
            "variacion_prediccion_random_forest_pct"
        ]
    ].head(10).to_string()
)



# 15. GUARDAR RESULTADOS


archivos = {

    "cambios_anuales_extremos_2035.csv":
        cambios_extremos,

    "cambios_acumulados_extremos_2035.csv":
        cambios_acumulados,

    "diferencias_estrategias_2035.csv":
        diferencias_estrategias,

    "evolucion_niveles_2035.csv":
        resumen_niveles.reset_index(),

    "evolucion_partidos_2035.csv":
        resumen_partidos.reset_index()

}

for nombre, datos in archivos.items():

    datos.to_csv(
        RUTA_MODELADO / nombre,
        index=False
    )


print("\n")

print("ARCHIVOS GUARDADOS CORRECTAMENTE")


for nombre in archivos:
    print(nombre)