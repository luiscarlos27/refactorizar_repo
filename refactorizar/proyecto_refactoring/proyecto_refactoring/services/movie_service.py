"""Capa de servicios: casos de uso de peliculas con dependencias inyectadas."""

import json
from typing import Any, cast

from api.omdb_client import OmdbClient
from exceptions import ApiClientError, MovieNotFoundError
from logging_config import correlation_scope, get_logger
from models.movie import Movie
from storage.cache import Cache
from storage.favorites_repository import FavoritesRepository
from storage.history_repository import HistoryRepository

logger = get_logger(__name__)

_PELICULAS_POPULARES: list[dict[str, Any]] = [
    {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
    {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
    {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
    {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
    {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8},
]

_PELICULAS_ACCION: list[dict[str, Any]] = [
    {"titulo": "Die Hard", "anio": 1988, "rating": 8.2},
    {"titulo": "Mad Max Fury Road", "anio": 2015, "rating": 8.1},
]

_PELICULAS_COMEDIA: list[dict[str, Any]] = [
    {"titulo": "Superbad", "anio": 2007, "rating": 7.6},
    {"titulo": "The Hangover", "anio": 2009, "rating": 7.7},
]


class MovieService:
    """Casos de uso de peliculas.

    Args:
        omdb_client: Cliente HTTP de OMDB.
        favorites: Repositorio de favoritas.
        history: Repositorio de historial.
        cache: Cache de respuestas de OMDB por titulo.
    """

    def __init__(
        self,
        omdb_client: OmdbClient,
        favorites: FavoritesRepository,
        history: HistoryRepository,
        cache: Cache,
    ) -> None:
        self._omdb_client = omdb_client
        self._favorites = favorites
        self._history = history
        self._cache = cache

    def buscar_por_titulo(self, titulo: str) -> Movie | None:
        """Busca una pelicula por titulo usando cache, con degradacion.

        Returns:
            Movie si hay exito, None si la API no responde.
        Raises:
            MovieNotFoundError: si OMDB responde pero no encuentra la pelicula.
        """
        with correlation_scope("buscar_pelicula"):
            cacheado = self._cache.get(titulo)
            if cacheado is not None:
                logger.debug("Cache acertado para %s", titulo)
                return Movie.from_omdb(cast(dict[str, Any], cacheado))

            try:
                datos = self._omdb_client.buscar_por_titulo(titulo)
            except ApiClientError as exc:
                logger.error("Busqueda de %s fallo por API OMDB: %s", titulo, exc)
                return None

            if datos is None:
                logger.info("Pelicula no encontrada para %s", titulo)
                raise MovieNotFoundError(f"Pelicula no encontrada: {titulo}")
            self._cache.set(titulo, datos)
            return Movie.from_omdb(datos)

    def buscar_por_actor(self, actor: str) -> list[Movie]:
        """Busca peliculas de un actor, con degradacion a lista vacia."""
        with correlation_scope("buscar_actor"):
            try:
                resultados = self._omdb_client.buscar_por_actor(actor)
            except ApiClientError as exc:
                logger.error("Busqueda por actor %s fallo por API OMDB: %s", actor, exc)
                return []
            return [Movie.from_omdb(r) for r in resultados]

    def populares(self) -> list[Movie]:
        """Devuelve el catalogo local de peliculas populares."""
        return [_movie_local(d) for d in _PELICULAS_POPULARES]

    def buscar_por_genero(self, genero: str) -> list[Movie]:
        """Busca peliculas por genero usando catalogos locales."""
        if genero.lower() == "accion":
            return [_movie_local(d) for d in _PELICULAS_ACCION]
        if genero.lower() == "comedia":
            return [_movie_local(d) for d in _PELICULAS_COMEDIA]
        return [_movie_local(d) for d in _PELICULAS_ACCION + _PELICULAS_COMEDIA]

    def agregar_favorita(self, movie: Movie) -> bool:
        """Agrega una pelicula a favoritas."""
        return self._favorites.agregar(movie)

    def eliminar_favorita(self, titulo: str) -> bool:
        """Elimina una pelicula de favoritas por titulo."""
        return self._favorites.eliminar(titulo)

    def listar_favoritas(self) -> list[Movie]:
        """Lista las peliculas favoritas."""
        return self._favorites.listar()

    def registrar_busqueda(self, movie: Movie) -> None:
        """Registra una busqueda en el historial."""
        self._history.registrar(movie.title)

    def limpiar_historial(self) -> None:
        """Limpia el historial de busquedas."""
        self._history.limpiar()

    def listar_historial(self) -> list[dict[str, str]]:
        """Lista las entradas del historial."""
        return self._history.listar()

    def estadisticas(self) -> dict[str, int]:
        """Devuelve totales de favoritas e historial."""
        return {
            "total_favoritas": self._favorites.cantidad,
            "total_historial": self._history.cantidad,
        }

    def exportar_a_json(self, nombre_archivo: str) -> None:
        """Exporta favoritas, historial y estadisticas a JSON."""
        data = {
            "favoritas": self._favorites.to_json_list(),
            "historial": self._history.to_json_list(),
            "estadisticas": self.estadisticas(),
        }
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def importar_a_json(self, nombre_archivo: str) -> None:
        """Importa favoritas e historial desde un archivo JSON."""
        with open(nombre_archivo, encoding="utf-8") as f:
            data = json.load(f)
        self._favorites.cargar(data.get("favoritas", []))
        self._history.cargar(data.get("historial", []))


def _movie_local(datos: dict[str, Any]) -> Movie:
    """Convierte un diccionario del catalogo local en Movie."""
    return Movie(
        title=str(datos.get("titulo") or ""),
        year=str(datos.get("anio") or ""),
        rating=cast(float | None, datos.get("rating")),
    )
