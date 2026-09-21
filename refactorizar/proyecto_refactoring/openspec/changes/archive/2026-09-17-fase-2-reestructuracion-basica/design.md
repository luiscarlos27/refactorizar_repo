## Context

Tras la fase 1 sabemos que el código vivo se limita a `main.py` → `api_movies.py`. El resto del paquete (90 `*_config.py`, managers duplicados, `app.py`, `utils.py`, `logger.py`, `log_manager.py`, `log_config.py`, `cache_manager.py` vs `cache_manager_v2.py`) es código muerto o duplicado. Esta fase limpia y consolida el código vivo con estándares básicos, sin rediseñar la arquitectura (fase 3).

## Goals / Non-Goals

**Goals:**
- Reducir el paquete a un conjunto de módulos vivos y coherentes.
- Configuración única tipada con valores por defecto.
- Código vivo con type hints, f-strings e imports específicos.
- Mantener la app funcional (`python main.py`) al final de la fase.

**Non-Goals:**
- No separar responsabilidades en paquetes (fase 3).
- No implementar manejo de errores robusto ni logging estructurado (fase 4).
- No abordar seguridad de credenciales (fase 5).
- No crear tests (fase 6).

## Decisions

- **`config.py` basado en dicts tipados**: se modela la configuración con valores por defecto explícitos y funciones de acceso tipadas; se acepta un esquema simple (dataclass `AppConfig`) en lugar de replicar las plantillas de los 90 configs.
- **`constants.py` separado de `config.py`**: las constantes inmutables (URLs, API key, nombres de archivo) van en `constants.py`; lo que es editable en runtime va en `config.py`. Esto evita acoplar valores fijos con configuración dinámica.
- **Eliminación agresiva de código muerto**: se eliminan todos los `*_config.py` y duplicados de la fase 1; la app no los importa, por lo que el riesgo es mínimo. Cualquier dependencia encontrada se revisa antes de eliminar.
- **`api_movies.py` se mantiene como módulo de negocio funcional** durante esta fase; su división en clientes/servicios ocurre en fase 3.
- **Se conserva `utils.py` y `logger.py` solo si son usados por el código vivo**; en caso contrario se eliminan en esta fase.

## Risks / Trade-offs

- [Eliminar un config que la app usara indirectamente] → Antes de eliminar se verifica con el mapa de dependencias de fase 1 y una búsqueda de referencias por nombre.
- [`app.py` requerido por la evaluación académica] → Documentado en fase 1; se asume que el punto de entrada es `main.py` y se elimina `app.py`. Se puede revertir si la evaluación exige lo contrario.
- [Cambios masivos en `main.py`/`api_movies.py` rompen la app] → Se verifica `python main.py` al final y se mantienen las firmas de funciones de API para no romper la UI.

## Migration Plan

1. Crear `constants.py` y `config.py`.
2. Refactorizar `api_movies.py`: imports específicos, constants, f-strings, type hints.
3. Refactorizar `main.py`: imports específicos, f-strings, type hints, unificación de `app.py`.
4. Eliminar `app.py`, los `*_config.py` y duplicados.
5. Verificar `python main.py` y `ruff check`.
6. Rollback: restaurar archivos desde git (se recomienda commit previo).

## Open Questions

- ¿Se conserva `utils.py` (utilidades generales) o se integra su contenido útil en módulos de fase 3?