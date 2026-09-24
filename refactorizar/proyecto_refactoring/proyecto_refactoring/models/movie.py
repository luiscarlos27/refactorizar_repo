"""Modelo de dominio Movie para peliculas de OMDB."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Movie:
    """Pelicula de OMDB con campos tipados."""

    title: str
    year: str | None = None
    rating: float | None = None
    genre: str | None = None
    director: str | None = None
    actors: str | None = None
    plot: str | None = None
    country: str | None = None
    awards: str | None = None

    def __post_init__(self) -> None:
        """Valida invariantes basicos del modelo."""
        if self.year is not None and self.year.isdigit():
            anio = int(self.year)
            if not 1888 <= anio <= datetime.now().year + 1:
                raise ValueError(f"Anio invalido: {self.year}")
        if self.rating is not None and not 0.0 <= self.rating <= 10.0:
            raise ValueError(f"Rating invalido: {self.rating}")

    @classmethod
    def from_omdb(cls, data: dict[str, Any]) -> Movie:
        """Construye una Movie desde el diccionario crudo de OMDB.

        Acepta tanto las claves originales de OMDB (Title, Year, imdbRating)
        como las normalizadas (title, year, rating).
        """
        return cls(
            title=str(data.get("Title") or data.get("title") or "Desconocida"),
            year=_texto(data.get("Year") or data.get("year")),
            rating=_flotante(data.get("imdbRating") or data.get("rating")),
            genre=_texto(data.get("Genre") or data.get("genre")),
            director=_texto(data.get("Director") or data.get("director")),
            actors=_texto(data.get("Actors") or data.get("actors")),
            plot=_texto(data.get("Plot") or data.get("plot")),
            country=_texto(data.get("Country") or data.get("country")),
            awards=_texto(data.get("Awards") or data.get("awards")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serializa la Movie como diccionario para persistencia JSON."""
        return {
            "title": self.title,
            "year": self.year,
            "rating": self.rating,
            "genre": self.genre,
            "director": self.director,
            "actors": self.actors,
            "plot": self.plot,
            "country": self.country,
            "awards": self.awards,
        }


def _texto(valor: Any) -> str | None:
    """Convierte un valor en texto o None si esta vacio."""
    if valor is None or valor == "" or valor == "N/A":
        return None
    return str(valor)


def _flotante(valor: Any) -> float | None:
    """Convierte un valor en flotante o None si no es convertible."""
    if valor is None or valor == "" or valor == "N/A":
        return None
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None
