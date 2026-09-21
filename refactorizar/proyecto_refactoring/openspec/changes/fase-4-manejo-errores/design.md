## Context

Tras la fase 3, la app tiene arquitectura limpia por capas pero aún usa `bare except`, `print()` y llamadas HTTP sin protección. Esta fase endurece errores, logging y resiliencia usando `tenacity` (retries) y `pybreaker` (circuit breaker). Aplicamos patrones de resiliencia de sistemas distribuidos a escala local: toda llamada externa con timeout + retry budget + degradación.

## Goals / Non-Goals

**Goals:**
- Jerarquía de excepciones explícita y completa.
- Cero `bare except` y cero `print()` de depuración.
- Logging estructurado con correlation IDs.
- Llamadas externas con timeout, reintentos con backoff y circuit breaker.
- La app no crashea ante fallos de red; degrada con mensajes controlados.

**Non-Goals:**
- No migrar a async (se mantiene `requests` síncrono).
- No implementar tracing distribuido real (solo correlation ID local).
- No abordar seguridad de credenciales (fase 5).
- No crear tests (fase 6).

## Decisions

- **Jerarquía de excepciones**: base `AppError(Exception)`; subclases `ApiClientError`, `MovieNotFoundError`, `SeriesNotFoundError`, `NetworkError`, `ConfigError`. Los clientes traducen excepciones de `requests` a `NetworkError`/`ApiClientError`.
- **Logging**: módulo `logging.py` (o `core/logging_config.py`) que configura handlers a consola y archivo; cada módulo crea `logging.getLogger(__name__)`. Correlation ID mediante un campo contextual propagado (p. ej. argumento de contexto o `contextvars`).
- **Resiliencia con `tenacity`**: decorador `@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=4))` sobre las llamadas internas de los clientes, elevando a `NetworkError` al agotar intentos.
- **Circuit breaker con `pybreaker`**: una instancia `CircuitBreaker(fail_max=5, reset_timeout=30)` compartida por cliente; al abrirse, las llamadas fallan rápido y la capa de servicio degrada.
- **Degradación en servicios**: `buscar_por_titulo` retorna `None` (o `Movie` si hay éxito); `buscar_series` retorna `[]`; la UI captura `AppError` y muestra mensajes amigables.
- **Sin breakers globales**: el breaker vive en el cliente, no en módulos globales.

## Risks / Trade-offs

- [`tenacity`/`pybreaker` añaden dependencias] → Son librerías ligeras y estándar; se declaran en `pyproject.toml`.
- [Circuit breaker puede bloquear recuperación en pruebas locales] → Umbral (5) y reset (30 s) configurables para permitir pruebas.
- [Correlation ID complejo de propagar] → Se limita al contexto de una operación de búsqueda; no se introduce infraestructura de tracing.
- [Cambio en comportamiento visible de la UI] → Mensajes amigables reemplazan textos de error crudos; se verifica con ejecución manual.

## Migration Plan

1. Completar `exceptions/` con la jerarquía.
2. Configurar logging centralizado y correlation ID.
3. Añadir timeouts a los clientes.
4. Añadir retries (`tenacity`) y circuit breaker (`pybreaker`) a los clientes.
5. Traducir errores y propagar excepciones de dominio.
6. Ajustar servicios para degradar y UI para mostrar mensajes controlados.
7. Eliminar `bare except` y `print()` restantes.
8. Verificar `python main.py`, `ruff check`.
9. Rollback: git checkout de la fase previa.

## Open Questions

- ¿El correlation ID se expone en la UI o solo en logs? (Se asume solo en logs.)