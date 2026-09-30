---
name: api-integration-rest
description: Disena e implementa clientes HTTP REST robustos y resilientes en Python con requests, reintentos con backoff exponencial y jitter, timeouts explicitos, manejo de rate limits, circuit breaker, cache con TTL y traduccion de errores a excepciones de dominio. Usar cuando el usuario pida "conectar a una API", "crear cliente REST", "integrar API externa", "manejar reintentos HTTP", "agregar timeout", "circuit breaker", "cachear respuestas de API" o "hacer solicitudes resilientes". No usar para clientes async con httpx/aiohttp.
license: MIT
compatibility: opencode
metadata:
  author: refactorizar_repo
  version: "1.0.0"
  domain: api-architecture
  triggers: API REST, cliente HTTP, requests,httpx, integrar API, endpoint, reintentos, retry, backoff exponencial, jitter, timeout, rate limit, 429, Retry-After, circuit breaker, pybreaker, tenacity, cache TTL, session reuse, connection pooling
  role: specialist
  scope: implementation
  output-format: code
  related-skills: python-pro, secure-code-guardian, refactoring-code-smells, pytest-testing-automation, monitoring-expert
---

# Integracion Robusta a APIs REST

Constructor de clientes REST listos para produccion en Python. El objetivo es
que un fallo transitorio de la red, una sobrecarga del servidor o un limite de
tasa se traduzcan en un comportamiento predecible, y que el secreto nunca se
exponga.

Alcance: **Python sincrono con `requests`**. Si el proyecto es async, esta skill
no aplica tal cual (ver la nota final).

## Core Workflow

1. **Configuracion centralizada** - Base URL, timeouts y credenciales en un objeto
   de configuracion validado, nunca en el cliente ni en el codigo de negocio.
2. **Timeouts explicitos** - Sin timeout, una peticion puede colgarse para
   siempre. Timeout de conexion y de lectura separados, siempre configurables.
3. **Reintentos solo de transitorios** - Backoff exponencial con jitter para
   errores de red y 5xx; nunca para 4xx de cliente. Ver
   `references/retry-y-breaker.md`.
4. **Circuit breaker** - Cortar el flujo cuando la tasa de fallos consecutivos
   supera un umbral, para no castigar al servidor degradado.
5. **Traduccion de errores** - Cada fallo del transporte se traduce a una
   excepcion de dominio propia. Ver `references/errores-y-secretos.md`.
6. **Capa de abstraccion** - El cliente devuelve datos de dominio validados, no
   el JSON crudo ni el objeto `Response`.
7. **Cache con TTL** - Evitar llamadas repetidas y respectar el rate limit.
8. **Degradacion elegante** - Definir que devuelve el servicio cuando la API no
   responde, en lugar de propagar el fallo hasta la interfaz.
9. **Pruebas sin red** - Interceptar en el transporte con `responses` o
   `pytest-mock`. Nunca llamadas reales en la suite.

## Decisiones de diseno

| Decision | Motivo |
|---|---|
| `requests.Session` reutilizada | Connection pooling y reutilizacion de conexiones TCP/TLS |
| Timeout `(conexion, lectura)` como tupla | Evita que un servidor lento bloquee el pool de conexiones |
| Reintentos en el cliente, no en el servicio | El servicio no debe conocer la politica de red |
| Errores de dominio, no `requests` | Las capas superiores no dependen del transporte |
| Config por dataclass validada | Timeouts y reintentos se pueden testear y ajustar |
| Claves por entorno | Ningun secreto en el codigo ni en los logs |

## Ejemplo de cliente con el stack de referencia

```python
import requests
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential


class ApiClientError(Exception):
    """Fallo recuperable de la API."""


class NetworkError(ApiClientError):
    """Fallo de red o timeout."""


class PeliculaClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 10, max_retries: int = 3) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._timeout = timeout
        # Session reutilizada: pooling de conexiones entre llamadas
        self._session = requests.Session()
        self._retrier = Retrying(
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=1, max=10),
            retry=retry_if_exception_type(NetworkError),
            reraise=True,
        )

    def buscar(self, titulo: str) -> dict[str, object] | None:
        def _request() -> dict[str, object]:
            try:
                respuesta = self._session.get(
                    self._base_url,
                    params={"t": titulo, "apikey": self._api_key},
                    timeout=self._timeout,          # nunca sin timeout
                    headers={"Accept": "application/json"},
                )
            except requests.exceptions.Timeout as exc:
                raise NetworkError(f"Timeout al consultar {self._base_url}") from exc
            except requests.exceptions.ConnectionError as exc:
                raise NetworkError(f"Fallo de conexion con {self._base_url}") from exc
            except requests.exceptions.RequestException as exc:
                raise ApiClientError(f"Error HTTP: {exc}") from exc

            respuesta.raise_for_status()
            return respuesta.json()

        return self._retrier(_request)
```

## Rate limits

- Respetar el encabezado `Retry-After` cuando venga en un `429` o `503`: es la
  indicacion autoritativa del servidor y tiene prioridad sobre el backoff propio.
- Registrar el limite si la API lo expone en encabezados (`X-RateLimit-*`).
- El circuit breaker es la segunda linea de defensa cuando el limite se
  incumple repetidamente.

## Cache

- Cachear en memoria con TTL para evitar llamadas identicas consecutivas.
- TTL configurable, no constante magica.
- Invalidar o ignorar el cache cuando los datos sean de un solo uso.

## Reference Guide

- `references/retry-y-breaker.md` - Tabla reintentable / no reintentable, formula de
  backoff en codigo plano, `Retry-After`, circuit breaker con `pybreaker`.
- `references/errores-y-secretos.md` - Traduccion a excepciones de dominio,
  manejo de secretos por entorno, validacion de respuestas, degradacion elegante.

## Nota de alcance: async

Esta skill cubre el cliente sincrono. Para `httpx.AsyncClient` / `aiohttp`:

- El resto de reglas aplican igual (timeouts, reintentos, traduccion de errores,
  secretos).
- Cambia la libreria de interceptacion en tests: `respx` en vez de `responses`.
- El circuit breaker debe ser compartido entre tareas concurrentes; un breaker
  por peticion anula el patron.
