M = 1000  # Valor grande para penalizar las variables inventadas


# 1. PEDIR LOS DATOS (CON MENÚ NUMÉRICO)

print("=== MÉTODO DE LA GRAN M ===")
while True:
    op_obj = input("¿Qué deseas hacer? (1: Maximizar, 2: Minimizar): ").strip().lower()
    if op_obj in ["1", "max"]:
        objetivo = "max"
        break
    elif op_obj in ["2", "min"]:
        objetivo = "min"
        break
    print("  [!] Opción no válida. Escribe 1 o 2.")

num_x = int(input("¿Cuántas variables (x) tiene tu problema?: "))


print("\n--- PASO 1: FUNCIÓN OBJETIVO (Z) ---")
coef_z = []
for i in range(num_x):
    valor = float(input(f"  Ingresa el valor que acompaña a x{i + 1}: "))
    coef_z.append(valor)

num_rest = int(input("\n¿Cuántas restricciones tiene tu problema?: "))

restricciones = []
for i in range(num_rest):
    print(f"\n--- RESTRICCIÓN {i + 1} ---")
    fila_x = []
    for j in range(num_x):
        valor = float(input(f"  Valor de x{j + 1}: "))
        fila_x.append(valor)

    while True:
        op_signo = input("  Signo (1: <=,  2: >=,  3: =): ").strip()
        if op_signo in ["1", "<=", "<"]:
            signo = "<="
            break
        elif op_signo in ["2", ">=", ">"]:
            signo = ">="
            break
        elif op_signo in ["3", "="]:
            signo = "="
            break
        print("  [!] Opción no válida. Escribe 1, 2 o 3.")

    resultado = float(input("  Número después del signo: "))

    # Si el resultado es negativo, multiplicamos toda la fila por -1
    if resultado < 0:
        for j in range(num_x):
            fila_x[j] = -fila_x[j]
        resultado = -resultado
        if signo == "<=":
            signo = ">="
        elif signo == ">=":
            signo = "<="

    restricciones.append([fila_x, signo, resultado])



# 2. ARMAR LA TABLA SIMPLEX INICIAL

columnas = []
for j in range(num_x):
    columnas.append(f"x{j + 1}")

base = []
vars_extra = []  # Guardará: [nombre, fila_donde_va, valor (+1 o -1)]
cont_s, cont_e, cont_r = 1, 1, 1

for i in range(num_rest):
    signo = restricciones[i][1]
    if signo == "<=":
        nombre = f"S{cont_s}"
        cont_s += 1
        vars_extra.append([nombre, i, 1.0])
        base.append(nombre)
    elif signo == ">=":
        nombre_e = f"E{cont_e}"
        nombre_r = f"R{cont_r}"
        cont_e += 1
        cont_r += 1
        vars_extra.append([nombre_e, i, -1.0])
        vars_extra.append([nombre_r, i, 1.0])
        base.append(nombre_r)
    elif signo == "=":
        nombre_r = f"R{cont_r}"
        cont_r += 1
        vars_extra.append([nombre_r, i, 1.0])
        base.append(nombre_r)

for item in vars_extra:
    columnas.append(item[0])
columnas.append("Solucion")

total_cols = len(columnas)

# Crear Fila Z (fila 0)
fila_z = [0.0] * total_cols
for j in range(num_x):
    fila_z[j] = -coef_z[j]

for c in range(total_cols):
    if columnas[c].startswith("R"):
        fila_z[c] = M if objetivo == "max" else -M

# Crear filas de las restricciones
tabla = [fila_z]
for i in range(num_rest):
    fila = [0.0] * total_cols
    for j in range(num_x):
        fila[j] = restricciones[i][0][j]
    fila[-1] = restricciones[i][2]
    tabla.append(fila)

for idx_extra in range(len(vars_extra)):
    fila_destino = vars_extra[idx_extra][1] + 1
    valor = vars_extra[idx_extra][2]
    tabla[fila_destino][num_x + idx_extra] = valor


# Limpiar las M de la fila Z en las columnas R que están en la base
for i in range(num_rest):
    if base[i].startswith("R"):
        col_r = columnas.index(base[i])
        multiplicador = tabla[0][col_r]
        for c in range(total_cols):
            tabla[0][c] = tabla[0][c] - multiplicador * tabla[i + 1][c]



# Función auxiliar para dibujar la tabla en pantalla
def imprimir_tabla(titulo):
    print(f"\n=== {titulo} ===")
    print("Base   |", end="")
    for col in columnas:
        print(f"{col:>9}", end="")
    print("\n" + "-" * (9 * total_cols + 8))

    nombres_filas = ["Z"] + base
    for i in range(len(tabla)):
        print(f"{nombres_filas[i]:<6} |", end="")
        for num in tabla[i]:
            print(f"{num:9.2f}", end="")
        print()

imprimir_tabla("TABLA INICIAL")




# 3. RESOLVER ITERACIÓN POR ITERACIÓN (GAUSS-JORDAN)

iteracion = 1
while True:
    # A) Buscar columna que entra (según max o min)
    col_pivote = -1
    if objetivo == "max":
        mejor_valor = -0.00001
        for c in range(total_cols - 1):
            if tabla[0][c] < mejor_valor:
                mejor_valor = tabla[0][c]
                col_pivote = c
    else:
        mejor_valor = 0.00001
        for c in range(total_cols - 1):
            if tabla[0][c] > mejor_valor:
                mejor_valor = tabla[0][c]
                col_pivote = c


    # Si no hay columna que mejore Z, ya llegamos al óptimo
    if col_pivote == -1:
        break


    # B) Buscar fila que sale (razón mínima positiva)
    fila_pivote = -1
    menor_razon = float("inf")
    for f in range(1, len(tabla)):
        elemento = tabla[f][col_pivote]
        if elemento > 0.00001:
            razon = tabla[f][-1] / elemento
            if razon < menor_razon:
                menor_razon = razon
                fila_pivote = f


    if fila_pivote == -1:
        print("\n[!] El problema NO tiene solución acotada (crece al infinito).")
        exit()


    # C) Actualizar variable básica y hacer ceros (Pivoteo)
    base[fila_pivote - 1] = columnas[col_pivote]
    pivote = tabla[fila_pivote][col_pivote]

    for c in range(total_cols):
        tabla[fila_pivote][c] = tabla[fila_pivote][c] / pivote

    for f in range(len(tabla)):
        if f != fila_pivote:
            factor = tabla[f][col_pivote]
            for c in range(total_cols):
                tabla[f][c] = tabla[f][c] - factor * tabla[fila_pivote][c]

    imprimir_tabla(f"ITERACIÓN {iteracion}")
    iteracion += 1



# 4. MOSTRAR RESULTADO FINAL

print("\n================ RESULTADO FINAL ================")
infactible = False
for i in range(len(base)):
    if base[i].startswith("R") and tabla[i + 1][-1] > 0.001:
        infactible = True

if infactible:
    print("El problema NO tiene solución factible (quedó una variable R > 0).")
else:
    print(f"Valor óptimo de Z = {tabla[0][-1]:.2f}")
    for j in range(num_x):
        nombre_x = f"x{j + 1}"
        if nombre_x in base:
            fila_x = base.index(nombre_x) + 1
            print(f"  {nombre_x} = {tabla[fila_x][-1]:.2f}")
        else:
            print(f"  {nombre_x} = 0.00")