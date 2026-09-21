## Context

El proyecto hardcodea la API key de OMDB (`"trilogy"`) en el código y no valida entradas del usuario, lo que genera errores en runtime y riesgo de rutas inseguras. Esta fase aplica hardening de secretos y validación por capa.

## Goals / Non-Goals

**Goals:**
- Cero secretos en el código fuente.
- `.env` + `.env.example` + `.gitignore`.
- Validación de entradas de usuario y de configuración.
- Nombres de archivo seguros en export/import.

**Non-Goals:**
- No implementar autenticación de usuarios.
- No cifrar datos en repositorios locales (fuera de alcance de una app CLI local).
- No crear tests (fase 6).

## Decisions

- **`python-dotenv`**: carga el `.env` en el arranque; los clientes leen `OMDB_API_KEY` desde el entorno con valor por defecto vacío si no existe (documentado como desarrollo).
- **Fallback de desarrollo**: se permite un valor por defecto solo de desarrollo (la demo key "trilogy") y solo si la variable no está definida, para no romper el flujo educativo; este fallback se elimina o se marca claramente como no apto para producción.
- **Validación de entrada en UI**: una función auxiliar de validación (`ui/validation.py` o dentro de `ui/menu.py`) reutilizable por las distintas opciones del menú.
- **Validación de config**: en `config.py` al cargar (tipos y rangos), lanzando `ConfigError` (fase 4).
- **Sanitización de archivos**: se permiten solo nombres base seguros (letras, números, `_`, `-`); se rechazan separadores de ruta.

## Risks / Trade-offs

- [Fallback de clave en código reintroduce secreto] → Se elimina o se limita a entorno de desarrollo con advertencia de log; se audita con `security-reviewer`.
- [Validación excesiva complica la UX] → Mensajes claros y re-solicitud; se valida lo mínimo necesario para seguridad.
- [Cambios en `.env` rompen la ejecución local] → `.env.example` documenta las variables; si falta la clave se muestra error claro, no crash silencioso.

## Migration Plan

1. Añadir `python-dotenv` y cargar entorno en el arranque.
2. Crear `.env.example` y actualizar `.gitignore`.
3. Mover la API key a variable de entorno y eliminar hardcodes.
4. Implementar validación de entrada de usuario en la UI.
5. Implementar validación de configuración en `config.py`.
6. Sanitizar nombres de archivo en repositorios.
7. Revisión de seguridad (skill `security-reviewer`).
8. Verificar `python main.py`, `ruff check`.
9. Rollback: git checkout de la fase previa.

## Open Questions

- ¿El fallback de desarrollo de la demo key "trilogy" se mantiene o se elimina por completo? (Se asume mantener solo si es indispensable para la evaluación académica.)