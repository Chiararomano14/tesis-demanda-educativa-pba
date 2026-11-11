
from pathlib import Path
import pandas as pd

MODELOS_DIR = Path(__file__).resolve().parent

archivo = MODELOS_DIR / "proyecciones_prophet_territorial_2026_2035.csv"

df = pd.read_csv(archivo)

# Casos detectados durante la revisión de estabilidad
correcciones = [
    ("CASTELLI", "INICIAL", 294.0),
    ("LEZAMA", "INICIAL", 7.0),
    ("LEZAMA", "PRIMARIA", 44.0)
]

registro = []

for partido, nivel, valor in correcciones:

    mascara = (
        (df["partido"] == partido) &
        (df["nivel"] == nivel)
    )

    filas = df.loc[mascara].copy()

    if len(filas) != 10:
        raise ValueError(
            f"Se esperaban 10 predicciones para {partido} - {nivel}"
        )

    for _, fila in filas.iterrows():
        registro.append({
            "partido": partido,
            "nivel": nivel,
            "anio": int(fila["anio"]),
            "prophet_original": float(fila["prophet"]),
            "valor_corregido": valor,
            "metodo": "persistencia_por_estabilidad"
        })

    df.loc[mascara, "prophet"] = valor

# Guardar las proyecciones corregidas
df.to_csv(
    MODELOS_DIR / "proyecciones_prophet_territorial_2026_2035_corregidas.csv",
    index=False
)

pd.DataFrame(registro).to_csv(
    MODELOS_DIR / "registro_correcciones_estabilidad_prophet.csv",
    index=False
)

# Calcular totales actualizados
por_nivel = (
    df.groupby(["anio", "nivel"], as_index=False)["prophet"]
    .sum()
)

provincial = (
    df.groupby("anio", as_index=False)["prophet"]
    .sum()
)

por_nivel.to_csv(
    MODELOS_DIR / "totales_prophet_corregidos_por_nivel.csv",
    index=False
)

provincial.to_csv(
    MODELOS_DIR / "totales_prophet_corregidos_provincial.csv",
    index=False
)

print("\n========== CORRECCION FINAL PROPHET ==========")
print("Series corregidas:", len(correcciones))
print("Predicciones totales:", len(df))

print("\nTOTAL PROVINCIAL POR AÑO")
print(provincial.round(2).to_string(index=False))

print("\nTOTAL POR NIVEL EN 2035")
print(
    por_nivel[por_nivel["anio"] == 2035]
    .round(2).to_string(index=False)
)

print("\nArchivos guardados correctamente.")
