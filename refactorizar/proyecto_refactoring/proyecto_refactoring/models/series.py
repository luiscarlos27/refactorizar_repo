"""Modelo de dominio Series para series de TVMaze."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Series:
    """Serie de TVMaze con campos tipados."""

    id_: int | None
    name: str = ""
    language: str | None = None
    genres: list[str] = field(default_factory=list)
    rating: float | None = None
    status: str | None = None
    premiered: str | None = None
    ended: str | None = None
    runtime: int | None = None
    summary: str | None = None

    @classmethod
    def from_tvmaze(cls, data: dict[str, Any]) -> Series:
        """Construye una Series desde la respuesta de TVMaze.

        Acepta tanto los resultados de busqueda (con clave "show") como los
        detalles directos de un endpoint de serie.
        """
        show = data.get("show")
        if not isinstance(show, dict):
            show = data

        raw_id = show.get("id")
        id_serie = int(raw_id) if raw_id is not None else None

        raw_runtime = show.get("runtime")
        runtime = int(raw_runtime) if raw_runtime is not None else None

        genres_raw = show.get("genres")
        genres = [str(g) for g in genres_raw] if isinstance(genres_raw, list) else []

        return cls(
            id_=id_serie,
            name=str(show.get("name") or ""),
            language=_texto(show.get("language")),
            genres=genres,
            rating=_rating_promedio(show.get("rating")),
            status=_texto(show.get("status")),
            premiered=_texto(show.get("premiered")),
            ended=_texto(show.get("ended")),
            runtime=runtime,
            summary=_texto(show.get("summary")),
        )


def _texto(valor: Any) -> str | None:
    """Convierte un valor en texto o None si esta vacio."""
    if valor is None or valor == "":
        return None
    return str(valor)


def _rating_promedio(valor: Any) -> float | None:
    """Extrae el promedio del objeto rating de TVMaze."""
    if not isinstance(valor, dict):
        return None
    promedio = valor.get("average")
    if promedio is None:
        return None
    try:
        return float(promedio)
    except (TypeError, ValueError):
        return None
