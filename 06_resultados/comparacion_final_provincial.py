
from pathlib import Path
import numpy as np
import pandas as pd

# Carpetas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = Path(__file__).resolve().parent

# Predicciones originales de Random Forest y persistencia
ruta = BASE_DIR / "modelado" / "predicciones_test_recursivo.csv"
df = pd.read_csv(ruta)

# Agrupar por año y nivel educativo
provincial = (
    df.groupby(["anio", "nivel"])[
        ["matricula_real", "baseline", "random_forest"]
    ]
    .sum(min_count=1)
    .reset_index()
)

# Resultados ya calculados de ARIMA y Prophet
# MAE, RMSE y MAPE del test 2024-2025
metricas_anteriores = {
    "INICIAL": {
        "ARIMA": (55008.99, 58085.40, 9.36),
        "Prophet": (17653.35, 19060.76, 3.01)
    },
    "PRIMARIA": {
        "ARIMA": (65188.03, 70252.18, 4.00),
        "Prophet": (101696.86, 105825.06, 6.22)
    },
    "SECUNDARIA": {
        "ARIMA": (29580.24, 30359.43, 1.79),
        "Prophet": (52765.83, 53706.56, 3.19)
    }
}

resultados = []

# Calcular métricas provinciales para los modelos originales
for nivel in ["INICIAL", "PRIMARIA", "SECUNDARIA"]:

    datos = provincial[
        provincial["nivel"] == nivel
    ].sort_values("anio")

    reales = datos["matricula_real"].to_numpy()

    for nombre, columna in [
        ("Persistencia", "baseline"),
        ("Random Forest", "random_forest")
    ]:

        predicciones = datos[columna].to_numpy()

        mae = np.mean(np.abs(reales - predicciones))

        rmse = np.sqrt(
            np.mean((reales - predicciones) ** 2)
        )

        mape = np.mean(
            np.abs((reales - predicciones) / reales)
        ) * 100

        resultados.append({
            "nivel": nivel,
            "modelo": nombre,
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "MAPE": round(mape, 2)
        })

    # Incorporar resultados de ARIMA y Prophet
    for nombre, valores in metricas_anteriores[nivel].items():

        mae, rmse, mape = valores

        resultados.append({
            "nivel": nivel,
            "modelo": nombre,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        })

# Tabla final
tabla = pd.DataFrame(resultados)

print("\n========== COMPARACIÓN PROVINCIAL 2024-2025 ==========")
print(
    tabla.sort_values(["nivel", "MAE"])
    .to_string(index=False)
)

# Guardar resultados
salida = MODELOS_DIR / "comparacion_final_provincial.csv"
tabla.to_csv(salida, index=False)

print(f"\nResultados guardados en: {salida}")

# Mostrar predicciones provinciales originales
print("\n========== TOTALES PROVINCIALES ==========")
print(provincial.to_string(index=False))

print("\nNOTA METODOLÓGICA:")
print(
    "En Secundaria, Random Forest y persistencia "
    "cubren 134 partidos, mientras que ARIMA y Prophet "
    "utilizan los totales provinciales de 135 partidos."
)
