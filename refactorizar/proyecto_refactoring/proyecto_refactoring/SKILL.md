# SKILLS PARA OPENCODE

Las 3 skills del proyecto viven en el mismo directorio que la libreria de skills
instalada, con el formato valido de opencode: una carpeta por skill con su
`SKILL.md` (frontmatter `name` + `description`) y guias de detalle en
`references/`.

```text
refactorizar/opencode-skills/opencode-skills-main/.opencode/skills/
├── refactoring-code-smells/
│   ├── SKILL.md
│   └── references/
│       ├── deteccion.md          # smell -> comando de deteccion -> tecnica
│       └── quality-gate.md       # ruff + mypy --strict + pytest + compileall
├── api-integration-rest/
│   ├── SKILL.md
│   └── references/
│       ├── retry-y-breaker.md    # reintentable/no reintentable, backoff, breaker
│       └── errores-y-secretos.md # excepciones de dominio, claves, degradacion
└── pytest-testing-automation/
    ├── SKILL.md
    └── references/
        ├── fixtures-y-mocks.md   # yield, scopes, factories, mock de HTTP
        └── cobertura-y-ci.md     # umbral 90 %, informes, casos limite
```

## Los 3 skills

| Skill | Proposito | Triggers |
|---|---|---|
| `refactoring-code-smells` | Eliminar malas practicas (code smells), estado global y duplicacion, sin alterar el comportamiento; exige quality gate | "refactorizar codigo", "quitar variables globales", "limpiar code smells" |
| `api-integration-rest` | Clientes REST robustos en Python: timeouts, reintentos con backoff, circuit breaker, cache con TTL, excepciones de dominio | "conectar a una API", "crear cliente REST", "manejar reintentos HTTP" |
| `pytest-testing-automation` | Suites pytest con fixtures, parametrizacion, mock de APIs y cobertura >= 90 % | "crear tests unitarios", "mockear llamadas HTTP", "medir cobertura" |

## Formato valido de un skill

```text
.opencode/skills/nombre-skill/SKILL.md
```

```markdown
---
name: nombre-skill
description: Que hace y cuando usarlo, con los triggers literales primero.
---

# Titulo del skill

(instrucciones en markdown)
```

Reglas del formato (opencode escanea `**/SKILL.md` dentro de los directorios de
skills registrados):

- `name` es obligatorio, en minusculas con guiones, y debe coincidir con el
  nombre de la carpeta.
- `description` es efectivamente obligatorio: sin ella la skill no se muestra.
- `allowed-tools` **no** es un campo valido del frontmatter de skills en opencode
  (es sintaxis de otra herramienta). Las capacidades se controlan con
  `permission` en `opencode.json`, no en el skill.

## Como se cargan

Las skills se registran en `.opencode/opencode.json` del workspace:

```json
{
  "skills": {
    "paths": ["refactorizar/opencode-skills/opencode-skills-main/.opencode/skills"]
  }
}
```

1. opencode las detecta al iniciar (reiniciar tras cualquier cambio).
2. Se invocan con `/skill nombre-del-skill` o las activa el agente cuando el
   mensaje coincide con sus triggers.
3. Las skills instaladas de la libreria (66) conviven con estas 3 sin conflicto:
   los nombres no se repiten.

## Versionado

- El `.gitignore` del workspace excluye `.opencode/` en cualquier nivel, asi que
  las 3 skills propias se versionan mediante una cadena de excepciones en
  `.gitignore` (solo sus carpetas, no el resto de la libreria).
- Verificar con `git check-ignore -v <ruta>/SKILL.md`: sin salida significa que
  el archivo es versionable.
