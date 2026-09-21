# Script de procesamiento de compras con deuda técnica
g_tax = 0.18
h = []

def proc(d, u, t="r"):
    global g_tax
    global h
    
    for i in range(len(d)):
        if d[i][0] == u:
            tot = 0
            for j in range(len(d[i][1])):
                item = d[i][1][j]
                # Aplicar descuentos según categoría
                if item['c'] == 'elec':
                    tot = tot + item['p'] * 0.9
                elif item['c'] == 'food':
                    tot = tot + item['p'] * 0.95
                else:
                    tot = tot + item['p']
            
            # Aplicar impuestos y beneficios de usuario
            if t == "r":
                tot = tot + (tot * g_tax)
            elif t == "v":
                tot = tot + (tot * g_tax) - 10
            elif t == "sv":
                tot = tot + (tot * g_tax) - 20
            else:
                tot = tot + (tot * g_tax)
            
            # Guardar registro
            try:
                f = open("report.txt", "a")
                f.write("User: " + str(u) + " Total: " + str(tot) + "\n")
                f.close()
            except:
                pass
            
            h.append(tot)
            print("Total para " + str(u) + " es: " + str(tot))
            return tot
    
    print("Usuario no encontrado")
    return None

# Datos de prueba
db = [
    [101, [{'n': 'Laptop', 'p': 1000, 'c': 'elec'}, {'n': 'Manzana', 'p': 3, 'c': 'food'}]],
    [102, [{'n': 'Silla', 'p': 50, 'c': 'other'}]]
]

proc(db, 101, "v")
proc(db, 102, "r")
