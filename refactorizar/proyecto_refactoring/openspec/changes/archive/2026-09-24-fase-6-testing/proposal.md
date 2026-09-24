## Why

El proyecto no tiene ninguna prueba automatizada. Las fases 2-5 refactorizaron el código de forma estructural, por lo que se necesita una suite de tests que garantice que el comportamiento se conserva, prevenga regresiones y permita medir la cobertura. Esta fase crea una suite `pytest` con tests unitarios (modelos, servicios, repositorios, validación), tests de integración con APIs mockeadas y cobertura objetivo ≥ 90%.

## What Changes

- Se crea el directorio `tests/` con estructura organizada por capa (models, api, services, storage, ui, config).
- Se configuran `pytest`, `pytest-mock`, `pytest-cov` en `pyproject.toml` (con `[tool.pytest.ini_options]` y umbral de cobertura).
- Tests unitarios para modelos (creación, validación, conversión), repositorios (favoritos, historial, caché, export/import), servicios (delegación, degradación) y validación de entrada.
- Tests de integración de clientes HTTP con mocks de `requests` (`pytest-mock`) para OMDB y TVMaze.
- Fixtures reutilizables y datos de ejemplo parametrizados.
- Cobertura medida con `pytest --cov` y objetivo ≥ 90%.

## Capabilities

### New Capabilities
- `test-suite`: Suite de pruebas automatizadas con pytest, mocks de APIs externas y cobertura ≥ 90%.

### Modified Capabilities

## Impact

- Código afectado: ninguno funcional (solo tests nuevos).
- Archivos nuevos: `tests/` completo, `conftest.py`, fixtures y datos de ejemplo.
- Dependencias nuevas (dev): `pytest`, `pytest-mock`, `pytest-cov`.
- Configuración: secciones `[tool.pytest.ini_options]` y `[tool.coverage]` en `pyproject.toml`.