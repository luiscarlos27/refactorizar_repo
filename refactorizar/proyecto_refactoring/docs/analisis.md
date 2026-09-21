# Análisis del Código — Fase 1

> Documento resultante del change OpenSpec `fase-1-analisis-codigo` (capability `codebase-analysis`).
> Fecha: 2026-09-17. Alcance: paquete `proyecto_refactoring/` (118 archivos `.py`, ~19.122 líneas).

---

## 1. Mapa de dependencias

Análisis de imports entre módulos del propio paquete (excluyendo librerías estándar y de terceros).

### Resultado

| Módulo | Importa de | Es importado por |
|---|---|---|
| `main.py` | `api_movies.py` (wildcard `from api_movies import *`) | — |
| `api_movies.py` | — | `main.py` |
| Resto (116 módulos) | — | — |

### Conclusión

- **Código vivo**: solo `main.py` y `api_movies.py` forman la cadena ejecutable.
- **Código muerto**: los 116 módulos restantes no son importados por ningún otro módulo del paquete.

### Verificación de falsos positivos

- No se encontraron imports dinámicos (`importlib`, `__import__`, `import_string`, `pkgutil`) en ningún módulo.
- No se encontraron referencias por nombre a módulos del paquete.
- Conclusión: la clasificación de código muerto es fiable.

---

## 2. Inventario de código muerto

Todos los módulos listados a continuación **no son importados por ningún otro módulo** del paquete.

### 2.1 Categoría configuración — 88 archivos `*_config.py` (13.358 líneas)

Subgrupos:

- `api_cache_*_config.py` (47 archivos): caché de API por temática (alerting, analytics, architecture, best_practices, cleanup, collaboration, compliance, compression, debug, deprecation, deprecation_schedule, disaster_recovery, distribution, documentation, evolution, failover, future, governance, innovation, integration, intelligence, invalidation, legacy, lifecycle, load_testing, mentoring, metrics, migration, migration_schedule, monitoring, observability, performance, performance_testing, preloading, recommendations, recovery, reporting, resilience_testing, scalability, security, security_testing, serialization, stress_testing, testing, training, validation, warming).
- Otros `api_*_config.py` (18 archivos): auth, bulkhead, caching_strategy, circuit_breaker, config, debug, degradation, error_handling, failover, logging, monitoring, performance, rate_limiter, rate_limit, retry, security, testing, timeout, timeout_retry.
- Config generales (23 archivos): accessibility, backup, cache, cache_expiry, database, debug, display, email, language, log, maintenance, network, notification, performance, privacy, proxy, search, security, storage, theme, ui.

### 2.2 Categoría gestión — 23 archivos `*_manager.py` (4.130 líneas)

`audit_manager`, `backup_manager`, `cache_manager`, `config_manager`, `data_manager`, `error_manager`, `export_manager`, `favorites_manager`, `feature_manager`, `history_manager`, `log_manager`, `metadata_manager`, `notification_manager`, `permission_manager`, `plugin_manager`, `report_manager`, `schedule_manager`, `settings_manager`, `state_manager`, `stats_manager`, `tag_manager`, `user_manager`, `version_manager`.

### 2.3 Otros módulos muertos — 5 archivos (807 líneas)

- `app.py` (255 líneas): variante duplicada del punto de entrada.
- `utils.py` (278 líneas): utilidades generales no usadas.
- `logger.py` (137 líneas): logging no usado.
- `cache_manager_v2.py`: duplicado de `cache_manager.py`.
- `config_manager_v2.py`: duplicado de `config_manager.py`.

### Resumen

| Categoría | Archivos | Líneas |
|---|---|---|
| Configuración (`*_config.py`) | 88 | 13.358 |
| Gestión (`*_manager.py`) | 23 | 4.130 |
| Otros muertos | 5 | 807 |
| **Código muerto total** | **116** | **18.295** |
| Código vivo (`main.py` + `api_movies.py`) | 2 | 521 |
| **Total paquete** | **118** | **19.122** |

> El 96 % de las líneas del paquete corresponde a código muerto o duplicado.

---

## 3. Duplicación de módulos

Grupos detectados por responsabilidad funcional (no por nombre):

| Grupo | Módulos | Responsabilidad | Recomendación |
|---|---|---|---|
| Logging | `logger.py`, `log_manager.py`, `log_config.py` | Registro de eventos | Conservar un único módulo (a crear en fase 4 con el módulo `logging`) |
| Configuración | `config_manager.py`, `config_manager_v2.py` | Gestión de configuración | Conservar uno solo (se sustituirá por `config.py` en fase 2) |
| Caché | `cache_manager.py`, `cache_manager_v2.py` | Caché de respuestas | Conservar uno solo (se encapsulará en `storage/` en fase 3) |
| Punto de entrada | `app.py`, `main.py` | Arranque de la aplicación | Conservar `main.py` como entrada única |
| Favoritos | `favorites_manager.py` vs funciones en `api_movies.py` (`agregar_a_favoritas`, `eliminar_de_favoritas`) | Gestión de favoritos | Consolidar en repositorio (fase 3) |
| Historial | `history_manager.py` vs `agregar_al_historial`, `limpiar_historial` en `api_movies.py` | Historial de búsquedas | Consolidar en repositorio (fase 3) |
| Estadísticas | `stats_manager.py` vs `obtener_estadisticas` en `api_movies.py` | Estadísticas | Consolidar en servicio (fase 3) |

---

## 4. Catálogo de malas prácticas en código vivo

Métricas por módulo (líneas, `bare except`, sentencias `global`, wildcard imports, concatenación de strings, `print()`):

| Módulo | Líneas | `except:` | `global` | Wildcard | Concatenación | `print()` |
|---|---|---|---|---|---|---|
| `main.py` | 334 | 10 | 0 | 1 | 31 | 73 |
| `api_movies.py` | 187 | 0 | 7 | 0 | 10 | 5 |
| `app.py` (muerto) | 255 | 0 | 2 | 0 | 22 | 40 |
| `utils.py` (muerto) | 278 | 13 | 0 | 0 | 25 | 7 |
| `logger.py` (muerto) | 137 | 0 | 0 | 0 | 5 | 1 |

### 4.1 Bare except en código vivo

- `main.py`: 10 bloques `except:` sin excepción específica (p. ej. en `mostrar_pelicula`, `funcion_importar`).
- `utils.py` (muerto): 13 bloques.

### 4.2 Variables globales en código vivo

- `api_movies.py` (7 sentencias `global`): `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_PELICULAS`, `CACHE_SERIES`.
- Variables globales definidas: `API_KEY_OMDB`, `API_KEY_TMDB`, `BASE_URL_OMDB`, `BASE_URL_TMDB`, `BASE_URL_TVMAZE`, `USUARIO_LOGUEADO`, `PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_PELICULAS`, `CACHE_SERIES`, `CONFIG`.

### 4.3 Wildcard imports

- `main.py`: `from api_movies import *` (línea 7).

### 4.4 Strings hardcodeados

- `API_KEY_OMDB = "trilogy"` (demo key) hardcodeada en `api_movies.py` y `app.py`.
- URLs base hardcodeadas en `api_movies.py`.
- `"fecha": "hoy"` hardcodeado en `agregar_al_historial`.

### 4.5 Concatenación de strings

- `main.py`: 31 casos; `api_movies.py`: 10 casos; 42 en total en código vivo.

### 4.6 Otros hallazgos

- Sin tests automatizados (0 archivos `test_*` / `tests/`).
- Sin `pyproject.toml`; `requirements.txt` con solo `requests` y `json5`.
- Sin control de versiones (sin repo git inicializado).
- Múltiples implementaciones del mismo concepto sin importar (`logger`/`log_manager`/`log_config`).
- `time.sleep` artificial en `main.py` (`delay(1)`) para simular carga.

---

## 5. Secciones por fase y acciones sugeridas

| Hallazgo | Fase | Acción |
|---|---|---|
| Código muerto (116 módulos) | F2 | Eliminar `*_config.py`, managers muertos, `app.py`, `utils.py` |
| Configuración dispersa | F2 | Crear `config.py` + `constants.py` |
| Wildcard import, concatenación, sin type hints | F2 | Imports específicos, f-strings, type hints |
| Lógica mezclada (API + negocio + presentación) | F3 | Paquetes `api/`, `services/`, `models/`, `ui/`, `storage/` |
| Globals de favoritos/historial/caché | F3 | Repositorios con inyección de dependencias |
| Bare except, sin logging estructurado | F4 | Jerarquía de excepciones + módulo `logging` |
| Sin resiliencia en llamadas HTTP | F4 | Timeout + retries + circuit breaker |
| API key hardcodeada, sin validación de entrada | F5 | `.env` + validación |
| Sin tests | F6 | Suite pytest con cobertura ≥ 90 % |