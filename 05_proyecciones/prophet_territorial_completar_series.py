
from pathlib import Path
import pandas as pd

MODELOS_DIR = Path(__file__).resolve().parent

archivo = (
    MODELOS_DIR /
    "proyecciones_prophet_territorial_2026_2035_corregidas.csv"
)

df = pd.read_csv(archivo)

# Series con historial incompleto
series_respaldo = [
    ("CASTELLI", "SECUNDARIA", 558.0, "respaldo_historial_corto"),
    ("LEZAMA", "SECUNDARIA", 65.0, "persistencia_historial_incompleto")
]

nuevas_filas = []
registro = []

for partido, nivel, valor, metodo in series_respaldo:

    existe = (
        (df["partido"] == partido) &
        (df["nivel"] == nivel)
    ).any()

    if existe:
        raise ValueError(
            f"La serie {partido} - {nivel} ya existe."
        )

    for anio in range(2026, 2036):
        nuevas_filas.append({
            "partido": partido,
            "nivel": nivel,
            "anio": anio,
            "prophet": valor,
            "prediccion_original": float("nan")
        })

    registro.append({
        "partido": partido,
        "nivel": nivel,
        "valor_anual": valor,
        "metodo": metodo
    })

completo = pd.concat(
    [df, pd.DataFrame(nuevas_filas)],
    ignore_index=True
)

completo = completo.sort_values(
    ["partido", "nivel", "anio"]
).reset_index(drop=True)

# Verificaciones de cobertura
assert len(completo) == 4050
assert completo.groupby(["partido", "nivel"]).ngroups == 405
assert not completo.duplicated(
    ["partido", "nivel", "anio"]
).any()
assert completo["prophet"].notna().all()

# Guardar resultados completos
completo.to_csv(
    MODELOS_DIR /
    "proyecciones_prophet_territorial_2026_2035_completas.csv",
    index=False
)

pd.DataFrame(registro).to_csv(
    MODELOS_DIR / "registro_series_respaldo_prophet.csv",
    index=False
)

por_nivel = (
    completo.groupby(["anio", "nivel"], as_index=False)["prophet"]
    .sum()
)

provincial = (
    completo.groupby("anio", as_index=False)["prophet"]
    .sum()
)

por_nivel.to_csv(
    MODELOS_DIR /
    "totales_prophet_territorial_completos_por_nivel.csv",
    index=False
)

provincial.to_csv(
    MODELOS_DIR /
    "totales_prophet_territorial_completos_provincial.csv",
    index=False
)

print("\n========== PROPHET TERRITORIAL COMPLETO ==========")
print("Series territoriales:", completo.groupby(
    ["partido", "nivel"]
).ngroups)
print("Predicciones totales:", len(completo))
print("Series incorporadas:", len(registro))

print("\nTOTAL PROVINCIAL POR AÑO")
print(provincial.round(2).to_string(index=False))

print("\nTOTAL POR NIVEL EN 2035")
print(
    por_nivel[por_nivel["anio"] == 2035]
    .round(2).to_string(index=False)
)

print("\nArchivos guardados correctamente.")
