
# 1. IMPORTAR LIBRERÍAS


from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder



# 2. DEFINIR RUTAS


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_MODELADO = Path(__file__).resolve().parent

ruta_dataset = (
    RUTA_PROYECTO / "01_datos" / "dataset_modelado_features.csv"
)



# 3. CARGAR DATOS


df = pd.read_csv(ruta_dataset)


print("PROYECCIONES DE MATRÍCULA 2026–2035")


print("\nDimensiones del dataset:", df.shape)

historico = df[
    (df["anio"] <= 2025)
    & df["matricula"].notna()
].copy()

print("Observaciones históricas:", len(historico))



# 4. DEFINIR VARIABLES DEL MODELO


variables_modelo = [
    "partido",
    "nivel",
    "anio",
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]

variables_categoricas = [
    "partido",
    "nivel"
]

variables_numericas = [
    "anio",
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]



# 5. PREPARAR ENTRENAMIENTO


# Usamos años desde 2015 porque necesitamos tres
# matrículas anteriores para construir las variables.

entrenamiento = historico[
    historico["anio"] >= 2015
].dropna(
    subset=variables_modelo + ["matricula"]
).copy()

X_train = entrenamiento[variables_modelo]
y_train = entrenamiento["matricula"]

print("\nObservaciones de entrenamiento:", len(entrenamiento))
print("Años de entrenamiento:",
      entrenamiento["anio"].min(),
      "-",
      entrenamiento["anio"].max())



# 6. ENTRENAR RANDOM FOREST


preprocesador = ColumnTransformer(
    transformers=[
        (
            "categoricas",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            variables_categoricas
        ),
        (
            "numericas",
            "passthrough",
            variables_numericas
        )
    ]
)

modelo_rf = Pipeline(
    steps=[
        ("preprocesador", preprocesador),
        (
            "modelo",
            RandomForestRegressor(
                n_estimators=300,
                max_depth=None,
                min_samples_leaf=2,
                max_features=0.7,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

print("\nEntrenando Random Forest...")

modelo_rf.fit(
    X_train,
    y_train
)

print("Random Forest entrenado correctamente.")



# 7. PREPARAR MATRÍCULAS RECIENTES


recientes = historico[
    historico["anio"].isin(
        [2023, 2024, 2025]
    )
][
    [
        "partido",
        "nivel",
        "anio",
        "matricula"
    ]
].copy()

recientes = recientes.pivot(
    index=["partido", "nivel"],
    columns="anio",
    values="matricula"
)

# Necesitamos los tres años completos.

recientes = recientes.dropna(
    subset=[2023, 2024, 2025]
)

print("\nSeries con historia reciente completa:",
      len(recientes))



# 8. CALCULAR TENDENCIA RECIENTE


recientes["cambio_anual"] = (
    recientes[2025] - recientes[2023]
) / 2

recientes["tasa_anual"] = (
    recientes["cambio_anual"]
    / recientes[2025]
)

# Mantenemos el mismo límite utilizado
# en la evaluación histórica.

recientes["tasa_controlada"] = (
    recientes["tasa_anual"]
    .clip(
        lower=-0.10,
        upper=0.10
    )
)



# 9. GENERAR PROYECCIONES


resultados = []

ANIO_INICIAL = 2026
ANIO_FINAL = 2035

print("\nGenerando proyecciones...")

for (partido, nivel), fila in recientes.iterrows():

    matricula_2023 = float(fila[2023])
    matricula_2024 = float(fila[2024])
    matricula_2025 = float(fila[2025])

    tasa = float(fila["tasa_controlada"])

    # Historial utilizado por Random Forest.
    # Se actualizará con cada predicción.

    historial_rf = {
        2023: matricula_2023,
        2024: matricula_2024,
        2025: matricula_2025
    }

    for anio in range(
        ANIO_INICIAL,
        ANIO_FINAL + 1
    ):

        horizonte = anio - 2025

        
        # A. BASELINE
        

        pred_baseline = matricula_2025

        
        # B. TENDENCIA
        

        pred_tendencia = (
            matricula_2025
            * (1 + tasa) ** horizonte
        )

        pred_tendencia = max(
            0,
            pred_tendencia
        )

        
        # C. RANDOM FOREST RECURSIVO
        

        lag_1 = historial_rf[anio - 1]
        lag_2 = historial_rf[anio - 2]
        lag_3 = historial_rf[anio - 3]

        if lag_2 > 0:

            variacion_anual = (
                lag_1 - lag_2
            ) / lag_2

        else:

            variacion_anual = 0

        tendencia_3_anios = (
            lag_1 - lag_3
        ) / 2

        entrada_rf = pd.DataFrame([{

            "partido": partido,
            "nivel": nivel,
            "anio": anio,

            "matricula_lag_1": lag_1,
            "matricula_lag_2": lag_2,
            "matricula_lag_3": lag_3,

            "variacion_anual_matricula":
                variacion_anual,

            "tendencia_3_anios":
                tendencia_3_anios
        }])

        pred_rf = float(
            modelo_rf.predict(
                entrada_rf[variables_modelo]
            )[0]
        )

        pred_rf = max(
            0,
            pred_rf
        )

        # Guardamos la predicción para utilizarla
        # como dato anterior en el próximo año.

        historial_rf[anio] = pred_rf

        
        # D. GUARDAR RESULTADOS
        

        resultados.append({

            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "horizonte": horizonte,

            "prediccion_baseline":
                pred_baseline,

            "prediccion_tendencia":
                pred_tendencia,

            "prediccion_random_forest":
                pred_rf
        })


proyecciones = pd.DataFrame(resultados)



# 10. VALIDAR RESULTADOS


print("\n")

print("VALIDACIÓN DE PROYECCIONES")


print("\nCantidad de proyecciones:", len(proyecciones))

print("Partidos:", proyecciones["partido"].nunique())

print("Niveles:", proyecciones["nivel"].nunique())

print(
    "Años:",
    proyecciones["anio"].min(),
    "-",
    proyecciones["anio"].max()
)

columnas_predicciones = [
    "prediccion_baseline",
    "prediccion_tendencia",
    "prediccion_random_forest"
]

print("\nValores nulos:")

print(
    proyecciones[
        columnas_predicciones
    ].isna().sum()
)

print("\nValores negativos:")

print(
    (
        proyecciones[
            columnas_predicciones
        ] < 0
    ).sum()
)

print("\nValores no finitos:")

print(
    pd.Series({
        columna: (
            ~np.isfinite(proyecciones[columna])
        ).sum()
        for columna in columnas_predicciones
    })
)

duplicados = proyecciones.duplicated(
    subset=[
        "partido",
        "nivel",
        "anio"
    ]
).sum()

print("\nClaves duplicadas:", duplicados)

series_esperadas = 135 * 3
filas_esperadas = series_esperadas * 10

print("\nFilas esperadas:", filas_esperadas)

if len(proyecciones) != filas_esperadas:

    print(
        "ADVERTENCIA: faltan combinaciones "
        "de partido, nivel o año."
    )



# 11. RESUMEN PROVINCIAL POR AÑO Y NIVEL


resumen_nivel = proyecciones.groupby(
    ["anio", "nivel"]
)[
    columnas_predicciones
].sum().reset_index()



# 12. RESUMEN PROVINCIAL POR AÑO


resumen_provincial = proyecciones.groupby(
    "anio"
)[
    columnas_predicciones
].sum().reset_index()


print("\n")

print("RESUMEN PROVINCIAL")


print(
    resumen_provincial.to_string(index=False)
)



# 13. COMPARAR 2025 CON 2035


matricula_2025_total = (
    historico[
        historico["anio"] == 2025
    ]["matricula"].sum()
)

proyeccion_2035 = (
    resumen_provincial[
        resumen_provincial["anio"] == 2035
    ]
)

print("\n")

print("COMPARACIÓN 2025 VS. 2035")


print(
    "Matrícula real 2025:",
    round(matricula_2025_total)
)

for columna in columnas_predicciones:

    valor_2035 = float(
        proyeccion_2035[columna].iloc[0]
    )

    variacion_pct = (
        (
            valor_2035
            - matricula_2025_total
        )
        / matricula_2025_total
    ) * 100

    print(
        f"{columna}: "
        f"{valor_2035:,.0f} alumnos "
        f"({variacion_pct:+.2f} %)"
    )



# 14. GUARDAR RESULTADOS


proyecciones.to_csv(
    RUTA_MODELADO
    / "proyecciones_matricula_2026_2035.csv",
    index=False
)

resumen_nivel.to_csv(
    RUTA_MODELADO
    / "proyecciones_por_nivel_2026_2035.csv",
    index=False
)

resumen_provincial.to_csv(
    RUTA_MODELADO
    / "proyecciones_provinciales_2026_2035.csv",
    index=False
)

print("\n")

print("ARCHIVOS GUARDADOS CORRECTAMENTE")


print("proyecciones_matricula_2026_2035.csv")
print("proyecciones_por_nivel_2026_2035.csv")
print("proyecciones_provinciales_2026_2035.csv")