"""Cliente HTTP dedicado para la API de OMDB, sin logica de negocio."""

from typing import Any, cast

import pybreaker
import requests
from config import AppConfig
from constants import OMDB_API_KEY, OMDB_BASE_URL
from exceptions import ApiClientError, NetworkError
from logging_config import get_logger
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = get_logger(__name__)


class OmdbClient:
    """Encapsula las llamadas REST a OMDB con timeout, retries y breaker.

    Args:
        config: Configuracion inyectada (timeout, retries, throttle).
    """

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._breaker = pybreaker.CircuitBreaker(
            fail_max=config.circuit_fail_max,
            reset_timeout=config.circuit_reset_timeout,
        )
        self._retrier = _crear_retrier(config)

    def buscar_por_titulo(self, titulo: str) -> dict[str, Any] | None:
        """Busca una pelicula por titulo.

        Returns:
            Datos de la pelicula o None si OMDB responde ``Response=False``.
        """
        data = self._get({"t": titulo, "apikey": OMDB_API_KEY})
        if data.get("Response") == "True":
            return data
        return None

    def buscar_por_actor(self, actor: str) -> list[dict[str, Any]]:
        """Busca peliculas de un actor.

        Returns:
            Lista de resultados de la busqueda.
        """
        data = self._get({"s": actor, "type": "movie", "apikey": OMDB_API_KEY})
        if data.get("Response") == "True":
            return cast(list[dict[str, Any]], data.get("Search", []))
        return []

    def _ejecutar(self, params: dict[str, str]) -> Any:
        """Llama protegido por el circuit breaker y reintentos."""
        try:
            return self._retrier(self._breaker.call, self._request, params)
        except pybreaker.CircuitBreakerError as exc:
            logger.warning("Circuito abierto para OMDB: %s", exc)
            raise NetworkError("OMDB no disponible (circuito abierto)") from exc

    def _request(self, params: dict[str, str]) -> Any:
        """Realiza la peticion GET a OMDB y devuelve el JSON."""
        logger.debug("Haciendo request a %s", OMDB_BASE_URL)
        try:
            response = requests.get(
                OMDB_BASE_URL, params=params, timeout=self._config.timeout
            )
        except requests.exceptions.Timeout as exc:
            raise NetworkError(f"Timeout al contactar OMDB: {exc}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(f"Fallo de conexion con OMDB: {exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise ApiClientError(f"Error HTTP de OMDB: {exc}") from exc

        if self._config.verbose:
            logger.debug("Status code: %s", response.status_code)
        return response.json()

    def _get(self, params: dict[str, str]) -> dict[str, Any]:
        """Ejecuta la llamada a OMDB (reintenta y degrada)."""
        return cast(dict[str, Any], self._ejecutar(params))


def _crear_retrier(config: AppConfig) -> Retrying:
    """Construye el reintentador con los parametros de la configuracion."""
    return Retrying(
        stop=stop_after_attempt(config.max_retries),
        wait=wait_exponential(multiplier=1, max=4),
        retry=retry_if_exception_type(NetworkError),
        reraise=True,
    )
