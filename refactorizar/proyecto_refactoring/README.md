# Proyecto de Refactoring - Películas y Series

Aplicación CLI de películas y series que conecta a APIs públicas (OMDB y TVMaze) sin requerir API keys de registro.

## Estado

Proyecto educativo en proceso de refactoring dirigido por **OpenSpec** (flujo `spec-driven`).
Fases completadas: 1 (análisis) y 2 (reestructuración básica).

## Estructura actual

```
proyecto_refactoring/
├── main.py          # Punto de entrada (composición de dependencias)
├── api_movies.py    # Acceso a APIs OMDB y TVMaze
├── config.py        # Configuración única (dataclass AppConfig)
├── constants.py     # Constantes centralizadas (URLs, timeouts, API key)
├── pyproject.toml   # Dependencias y config de herramientas (ruff, mypy, pytest)
├── requirements.txt # Dependencias base
├── openspec/        # Especificaciones del refactoring (OpenSpec)
├── docs/            # Documentación del análisis
└── codigo_muerto_bak/  # Backup de los 116 módulos eliminados en la fase 2
```

## Cómo Ejecutar

```bash
python main.py
```

## Herramientas de calidad

```bash
ruff check .          # Lint
mypy --strict .       # Type checking
pytest                # Tests (fase 6)
```

## Mejoras aplicadas (fase 2)

- **Configuración única**: 88 módulos `*_config.py` reemplazados por `config.py` (dataclass con validación).
- **Constantes centralizadas**: URLs y valores hardcodeados en `constants.py`.
- **Imports específicos**: eliminado `from api_movies import *`.
- **Type hints completos** en todo el código vivo (`mypy --strict` limpio).
- **F-strings** en lugar de concatenación.
- **Código muerto eliminado**: 116 módulos movidos a `codigo_muerto_bak/` (96 % de las líneas del proyecto original).

## Fases del refactoring (OpenSpec)

| Fase | Change | Estado |
|---|---|---|
| 1 | `fase-1-analisis-codigo` | Archivado |
| 2 | `fase-2-reestructuracion-basica` | Archivado |
| 3 | `fase-3-separacion-responsabilidades` | Archivado |
| 4 | `fase-4-manejo-errores` | Archivado |
| 5 | `fase-5-seguridad` | Archivado |
| 6 | `fase-6-testing` | Archivado |