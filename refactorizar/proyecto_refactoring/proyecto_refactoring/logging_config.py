"""Configuracion centralizada de logging y correlation ID por operacion."""

import logging
import sys
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from config import AppConfig

_FORMAT = "[%(asctime)s] %(levelname)-8s [%(correlation_id)s] %(name)s: %(message)s"
_LOG_FILENAME = "app.log"

_correlation_ctx: ContextVar[str] = ContextVar("correlation_id", default="-")


class _CorrelationFilter(logging.Filter):
    """Adjunta el correlation ID activo a cada registro."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = _correlation_ctx.get()
        return True


def setup_logging(config: AppConfig) -> None:
    """Configura consola y archivo con nivel segun ``config`` (solo una vez)."""
    root = logging.getLogger()
    if root.handlers:
        return

    nivel = logging.DEBUG if config.debug else logging.INFO
    root.setLevel(nivel)

    formatter = logging.Formatter(_FORMAT)

    filtro = _CorrelationFilter()

    consola = logging.StreamHandler(sys.stdout)
    consola.setLevel(nivel)
    consola.setFormatter(formatter)
    consola.addFilter(filtro)
    root.addHandler(consola)

    archivo = logging.FileHandler(_LOG_FILENAME, encoding="utf-8")
    archivo.setLevel(logging.DEBUG)
    archivo.setFormatter(formatter)
    archivo.addFilter(filtro)
    root.addHandler(archivo)

    if config.debug:
        root.debug("Logging configurado (consola + %s)", _LOG_FILENAME)


def get_logger(nombre: str) -> logging.Logger:
    """Devuelve un logger con el nombre del modulo."""
    return logging.getLogger(nombre)


@contextmanager
def correlation_scope(scope: str) -> Iterator[str]:
    """Genera un correlation ID para una operacion y lo propaga al contexto.

    Todos los registros emitidos dentro del bloque comparten el mismo ID.
    """
    correlation_id = f"{scope}-{uuid.uuid4().hex[:8]}"
    token = _correlation_ctx.set(correlation_id)
    try:
        yield correlation_id
    finally:
        _correlation_ctx.reset(token)
