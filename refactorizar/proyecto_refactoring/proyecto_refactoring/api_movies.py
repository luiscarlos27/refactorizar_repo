"""Modulo de acceso a APIs de peliculas (OMDB) y series (TVMaze).

Refactorizado: constantes centralizadas, f-strings y type hints.
La separacion en clientes dedicados ocurre en la fase 3.
"""

import json
from typing import Any, cast

import requests
from config import CONFIG
from constants import OMDB_API_KEY, OMDB_BASE_URL, TVMAZE_BASE_URL

PELICULAS_FAVORITAS: list[dict[str, Any]] = []
HISTORIAL_BUSQUEDAS: list[dict[str, str]] = []
CACHE_PELICULAS: dict[str, dict[str, Any]] = {}
CACHE_SERIES: dict[str, list[dict[str, Any]]] = {}


def hacer_request(url: str, params: dict[str, str] | None = None) -> Any:
    """Realiza una peticion GET y devuelve la respuesta como JSON.

    Args:
        url: URL destino.
        params: parametros de consulta opcionales.

    Returns:
        Respuesta JSON (puede ser dict o list segun el endpoint).
    """
    if CONFIG.debug:
        print(f"DEBUG: Haciendo request a {url}")

    response = requests.get(url, params=params, timeout=CONFIG.timeout)

    if CONFIG.verbose:
        print(f"DEBUG: Status code: {response.status_code}")

    return response.json()


def buscar_pelicula(titulo: str) -> dict[str, Any] | None:
    """Busca una pelicula por titulo en OMDB.

    Args:
        titulo: Titulo de la pelicula.

    Returns:
        Datos de la pelicula o None si no se encuentra.
    """
    if titulo in CACHE_PELICULAS:
        if CONFIG.debug:
            print(f"DEBUG: Usando cache para {titulo}")
        return CACHE_PELICULAS[titulo]

    url = f"{OMDB_BASE_URL}?t={titulo}&apikey={OMDB_API_KEY}"
    data = cast(dict[str, Any], hacer_request(url))

    if data.get("Response") == "True":
        CACHE_PELICULAS[titulo] = data
        return data
    return None


def buscar_peliculas_por_actor(actor: str) -> list[dict[str, Any]]:
    """Busca peliculas por actor en OMDB.

    Args:
        actor: Nombre del actor.

    Returns:
        Lista de peliculas encontradas.
    """
    url = f"{OMDB_BASE_URL}?s={actor}&type=movie&apikey={OMDB_API_KEY}"
    data = cast(dict[str, Any], hacer_request(url))

    if data.get("Response") == "True":
        return cast(list[dict[str, Any]], data.get("Search", []))
    return []


def buscar_series(nombre: str) -> list[dict[str, Any]]:
    """Busca series en TVMaze.

    Args:
        nombre: Nombre de la serie.

    Returns:
        Lista de resultados de la busqueda.
    """
    cache_key = f"series_{nombre}"
    if cache_key in CACHE_SERIES:
        return CACHE_SERIES[cache_key]

    url = f"{TVMAZE_BASE_URL}/search/shows?q={nombre}"
    data = cast(list[dict[str, Any]], hacer_request(url))

    CACHE_SERIES[cache_key] = data
    return data


def obtener_detalles_serie(id_serie: int) -> dict[str, Any]:
    """Obtiene los detalles de una serie por id.

    Args:
        id_serie: Identificador de la serie en TVMaze.

    Returns:
        Detalles de la serie.
    """
    url = f"{TVMAZE_BASE_URL}/shows/{id_serie}"
    return cast(dict[str, Any], hacer_request(url))


def obtener_peliculas_populares() -> list[dict[str, Any]]:
    """Retorna una lista local de peliculas populares.

    Returns:
        Lista de peliculas populares.
    """
    return [
        {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
        {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
        {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
        {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
        {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8},
    ]


def buscar_peliculas_por_genero(genero: str) -> list[dict[str, Any]]:
    """Busca peliculas por genero usando listas locales.

    Args:
        genero: Genero solicitado (accion, comedia u otro).

    Returns:
        Lista de peliculas del genero.
    """
    peliculas_accion = [
        {"titulo": "Die Hard", "anio": 1988, "rating": 8.2},
        {"titulo": "Mad Max Fury Road", "anio": 2015, "rating": 8.1},
    ]
    peliculas_comedia = [
        {"titulo": "Superbad", "anio": 2007, "rating": 7.6},
        {"titulo": "The Hangover", "anio": 2009, "rating": 7.7},
    ]

    if genero.lower() == "accion":
        return peliculas_accion
    if genero.lower() == "comedia":
        return peliculas_comedia
    return peliculas_accion + peliculas_comedia


def agregar_a_favoritas(pelicula: dict[str, Any]) -> bool:
    """Agrega una pelicula a favoritas si no existe.

    Args:
        pelicula: Datos de la pelicula.

    Returns:
        True si se agrego, False si ya estaba.
    """
    titulo = pelicula.get("Title")
    for p in PELICULAS_FAVORITAS:
        if p.get("Title") == titulo:
            return False

    PELICULAS_FAVORITAS.append(pelicula)
    return True


def eliminar_de_favoritas(titulo: str) -> bool:
    """Elimina una pelicula de favoritas por titulo.

    Args:
        titulo: Titulo de la pelicula a eliminar.

    Returns:
        True si se elimino, False si no existia.
    """
    for i in range(len(PELICULAS_FAVORITAS)):
        if PELICULAS_FAVORITAS[i].get("Title") == titulo:
            PELICULAS_FAVORITAS.pop(i)
            return True
    return False


def agregar_al_historial(pelicula: dict[str, Any]) -> None:
    """Agrega una busqueda al historial.

    Args:
        pelicula: Datos de la pelicula buscada.
    """
    HISTORIAL_BUSQUEDAS.append({"titulo": pelicula.get("Title", ""), "fecha": "hoy"})


def limpiar_historial() -> None:
    """Limpia el historial de busquedas."""
    HISTORIAL_BUSQUEDAS.clear()


def obtener_estadisticas() -> dict[str, int]:
    """Obtiene estadisticas de favoritas e historial.

    Returns:
        Diccionario con totales.
    """
    return {
        "total_favoritas": len(PELICULAS_FAVORITAS),
        "total_historial": len(HISTORIAL_BUSQUEDAS),
    }


def exportar_a_json(nombre_archivo: str) -> None:
    """Exporta favoritas, historial y estadisticas a JSON.

    Args:
        nombre_archivo: Nombre del archivo de salida.
    """
    data = {
        "favoritas": PELICULAS_FAVORITAS,
        "historial": HISTORIAL_BUSQUEDAS,
        "estadisticas": obtener_estadisticas(),
    }

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print(f"Exportado a {nombre_archivo}")


def importar_de_json(nombre_archivo: str) -> None:
    """Importa favoritas e historial desde un JSON.

    Args:
        nombre_archivo: Nombre del archivo a importar.
    """
    with open(nombre_archivo, encoding="utf-8") as f:
        data = json.load(f)

    PELICULAS_FAVORITAS.clear()
    PELICULAS_FAVORITAS.extend(data.get("favoritas", []))
    HISTORIAL_BUSQUEDAS.clear()
    HISTORIAL_BUSQUEDAS.extend(data.get("historial", []))

    print(f"Importado desde {nombre_archivo}")
