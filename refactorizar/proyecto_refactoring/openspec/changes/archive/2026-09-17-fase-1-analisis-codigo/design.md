## Context

El paquete `proyecto_refactoring/proyecto_refactoring/` es una app CLI educativa de películas y series con malas prácticas intencionales. Contiene 118 archivos `.py` (~19.100 líneas). Análisis previo indica que solo `main.py` importa `api_movies.py`; los demás módulos (90 `*_config.py`, 23 `*_manager.py`, y otros como `app.py`, `utils.py`, `logger.py`) no son importados por ningún otro módulo. Este change formaliza ese conocimiento en un documento verificable.

## Goals / Non-Goals

**Goals:**
- Producir un mapa de dependencias verificado con herramientas (grep/scripts) y no solo lectura manual.
- Inventariar código muerto con criterios objetivos: módulo no importado por ningún otro.
- Documentar duplicaciones de responsabilidad y recomendar el módulo a conservar.
- Catalogar malas prácticas del código vivo como insumo para fases posteriores.

**Non-Goals:**
- No eliminar ningún archivo (eso ocurre en fases 2-3).
- No modificar código de la aplicación.
- No crear tests.
- No decidir aún la arquitectura destino final (fase 3).

## Decisions

- **Criterio de código muerto**: un módulo se clasifica como muerto si no es importado por ningún otro módulo del paquete, ignorando imports de librerías estándar/terceros y de sí mismo.
- **Herramienta de análisis**: se usa un script PowerShell/grep para detectar `import X` y `from X import` por módulo; se contrasta con lectura manual de los módulos clave (`main.py`, `api_movies.py`).
- **Grupos de duplicación**: se agrupan por responsabilidad funcional, no por nombre. Se recomienda conservar: `main.py` (entrada), `api_movies.py` (API), y un único módulo de config/logging aún por crear en fase 2.
- **Documento único**: todos los hallazgos se consolidan en `docs/analisis.md` en la raíz del proyecto para trazabilidad entre fases.

## Risks / Trade-offs

- [Análisis manual incompleto por volumen de archivos] → Verificación automatizada (script de imports) más lectura de los módulos vivos.
- [Código muerto que en realidad se usa dinámicamente (importlib, exec)] → Se busca además cualquier `__import__`, `importlib`, o referencia por nombre antes de clasificar como muerto.
- [`app.py` podría ser referencia esperada por evaluador] → Se documenta su relación con `main.py` y se deja la decisión de unificación a fase 2.

## Migration Plan

No aplica: esta fase no produce cambios en el código de la aplicación.

## Open Questions

- ¿Se debe conservar `app.py` como entrada alternativa por requisito del enunciado o puede unificarse en `main.py` en fase 2? (Se asume unificación, verificable en fase 2.)