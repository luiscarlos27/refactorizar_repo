## Why

El código de la fase 3 aún depende de `bare except`, no distingue tipos de error, imprime trazas por consola sin formato y llama a APIs externas sin protección frente a fallos de red ni reintentos. Esta fase introduce una jerarquía de excepciones explícita, logging estructurado con el módulo `logging` (con correlation ID por operación) y resiliencia en las llamadas externas (timeouts, reintentos con backoff, circuit breaker y degradación elegante), de modo que la app nunca crashee ante fallos de red.

## What Changes

- Se completa la jerarquía de excepciones en `exceptions/`: `ApiClientError`, `MovieNotFoundError`, `SeriesNotFoundError`, `NetworkError`, `ConfigError`.
- Se sustituyen todos los `bare except:` del código por excepciones específicas.
- Se implementa logging centralizado con el módulo `logging` (niveles, handlers a archivo y consola), reemplazando `print()` de depuración.
- Se añade un correlation/trace ID por operación de búsqueda que se propaga a los registros de esa operación.
- Se añade resiliencia a los clientes HTTP: timeouts explícitos, reintentos con backoff exponencial (`tenacity`) y circuit breaker (`pybreaker`).
- Se implementa degradación elegante: ante fallo de API, el servicio retorna valores por defecto/`None` y la UI muestra un mensaje controlado.

## Capabilities

### New Capabilities
- `error-handling`: Jerarquía de excepciones de dominio y reemplazo de `bare except`.
- `logging`: Logging estructurado con el módulo `logging` y correlation IDs por operación.
- `api-resilience`: Timeouts, reintentos con backoff, circuit breaker y degradación elegante en llamadas externas.

### Modified Capabilities

## Impact

- Código afectado: `api/`, `services/`, `ui/`, `main.py`, `exceptions/`.
- Dependencias nuevas: `tenacity`, `pybreaker`.
- Sin cambios de contrato de las APIs externas.
- Se eliminan los `print()` de depuración.