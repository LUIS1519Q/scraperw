import pandas as pd
import requests
import re
from collections import Counter

# ===============================
# PARÁMETROS GENERALES
# ===============================
PAGINA_WIKI = "https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)"
ARCHIVO_EXCEL = "frases_latinas_completas.xlsx"


def obtener_frases():
    """
    Descarga las tablas de frases latinas desde Wikipedia
    y las devuelve en un DataFrame limpio.
    """
    print("Iniciando conexión con Wikipedia...")
    print("La página es grande, por favor espera...")

    try:
        # Cabecera para simular un navegador real
        cabecera = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        respuesta = requests.get(PAGINA_WIKI, headers=cabecera)
        respuesta.raise_for_status()

        # Leer todas las tablas del HTML descargado
        tablas_html = pd.read_html(respuesta.text, header=0)

        print(f"Tablas encontradas: {len(tablas_html)}")

        # Unir todas las tablas en una sola
        datos = pd.concat(tablas_html, ignore_index=True)

        # Verificar que existan las columnas esperadas
        if "Latin" not in datos.columns or "Translation" not in datos.columns:
            print("No se encontraron las columnas necesarias.")
            return None

        return datos[["Latin", "Translation"]].dropna()

    except Exception as error:
        print("Ocurrió un error al obtener los datos:")
        print(error)
        return None


def guardar_y_analizar(dataframe):
    """
    Guarda los datos en Excel y analiza
    las palabras más repetidas.
    """
    if dataframe is None:
        return None

    print(f"Guardando {len(dataframe)} registros en Excel...")
    dataframe.to_excel(ARCHIVO_EXCEL, index=False)

    print("Realizando análisis de palabras...")

    def contar_palabras(columna):
        texto_unido = " ".join(columna.astype(str)).lower()
        palabras_validas = re.findall(r"\b[a-zA-Z]{4,}\b", texto_unido)
        return Counter(palabras_validas).most_common(5)

    palabras_latin = contar_palabras(dataframe["Latin"])
    palabras_ingles = contar_palabras(dataframe["Translation"])

    print("Palabras más comunes en latín:")
    print(palabras_latin)

    print("Palabras más comunes en inglés:")
    print(palabras_ingles)

    # Devolver solo las palabras (sin el conteo)
    return [palabra for palabra, _ in palabras_ingles]


def crear_frases(palabras_clave):
    """
    Genera frases en español usando
    las palabras más frecuentes.
    """
    print("\nFrases generadas:")

    modelos = [
        "El concepto de '{}' ha marcado la historia.",
        "Muchos pensadores hablaron sobre '{}'.",
        "'{}' es una idea fundamental en la filosofía.",
        "La sociedad moderna aún depende de '{}'.",
        "Comprender '{}' nos ayuda a reflexionar."
    ]

    # Asegurar que haya suficientes palabras
    while len(palabras_clave) < 5:
        palabras_clave.append("vida")

    for i in range(5):
        print(f"{i + 1}. {modelos[i].format(palabras_clave[i])}")


# ===============================
# EJECUCIÓN PRINCIPAL
# ===============================
if __name__ == "__main__":
    frases_df = obtener_frases()
    palabras_frecuentes = guardar_y_analizar(frases_df)

    if palabras_frecuentes:
        crear_frases(palabras_frecuentes)
