"""Configuracion unica de la aplicacion.

Reemplaza los modulos de configuracion dispersos del codigo original.
"""

from dataclasses import dataclass

from constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT


@dataclass
class AppConfig:
    """Configuracion de la aplicacion con valores por defecto tipados."""

    debug: bool = True
    verbose: bool = True
    timeout: int = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES

    def __post_init__(self) -> None:
        """Valida invariantes basicos de la configuracion."""
        if self.timeout <= 0:
            raise ValueError(f"timeout debe ser positivo: {self.timeout}")
        if self.max_retries < 0:
            raise ValueError(f"max_retries no puede ser negativo: {self.max_retries}")


CONFIG = AppConfig()
