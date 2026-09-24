## ADDED Requirements

### Requirement: Timeouts explícitos en llamadas HTTP
El sistema SHALL configurar un timeout explícito y razonable en toda llamada HTTP a OMDB y TVMaze, tomado de la configuración.

#### Scenario: Timeout configurado
- **WHEN** un cliente HTTP realiza una petición
- **THEN** pasa un valor de timeout no nulo y configurable a `requests.get`

### Requirement: Reintentos con backoff
El sistema SHALL reintentar llamadas HTTP fallidas con backoff exponencial y un número máximo de intentos configurable.

#### Scenario: Reintento tras fallo transitorio
- **WHEN** una llamada HTTP falla por error transitorio
- **THEN** se reintenta hasta el máximo de intentos configurado con espera creciente entre intentos

#### Scenario: Sin reintento infinito
- **WHEN** se agotan los reintentos
- **THEN** se lanza `NetworkError` y no se siguen reintentando

### Requirement: Circuit breaker en llamadas externas
El sistema SHALL proteger las llamadas externas con un circuit breaker que abra tras un número de fallos consecutivos y permita medio abierto tras un periodo de espera.

#### Scenario: Circuito abierto
- **WHEN** se acumulan fallos consecutivos superiores al umbral
- **THEN** las llamadas posteriores fallan rápido sin intentar la red hasta que el circuito pase a medio abierto

### Requirement: Degradación elegante
El sistema SHALL degradar de forma controlada ante fallos de API: los servicios retornan `None` o valores por defecto y la UI muestra un mensaje amigable, sin que la aplicación termine con excepción no controlada.

#### Scenario: API caída sin crash
- **WHEN** la API de películas no responde
- **THEN** la búsqueda devuelve `None` y la UI muestra "No se pudo completar la búsqueda", y la aplicación continúa ejecutándose