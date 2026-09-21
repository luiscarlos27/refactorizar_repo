## Why

El proyecto contiene claves hardcodeadas en el código fuente (`API_KEY_OMDB = "trilogy"` en `api_movies.py` y su equivalente en `config_manager_v2.py`) y no valida las entradas del usuario (títulos, géneros, nombres de archivo, opciones numéricas), lo que puede provocar errores inesperados, rutas inválidas o llamadas a API con payloads mal formados. Esta fase mueve los secretos a variables de entorno, elimina datos sensibles hardcodeados y añade validación de entrada por capa.

## What Changes

- Se mueven las claves de API a variables de entorno mediante `python-dotenv` (`.env` + `.env.example`).
- Se eliminan todos los valores sensibles hardcodeados del código.
- Se añade validación de entrada de usuario: títulos no vacíos, opciones numéricas válidas, nombres de archivo seguros.
- Se valida la configuración al cargarla (`config.py`), rechazando valores inválidos.
- Se evitan rutas peligrosas en exportación/importación de archivos (nombres sanitizados).

## Capabilities

### New Capabilities
- `security-hardening`: Secretos en variables de entorno y eliminación de datos sensibles hardcodeados.
- `input-validation`: Validación de entradas de usuario y de configuración por capa.

### Modified Capabilities

## Impact

- Código afectado: `config.py`, `constants.py`, clientes (`api/`), servicios, UI (`ui/menu.py`, `ui/display.py`), `main.py`.
- Dependencias nuevas: `python-dotenv`.
- Archivos nuevos: `.env.example` (`.env` queda en `.gitignore`).
- Sin cambios de contrato de las APIs externas.