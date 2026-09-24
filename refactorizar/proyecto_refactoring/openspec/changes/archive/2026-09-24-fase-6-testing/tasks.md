## 1. Configuración de herramientas

- [x] 1.1 Añadir `pytest`, `pytest-mock`, `pytest-cov` como dependencias dev en `pyproject.toml`
- [x] 1.2 Configurar `[tool.pytest.ini_options]` (testpaths, addopts) y `[tool.coverage]` (omit tests, fail_under=90)

## 2. Fixtures

- [x] 2.1 Crear `tests/conftest.py` con fixtures de clientes mockeados (OMDB, TVMaze)
- [x] 2.2 Crear fixtures de repositorios temporales (favoritos, historial, caché) con `tmp_path`
- [x] 2.3 Crear fixtures de modelos de ejemplo y respuestas fijas de APIs

## 3. Tests por capa

- [x] 3.1 Tests de modelos: creación, validación (`__post_init__`), conversión desde diccionarios
- [x] 3.2 Tests de clientes API: búsquedas, detalles, errores HTTP, timeout
- [x] 3.3 Tests de servicios: delegación, degradación ante `NetworkError`, gestión de favoritos/historial
- [x] 3.4 Tests de repositorios: agregar/eliminar/consultar, export/import JSON, TTL de caché
- [x] 3.5 Tests de validación de entrada y de configuración (`ConfigError`)
- [x] 3.6 Tests de UI: renderizado y flujo de menú (monkeypatch de `input`)

## 4. Cobertura y trazabilidad

- [x] 4.1 Traducir escenarios clave de specs de fases 1-5 a tests (búsquedas, degradación, validación, secretos)
- [x] 4.2 Ejecutar `pytest --cov --cov-fail-under=90` hasta obtener verde y coverage ≥ 90%
- [x] 4.3 Revisar reporte de coverage y añadir tests para ramas descubiertas

## 5. Verificación

- [x] 5.1 Ejecutar suite completa sin acceso a red (verificar que no se hacen llamadas reales)
- [x] 5.2 Ejecutar `ruff check` sin errores bloqueantes en tests y código
