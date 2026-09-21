# codebase-analysis Specification

## Purpose
TBD - created by archiving change fase-1-analisis-codigo. Update Purpose after archive.
## Requirements
### Requirement: Mapa de dependencias completo
El sistema SHALL producir un mapa de dependencias que liste, para cada módulo `.py` del paquete, los módulos del proyecto que importa y los que lo importan a él, de modo que se distinga el código vivo del código muerto.

#### Scenario: Solo main y api_movies se importan entre sí
- **WHEN** se ejecuta el análisis sobre el paquete `proyecto_refactoring/`
- **THEN** el mapa de dependencias indica que `main.py` importa `api_movies.py` y que ningún otro módulo del paquete es importado por otro

#### Scenario: Código muerto identificable
- **WHEN** un módulo no es importado por ningún otro módulo del proyecto
- **THEN** el mapa lo clasifica como candidato a código muerto con su nombre y ruta

### Requirement: Inventario de código muerto
El sistema SHALL listar todos los módulos no referenciados por ningún otro módulo, agrupados por categoría (configuración, gestión, utilidades), con recuento por categoría.

#### Scenario: Inventario de módulos de configuración
- **WHEN** se genera el inventario
- **THEN** se listan los 90 módulos `*_config.py` no importados y se indica que constituyen la categoría de configuración

#### Scenario: Inventario de módulos de gestión
- **WHEN** se genera el inventario
- **THEN** se listan los módulos `*_manager.py` no importados y se indica que constituyen la categoría de gestión

### Requirement: Reporte de duplicación de módulos
El sistema SHALL detectar y documentar grupos de módulos con la misma responsabilidad funcional, señalando el módulo recomendado a conservar en cada grupo.

#### Scenario: Duplicados de configuración
- **WHEN** se detecta que `config_manager.py` y `config_manager_v2.py` implementan la misma responsabilidad de gestión de configuración
- **THEN** el reporte los agrupa como duplicados y recomienda el módulo a conservar

#### Scenario: Duplicados de logging
- **WHEN** se detecta que `logger.py`, `log_manager.py` y `log_config.py` implementan la misma responsabilidad de registro
- **THEN** el reporte los agrupa como duplicados y recomienda un único módulo de logging

#### Scenario: Duplicado de aplicación principal
- **WHEN** se detecta que `app.py` y `main.py` duplican el punto de entrada de la aplicación
- **THEN** el reporte los agrupa como duplicados y recomienda `main.py` como punto de entrada único

### Requirement: Catálogo de malas prácticas en código vivo
El sistema SHALL catalogar las malas prácticas presentes en los módulos vivos (`main.py` y `api_movies.py`), incluyendo `bare except`, variables globales, wildcard imports y concatenación de strings.

#### Scenario: Bare except identificados
- **WHEN** se analiza `main.py`
- **THEN** se cuentan y localizan los bloques `except:` sin tipo de excepción especificado

#### Scenario: Variables globales identificadas
- **WHEN** se analiza `api_movies.py`
- **THEN** se listan las variables globales mutables y sus usos con `global`

#### Scenario: Wildcard import identificado
- **WHEN** se analiza `main.py`
- **THEN** se localiza el import `from api_movies import *`

### Requirement: Documento de análisis entregable
El sistema SHALL publicar todos los hallazgos anteriores en el documento `docs/analisis.md`, con estructura por secciones: dependencias, inventario, duplicados y malas prácticas.

#### Scenario: Documento generado
- **WHEN** el análisis está completo
- **THEN** existe `docs/analisis.md` en la raíz del proyecto con todas las secciones requeridas

