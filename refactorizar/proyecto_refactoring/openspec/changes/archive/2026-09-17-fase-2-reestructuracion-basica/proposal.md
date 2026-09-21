## Why

El código base acumula 90 módulos `*_config.py` (casi todos código muerto con la misma plantilla), constantes y strings hardcodeados dispersos, wildcard imports y concatenación de strings. Esta fase consolida la configuración en un único módulo, centraliza constantes, y aplica estándares básicos de calidad (type hints, f-strings, imports específicos) sobre el código vivo, sin reestructurar aún la arquitectura. Es el primer paso de mejora directa del código y reduce el riesgo de las fases 3-6.

## What Changes

- Se crea `config.py` único que reemplaza funcionalmente a los 90 `*_config.py`, con carga/validación y valores por defecto.
- Se crea `constants.py` para valores hardcodeados (URLs base, API key, timeouts, nombres de archivo).
- Se elimina el wildcard import `from api_movies import *` en `main.py` y se reemplaza por imports específicos.
- Se convierten concatenaciones de strings a f-strings en el código vivo.
- Se añaden type hints a las funciones de `main.py` y `api_movies.py`.
- Se unifica `app.py` en `main.py` (se elimina el duplicado).
- Se elimina código muerto de configuración que no aporta valor (los 90 `*_config.py` y duplicados de managers de configuración/logger según inventario de fase 1).

## Capabilities

### New Capabilities
- `config-management`: Configuración única, tipada y validada, que reemplaza los módulos de configuración dispersos.
- `code-quality`: Estándares básicos de calidad sobre el código vivo: type hints, f-strings, imports específicos, sin wildcard imports.

### Modified Capabilities

## Impact

- Código afectado: `main.py`, `api_movies.py`, `app.py` (eliminado), nuevos `config.py` y `constants.py`.
- Se eliminan los 90 `*_config.py` y duplicados de configuración/logging.
- Sin cambios en dependencias de terceros. Sin cambios de API pública externa.