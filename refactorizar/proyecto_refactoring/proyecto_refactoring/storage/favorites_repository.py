"""Repositorio de favoritos, unico dueno del estado y su persistencia."""

from typing import Any

from models.movie import Movie


class FavoritesRepository:
    """Gestiona las peliculas favoritas evitando duplicados por titulo."""

    def __init__(self) -> None:
        self._favoritas: list[Movie] = []

    def listar(self) -> list[Movie]:
        """Devuelve una copia de las favoritas."""
        return list(self._favoritas)

    def agregar(self, movie: Movie) -> bool:
        """Agrega una pelicula si no existe otra con el mismo titulo.

        Returns:
            True si se agrego, False si ya estaba.
        """
        if any(fav.title == movie.title for fav in self._favoritas):
            return False
        self._favoritas.append(movie)
        return True

    def eliminar(self, titulo: str) -> bool:
        """Elimina una favorita por titulo.

        Returns:
            True si se elimino, False si no existia.
        """
        for i in range(len(self._favoritas)):
            if self._favoritas[i].title == titulo:
                self._favoritas.pop(i)
                return True
        return False

    @property
    def cantidad(self) -> int:
        """Numero de favoritas."""
        return len(self._favoritas)

    def to_json_list(self) -> list[dict[str, Any]]:
        """Serializa las favoritas para exportacion JSON."""
        return [fav.to_dict() for fav in self._favoritas]

    def cargar(self, datos: list[dict[str, Any]]) -> None:
        """Reemplaza el estado con datos importados de JSON."""
        self._favoritas = [Movie.from_omdb(d) for d in datos]
