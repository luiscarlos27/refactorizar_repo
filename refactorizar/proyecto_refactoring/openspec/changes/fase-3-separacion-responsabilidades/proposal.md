## Why

El código vivo tras la fase 2 sigue concentrado en dos módulos con lógica mezclada: `api_movies.py` combina llamadas HTTP, lógica de negocio, estado global (favoritos, historial) y presentación indirecta; `main.py` mezcla UI, flujo de menú y reglas de negocio. Esta fase aplica separación de responsabilidades (SOLID) y bounded contexts a escala local: paquetes `api/`, `services/`, `models/`, `ui/`, `storage/` y `exceptions/`, con inyección de dependencias y estado encapsulado en cada capa. Es el paso estructural central del refactoring.

## What Changes

- Se crea `models/` con dataclasses de dominio: `Movie`, `Series`, con validación en `__post_init__`.
- Se crea `api/` con clientes HTTP dedicados: `omdb_client.py` y `tvmaze_client.py`, con contrato público claro y sin lógica de dominio.
- Se crea `services/` con casos de uso: `movie_service.py` y `series_service.py`.
- Se crea `storage/` con repositorios de favoritos, historial y caché, cada uno dueño exclusivo de sus datos.
- Se crea `ui/` con `menu.py` (navegación) y `display.py` (presentación pura, sin lógica de negocio).
- Se crea `exceptions/` con la jerarquía de excepciones de dominio (ampliada en fase 4).
- `main.py` queda como punto de entrada que compone las dependencias.
- Se elimina el estado global (`PELICULAS_FAVORITAS`, `HISTORIAL_BUSQUEDAS`, `CACHE_*`) en favor de instancias inyectadas.
- Se versionan los endpoints de API en `constants.py` (API versioning local).

## Capabilities

### New Capabilities
- `api-clients`: Clientes HTTP especializados por proveedor (OMDB, TVMaze) con contrato público estable.
- `domain-models`: Modelos de dominio tipados (Movie, Series) con validación.
- `service-layer`: Capa de casos de uso que orquesta clientes, modelos y almacenamiento.
- `ui-layer`: Presentación y navegación desacopladas de la lógica de negocio.
- `storage`: Persistencia de favoritos, historial y caché con propiedad exclusiva de datos.

### Modified Capabilities

## Impact

- Código afectado: reestructuración completa de `api_movies.py` y `main.py` en paquetes.
- Nuevos paquetes: `api/`, `services/`, `models/`, `ui/`, `storage/`, `exceptions/`.
- Se mantienen las APIs externas OMDB y TVMaze sin cambios de contrato.
- Dependencias nuevas: ninguna en esta fase (se inyectan manualmente).