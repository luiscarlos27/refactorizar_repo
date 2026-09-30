---
name: pytest-testing-automation
description: Disena, escribe y organiza suites de pruebas unitarias e integradas en Python con pytest, usando fixtures con ciclo de vida yield, scopes, factories, parametrizacion con ids, mock de APIs externas con pytest-mock o responses, aserciones nativas con patron AAA y cobertura con pytest-cov. Usar cuando el usuario pida "crear tests unitarios", "escribir pruebas con pytest", "configurar conftest.py", "mockear llamadas HTTP", "parametrizar tests", "aumentar cobertura" o "medir cobertura de tests". No usar para JavaScript/Jest ni para suites legacy con unittest.
license: MIT
compatibility: opencode
metadata:
  author: refactorizar_repo
  version: "1.0.0"
  domain: quality
  triggers: pytest, test unitario, tests, pruebas, conftest.py, fixture, mock, mocker, responses, respx, parametrize, cobertura, coverage, pytest-cov, AAA, assert, test suite, calidad de codigo, TDD
  role: specialist
  scope: testing
  output-format: report
  related-skills: test-master, python-pro, refactoring-code-smells, api-integration-rest, playwright-expert
---

# Automatizacion de Pruebas con Pytest

Constructor de suites de pruebas deterministas, rapidas y aisladas. Una prueba
que depende de la red, del reloj o del orden de ejecucion no es una prueba: es una
fuente de falsos negativos.

## Core Workflow

1. **Reconocer la estructura existente** - Respetar el layout, el `conftest.py` y
   las convenciones de mock del proyecto. No imponer otro layout sin motivo.
2. **Aislar las dependencias** - Ninguna prueba toca red, disco real, reloj ni
   procesos externos.
3. **Una prueba, un comportamiento** - Nombre descriptivo, patron AAA, una
   asercion conceptual.
4. **Parametrizar en vez de repetir** - Casos multiples via `@pytest.mark.parametrize`.
5. **Cubrir los limites, no solo el camino feliz** - Errores, vacios, TTL,
   agotamiento de reintentos, validacion fallida.
6. **Medir cobertura y leer los huecos** - La cobertura alta no es cobertura
   efectiva; un `return` temprano sin probar infla el numero.
7. **Quality gate** - La suite debe pasar junto a `ruff` y `mypy --strict`.

## Estructura

Seguir el layout del proyecto. En el proyecto de referencia, el codigo vive en un
paquete plano y `tests/` esta al lado, con `sys.path` ajustado en `conftest.py`:

```text
proyecto_refactoring/          # el proyecto
├── proyecto_refactoring/      # codigo vivo
│   ├── config.py
│   ├── main.py
│   ├── models/
│   ├── services/
│   ├── storage/
│   ├── api/
│   ├── ui/
│   └── exceptions/
└── tests/                     # un subdirectorio por capa
    ├── conftest.py
    ├── models/
    ├── services/
    ├── storage/
    ├── api/
    ├── ui/
    └── test_config.py
```

`conftest.py` es donde se ajusta el `sys.path` y se centralizan las fixtures
compartidas:

```python
import sys
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
PAQUETE_DIR = BASE_DIR / "proyecto_refactoring"

if str(PAQUETE_DIR) not in sys.path:
    sys.path.insert(0, str(PAQUETE_DIR))
```

`src layout` (codigo en `src/<paquete>/`) es preferible en proyectos nuevos,
porque aísla el codigo de los imports accidentales desde la raiz. En un proyecto
existente, migrar requiere tocar imports y `conftest.py`: es un cambio con
riesgo, no una mejora de estilo. No hacerlo sin peticion expresa.

## Configuracion de pytest

En `pyproject.toml`, bajo `[tool.pytest.ini_options]`:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = "-ra --strict-markers --strict-config"
markers = [
    "slow: pruebas lentas",
    "integration: requieren servicios externos",
    "smoke: humo de ruta critica",
]
```

Que se activa y que no, y por que:

| Opcion | Estado | Motivo |
|---|---|---|
| `testpaths` | Si | Acota la recoleccion a `tests/` |
| `-ra` | Si | Resumen de pruebas no aprobadas |
| `--strict-markers` | Si | Un marcador mal escrito falla en vez de ignorarse en silencio |
| `--strict-config` | Si | Una clave de config desconocida se detecta al inicio |
| `asyncio_mode` | **Solo con `pytest-asyncio`** | Sin el plugin, es una clave desconocida y `--strict-config` aborta |
| `--import-mode=importlib` | **No por defecto** | Puede romper proyectos que resuelven imports con `sys.path` en `conftest.py` |

`asyncio_mode` y `--import-mode=importlib` son cambios de bajo rendimiento y alto
riesgo: solo si la suite ya es async o si los imports son un problema medido.

## Patron AAA y aserciones nativas

```python
import pytest


def test_buscar_pelicula_devuelve_datos(client, mocker, omdb_response):
    # Arrange
    mocker.patch("api.omdb_client.requests.get", return_value=_mock(mocker, omdb_response))

    # Act
    resultado = client.buscar_por_titulo("Inception")

    # Assert
    assert resultado is not None
    assert resultado["Title"] == "Inception"


def test_timeout_se_traduce_a_network_error(client, mocker):
    # Arrange
    import requests
    mocker.patch(
        "api.omdb_client.requests.get",
        side_effect=requests.exceptions.Timeout("timeout"),
    )

    # Act + Assert
    with pytest.raises(NetworkError, match="Timeout al contactar"):
        client.buscar_por_titulo("Inception")
```

Usar `assert` nativo: pytest reescribe el arbol de aserciones y muestra la
comparacion real cuando falla, algo que `self.assertEqual` no hace.

Para excepciones, `pytest.raises(..., match=...)` verifica el tipo **y** el
mensaje: un `match` equivocado detecta un mensaje cambiado por error.

## Reference Guide

- `references/fixtures-y-mocks.md` - `yield` teardown, scopes, factory fixtures,
  `parametrize` con `ids`, y las tres tecnicas de mock de HTTP con cuando usarlas.
- `references/cobertura-y-ci.md` - Umbral, informes, comandos utiles y la matriz de
  casos limite que un proyecto de cliente REST debe cubrir.

## Matriz minima de cobertura

Ningun modulo de cliente, servicio o repositorio se considera cubierto sin al
menos estos casos:

| Categoria | Casos |
|---|---|
| Camino feliz | Exito con datos, exito con lista vacia |
| Errores | Excepcion de cada rama de `except` |
| Limites | TTL expirado, lista vacia, entrada invalida |
| Resiliencia | Reintentos agotados, circuito abierto, API caida |
| Validacion | Config invalida, modelo con invariantes rotas |
| Integridad | Secretos ausentes del log, claves no en el repo |

## Que NO hacer

- **NO** llamar a una API real en la suite. Consume cuota, es lenta y falla por
  causas ajenas al codigo bajo prueba.
- **NO** usar bucles `for` con `assert` dentro de un test**: el primer fallo corta
  el bucle y oculta el resto de casos. Usar `parametrize`.
- **NO** importar `conftest.py` a mano. pytest lo descubre e inyecta solo.
- **NO** compartir estado mutable entre tests (listas, diccionarios a nivel de
  modulo). Produce tests que pasan solos y fallan en suite.
- **NO** testear la implementacion en vez del comportamiento: `assert cliente._x
  == 3` se rompe con cada refactorizacion interna.
- **NO** relajar el umbral de cobertura ni marcar `skip` para hacer pasar la
  suite. Un `skip` sin justificacion es una prueba perdida.
- **NO** asyncio** sin `pytest-asyncio` instalado**; la clave de config hara fallar
  toda la suite.
