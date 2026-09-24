## 1. Modelos de dominio

- [x] 1.1 Crear `models/__init__.py`, `models/movie.py` con dataclass `Movie` y validación
- [x] 1.2 Crear `models/series.py` con dataclass `Series` y validación
- [x] 1.3 Añadir classmethods de conversión desde respuestas OMDB/TVMaze

## 2. Clientes HTTP

- [x] 2.1 Crear `api/__init__.py` y `api/omdb_client.py` con `OmdbClient`
- [x] 2.2 Crear `api/tvmaze_client.py` con `TvmazeClient`
- [x] 2.3 Mover URLs/endpoints a `constants.py` y usarlos desde los clientes

## 3. Almacenamiento

- [x] 3.1 Crear `storage/__init__.py` y `storage/favorites_repository.py`
- [x] 3.2 Crear `storage/history_repository.py`
- [x] 3.3 Crear `storage/cache.py` con TTL, reemplazando `CACHE_PELICULAS`/`CACHE_SERIES`
- [x] 3.4 Implementar export/import JSON en repositorios

## 4. Servicios

- [x] 4.1 Crear `services/__init__.py` y `services/movie_service.py`
- [x] 4.2 Crear `services/series_service.py`
- [x] 4.3 Inyectar clientes y repositorios en los servicios

## 5. UI

- [x] 5.1 Crear `ui/__init__.py` y `ui/display.py` (solo renderizado)
- [x] 5.2 Crear `ui/menu.py` (navegación, delega en servicios)
- [x] 5.3 Crear `exceptions/__init__.py` con jerarquía base de excepciones

## 6. Composición y limpieza

- [x] 6.1 Reescribir `main.py` como composition root (clientes → repositorios → servicios → menú)
- [x] 6.2 Eliminar `api_movies.py` tras migrar todas sus funciones
- [x] 6.3 Eliminar módulos muertos restantes verificados en fase 1
- [x] 6.4 Verificar ausencia de variables globales mutables en el paquete

## 7. Verificación

- [x] 7.1 Ejecutar `python -m compileall` sin errores
- [x] 7.2 Ejecutar `ruff check` sin errores bloqueantes
- [x] 7.3 Ejecutar `python main.py` y validar búsquedas, favoritos, historial y export/import