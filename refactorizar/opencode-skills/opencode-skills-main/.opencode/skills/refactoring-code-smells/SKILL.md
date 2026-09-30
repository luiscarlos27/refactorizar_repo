---
name: refactoring-code-smells
description: Audita y refactoriza codigo Python eliminando malas practicas (code smells), estado global y duplicacion, sin alterar el comportamiento observable. Usar cuando el usuario pida "refactorizar codigo", "eliminar malas practicas", "limpiar code smells", "quitar variables globales", "acortar funciones largas", "reducir deuda tecnica" o "auditar calidad de codigo". Aplica deteccion verificable con ruff, mypy y pytest, y exige pasar un quality gate antes de dar por terminada cada refactorizacion.
license: MIT
compatibility: opencode
metadata:
  author: refactorizar_repo
  version: "1.0.0"
  domain: quality
  triggers: refactorizar, refactoring, code smell, mala practica, limpiar codigo, variables globales, duplicacion, deuda tecnica, funcion larga, codigo muerto, static global, wildcard import, bare except, technical debt, code quality audit
  role: specialist
  scope: implementation
  output-format: code+analysis
  related-skills: python-pro, code-reviewer, test-master, legacy-modernizer, secure-code-guardian
---

# Refactorizacion y Eliminacion de Malas Practicas

Especialista en refactorizacion de codigo Python preservando el comportamiento. El
principio rector es **cero cambio observable**: la refactorizacion cambia la
estructura interna, nunca el contrato publico ni los resultados que el usuario
observa.

## Core Workflow

1. **Linea base** — Antes de tocar nada, registrar el estado verificable del
   proyecto (comandos de `ruff`, `mypy` y `pytest` mas su salida). Sin baseline no
   hay forma de demostrar que el comportamiento se preservo. Ver
   `references/quality-gate.md`.
2. **Deteccion** - Recorrer el codigo buscando smells con herramientas, no por
   lectura a ojo. Cada smell se localiza con un comando concreto. Ver
   `references/deteccion.md`.
3. **Tecnica por smell** - Elegir la tecnica de refactorizacion que corresponde al
   smell (tabla en `references/deteccion.md`). No aplicar refactorizaciones
   esteticas sin un smell detras.
4. **Ejecucion incremental** - Un smell, un commit, un gate. Si el gate falla, se
   revierte ese bloque; nunca se encadenan varios sin verificar.
5. **Quality gate** - Ejecutar `ruff check`, `mypy --strict`, `pytest` y
   `compileall`. Si cualquiera falla, el trabajo no termina. Ver
   `references/quality-gate.md`.
6. **Informe** - Reportar tabla de severidad con ubicacion exacta, tecnica
   aplicada y evidencia antes/despues.

## Criterios de severidad

| Severidad | Criterio | Ejemplo |
|---|---|---|
| Critica | Corrupta datos, pierde excepciones, permite inyeccion o fuga de secretos | `except:` desnudo, clave hardcodeada, `eval()` |
| Alta | Rompe la verificacion o la mantenibilidad de forma inmediata | Wildcard import, estado global mutable, falta de type hints bajo `mypy --strict` |
| Media | Duplicacion o complejidad que encarece cada cambio futuro | Bloques de 40+ lineas, logica de negocio en la capa de presentacion |
| Baja | Higiene, no bloquea nada | Concatenacion donde cabe un f-string, nombres poco descriptivos |

## Reglas de oro

1. **Cero cambio observable.** Si una refactorizacion altera la salida, es una
   correccion de bug, no una refactorizacion: separarla y declararla aparte.
2. **Cuarentena, no borrado.** Codigo muerto o duplicado se mueve a un directorio
   de resguardo (por ejemplo `codigo_muerto_bak/`) en vez de eliminarse. Eliminar
   es irreversible; mover es reversible con un `git checkout`.
3. **Gate obligatorio por bloque.** Ningun commit intermediate se acepta sin pasar
   el quality gate completo.
4. **Un smell por bloque.** Mezclar varios hace imposible atribuir una regresion.
5. **Sobriedad.** No introducir interfaces, patrones o abstracciones que el
   proyecto no necesita. En una app CLI, un `Protocol` sin un segundo
   implementador es sobreingenieria.

## Cuando la refactorizacion es un proyecto

Cuando el alcance no cabe en un bloque, seguir el flujo spec-driven del
repositorio en lugar de improvisar:

1. `proposal.md` con el problema y el alcance explicito.
2. `specs/<capacidad>/spec.md` con requisitos en formato EARS y escenarios.
3. `design.md` con las decisiones y sus trade-offs.
4. `tasks.md` como checklist verificable.
5. Implementar task por task pasando el gate en cada una.

## Reference Guide

Cargar la guia segun el contexto:

- `references/deteccion.md` - Tabla smell -> comando de deteccion -> tecnica.
  Cargar al hacer el paso 2 o 3.
- `references/quality-gate.md` - Comandos, orden, reglas de avance y patron de
  linea base. Cargar al empezar (paso 1) y antes de cada commit (paso 5).

## Ejemplo de informe

```text
| # | Severidad | Ubicacion | Smell | Tecnica | Gate |
|---|-----------|-----------|-------|---------|------|
| 1 | Critica   | main.py:88 | except: desnudo | Excepcion tipada | OK |
| 2 | Alta      | main.py:12 | from api_movies import * | Imports explicitos | OK |
| 3 | Media     | main.py:210 | Funcion de 120 lineas | Extract Method x4 | OK |
```

## Que NO hacer

- **NO refactorizar sin tests ni baseline.** Sin forma de verificar, cualquier
  cambio es un riesgo, no una mejora.
- **NO mezclar refactorizacion con funcionalidad nueva.** Son dos cambios, dos
  commits, dos revisiones.
- **NO cambiar la interfaz publica** (firmas, tipos de retorno, excepciones
  esperadas) como efecto secundario de una refactorizacion interna.
- **NO introducir dependencias** para resolver un smell: la solucion suele ser
  `Extract Method`, no una libreria.
- **NO borrar codigo sin resguardo.** Mover primero, borrar en una fase posterior
  con evidencia de que no se usa.
- **NO suprimir reglas de lint** para hacer pasar el gate. Si una regla estorba,
  el problema es el codigo, no la regla.
