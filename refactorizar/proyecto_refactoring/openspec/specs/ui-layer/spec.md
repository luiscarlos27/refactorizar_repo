# ui-layer Specification

## Purpose
Capa de UI desacoplada: módulos de navegación y renderizado sin lógica de negocio, con `main.py` como composition root.
## Requirements
### Requirement: Presentación desacoplada
El sistema SHALL exponer módulos de UI en `ui/` (`menu.py` para navegación y `display.py` para renderizado) que no contengan lógica de negocio.

#### Scenario: Display sin lógica de negocio
- **WHEN** se inspecciona `ui/display.py`
- **THEN** solo formatea y muestra datos recibidos como parámetros, sin llamar a clientes HTTP ni gestionar estado

#### Scenario: Menú que delega en servicios
- **WHEN** el usuario selecciona una opción del menú
- **THEN** el flujo de `ui/menu.py` invoca a los servicios inyectados y pasa los resultados a `display`

### Requirement: Entrada única de aplicación
El sistema SHALL mantener `main.py` como punto de entrada que construye y compone las dependencias (clientes, repositorios, servicios, menú).

#### Scenario: Composición en main
- **WHEN** se ejecuta `main.py`
- **THEN** instancia los clientes, repositorios y servicios, y arranca el menú con esas dependencias inyectadas
