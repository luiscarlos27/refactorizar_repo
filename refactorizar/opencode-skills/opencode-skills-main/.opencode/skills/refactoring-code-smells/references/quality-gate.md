# Quality Gate

La refactorizacion no esta terminada hasta que el gate pasa. El gate es la unica
evidencia aceptable de que el comportamiento se preservo.

## Comandos

Desde `refactorizar/proyecto_refactoring/`:

```bash
ruff check .                                  # Lint (E,F,W,I,UP,B,SIM)
mypy --strict .                               # Tipado estricto
pytest                                        # Suite completa
python -m compileall -q proyecto_refactoring  # Sin errores de sintaxis
```

Cobertura, cuando el cambio toca logica de negocio:

```bash
pytest --cov=proyecto_refactoring --cov-report=term-missing
```

El umbral vive en `pyproject.toml` (`[tool.coverage.report] fail_under = 90`), asi
que `pytest` ya falla si la cobertura baja del 90 %. No hace falta pasar el flag
a mano salvo para ver el informe.

## Orden

```text
ruff check  ->  mypy --strict  ->  pytest  ->  compileall
```

Se detiene en el primer fallo. Arreglar el bloque, no avanzar con el gate en rojo.
El orden va de lo mas barato y rapido (segundos) a lo mas caro.

## Patron de linea base

Antes de modificar, capturar la salida para poder comparar despues:

```bash
ruff check . > /tmp/gate_ruff_before.txt 2>&1
mypy --strict . > /tmp/gate_mypy_before.txt 2>&1
pytest > /tmp/gate_pytest_before.txt 2>&1
```

Despues del bloque:

```bash
ruff check . > /tmp/gate_ruff_after.txt 2>&1
diff /tmp/gate_ruff_before.txt /tmp/gate_ruff_after.txt
```

Reglas de comparacion:

- **Ruff:** el numero de errores no puede aumentar. Ir a cero es lo esperado.
- **Mypy:** el numero de errores no puede aumentar. Un error preexistente que se
  resuelve es una mejora, se anota.
- **Pytest:** el mismo numero de tests pasando, y **cero tests nuevos en rojo**.
  Un test que falla porque el codigo cambio de comportamiento es una regresion,
  no un test que se actualiza.
- **Salida del programa:** si el cambio es de refactorizacion pura, la salida
  debe ser identica. Comparar byte a byte cuando la CLI genera archivo.

## Reglas de avance

| Situacion | Decision |
|---|---|
| Gate verde, sin cambios de comportamiento | Commit del bloque |
| Gate verde, la cobertura subio | Commit y anotar la mejora |
| Gate rojo por el cambio | Revertir el bloque, replantear la tecnica |
| Gate verde pero cambia la salida | No es refactorizacion: separar como correccion |
| Falla un test preexistente | No tocar el test para hacerlo pasar |

## Anti-patterns de gate

- **NO** relajar el umbral de cobertura para que el gate pase.
- **NO** editar un test para que acepte el codigo refactorizado sin justificar el
  cambio de expectativa.
- **NO** anadir `# type: ignore` o `# noqa` mas alla de lo estrictamente
  justificado y documentado.
- **NO** declarar el trabajo terminado sin ejecutar el gate.
- **NO** ejecutar el gate una sola vez al final: se ejecuta por cada bloque.

## Evidencia para el informe

Registrar por bloque:

```text
Bloque: globals a repositorio inyectado
ruff:    12 errores -> 0
mypy:    0 errores -> 0
pytest:  152 pasando -> 152 pasando
salida:  identica (diff vacio)
```

Estos numeros son los que convierten un reporte de refactorizacion en algo
verificable por un tercero.
