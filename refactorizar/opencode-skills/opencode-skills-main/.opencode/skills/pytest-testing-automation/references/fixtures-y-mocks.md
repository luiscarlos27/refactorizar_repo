# Fixtures y Mocking

## Ciclo de vida con `yield`

El codigo antes del `yield` es *setup*, el de despues es *teardown*, y se
ejecuta aunque la prueba falle. Esa garantia es la razon para preferir `yield`
sobre un `return` con limpieza manual.

```python
import pytest


@pytest.fixture
def cache():
    c = Cache(ttl_segundos=300)      # setup
    yield c                           # la prueba usa c
    c.limpiar()                       # teardown garantizado


@pytest.fixture
def archivo_temporal(tmp_path):
    ruta = tmp_path / "datos.json"
    ruta.write_text("[]")
    yield ruta
    # tmp_path ya lo limpia pytest; no hace falta borrar a mano
```

## Scopes

| Scope | Cuándo | Ejemplo |
|---|---|---|
| `function` (por defecto) | Estado aislado por prueba | Cache en memoria, cliente |
| `module` | Reutilizable dentro de un archivo, sin coste por prueba | Datos de lectura |
| `session` | Recurso costoso, creado una vez para toda la suite | Motor de BD, servidor HTTP de test |

Regla: un scope amplio convierte a las pruebas en estado compartido. Bajar a
`session` solo si el setup es caro de verdad.

## Factory fixtures

Cuando una prueba necesita varios objetos con variaciones, la fixture devuelve una
fabrica, no un objeto:

```python
@pytest.fixture
def make_pelicula():
    # Allow-override: parametros opcionales en vez de fixtures multiples
    def _make_pelicula(titulo="Inception", anio="2010", calificacion=8.8):
        return Pelicula(titulo=titulo, anio=anio, calificacion=calificacion)
    return _make_pelicula


def test_con_mala_calificacion(make_pelicula):
    p = make_pelicula(calificacion=2.0)
    assert p.calificacion == 2.0
```

## Fixtures de datos de ejemplo

Centralizar en `conftest.py` los datos que usan varias pruebas:

```python
@pytest.fixture
def omdb_response() -> dict:
    return {
        "Response": "True",
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Genre": "Sci-Fi",
    }
```

Ventaja: cuando la API cambia un campo, se actualiza en un solo sitio en vez de
en veinte pruebas.

## Parametrizacion

```python
import pytest


@pytest.mark.parametrize(
    "titulo,esperado",
    [
        ("Inception", True),
        ("NoExiste", False),
        ("", False),
    ],
    ids=["encontrada", "inexistente", "entrada_vacia"],
)
def test_buscar_pelicula(titulo, esperado, client, mocker, omdb_response):
    mocker.patch(
        "api.omdb_client.requests.get",
        return_value=_mock(mocker, omdb_response),
    )
    assert (client.buscar_por_titulo(titulo) is not None) == esperado
```

`ids` convierte `test_buscar_pelicula[encontrada-True]` en un nombre legible.
Sin `ids`, el reporte muestra el valor crudo, que en datos complejos es ilegible.

## Mock de HTTP: tres tecnicas

| Tecnica | Cuando usarla | Anade dependencia |
|---|---|---|
| `pytest-mock` (`mocker`) | Convencion ya establecida en el proyecto; patch puntual de una funcion | ya instalado |
| `responses` | Intercepta por URL y status; mas declarativo, mejor para varios endpoints | `pip install responses` |
| `respx` | Solo para clientes async con `httpx` | `pip install respx pytest-asyncio` |

### Opcion A: `pytest-mock` (convencion del proyecto de referencia)

```python
import pytest


@pytest.fixture
def client(config) -> PeliculaClient:
    return PeliculaClient(config, api_key="test-key")


def _mock(mocker, data, status=200):
    respuesta = mocker.Mock()
    respuesta.json.return_value = data
    respuesta.status_code = status
    return respuesta


def test_exito(client, mocker, omdb_response):
    mocker.patch("api.omdb_client.requests.get", return_value=_mock(mocker, omdb_response))
    assert client.buscar_por_titulo("Inception")["Title"] == "Inception"


def test_timeout(client, mocker):
    import requests
    mocker.patch(
        "api.omdb_client.requests.get",
        side_effect=requests.exceptions.Timeout("timeout"),
    )
    with pytest.raises(NetworkError, match="Timeout al contactar"):
        client.buscar_por_titulo("X")
```

Puntos clave:

- **Parchear donde se usa, no donde se define.** `api.omdb_client.requests.get`,
  no `requests.get`: parchear el origen no surte efecto si el modulo ya hizo
  `import requests`.
- **`side_effect`** para excepciones, `return_value` para respuestas normales.
- **`mocker` se revierte solo** al terminar la prueba. Con `unittest.mock.patch`
  a mano, un test que falla antes del `patch.stop` deja el mock puesto y
  contamina el resto de la suite.

### Opcion B: `responses` (mas declarativo)

```python
import responses


@responses.activate
def test_exito_con_responses(omdb_response):
    responses.add(
        responses.GET,
        "https://api.omdbapi.com/",
        json=omdb_response,
        status=200,
    )
    assert PeliculaClient("https://api.omdbapi.com/", "k").buscar("Inception") is not None
```

`responses` permite ademas afirmar que no hubo llamadas inesperadas
(`assert_all_requests_are_fired`), util para detectar peticiones que el test no
declaro.

### Opcion C: `respx` (async)

```python
import pytest
import respx
from httpx import Response


@pytest.mark.asyncio
@respx.mock
async def test_async():
    respx.get("https://api.example.com/x").mock(return_value=Response(200, json={"ok": True}))
    ...
```

## Mockear el tiempo

El TTL de la cache y los reintentos dependen del reloj. Inyectar el tiempo en vez
de esperar:

```python
def test_cache_expira(make_pelicula, mocker):
    cache = Cache(ttl_segundos=1)
    cache.guardar("k", make_pelicula())
    mocker.patch("time.monotonic", return_value=999.0)   # salto mas alla del TTL
    assert cache.obtener("k") is None
```

## Trampas

- **Parchear el simbolo equivocado.** Parchear `requests.get` en el test no
  surte efecto sobre un modulo que ya habia importado la referencia.
- **Mock que devuelve `Mock()` sin configurar.** `respuesta.json()` devuelve otro
  `Mock`, y la prueba pasa probando nada. Configurar `status_code` y
  `json.return_value`.
- **Estado compartido entre pruebas.** Una fixture de scope `session` mutable hace
  que el resultado dependa del orden de ejecucion. Con `pytest -p no:randomly` se
  ve; sin el, el fallo aparece en CI y no en local.
- **Probar el mock en vez del codigo.** `assert mock.call_count == 1` verifica el
  mock. Verificar el comportamiento: excepcion de dominio, valor devuelto.
- **`mocker.patch.object` sobre atributo interno.** Si el atributo es privado
  (`_breaker`), la prueba queda acoplada a la implementacion y se rompe con
  cualquier refactorizacion interna.
