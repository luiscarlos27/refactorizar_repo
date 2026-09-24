"""Capa de servicios: casos de uso de series con dependencias inyectadas."""

from typing import Any, cast

from api.tvmaze_client import TvmazeClient
from exceptions import ApiClientError, SeriesNotFoundError
from logging_config import correlation_scope, get_logger
from models.series import Series
from storage.cache import Cache

logger = get_logger(__name__)


class SeriesService:
    """Casos de uso de series.

    Args:
        tvmaze_client: Cliente HTTP de TVMaze.
        cache: Cache de resultados de busqueda por nombre.
    """

    def __init__(self, tvmaze_client: TvmazeClient, cache: Cache) -> None:
        self._client = tvmaze_client
        self._cache = cache

    def buscar(self, nombre: str) -> list[Series]:
        """Busca series por nombre usando cache, con degradacion.

        Returns:
            Lista de series o [] si la API no responde.
        Raises:
            SeriesNotFoundError: si TVMaze responde sin resultados.
        """
        with correlation_scope("buscar_series"):
            clave = f"series_{nombre}"
            cacheado = self._cache.get(clave)
            if cacheado is not None:
                logger.debug("Cache acertado para %s", nombre)
                return [
                    Series.from_tvmaze(item)
                    for item in cast(list[dict[str, Any]], cacheado)
                ]

            try:
                resultados = self._client.buscar_series(nombre)
            except ApiClientError as exc:
                logger.error("Busqueda de series %s fallo por API TVMaze: %s", nombre, exc)
                return []

            if not resultados:
                logger.info("Sin resultados para serie %s", nombre)
                raise SeriesNotFoundError(f"Serie no encontrada: {nombre}")
            self._cache.set(clave, resultados)
            return [Series.from_tvmaze(item) for item in resultados]

    def obtener_detalles(self, id_serie: int) -> Series | None:
        """Obtiene los detalles de una serie por id, con degradacion.

        Returns:
            Series con detalle o None si la API no responde.
        """
        with correlation_scope("detalle_serie"):
            try:
                detalles = self._client.obtener_detalles(id_serie)
            except ApiClientError as exc:
                logger.error("Detalles de serie %s fallaron por API TVMaze: %s", id_serie, exc)
                return None
            return Series.from_tvmaze(detalles)
