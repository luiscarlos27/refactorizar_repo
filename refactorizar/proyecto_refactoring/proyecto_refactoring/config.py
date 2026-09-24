"""Configuracion unica de la aplicacion.

Reemplaza los modulos de configuracion dispersos del codigo original.
"""

from dataclasses import dataclass

from constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from exceptions import ConfigError


@dataclass
class AppConfig:
    """Configuracion de la aplicacion con valores por defecto tipados."""

    debug: bool = True
    verbose: bool = True
    timeout: int = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES
    circuit_fail_max: int = 5
    circuit_reset_timeout: float = 30.0

    def __post_init__(self) -> None:
        """Valida tipos e invariantes basicos de la configuracion."""
        if not isinstance(self.debug, bool) or not isinstance(self.verbose, bool):
            raise ConfigError("debug y verbose deben ser booleanos")
        if isinstance(self.timeout, bool) or not isinstance(self.timeout, int):
            raise ConfigError(f"timeout debe ser un entero: {self.timeout!r}")
        if isinstance(self.max_retries, bool) or not isinstance(self.max_retries, int):
            raise ConfigError(f"max_retries debe ser un entero: {self.max_retries!r}")
        if isinstance(self.circuit_fail_max, bool) or not isinstance(self.circuit_fail_max, int):
            raise ConfigError(
                f"circuit_fail_max debe ser un entero: {self.circuit_fail_max!r}"
            )
        if isinstance(self.circuit_reset_timeout, bool) or not isinstance(
            self.circuit_reset_timeout, (int, float)
        ):
            raise ConfigError(
                f"circuit_reset_timeout debe ser numerico: {self.circuit_reset_timeout!r}"
            )
        if self.timeout <= 0:
            raise ConfigError(f"timeout debe ser positivo: {self.timeout}")
        if self.max_retries < 0:
            raise ConfigError(f"max_retries no puede ser negativo: {self.max_retries}")
        if self.circuit_fail_max <= 0:
            raise ConfigError(f"circuit_fail_max debe ser positivo: {self.circuit_fail_max}")
        if self.circuit_reset_timeout <= 0:
            raise ConfigError(
                f"circuit_reset_timeout debe ser positivo: {self.circuit_reset_timeout}"
            )
