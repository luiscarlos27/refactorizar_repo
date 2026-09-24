# domain-models Specification

## Purpose
Modelos de dominio tipados (dataclasses) con validación de invariantes y conversión desde los diccionarios crudos de cada API.
## Requirements
### Requirement: Modelos de dominio tipados
El sistema SHALL representar películas y series mediante dataclasses en `models/movie.py` y `models/series.py`, con campos tipados para los datos relevantes (título, año, rating, género, etc.).

#### Scenario: Creación de Movie
- **WHEN** se construye una `Movie` con datos de OMDB
- **THEN** los atributos tipados (title, year, rating, genre) quedan poblados y accesibles

#### Scenario: Creación de Series
- **WHEN** se construye una `Series` a partir de la respuesta de TVMaze
- **THEN** los atributos tipados (nombre, idioma, géneros, estado) quedan poblados y accesibles

### Requirement: Validación en modelos
El sistema SHALL validar invariantes básicos en los modelos mediante `__post_init__` (p. ej. año y rating dentro de rangos plausibles cuando estén presentes).

#### Scenario: Año inválido rechazado
- **WHEN** se crea una `Movie` con un año fuera de rango
- **THEN** se lanza `ValueError` indicando el año inválido

### Requirement: Conversión desde API
El sistema SHALL proveer métodos/classmethods para construir modelos a partir de los diccionarios crudos de cada API (OMDB y TVMaze).

#### Scenario: Conversión desde diccionario OMDB
- **WHEN** se invoca el classmethod de conversión con la respuesta de OMDB
- **THEN** produce una `Movie` con los campos mapeados correctamente
