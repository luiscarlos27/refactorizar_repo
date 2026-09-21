## ADDED Requirements

### Requirement: Cliente HTTP por proveedor
El sistema SHALL exponer un cliente HTTP dedicado por proveedor externo: `OmdbClient` en `api/omdb_client.py` y `TvmazeClient` en `api/tvmaze_client.py`. Cada cliente SHALL encapsular las llamadas REST de su proveedor sin contener lógica de negocio.

#### Scenario: Búsqueda de película por título
- **WHEN** `OmdbClient.buscar_pelicula(titulo)` es invocado
- **THEN** retorna un diccionario con los datos de la película o `None` si OMDB responde `Response=False`

#### Scenario: Búsqueda de series
- **WHEN** `TvmazeClient.buscar_series(nombre)` es invocado
- **THEN** retorna la lista de resultados de TVMaze

#### Scenario: Detalles de serie
- **WHEN** `TvmazeClient.obtener_detalles(id_serie)` es invocado
- **THEN** retorna el diccionario con los detalles de la serie

### Requirement: Sin lógica de dominio en clientes
El sistema SHALL mantener los clientes HTTP libres de lógica de negocio: no gestionan favoritos, historial, estadísticas ni reglas de la aplicación.

#### Scenario: Cliente sin estado de dominio
- **WHEN** se inspecciona `api/omdb_client.py`
- **THEN** no contiene referencias a favoritos, historial ni variables globales de la aplicación

### Requirement: Versión de endpoints centralizada
El sistema SHALL declarar los endpoints y parámetros de API (URLs base, claves de versión) en `constants.py` y usarlos desde los clientes.

#### Scenario: URLs desde constants
- **WHEN** un cliente construye una URL
- **THEN** la compone a partir de constantes definidas en `constants.py`, sin strings hardcodeados inline