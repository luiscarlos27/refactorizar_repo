"""Cache en memoria con TTL para respuestas de APIs externas."""

from dataclasses import dataclass
from time import monotonic
from typing import Any


@dataclass
class _Entrada:
    """Valor cacheado con su instante de expiracion."""

    valor: Any
    expira_en: float


class Cache:
    """Cache simple por clave con tiempo de expiracion (TTL)."""

    def __init__(self, ttl_segundos: int = 300) -> None:
        self._ttl_segundos = ttl_segundos
        self._datos: dict[str, _Entrada] = {}

    def get(self, clave: str) -> Any | None:
        """Devuelve el valor cacheado o None si no existe o expiro."""
        entrada = self._datos.get(clave)
        if entrada is None:
            return None
        if monotonic() >= entrada.expira_en:
            del self._datos[clave]
            return None
        return entrada.valor

    def set(self, clave: str, valor: Any, ttl_segundos: int | None = None) -> None:
        """Guarda un valor asociado a una clave con TTL."""
        ttl = ttl_segundos if ttl_segundos is not None else self._ttl_segundos
        self._datos[clave] = _Entrada(valor=valor, expira_en=monotonic() + ttl)

    def clear(self) -> None:
        """Elimina todos los valores cacheados."""
        self._datos.clear()
