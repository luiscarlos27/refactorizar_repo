# test-suite Specification

## Purpose
Suite de pruebas automatizada con pytest que cubre todas las capas del paquete sin acceso a red, con fixtures reutilizables y cobertura mínima del 90%.
## Requirements
### Requirement: Suite de tests con pytest
El sistema SHALL proveer una suite de pruebas ejecutable con `pytest` que cubra los módulos del paquete (modelos, clientes, servicios, repositorios, UI y configuración).

#### Scenario: Ejecución de la suite
- **WHEN** se ejecuta `pytest`
- **THEN** todos los tests pasan y no se requieren credenciales ni conexión a las APIs externas

### Requirement: Tests unitarios por capa
El sistema SHALL incluir tests unitarios para: modelos (creación, validación, conversión), repositorios (favoritos, historial, caché, export/import), servicios (delegación y degradación) y validación de entrada de usuario.

#### Scenario: Validación de modelos
- **WHEN** se crea una `Movie` con año fuera de rango
- **THEN** el test verifica que se lanza `ValueError`

#### Scenario: Servicio con API fallida
- **WHEN** el cliente OMDB lanza `NetworkError`
- **THEN** el test verifica que el servicio degrada (retorna `None`) sin propagar el error

### Requirement: Mocks de APIs externas
El sistema SHALL simular las respuestas de OMDB y TVMaze mediante `pytest-mock`, sin realizar llamadas reales a la red.

#### Scenario: OMDB mockeado
- **WHEN** se ejecuta un test de búsqueda de película
- **THEN** la llamada HTTP se simula con una respuesta fija y no se contacta a la red

#### Scenario: TVMaze mockeado
- **WHEN** se ejecuta un test de búsqueda de series
- **THEN** la llamada HTTP se simula con una respuesta fija y no se contacta a la red

### Requirement: Fixtures y datos de prueba
El sistema SHALL definir fixtures reutilizables en `tests/conftest.py` (clientes mockeados, repositorios temporales, modelos de ejemplo) y datos de prueba parametrizados.

#### Scenario: Repositorio temporal
- **WHEN** un test necesita un repositorio de favoritos
- **THEN** se usa una fixture que aísla el estado por test

### Requirement: Cobertura mínima
El sistema SHALL alcanzar una cobertura de código ≥ 90% medida con `pytest --cov`, excluyendo los tests mismos.

#### Scenario: Umbral de cobertura
- **WHEN** se ejecuta `pytest --cov --cov-fail-under=90`
- **THEN** la cobertura total es ≥ 90% y el comando termina con éxito

### Requirement: Escenarios por requirement de specs
El sistema SHALL traducir los escenarios WHEN/THEN de las specs de las fases 1-5 en casos de prueba automatizados, de modo que cada scenario especificado tenga un test asociado.

#### Scenario: Trazabilidad de scenarios
- **WHEN** se completa la fase
- **THEN** los escenarios clave de las specs (búsquedas, favoritos, degradación, validación, secretos) tienen tests correspondientes
