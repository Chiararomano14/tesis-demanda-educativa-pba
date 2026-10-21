import pandas as pd
from pathlib import Path



# 1. RUTAS

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_MODELADO = RUTA_PROYECTO / "04_modelado"

ruta_train = RUTA_MODELADO / "train.csv"
ruta_validacion = RUTA_MODELADO / "validacion.csv"
ruta_test = RUTA_MODELADO / "test.csv"



# 2. CARGAR DATOS

train = pd.read_csv(ruta_train)
validacion = pd.read_csv(ruta_validacion)
test = pd.read_csv(ruta_test)

print("\n")
print("PREPARACIÓN DE VARIABLES PARA MODELADO")



# 3. DEFINIR VARIABLES

variables_modelo_base = [
    "partido",
    "nivel",
    "anio",
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]

objetivo = "matricula"

print("\n=== VARIABLES PREDICTORAS ===")

for variable in variables_modelo_base:
    print("-", variable)

print("\nVariable objetivo:")
print("-", objetivo)



# 4. SELECCIONAR COLUMNAS NECESARIAS

columnas_necesarias = (
    variables_modelo_base
    + [objetivo]
)

train_modelo = train[
    columnas_necesarias
].copy()

validacion_modelo = validacion[
    columnas_necesarias
].copy()

test_modelo = test[
    columnas_necesarias
].copy()



# 5. REVISAR FALTANTES

print("\n=== FALTANTES ANTES DE PREPARAR EL MODELO ===")

print("\nTRAIN")
print(
    train_modelo.isna().sum()
)

print("\nVALIDACIÓN")
print(
    validacion_modelo.isna().sum()
)

print("\nTEST")
print(
    test_modelo.isna().sum()
)



# 6. IDENTIFICAR FILAS COMPLETAS

train_completo = train_modelo.dropna().copy()
validacion_completa = validacion_modelo.dropna().copy()
test_completo = test_modelo.dropna().copy()


print("\n=== FILAS DISPONIBLES PARA MODELADO ===")

print(
    "TRAIN:",
    len(train_completo),
    "de",
    len(train_modelo)
)

print(
    "VALIDACIÓN:",
    len(validacion_completa),
    "de",
    len(validacion_modelo)
)

print(
    "TEST:",
    len(test_completo),
    "de",
    len(test_modelo)
)



# 7. CONTROL DE PÉRDIDA DE FILAS

print("\n=== FILAS EXCLUIDAS POR FALTANTES ===")

print(
    "TRAIN:",
    len(train_modelo) - len(train_completo)
)

print(
    "VALIDACIÓN:",
    len(validacion_modelo)
    - len(validacion_completa)
)

print(
    "TEST:",
    len(test_modelo)
    - len(test_completo)
)



# 8. CREAR X E Y

X_train = train_completo[
    variables_modelo_base
].copy()

y_train = train_completo[
    objetivo
].copy()

X_validacion = validacion_completa[
    variables_modelo_base
].copy()

y_validacion = validacion_completa[
    objetivo
].copy()

X_test = test_completo[
    variables_modelo_base
].copy()

y_test = test_completo[
    objetivo
].copy()



# 9. CONTROL FINAL


print("\n=== DIMENSIONES FINALES ===")

print(
    "X_train:",
    X_train.shape,
    "| y_train:",
    y_train.shape
)

print(
    "X_validación:",
    X_validacion.shape,
    "| y_validación:",
    y_validacion.shape
)

print(
    "X_test:",
    X_test.shape,
    "| y_test:",
    y_test.shape
)

print("\nPreparación de variables finalizada.")


# 10. IMPORTAR HERRAMIENTAS DE MODELADO


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np



# 11. DEFINIR VARIABLES CATEGÓRICAS Y NUMÉRICAS


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


print("\n")
print("ENTRENAMIENTO - REGRESIÓN LINEAL")


print("\nVariables categóricas:")
for variable in variables_categoricas:
    print("-", variable)

print("\nVariables numéricas:")
for variable in variables_numericas:
    print("-", variable)



# 12. PREPARAR TRANSFORMACIÓN DE VARIABLES


preprocesamiento = ColumnTransformer(
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



# 13. CREAR PIPELINE


modelo_regresion = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
        (
            "modelo",
            LinearRegression()
        )
    ]
)



# 14. ENTRENAR MODELO


modelo_regresion.fit(
    X_train,
    y_train
)

print("\nModelo entrenado correctamente.")



# 15. PREDECIR SOBRE VALIDACIÓN


predicciones_validacion = (
    modelo_regresion.predict(
        X_validacion
    )
)



# 16. CALCULAR MÉTRICAS


mae_regresion = mean_absolute_error(
    y_validacion,
    predicciones_validacion
)

rmse_regresion = np.sqrt(
    mean_squared_error(
        y_validacion,
        predicciones_validacion
    )
)


mascara_mape = y_validacion != 0

mape_regresion = np.mean(
    np.abs(
        (
            y_validacion[mascara_mape]
            - predicciones_validacion[mascara_mape]
        )
        / y_validacion[mascara_mape]
    )
) * 100


print("\n=== REGRESIÓN LINEAL - VALIDACIÓN ===")

print(
    f"MAE:  {mae_regresion:.2f}"
)

print(
    f"RMSE: {rmse_regresion:.2f}"
)

print(
    f"MAPE: {mape_regresion:.2f} %"
)



# 17. CONTROL DE PREDICCIONES


resultados_validacion = (
    validacion_completa[
        [
            "partido",
            "nivel",
            "anio",
            "matricula"
        ]
    ]
    .copy()
)

resultados_validacion[
    "prediccion_regresion"
] = predicciones_validacion

resultados_validacion[
    "error_absoluto"
] = np.abs(
    resultados_validacion["matricula"]
    - resultados_validacion["prediccion_regresion"]
)


print("\n=== EJEMPLOS DE PREDICCIONES ===")

print(
    resultados_validacion[
        [
            "partido",
            "nivel",
            "anio",
            "matricula",
            "prediccion_regresion",
            "error_absoluto"
        ]
    ].head(10)
)



# 18. CONTROL DE PREDICCIONES NEGATIVAS


predicciones_negativas = (
    predicciones_validacion < 0
).sum()

print("\nPredicciones negativas:")
print(predicciones_negativas)



# 19. GUARDAR RESULTADOS


ruta_resultados_regresion = (
    RUTA_MODELADO
    / "resultados_regresion_validacion.csv"
)

resultados_validacion.to_csv(
    ruta_resultados_regresion,
    index=False
)

print("\nResultados guardados correctamente:")
print(ruta_resultados_regresion)


# 20. IMPORTAR MODELOS ALTERNATIVOS


from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)


print("\n")
print("ENTRENAMIENTO - MODELOS ALTERNATIVOS")

# 21. RANDOM FOREST
modelo_random_forest = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
        (
            "modelo",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


print("\nEntrenando Random Forest...")

modelo_random_forest.fit(
    X_train,
    y_train
)

predicciones_rf = (
    modelo_random_forest.predict(
        X_validacion
    )
)

# 22. MÉTRICAS RANDOM FOREST
mae_rf = mean_absolute_error(
    y_validacion,
    predicciones_rf
)

rmse_rf = np.sqrt(
    mean_squared_error(
        y_validacion,
        predicciones_rf
    )
)

mape_rf = np.mean(
    np.abs(
        (
            y_validacion[mascara_mape]
            - predicciones_rf[mascara_mape]
        )
        / y_validacion[mascara_mape]
    )
) * 100


print("\n=== RANDOM FOREST - VALIDACIÓN ===")
print(f"MAE:  {mae_rf:.2f}")
print(f"RMSE: {rmse_rf:.2f}")
print(f"MAPE: {mape_rf:.2f} %")

negativas_rf = (
    predicciones_rf < 0
).sum()

print(
    "Predicciones negativas:",
    negativas_rf
)



# 23. GRADIENT BOOSTING


modelo_gradient_boosting = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
        (
            "modelo",
            GradientBoostingRegressor(
                random_state=42
            )
        )
    ]
)


print("\nEntrenando Gradient Boosting...")

modelo_gradient_boosting.fit(
    X_train,
    y_train
)

predicciones_gb = (
    modelo_gradient_boosting.predict(
        X_validacion
    )
)



# 24. MÉTRICAS GRADIENT BOOSTING


mae_gb = mean_absolute_error(
    y_validacion,
    predicciones_gb
)

rmse_gb = np.sqrt(
    mean_squared_error(
        y_validacion,
        predicciones_gb
    )
)

mape_gb = np.mean(
    np.abs(
        (
            y_validacion[mascara_mape]
            - predicciones_gb[mascara_mape]
        )
        / y_validacion[mascara_mape]
    )
) * 100


print("\n=== GRADIENT BOOSTING - VALIDACIÓN ===")
print(f"MAE:  {mae_gb:.2f}")
print(f"RMSE: {rmse_gb:.2f}")
print(f"MAPE: {mape_gb:.2f} %")

negativas_gb = (
    predicciones_gb < 0
).sum()

print(
    "Predicciones negativas:",
    negativas_gb
)



# 25. COMPARACIÓN PRELIMINAR


comparacion_modelos = pd.DataFrame({
    "modelo": [
        "Regresión Lineal",
        "Random Forest",
        "Gradient Boosting"
    ],

    "MAE": [
        mae_regresion,
        mae_rf,
        mae_gb
    ],

    "RMSE": [
        rmse_regresion,
        rmse_rf,
        rmse_gb
    ],

    "MAPE": [
        mape_regresion,
        mape_rf,
        mape_gb
    ],

    "predicciones_negativas": [
        predicciones_negativas,
        negativas_rf,
        negativas_gb
    ]
})


comparacion_modelos = (
    comparacion_modelos
    .sort_values("MAE")
    .reset_index(drop=True)
)


print("\n")
print("COMPARACIÓN PRELIMINAR - VALIDACIÓN")


print(
    comparacion_modelos.to_string(
        index=False
    )
)



# 26. GUARDAR PREDICCIONES


resultados_modelos = (
    validacion_completa[
        [
            "partido",
            "nivel",
            "anio",
            "matricula"
        ]
    ]
    .copy()
)

resultados_modelos[
    "prediccion_regresion"
] = predicciones_validacion

resultados_modelos[
    "prediccion_random_forest"
] = predicciones_rf

resultados_modelos[
    "prediccion_gradient_boosting"
] = predicciones_gb


ruta_resultados_modelos = (
    RUTA_MODELADO
    / "resultados_modelos_validacion.csv"
)

resultados_modelos.to_csv(
    ruta_resultados_modelos,
    index=False
)


ruta_comparacion = (
    RUTA_MODELADO
    / "comparacion_modelos_validacion.csv"
)

comparacion_modelos.to_csv(
    ruta_comparacion,
    index=False
)


print("\nResultados guardados correctamente:")
print(ruta_resultados_modelos)
print(ruta_comparacion)

# 27. COMPARAR CONJUNTOS DE VARIABLES


print("\n")

print("COMPARACIÓN DE CONJUNTOS DE VARIABLES")




# 28. DEFINIR CONJUNTOS


conjuntos_variables = {

    "A - Solo lag 1": [
        "matricula_lag_1"
    ],

    "B - Tres lags": [
        "matricula_lag_1",
        "matricula_lag_2",
        "matricula_lag_3"
    ],

    "C - Lags + partido + nivel": [
        "partido",
        "nivel",
        "matricula_lag_1",
        "matricula_lag_2",
        "matricula_lag_3"
    ],

    "D - Modelo completo": [
        "partido",
        "nivel",
        "anio",
        "matricula_lag_1",
        "matricula_lag_2",
        "matricula_lag_3",
        "variacion_anual_matricula",
        "tendencia_3_anios"
    ]
}



# 29. FUNCIÓN PARA EVALUAR CADA CONJUNTO


def evaluar_conjunto_random_forest(
    nombre,
    variables
):

    columnas = variables + ["matricula"]

    train_temp = train[
        columnas
    ].dropna().copy()

    validacion_temp = validacion[
        columnas
    ].dropna().copy()


    X_train_temp = train_temp[
        variables
    ]

    y_train_temp = train_temp[
        "matricula"
    ]

    X_validacion_temp = validacion_temp[
        variables
    ]

    y_validacion_temp = validacion_temp[
        "matricula"
    ]


    # ----------------------------------------
    # Separar variables categóricas y numéricas
    # ----------------------------------------

    categoricas = [
        variable
        for variable in variables
        if variable in ["partido", "nivel"]
    ]

    numericas = [
        variable
        for variable in variables
        if variable not in categoricas
    ]


    # ----------------------------------------
    # Preprocesamiento
    # ----------------------------------------

    transformaciones = []

    if categoricas:

        transformaciones.append(
            (
                "categoricas",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categoricas
            )
        )

    if numericas:

        transformaciones.append(
            (
                "numericas",
                "passthrough",
                numericas
            )
        )


    preprocesamiento_temp = ColumnTransformer(
        transformers=transformaciones
    )


    # ----------------------------------------
    # Modelo
    # ----------------------------------------

    modelo_temp = Pipeline(
        steps=[
            (
                "preprocesamiento",
                preprocesamiento_temp
            ),
            (
                "modelo",
                RandomForestRegressor(
                    n_estimators=200,
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )


    modelo_temp.fit(
        X_train_temp,
        y_train_temp
    )


    predicciones = modelo_temp.predict(
        X_validacion_temp
    )


    # ----------------------------------------
    # Métricas
    # ----------------------------------------

    mae = mean_absolute_error(
        y_validacion_temp,
        predicciones
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_validacion_temp,
            predicciones
        )
    )

    mascara = y_validacion_temp != 0

    mape = np.mean(
        np.abs(
            (
                y_validacion_temp[mascara]
                - predicciones[mascara]
            )
            / y_validacion_temp[mascara]
        )
    ) * 100


    negativas = (
        predicciones < 0
    ).sum()


    return {
        "conjunto": nombre,
        "variables": len(variables),
        "train_filas": len(train_temp),
        "validacion_filas": len(validacion_temp),
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "negativas": negativas
    }



# 30. EVALUAR TODOS LOS CONJUNTOS


resultados_conjuntos = []

for nombre, variables in conjuntos_variables.items():

    print(
        f"\nEvaluando: {nombre}"
    )

    resultado = evaluar_conjunto_random_forest(
        nombre,
        variables
    )

    resultados_conjuntos.append(
        resultado
    )



# 31. CREAR TABLA COMPARATIVA


comparacion_variables = pd.DataFrame(
    resultados_conjuntos
)

comparacion_variables = (
    comparacion_variables
    .sort_values("MAE")
    .reset_index(drop=True)
)


print("\n")

print("RESULTADOS POR CONJUNTO DE VARIABLES")


print(
    comparacion_variables.to_string(
        index=False
    )
)



# 32. GUARDAR RESULTADOS


ruta_comparacion_variables = (
    RUTA_MODELADO
    / "comparacion_conjuntos_variables.csv"
)

comparacion_variables.to_csv(
    ruta_comparacion_variables,
    index=False
)

print("\nResultados guardados correctamente:")
print(ruta_comparacion_variables)


# 33. AJUSTE CONTROLADO DE HIPERPARÁMETROS


from itertools import product

print("\n")
print("AJUSTE CONTROLADO DE HIPERPARÁMETROS")

# 34. USAR MISMAS FILAS PARA TODAS LAS CONFIGURACIONES


variables_ajuste = [
    "partido",
    "nivel",
    "anio",
    "matricula_lag_1",
    "matricula_lag_2",
    "matricula_lag_3",
    "variacion_anual_matricula",
    "tendencia_3_anios"
]

columnas_ajuste = (
    variables_ajuste
    + ["matricula"]
)

train_ajuste = (
    train[columnas_ajuste]
    .dropna()
    .copy()
)

validacion_ajuste = (
    validacion[columnas_ajuste]
    .dropna()
    .copy()
)

X_train_ajuste = train_ajuste[
    variables_ajuste
]

y_train_ajuste = train_ajuste[
    "matricula"
]

X_validacion_ajuste = validacion_ajuste[
    variables_ajuste
]

y_validacion_ajuste = validacion_ajuste[
    "matricula"
]

print(
    "\nFilas de entrenamiento:",
    len(train_ajuste)
)

print(
    "Filas de validación:",
    len(validacion_ajuste)
)



# 35. FUNCIÓN PARA CALCULAR MÉTRICAS


def calcular_metricas(
    reales,
    predicciones
):

    mae = mean_absolute_error(
        reales,
        predicciones
    )

    rmse = np.sqrt(
        mean_squared_error(
            reales,
            predicciones
        )
    )

    mascara = reales != 0

    mape = np.mean(
        np.abs(
            (
                reales[mascara]
                - predicciones[mascara]
            )
            / reales[mascara]
        )
    ) * 100

    negativas = (
        predicciones < 0
    ).sum()

    return (
        mae,
        rmse,
        mape,
        negativas
    )



# 36. CONFIGURACIONES RANDOM FOREST


configuraciones_rf = [
    {
        "n_estimators": 200,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": 1.0
    },
    {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 2,
        "max_features": 1.0
    },
    {
        "n_estimators": 300,
        "max_depth": 15,
        "min_samples_leaf": 1,
        "max_features": 1.0
    },
    {
        "n_estimators": 300,
        "max_depth": 15,
        "min_samples_leaf": 2,
        "max_features": 1.0
    },
    {
        "n_estimators": 300,
        "max_depth": 10,
        "min_samples_leaf": 2,
        "max_features": 1.0
    },
    {
        "n_estimators": 300,
        "max_depth": None,
        "min_samples_leaf": 2,
        "max_features": 0.7
    }
]


resultados_rf_ajuste = []


print("\n")
print("RANDOM FOREST")
print("-" * 70)


for numero, config in enumerate(
    configuraciones_rf,
    start=1
):

    modelo_rf_temp = Pipeline(
        steps=[
            (
                "preprocesamiento",
                preprocesamiento
            ),
            (
                "modelo",
                RandomForestRegressor(
                    n_estimators=config[
                        "n_estimators"
                    ],
                    max_depth=config[
                        "max_depth"
                    ],
                    min_samples_leaf=config[
                        "min_samples_leaf"
                    ],
                    max_features=config[
                        "max_features"
                    ],
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )

    modelo_rf_temp.fit(
        X_train_ajuste,
        y_train_ajuste
    )

    predicciones = (
        modelo_rf_temp.predict(
            X_validacion_ajuste
        )
    )

    mae, rmse, mape, negativas = (
        calcular_metricas(
            y_validacion_ajuste,
            predicciones
        )
    )

    resultados_rf_ajuste.append({
        "modelo": "Random Forest",
        "configuracion": numero,
        "n_estimators": config[
            "n_estimators"
        ],
        "max_depth": config[
            "max_depth"
        ],
        "min_samples_leaf": config[
            "min_samples_leaf"
        ],
        "max_features": config[
            "max_features"
        ],
        "learning_rate": np.nan,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "negativas": negativas
    })

    print(
        f"Configuración {numero}: "
        f"MAE={mae:.2f} | "
        f"RMSE={rmse:.2f} | "
        f"MAPE={mape:.2f}%"
    )



# 37. CONFIGURACIONES GRADIENT BOOSTING


configuraciones_gb = [
    {
        "n_estimators": 100,
        "learning_rate": 0.10,
        "max_depth": 3
    },
    {
        "n_estimators": 200,
        "learning_rate": 0.05,
        "max_depth": 3
    },
    {
        "n_estimators": 300,
        "learning_rate": 0.03,
        "max_depth": 3
    },
    {
        "n_estimators": 150,
        "learning_rate": 0.05,
        "max_depth": 2
    },
    {
        "n_estimators": 200,
        "learning_rate": 0.05,
        "max_depth": 2
    },
    {
        "n_estimators": 200,
        "learning_rate": 0.03,
        "max_depth": 2
    }
]


resultados_gb_ajuste = []


print("\n")
print("GRADIENT BOOSTING")
print("-" * 70)


for numero, config in enumerate(
    configuraciones_gb,
    start=1
):

    modelo_gb_temp = Pipeline(
        steps=[
            (
                "preprocesamiento",
                preprocesamiento
            ),
            (
                "modelo",
                GradientBoostingRegressor(
                    n_estimators=config[
                        "n_estimators"
                    ],
                    learning_rate=config[
                        "learning_rate"
                    ],
                    max_depth=config[
                        "max_depth"
                    ],
                    random_state=42
                )
            )
        ]
    )

    modelo_gb_temp.fit(
        X_train_ajuste,
        y_train_ajuste
    )

    predicciones = (
        modelo_gb_temp.predict(
            X_validacion_ajuste
        )
    )

    mae, rmse, mape, negativas = (
        calcular_metricas(
            y_validacion_ajuste,
            predicciones
        )
    )

    resultados_gb_ajuste.append({
        "modelo": "Gradient Boosting",
        "configuracion": numero,
        "n_estimators": config[
            "n_estimators"
        ],
        "max_depth": config[
            "max_depth"
        ],
        "min_samples_leaf": np.nan,
        "max_features": np.nan,
        "learning_rate": config[
            "learning_rate"
        ],
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "negativas": negativas
    })

    print(
        f"Configuración {numero}: "
        f"MAE={mae:.2f} | "
        f"RMSE={rmse:.2f} | "
        f"MAPE={mape:.2f}%"
    )



# 38. COMPARAR CONFIGURACIONES


resultados_hiperparametros = pd.DataFrame(
    resultados_rf_ajuste
    + resultados_gb_ajuste
)

resultados_hiperparametros = (
    resultados_hiperparametros
    .sort_values("MAE")
    .reset_index(drop=True)
)


print("\n")
print("RESULTADOS DEL AJUSTE DE HIPERPARÁMETROS")

print(
    resultados_hiperparametros.to_string(
        index=False
    )
)



# 39. MEJOR CONFIGURACIÓN DE CADA MODELO


mejor_rf = (
    resultados_hiperparametros[
        resultados_hiperparametros[
            "modelo"
        ] == "Random Forest"
    ]
    .sort_values("MAE")
    .iloc[0]
)

mejor_gb = (
    resultados_hiperparametros[
        resultados_hiperparametros[
            "modelo"
        ] == "Gradient Boosting"
    ]
    .sort_values("MAE")
    .iloc[0]
)


print("\n")

print("MEJORES CONFIGURACIONES")


print("\nRandom Forest:")
print(mejor_rf)

print("\nGradient Boosting:")
print(mejor_gb)



# 40. GUARDAR RESULTADOS


ruta_hiperparametros = (
    RUTA_MODELADO
    / "ajuste_hiperparametros.csv"
)

resultados_hiperparametros.to_csv(
    ruta_hiperparametros,
    index=False
)

print("\nResultados guardados correctamente:")
print(ruta_hiperparametros)


# 41. COMPARACIÓN FINAL DE MODELOS DE MACHINE LEARNING


print("\n")

print("COMPARACIÓN FINAL DE MODELOS - VALIDACIÓN")




# 42. REGRESIÓN LINEAL SOBRE LAS MISMAS 808 FILAS


modelo_regresion_final = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
        (
            "modelo",
            LinearRegression()
        )
    ]
)

modelo_regresion_final.fit(
    X_train_ajuste,
    y_train_ajuste
)

pred_regresion_final = (
    modelo_regresion_final.predict(
        X_validacion_ajuste
    )
)

mae_lr_final, rmse_lr_final, mape_lr_final, neg_lr_final = (
    calcular_metricas(
        y_validacion_ajuste,
        pred_regresion_final
    )
)



# 43. RANDOM FOREST CON MEJORES HIPERPARÁMETROS


modelo_rf_final = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
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

modelo_rf_final.fit(
    X_train_ajuste,
    y_train_ajuste
)

pred_rf_final = (
    modelo_rf_final.predict(
        X_validacion_ajuste
    )
)

mae_rf_final, rmse_rf_final, mape_rf_final, neg_rf_final = (
    calcular_metricas(
        y_validacion_ajuste,
        pred_rf_final
    )
)



# 44. GRADIENT BOOSTING CON MEJORES HIPERPARÁMETROS


modelo_gb_final = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento
        ),
        (
            "modelo",
            GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=3,
                random_state=42
            )
        )
    ]
)

modelo_gb_final.fit(
    X_train_ajuste,
    y_train_ajuste
)

pred_gb_final = (
    modelo_gb_final.predict(
        X_validacion_ajuste
    )
)

mae_gb_final, rmse_gb_final, mape_gb_final, neg_gb_final = (
    calcular_metricas(
        y_validacion_ajuste,
        pred_gb_final
    )
)



# 45. CREAR TABLA FINAL DE COMPARACIÓN


comparacion_final_ml = pd.DataFrame({

    "modelo": [
        "Regresión Lineal",
        "Random Forest ajustado",
        "Gradient Boosting ajustado"
    ],

    "MAE": [
        mae_lr_final,
        mae_rf_final,
        mae_gb_final
    ],

    "RMSE": [
        rmse_lr_final,
        rmse_rf_final,
        rmse_gb_final
    ],

    "MAPE": [
        mape_lr_final,
        mape_rf_final,
        mape_gb_final
    ],

    "predicciones_negativas": [
        neg_lr_final,
        neg_rf_final,
        neg_gb_final
    ]
})


comparacion_final_ml = (
    comparacion_final_ml
    .sort_values("MAE")
    .reset_index(drop=True)
)


print("\nResultados sobre las mismas 808 observaciones:\n")

print(
    comparacion_final_ml.to_string(
        index=False
    )
)



# 46. IDENTIFICAR MEJOR MODELO SEGÚN MAE


mejor_modelo_ml = (
    comparacion_final_ml.iloc[0]
)

print("\n")

print("MEJOR MODELO DE MACHINE LEARNING")


print(
    "\nModelo:",
    mejor_modelo_ml["modelo"]
)

print(
    f"MAE: {mejor_modelo_ml['MAE']:.2f}"
)

print(
    f"RMSE: {mejor_modelo_ml['RMSE']:.2f}"
)

print(
    f"MAPE: {mejor_modelo_ml['MAPE']:.2f} %"
)

print(
    "Predicciones negativas:",
    int(
        mejor_modelo_ml[
            "predicciones_negativas"
        ]
    )
)



# 47. GUARDAR PREDICCIONES Y COMPARACIÓN


resultados_finales_ml = (
    validacion_ajuste[
        [
            "partido",
            "nivel",
            "anio",
            "matricula"
        ]
    ]
    .copy()
)

resultados_finales_ml[
    "prediccion_regresion"
] = pred_regresion_final

resultados_finales_ml[
    "prediccion_random_forest"
] = pred_rf_final

resultados_finales_ml[
    "prediccion_gradient_boosting"
] = pred_gb_final


ruta_comparacion_final = (
    RUTA_MODELADO
    / "comparacion_final_modelos_ml.csv"
)

ruta_predicciones_finales = (
    RUTA_MODELADO
    / "predicciones_validacion_modelos_ml.csv"
)


comparacion_final_ml.to_csv(
    ruta_comparacion_final,
    index=False
)

resultados_finales_ml.to_csv(
    ruta_predicciones_finales,
    index=False
)


print("\nResultados guardados correctamente:")
print(ruta_comparacion_final)
print(ruta_predicciones_finales)


# 48. COMPARACIÓN FORMAL CONTRA BASELINE


print("\n")

print("COMPARACIÓN FORMAL - RANDOM FOREST VS BASELINE")




# 49. OBTENER PREDICCIONES DEL BASELINE


# El baseline predice que la matrícula será igual
# a la del año inmediatamente anterior.

predicciones_baseline_final = (
    X_validacion_ajuste["matricula_lag_1"]
    .to_numpy()
)



# 50. CALCULAR MÉTRICAS DEL BASELINE


mae_baseline_final, rmse_baseline_final, mape_baseline_final, neg_baseline_final = (
    calcular_metricas(
        y_validacion_ajuste,
        predicciones_baseline_final
    )
)


print("\n=== BASELINE - MISMAS 808 OBSERVACIONES ===")

print(f"MAE:  {mae_baseline_final:.2f}")
print(f"RMSE: {rmse_baseline_final:.2f}")
print(f"MAPE: {mape_baseline_final:.2f} %")



# 51. COMPARAR BASELINE Y RANDOM FOREST


comparacion_baseline_rf = pd.DataFrame({

    "modelo": [
        "Baseline",
        "Random Forest ajustado"
    ],

    "MAE": [
        mae_baseline_final,
        mae_rf_final
    ],

    "RMSE": [
        rmse_baseline_final,
        rmse_rf_final
    ],

    "MAPE": [
        mape_baseline_final,
        mape_rf_final
    ],

    "predicciones_negativas": [
        neg_baseline_final,
        neg_rf_final
    ]
})


comparacion_baseline_rf = (
    comparacion_baseline_rf
    .sort_values("MAE")
    .reset_index(drop=True)
)


print("\n")

print("RESULTADO FINAL - BASELINE VS RANDOM FOREST")


print(
    comparacion_baseline_rf.to_string(
        index=False
    )
)



# 52. CALCULAR DIFERENCIA DE MAE


diferencia_mae = (
    mae_rf_final
    - mae_baseline_final
)

diferencia_porcentual = (
    diferencia_mae
    / mae_baseline_final
) * 100


print("\n")

print("DIFERENCIA ENTRE MODELOS")


print(
    f"Diferencia de MAE: {diferencia_mae:.2f} alumnos"
)

print(
    f"Diferencia porcentual: {diferencia_porcentual:.2f} %"
)


if mae_rf_final < mae_baseline_final:

    print(
        "\nRandom Forest supera al baseline."
    )

elif mae_rf_final > mae_baseline_final:

    print(
        "\nEl baseline supera a Random Forest."
    )

else:

    print(
        "\nAmbos modelos obtuvieron el mismo MAE."
    )



# 53. GUARDAR COMPARACIÓN


ruta_comparacion_baseline = (
    RUTA_MODELADO
    / "comparacion_baseline_random_forest.csv"
)

comparacion_baseline_rf.to_csv(
    ruta_comparacion_baseline,
    index=False
)


print("\nResultados guardados correctamente:")
print(ruta_comparacion_baseline)