## Context

El proyecto no tiene tests. Tras refactorizar estructura (F3), errores (F4) y seguridad (F5), es necesario fijar el comportamiento con una suite automatizada. Las APIs externas (OMDB, TVMaze) no deben contactarse en los tests.

## Goals / Non-Goals

**Goals:**
- Suite `pytest` organizada por capa con fixtures y mocks.
- Cobertura ≥ 90%.
- Tests aislados de la red y de credenciales reales.
- Escenarios de specs de fases previas cubiertos.

**Non-Goals:**
- No hacer tests E2E de la UI de consola completa (dependen de `input()`).
- No integrar CI/CD (fuera de alcance).
- No testear código muerto eliminado.

## Decisions

- **Estructura de tests**: `tests/` con `conftest.py` (fixtures globales) y subcarpetas por capa: `tests/models/`, `tests/api/`, `tests/services/`, `tests/storage/`, `tests/ui/`, `tests/test_config.py`.
- **Mocking de red**: `pytest-mock` parchea `requests.Session.get`/`requests.get` en los clientes; se evita `responses` para mantener pocas dependencias.
- **Fixtures**: `conftest.py` define `omdb_client`, `tvmaze_client`, `favorites_repository`, `history_repository`, `movie_service`, `series_service`, `sample_movie`, `sample_series`, usando `tmp_path` para repositorios con persistencia.
- **Cobertura**: `[tool.coverage]` con `omit` de `tests/`; umbral `fail_under = 90`.
- **Configuración pytest**: `[tool.pytest.ini_options]` con `testpaths = ["tests"]` y `addopts` para verbose.
- **Datos de ejemplo**: se incluyen respuestas OMDB/TVMaze en fixtures como diccionarios fijos.

## Risks / Trade-offs

- [Cobertura < 90% por código muerto restante] → El paquete ya fue reducido en fases 2-3; si falta cobertura se añaden tests adicionales, no se bajan umbrales.
- [Mocks frágiles si cambia el cliente] → Se mokean a nivel de `requests` para que el comportamiento del cliente se pruebe de verdad.
- [Tests de UI dependen de `input()`] → Se extrae la lógica de menú en funciones puras testables o se simula `input` con monkeypatch cuando sea viable.
- [Variabilidad temporal/correlation IDs en logs] → No se asertan valores temporales exactos; se verifica presencia de campos.

## Migration Plan

1. Añadir dependencias dev (`pytest`, `pytest-mock`, `pytest-cov`) en `pyproject.toml`.
2. Configurar `[tool.pytest.ini_options]` y `[tool.coverage]`.
3. Crear `tests/conftest.py` con fixtures.
4. Escribir tests por capa.
5. Ejecutar `pytest --cov --cov-fail-under=90` hasta verde.
6. Rollback: los tests son aditivos; no afectan al código funcional.

## Open Questions

- ¿Se requiere también una prueba de humo de `main.py` (monkeypatch de `input`) o basta con tests por capa? (Se asume humo básico opcional.)