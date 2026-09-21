## 1. Secretos en entorno

- [ ] 1.1 Añadir `python-dotenv` a `pyproject.toml`
- [ ] 1.2 Cargar variables de entorno al arrancar la aplicación
- [ ] 1.3 Crear `.env.example` con las variables requeridas documentadas
- [ ] 1.4 Añadir `.env` a `.gitignore`
- [ ] 1.5 Eliminar la API key hardcodeada del código y leerla de la variable de entorno
- [ ] 1.6 Verificar que no quedan claves literales en los módulos del paquete

## 2. Validación de entrada de usuario

- [ ] 2.1 Validar títulos de búsqueda (no vacíos, longitud máxima) y re-solicitar si es inválido
- [ ] 2.2 Validar opciones numéricas de menú y de listas (rango válido, sin accesos fuera de índice)
- [ ] 2.3 Sanitizar y validar nombres de archivo en export/import

## 3. Validación de configuración

- [ ] 3.1 Validar tipos y rangos de la configuración al cargar (`timeout`, `max_retries`, tamaños)
- [ ] 3.2 Lanzar `ConfigError` ante configuraciones inválidas con mensaje descriptivo

## 4. Revisión de seguridad

- [ ] 4.1 Ejecutar revisión de seguridad (skill `security-reviewer`) y corregir hallazgos
- [ ] 4.2 Verificar que no se registran secretos en logs

## 5. Verificación

- [ ] 5.1 Ejecutar `python -m compileall` sin errores
- [ ] 5.2 Ejecutar `ruff check` sin errores bloqueantes
- [ ] 5.3 Ejecutar `python main.py` y validar flujos con entrada inválida y sin clave configurada