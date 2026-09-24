## Context

Tras la fase 2, el código vivo es `main.py` → `api_movies.py`, con estado global (`PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_*`) y lógica de negocio mezclada con presentación. Esta fase aplica separación de responsabilidades y bounded contexts a escala local: cada capa dueña de sus datos y responsabilidades, con inyección de dependencias.

## Goals / Non-Goals

**Goals:**
- Estructura de paquetes clara: `models/`, `api/`, `services/`, `storage/`, `ui/`, `exceptions/`.
- Eliminar variables globales mutables.
- Inyección de dependencias desde `main.py`.
- Aplicar principios SOLID (SRP, DIP, OCP en clientes) y DDD local (bounded contexts, entidades de dominio).
- Mantener la funcionalidad de la app sin cambios de comportamiento visible.

**Non-Goals:**
- No implementar manejo de errores robusto (fase 4).
- No abordar seguridad de credenciales (fase 5).
- No crear tests (fase 6).
- No introducir async/async HTTP (se mantiene `requests` síncrono).
- No implementar resiliencia (retries/circuit breaker) — fase 4.

## Decisions

- **Patrón de repositorio**: `FavoritesRepository` y `HistoryRepository` encapsulan estado + persistencia JSON, cumpliendo "cada contexto dueño de sus datos".
- **Clientes HTTP como clases con responsabilidad única**: `OmdbClient` y `TvmazeClient` reciben configuración (URLs/timeout) por inyección; su contrato público devuelve datos crudos o modelos según corresponda.
- **Modelos de dominio**: dataclasses `Movie` y `Series` con validación en `__post_init__` y classmethods de conversión desde las respuestas de API.
- **Servicios como orquestadores**: `MovieService` y `SeriesService` coordinan clientes, modelos y repositorios; sin conocer la UI.
- **UI como consumidora**: `menu.py` y `display.py` reciben servicios inyectados; `display` solo formatea.
- **Composición en `main.py`**: único lugar donde se construyen las dependencias concretas (composition root).
- **Excepciones de dominio**: jerarquía base en `exceptions/` (ampliada en fase 4): `MovieNotFoundError`, `SeriesNotFoundError`, `ApiClientError`.

## Risks / Trade-offs

- [Cambio estructural grande rompe funcionalidad] → Migración incremental por funcionalidad (buscar, favoritos, historial, export/import) con verificación manual tras cada bloque.
- [Sobreingeniería para una app CLI] → Se limita el diseño a lo necesario (sin interfaces abstractas forzadas); los protocolos se introducen solo si la inyección de dependencias lo requiere.
- [Pérdida de comportamiento en conversión a modelos] → Los modelos conservan los campos que la UI utiliza (Title/Year/imdbRating/Genre/... y show/name/...).
- [Módulos muertos restantes de fases previas] → Se eliminan al consolidar la estructura, verificando dependencias.

## Migration Plan

1. Crear paquetes y modelos (`models/`).
2. Migrar clientes HTTP (`api/`).
3. Migrar repositorios y caché (`storage/`).
4. Migrar servicios (`services/`).
5. Migrar UI (`ui/`).
6. Reescribir `main.py` como composition root.
7. Eliminar `api_movies.py` y cualquier módulo muerto restante.
8. Verificar `python main.py` y `ruff check`.
9. Rollback: git checkout de la fase previa.

## Open Questions

- ¿Se preserva `api_movies.py` como capa de compatibilidad o se elimina por completo? (Se asume eliminación al completar la migración de todas sus funciones.)