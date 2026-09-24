# error-handling Specification

## Purpose
Manejo de errores robusto y consistente: jerarquía de excepciones de dominio, eliminación de `bare except` y traducción de errores de red a excepciones propias.
## Requirements
### Requirement: Jerarquía de excepciones de dominio
El sistema SHALL definir en `exceptions/` una jerarquía de excepciones con una base común `AppError` y subclases específicas: `ApiClientError`, `MovieNotFoundError`, `SeriesNotFoundError`, `NetworkError`, `ConfigError`.

#### Scenario: Excepción base compartida
- **WHEN** el código captura errores de la aplicación
- **THEN** puede capturar `AppError` para cubrir todas las subclases de dominio

#### Scenario: Errores específicos por dominio
- **WHEN** una película no se encuentra
- **THEN** se lanza `MovieNotFoundError`; cuando una serie no se encuentra, se lanza `SeriesNotFoundError`

### Requirement: Reemplazo de bare except
El sistema SHALL eliminar todos los bloques `except:` sin tipo de excepción y reemplazarlos por capturas de excepciones específicas.

#### Scenario: Sin bare except en el paquete
- **WHEN** se analiza el paquete
- **THEN** no existen bloques `except:` sin excepción especificada

### Requirement: Manejo de errores de red
El sistema SHALL lanzar `NetworkError` (o subclase de `ApiClientError`) cuando una llamada HTTP falla por tiempo o conectividad, en lugar de dejar propagar excepciones de la librería HTTP.

#### Scenario: Fallo de red identificable
- **WHEN** un cliente HTTP sufre `requests.exceptions.Timeout` o `requests.exceptions.ConnectionError`
- **THEN** se traduce a `NetworkError` antes de propagarse a la capa de servicio