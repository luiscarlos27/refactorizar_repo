## 1. Excepciones

- [x] 1.1 Definir `AppError` base y subclases (`ApiClientError`, `MovieNotFoundError`, `SeriesNotFoundError`, `NetworkError`, `ConfigError`) en `exceptions/`
- [x] 1.2 Traducir excepciones de `requests` a `NetworkError`/`ApiClientError` en los clientes

## 2. Logging

- [x] 2.1 Crear módulo de configuración de logging (handlers consola + archivo, nivel configurable)
- [x] 2.2 Sustituir `print()` de depuración por `logging` en todo el paquete
- [x] 2.3 Implementar correlation ID por operación de búsqueda y propagarlo a los registros

## 3. Resiliencia en clientes HTTP

- [x] 3.1 Añadir timeouts explícitos y configurables a todas las llamadas HTTP
- [x] 3.2 Añadir reintentos con backoff exponencial (`tenacity`) y máximo de intentos configurable
- [x] 3.3 Añadir circuit breaker (`pybreaker`) a los clientes (fail_max y reset_timeout configurables)
- [x] 3.4 Asegurar que al agotarse reintentos se lanza `NetworkError`

## 4. Degradación elegante

- [x] 4.1 Hacer que los servicios retornen `None`/`[]` ante fallos de API
- [x] 4.2 Capturar `AppError` en la UI y mostrar mensajes amigables sin crash
- [x] 4.3 Verificar que la app continúa tras un fallo de red simulado

## 5. Limpieza

- [x] 5.1 Eliminar todos los `bare except:` del paquete
- [x] 5.2 Eliminar los `print()` de depuración restantes
- [x] 5.3 Declarar `tenacity` y `pybreaker` en `pyproject.toml`

## 6. Verificación

- [x] 6.1 Ejecutar `python -m compileall` sin errores
- [x] 6.2 Ejecutar `ruff check` sin errores bloqueantes
- [x] 6.3 Ejecutar `python main.py` y validar flujos normales y con API simulada caída