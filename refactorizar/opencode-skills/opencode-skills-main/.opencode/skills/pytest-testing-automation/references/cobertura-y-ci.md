# Cobertura y CI

## Configuracion

La cobertura se configura en `pyproject.toml`, no en la linea de comandos:

```toml
[tool.coverage.run]
source = ["proyecto_refactoring"]
omit = ["proyecto_refactoring/main.py"]

[tool.coverage.report]
fail_under = 90
show_missing = true
```

Con `fail_under` aqui, `pytest` ya falla cuando la cobertura baja del umbral: no
hace falta recordarlo en ningun script.

`omit` para `main.py` es una decision a justificar: el composition root es codigo
de arranque (lectura de argumentos, construccion de dependencias) y su
cobertura aporta poco valor frente al coste de testearlo. Documentar el motivo
cuando se excluya un modulo, para que no parezca una exclusion oportunista.

## Comandos

```bash
pytest                                             # suite completa (aplica el umbral)
pytest --cov=proyecto_refactoring --cov-report=term-missing
pytest --cov=proyecto_refactoring --cov-report=xml:coverage.xml   # para SonarQube
pytest -n auto                                     # paralelo (pytest-xdist)
pytest --lf -x -v                                  # solo lo que fallo, parar al primero
pytest -m "not slow"                               # excluir pruebas lentas
pytest tests/services -k cache                     # un modulo, un concepto
```

Reportes: `term-missing` en consola durante el desarrollo, `xml` en CI para
integrar con SonarQube o Coveralls.

## La cobertura no es el objetivo

Un porcentaje alto se puede alcanzar sin probar nada. Los patrones que inflan la
metrica sin aportar valor:

| Patron | Por que no cuenta |
|---|---|
| `return` temprano sin probar | Linea cubierta, logica no verificada |
| `except: pass` | Se "cubre" la rama de error sin comprobar nada |
| Test que solo llama a la funcion | Sin `assert`, la prueba no verifica |
| Codigo trivial (getters, `__repr__`) | Suma lineas, resta porcentaje util |
| `# pragma: no cover` | Excluir en lugar de probar |

Por eso `fail_under` va acompanado de revision de los huecos: leer
`term-missing` y preguntarse si cada linea sin cubrir es codigo que puede fallar.

## Matriz de casos limite por capa

| Capa | Casos que no deben faltar |
|---|---|
| `models/` | Invariantes validas e invalidas (`__post_init__`), campos ausentes en la respuesta, conversion desde la API |
| `storage/` | Entrada vacia, entrada duplicada, TTL vigente, TTL expirado, persistencia entre instancias |
| `api/` | Exito, `Response: False`, 404, timeout, connection error, error HTTP generico, reintentos agotados, circuito abierto |
| `services/` | Exito, sin resultados, API caida (degradacion a `None` / `[]`) |
| `ui/` | Entrada valida, entrada invalida, opcion de menu inexistente, EOF (Ctrl+D) |
| `config.py` | Cada invariante de `__post_init__` que lanza `ConfigError` |
| `exceptions/` | Que la jerarquia se puede capturar por su clase base |

## Integracion en CI

```yaml
# Etapas minimas de un pipeline
- ruff check .
- mypy --strict .
- pytest --cov=proyecto_refactoring --cov-report=xml:coverage.xml
```

Las tres etapas en un solo job, en ese orden: lint y tipos son segundos y
descartan la mayoria de los fallos antes de gastar minutos en la suite.

## Señales de una suite enferma

| Sintoma | Causa probable |
|---|---|
| Falla en CI y pasa en local | Tests dependientes del orden o de la red |
| Falla intermitente | Hora o aleatoriedad sin inyectar |
| Suite lenta | Falta `mocker` en alguna prueba, o falta de `-n auto` |
| Cobertura baja sin cambios | Modulos nuevos sin testear |
| Cobertura alta y muchos fallos | Metrica manipulada con `no cover` o asserts debiles |

## Trampas

- **Subir el umbral para que la suite pase.** Convierte la cobertura en decorado.
- **`pytest -x` en la rutina local sin`**`-x` en CI. Parar en el primer fallo es
  comodo localmente y oculta fallos multiples en CI.
- **Marcar `skip` sin motivo.** Un `skip` acumula y termina ocultando un bug.
- **Mismo nombre de test en dos modulos.** El reporte los distingue por ruta, pero
  el mensaje de fallo se vuelve ambiguo. Prefijar por concepto.
- **`--cov` con una ruta que no existe.** Falla en silencio o reporta 0 % y se
  interpreta como un problema de cobertura real.
