# logging Specification

## Purpose
Logging estructurado y trazable: registro de eventos con el módulo estándar `logging`, configuración centralizada y correlation ID por operación.
## Requirements
### Requirement: Logging con el módulo logging
El sistema SHALL registrar eventos mediante el módulo estándar `logging` con niveles apropiados (DEBUG, INFO, WARNING, ERROR), en lugar de `print()` de depuración.

#### Scenario: Registro de errores
- **WHEN** ocurre un error en un servicio
- **THEN** se registra con `logger.error(...)` incluyendo contexto del fallo

#### Scenario: Registro de eventos de negocio
- **WHEN** se completa una búsqueda
- **THEN** se registra con `logger.info(...)` el evento y su resultado

### Requirement: Configuración de logging centralizada
El sistema SHALL configurar el logging una única vez (handlers a consola y archivo, nivel configurable) desde un módulo de logging dedicado.

#### Scenario: Configuración única
- **WHEN** la aplicación arranca
- **THEN** se configura el logging una sola vez y todos los módulos usan loggers derivados de esa configuración

### Requirement: Correlation ID por operación
El sistema SHALL generar un identificador de correlación (correlation ID) al inicio de cada operación de búsqueda y propagarlo a los registros emitidos durante esa operación.

#### Scenario: Trazabilidad de una búsqueda
- **WHEN** se ejecuta una búsqueda de película
- **THEN** todos los registros asociados a esa operación incluyen el mismo correlation ID