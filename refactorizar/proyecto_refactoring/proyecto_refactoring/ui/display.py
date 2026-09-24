"""Renderizado de datos en terminal. Sin logica de negocio ni estado."""

import time

from models.movie import Movie
from models.series import Series


def clear_screen() -> None:
    """Limpia la pantalla de la consola con una secuencia ANSI."""
    print("\033[2J\033[H", end="")


def print_separator(char: str = "=", length: int = 60) -> None:
    """Imprime un separador en pantalla."""
    print(char * length)


def print_header(text: str) -> None:
    """Imprime un encabezado centrado."""
    print_separator()
    print(text.upper().center(60))
    print_separator()


def delay(seconds: float) -> None:
    """Espera un numero de segundos."""
    time.sleep(seconds)


def mostrar_pelicula(pelicula: Movie | None) -> None:
    """Muestra los datos de una pelicula."""
    print_separator()
    if pelicula is None:
        print("No se encontro la pelicula")
        print_separator()
        return

    campos = {
        "Titulo": pelicula.title,
        "Anio": pelicula.year,
        "Rating IMDB": pelicula.rating,
        "Genero": pelicula.genre,
        "Director": pelicula.director,
        "Actores": pelicula.actors,
        "Trama": pelicula.plot,
        "Pais": pelicula.country,
        "Premios": pelicula.awards,
    }
    for etiqueta, valor in campos.items():
        print(f"{etiqueta}: {valor if valor is not None else 'N/A'}")
    print_separator()


def mostrar_serie(serie: Series) -> None:
    """Muestra los datos de una serie."""
    print_separator()
    campos = {
        "Nombre": serie.name,
        "Idioma": serie.language,
        "Generos": serie.genres,
        "Rating": serie.rating,
        "Estado": serie.status,
        "Estreno": serie.premiered,
        "Final": serie.ended,
        "Episodios": serie.runtime,
    }
    for etiqueta, valor in campos.items():
        print(f"{etiqueta}: {valor if valor is not None else 'N/A'}")

    resumen = str(serie.summary or "N/A")
    print(f"Resumen: {resumen[:200]}...")
    print_separator()


def mostrar_lista_peliculas(peliculas: list[Movie]) -> None:
    """Muestra una lista numerada de peliculas."""
    for i, pelicula in enumerate(peliculas, start=1):
        if pelicula.rating is not None:
            print(
                f"{i}. {pelicula.title} ({pelicula.year or 'N/A'})"
                f" - {pelicula.rating}"
            )
        else:
            print(f"{i}. {pelicula.title} ({pelicula.year or 'N/A'})")
