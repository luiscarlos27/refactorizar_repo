# Deteccion de Code Smells

Cada smell se localiza con un comando verificable. No se documenta un smell que
no se pueda detectar de forma reproducible.

## Tabla smell -> deteccion -> tecnica

| Smell | Deteccion | Tecnica de refactorizacion |
|---|---|---|
| `except:` desnudo | `ruff check --select E722` | Reemplazar por la excepcion concreta; propagar el resto |
| Captura de excepcion sin usar | `ruff check --select F841` + revision de `except X:` vacio | Eliminar el `try` o registrar la excepcion |
| Wildcard import | `ruff check --select F403,F405` | Imports explicos, uno por simbolo |
| Simbolo importado sin usar | `ruff check --select F401` | Eliminar el import |
| Concatenacion de strings | `ruff check --select UP032` | f-strings |
| Formateo `%` o `.format()` | `ruff check --select UP031` | f-strings |
| `isinstance(x, bool)` sobre un `int` | `ruff check --select E712,E711` | Comparacion con `True` / `is None` |
| Comparacion con `None` usando `==` | `ruff check --select E711` | `is None` |
| Condicional anidado profundo | `ruff check --select SIM102,SIM108` | `Extract Method` + caso temprano |
| Mutable por defecto en argumento | `ruff check --select B006` | `None` como sentinel y creacion interna |
| Blucle con `if` sobre `continue` | `ruff check --select SIM` | Reestructurar el bucle |
| Falta de type hints | `mypy --strict .` | Anotar firmas y retornos |
| Any implicito en frontera | `mypy --strict .` (error `no-untyped-def`) | Anotar explicito, `cast` solo tras validar |
| Imports sin ordenar | `ruff check --select I` | Ordenar imports |
| Uso de `print` en logica | Busqueda de `print(` fuera de `ui/` | `logging` con modulo y nivel |
| Variable global mutable | Busqueda de `^global ` y de asignaciones a nivel de modulo | Encapsular en clase o repositorio, inyectar |
| Literal de URL o host en codigo | Busqueda de `http` en `.py` | Constante en `constants.py` |
| Secreto o clave hardcodeada | Busqueda de `api_key`, `token`, `password`, `secret` | Variable de entorno + `.env` en `.gitignore` |
| Codigo muerto o duplicado | Modulos no alcanzables desde el composition root | Mover a directorio de resguardo |

## Detecciones que ruff no cubre

Ruff no comprueba estado global ni literales sospechosos. Complementar siempre
con busqueda textual y con el grafo de dependencias:

```bash
# Estado global
grep -rn "^global \|^[A-Z_]\{3,\} *[:=]" --include="*.py" .

# Impresion en vez de logging
grep -rn "print(" --include="*.py" . | grep -v "/ui/"

# Endpoints y literales de red
grep -rn "http://\|https://" --include="*.py" . | grep -v "constants.py"

# Posibles secretos
grep -rniE "(api[_-]?key|token|password|secret)\s*[:=]\s*[\"'][^\"']+[\"']" --include="*.py" .
```

Para el mapa de dependencias y el inventario de modulos inalcanzables, consultar
el analisis de la fase 1 del proyecto (`docs/analisis.md`) o el grafo de
dependencias del repositorio antes de decidir que un modulo esta muerto.

## Triaje

Antes de refactorizar, clasificar cada hallazgo:

1. **Es codigo vivo?** Confirmar alcanzabilidad desde el composition root. Un
   modulo no alcanzable se pone en cuarentena, no se refactoriza.
2. **Es duplicado?** Dos modulos con el mismo proposito se consolidan en uno; no
   se refactorizan los dos.
3. **Afecta al comportamiento?** Si es asi, no es refactorizacion: es correccion
   de bug, se separa y se declara aparte.
4. **Cual es el peor smell primero?** Critico, luego alta, luego media, luego
   baja. El orden importa porque un bloque critico puede ocultar a los demas.

## Anti-smells del propio refactor

| Anti-pattern | Por que falla | Que hacer |
|---|---|---|
| Refactorizar sin baseline | No se puede demostrar que nada cambio | Registrar `ruff`/`mypy`/`pytest` antes |
| Anadir una capa "por si acaso" | Sobreingenieria en una app CLI | Solo si hay un segundo implementador |
| Bucle `for` dentro de un test | El primer fallo oculta el resto | `pytest.mark.parametrize` |
| Supresion `# noqa` para pasar el gate | Enmascara el problema | Arreglar el codigo |
| Mover logica al composition root | El composition root solo compone | Logica a la capa que le corresponde |
