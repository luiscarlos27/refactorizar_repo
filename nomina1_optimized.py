"""Calculo de nomina mensual optimizado en Python puro (sin dependencias).

Es mas rapido que nomina1.py a nivel de programa porque elimina el trabajo
recurrente que el original hace por cada empleado:
  - sin print() por fila
  - sin variable global (devuelve el resultado)
  - sin escritura linea a linea: un solo "\n".join antes de escribir
  - impuesto de mes calculado una sola vez (fuera del bucle)

El resultado (valor y formato) es identico al original:
    ID:<id> Name:<nombre> Pay:<float>
"""

PEAK_MONTHS = ("Jan", "Dec")

EMPLOYEES = [
    {"i": 1, "n": "Carlos", "t": "FT", "h": 160, "d": 2},
    {"i": 2, "n": "Ana", "t": "PT", "h": 80, "d": 0},
    {"i": 3, "n": "Luis", "t": "C", "h": 100, "d": 5},
]

OUTPUT_PATH = "payroll_output_optimized.txt"


def payroll(employees, month):
    """Calcula la nomina y devuelve las lineas de salida formateadas.

    Las operaciones aritmeticas replican exactamente el algoritmo original
    para conservar el mismo resultado de punto flotante (tasa de impuesto
    hoisteada fuera del bucle porque depende solo del mes, no del empleado).
    """
    peak_tax = 0.10
    regular_tax = 0.15
    tax = peak_tax if month == "Jan" or month == "Dec" else regular_tax

    lines = []
    append = lines.append
    for emp in employees:
        emp_type = emp["t"]
        hours = emp["h"]
        absent_days = emp["d"]
        if emp_type == "FT":
            salary = hours * 25
            if absent_days == 0:
                salary += 200
            elif absent_days <= 2:
                salary += 100
            else:
                salary -= 50
            salary -= salary * tax
            append("ID:" + str(emp["i"]) + " Name:" + emp["n"] + " Pay:" + str(salary))
        elif emp_type == "PT":
            salary = hours * 15
            if absent_days == 0:
                salary += 100
            elif absent_days <= 2:
                salary += 50
            else:
                salary -= 25
            salary -= salary * tax
            append("ID:" + str(emp["i"]) + " Name:" + emp["n"] + " Pay:" + str(salary))
        elif emp_type == "C":
            salary = hours * 30
            salary -= salary * 0.05
            append("ID:" + str(emp["i"]) + " Name:" + emp["n"] + " Pay:" + str(salary))
        # tipos desconocidos: el original los omite y solo imprime "Unknown type".
    return lines


def write_output(lines, path=OUTPUT_PATH):
    """Escribe todos los registros en una sola operacion de I/O."""
    with open(path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines) + ("\n" if lines else ""))


def main():
    result = payroll(EMPLOYEES, "Jan")
    write_output(result)
    print(f"Processed {len(result)} employees -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()