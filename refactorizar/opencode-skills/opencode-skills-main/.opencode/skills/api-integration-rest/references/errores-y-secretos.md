# Errores, Secretos y Degradacion

Como convertir fallos del transporte en comportamiento correcto de la aplicacion.

## Jerarquia de excepciones de dominio

Las capas superiores no deben conocer `requests`. El cliente traduce:

```python
# exceptions/__init__.py
class AppError(Exception):
    """Base de todos los errores de la aplicacion."""

class ConfigError(AppError):
    """Configuracion invalida."""

class ApiClientError(AppError):
    """Fallo de la API remota."""

class NetworkError(ApiClientError):
    """Fallo de red, timeout o circuito abierto."""

class PeliculaNotFoundError(ApiClientError):
    """La pelicula solicitada no existe."""
```

Jerarquia: `AppError` agrupa todo lo que la aplicacion sabe manejar, lo que
permite capturar de una vez en el composition root y tratar "error de negocio"
(distinto de un bug) de forma uniforme.

## Traduccion de fallos del transporte

| Fallo del transporte | Excepcion de dominio | Causa preservada |
|---|---|---|
| `requests.exceptions.Timeout` | `NetworkError("Timeout al consultar X")` | `from exc` |
| `requests.exceptions.ConnectionError` | `NetworkError("Fallo de conexion con X")` | `from exc` |
| `requests.exceptions.RequestException` | `ApiClientError(...)` | `from exc` |
| `pybreaker.CircuitBreakerError` | `NetworkError("circuito abierto")` | `from exc` |
| HTTP 404 | `PeliculaNotFoundError(...)` | `from exc` |
| JSON malformado | `ApiClientError("respuesta invalida")` | `from exc` |
| Respuesta con esquema inesperado | Error de validacion del modelo | `from exc` |

Reglas:

1. **Nunca `except:` desnudo.** Atrapa la excepcion concreta.
2. **Siempre `raise ... from exc`.** Sin la cadena de causa, el log pierde el
   error original, que es la mitad del diagnostico.
3. **No filtrar el traceback al usuario.** El traceback va al log; a la interfaz
   llega un mensaje accionable.
4. **No relanzar la excepcion del transporte.** Si sube hasta la capa de UI, esa
   capa queda atada a la libreria de HTTP.

## Secretos

La clave de la API se lee del entorno, nunca del codigo:

```python
import os
from dotenv import load_dotenv

load_dotenv()                      # lee .env en local
api_key = os.environ.get("OMDB_API_KEY", "")
```

Reglas innegociables:

- **Ningun secreto en el repositorio.** `.env` en `.gitignore`; solo `.env.example`
  versionado con la clave en blanco.
- **Nunca loguear la clave ni la URL completa con query string**, que suele
  incluirla como parametro.
- **Validar la clave al arrancar** y fallar temprano con un mensaje claro, en
  lugar de descubrir el problema en la primera busqueda del usuario.
- **Rotar si se filtra.** Un secreto en un commit es un secreto filtrado;
  reescribir el historial no lo devuelve.

```python
# Correcto: registra el host, no la consulta con la clave
logger.debug("Consultando %s", OMDB_BASE_URL)

# Incorrecto
logger.debug("GET %s?apikey=%s", url, api_key)
```

## Validacion de respuestas

No devolver el JSON crudo a las capas superiores:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Pelicula:
    titulo: str
    anio: str
    calificacion: float | None

    @classmethod
    def desde_api(cls, datos: dict[str, object]) -> "Pelicula":
        titulo = datos.get("Title")
        if not isinstance(titulo, str):
            raise ApiClientError("La API no devolvio 'Title'")
        return cls(
            titulo=titulo,
            anio=str(datos.get("Year", "")),
            calificacion=_a_float(datos.get("imdbRating")),
        )
```

La validacion ocurre en la frontera: dentro del proyecto, los datos ya son del
tipo correcto y `mypy --strict` puede asumirlo.

## Degradacion elegante

Decidir explicitamente que hace el servicio cuando la API falla:

| Situacion | Servicio devuelve | La UI muestra |
|---|---|---|
| Sin resultados | `None` | "No se encontraron peliculas" |
| Fallo de red | `None` / `[]` | "No se pudo conectar, intenta de nuevo" |
| Circuito abierto | `None` | "Servicio no disponible temporalmente" |
| Timeout | `None` | "La consulta tardo demasiado" |

La app **no crashea** por un fallo de red. La excepcion se registra en el log con
contexto y la interfaz continua disponible para el resto de opciones del menu.

```python
def buscar_pelicula(self, titulo: str) -> Pelicula | None:
    try:
        datos = self._client.buscar(titulo)
    except NetworkError as exc:
        logger.warning("Busqueda fallida para %r: %s", titulo, exc)
        return None                      # degradar, no propagar
    if datos is None:
        return None
    return Pelicula.desde_api(datos)
```

## Logging

- Nivel `debug` para detalle de una peticion; `info` para operaciones de negocio;
  `warning` para degradaciones recuperables; `error` para fallos no manejados.
- Formato con parametros posicionales (`logger.debug("GET %s", url)`), no
  f-strings: el mensaje solo se formatea si el nivel esta activo.
- Un identificador de correlacion por operacion, propagado a todos los registros
  de esa operacion, permite reconstruir que ocurrio en una busqueda concreta.
- Nunca `print()`: el `print` no tiene nivel, ni destino, ni contexto.
