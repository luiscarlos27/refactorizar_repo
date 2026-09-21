## 1. Constantes y configuración

- [x] 1.1 Crear `constants.py` con URLs base (OMDB/TVMaze), API key, timeouts y nombres de archivo
- [x] 1.2 Crear `config.py` con `AppConfig` (dataclass) y valores por defecto
- [x] 1.3 Añadir funciones de carga/validación en `config.py`

## 2. Refactorización de api_movies.py

- [x] 2.1 Sustituir constantes hardcodeadas por imports de `constants.py`
- [x] 2.2 Convertir concatenación de strings a f-strings
- [x] 2.3 Añadir type hints a todas las funciones
- [x] 2.4 Eliminar imports no usados

## 3. Refactorización de main.py

- [x] 3.1 Reemplazar `from api_movies import *` por imports específicos
- [x] 3.2 Convertir concatenación de strings a f-strings
- [x] 3.3 Añadir type hints a todas las funciones
- [x] 3.4 Unificar funcionalidad de `app.py` en `main.py`

## 4. Eliminación de código muerto y duplicados

- [x] 4.1 Eliminar `app.py`
- [x] 4.2 Eliminar los 88 módulos `*_config.py`
- [x] 4.3 Eliminar managers duplicados de configuración y logging (`config_manager.py`, `config_manager_v2.py`, `logger.py`, `log_manager.py`, `log_config.py`, y `cache_manager.py`/`cache_manager_v2.py` según inventario)
- [x] 4.4 Eliminar otros módulos muertos verificados en fase 1 (`utils.py` y demás, si no son usados)

## 5. Verificación

- [x] 5.1 Ejecutar `python -m compileall` sin errores
- [x] 5.2 Ejecutar `ruff check` sin errores bloqueantes
- [x] 5.3 Ejecutar `python main.py` y validar que el menú funciona