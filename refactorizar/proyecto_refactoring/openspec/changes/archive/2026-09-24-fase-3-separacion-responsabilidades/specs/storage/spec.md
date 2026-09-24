## ADDED Requirements

### Requirement: Repositorios de datos de usuario
El sistema SHALL exponer repositorios en `storage/` para favoritos (`FavoritesRepository`) e historial (`HistoryRepository`), cada uno dueño exclusivo de su estado y persistencia.

#### Scenario: Favoritos en memoria
- **WHEN** se agrega y consulta una película favorita
- **THEN** el `FavoritesRepository` mantiene la lista y evita duplicados por título

#### Scenario: Historial con timestamps
- **WHEN** se registra una búsqueda
- **THEN** el `HistoryRepository` almacena título y timestamp, y permite limpiarlo

### Requirement: Caché encapsulada
El sistema SHALL encapsular el caché de respuestas de API en `storage/` (p. ej. `cache.py`), reemplazando las variables globales `CACHE_PELICULAS` y `CACHE_SERIES`.

#### Scenario: Caché con TTL
- **WHEN** se consulta una clave reciente
- **THEN** se devuelve el valor cacheado; si expiró, se elimina y se trata como ausente

#### Scenario: Sin estado global
- **WHEN** se completa la fase
- **THEN** no existen variables globales mutables de favoritos, historial ni caché en los módulos del paquete

### Requirement: Persistencia opcional en JSON
El sistema SHALL permitir exportar e importar favoritos e historial a JSON (funcionalidad existente de `exportar_a_json`/`importar_de_json`) desde los repositorios.

#### Scenario: Exportación de datos
- **WHEN** se invoca la exportación
- **THEN** se escribe un archivo JSON con favoritos e historial actuales

#### Scenario: Importación de datos
- **WHEN** se invoca la importación sobre un archivo JSON válido
- **THEN** los repositorios cargan favoritos e historial desde el archivo