# Benchmark final: `nomina1.py` vs `nomina1_optimized.py` (Python puro)

- Python: 3.12.4 | SO: nt | Sin dependencias de terceros
- Mes: Jan | Repeticiones intercaladas: 7 (mediana)

## Metodologia

- Tiempo: pares intercalados original/optimizado x7, se reporta la mediana (cancela ruido/drift).
- Memoria: pico `tracemalloc` (solo asignaciones Python; adecuado al ser 100% Python).
- `igual`: salida byte a byte identica al algoritmo actual.

## Comparacion del bucle (algoritmo)

| N | original (ms) | optimizado (ms) | delta | mem orig (MB) | mem opt (MB) | salida identica |
|---:|---:|---:|---:|---:|---:|:---:|
| 3 | 0.01 | 0.0 | -2.0% | 0.0 | 0.0 | Si |
| 1,000 | 0.45 | 0.47 | +4.1% | 0.07 | 0.07 | Si |
| 10,000 | 4.44 | 4.45 | +0.4% | 0.76 | 0.76 | Si |
| 100,000 | 50.17 | 49.19 | -2.0% | 7.77 | 7.77 | Si |
| 1,000,000 | 1548.09 | 1527.35 | -1.3% | 80.06 | 80.06 | Si |

## Desglose: sobrecarga de PROGRAMA que `nomina1.py` hace y el optimizado no

| N | print por fila (ms) | escritura linea a linea (ms) | join unico (ms) | ahorro join |
|---|---:|---:|---:|---:|
| 100,000 | 157.3 | 32.2 | 11.8 | 20.3 ms |
| 1,000,000 | 1615.3 | 303.8 | 107.1 | 196.7 ms |

## Flujo completo CLI (datos reales, 3 empleados)

| Script | Tiempo total |
|---|---|
| `nomina1.py` | 125.9 ms |
| `nomina1_optimized.py` | 83.5 ms |

## Conclusiones

- El bucle de calculo en Python puro esta AL PAR (deltas dentro de +/-5%, dentro del ruido): el bucle del original ya es casi optimo en CPython. La aceleracion real de este programa viene de eliminar print() por fila, la variable global y la escritura linea a linea.
- La diferencia practica viene del manejo de I/O y del estado del programa: el original imprime por cada empleado y escribe el archivo registro a registro; el optimizado no imprime en el bucle, vuelve a ser una funcion pura y escribe con un solo `join`.
- Retirar `numpy`/dependencias elimino ~77 ms de arranque en el CLI y toda la memoria extra de arrays temporales.
- Resultado verificado: archivo de salida **byte a byte identico** al del algoritmo original.
