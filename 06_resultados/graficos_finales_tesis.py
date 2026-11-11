
# GRAFICOS FINALES - TESIS DE CIENCIA DE DATOS
# Prediccion de la matricula educativa en Buenos Aires

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# 1. CONFIGURACION GENERAL

MODELOS_DIR = Path(__file__).resolve().parent
BASE_DIR = MODELOS_DIR.parent
MODELADO_DIR = BASE_DIR / "modelado"

GRAFICOS_DIR = MODELOS_DIR / "graficos_finales"
GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

NIVELES = ["INICIAL", "PRIMARIA", "SECUNDARIA"]

MODELOS = [
    "random_forest",
    "arima",
    "prophet",
    "persistencia"
]

NOMBRES = {
    "random_forest": "Random Forest",
    "arima": "ARIMA",
    "prophet": "Prophet",
    "persistencia": "Persistencia"
}

COLORES = {
    "random_forest": "#4472C4",
    "arima": "#ED7D31",
    "prophet": "#70AD47",
    "persistencia": "#A5A5A5",
    "tendencia": "#9467BD"
}


# 2. FUNCION PARA GUARDAR GRAFICOS

def guardar_grafico(fig, nombre):

    ruta_png = GRAFICOS_DIR / f"{nombre}.png"
    ruta_pdf = GRAFICOS_DIR / f"{nombre}.pdf"

    fig.savefig(
        ruta_png,
        dpi=300,
        bbox_inches="tight"
    )

    fig.savefig(
        ruta_pdf,
        bbox_inches="tight"
    )

    print(f"\nGrafico guardado: {nombre}")
    print("PNG:", ruta_png)
    print("PDF:", ruta_pdf)


# FIGURA 8 - COMPARACION DEL MAE POR NIVEL EDUCATIVO

def figura_8_comparacion_mae():

    # Cargar resultados definitivos del test
    df = pd.read_csv(
        MODELOS_DIR / "metricas_comparacion_final.csv"
    )

    df = df[df["escala"] == "territorial"].copy()

    fig, axes = plt.subplots(
        1, 3,
        figsize=(15, 5.5)
    )

    for ax, nivel in zip(axes, NIVELES):

        datos = df[
            df["nivel"] == nivel
        ].set_index("modelo")

        valores = [
            datos.loc[modelo, "MAE"]
            for modelo in MODELOS
        ]

        etiquetas = [
            NOMBRES[modelo]
            for modelo in MODELOS
        ]

        colores = [
            COLORES[modelo]
            for modelo in MODELOS
        ]

        barras = ax.bar(
            etiquetas,
            valores,
            color=colores,
            width=0.65
        )

        mejor_valor = min(valores)

        for barra, valor in zip(barras, valores):

            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 8,
                f"{valor:.1f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight=(
                    "bold"
                    if valor == mejor_valor
                    else "normal"
                )
            )

        ax.set_title(
            nivel.capitalize(),
            fontsize=13,
            fontweight="bold",
            pad=12
        )

        ax.set_ylabel("MAE (estudiantes)")
        ax.set_ylim(0, max(valores) * 1.20)

        ax.tick_params(axis="x", rotation=30)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.grid(
            axis="y",
            alpha=0.2,
            linestyle="--"
        )

        ax.set_axisbelow(True)

    fig.suptitle(
        "Comparacion del error de prediccion por nivel educativo",
        fontsize=16,
        fontweight="bold",
        y=0.97
    )

    fig.text(
        0.5,
        0.025,
        "Test 2024-2025 | 806 observaciones comparables | "
        "Menor MAE indica mejor desempeño",
        ha="center",
        fontsize=10
    )

    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        top=0.82,
        bottom=0.25,
        wspace=0.25
    )

    guardar_grafico(
        fig,
        "figura_8_comparacion_mae"
    )

    plt.show()
    plt.close(fig)


# FIGURA 9 - ERROR SEGUN HORIZONTE DE PREDICCION

def figura_9_comparacion_horizontes():

    # Cargar metricas por horizonte
    df = pd.read_csv(
        MODELOS_DIR / "metricas_comparacion_horizontes.csv"
    )

    df = df[df["escala"] == "territorial"].copy()

    fig, axes = plt.subplots(
        1, 3,
        figsize=(15, 5.5)
    )

    for ax, nivel in zip(axes, NIVELES):

        datos_nivel = df[
            df["nivel"] == nivel
        ]

        for modelo in MODELOS:

            datos = datos_nivel[
                datos_nivel["modelo"] == modelo
            ].sort_values("horizonte")

            ax.plot(
                datos["horizonte"],
                datos["MAE"],
                marker="o",
                markersize=7,
                linewidth=2.5,
                color=COLORES[modelo],
                label=NOMBRES[modelo]
            )

        ax.set_title(
            nivel.capitalize(),
            fontsize=14,
            fontweight="bold",
            pad=12
        )

        ax.set_xticks([1, 2])
        ax.set_xticklabels([
            "2024 (H1)",
            "2025 (H2)"
        ])

        ax.set_xlim(0.85, 2.15)

        ax.set_ylabel(
            "MAE (estudiantes)",
            fontsize=11
        )

        ax.set_ylim(
            0,
            datos_nivel["MAE"].max() * 1.15
        )

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.25
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)

    fig.suptitle(
        "Evolucion del error segun el horizonte de prediccion",
        fontsize=16,
        fontweight="bold",
        y=0.97
    )

    handles, labels = axes[0].get_legend_handles_labels()

    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.09),
        ncol=4,
        frameon=False,
        fontsize=11
    )

    fig.text(
        0.5,
        0.025,
        "Test 2024-2025 | Entrenamiento hasta 2023 | "
        "Menor MAE indica mejor desempeño",
        ha="center",
        fontsize=10
    )

    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        top=0.82,
        bottom=0.25,
        wspace=0.25
    )

    guardar_grafico(
        fig,
        "figura_9_comparacion_horizontes"
    )

    plt.show()
    plt.close(fig)


# FIGURA 10 - EVOLUCION HISTORICA Y PROYECCIONES

def figura_10_evolucion_proyecciones():

    # 1. CARGAR MATRICULA HISTORICA (2012-2025)

    historico = pd.read_csv(
        BASE_DIR / "dataset_modelado_features.csv"
    )

    historico = historico[
        historico["anio"].between(2012, 2025)
    ].copy()

    historico = (
        historico.groupby("anio", as_index=False)["matricula"]
        .sum()
    )

    # 2. CARGAR PROYECCIONES ARIMA

    arima = pd.read_csv(
        MODELOS_DIR /
        "proyecciones_arima_territorial_2026_2035_completas.csv"
    )

    arima = (
        arima.groupby("anio", as_index=False)["matricula_predicha"]
        .sum()
    )

    # 3. CARGAR PROYECCIONES PROPHET

    prophet = pd.read_csv(
        MODELOS_DIR /
        "proyecciones_prophet_territorial_2026_2035_completas.csv"
    )

    prophet = (
        prophet.groupby("anio", as_index=False)["prophet"]
        .sum()
    )

    # 4. CARGAR RANDOM FOREST Y PERSISTENCIA

    rf = pd.read_csv(
        MODELADO_DIR /
        "proyecciones_provinciales_2026_2035.csv"
    )

    # 5. VERIFICAR LOS DATOS

    for nombre, datos in [
        ("ARIMA", arima),
        ("Prophet", prophet),
        ("Random Forest", rf)
    ]:
        if sorted(datos["anio"].tolist()) != list(range(2026, 2036)):
            raise ValueError(
                f"Los años de proyección no coinciden en {nombre}"
            )

    valor_2025 = historico.loc[
        historico["anio"] == 2025,
        "matricula"
    ].iloc[0]

    print("\n========== FIGURA 10 ==========")
    print("Matricula historica 2025:", round(valor_2025))

    # Convertir a millones para el gráfico
    historico["matricula"] /= 1_000_000
    arima["matricula_predicha"] /= 1_000_000
    prophet["prophet"] /= 1_000_000

    rf["prediccion_random_forest"] /= 1_000_000
    rf["prediccion_baseline"] /= 1_000_000
    rf["prediccion_tendencia"] /= 1_000_000

    valor_inicial = valor_2025 / 1_000_000

    # 6. CREAR FIGURA

    fig, ax = plt.subplots(figsize=(14, 6.5))

    ax.plot(
        historico["anio"],
        historico["matricula"],
        color="#222222",
        linewidth=3,
        marker="o",
        markersize=4,
        label="Matricula historica",
        zorder=5
    )

    # Cada proyección comienza en el último dato real
    series = [
        (
            arima,
            "matricula_predicha",
            "arima",
            "ARIMA territorial",
            "-"
        ),
        (
            prophet,
            "prophet",
            "prophet",
            "Prophet territorial",
            "-"
        ),
        (
            rf,
            "prediccion_random_forest",
            "random_forest",
            "Random Forest",
            "-"
        ),
        (
            rf,
            "prediccion_baseline",
            "persistencia",
            "Persistencia",
            "--"
        ),
        (
            rf,
            "prediccion_tendencia",
            "tendencia",
            "Tendencia reciente",
            "-."
        )
    ]

    for datos, columna, modelo, etiqueta, estilo in series:

        anios = [2025] + datos["anio"].tolist()
        valores = [valor_inicial] + datos[columna].tolist()

        ax.plot(
            anios,
            valores,
            color=COLORES[modelo],
            linewidth=2.5,
            linestyle=estilo,
            label=etiqueta
        )

    # Separar historia y proyecciones
    ax.axvline(
        2025,
        color="#777777",
        linestyle=":",
        linewidth=1.5
    )

    ax.axvspan(
        2025,
        2035,
        color="#A5A5A5",
        alpha=0.06
    )

    ax.set_title(
        "Evolucion historica y proyecciones de la matricula educativa",
        fontsize=16,
        fontweight="bold",
        pad=18
    )

    ax.set_xlabel("Año", fontsize=11)

    ax.set_ylabel(
        "Matricula (millones de estudiantes)",
        fontsize=11
    )

    ax.set_xlim(2012, 2035)
    ax.set_xticks([2012, 2015, 2018, 2021, 2025, 2028, 2031, 2035])

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=5,
        frameon=False,
        fontsize=10
    )

    fig.subplots_adjust(
        left=0.09,
        right=0.98,
        top=0.88,
        bottom=0.23
    )

    # 7. GUARDAR FIGURA

    guardar_grafico(
        fig,
        "figura_10_evolucion_proyecciones"
    )

    print("\nPROYECCIONES PARA 2035")
    print(
        "ARIMA:",
        round(arima["matricula_predicha"].iloc[-1] * 1_000_000)
    )
    print(
        "Prophet:",
        round(prophet["prophet"].iloc[-1] * 1_000_000)
    )
    print(
        "Random Forest:",
        round(rf["prediccion_random_forest"].iloc[-1] * 1_000_000)
    )
    print(
        "Persistencia:",
        round(rf["prediccion_baseline"].iloc[-1] * 1_000_000)
    )
    print(
        "Tendencia reciente:",
        round(rf["prediccion_tendencia"].iloc[-1] * 1_000_000)
    )

    plt.show()
    plt.close(fig)



# FIGURAS 11, 12 Y 13 - PROYECCIONES POR NIVEL EDUCATIVO
def graficos_proyecciones_por_nivel():

    # 1. CARGAR DATOS HISTORICOS

    historico = pd.read_csv(
        BASE_DIR / "dataset_modelado_features.csv"
    )

    historico = historico[
        historico["anio"].between(2012, 2025)
    ].copy()

    historico = (
        historico.groupby(
            ["anio", "nivel"],
            as_index=False
        )["matricula"].sum()
    )

    # 2. CARGAR PROYECCIONES

    arima = pd.read_csv(
        MODELOS_DIR /
        "proyecciones_arima_territorial_2026_2035_completas.csv"
    )

    arima = (
        arima.groupby(
            ["anio", "nivel"],
            as_index=False
        )["matricula_predicha"].sum()
    )

    prophet = pd.read_csv(
        MODELOS_DIR /
        "proyecciones_prophet_territorial_2026_2035_completas.csv"
    )

    prophet = (
        prophet.groupby(
            ["anio", "nivel"],
            as_index=False
        )["prophet"].sum()
    )

    rf = pd.read_csv(
        MODELADO_DIR /
        "proyecciones_por_nivel_2026_2035.csv"
    )

    # 3. CONFIGURAR LOS TRES GRAFICOS

    figuras = {
        "INICIAL": (11, "Nivel Inicial"),
        "PRIMARIA": (12, "Nivel Primaria"),
        "SECUNDARIA": (13, "Nivel Secundaria")
    }

    series = [
        (arima, "matricula_predicha", "arima",
         "ARIMA territorial", "-"),
        (prophet, "prophet", "prophet",
         "Prophet territorial", "-"),
        (rf, "prediccion_random_forest", "random_forest",
         "Random Forest", "-"),
        (rf, "prediccion_tendencia", "tendencia",
         "Tendencia reciente", "-."),
        (rf, "prediccion_baseline", "persistencia",
         "Persistencia", "--")
    ]

    # 4. GENERAR UNA FIGURA POR NIVEL

    for nivel, (numero, titulo) in figuras.items():

        hist_nivel = historico[
            historico["nivel"] == nivel
        ].sort_values("anio")

        ultimo_valor = hist_nivel.loc[
            hist_nivel["anio"] == 2025,
            "matricula"
        ].iloc[0]

        fig, ax = plt.subplots(figsize=(13, 6))

        # Matricula historica
        ax.plot(
            hist_nivel["anio"],
            hist_nivel["matricula"] / 1_000_000,
            color="#222222",
            linewidth=3,
            marker="o",
            markersize=4,
            label="Matrícula histórica",
            zorder=5
        )

        # Proyecciones
        for datos, columna, modelo, etiqueta, estilo in series:

            datos_nivel = datos[
                datos["nivel"] == nivel
            ].sort_values("anio")

            anios = [2025] + datos_nivel["anio"].tolist()

            valores = (
                [ultimo_valor] +
                datos_nivel[columna].tolist()
            )

            ax.plot(
                anios,
                [valor / 1_000_000 for valor in valores],
                color=COLORES[modelo],
                linewidth=2.5,
                linestyle=estilo,
                label=etiqueta
            )

        # Separacion entre historia y proyecciones
        ax.axvline(
            2025,
            color="#777777",
            linestyle=":",
            linewidth=1.5
        )

        ax.axvspan(
            2025,
            2035,
            color="#A5A5A5",
            alpha=0.06
        )

        ax.set_title(
            f"Evolución histórica y proyecciones de matrícula - {titulo}",
            fontsize=16,
            fontweight="bold",
            pad=18
        )

        ax.set_xlabel("Año", fontsize=11)
        ax.set_ylabel(
            "Matrícula (millones de estudiantes)",
            fontsize=11
        )

        ax.set_xlim(2012, 2035)
        ax.set_xticks(list(range(2012, 2036, 2)))

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.25
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)

        ax.legend(
            loc="upper center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=3,
            frameon=False,
            fontsize=10
        )

        fig.subplots_adjust(
            left=0.09,
            right=0.98,
            top=0.88,
            bottom=0.25
        )

        # Guardar figura
        nombre_archivo = (
            f"figura_{numero}_proyecciones_{nivel.lower()}"
        )

        guardar_grafico(fig, nombre_archivo)

        plt.show()
        plt.close(fig)

        print(f"\n========== FIGURA {numero}: {nivel} ==========")

        for datos, columna, modelo, etiqueta, estilo in series:

            valor_2035 = datos.loc[
                (datos["nivel"] == nivel) &
                (datos["anio"] == 2035),
                columna
            ].sum()

            print(f"{etiqueta}: {valor_2035:,.0f}")

# FIGURA 14 - VARIACION TERRITORIAL DE LA MATRICULA

def figura_14_variacion_territorial():

    # 1. CARGAR MATRICULA REAL DE 2025

    historico = pd.read_csv(
        BASE_DIR / "dataset_modelado_features.csv"
    )

    historico = historico[
        historico["anio"] == 2025
    ].copy()

    historico = (
        historico.groupby(
            "partido",
            as_index=False
        )["matricula"].sum(min_count=1)
    )

    historico = historico.rename(
        columns={"matricula": "matricula_2025"}
    )

    # 2. CARGAR PROYECCIONES RANDOM FOREST 2035

    proyecciones = pd.read_csv(
        MODELADO_DIR /
        "proyecciones_matricula_2026_2035.csv"
    )

    proyecciones = proyecciones[
        proyecciones["anio"] == 2035
    ].copy()

    proyecciones = (
        proyecciones.groupby(
            "partido",
            as_index=False
        )["prediccion_random_forest"].sum(min_count=1)
    )

    proyecciones = proyecciones.rename(
        columns={
            "prediccion_random_forest": "matricula_2035"
        }
    )

    # 3. UNIR Y CALCULAR VARIACION PORCENTUAL

    df = historico.merge(
        proyecciones,
        on="partido",
        how="inner",
        validate="one_to_one"
    )

    df = df.dropna(
        subset=["matricula_2025", "matricula_2035"]
    )

    # Evitar divisiones por cero
    df = df[df["matricula_2025"] > 0].copy()

    df["variacion_pct"] = (
        (
            df["matricula_2035"] -
            df["matricula_2025"]
        ) / df["matricula_2025"]
    ) * 100

    # 4. RESUMEN TERRITORIAL

    disminuyen = (df["variacion_pct"] < 0).sum()
    aumentan = (df["variacion_pct"] > 0).sum()
    sin_cambio = (df["variacion_pct"] == 0).sum()

    print("\n========== FIGURA 14 ==========")
    print("Partidos analizados:", len(df))
    print("Partidos con disminucion:", disminuyen)
    print("Partidos con aumento:", aumentan)
    print("Partidos sin cambios:", sin_cambio)

    print(
        "Variacion mediana:",
        f"{df['variacion_pct'].median():.2f}%"
    )

    print(
        "Variacion provincial agregada:",
        f"{((df['matricula_2035'].sum() / df['matricula_2025'].sum()) - 1) * 100:.2f}%"
    )

    # 5. CREAR HISTOGRAMA

    fig, ax = plt.subplots(figsize=(13, 6))

    ax.hist(
        df["variacion_pct"],
        bins=20,
        color=COLORES["random_forest"],
        edgecolor="white",
        linewidth=1,
        alpha=0.85
    )

    # Linea de variacion nula
    ax.axvline(
        0,
        color="#333333",
        linestyle="--",
        linewidth=1.7,
        label="Sin variación (0%)"
    )

    # Linea de variacion mediana
    ax.axvline(
        df["variacion_pct"].median(),
        color="#ED7D31",
        linestyle="-",
        linewidth=2,
        label="Mediana de los partidos"
    )

    ax.set_title(
        "Distribución territorial de la variación proyectada "
        "de la matrícula (2025-2035)",
        fontsize=15,
        fontweight="bold",
        pad=18
    )

    ax.set_xlabel(
        "Variación proyectada de matrícula (%)",
        fontsize=11
    )

    ax.set_ylabel(
        "Cantidad de partidos",
        fontsize=11
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)

    ax.legend(
        loc="upper right",
        frameon=False,
        fontsize=10
    )

    fig.text(
        0.5,
        0.025,
        f"Random Forest | 2025-2035 | "
        f"{len(df)} partidos analizados | "
        f"{disminuyen} disminuyen, {aumentan} aumentan",
        ha="center",
        fontsize=10
    )

    fig.subplots_adjust(
        left=0.09,
        right=0.98,
        top=0.87,
        bottom=0.18
    )

    # 6. GUARDAR FIGURA Y RESULTADOS

    guardar_grafico(
        fig,
        "figura_14_variacion_territorial"
    )

    df.sort_values("variacion_pct").to_csv(
        GRAFICOS_DIR / "datos_figura_14_variacion_territorial.csv",
        index=False
    )

    plt.show()
    plt.close(fig)


# FIGURA 15 - COINCIDENCIA ENTRE MODELOS DE PROYECCION

def figura_15_coincidencia_modelos():

    
    # 1. MATRICULA HISTORICA DE 2025
    

    historico = pd.read_csv(
        BASE_DIR / "dataset_modelado_features.csv"
    )

    historico = historico[
        historico["anio"] == 2025
    ].copy()

    historico = (
        historico.groupby("partido", as_index=False)["matricula"]
        .sum(min_count=1)
        .rename(columns={"matricula": "matricula_2025"})
    )

    
    # 2. PROYECCIONES RANDOM FOREST PARA 2035
    

    rf = pd.read_csv(
        MODELADO_DIR /
        "proyecciones_matricula_2026_2035.csv"
    )

    rf = rf[rf["anio"] == 2035].copy()

    rf = (
        rf.groupby("partido", as_index=False)["prediccion_random_forest"]
        .sum(min_count=1)
        .rename(columns={
            "prediccion_random_forest": "random_forest"
        })
    )

    
    # 3. PROYECCIONES ARIMA PARA 2035
    

    arima = pd.read_csv(
        MODELOS_DIR /
        "proyecciones_arima_territorial_2026_2035_completas.csv"
    )

    arima = arima[arima["anio"] == 2035].copy()

    arima = (
        arima.groupby("partido", as_index=False)["matricula_predicha"]
        .sum(min_count=1)
        .rename(columns={"matricula_predicha": "arima"})
    )

    
    # 4. PROYECCIONES PROPHET PARA 2035
    

    prophet = pd.read_csv(
        MODELOS_DIR /
        "proyecciones_prophet_territorial_2026_2035_completas.csv"
    )

    prophet = prophet[prophet["anio"] == 2035].copy()

    prophet = (
        prophet.groupby("partido", as_index=False)["prophet"]
        .sum(min_count=1)
    )

    
    # 5. UNIR RESULTADOS
    

    df = (
        historico
        .merge(rf, on="partido", how="inner", validate="one_to_one")
        .merge(arima, on="partido", how="inner", validate="one_to_one")
        .merge(prophet, on="partido", how="inner", validate="one_to_one")
    )

    df = df.dropna(
        subset=[
            "matricula_2025",
            "random_forest",
            "arima",
            "prophet"
        ]
    )

    df = df[df["matricula_2025"] > 0].copy()

    
    # 6. CALCULAR VARIACIONES PORCENTUALES
    

    modelos_comparados = [
        "random_forest",
        "arima",
        "prophet"
    ]

    for modelo in modelos_comparados:

        df[f"variacion_{modelo}"] = (
            (df[modelo] - df["matricula_2025"])
            / df["matricula_2025"]
        ) * 100

    
    # 7. CLASIFICAR DIRECCION DEL CAMBIO
    

    UMBRAL_ESTABILIDAD = 1.0

    def clasificar_variacion(valor):

        if valor < -UMBRAL_ESTABILIDAD:
            return "Disminucion"

        if valor > UMBRAL_ESTABILIDAD:
            return "Aumento"

        return "Estabilidad"

    for modelo in modelos_comparados:

        df[f"direccion_{modelo}"] = (
            df[f"variacion_{modelo}"]
            .apply(clasificar_variacion)
        )

    def clasificar_coincidencia(fila):

        direcciones = [
            fila[f"direccion_{modelo}"]
            for modelo in modelos_comparados
        ]

        if len(set(direcciones)) == 1:

            if direcciones[0] == "Disminucion":
                return "Coinciden en disminucion"

            if direcciones[0] == "Aumento":
                return "Coinciden en aumento"

            return "Coinciden en estabilidad"

        return "Difieren"

    df["coincidencia"] = df.apply(
        clasificar_coincidencia,
        axis=1
    )

    
    # 8. RESUMIR RESULTADOS
    

    categorias = [
        "Coinciden en disminucion",
        "Coinciden en aumento",
        "Coinciden en estabilidad",
        "Difieren"
    ]

    conteos = (
        df["coincidencia"]
        .value_counts()
        .reindex(categorias, fill_value=0)
    )

    print("\n========== FIGURA 15 ==========")
    print("Partidos analizados:", len(df))
    print("\nCoincidencia entre modelos:")

    for categoria, cantidad in conteos.items():
        print(f"{categoria}: {cantidad}")

    print("\n========== DIRECCION POR MODELO ==========")

    for modelo in modelos_comparados:

        print(f"\n{NOMBRES[modelo]}")

        conteos_modelo = (
            df[f"direccion_{modelo}"]
            .value_counts()
        )

        for categoria in ["Disminucion", "Estabilidad", "Aumento"]:
            print(
                f"{categoria}:",
                conteos_modelo.get(categoria, 0)
            )

    
    # 9. CREAR GRAFICO
    

    fig, ax = plt.subplots(figsize=(13, 6))

    etiquetas = [
        "Coinciden en\n disminución",
        "Coinciden en\n aumento",
        "Coinciden en\n estabilidad",
        "Difieren"
    ]

    colores_barras = [
        "#C9302C",
        "#70AD47",
        "#5B9BD5",
        "#ED7D31"
    ]

    barras = ax.bar(
        etiquetas,
        conteos.values,
        color=colores_barras,
        width=0.65
    )

    for barra, cantidad in zip(barras, conteos.values):

        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.8,
            str(cantidad),
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold"
        )

    ax.set_title(
        "Coincidencia entre modelos de proyección de matrícula",
        fontsize=16,
        fontweight="bold",
        pad=18
    )

    ax.set_ylabel(
        "Cantidad de partidos",
        fontsize=11
    )

    ax.set_ylim(
        0,
        max(conteos.max() * 1.15, 5)
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)

    fig.text(
        0.5,
        0.025,
        f"Random Forest, ARIMA y Prophet | Horizonte 2035 | "
        f"{len(df)} partidos | Estabilidad: ±1%",
        ha="center",
        fontsize=10
    )

    fig.subplots_adjust(
        left=0.09,
        right=0.98,
        top=0.86,
        bottom=0.19
    )

    
    # 10. GUARDAR RESULTADOS
    

    guardar_grafico(
        fig,
        "figura_15_coincidencia_modelos"
    )

    df.sort_values("partido").to_csv(
        GRAFICOS_DIR / "datos_figura_15_coincidencia_modelos.csv",
        index=False
    )

    plt.show()
    plt.close(fig)



# FIGURA 16 - DIRECCION DEL CAMBIO POR MODELO

def figura_16_direccion_por_modelo():

    # 1. CARGAR RESULTADOS DE LA FIGURA 15

    df = pd.read_csv(
        GRAFICOS_DIR / "datos_figura_15_coincidencia_modelos.csv"
    )

    modelos = ["random_forest", "arima", "prophet"]

    categorias = [
        "Disminucion",
        "Estabilidad",
        "Aumento"
    ]

    colores_categorias = {
        "Disminucion": "#C9302C",
        "Estabilidad": "#5B9BD5",
        "Aumento": "#70AD47"
    }

    # 2. CONTAR PARTIDOS POR MODELO

    resultados = []

    for modelo in modelos:

        conteos = (
            df[f"direccion_{modelo}"]
            .value_counts()
            .reindex(categorias, fill_value=0)
        )

        resultados.append({
            "modelo": NOMBRES[modelo],
            "Disminucion": int(conteos["Disminucion"]),
            "Estabilidad": int(conteos["Estabilidad"]),
            "Aumento": int(conteos["Aumento"])
        })

    resumen = pd.DataFrame(resultados)

    print("\n========== FIGURA 16 ==========")
    print(resumen.to_string(index=False))

    # 3. CREAR GRAFICO DE BARRAS APILADAS

    fig, ax = plt.subplots(figsize=(11, 6))

    posiciones = list(range(len(modelos)))
    base = [0] * len(modelos)

    for categoria in categorias:

        valores = resumen[categoria].tolist()

        barras = ax.bar(
            posiciones,
            valores,
            bottom=base,
            color=colores_categorias[categoria],
            width=0.58,
            label=categoria
        )

        # Mostrar cantidad dentro de cada segmento
        for barra, valor, inicio in zip(
            barras, valores, base
        ):

            if valor > 0:

                ax.text(
                    barra.get_x() + barra.get_width() / 2,
                    inicio + valor / 2,
                    str(valor),
                    ha="center",
                    va="center",
                    fontsize=12,
                    fontweight="bold",
                    color="white"
                )

        base = [
            inicio + valor
            for inicio, valor in zip(base, valores)
        ]

    # 4. FORMATO DEL GRAFICO

    ax.set_xticks(posiciones)

    ax.set_xticklabels(
        resumen["modelo"],
        fontsize=12
    )

    ax.set_ylim(0, 145)
    ax.set_yticks(range(0, 136, 15))

    ax.set_ylabel(
        "Cantidad de partidos",
        fontsize=11
    )

    ax.set_title(
        "Dirección del cambio proyectado por modelo",
        fontsize=16,
        fontweight="bold",
        pad=18
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=3,
        frameon=False,
        fontsize=11
    )

    fig.text(
        0.5,
        0.025,
        "Proyección 2025-2035 | 135 partidos | "
        "Estabilidad: variación entre -1% y +1%",
        ha="center",
        fontsize=10
    )

    fig.subplots_adjust(
        left=0.10,
        right=0.97,
        top=0.86,
        bottom=0.23
    )

    # 5. GUARDAR FIGURA Y TABLA

    guardar_grafico(
        fig,
        "figura_16_direccion_por_modelo"
    )

    resumen.to_csv(
        GRAFICOS_DIR / "datos_figura_16_direccion_por_modelo.csv",
        index=False
    )

    plt.show()
    plt.close(fig)



# ============================================================
# GRAFICOS TERRITORIALES: AUMENTOS Y DISMINUCIONES 2025-2035
# Modelos: ARIMA, Prophet y Tendencia historica
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

BASE_DIR = Path("/Users/chiararomano/PycharmProjects/tesis")
MODELOS_DIR = BASE_DIR / "nuevos modelos"
SALIDA_DIR = MODELOS_DIR / "graficos_territoriales"
SALIDA_DIR.mkdir(parents=True, exist_ok=True)

ANIO_BASE = 2025
ANIO_PROYECCION = 2035


def normalizar_texto(valor):
    texto = str(valor).strip().upper()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(
        caracter for caracter in texto
        if not unicodedata.combining(caracter)
    )


def cargar_matricula_2025():
    ruta = BASE_DIR / "dataset_modelado_features.csv"
    df = pd.read_csv(ruta)

    columnas = {"partido", "nivel", "anio", "matricula"}
    faltantes = columnas - set(df.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas en el dataset historico: {faltantes}"
        )

    df = df[df["anio"] == ANIO_BASE].copy()
    df["partido"] = df["partido"].map(normalizar_texto)
    df["matricula"] = pd.to_numeric(
        df["matricula"], errors="coerce"
    )

    if df["matricula"].isna().any():
        raise ValueError("Hay matriculas faltantes en 2025.")

    return (
        df.groupby("partido", as_index=False)["matricula"]
        .sum()
        .rename(columns={"matricula": "matricula_2025"})
    )


def cargar_proyecciones(ruta, columna_prediccion):
    df = pd.read_csv(ruta)

    columnas = {"partido", "nivel", "anio", columna_prediccion}
    faltantes = columnas - set(df.columns)

    if faltantes:
        raise ValueError(
            f"En {ruta.name} faltan columnas: {faltantes}"
        )

    df = df[df["anio"] == ANIO_PROYECCION].copy()
    df["partido"] = df["partido"].map(normalizar_texto)
    df[columna_prediccion] = pd.to_numeric(
        df[columna_prediccion], errors="coerce"
    )

    if df[columna_prediccion].isna().any():
        raise ValueError(
            f"Hay predicciones faltantes en {ruta.name}"
        )

    return (
        df.groupby("partido", as_index=False)[columna_prediccion]
        .sum()
        .rename(columns={
            columna_prediccion: "matricula_2035"
        })
    )


def calcular_variaciones(historico, proyecciones, modelo):
    df = historico.merge(
        proyecciones,
        on="partido",
        how="outer",
        validate="one_to_one",
        indicator=True
    )

    if not (df["_merge"] == "both").all():
        partidos = df.loc[
            df["_merge"] != "both", "partido"
        ].tolist()
        raise ValueError(
            f"{modelo}: partidos sin correspondencia: {partidos}"
        )

    df = df.drop(columns="_merge")

    df["variacion_absoluta"] = (
        df["matricula_2035"] - df["matricula_2025"]
    )

    df["variacion_porcentual"] = (
        df["variacion_absoluta"] / df["matricula_2025"] * 100
    )

    return df


def graficar_variaciones(df, modelo, tipo, nombre_archivo):
    if tipo == "disminuciones":
        datos = (
            df[df["variacion_absoluta"] < 0]
            .nsmallest(10, "variacion_absoluta")
            .sort_values("variacion_absoluta", ascending=True)
        )
        color = "#C62828"
        titulo = "Partidos con mayores disminuciones proyectadas"

    else:
        datos = (
            df[df["variacion_absoluta"] > 0]
            .nlargest(10, "variacion_absoluta")
            .sort_values("variacion_absoluta", ascending=True)
        )
        color = "#2E7D32"
        titulo = "Partidos con mayores aumentos proyectados"

    if datos.empty:
        print(f"{modelo}: no hay {tipo} proyectados.")
        return

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.barh(
        datos["partido"],
        datos["variacion_absoluta"],
        color=color
    )

    ax.set_title(
        f"{titulo}\n{modelo}, 2025-2035",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Variacion absoluta de matricula")
    ax.set_ylabel("Partido")
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)

    plt.tight_layout()

    ruta_salida = SALIDA_DIR / nombre_archivo
    plt.savefig(ruta_salida, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Grafico guardado: {ruta_salida.name}")


def procesar_modelo(modelo, ruta, columna, historico):
    if not ruta.exists():
        print(f"\nArchivo no encontrado para {modelo}: {ruta}")
        return

    print(f"\n========== {modelo.upper()} ==========")

    proyecciones = cargar_proyecciones(ruta, columna)
    df = calcular_variaciones(
        historico, proyecciones, modelo
    )

    print("Partidos analizados:", len(df))
    print(
        "Disminuciones:",
        (df["variacion_absoluta"] < 0).sum()
    )
    print(
        "Aumentos:",
        (df["variacion_absoluta"] > 0).sum()
    )
    print(
        "Sin variacion:",
        (df["variacion_absoluta"] == 0).sum()
    )

    nombre = modelo.lower().replace(" ", "_")

    graficar_variaciones(
        df, modelo, "disminuciones",
        f"{nombre}_mayores_disminuciones.png"
    )

    graficar_variaciones(
        df, modelo, "aumentos",
        f"{nombre}_mayores_aumentos.png"
    )

    df.to_csv(
        SALIDA_DIR / f"{nombre}_variaciones_2025_2035.csv",
        index=False
    )


# ============================================================
# EJECUCION
# ============================================================

historico_2025 = cargar_matricula_2025()

procesar_modelo(
    "ARIMA",
    MODELOS_DIR /
    "proyecciones_arima_territorial_2026_2035_completas.csv",
    "matricula_predicha",
    historico_2025
)

procesar_modelo(
    "Prophet",
    MODELOS_DIR /
    "proyecciones_prophet_territorial_2026_2035_completas.csv",
    "prophet",
    historico_2025
)

# Tendencia historica:
# Completar con el CSV definitivo de proyecciones 2026-2035.
# No utilizar un archivo que contenga solo predicciones de prueba.

RUTA_TENDENCIA = (
    BASE_DIR / "modelado" /
    "proyecciones_matricula_2026_2035.csv"
)

procesar_modelo(
    "Tendencia historica",
    RUTA_TENDENCIA,
    "prediccion_tendencia",
    historico_2025
)

if RUTA_TENDENCIA.exists():
    df_tendencia = pd.read_csv(RUTA_TENDENCIA, nrows=0)
    posibles_columnas = [
        "matricula_predicha",
        "prediccion_tendencia",
        "tendencia",
        "prediccion"
    ]
    columna_tendencia = next(
        (c for c in posibles_columnas if c in df_tendencia.columns),
        None
    )

    if columna_tendencia is None:
        print(
            "\nTendencia historica: revisar el nombre "
            "de la columna de predicciones."
        )
    else:
        procesar_modelo(
            "Tendencia historica",
            RUTA_TENDENCIA,
            columna_tendencia,
            historico_2025
        )
else:
    print(
        "\nTendencia historica: falta identificar "
        "el CSV definitivo de proyecciones."
    )

print("\nProceso de graficos territoriales finalizado.")


import pandas as pd
from pathlib import Path

base = Path("/Users/chiararomano/PycharmProjects/tesis/modelado")

archivos = [
    "predicciones_tendencia_historica.csv",
    "proyecciones_matricula_2026_2035.csv",
    "proyecciones_por_nivel_2026_2035.csv",
    "proyecciones_provinciales_2026_2035.csv"
]

for nombre in archivos:
    ruta = base / nombre

    print(f"\n========== {nombre} ==========")

    if ruta.exists():
        df = pd.read_csv(ruta)

        print("Dimensiones:", df.shape)
        print("Columnas:", df.columns.tolist())
        print("\nPrimeras filas:")
        print(df.head(3).to_string(index=False))
    else:
        print("Archivo no encontrado")


# EJECUCION DE TODOS LOS GRAFICOS

def main():

    print("\n========== GRAFICOS FINALES DE LA TESIS ==========")

    # figura_8_comparacion_mae()
    # figura_9_comparacion_horizontes()
    # figura_10_evolucion_proyecciones()
    # graficos_proyecciones_por_nivel()
    # figura_14_variacion_territorial()
    # figura_15_coincidencia_modelos()
    # figura_16_direccion_por_modelo()

    print("\nTodos los graficos disponibles fueron generados.")


if __name__ == "__main__":
    main()
