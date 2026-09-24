"""Cliente HTTP dedicado para la API de TVMaze, sin logica de negocio."""

from typing import Any, cast

import pybreaker
import requests
from config import AppConfig
from constants import TVMAZE_BASE_URL
from exceptions import ApiClientError, NetworkError
from logging_config import get_logger
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = get_logger(__name__)


class TvmazeClient:
    """Encapsula las llamadas REST a TVMaze con timeout, retries y breaker.

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

    def buscar_series(self, nombre: str) -> list[dict[str, Any]]:
        """Busca series por nombre.

        Returns:
            Lista de resultados de la busqueda.
        """
        url = f"{TVMAZE_BASE_URL}/search/shows"
        return cast(list[dict[str, Any]], self._ejecutar(url, {"q": nombre}))

    def obtener_detalles(self, id_serie: int) -> dict[str, Any]:
        """Obtiene los detalles de una serie por id.

        Returns:
            Diccionario con los detalles de la serie.
        """
        url = f"{TVMAZE_BASE_URL}/shows/{id_serie}"
        return cast(dict[str, Any], self._ejecutar(url, None))

    def _ejecutar(self, url: str, params: dict[str, str] | None) -> Any:
        """Llama protegido por el circuit breaker y reintentos."""
        try:
            return self._retrier(self._breaker.call, self._request, url, params)
        except pybreaker.CircuitBreakerError as exc:
            logger.warning("Circuito abierto para TVMaze: %s", exc)
            raise NetworkError("TVMaze no disponible (circuito abierto)") from exc

    def _request(self, url: str, params: dict[str, str] | None) -> Any:
        """Realiza la peticion GET a TVMaze y devuelve el JSON."""
        logger.debug("Haciendo request a %s", url)
        try:
            response = requests.get(url, params=params, timeout=self._config.timeout)
        except requests.exceptions.Timeout as exc:
            raise NetworkError(f"Timeout al contactar TVMaze: {exc}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise NetworkError(f"Fallo de conexion con TVMaze: {exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise ApiClientError(f"Error HTTP de TVMaze: {exc}") from exc

        if self._config.verbose:
            logger.debug("Status code: %s", response.status_code)
        return response.json()


def _crear_retrier(config: AppConfig) -> Retrying:
    """Construye el reintentador con los parametros de la configuracion."""
    return Retrying(
        stop=stop_after_attempt(config.max_retries),
        wait=wait_exponential(multiplier=1, max=4),
        retry=retry_if_exception_type(NetworkError),
        reraise=True,
    )
