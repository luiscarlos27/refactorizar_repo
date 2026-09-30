# Reintentos y Circuit Breaker

Politica de resiliencia ante fallos transitorios. El objetivo es no amplificar un
incidente: si el servidor esta caido, el cliente no debe sumar presion.

## Que se reintenta y que no

| Situacion | Reintentable | Notas |
|---|---|---|
| `requests.exceptions.Timeout` | Si | Transitorio por definicion |
| `requests.exceptions.ConnectionError` | Si | DNS, conexion rechazada, reset |
| HTTP 500 Internal Server Error | Si | Fallo del servidor |
| HTTP 502 Bad Gateway | Si | Proxy o upstream caido |
| HTTP 503 Service Unavailable | Si | Suele venir con `Retry-After` |
| HTTP 504 Gateway Timeout | Si | El upstream no respondio |
| HTTP 429 Too Many Requests | Si | Respetar `Retry-After` |
| HTTP 400 Bad Request | **No** | Peticion invalida: reintentar repetiria el error |
| HTTP 401 Unauthorized | **No** | Credencial incorrecta: no mejora con esperas |
| HTTP 403 Forbidden | **No** | Permiso denegado |
| HTTP 404 Not Found | **No** | El recurso no existe |
| HTTP 422 Unprocessable Entity | **No** | Validacion de entrada fallo |

Regla: se reintenta lo que **podria** funcionar igual en el siguiente intento.
Un 400 no va a convertirse en un 200 por esperar mas.

## Backoff exponencial con jitter

```text
delay = min(base * 2 ** intento, tope_maximo) + aleatorio(0, jitter)
```

En codigo:

```python
import random

base, tope, jitter = 1.0, 30.0, 0.5
intento = 2
delay = min(base * 2 ** intento, tope) + random.uniform(0, jitter)   # ~4.0-4.5 s
```

Con `tenacity` esto ya viene resuelto y con tests:

```python
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential

Retrying(
    stop=stop_after_attempt(3),                       # tope duro de intentos
    wait=wait_exponential(multiplier=1, max=10),      # backoff acotado a 10 s
    retry=retry_if_exception_type(NetworkError),      # solo transitorios
    reraise=True,                                     # relanza la ultima excepcion
)
```

Por que el jitter importa: sin el, todos los clientes que fallaron a la vez
reintentan a la vez, y la senal se convierte en un pico que tumba al servidor que
se estaba recuperando. Es el problema de la manada atronadora.

Por que `reraise=True`: sin el, `tenacity` lanza su propia excepcion y se pierde
la causa original, que es justo lo que se necesita para diagnosticar.

## Limites

- **Tope de intentos:** 3 a 5. Nunca reintentos infinitos: un bucle infinito
  contra un servidor caido consume recursos sin limite.
- **Tope de espera:** el backoff sin techo produce esperas de minutos, que en una
  CLI se traduce en "la app se congela".
- **Presupuesto total:** el tiempo total de reintentos debe ser compatible con la
  expectativa del usuario. Si el usuario espera 2 segundos, tres reintentos con
  backoff de 10 s son un fallo de diseño, no de red.

## Circuit breaker

El reintento resuelve fallos aislados. El circuit breaker resuelve el fallo
sostenido: cuando el servidor esta caido, abrir el circuito y dejar de intentarlo
protege al cliente y al servidor.

Estados: `closed` (normal) -> `open` (deja de llamar) -> `half-open` (prueba si
volvio).

```python
import pybreaker

breaker = pybreaker.CircuitBreaker(
    fail_max=5,           # 5 fallos consecutivos abren el circuito
    reset_timeout=30,     # 30 s en open antes de probar en half-open
)

def _llamar() -> dict:
    return breaker.call(self._request, params)
```

Al abrirse:

```python
try:
    datos = self._retrier(self._breaker.call, self._request, params)
except pybreaker.CircuitBreakerError as exc:
    logger.warning("Circuito abierto: %s", exc)
    raise NetworkError("API no disponible (circuito abierto)") from exc
```

Parametros a ajustar:

| Parametro | Efecto | Valor de partida |
|---|---|---|
| `fail_max` | Numero de fallos consecutivos que abren el circuito | 5 |
| `reset_timeout` | Segundos en `open` antes de probar de nuevo | 30 |
| `exclude` | Excepciones que no cuentan como fallo | `[]` |

Un `reset_timeout` corto hace sondar con frecuencia un servidor que sigue caido.
Uno largo retrasa la recuperacion. El valor correcto depende de la API.

## Orden de composicion

```text
CircuitBreaker.call( Retrying( request ) )
```

Es decir, cada intento individual pasa por el breaker, y el retrier reintenta
llamando al breaker de nuevo. Al revés, el retrier consumiria sus intentos
mientras el circuito ya esta abierto y los gastaria sin hacer nada.

## Combinacion con cache y rate limit

- La cache reduce la frecuencia de llamadas, y con ella la probabilidad de abrir
  el circuito por trafico evitable.
- Un `429` sostenido es sintoma de que el rate limit local no se respeta: revisar
  el cache antes de considerar subir `fail_max` o `reset_timeout`.

## Trampas

- **Reintentar tambien los 4xx de cliente.** Multiplica el numero de peticiones
  sin ninguna probabilidad de exito y consume cuota del usuario.
- **Backoff sin tope ni jitter.** Bloquea la app y amplifica la caida.
- **Breaker por peticion.** Si se crea un `CircuitBreaker` dentro del metodo que
  llama, nunca acumula fallos y nunca se abre. Debe vivir en el cliente.
- **Confundir `Timeout` con lentitud.** Un timeout corto produce reintentos que
  empeoran la carga; medir antes de bajar el valor.
- **Exponer la excepcion cruda al usuario.** Traducir a excepcion de dominio con
  un mensaje accionable (ver `errores-y-secretos.md`).
