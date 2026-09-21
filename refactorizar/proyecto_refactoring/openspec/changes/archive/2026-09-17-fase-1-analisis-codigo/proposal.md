## Why

El proyecto `proyecto_refactoring/` contiene 118 archivos `.py` (~19.100 líneas), de los cuales la gran mayoría es código muerto o duplicado (90 `*_config.py`, 23 `*_manager.py`). Antes de reestructurar, es imprescindible conocer con exactitud qué módulos se usan realmente, qué dependencias existen y dónde están las malas prácticas. Sin este análisis, cualquier refactoring posterior eliminaría archivos con efectos imprevistos o mantendría duplicaciones por desconocimiento. Este change documenta el estado del código para que las fases 2-6 se ejecuten sobre un inventario verificado.

## What Changes

- Se genera un mapa de dependencias real entre módulos del proyecto.
- Se documenta un inventario completo de código muerto (módulos no importados por nadie).
- Se identifican duplicaciones de módulos (p. ej. `logger.py` vs `log_manager.py` vs `log_config.py`, `config_manager.py` vs `config_manager_v2.py`, `app.py` vs `main.py`).
- Se catalogan malas prácticas localizadas en el código vivo: `bare except`, variables globales, wildcard imports, strings hardcodeados, concatenación de strings.
- Se produce el documento `docs/analisis.md` con todos los hallazgos.

No se modifica código de la aplicación en esta fase; solo se documenta.

## Capabilities

### New Capabilities
- `codebase-analysis`: Inventario verificado del código: dependencias, código muerto, duplicados y malas prácticas, como base para las fases de refactoring.

### Modified Capabilities

## Impact

- Código afectado: ninguno (solo lectura). Análisis de los 118 archivos `.py` del paquete `proyecto_refactoring/`.
- Nuevo documento: `docs/analisis.md`.
- Sin cambios de dependencias ni de API.