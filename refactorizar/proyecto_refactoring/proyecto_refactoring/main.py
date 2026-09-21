"""Punto de entrada de la aplicacion de peliculas y series."""

import os
import sys
import time
from typing import Any

from api_movies import (
    HISTORIAL_BUSQUEDAS,
    PELICULAS_FAVORITAS,
    agregar_a_favoritas,
    agregar_al_historial,
    buscar_pelicula,
    buscar_peliculas_por_actor,
    buscar_peliculas_por_genero,
    buscar_series,
    eliminar_de_favoritas,
    exportar_a_json,
    importar_de_json,
    limpiar_historial,
    obtener_detalles_serie,
    obtener_estadisticas,
    obtener_peliculas_populares,
)
from config import CONFIG
from constants import APP_NAME


def clear_screen() -> None:
    """Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")


def print_separator(char: str = "=", length: int = 60) -> None:
    """Imprime un separador en pantalla.

    Args:
        char: Caracter del separador.
        length: Longitud del separador.
    """
    print(char * length)


def print_header(text: str) -> None:
    """Imprime un encabezado centrado.

    Args:
        text: Texto del encabezado.
    """
    print_separator()
    print(text.upper().center(60))
    print_separator()


def delay(seconds: float) -> None:
    """Espera un numero de segundos.

    Args:
        seconds: Segundos a esperar.
    """
    time.sleep(seconds)


def mostrar_pelicula(pelicula: dict[str, Any] | None) -> None:
    """Muestra los datos de una pelicula.

    Args:
        pelicula: Datos de la pelicula o None.
    """
    print_separator()
    if pelicula is None:
        print("No se encontro la pelicula")
        print_separator()
        return

    campos = {
        "Titulo": "Title",
        "Anio": "Year",
        "Rating IMDB": "imdbRating",
        "Genero": "Genre",
        "Director": "Director",
        "Actores": "Actors",
        "Trama": "Plot",
        "Pais": "Country",
        "Premios": "Awards",
    }
    for etiqueta, clave in campos.items():
        print(f"{etiqueta}: {pelicula.get(clave, 'N/A')}")
    print_separator()


def mostrar_serie(serie: dict[str, Any]) -> None:
    """Muestra los datos de una serie.

    Args:
        serie: Datos de la serie.
    """
    print_separator()
    show = serie.get("show", serie)

    campos = {
        "Nombre": show.get("name", "N/A"),
        "Idioma": show.get("language", "N/A"),
        "Generos": show.get("genres", []),
        "Rating": show.get("rating", {}).get("average", "N/A"),
        "Estado": show.get("status", "N/A"),
        "Estreno": show.get("premiered", "N/A"),
        "Final": show.get("ended", "N/A"),
        "Episodios": show.get("runtime", "N/A"),
    }
    for etiqueta, valor in campos.items():
        print(f"{etiqueta}: {valor}")

    resumen = str(show.get("summary", "N/A"))
    print(f"Resumen: {resumen[:200]}...")
    print_separator()


def mostrar_lista_peliculas(peliculas: list[dict[str, Any]]) -> None:
    """Muestra una lista numerada de peliculas.

    Args:
        peliculas: Lista de peliculas a mostrar.
    """
    for i, pelicula in enumerate(peliculas, start=1):
        if "titulo" in pelicula:
            print(
                f"{i}. {pelicula['titulo']} ({pelicula.get('anio', 'N/A')})"
                f" - {pelicula.get('rating', 'N/A')}"
            )
        elif "Title" in pelicula:
            print(f"{i}. {pelicula['Title']} ({pelicula.get('Year', 'N/A')})")
        else:
            print(f"{i}. Pelicula desconocida")


def funcion_buscar_pelicula() -> None:
    """Flujo de busqueda de pelicula por titulo."""
    titulo = input("Ingrese el titulo de la pelicula: ")
    print("Buscando...")
    delay(1)

    pelicula = buscar_pelicula(titulo)
    mostrar_pelicula(pelicula)

    if pelicula is not None:
        agregar_al_historial(pelicula)
        opcion = input("\nAgregar a favoritos? (s/n): ")
        if opcion.lower() == "s":
            if agregar_a_favoritas(pelicula):
                print("Agregada a favoritos!")
            else:
                print("Ya esta en favoritos")

    input("\nPresione Enter para continuar...")


def funcion_buscar_actor() -> None:
    """Flujo de busqueda de peliculas por actor."""
    actor = input("Ingrese el nombre del actor: ")
    print("Buscando peliculas del actor...")

    peliculas = buscar_peliculas_por_actor(actor)

    if len(peliculas) > 0:
        mostrar_lista_peliculas(peliculas)

        opcion = input("\nSeleccione una pelicula para ver detalles (0 para volver): ")
        if opcion.isdigit():
            indice = int(opcion) - 1
            if 0 <= indice < len(peliculas):
                detalles = buscar_pelicula(str(peliculas[indice]["Title"]))
                mostrar_pelicula(detalles)
    else:
        print("No se encontraron peliculas para ese actor")

    input("\nPresione Enter para continuar...")


def funcion_buscar_series() -> None:
    """Flujo de busqueda de series."""
    nombre = input("Ingrese el nombre de la serie: ")
    print("Buscando series...")

    series = buscar_series(nombre)

    if len(series) > 0:
        for i, serie in enumerate(series, start=1):
            show = serie.get("show", {})
            print(f"{i}. {show.get('name', '')} ({show.get('status', '')})")

        opcion = input("\nSeleccione una serie para ver detalles (0 para volver): ")
        if opcion.isdigit():
            indice = int(opcion) - 1
            if 0 <= indice < len(series):
                id_serie = series[indice].get("show", {}).get("id")
                if id_serie is not None:
                    detalles = obtener_detalles_serie(id_serie)
                    mostrar_serie(detalles)
    else:
        print("No se encontraron series")

    input("\nPresione Enter para continuar...")


def funcion_peliculas_populares() -> None:
    """Muestra las peliculas populares."""
    print_header("PELICULAS POPULARES")
    peliculas = obtener_peliculas_populares()
    mostrar_lista_peliculas(peliculas)
    input("\nPresione Enter para continuar...")


def funcion_buscar_por_genero() -> None:
    """Flujo de busqueda de peliculas por genero."""
    print("Generos disponibles: accion, comedia")
    genero = input("Ingrese el genero: ")
    print("Buscando...")

    peliculas = buscar_peliculas_por_genero(genero)
    mostrar_lista_peliculas(peliculas)

    input("\nPresione Enter para continuar...")


def funcion_ver_favoritos() -> None:
    """Muestra las peliculas favoritas."""
    print_header("MIS FAVORITOS")
    if len(PELICULAS_FAVORITAS) > 0:
        for i, pelicula in enumerate(PELICULAS_FAVORITAS, start=1):
            print(f"{i}. {pelicula.get('Title', '')}")

        opcion = input("\nDesea eliminar alguna? (numero o Enter para volver): ")
        if opcion.isdigit():
            indice = int(opcion) - 1
            if 0 <= indice < len(PELICULAS_FAVORITAS):
                titulo = PELICULAS_FAVORITAS[indice].get("Title")
                if titulo is not None and eliminar_de_favoritas(str(titulo)):
                    print("Eliminada de favoritos")
    else:
        print("No tienes peliculas favoritas")

    input("\nPresione Enter para continuar...")


def funcion_ver_historial() -> None:
    """Muestra el historial de busquedas."""
    print_header("HISTORIAL DE BUSQUEDAS")
    if len(HISTORIAL_BUSQUEDAS) > 0:
        for i, entrada in enumerate(HISTORIAL_BUSQUEDAS, start=1):
            print(f"{i}. {entrada['titulo']}")

        opcion = input("\nLimpiar historial? (s/n): ")
        if opcion.lower() == "s":
            limpiar_historial()
            print("Historial limpiado")
    else:
        print("No hay historial")

    input("\nPresione Enter para continuar...")


def funcion_estadisticas() -> None:
    """Muestra las estadisticas de la aplicacion."""
    print_header("ESTADISTICAS")
    stats = obtener_estadisticas()
    print(f"Total favoritas: {stats['total_favoritas']}")
    print(f"Total historial: {stats['total_historial']}")
    input("\nPresione Enter para continuar...")


def funcion_exportar() -> None:
    """Exporta los datos a un archivo JSON."""
    nombre = input("Nombre del archivo (sin extension): ")
    exportar_a_json(f"{nombre}.json")
    input("\nPresione Enter para continuar...")


def funcion_importar() -> None:
    """Importa los datos desde un archivo JSON."""
    nombre = input("Nombre del archivo (sin extension): ")
    try:
        importar_de_json(f"{nombre}.json")
    except OSError:
        print("Error al importar archivo")
    input("\nPresione Enter para continuar...")


def funcion_configuracion() -> None:
    """Permite modificar la configuracion de la aplicacion."""
    print_header("CONFIGURACION")
    print(f"1. Debug: {CONFIG.debug}")
    print(f"2. Verbose: {CONFIG.verbose}")
    print(f"3. Timeout: {CONFIG.timeout}")

    opcion = input("\nSeleccione opcion a cambiar (0 para volver): ")
    if opcion == "1":
        CONFIG.debug = not CONFIG.debug
        print(f"Debug ahora es: {CONFIG.debug}")
    elif opcion == "2":
        CONFIG.verbose = not CONFIG.verbose
        print(f"Verbose ahora es: {CONFIG.verbose}")
    elif opcion == "3":
        try:
            CONFIG.timeout = int(input("Nuevo timeout: "))
        except ValueError:
            print("Timeout invalido")

    input("\nPresione Enter para continuar...")


def menu_principal() -> None:
    """Menu principal de la aplicacion."""
    opciones = {
        "1": funcion_buscar_pelicula,
        "2": funcion_buscar_actor,
        "3": funcion_buscar_series,
        "4": funcion_peliculas_populares,
        "5": funcion_buscar_por_genero,
        "6": funcion_ver_favoritos,
        "7": funcion_ver_historial,
        "8": funcion_estadisticas,
        "9": funcion_exportar,
        "10": funcion_importar,
        "11": funcion_configuracion,
    }

    while True:
        clear_screen()
        print_header(APP_NAME)
        print("1. Buscar pelicula por titulo")
        print("2. Buscar por actor")
        print("3. Buscar series")
        print("4. Ver peliculas populares")
        print("5. Buscar por genero")
        print("6. Ver favoritos")
        print("7. Ver historial")
        print("8. Ver estadisticas")
        print("9. Exportar datos")
        print("10. Importar datos")
        print("11. Configuracion")
        print("12. Salir")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "12":
            print("Hasta luego!")
            break
        if opcion in opciones:
            opciones[opcion]()
        else:
            print("Opcion invalida")
            delay(1)


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)
