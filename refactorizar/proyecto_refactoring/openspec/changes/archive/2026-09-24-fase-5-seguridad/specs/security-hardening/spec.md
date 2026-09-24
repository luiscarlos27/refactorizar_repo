## ADDED Requirements

### Requirement: Secretos en variables de entorno
El sistema SHALL leer las claves de API y valores sensibles desde variables de entorno, con soporte de un archivo `.env` cargado por `python-dotenv`, y nunca hardcodearlos en el código fuente.

#### Scenario: Clave desde entorno
- **WHEN** la aplicación necesita la clave de OMDB
- **THEN** la obtiene de una variable de entorno; si no está definida, falla al arrancar con un mensaje claro (sin valores por defecto en el código)

#### Scenario: Sin claves en el código
- **WHEN** se busca en el código fuente por valores de API key
- **THEN** no aparecen claves literales hardcodeadas en los módulos del paquete

### Requirement: Plantilla de entorno
El sistema SHALL proveer un archivo `.env.example` con las variables de entorno requeridas, sus nombres y valores de ejemplo, sin secretos reales.

#### Scenario: Variables documentadas
- **WHEN** un desarrollador revisa `.env.example`
- **THEN** encuentra la lista de variables requeridas con comentarios de uso

### Requirement: Archivo .env excluido del control de versiones
El sistema SHALL excluir el archivo `.env` del control de versiones mediante `.gitignore`.

#### Scenario: .env no versionado
- **WHEN** se inspecciona `.gitignore`
- **THEN** contiene una entrada para `.env`