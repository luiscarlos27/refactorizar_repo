## ADDED Requirements

### Requirement: Configuración única
El sistema SHALL proveer un único módulo `config.py` que concentre toda la configuración de la aplicación (URLs, timeouts, claves, flags), reemplazando a los módulos de configuración dispersos y no usados.

#### Scenario: Acceso a valores de configuración tipados
- **WHEN** el código solicita una clave de configuración
- **THEN** `config.py` devuelve el valor con su tipo correcto y un valor por defecto razonable si la clave no existe

#### Scenario: Eliminación de configs dispersos
- **WHEN** se completa la fase
- **THEN** los 90 módulos `*_config.py` y los managers de configuración duplicados ya no existen en el paquete

### Requirement: Centralización de constantes
El sistema SHALL centralizar en `constants.py` los valores hardcodeados de URLs, API keys, timeouts y nombres de archivo usados por la aplicación.

#### Scenario: URLs centralizadas
- **WHEN** un módulo necesita la URL base de OMDB o TVMaze
- **THEN** obtiene el valor de `constants.py` y no lo define inline

### Requirement: Imports específicos
El sistema SHALL reemplazar los wildcard imports por imports explícitos de los símbolos usados.

#### Scenario: Sin wildcard en main
- **WHEN** se compila `main.py`
- **THEN** ya no contiene `from api_movies import *` y solo importa los símbolos necesarios

### Requirement: Type hints en funciones vivas
El sistema SHALL añadir anotaciones de tipo completas a todas las funciones de `main.py` y `api_movies.py`, incluidos parámetros y retornos.

#### Scenario: Funciones tipadas
- **WHEN** se inspecciona cualquier función pública de `api_movies.py`
- **THEN** declara tipos para todos sus parámetros y su valor de retorno

### Requirement: F-strings sobre concatenación
El sistema SHALL sustituir la concatenación de strings por f-strings en todo el código vivo.

#### Scenario: Mensajes con f-strings
- **WHEN** el código construye un mensaje o URL con variables
- **THEN** usa f-strings en lugar de concatenación con `+`

### Requirement: Punto de entrada único
El sistema SHALL mantener `main.py` como único punto de entrada de la aplicación, eliminando el duplicado `app.py`.

#### Scenario: Eliminación de app.py
- **WHEN** se completa la fase
- **THEN** el archivo `app.py` no existe y toda la funcionalidad reside en `main.py` y sus módulos de soporte