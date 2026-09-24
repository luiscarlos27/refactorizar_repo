# input-validation Specification

## Purpose
Validación de entradas de usuario, de configuración y de nombres de archivo antes de procesarlas, rechazando valores inválidos con mensajes claros y sin efectos secundarios.
## Requirements
### Requirement: Validación de entradas de usuario
El sistema SHALL validar las entradas del usuario antes de procesarlas: textos no vacíos y acotados en longitud, opciones numéricas dentro de rangos válidos, y rechazo con mensaje claro de entradas inválidas.

#### Scenario: Título vacío rechazado
- **WHEN** el usuario ingresa un título de película vacío o solo espacios
- **THEN** el sistema muestra un mensaje de error y vuelve a solicitar la entrada sin llamar a la API

#### Scenario: Opción numérica fuera de rango
- **WHEN** el usuario ingresa un número de opción fuera del rango de la lista mostrada
- **THEN** el sistema muestra un mensaje de opción inválida y no accede a índices inexistentes

### Requirement: Validación de configuración
El sistema SHALL validar la configuración cargada (tipos y rangos de timeouts, intentos, tamaños) y rechazar configuraciones inválidas con `ConfigError`.

#### Scenario: Timeout inválido
- **WHEN** la configuración declara un timeout no numérico o negativo
- **THEN** se lanza `ConfigError` con un mensaje descriptivo

### Requirement: Nombres de archivo seguros
El sistema SHALL sanitizar y validar nombres de archivo para exportación/importación, impidiendo rutas con separadores o caracteres peligrosos.

#### Scenario: Nombre de archivo con ruta rechazado
- **WHEN** el usuario ingresa un nombre de archivo que contiene separadores de ruta
- **THEN** el sistema lo rechaza o lo sanitiza y no escribe fuera del directorio de datos
