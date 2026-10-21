import os
import pandas as pd

# LIMPIEZA DE FECUNDIDAD
# FEC_01 - HIJOS NACIDOS VIVOS Y PROMEDIO POR MUJER

# 1. RUTAS
carpeta_fecundidad = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "necesarios /fecundidad"
)

carpeta_salida = (
    "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
    "datos_limpios"
)

#
# # 2. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO FEC_01
#
# archivo_fec_01 = None
#
# for archivo in os.listdir(carpeta_fecundidad):
#
#     if (
#         archivo.startswith("1.2")
#         and archivo.lower().endswith(".xlsx")
#     ):
#         archivo_fec_01 = os.path.join(
#             carpeta_fecundidad,
#             archivo
#         )
#         break
#
#
# if archivo_fec_01 is None:
#     raise FileNotFoundError(
#         "No se encontró el archivo FEC_01"
#     )
#
#
# print("\nARCHIVO FEC_01:")
# print(archivo_fec_01)
#
# # 3. IDENTIFICAR Y LEER LA HOJA PRINCIPAL
#
# excel_fec_01 = pd.ExcelFile(
#     archivo_fec_01
# )
#
# hoja_fec_01 = None
#
# for hoja in excel_fec_01.sheet_names:
#
#     nombre_normalizado = (
#         hoja
#         .replace("\xa0", " ")
#         .strip()
#     )
#
#     if nombre_normalizado == "Cuadro 1.2":
#
#         hoja_fec_01 = hoja
#         break
#
#
# if hoja_fec_01 is None:
#
#     raise ValueError(
#         "No se encontró la hoja Cuadro 1.2"
#     )
#
#
# print("\nHOJA FEC_01 ENCONTRADA:")
# print(repr(hoja_fec_01))
#
#
# df = pd.read_excel(
#     archivo_fec_01,
#     sheet_name=hoja_fec_01,
#     header=None
# )
#
#
# # 4. QUEDARNOS SOLO CON LAS FILAS DE PARTIDOS
# #
# # Los códigos de partido de Buenos Aires tienen 5 dígitos
# # y comienzan con 06.
# # De esta forma eliminamos:
# # - Total provincial
# # - 24 Partidos del Gran Buenos Aires
# # - Resto de partidos
# # - encabezados
# # - notas
# # - fuente
#
# codigo = (
#     df[0]
#     .astype(str)
#     .str.extract(r"(06\d{3})", expand=False)
# )
#
# df = df[
#     codigo.notna()
# ].copy()
#
# df["codigo_partido"] = codigo[
#     codigo.notna()
# ].values
#
#
# # 5. SEPARAR EL NOMBRE DEL PARTIDO DEL CÓDIGO
#
# df["partido"] = (
#     df[0]
#     .astype(str)
#     .str.replace(
#         r"06\d{3}",
#         "",
#         regex=True
#     )
#     .str.replace(
#         "\xa0",
#         " ",
#         regex=False
#     )
#     .str.strip()
#     .str.upper()
# )
#
#
# # 6. CONSTRUIR EL DATASET FEC_01
#
# fec_01 = pd.DataFrame({
#
#     "codigo_partido":
#         df["codigo_partido"],
#
#     "partido":
#         df["partido"],
#
#     "mujeres_14_49":
#         df[1],
#
#     "sin_hijos":
#         df[2],
#
#     "con_1_hijo":
#         df[3],
#
#     "con_2_hijos":
#         df[4],
#
#     "con_3_hijos":
#         df[5],
#
#     "con_4_hijos":
#         df[6],
#
#     "con_5_mas_hijos":
#         df[7],
#
#     "promedio_hijos_por_mujer":
#         df[8]
# })
#
#
# # 7. CONVERTIR COLUMNAS NUMÉRICAS
#
# columnas_enteras = [
#     "mujeres_14_49",
#     "sin_hijos",
#     "con_1_hijo",
#     "con_2_hijos",
#     "con_3_hijos",
#     "con_4_hijos",
#     "con_5_mas_hijos"
# ]
#
#
# for columna in columnas_enteras:
#
#     fec_01[columna] = pd.to_numeric(
#         fec_01[columna],
#         errors="coerce"
#     ).astype("Int64")
#
#
# fec_01["promedio_hijos_por_mujer"] = (
#     pd.to_numeric(
#         fec_01["promedio_hijos_por_mujer"],
#         errors="coerce"
#     )
# )
#
#
# # 8. CONTROL INTERNO
#
# fec_01["suma_categorias_hijos"] = (
#     fec_01["sin_hijos"]
#     + fec_01["con_1_hijo"]
#     + fec_01["con_2_hijos"]
#     + fec_01["con_3_hijos"]
#     + fec_01["con_4_hijos"]
#     + fec_01["con_5_mas_hijos"]
# )
#
#
# fec_01["diferencia_control"] = (
#     fec_01["mujeres_14_49"]
#     - fec_01["suma_categorias_hijos"]
# )
#
#
# # 9. VALIDACIONES
#
#
# print("VALIDACIÓN FEC_01")
#
#
#
# print("\nDIMENSIONES:")
# print(fec_01.shape)
#
#
# print("\nCANTIDAD DE PARTIDOS:")
# print(
#     fec_01["partido"].nunique()
# )
#
#
# print("\nCANTIDAD DE CÓDIGOS:")
# print(
#     fec_01["codigo_partido"].nunique()
# )
#
#
# print("\nPARTIDOS DUPLICADOS:")
# print(
#     fec_01["partido"].duplicated().sum()
# )
#
#
# print("\nCÓDIGOS DUPLICADOS:")
# print(
#     fec_01["codigo_partido"].duplicated().sum()
# )
#
#
# print("\nVALORES NULOS:")
# print(
#     fec_01.isna().sum()
# )
#
#
# print("\nCONTROLES CON DIFERENCIA:")
# errores_control = fec_01[
#     fec_01["diferencia_control"] != 0
# ]
#
# if errores_control.empty:
#     print(
#         "Todos los registros son consistentes."
#     )
# else:
#     print(
#         errores_control.to_string(index=False)
#     )
#
#
# # 10. CONTROL ESPECÍFICO DE GENERAL PUEYRREDÓN
#
# print("\nGENERAL PUEYRREDÓN:")
#
# print(
#     fec_01[
#         fec_01["codigo_partido"] == "06357"
#     ].to_string(index=False)
# )
#
#
# # 11. GUARDAR DATASET LIMPIO
#
# os.makedirs(
#     carpeta_salida,
#     exist_ok=True
# )
#
#
# archivo_salida = os.path.join(
#     carpeta_salida,
#     "fecundidad_fec01_limpio.csv"
# )
#
#
# fec_01.to_csv(
#     archivo_salida,
#     index=False,
#     encoding="utf-8-sig"
# )
#
#
# # 12. VERIFICAR EL ARCHIVO EXPORTADO
#
# fec_01_verificacion = pd.read_csv(
#     archivo_salida,
#     dtype={
#         "codigo_partido": str
#     }
# )
#
#
# print("ARCHIVO FEC_01 GUARDADO")
#
#
# print("\nRUTA:")
# print(archivo_salida)
#
#
# print("\nDIMENSIONES DEL ARCHIVO EXPORTADO:")
# print(
#     fec_01_verificacion.shape
# )
#
#
# print("\nCANTIDAD DE PARTIDOS:")
# print(
#     fec_01_verificacion[
#         "partido"
#     ].nunique()
# )
#
#
# print("\nCANTIDAD DE CÓDIGOS:")
# print(
#     fec_01_verificacion[
#         "codigo_partido"
#     ].nunique()
# )
#
#
# print("\nDUPLICADOS:")
# print(
#     fec_01_verificacion[
#         "codigo_partido"
#     ].duplicated().sum()
# )
#
#
# print("\nLIMPIEZA FEC_01 FINALIZADA CORRECTAMENTE")
#
#
# # LIMPIEZA DE FECUNDIDAD
# # FEC_02 - HIJOS NACIDOS VIVOS POR GRUPOS DE EDAD
# print('--------------------------------------------------------------')
# print('LIMPIEZA DE FECUNDIDAD')
# print('FEC_02 - HIJOS NACIDOS VIVOS POR GRUPOS DE EDAD')
#
# # 1. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO FEC_02
#
# archivo_fec_02 = None
#
# for archivo in os.listdir(carpeta_fecundidad):
#
#     if (
#         archivo.startswith("2.2")
#         and archivo.lower().endswith(".xlsx")
#     ):
#         archivo_fec_02 = os.path.join(
#             carpeta_fecundidad,
#             archivo
#         )
#         break
#
#
# if archivo_fec_02 is None:
#     raise FileNotFoundError(
#         "No se encontró el archivo FEC_02"
#     )
#
#
# print("\nARCHIVO FEC_02:")
# print(archivo_fec_02)
#
#
# # 2. LEER LAS HOJAS DEL EXCEL
#
# excel_fec_02 = pd.ExcelFile(
#     archivo_fec_02
# )
#
#
# # Identificamos únicamente las hojas correspondientes
# # a partidos.
# # La hoja "Cuadro 2.2" provincial queda afuera.
#
# hojas_partidos = []
#
# for hoja in excel_fec_02.sheet_names:
#
#     nombre_normalizado = (
#         hoja
#         .replace("\xa0", " ")
#         .strip()
#     )
#
#     if nombre_normalizado.startswith("Cuadro 2.2."):
#
#         numero = nombre_normalizado.replace(
#             "Cuadro 2.2.",
#             ""
#         )
#
#         if numero.isdigit():
#             hojas_partidos.append(hoja)
#
#
# print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
# print(len(hojas_partidos))
#
#
# # 3. EXTRAER LOS DATOS DE CADA PARTIDO
#
# registros = []
#
# grupos_edad_validos = [
#     "14",
#     "15-19",
#     "20-24",
#     "25-29",
#     "30-34",
#     "35-39",
#     "40-44",
#     "45-49"
# ]
#
#
# for hoja in hojas_partidos:
#
#     df = pd.read_excel(
#         archivo_fec_02,
#         sheet_name=hoja,
#         header=None
#     )
#
#         # OBTENER NOMBRE DEL PARTIDO DESDE EL TÍTULO
#
#     titulo = None
#
#     for i in range(min(6, len(df))):
#
#         texto = str(df.iloc[i, 0])
#
#         # Normalizar espacios especiales del Excel
#
#         texto = texto.replace("\xa0", " ")
#
#         # Unificar espacios repetidos
#
#         texto = " ".join(texto.split())
#
#         if "partido " in texto.lower():
#             titulo = texto
#
#             break
#
#     if titulo is None:
#         print("\nERROR EN LA HOJA:")
#
#         print(repr(hoja))
#
#         print("\nPRIMERAS 6 FILAS DE LA COLUMNA 0:")
#
#         print(df.iloc[:6, 0].to_string())
#
#         raise ValueError(
#
#             f"No se pudo identificar el partido en {hoja}"
#
#         )
#
#     # Extraer todo lo que aparece después de "partido "
#
#     posicion_partido = titulo.lower().find(
#
#         "partido "
#
#     )
#
#     partido = titulo[
#
#               posicion_partido + len("partido "):
#
#               ]
#
#     # El nombre termina antes del siguiente punto
#
#     partido = partido.split(".")[0]
#
#     partido = partido.strip().upper()
#
#
#         # EXTRAER LOS GRUPOS DE EDAD
#
#     for _, fila in df.iterrows():
#
#         grupo_edad = str(fila.iloc[0]).strip()
#
#         if grupo_edad not in grupos_edad_validos:
#             continue
#
#         registros.append({
#
#             "partido":
#                 partido,
#
#             "grupo_edad":
#                 grupo_edad,
#
#             "mujeres":
#                 fila.iloc[1],
#
#             "sin_hijos":
#                 fila.iloc[2],
#
#             "con_1_hijo":
#                 fila.iloc[3],
#
#             "con_2_hijos":
#                 fila.iloc[4],
#
#             "con_3_hijos":
#                 fila.iloc[5],
#
#             "con_4_hijos":
#                 fila.iloc[6],
#
#             "con_5_mas_hijos":
#                 fila.iloc[7],
#
#             "promedio_hijos_por_mujer":
#                 fila.iloc[8]
#         })
#
#
# # 4. CREAR DATAFRAME
#
# fec_02 = pd.DataFrame(
#     registros
# )
#
#
#
# # TODAVÍA NO MODIFICAMOS LOS "-"
#
#
# columnas_con_cantidades = [
#     "mujeres",
#     "sin_hijos",
#     "con_1_hijo",
#     "con_2_hijos",
#     "con_3_hijos",
#     "con_4_hijos",
#     "con_5_mas_hijos"
# ]
#
#
# # 5. CONTAR GUIONES ANTES DE CONVERTIR A NÚMEROS
#
# print("\n" + "=" * 70)
# print("VALORES '-' EN FEC_02")
#
#
#
# for columna in columnas_con_cantidades:
#
#     cantidad_guiones = (
#         fec_02[columna]
#         .astype(str)
#         .str.strip()
#         .eq("-")
#         .sum()
#     )
#
#     print(
#         f"{columna}: {cantidad_guiones}"
#     )
#
#
# # 6. VALIDACIONES ESTRUCTURALES
#
# print("\n" + "=" * 70)
# print("VALIDACIÓN ESTRUCTURAL FEC_02")
#
#
# print("\nDIMENSIONES:")
# print(fec_02.shape)
#
#
# print("\nCANTIDAD DE PARTIDOS:")
# print(
#     fec_02["partido"].nunique()
# )
#
#
# print("\nCANTIDAD DE GRUPOS DE EDAD:")
# print(
#     fec_02["grupo_edad"].nunique()
# )
#
#
# print("\nGRUPOS DE EDAD ENCONTRADOS:")
# print(
#     sorted(
#         fec_02["grupo_edad"].unique()
#     )
# )
#
#
# print("\nCANTIDAD DE FILAS POR PARTIDO:")
#
# filas_por_partido = (
#     fec_02
#     .groupby("partido")
#     .size()
# )
#
# print(
#     filas_por_partido.value_counts().sort_index()
# )
#
#
# # 7. BUSCAR DUPLICADOS PARTIDO - GRUPO DE EDAD
#
# duplicados = fec_02.duplicated(
#     subset=[
#         "partido",
#         "grupo_edad"
#     ]
# )
#
#
# print("\nDUPLICADOS PARTIDO-GRUPO_EDAD:")
# print(
#     duplicados.sum()
# )
#
#
# if duplicados.any():
#
#     print("\nREGISTROS DUPLICADOS:")
#
#     print(
#         fec_02[
#             duplicados
#         ].to_string(index=False)
#     )
#
#
# # 8. VERIFICAR SI TODOS LOS PARTIDOS TIENEN
# # LOS 8 GRUPOS DE EDAD
#
# partidos_incompletos = (
#     fec_02
#     .groupby("partido")["grupo_edad"]
#     .nunique()
# )
#
# partidos_incompletos = partidos_incompletos[
#     partidos_incompletos != 8
# ]
#
#
# print("\nPARTIDOS SIN 8 GRUPOS DE EDAD:")
#
# if partidos_incompletos.empty:
#
#     print(
#         "Todos los partidos tienen los 8 grupos de edad."
#     )
#
# else:
#
#     print(
#         partidos_incompletos
#     )
#
#
# # 9. MOSTRAR ALGUNOS REGISTROS PARA CONTROL
#
# print("\nPRIMERAS 16 FILAS:")
#
# print(
#     fec_02
#     .head(16)
#     .to_string(index=False)
# )
#
#
# # 10. CONTROL DE GENERAL PUEYRREDÓN
#
# print("\nGENERAL PUEYRREDÓN:")
#
# control_pueyrredon = fec_02[
#     fec_02["partido"]
#     .str.contains(
#         "PUEYRRED",
#         case=False,
#         na=False
#     )
# ]
#
# print(
#     control_pueyrredon.to_string(
#         index=False
#     )
# )
#
#
# # LIMPIEZA DEFINITIVA FEC_02
#
#
# print("\n" + "=" * 70)
# print("LIMPIEZA DEFINITIVA FEC_02")
#
#
#
#
# # 1. REEMPLAZAR "-" POR 0
#
#
# columnas_categorias = [
#     "sin_hijos",
#     "con_1_hijo",
#     "con_2_hijos",
#     "con_3_hijos",
#     "con_4_hijos",
#     "con_5_mas_hijos"
# ]
#
#
# for columna in columnas_categorias:
#
#     fec_02[columna] = (
#         fec_02[columna]
#         .replace("-", 0)
#     )
#
#     fec_02[columna] = pd.to_numeric(
#         fec_02[columna],
#         errors="raise"
#     ).astype(int)
#
#
#
# # 2. ASEGURAR TIPOS NUMÉRICOS
#
#
# fec_02["mujeres"] = pd.to_numeric(
#     fec_02["mujeres"],
#     errors="raise"
# ).astype(int)
#
#
# fec_02["promedio_hijos_por_mujer"] = pd.to_numeric(
#     fec_02["promedio_hijos_por_mujer"],
#     errors="raise"
# )
#
#
#
# # 3. CREAR CONTROL DE CONSISTENCIA
#
#
# fec_02["suma_categorias_hijos"] = (
#     fec_02["sin_hijos"]
#     + fec_02["con_1_hijo"]
#     + fec_02["con_2_hijos"]
#     + fec_02["con_3_hijos"]
#     + fec_02["con_4_hijos"]
#     + fec_02["con_5_mas_hijos"]
# )
#
#
# fec_02["diferencia_control"] = (
#     fec_02["mujeres"]
#     - fec_02["suma_categorias_hijos"]
# )
#
#
#
# # 4. VALIDACIÓN FINAL
#
#
# print("\nDIMENSIONES:")
# print(fec_02.shape)
#
#
# print("\nVALORES NULOS:")
# print(
#     fec_02.isnull().sum()
# )
#
#
# print("\nTIPOS DE DATOS:")
# print(
#     fec_02.dtypes
# )
#
#
# print("\nVALORES '-' QUE QUEDARON:")
#
# for columna in columnas_categorias:
#
#     cantidad = (
#         fec_02[columna]
#         .astype(str)
#         .eq("-")
#         .sum()
#     )
#
#     print(
#         f"{columna}: {cantidad}"
#     )
#
#
#
# # 5. CONTROL MUJERES = SUMA DE CATEGORÍAS
#
#
# errores_control = fec_02[
#     fec_02["diferencia_control"] != 0
# ]
#
#
# print(
#     "\nREGISTROS DONDE LA SUMA DE CATEGORÍAS "
#     "NO COINCIDE CON MUJERES:"
# )
#
# if errores_control.empty:
#
#     print(
#         "Todos los registros son consistentes."
#     )
#
# else:
#
#     print(
#         errores_control.to_string(index=False)
#     )
#
#
#
# # 6. CONTROL DE GENERAL PUEYRREDÓN
#
#
# print("\nGENERAL PUEYRREDÓN:")
#
# print(
#     fec_02[
#         fec_02["partido"]
#         .str.contains(
#             "PUEYRRED",
#             case=False,
#             na=False
#         )
#     ].to_string(index=False)
# )
#
#
#
# # 7. MOSTRAR PRIMERAS FILAS
#
#
# print("\nPRIMERAS 16 FILAS FEC_02:")
#
# print(
#     fec_02
#     .head(16)
#     .to_string(index=False)
# )
#
#
# print("\n" + "=" * 70)
# print("VALIDACIÓN FINAL FEC_02 TERMINADA")
# print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
# print("=" * 70)
#
# # GUARDAR FEC_02
#
# carpeta_datos_limpios = (
#
#     "/Users/chiararomano/Desktop/Tesis ☠️/datos tesis/"
#
#     "datos_limpios"
#
# )
#
# ruta_salida_fec_02 = os.path.join(
#
#     carpeta_datos_limpios,
#
#     "fecundidad_fec02_limpio.csv"
#
# )
#
# fec_02.to_csv(
#
#     ruta_salida_fec_02,
#
#     index=False,
#
#     encoding="utf-8-sig"
#
# )
#
# print("\n" + "=" * 70)
#
# print("ARCHIVO FEC_02 GUARDADO")
#
# print("=" * 70)
#
# print("\nRUTA:")
#
# print(ruta_salida_fec_02)
#
# print("\nDIMENSIONES DEL ARCHIVO EXPORTADO:")
#
# print(fec_02.shape)
#
# print("\nCANTIDAD DE PARTIDOS:")
#
# print(fec_02["partido"].nunique())
#
# print("\nCANTIDAD DE GRUPOS DE EDAD:")
#
# print(fec_02["grupo_edad"].nunique())
#
# print("\nLIMPIEZA FEC_02 FINALIZADA CORRECTAMENTE")

#
# # LIMPIEZA DE FECUNDIDAD
# # FEC_03 - HIJOS NACIDOS VIVOS EN EL ÚLTIMO AÑO
# # POR EDAD Y PARTIDO
#
#
# print("--------------------------------------------------------------")
# print("LIMPIEZA DE FECUNDIDAD")
# print("FEC_03 - HIJOS NACIDOS VIVOS EN EL ÚLTIMO AÑO POR EDAD")
#
#
#
# # 1. BUSCAR AUTOMÁTICAMENTE EL ARCHIVO FEC_03
#
#
# archivo_fec_03 = None
#
# for archivo in os.listdir(carpeta_fecundidad):
#
#     if (
#         archivo.startswith("17.2")
#         and archivo.lower().endswith(".xlsx")
#     ):
#         archivo_fec_03 = os.path.join(
#             carpeta_fecundidad,
#             archivo
#         )
#         break
#
#
# if archivo_fec_03 is None:
#     raise FileNotFoundError(
#         "No se encontró el archivo FEC_03"
#     )
#
#
# print("\nARCHIVO FEC_03:")
# print(archivo_fec_03)
#
#
#
# # 2. LEER LAS HOJAS DEL EXCEL
#
#
# excel_fec_03 = pd.ExcelFile(
#     archivo_fec_03
# )
#
#
# # Queremos solamente las hojas correspondientes a partidos.
# # La hoja "Cuadro 17.2" contiene el total provincial,
# # por lo tanto queda afuera.
#
# hojas_partidos = []
#
# for hoja in excel_fec_03.sheet_names:
#
#     nombre_normalizado = (
#         hoja
#         .replace("\xa0", " ")
#         .strip()
#     )
#
#     if nombre_normalizado.startswith("Cuadro 17.2."):
#
#         numero = nombre_normalizado.replace(
#             "Cuadro 17.2.",
#             ""
#         )
#
#         if numero.isdigit():
#             hojas_partidos.append(hoja)
#
#
# print("\nCANTIDAD DE HOJAS DE PARTIDOS:")
# print(len(hojas_partidos))
#
#
#
# # 3. DEFINIR LOS GRUPOS DE EDAD VÁLIDOS
#
#
# grupos_edad_validos = [
#     "14",
#     "15-19",
#     "20-24",
#     "25-29",
#     "30-34",
#     "35-39",
#     "40-44",
#     "45-49"
# ]
#
#
#
# # 4. EXTRAER LOS DATOS DE CADA PARTIDO
#
#
# registros = []
#
#
# for hoja in hojas_partidos:
#
#     df = pd.read_excel(
#         archivo_fec_03,
#         sheet_name=hoja,
#         header=None
#     )
#
#
#     # --------------------------------------------------------
#     # OBTENER EL NOMBRE DEL PARTIDO DESDE EL TÍTULO
#     # --------------------------------------------------------
#
#     titulo = None
#
#     for i in range(min(6, len(df))):
#
#         texto = str(
#             df.iloc[i, 0]
#         )
#
#         # Eliminar espacios especiales provenientes del Excel
#         texto = texto.replace(
#             "\xa0",
#             " "
#         )
#
#         # Unificar espacios repetidos
#         texto = " ".join(
#             texto.split()
#         )
#
#         if "partido " in texto.lower():
#
#             titulo = texto
#             break
#
#
#     if titulo is None:
#
#         print("\nERROR EN LA HOJA:")
#         print(repr(hoja))
#
#         print("\nPRIMERAS 6 FILAS DE LA COLUMNA 0:")
#         print(
#             df.iloc[:6, 0].to_string()
#         )
#
#         raise ValueError(
#             f"No se pudo identificar el partido en {hoja}"
#         )
#
#
#     # --------------------------------------------------------
#     # EXTRAER EL NOMBRE DEL PARTIDO
#     # --------------------------------------------------------
#
#     posicion_partido = titulo.lower().find(
#         "partido "
#     )
#
#     partido = titulo[
#         posicion_partido + len("partido "):
#     ]
#
#     # El nombre del partido termina antes del siguiente punto
#     partido = partido.split(".")[0]
#
#     partido = partido.strip().upper()
#
#
#     # --------------------------------------------------------
#     # EXTRAER LOS 8 GRUPOS DE EDAD
#     # --------------------------------------------------------
#
#     for _, fila in df.iterrows():
#
#         grupo_edad = str(
#             fila.iloc[0]
#         ).strip()
#
#         if grupo_edad not in grupos_edad_validos:
#             continue
#
#
#         registros.append({
#
#             "partido":
#                 partido,
#
#             "grupo_edad":
#                 grupo_edad,
#
#             "mujeres":
#                 fila.iloc[1],
#
#             "con_hijos_ultimo_anio":
#                 fila.iloc[2],
#
#             "sin_hijos_ultimo_anio":
#                 fila.iloc[3]
#         })
#
#
#
# # 5. CREAR EL DATAFRAME
#
#
# fec_03 = pd.DataFrame(
#     registros
# )
#
#
#
# # 6. CONTAR LOS "-" ANTES DE MODIFICARLOS
#
#
# columnas_cantidades = [
#     "mujeres",
#     "con_hijos_ultimo_anio",
#     "sin_hijos_ultimo_anio"
# ]
#
#
# print("\n" + "=" * 70)
# print("VALORES '-' EN FEC_03")
#
#
#
# for columna in columnas_cantidades:
#
#     cantidad_guiones = (
#         fec_03[columna]
#         .astype(str)
#         .str.strip()
#         .eq("-")
#         .sum()
#     )
#
#     print(
#         f"{columna}: {cantidad_guiones}"
#     )
#
#
#
# # 7. REEMPLAZAR "-" POR 0 Y CONVERTIR A ENTEROS
#
#
# for columna in columnas_cantidades:
#
#     fec_03[columna] = (
#         fec_03[columna]
#         .astype(str)
#         .str.strip()
#         .replace("-", "0")
#     )
#
#     fec_03[columna] = pd.to_numeric(
#         fec_03[columna],
#         errors="raise"
#     ).astype(int)
#
#
#
# # 8. CREAR CONTROL DE CONSISTENCIA
#
#
# # Para cada grupo de edad:
# #
# # mujeres =
# # con hijos nacidos vivos en el último año
# # +
# # sin hijos nacidos vivos en el último año
#
# fec_03["suma_con_sin_hijos"] = (
#     fec_03["con_hijos_ultimo_anio"]
#     + fec_03["sin_hijos_ultimo_anio"]
# )
#
#
# fec_03["diferencia_control"] = (
#     fec_03["mujeres"]
#     - fec_03["suma_con_sin_hijos"]
# )
#
#
#
# # 9. VALIDACIÓN ESTRUCTURAL
#
#
# print("\n" + "=" * 70)
# print("VALIDACIÓN ESTRUCTURAL FEC_03")
#
#
#
# print("\nDIMENSIONES:")
# print(
#     fec_03.shape
# )
#
#
# print("\nCANTIDAD DE PARTIDOS:")
# print(
#     fec_03["partido"].nunique()
# )
#
#
# print("\nCANTIDAD DE GRUPOS DE EDAD:")
# print(
#     fec_03["grupo_edad"].nunique()
# )
#
#
# print("\nGRUPOS DE EDAD ENCONTRADOS:")
# print(
#     sorted(
#         fec_03["grupo_edad"].unique()
#     )
# )
#
#
#
# # 10. VERIFICAR CANTIDAD DE FILAS POR PARTIDO
#
#
# filas_por_partido = (
#     fec_03
#     .groupby("partido")
#     .size()
# )
#
#
# print("\nCANTIDAD DE FILAS POR PARTIDO:")
#
# print(
#     filas_por_partido
#     .value_counts()
#     .sort_index()
# )
#
#
#
# # 11. BUSCAR DUPLICADOS PARTIDO - GRUPO DE EDAD
#
#
# duplicados = fec_03.duplicated(
#     subset=[
#         "partido",
#         "grupo_edad"
#     ]
# )
#
#
# print("\nDUPLICADOS PARTIDO-GRUPO_EDAD:")
# print(
#     duplicados.sum()
# )
#
#
# if duplicados.any():
#
#     print("\nREGISTROS DUPLICADOS:")
#
#     print(
#         fec_03[
#             duplicados
#         ].to_string(
#             index=False
#         )
#     )
#
#
#
# # 12. VERIFICAR QUE TODOS LOS PARTIDOS TENGAN 8 GRUPOS
#
#
# partidos_incompletos = (
#     fec_03
#     .groupby("partido")["grupo_edad"]
#     .nunique()
# )
#
#
# partidos_incompletos = partidos_incompletos[
#     partidos_incompletos != 8
# ]
#
#
# print("\nPARTIDOS SIN 8 GRUPOS DE EDAD:")
#
#
# if partidos_incompletos.empty:
#
#     print(
#         "Todos los partidos tienen los 8 grupos de edad."
#     )
#
# else:
#
#     print(
#         partidos_incompletos
#     )
#
#
#
# # 13. CONTROL DE VALORES NULOS
#
#
# print("\nVALORES NULOS:")
#
# print(
#     fec_03.isnull().sum()
# )
#
#
#
# # 14. CONTROL DE TIPOS DE DATOS
#
#
# print("\nTIPOS DE DATOS:")
#
# print(
#     fec_03.dtypes
# )
#
#
#
# # 15. CONTROL DE CONSISTENCIA
#
#
# errores_control = fec_03[
#     fec_03["diferencia_control"] != 0
# ]
#
#
# print(
#     "\nREGISTROS DONDE "
#     "CON HIJOS + SIN HIJOS NO COINCIDE CON MUJERES:"
# )
#
#
# if errores_control.empty:
#
#     print(
#         "Todos los registros son consistentes."
#     )
#
# else:
#
#     print(
#         errores_control.to_string(
#             index=False
#         )
#     )
#
#
#
# # 16. MOSTRAR PRIMERAS 16 FILAS
#
#
# print("\nPRIMERAS 16 FILAS FEC_03:")
#
# print(
#     fec_03
#     .head(16)
#     .to_string(
#         index=False
#     )
# )
#
#
#
# # 17. CONTROL DE GENERAL PUEYRREDÓN
#
#
# print("\nGENERAL PUEYRREDÓN:")
#
# control_pueyrredon = fec_03[
#     fec_03["partido"]
#     .str.contains(
#         "PUEYRRED",
#         case=False,
#         na=False
#     )
# ]
#
#
# print(
#     control_pueyrredon.to_string(
#         index=False
#     )
# )
#
#
#
# # 18. FIN DE LA LIMPIEZA PRELIMINAR
#
#
# print("\n" + "=" * 70)
# print("LIMPIEZA PRELIMINAR FEC_03 FINALIZADA")
# print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
# print("=" * 70)
#
# 
# # GUARDAR FEC_03
# 
#
# ruta_salida_fec_03 = os.path.join(
#     carpeta_salida,
#     "fecundidad_fec03_limpio.csv"
# )
#
# fec_03.to_csv(
#     ruta_salida_fec_03,
#     index=False,
#     encoding="utf-8-sig"
# )
#
#
# print("\n" + "=" * 70)
# print("ARCHIVO FEC_03 GUARDADO")
# print("=" * 70)
#
# print("\nRUTA:")
# print(ruta_salida_fec_03)
#
# print("\nDIMENSIONES DEL ARCHIVO EXPORTADO:")
# print(fec_03.shape)
#
# print("\nCANTIDAD DE PARTIDOS:")
# print(fec_03["partido"].nunique())
#
# print("\nCANTIDAD DE GRUPOS DE EDAD:")
# print(fec_03["grupo_edad"].nunique())
#
# print("\nDUPLICADOS PARTIDO-GRUPO_EDAD:")
# print(
#     fec_03.duplicated(
#         subset=["partido", "grupo_edad"]
#     ).sum()
# )
#
# print("\nLIMPIEZA FEC_03 FINALIZADA CORRECTAMENTE")
#


# VALIDACIÓN CRUZADA DE FECUNDIDAD
# FEC_01 - FEC_02 - FEC_03


print("=" * 70)
print("VALIDACIÓN CRUZADA DE FECUNDIDAD")
print("FEC_01 - FEC_02 - FEC_03")



# 1. CARGAR LOS TRES ARCHIVOS LIMPIOS


ruta_fec_01 = os.path.join(
    carpeta_salida,
    "fecundidad_fec01_limpio.csv"
)

ruta_fec_02 = os.path.join(
    carpeta_salida,
    "fecundidad_fec02_limpio.csv"
)

ruta_fec_03 = os.path.join(
    carpeta_salida,
    "fecundidad_fec03_limpio.csv"
)


fec_01 = pd.read_csv(
    ruta_fec_01,
    dtype={"codigo_partido": str}
)

fec_02 = pd.read_csv(
    ruta_fec_02
)

fec_03 = pd.read_csv(
    ruta_fec_03
)


print("\nARCHIVOS CARGADOS CORRECTAMENTE")


print("\nDIMENSIONES:")

print(
    "FEC_01:",
    fec_01.shape
)

print(
    "FEC_02:",
    fec_02.shape
)

print(
    "FEC_03:",
    fec_03.shape
)



# 2. COMPARAR LOS PARTIDOS DE LOS TRES ARCHIVOS


partidos_fec_01 = set(
    fec_01["partido"]
)

partidos_fec_02 = set(
    fec_02["partido"]
)

partidos_fec_03 = set(
    fec_03["partido"]
)


print("\n" + "=" * 70)
print("COMPARACIÓN DE PARTIDOS")


print("\nPARTIDOS FEC_01:")
print(
    len(partidos_fec_01)
)

print("\nPARTIDOS FEC_02:")
print(
    len(partidos_fec_02)
)

print("\nPARTIDOS FEC_03:")
print(
    len(partidos_fec_03)
)


print("\nPARTIDOS EN FEC_01 PERO NO EN FEC_02:")
print(
    sorted(
        partidos_fec_01
        - partidos_fec_02
    )
)


print("\nPARTIDOS EN FEC_02 PERO NO EN FEC_01:")
print(
    sorted(
        partidos_fec_02
        - partidos_fec_01
    )
)


print("\nPARTIDOS EN FEC_02 PERO NO EN FEC_03:")
print(
    sorted(
        partidos_fec_02
        - partidos_fec_03
    )
)


print("\nPARTIDOS EN FEC_03 PERO NO EN FEC_02:")
print(
    sorted(
        partidos_fec_03
        - partidos_fec_02
    )
)



# 3. COMPARAR MUJERES ENTRE FEC_02 Y FEC_03


# Ambos archivos tienen una fila por:
# partido + grupo de edad.
#
# Por lo tanto, podemos comparar directamente la cantidad
# de mujeres de cada combinación.

comparacion_02_03 = fec_02[
    [
        "partido",
        "grupo_edad",
        "mujeres"
    ]
].merge(

    fec_03[
        [
            "partido",
            "grupo_edad",
            "mujeres"
        ]
    ],

    on=[
        "partido",
        "grupo_edad"
    ],

    how="outer",

    suffixes=(
        "_fec02",
        "_fec03"
    ),

    indicator=True
)


print("\n" + "=" * 70)
print("COMPARACIÓN FEC_02 VS FEC_03")


print("\nRESULTADO DEL MERGE:")

print(
    comparacion_02_03["_merge"]
    .value_counts()
)


# Diferencia entre cantidades de mujeres

comparacion_02_03[
    "diferencia_mujeres"
] = (

    comparacion_02_03[
        "mujeres_fec02"
    ]

    -

    comparacion_02_03[
        "mujeres_fec03"
    ]
)


diferencias_02_03 = comparacion_02_03[

    comparacion_02_03[
        "diferencia_mujeres"
    ] != 0

]


print(
    "\nREGISTROS CON DIFERENCIAS "
    "EN CANTIDAD DE MUJERES:"
)


if diferencias_02_03.empty:

    print(
        "FEC_02 y FEC_03 coinciden "
        "en los 1080 registros."
    )

else:

    print(
        diferencias_02_03.to_string(
            index=False
        )
    )



# 4. SUMAR LOS GRUPOS DE EDAD DE FEC_02


# FEC_01 tiene una fila por partido.
# FEC_02 tiene ocho filas por partido.
#
# Para poder compararlos, primero sumamos las mujeres
# de los 8 grupos de edad de cada partido.

fec_02_por_partido = (

    fec_02

    .groupby(
        "partido",
        as_index=False
    )

    ["mujeres"]

    .sum()

    .rename(
        columns={
            "mujeres":
                "mujeres_fec02"
        }
    )
)



# 5. COMPARAR FEC_01 VS FEC_02


comparacion_01_02 = fec_01[
    [
        "partido",
        "mujeres_14_49"
    ]
].merge(

    fec_02_por_partido,

    on="partido",

    how="outer",

    indicator=True
)


comparacion_01_02[
    "diferencia_mujeres"
] = (

    comparacion_01_02[
        "mujeres_14_49"
    ]

    -

    comparacion_01_02[
        "mujeres_fec02"
    ]
)


print("\n" + "=" * 70)
print("COMPARACIÓN FEC_01 VS FEC_02")


print("\nRESULTADO DEL MERGE:")

print(
    comparacion_01_02["_merge"]
    .value_counts()
)


diferencias_01_02 = comparacion_01_02[

    comparacion_01_02[
        "diferencia_mujeres"
    ] != 0

]


print(
    "\nPARTIDOS DONDE LA SUMA DE LOS "
    "8 GRUPOS NO COINCIDE CON FEC_01:"
)


if diferencias_01_02.empty:

    print(
        "Los 135 partidos coinciden."
    )

else:

    print(
        diferencias_01_02.to_string(
            index=False
        )
    )



# 6. CONTROL ESPECÍFICO DE GENERAL PUEYRREDÓN


print("\n" + "=" * 70)
print("CONTROL GENERAL PUEYRREDÓN")


print("\nFEC_01:")

print(
    fec_01[
        fec_01["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ][
        [
            "partido",
            "mujeres_14_49"
        ]
    ].to_string(
        index=False
    )
)


print("\nFEC_02 - SUMA DE LOS 8 GRUPOS:")

print(
    fec_02_por_partido[
        fec_02_por_partido["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ].to_string(
        index=False
    )
)


print("\nFEC_03 - SUMA DE LOS 8 GRUPOS:")

fec_03_por_partido = (

    fec_03

    .groupby(
        "partido",
        as_index=False
    )

    ["mujeres"]

    .sum()
)


print(
    fec_03_por_partido[
        fec_03_por_partido["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ].to_string(
        index=False
    )
)



# 7. RESULTADO FINAL


print("\n" + "=" * 70)
print("VALIDACIÓN CRUZADA FINALIZADA")
print("NO SE GUARDÓ NINGÚN ARCHIVO NUEVO")
print("=" * 70)

print('--------------------------------------------------------------')
# CORRECCIÓN Y VALIDACIÓN FINAL DE NOMBRES DE PARTIDOS
# FEC_01 - FEC_02 - FEC_03

print("\n" + "=" * 70)
print("CORRECCIÓN DE NOMBRES DE PARTIDOS")
print("=" * 70)



# 1. CARGAR LOS TRES ARCHIVOS LIMPIOS


ruta_fec_01 = os.path.join(
    carpeta_salida,
    "fecundidad_fec01_limpio.csv"
)

ruta_fec_02 = os.path.join(
    carpeta_salida,
    "fecundidad_fec02_limpio.csv"
)

ruta_fec_03 = os.path.join(
    carpeta_salida,
    "fecundidad_fec03_limpio.csv"
)


fec_01 = pd.read_csv(
    ruta_fec_01,
    dtype={"codigo_partido": str}
)

fec_02 = pd.read_csv(ruta_fec_02)
fec_03 = pd.read_csv(ruta_fec_03)


print("\nARCHIVOS CARGADOS CORRECTAMENTE")



# 2. CORREGIR NOMBRES


# En FEC_02 y FEC_03 algunos nombres quedaron cortados
# porque durante la extracción se tomó el primer punto.

correcciones_fec_02_03 = {
    "JOSÉ C": "JOSÉ C. PAZ",
    "LEANDRO N": "LEANDRO N. ALEM"
}


fec_02["partido"] = fec_02["partido"].replace(
    correcciones_fec_02_03
)

fec_03["partido"] = fec_03["partido"].replace(
    correcciones_fec_02_03
)


# En FEC_01 SAN ANDRES aparece sin tilde.
# Unificamos el nombre con FEC_02 y FEC_03.

fec_01["partido"] = fec_01["partido"].replace({
    "SAN ANDRES DE GILES": "SAN ANDRÉS DE GILES"
})



# 3. COMPARAR LOS PARTIDOS NUEVAMENTE


partidos_fec_01 = set(
    fec_01["partido"].unique()
)

partidos_fec_02 = set(
    fec_02["partido"].unique()
)

partidos_fec_03 = set(
    fec_03["partido"].unique()
)


print("\n" + "=" * 70)
print("COMPARACIÓN DESPUÉS DE LAS CORRECCIONES")
print("=" * 70)


print("\nCANTIDAD DE PARTIDOS:")

print(
    "FEC_01:",
    len(partidos_fec_01)
)

print(
    "FEC_02:",
    len(partidos_fec_02)
)

print(
    "FEC_03:",
    len(partidos_fec_03)
)


print("\nFEC_01 PERO NO FEC_02:")
print(
    sorted(
        partidos_fec_01 - partidos_fec_02
    )
)


print("\nFEC_02 PERO NO FEC_01:")
print(
    sorted(
        partidos_fec_02 - partidos_fec_01
    )
)


print("\nFEC_02 PERO NO FEC_03:")
print(
    sorted(
        partidos_fec_02 - partidos_fec_03
    )
)


print("\nFEC_03 PERO NO FEC_02:")
print(
    sorted(
        partidos_fec_03 - partidos_fec_02
    )
)



# 4. COMPROBAR QUE LOS TRES TENGAN EXACTAMENTE
#    LOS MISMOS 135 PARTIDOS


mismos_partidos = (
    partidos_fec_01
    == partidos_fec_02
    == partidos_fec_03
)


print("\n" + "=" * 70)
print("RESULTADO FINAL")
print("=" * 70)


if mismos_partidos:

    print(
        "\nOK - Los tres archivos contienen "
        "exactamente los mismos partidos."
    )

    print(
        "Cantidad:",
        len(partidos_fec_01)
    )

else:

    print(
        "\nERROR - Todavía existen diferencias "
        "entre los nombres de los partidos."
    )



# 5. GUARDAR SOLAMENTE SI TODO COINCIDE


if mismos_partidos:

    fec_01.to_csv(
        ruta_fec_01,
        index=False,
        encoding="utf-8-sig"
    )

    fec_02.to_csv(
        ruta_fec_02,
        index=False,
        encoding="utf-8-sig"
    )

    fec_03.to_csv(
        ruta_fec_03,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nARCHIVOS ACTUALIZADOS CORRECTAMENTE:")

    print(
        "- fecundidad_fec01_limpio.csv"
    )

    print(
        "- fecundidad_fec02_limpio.csv"
    )

    print(
        "- fecundidad_fec03_limpio.csv"
    )

else:

    print(
        "\nNO SE GUARDÓ NINGÚN CAMBIO."
    )

    print(
        "Primero debemos resolver "
        "las diferencias restantes."
    )
# ============================================================
# INTEGRACIÓN FEC_02 + FEC_03
# FECUNDIDAD POR PARTIDO Y GRUPO DE EDAD
# ============================================================

print("\n" + "=" * 70)
print("INTEGRACIÓN FEC_02 + FEC_03")
print("=" * 70)


# ------------------------------------------------------------
# 1. HACER MERGE POR PARTIDO + GRUPO DE EDAD
# ------------------------------------------------------------

fec_edad = fec_02.merge(
    fec_03,
    on=[
        "partido",
        "grupo_edad"
    ],
    how="outer",
    suffixes=(
        "_fec02",
        "_fec03"
    ),
    indicator=True
)


# ------------------------------------------------------------
# 2. VALIDAR EL RESULTADO DEL MERGE
# ------------------------------------------------------------

print("\nRESULTADO DEL MERGE:")

print(
    fec_edad["_merge"].value_counts()
)


print("\nDIMENSIONES DESPUÉS DEL MERGE:")
print(
    fec_edad.shape
)


# ------------------------------------------------------------
# 3. CONTROLAR QUE MUJERES COINCIDA
# ------------------------------------------------------------

diferencias_mujeres = fec_edad[
    fec_edad["mujeres_fec02"]
    != fec_edad["mujeres_fec03"]
]


print("\nREGISTROS CON DIFERENCIAS EN MUJERES:")

if diferencias_mujeres.empty:

    print(
        "FEC_02 y FEC_03 coinciden "
        "en todos los registros."
    )

else:

    print(
        diferencias_mujeres[
            [
                "partido",
                "grupo_edad",
                "mujeres_fec02",
                "mujeres_fec03"
            ]
        ].to_string(
            index=False
        )
    )


# ------------------------------------------------------------
# 4. CREAR UNA ÚNICA COLUMNA MUJERES
# ------------------------------------------------------------

fec_edad["mujeres"] = (
    fec_edad["mujeres_fec02"]
)


# ------------------------------------------------------------
# 5. ELIMINAR COLUMNAS REDUNDANTES
# ------------------------------------------------------------

# Los controles diferencia_control y las sumas fueron útiles
# durante la limpieza, pero no necesitamos duplicarlos
# en la tabla integrada.

columnas_eliminar = [
    "mujeres_fec02",
    "mujeres_fec03",
    "suma_categorias_hijos",
    "diferencia_control_fec02",
    "suma_con_sin_hijos",
    "diferencia_control_fec03",
    "_merge"
]


fec_edad = fec_edad.drop(
    columns=columnas_eliminar
)


# ------------------------------------------------------------
# 6. ORDENAR LAS COLUMNAS
# ------------------------------------------------------------

fec_edad = fec_edad[
    [
        "partido",
        "grupo_edad",
        "mujeres",

        # FEC_02
        "sin_hijos",
        "con_1_hijo",
        "con_2_hijos",
        "con_3_hijos",
        "con_4_hijos",
        "con_5_mas_hijos",
        "promedio_hijos_por_mujer",

        # FEC_03
        "con_hijos_ultimo_anio",
        "sin_hijos_ultimo_anio"
    ]
]


# ------------------------------------------------------------
# 7. VALIDACIÓN DE LA TABLA INTEGRADA
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDACIÓN DE FECUNDIDAD POR EDAD")
print("=" * 70)


print("\nDIMENSIONES:")
print(
    fec_edad.shape
)


print("\nCANTIDAD DE PARTIDOS:")
print(
    fec_edad["partido"].nunique()
)


print("\nCANTIDAD DE GRUPOS DE EDAD:")
print(
    fec_edad["grupo_edad"].nunique()
)


print("\nDUPLICADOS PARTIDO-GRUPO_EDAD:")

print(
    fec_edad.duplicated(
        subset=[
            "partido",
            "grupo_edad"
        ]
    ).sum()
)


print("\nVALORES NULOS:")

print(
    fec_edad.isnull().sum()
)


# ------------------------------------------------------------
# 8. VERIFICAR FILAS POR PARTIDO
# ------------------------------------------------------------

filas_por_partido = (
    fec_edad
    .groupby("partido")
    .size()
)


print("\nCANTIDAD DE FILAS POR PARTIDO:")

print(
    filas_por_partido
    .value_counts()
    .sort_index()
)


# ------------------------------------------------------------
# 9. MOSTRAR GENERAL PUEYRREDÓN
# ------------------------------------------------------------

print("\nGENERAL PUEYRREDÓN:")

print(
    fec_edad[
        fec_edad["partido"]
        .str.contains(
            "PUEYRRED",
            case=False,
            na=False
        )
    ].to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 10. MOSTRAR PRIMERAS FILAS
# ------------------------------------------------------------

print("\nPRIMERAS 16 FILAS:")

print(
    fec_edad
    .head(16)
    .to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("INTEGRACIÓN FEC_02 + FEC_03 FINALIZADA")
print("TODAVÍA NO SE GUARDÓ NINGÚN ARCHIVO")
print("=" * 70)

# ============================================================
# GUARDAR FECUNDIDAD INTEGRADA POR EDAD
# FEC_02 + FEC_03
# ============================================================

ruta_fec_edad = os.path.join(
    carpeta_salida,
    "fecundidad_por_edad_limpio.csv"
)


fec_edad.to_csv(
    ruta_fec_edad,
    index=False,
    encoding="utf-8-sig"
)


print("\n" + "=" * 70)
print("ARCHIVO DE FECUNDIDAD POR EDAD GUARDADO")
print("=" * 70)

print("\nRUTA:")
print(ruta_fec_edad)

print("\nDIMENSIONES:")
print(fec_edad.shape)

print("\nCANTIDAD DE PARTIDOS:")
print(fec_edad["partido"].nunique())

print("\nCANTIDAD DE GRUPOS DE EDAD:")
print(fec_edad["grupo_edad"].nunique())

print("\nDUPLICADOS PARTIDO-GRUPO_EDAD:")
print(
    fec_edad.duplicated(
        subset=["partido", "grupo_edad"]
    ).sum()
)

print("\nVALORES NULOS TOTALES:")
print(
    fec_edad.isnull().sum().sum()
)

print("\nARCHIVO GUARDADO CORRECTAMENTE")