## ADDED Requirements

### Requirement: Capa de servicios de películas
El sistema SHALL exponer `MovieService` en `services/movie_service.py` con los casos de uso de películas: buscar por título, buscar por actor, buscar por género, obtener populares, gestionar favoritos y consultar estadísticas.

#### Scenario: Búsqueda de película
- **WHEN** `MovieService.buscar_por_titulo(titulo)` es invocado
- **THEN** delega en el cliente OMDB, convierte a `Movie` y retorna el modelo

#### Scenario: Gestión de favoritos
- **WHEN** se agrega o elimina una película de favoritos a través del servicio
- **THEN** la operación se delega al repositorio de favoritos y retorna un resultado booleano

### Requirement: Capa de servicios de series
El sistema SHALL exponer `SeriesService` en `services/series_service.py` con los casos de uso de series: búsqueda por nombre y obtención de detalles.

#### Scenario: Búsqueda de series
- **WHEN** `SeriesService.buscar(nombre)` es invocado
- **THEN** delega en el cliente TVMaze y retorna la lista de series

#### Scenario: Detalles de serie
- **WHEN** `SeriesService.obtener_detalles(id)` es invocado
- **THEN** delega en el cliente TVMaze y retorna los detalles

### Requirement: Inyección de dependencias en servicios
El sistema SHALL construir los servicios con dependencias inyectadas (clientes HTTP y repositorios) en lugar de usar estado global.

#### Scenario: Servicio construido con dependencias
- **WHEN** se instancia `MovieService`
- **THEN** recibe por parámetros el cliente OMDB y los repositorios de favoritos/historial, sin leer variables globales