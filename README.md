# Método de la Gran M

## 1. Descripción general del software

Este programa resuelve problemas de **programación lineal** desde la consola usando el **Método simplex** y el **Método de la Gran M**.

El usuario introduce:

1. Si desea maximizar o minimizar.
2. La cantidad de variables originales.
3. Los coeficientes de la función objetivo.
4. La cantidad de restricciones.
5. Los coeficientes, el signo y el resultado de cada restricción.

Después, el programa:

1. Convierte las restricciones en ecuaciones.
2. Agrega variables de holgura, exceso y artificiales.
3. Construye una tabla simplex.
4. Limpia las variables artificiales de la fila Z.
5. Encuentra iterativamente la variable que entra y la que sale.
6. Aplica operaciones de Gauss-Jordan.
7. Presenta el óptimo o informa que no existe solución.

No utiliza una librería externa de optimización. La resolución se implementa manualmente con listas y operaciones aritméticas.

---

## 2. Tecnologías utilizadas

| Tecnología | Uso dentro del programa |
|---|---|
| Python 3 | Lenguaje utilizado para todo el programa |
| `input()` | Solicita datos al usuario |
| `print()` | Muestra tablas y resultados |
| `while` y `for` | Controlan menús, lecturas e iteraciones |
| Listas de Python | Guardan restricciones, nombres de columnas y tablas |
| Cadenas `str` | Guardan nombres como `x1`, `S1`, `E1` y `R1` |
| Números `float` | Guardan coeficientes, resultados y cálculos |
| Operaciones de punto flotante | Permiten ejecutar el pivoteo simplex |

El programa no necesita instalar paquetes con `pip`.

---

## 3. Requisitos y ejecución

Requiere tener Python 3 instalado.

Desde la carpeta del proyecto, ejecuta:

```powershell
python gran_m.py
```

El programa se ejecutará por consola.

---

## 4. Ejemplo completo

Se puede usar como ejemplo el problema presentado en las diapositivas:

```text
Maximizar Z = 10x1 + 20x2 + 15x3

Sujeto a:

x1 + x2 + x3 <= 10
x1 + 2x2     >= 6
x2 + x3      = 4

x1, x2, x3 >= 0
```

Las respuestas deben ingresarse en este orden desde la consola:

```text
1
3
10
20
15
3
1
1
1
1
10
1
2
0
2
6
0
1
1
3
4
```

El significado de cada entrada es:

- `1`: maximizar la función objetivo.
- `3`: existen tres variables originales.
- `10`, `20` y `15`: coeficientes de `x1`, `x2` y `x3` en `Z`.
- `3`: existen tres restricciones.
- `1`, `1`, `1`, `1`, `10`: primera restricción `x1 + x2 + x3 <= 10`.
- `1`, `2`, `0`, `2`, `6`: segunda restricción `x1 + 2x2 >= 6`.
- `0`, `1`, `1`, `3`, `4`: tercera restricción `x2 + x3 = 4`.

Las variables extra que el programa puede generar son:

- `S1`: holgura de la primera restricción.
- `E1`: exceso de la segunda restricción.
- `R1`: variable artificial de la segunda restricción.
- `R2`: variable artificial de la tercera restricción.

La solución esperada para este problema es:

```text
Z = 140
x1 = 6
x2 = 4
x3 = 0
```

---

## 5. Conceptos matemáticos usados

### 5.1. Variables originales

Las variables originales son las que aparecen en el problema:

```text
x1, x2, x3, ...
```

Sus coeficientes se leen al inicio y después se usan tanto en la fila Z como en las restricciones.

### 5.2. Variables de holgura

Una restricción menor o igual:

```text
x1 + x2 <= 4
```

se transforma en:

```text
x1 + x2 + S1 = 4
```

`S1` representa la cantidad que falta para alcanzar exactamente el lado derecho.

Si se usan completamente los recursos, la holgura puede valer cero.

### 5.3. Variables de exceso

Una restricción mayor o igual:

```text
x1 + x2 >= 4
```

se transforma en:

```text
x1 + x2 - E1 + R1 = 4
```

`E1` representa la cantidad que excede el mínimo requerido.

### 5.4. Variables artificiales

Las variables artificiales se llaman `R` en el programa.

Se necesitan para construir una solución básica inicial en restricciones `>=` e `=`, porque no siempre existe una variable natural que pueda comenzar con valor positivo en la base.

Una variable artificial no debe aparecer en la solución final. Por eso se penaliza con `M`.

### 5.5. Constante M

```python
M = 1000
```

`M` representa una penalización grande.

- En maximización se usa `+M` en las columnas artificiales.
- En minimización se usa `-M`.

Como una solución real no puede depender de una variable artificial, el algoritmo intenta expulsarla de la base.

### 5.6. Variable básica

Una variable básica es una variable que tiene un valor definido por una fila de la tabla.

La lista `base` guarda cuál variable corresponde a cada fila.

Ejemplo:

```python
base = ["S1", "R1"]
```

Esto significa:

- La primera restricción tiene como variable básica `S1`.
- La segunda restricción tiene como variable básica `R1`.

### 5.7. Pivote

El pivote es la intersección de:

- Una variable que entra: determina una nueva columna.
- Una variable que sale: determina una fila.

El valor ubicado en esa intersección se normaliza a `1`, y el resto de su columna se convierte en ceros.

---

## 6. Bloque 1: declaración de M

```python
M = 1000
```

### Qué hace

Declara una constante global con el valor `1000`.

### Para qué sirve

Se utiliza como penalización para las variables artificiales `R`.

### Observación

Cuanto mayor sea el objetivo de minimizar o maximizar una solución artificial frente a una real, se debe usar una `M` suficientemente grande.

En este programa el valor está fijado y no se pregunta al usuario.

---

## 7. Bloque 2: selección del objetivo

```python
print("=== MÉTODO DE LA GRAN M ===")
while True:
    op_obj = input(
        "¿Qué deseas hacer? (1: Maximizar, 2: Minimizar): "
    ).strip().lower()
```

### Qué hace

- Muestra el título del programa.
- Abre un ciclo `while True`.
- Solicita qué operación desea realizar el usuario.
- `.strip()` elimina espacios al inicio y al final.
- `.lower()` convierte el texto a minúsculas.

### Condición de maximización

```python
if op_obj in ["1", "max"]:
    objetivo = "max"
    break
```

Si el usuario escribe `1` o `max`:

- Guarda `objetivo = "max"`.
- Ejecuta `break`.
- Sale del ciclo.

### Condición de minimización

```python
elif op_obj in ["2", "min"]:
    objetivo = "min"
    break
```

Si escribe `2` o `min`:

- Guarda `objetivo = "min"`.
- Sale del ciclo.

### Entrada inválida

```python
print("  [!] Opción no válida. Escribe 1 o 2.")
```

Si no coincide con ninguna opción, vuelve a pedir el dato.

---

## 8. Bloque 3: cantidad de variables

```python
num_x = int(input(
    "¿Cuántas variables (x) tiene tu problema?: "
))
```

### Qué hace

- Solicita un número.
- Convierte el texto recibido a entero mediante `int()`.
- Guarda el resultado en `num_x`.

### Ejemplo

Si escribe `3`, el programa trabajará con:

```text
x1, x2, x3
```

---

## 9. Bloque 4: coeficientes de la función objetivo

```python
coef_z = []
for i in range(num_x):
    valor = float(input(
        f"  Ingresa el valor que acompaña a x{i + 1}: "
    ))
    coef_z.append(valor)
```

### Paso a paso

1. `coef_z = []` crea una lista vacía.
2. `range(num_x)` genera tantos ciclos como variables existen.
3. `i + 1` convierte el índice 0, 1, 2 en `x1`, `x2`, `x3`.
4. `float()` convierte el dato a número decimal.
5. `append()` agrega el número al final de `coef_z`.

### Ejemplo

Si los coeficientes son `3` y `2`, la lista queda:

```python
coef_z = [3.0, 2.0]
```

La función objetivo representada sería:

```text
Z = 3x1 + 2x2
```

---

## 10. Bloque 5: cantidad de restricciones

```python
num_rest = int(input(
    "\n¿Cuántas restricciones tiene tu problema?: "
))
```

Convierte la cantidad ingresada en un entero y la guarda en `num_rest`.

Esta cantidad determina cuántas filas tendrá la parte inferior de la tabla simplex.

---

## 11. Bloque 6: lectura de las restricciones

```python
restricciones = []
for i in range(num_rest):
```

`restricciones` será una lista que contiene cada restricción.

Por ejemplo:

```python
[
    [[1.0, 1.0], "<=", 4.0],
    [[1.0, 0.0], "<=", 2.0]
]
```

Cada elemento tiene esta estructura:

```python
[[coeficientes], signo, lado_derecho]
```

---

## 12. Lectura de los coeficientes de una restricción

```python
fila_x = []
for j in range(num_x):
    valor = float(input(f"  Valor de x{j + 1}: "))
    fila_x.append(valor)
```

### Qué hace

Pide el coeficiente de cada variable dentro de una restricción.

### Ejemplo

Para:

```text
2x1 + 3x2 <= 10
```

La lista será:

```python
fila_x = [2.0, 3.0]
```

---

## 13. Lectura y validación del signo

```python
while True:
    op_signo = input(
        "  Signo (1: <=,  2: >=,  3: =): "
    ).strip()
```

Este ciclo continúa hasta que se ingrese un signo válido.

### Opciones aceptadas

```python
if op_signo in ["1", "<=", "<"]:
    signo = "<="
```

Acepta:

- `1`
- `<=`
- `<`

Aunque `<` no es estándar en programación lineal, el programa lo normaliza a `<=`.

```python
elif op_signo in ["2", ">=", ">"]:
    signo = ">="
```

Acepta `2`, `>=` o `>`.

```python
elif op_signo in ["3", "="]:
    signo = "="
```

Acepta `3` o `=`.

Si no coincide ninguna opción:

```python
print("  [!] Opción no válida. Escribe 1, 2 o 3.")
```

El ciclo vuelve a solicitar el signo.

---

## 14. Lectura del lado derecho

```python
resultado = float(input("  Número después del signo: "))
```

Pide el valor al lado derecho del signo y lo convierte a `float`.

Ejemplo:

```text
2x1 + x2 <= 8
```

El resultado es:

```python
resultado = 8.0
```

---

## 15. Normalización de resultados negativos

```python
if resultado < 0:
```

La tabla simplex trabaja mejor cuando el lado derecho es positivo o cero.

Si el resultado es negativo, el programa modifica toda la fila:

```python
for j in range(num_x):
    fila_x[j] = -fila_x[j]
resultado = -resultado
```

Esto cambia el signo de cada coeficiente y cambia el resultado a positivo.

Después invierte el signo original:

```python
if signo == "<=":
    signo = ">="
elif signo == ">=":
    signo = "<="
```

### Ejemplo

Entrada:

```text
-x1 + 2x2 <= -6
```

Después de normalizar:

```text
x1 - 2x2 >= 6
```

Esto es una transformación algebraicamente equivalente.

---

## 16. Guardado de la restricción

```python
restricciones.append([fila_x, signo, resultado])
```

Cada restricción queda guardada como una mini-lista:

```python
[coeficientes, signo, lado_derecho]
```

Después se repite el ciclo para leer la siguiente restricción.

---

## 17. Bloque 7: nombres de las variables originales

```python
columnas = []
for j in range(num_x):
    columnas.append(f"x{j + 1}")
```

`columnas` representa todas las columnas de la tabla.

Si existen 3 variables, comienza como:

```python
columnas = ["x1", "x2", "x3"]
```

---

## 18. Variables básicas y variables extra

```python
base = []
vars_extra = []
cont_s, cont_e, cont_r = 1, 1, 1
```

### Variables

- `base`: variables básicas por fila.
- `vars_extra`: holguras, excesos y artificiales creados.
- `cont_s`: contador para `S1`, `S2`, etc.
- `cont_e`: contador para `E1`, `E2`, etc.
- `cont_r`: contador para `R1`, `R2`, etc.

Cada elemento de `vars_extra` tendrá esta forma:

```python
[nombre, fila_donde_va, valor]
```

Ejemplo:

```python
["S1", 0, 1.0]
```

Significa:

- Nombre: `S1`.
- Se coloca en la fila de la restricción índice `0`.
- Su coeficiente es `1`.

---

## 19. Creación de holguras

```python
if signo == "<=":
    nombre = f"S{cont_s}"
    cont_s += 1
    vars_extra.append([nombre, i, 1.0])
    base.append(nombre)
```

Para una restricción `<=`:

1. Crea una variable `S`.
2. Incrementa el contador de holguras.
3. Agrega la holgura con coeficiente `1`.
4. La pone en la lista `base`.

Ejemplo:

```text
restricción 1 <=
```

Crea:

```python
base = ["S1"]
```

---

## 20. Creación de exceso y artificial

```python
elif signo == ">=":
    nombre_e = f"E{cont_e}"
    nombre_r = f"R{cont_r}"
```

Para una restricción `>=` crea dos variables:

- `E` con coeficiente `-1`.
- `R` con coeficiente `+1`.

```python
vars_extra.append([nombre_e, i, -1.0])
vars_extra.append([nombre_r, i, 1.0])
base.append(nombre_r)
```

La variable artificial `R` se coloca como variable básica inicial.

---

## 21. Creación de una artificial para igualdad

```python
elif signo == "=":
    nombre_r = f"R{cont_r}"
    cont_r += 1
    vars_extra.append([nombre_r, i, 1.0])
    base.append(nombre_r)
```

Una restricción de igualdad no necesita variable de exceso ni holgura. Solo necesita una variable artificial para obtener una solución básica inicial.

---

## 22. Incorporación de variables extra a las columnas

```python
for item in vars_extra:
    columnas.append(item[0])
columnas.append("Solucion")
```

Todos los nombres de `vars_extra` se agregan al vector `columnas`.

Después se agrega `"Solucion"`, que representa el lado derecho de cada ecuación.

Ejemplo:

```python
columnas = [
    "x1", "x2", "S1", "E1", "R1", "Solucion"
]
```

---

## 23. Cantidad total de columnas

```python
total_cols = len(columnas)
```

Guarda cuántas columnas tiene la tabla.

Esta cantidad se utiliza en ciclos y formatos de impresión.

---

## 24. Construcción de la fila Z

```python
fila_z = [0.0] * total_cols
```

Crea una fila llena de ceros.

El índice inicial corresponde a la fila Z, aunque la estructura real de la tabla es:

```text
tabla[0] = fila Z
tabla[1] = restricción 1
tabla[2] = restricción 2
```

---

## 25. Signo de los coeficientes originales en Z

```python
for j in range(num_x):
    fila_z[j] = -coef_z[j]
```

Los coeficientes originales se colocan con signo negativo para permitir el criterio simplex usado por el programa.

Ejemplo:

```python
coef_z = [3.0, 2.0]
```

produce:

```python
fila_z = [-3.0, -2.0, ...]
```

---

## 26. Penalización de variables artificiales

```python
for c in range(total_cols):
    if columnas[c].startswith("R"):
        fila_z[c] = M if objetivo == "max" else -M
```

### Qué hace

Recorre las columnas y busca nombres que comienzan con `R`.

### Maximización

```python
fila_z[c] = M
```

Usa una penalización positiva.

### Minimización

```python
fila_z[c] = -M
```

Usa una penalización negativa.

Las demás columnas artificiales no reciben este cambio.

---

## 27. Construcción de las filas de restricciones

```python
tabla = [fila_z]
for i in range(num_rest):
    fila = [0.0] * total_cols
```

La tabla comienza con la fila Z.

Luego se crea una fila de ceros por cada restricción.

---

## 28. Copia de coeficientes originales

```python
for j in range(num_x):
    fila[j] = restricciones[i][0][j]
```

Copia en la tabla los coeficientes de las variables originales.

Ejemplo:

```python
restricciones[i][0] = [2.0, 3.0]
```

Se coloca:

```text
fila[x1] = 2
fila[x2] = 3
```

---

## 29. Copia del lado derecho

```python
fila[-1] = restricciones[i][2]
tabla.append(fila)
```

- `fila[-1]` selecciona la última posición, que corresponde a `Solucion`.
- `tabla.append(fila)` agrega la fila a la tabla.

---

## 30. Ubicación de holguras, excesos y artificiales

```python
for idx_extra in range(len(vars_extra)):
    fila_destino = vars_extra[idx_extra][1] + 1
    valor = vars_extra[idx_extra][2]
    tabla[fila_destino][num_x + idx_extra] = valor
```

### `fila_destino`

Se suma `1` porque la fila `0` está reservada para Z.

Ejemplo:

- Restricción índice `0`.
- Fila real en tabla: `0 + 1 = 1`.

### `num_x + idx_extra`

Indica la posición de la variable extra dentro de `columnas`.

Las variables originales ocupan las primeras `num_x` posiciones.

### `valor`

Puede ser:

- `1.0` para una holgura o artificial.
- `-1.0` para una variable de exceso.

Este bloque convierte la fila de ceros en una ecuación concreta.

---

## 31. Limpieza de las M básicas

```python
for i in range(num_rest):
    if base[i].startswith("R"):
        col_r = columnas.index(base[i])
        multiplicador = tabla[0][col_r]
        for c in range(total_cols):
            tabla[0][c] = tabla[0][c] - multiplicador * tabla[i + 1][c]
```

### Por qué es necesario

Una variable artificial que ya está en la base no puede tener un valor distinto de cero en la fila Z.

Este bloque elimina la penalización `M` de la fila Z aplicando una operación elemental.

### Explicación de variables

- `base[i]`: variable básica de la fila `i`.
- `startswith("R")`: comprueba si la variable es artificial.
- `col_r`: posición de esa variable artificial.
- `multiplicador`: valor que está en la fila Z en la columna `R`.
- `tabla[i + 1][c]`: fila de la restricción básica.

La operación:

```python
tabla[0][c] =
    tabla[0][c] - multiplicador * tabla[i + 1][c]
```

convierte en cero la columna correspondiente a esa variable artificial.

---

## 32. Función para mostrar tablas

```python
def imprimir_tabla(titulo):
```

Define una función reutilizable que recibe el texto que aparecerá como título.

Las funciones permiten mostrar la tabla inicial y todas las iteraciones sin repetir el código de impresión.

---

## 33. Encabezado de la tabla

```python
print(f"\n=== {titulo} ===")
print("Base   |", end="")
```

Muestra el título y comienza la línea del encabezado sin terminarla con un salto de línea.

---

## 34. Impresión de nombres de columnas

```python
for col in columnas:
    print(f"{col:>9}", end="")
```

Recorre todas las columnas.

`>9` alinea cada nombre a la derecha dentro de nueve caracteres.

---

## 35. Línea separadora

```python
print("\n" + "-" * (9 * total_cols + 8))
```

Inicia una nueva línea y crea una línea horizontal según la cantidad de columnas.

---

## 36. Asociación de filas con variables básicas

```python
nombres_filas = ["Z"] + base
```

Crea una lista donde:

- La primera fila se llama `Z`.
- Las siguientes filas toman el nombre de las variables básicas.

Ejemplo:

```python
["Z", "S1", "R1"]
```

---

## 37. Impresión del contenido

```python
for i in range(len(tabla)):
    print(f"{nombres_filas[i]:<6} |", end="")
    for num in tabla[i]:
        print(f"{num:9.2f}", end="")
    print()
```

### Qué hace

1. Recorre cada fila.
2. Imprime su nombre.
3. Recorre todos sus números.
4. Los imprime con dos decimales.
5. Cambia de línea al terminar la fila.

Ejemplo de formato:

```text
Z     |    -3.00    -2.00     0.00
S1    |     1.00     1.00     4.00
```

---

## 38. Impresión de la tabla inicial

```python
imprimir_tabla("TABLA INICIAL")
```

Llama a la función y muestra la tabla antes de comenzar las iteraciones.

---

## 39. Bloque 8: iteraciones simplex

```python
iteracion = 1
while True:
```

`iteracion` comienza en `1` y se utiliza para numerar las tablas.

`while True` mantiene el proceso hasta que:

- Se encuentra el óptimo.
- Se detecta un problema ilimitado.
- Se cumple otra condición de salida.

---

## 40. Selección de la variable que entra

```python
col_pivote = -1
```

Inicialmente no existe una columna pivote.

El valor `-1` indica que aún no se encontró una variable que pueda entrar.

---

## 41. Criterio para maximización

```python
if objetivo == "max":
    mejor_valor = -0.00001
    for c in range(total_cols - 1):
        if tabla[0][c] < mejor_valor:
            mejor_valor = tabla[0][c]
            col_pivote = c
```

### Qué hace

Recorre todas las columnas excepto `Solucion`.

Busca el coeficiente negativo más pequeño en la fila Z.

`-0.00001` funciona como tolerancia:

- Ignora valores cercanos a cero.
- Reduce problemas causados por pequeños errores de punto flotante.

Ejemplo:

```text
fila Z: [-3, 2, 0, -1]
```

La columna de `-3` sería elegida antes que la de `-1`.

---

## 42. Criterio para minimización

```python
else:
    mejor_valor = 0.00001
    for c in range(total_cols - 1):
        if tabla[0][c] > mejor_valor:
            mejor_valor = tabla[0][c]
            col_pivote = c
```

En minimización busca el coeficiente positivo más grande.

Esto es el criterio contrario al utilizado para maximización.

---

## 43. Óptimo encontrado

```python
if col_pivote == -1:
    break
```

Si no se encontró ninguna columna mejor, no existe otra variable que pueda mejorar Z.

El ciclo termina y el programa pasa al resultado final.

---

## 44. Inicialización de la fila pivote

```python
fila_pivote = -1
menor_razon = float("inf")
```

- `fila_pivote = -1`: ninguna fila ha sido seleccionada todavía.
- `float("inf")`: representa infinito.
- Cada razón válida debe ser menor que este valor inicial.

---

## 45. Cálculo de la razón mínima

```python
for f in range(1, len(tabla)):
    elemento = tabla[f][col_pivote]
```

Comienza desde `1` porque `0` es la fila Z.

Recupera el elemento correspondiente a la columna que entró.

---

## 46. Filas válidas para salir

```python
if elemento > 0.00001:
```

Solo se consideran filas cuyo elemento sea claramente positivo.

Elementos negativos o cercanos a cero no deben producir una razón válida.

---

## 47. Cálculo de la razón

```python
razon = tabla[f][-1] / elemento
```

Divide el lado derecho entre el elemento de la columna pivote:

```text
razón = Solución / elemento de la columna entrante
```

---

## 48. Selección de la razón mínima

```python
if razon < menor_razon:
    menor_razon = razon
    fila_pivote = f
```

Cada vez que encuentra una razón menor, actualiza:

- La razón mínima.
- La fila que debe salir.

Por eso se obtiene la fila con la razón positiva mínima.

---

## 49. Problema ilimitado

```python
if fila_pivote == -1:
    print(
        "\n[!] El problema NO tiene solución acotada "
        "(crece al infinito)."
    )
    exit()
```

Si existe una variable que debería entrar pero ninguna fila puede salir:

- El problema no tiene solución acotada.
- El método termina inmediatamente.
- `exit()` detiene la ejecución del programa.

---

## 50. Cambio de la variable básica

```python
base[fila_pivote - 1] = columnas[col_pivote]
```

El índice `-1` corrige el desplazamiento causado por la fila Z.

Ejemplo:

- La fila pivote real es `tabla[2]`.
- `fila_pivote - 1 = 1`.
- La posición `1` de `base` cambia por la variable entrante.

---

## 51. Obtención del pivote

```python
pivote = tabla[fila_pivote][col_pivote]
```

Guarda el número situado en la intersección entre la variable que entra y la fila que sale.

---

## 52. Normalización de la fila pivote

```python
for c in range(total_cols):
    tabla[fila_pivote][c] =
        tabla[fila_pivote][c] / pivote
```

Cada elemento de la fila pivote se divide entre el pivote.

Después de esta operación, el elemento pivote debe ser exactamente `1`.

---

## 53. Conversión de ceros en la columna pivote

```python
for f in range(len(tabla)):
    if f != fila_pivote:
        factor = tabla[f][col_pivote]
        for c in range(total_cols):
            tabla[f][c] =
                tabla[f][c]
                - factor * tabla[fila_pivote][c]
```

### Qué hace

Recorre todas las filas menos la fila pivote.

`factor` es el valor que tiene cada fila en la columna que acaba de entrar.

Luego resta una combinación lineal de la fila pivote para convertir ese factor en cero.

Esto es el proceso de **Gauss-Jordan** aplicado a toda la tabla.

---

## 54. Impresión de cada iteración

```python
imprimir_tabla(f"ITERACIÓN {iteracion}")
iteracion += 1
```

Después de cada pivote:

1. Se imprime la nueva tabla.
2. Se incrementa el contador de iteración.

---

## 55. Bloque 9: resultado final

```python
print(
    "\n================ "
    "RESULTADO FINAL "
    "================"
)
```

Muestra el título del resultado después de terminar las iteraciones.

---

## 56. Comprobación de solución factible

```python
infactible = False
for i in range(len(base)):
    if base[i].startswith("R")
       and tabla[i + 1][-1] > 0.001:
        infactible = True
```

Recorre todas las variables básicas.

Si una variable artificial `R`:

- Sigue estando en la base.
- Tiene un valor mayor que `0.001`.

entonces el problema no tiene solución factible.

El valor `0.001` sirve como tolerancia porque los cálculos usan decimales.

---

## 57. Mensaje de infactibilidad

```python
if infactible:
    print(
        "El problema NO tiene solución factible "
        "(quedó una variable R > 0)."
    )
```

Significa que existe al menos una restricción que no puede cumplirse en una solución válida.

No se muestran valores de las variables cuando se detecta infactibilidad.

---

## 58. Presentación del valor óptimo

```python
else:
    print(f"Valor óptimo de Z = {tabla[0][-1]:.2f}")
```

Si existe una solución factible, la última posición de la fila Z contiene el valor óptimo.

`:.2f` muestra el número con dos decimales.

---

## 59. Obtención del valor de cada variable original

```python
for j in range(num_x):
    nombre_x = f"x{j + 1}"
```

Recorre todas las variables originales.

---

## 60. Variable básica encontrada

```python
if nombre_x in base:
    fila_x = base.index(nombre_x) + 1
    print(f"  {nombre_x} = "
          f"{tabla[fila_x][-1]:.2f}")
```

Si la variable aparece en `base`:

1. Busca su posición.
2. Suma `1` para encontrar la fila real.
3. Toma el valor de la columna `Solucion`.
4. Lo muestra.

Ejemplo:

```text
x1 está en la base
base: ["x1", "S1"]
fila de x1: tabla[1]
tabla[1][-1]: 4
```

Resultado:

```text
x1 = 4.00
```

---

## 61. Variable no básica

```python
else:
    print(f"  {nombre_x} = 0.00")
```

Si la variable no está en la base, su valor es cero.

Esto ocurre porque las variables fuera de la base tienen valor cero en una solución básica.

---

## 7. Flujo completo del programa

```text
Inicio
  ↓
Solicitar objetivo
  ↓
Solicitar cantidad y coeficientes de variables
  ↓
Solicitar cantidad y datos de restricciones
  ↓
Normalizar restricciones con lado derecho negativo
  ↓
Crear nombres de columnas
  ↓
Crear holguras, excesos y artificiales
  ↓
Construir la fila Z
  ↓
Construir las filas de restricciones
  ↓
Eliminar las M iniciales de las artificiales básicas
  ↓
Mostrar tabla inicial
  ↓
Buscar variable que entra
  ↓
¿Existe variable entrante?
  Sí → Buscar fila que sale
      ↓
      ¿Existe fila válida?
      Sí → Ejecutar pivote y repetir
      No → Mostrar solución ilimitada
  No → Comprobar si quedan artificiales positivas
      ↓
      Artificial positiva → No existe solución factible
      Sin artificial positiva → Mostrar solución óptima
```

---

## 8. Cómo se interpreta una fila de la tabla

Ejemplo:

```text
S1 | 1.00  1.00  1.00  0.00  4.00
```

Las columnas pueden representar:

```text
x1 | x2 | S1 | R1 | Solucion
```

Interpretación:

- `S1` es la variable básica de esa fila.
- `1.00` acompaña a `x1`.
- `1.00` acompaña a `x2`.
- `1.00` indica el coeficiente básico de `S1`.
- `0.00` indica que `R1` no está presente.
- `4.00` es el valor actual de `S1`.

---

## 9. Significado de las iteraciones

Cada iteración representa un cambio de solución básica.

El algoritmo:

1. Identifica una variable que puede mejorar la función objetivo.
2. Decide cuál variable básica debe salir.
3. Intercambia ambas variables.
4. Recalcula toda la tabla.

Las iteraciones continúan hasta que no exista una mejora posible.

---

## 10. Casos finales

### Solución óptima

Ocurre cuando:

- Ya no existe una columna que pueda mejorar Z.
- No quedan variables artificiales positivas.

El programa muestra `Z` y el valor de cada `x`.

### Solución infactible

Ocurre cuando una variable artificial `R` permanece en la base con un valor mayor que `0.001`.

Las restricciones originales son incompatibles.

### Solución ilimitada

Ocurre cuando existe una columna que debe entrar, pero ningún coeficiente positivo permite seleccionar una fila de salida.

El valor de Z puede crecer o disminuir indefinidamente según el objetivo.

---

## 11. Variables internas principales

| Variable | Tipo | Qué contiene |
|---|---|---|
| `M` | `float` o entero | Penalización grande |
| `objetivo` | `str` | `"max"` o `"min"` |
| `num_x` | `int` | Cantidad de variables originales |
| `coef_z` | `list[float]` | Coeficientes de Z |
| `num_rest` | `int` | Cantidad de restricciones |
| `restricciones` | `list` | Coeficientes, signos y lados derechos |
| `columnas` | `list[str]` | Nombres de todas las columnas |
| `base` | `list[str]` | Variable básica de cada fila |
| `vars_extra` | `list` | Holguras, excesos y artificiales |
| `tabla` | `list[list[float]]` | Tabla simplex completa |
| `col_pivote` | `int` | Índice de la columna que entra |
| `fila_pivote` | `int` | Índice de la fila que sale |
| `pivote` | `float` | Valor usado para pivotear |
| `iteracion` | `int` | Número de iteración |

---

## 12. Supuestos y limitaciones

- Las variables originales se consideran mayores o iguales a cero.
- Los valores deben poder convertirse con `float`.
- `M` está fijo en `1000`.
- La tolerancia para los pivotes es `0.00001`.
- La tolerancia para variables artificiales positivas es `0.001`.
- No hay interfaz gráfica.
- No hay validación avanzada para valores incorrectos.
- Los cálculos pueden presentar pequeños errores por punto flotante.
- Las tablas grandes pueden requerir desplazamiento horizontal en consola.

---

## 13. Archivos del proyecto

- [gran_m.py](gran_m.py): contiene toda la lógica del método.
- [README.md](README.md): explica el proyecto y el funcionamiento interno del código.
