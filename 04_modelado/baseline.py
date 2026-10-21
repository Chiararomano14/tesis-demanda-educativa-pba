import pandas as pd
import numpy as np
from pathlib import Path



# 1. RUTAS


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_MODELADO = RUTA_PROYECTO / "04_modelado"

ruta_validacion = RUTA_MODELADO / "validacion.csv"
ruta_test = RUTA_MODELADO / "test.csv"



# 2. CARGAR VALIDACIÓN Y TEST


validacion = pd.read_csv(ruta_validacion)
test = pd.read_csv(ruta_test)

print("\n=== DATOS CARGADOS ===")
print("Validación:", validacion.shape)
print("Test:", test.shape)



# 3. CREAR PREDICCIÓN BASELINE


# Baseline de persistencia:
# matrícula del próximo año = matrícula del año anterior

validacion["prediccion_baseline"] = (
    validacion["matricula_lag_1"]
)

test["prediccion_baseline"] = (
    test["matricula_lag_1"]
)



# 4. ELIMINAR SOLO CASOS SIN INFORMACIÓN PARA EL BASELINE


validacion_baseline = validacion.dropna(
    subset=["matricula", "prediccion_baseline"]
).copy()

test_baseline = test.dropna(
    subset=["matricula", "prediccion_baseline"]
).copy()


print("\n=== OBSERVACIONES EVALUABLES ===")
print("Validación:", len(validacion_baseline))
print("Test:", len(test_baseline))



# 5. FUNCIÓN PARA CALCULAR MÉTRICAS


def calcular_metricas(datos):

    real = datos["matricula"]
    predicho = datos["prediccion_baseline"]

    # Error absoluto medio
    mae = np.mean(
        np.abs(real - predicho)
    )

    # Raíz del error cuadrático medio
    rmse = np.sqrt(
        np.mean((real - predicho) ** 2)
    )

    # Error porcentual absoluto medio
    # Evitamos divisiones por cero
    mascara_mape = real != 0

    mape = np.mean(
        np.abs(
            (
                real[mascara_mape]
                - predicho[mascara_mape]
            )
            / real[mascara_mape]
        )
    ) * 100

    return mae, rmse, mape



# 6. MÉTRICAS DE VALIDACIÓN


mae_val, rmse_val, mape_val = calcular_metricas(
    validacion_baseline
)

print("\n=== BASELINE - VALIDACIÓN ===")
print(f"MAE:  {mae_val:.2f}")
print(f"RMSE: {rmse_val:.2f}")
print(f"MAPE: {mape_val:.2f} %")



# 7. MÉTRICAS DE TEST


mae_test, rmse_test, mape_test = calcular_metricas(
    test_baseline
)

print("\n=== BASELINE - TEST ===")
print(f"MAE:  {mae_test:.2f}")
print(f"RMSE: {rmse_test:.2f}")
print(f"MAPE: {mape_test:.2f} %")



# 8. RESULTADOS POR NIVEL EDUCATIVO


print("\n=== BASELINE POR NIVEL - TEST ===")

for nivel in sorted(
    test_baseline["nivel"].unique()
):

    datos_nivel = test_baseline[
        test_baseline["nivel"] == nivel
    ]

    mae, rmse, mape = calcular_metricas(
        datos_nivel
    )

    print(f"\n{nivel}")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f} %")



# 9. ERROR POR AÑO EN TEST


print("\n=== BASELINE POR AÑO - TEST ===")

for anio in sorted(
    test_baseline["anio"].unique()
):

    datos_anio = test_baseline[
        test_baseline["anio"] == anio
    ]

    mae, rmse, mape = calcular_metricas(
        datos_anio
    )

    print(f"\nAño {anio}")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f} %")



# 10. GUARDAR PREDICCIONES DEL BASELINE


ruta_resultados = (
    RUTA_MODELADO
    / "resultados_baseline_test.csv"
)

test_baseline.to_csv(
    ruta_resultados,
    index=False
)

print("\nResultados guardados correctamente:")
print(ruta_resultados)