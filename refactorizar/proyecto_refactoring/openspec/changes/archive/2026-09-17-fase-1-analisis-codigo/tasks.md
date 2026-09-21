## 1. Mapa de dependencias

- [x] 1.1 Ejecutar script de análisis de imports por módulo en `proyecto_refactoring/proyecto_refactoring/*.py`
- [x] 1.2 Registrar en `docs/analisis.md` el mapa completo: módulo → módulos importados y módulos que lo importan
- [x] 1.3 Verificar manualmente los módulos vivos `main.py` y `api_movies.py` y validar que coinciden con el mapa

## 2. Inventario de código muerto

- [x] 2.1 Listar módulos no importados por ningún otro, agrupados por categoría (config, manager, otros)
- [x] 2.2 Cuantificar por categoría (se espera: ~90 config, ~23 manager)
- [x] 2.3 Descartar falsos positivos: buscar `importlib`, `__import__` o referencias dinámicas antes de confirmar código muerto

## 3. Duplicación de módulos

- [x] 3.1 Documentar grupo `logger.py` / `log_manager.py` / `log_config.py` y recomendar módulo único
- [x] 3.2 Documentar grupo `config_manager.py` / `config_manager_v2.py` y recomendar módulo único
- [x] 3.3 Documentar grupo `app.py` / `main.py` y recomendar punto de entrada único
- [x] 3.4 Buscar otros grupos de duplicación por responsabilidad (no solo por nombre)

## 4. Catálogo de malas prácticas en código vivo

- [x] 4.1 Localizar y contar bloques `except:` sin excepción específica en `main.py`, `api_movies.py` y `utils.py`
- [x] 4.2 Listar variables globales mutables y usos con `global`
- [x] 4.3 Localizar wildcard imports y concatenación de strings
- [x] 4.4 Registrar hallazgos de strings hardcodeados y valores sensibles

## 5. Documento entregable

- [x] 5.1 Consolidar todo en `docs/analisis.md` con secciones: dependencias, inventario, duplicados, malas prácticas
- [x] 5.2 Revisar que `docs/analisis.md` incluye rutas y líneas de referencia para cada hallazgo