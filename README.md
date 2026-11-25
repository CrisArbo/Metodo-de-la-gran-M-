# Método de la Gran M - Programación Lineal

## 1. Descripción general del software

Este programa resuelve problemas de **programación lineal** utilizando el **Método simplex** y el **Método de la Gran M**.

Cuenta con una **interfaz gráfica sencilla y moderna construida en Python con Tkinter**, diseñada para ser intuitiva, rápida de usar y totalmente transparente en su procedimiento matemático.

El usuario puede:
1. Elegir si el objetivo es **Maximizar** o **Minimizar**.
2. Definir la cantidad de **variables de decisión** ($x_1, x_2, \dots$) y la cantidad de **restricciones**.
3. Generar dinámicamente las casillas del formulario con un solo clic.
4. Ingresar los coeficientes de la **función objetivo ($Z$)**.
5. Ingresar cada **restricción**, seleccionando el signo correspondiente ($\le$, $\ge$, $=$) y el valor del lado derecho.
6. Resolver el problema y visualizar en pantalla la **Tabla Inicial**, todas las **Iteraciones Simplex paso a paso** con las operaciones de Gauss-Jordan, y el **Resultado Final** (valor óptimo de $Z$ y valores de las variables).

El programa no utiliza librerías externas de optimización ni paquetes comerciales (como SciPy, PuLP o Gurobi). Todo el algoritmo simplex manual está programado desde cero usando únicamente la librería estándar de Python.

---

## 2. Tecnologías utilizadas y justificación

| Tecnología / Módulo | Tipo | Para qué se usa y por qué se eligió |
|---|---|---|
| Python 3 | Lenguaje base | Lenguaje de programación principal, legible, multiplataforma y estándar en ingeniería. |
| `tkinter` | Módulo estándar | Proporciona la ventana gráfica de usuario. Viene preinstalado con Python, por lo que no requiere descargas con `pip`. |
| `tkinter.ttk` | Submódulo gráfico | Widgets con diseño gráfico más moderno y limpio (botones, casillas, marcos y listas desplegables). |
| `tkinter.scrolledtext` | Submódulo gráfico | Área de texto con barras de desplazamiento para visualizar las tablas simplex completas sin cortes. |
| `tkinter.messagebox` | Submódulo gráfico | Ventanas emergentes de aviso en caso de que el usuario ingrese letras, símbolos o campos incompletos. |
| Listas y matrices de Python | Estructura de datos | Almacenan coeficientes, filas de restricciones, nombres de columnas y la tabla simplex completa. |
| Operaciones aritméticas manuales | Algoritmo | Implementan las operaciones elementales de fila de Gauss-Jordan paso a paso. |

El programa **no requiere instalar librerías externas**. Funciona en cualquier equipo con Python 3 instalado.

---

## 3. Requisitos, descarga y ejecución

### 3.1. Requisitos

- **Python 3** (versión 3.8 o superior). Se descarga gratuitamente desde [python.org](https://www.python.org/downloads/).
- En Windows y macOS, `tkinter` viene incluido automáticamente con la instalación estándar de Python.
- En sistemas Linux (Ubuntu/Debian), si no estuviera instalado, se instala con:
  ```bash
  sudo apt install python3-tk
  ```

---

### 3.2. Cómo descargar el proyecto

Puedes obtener el programa en cualquier computadora mediante cualquiera de estas opciones:

#### Opción A: Clonar con Git (Recomendada)
Abre la terminal o PowerShell y escribe:

```bash
git clone https://github.com/CrisArbo/Metodo-de-la-gran-M-.git
cd Metodo-de-la-gran-M-
```

#### Opción B: Descargar directamente el archivo `gran_m.py`
Desde la terminal:

```powershell
curl -O https://raw.githubusercontent.com/CrisArbo/Metodo-de-la-gran-M-/main/gran_m.py
```

O desde el navegador: abre [https://raw.githubusercontent.com/CrisArbo/Metodo-de-la-gran-M-/main/gran_m.py](https://raw.githubusercontent.com/CrisArbo/Metodo-de-la-gran-M-/main/gran_m.py), haz clic derecho y selecciona **Guardar como...** con el nombre `gran_m.py`.

#### Opción C: Descargar como archivo ZIP
1. Entra al repositorio en GitHub: [https://github.com/CrisArbo/Metodo-de-la-gran-M-](https://github.com/CrisArbo/Metodo-de-la-gran-M-)
2. Haz clic en el botón verde **Code** y elige **Download ZIP**.
3. Descomprime el archivo y abre una terminal en la carpeta resultante.

---

### 3.3. Ejecución

Dentro de la carpeta donde se encuentra `gran_m.py`, ejecuta:

```powershell
python gran_m.py
```

Se abrirá inmediatamente la ventana gráfica del programa.

---

## 4. Modo de uso paso a paso

1. **Configuración inicial:**
   - Selecciona si deseas **Maximizar** o **Minimizar**.
   - Ingresa cuántas **variables** tiene tu problema (por ejemplo, `2` o `3`).
   - Ingresa cuántas **restricciones** tiene tu problema.
   - Haz clic en el botón **Generar campos**.

2. **Ingreso de datos en el formulario:**
   - En la sección **Función Objetivo (Z)**, escribe los coeficientes que acompañan a cada variable ($x_1, x_2, \dots$).
   - En la sección **Restricciones**, escribe los coeficientes de cada variable para cada fila.
   - Selecciona en el selector desplegable el signo de la restricción: `<=`, `>=` o `=`.
   - Escribe el valor del lado derecho (término independiente) después del signo.
   - *Nota:* Si una variable no participa en una restricción o en la función objetivo, puedes escribir `0` o dejar la casilla en blanco (el programa la interpretará automáticamente como `0.0`).

3. **Resolución:**
   - Haz clic en **Resolver**.
   - En la parte inferior se generarán todas las tablas simplex alineadas:
     - **Tabla inicial:** Con las variables de holgura ($S$), exceso ($E$) y artificiales ($R$) añadidas y la fila $Z$ debidamente limpiada de penalizaciones.
     - **Iteraciones:** Cada paso indicará qué variable entra a la base, qué variable sale y cómo se transformaron las filas tras el pivoteo de Gauss-Jordan.
     - **Resultado final:** Mostrará el valor óptimo de $Z$ y el valor numérico de cada variable de decisión. Si el problema no tiene solución, indicará claramente si es *infactible* o *no acotado*.

4. **Nuevo problema:**
   - Puedes hacer clic en **Limpiar** para vaciar las casillas y resolver otro ejercicio.

---

## 5. Explicación del código paso a paso

El programa está contenido en el archivo [gran_m.py](gran_m.py) y se divide en dos grandes bloques: la **lógica matemática del método** y la **interfaz gráfica de usuario**.

### 5.1. Declaración de la constante M

```python
M = 1000.0
```

- **Qué hace:** Define el valor numérico de la constante de penalización $M$.
- **Por qué se usa:** En programación lineal, $M$ representa un número positivo arbitrariamente grande. Como las computadoras trabajan con números concretos, se utiliza `1000.0`, un valor suficientemente alto frente a los coeficientes normales para garantizar que el algoritmo expulse las variables artificiales de la base.

---

### 5.2. Función matemática: `resolver_gran_m`

Esta función contiene toda la resolución simplex manual y recibe 4 parámetros:
- `objetivo`: texto `"max"` o `"min"`.
- `num_x`: cantidad de variables originales ($x_1, x_2, \dots$).
- `coef_z`: lista con los coeficientes numéricos de la función objetivo.
- `restricciones`: lista donde cada elemento es `[fila_coeficientes, signo, lado_derecho]`.

#### Paso 1: Normalización de lados derechos negativos
```python
restricciones_proc = []
for fila_orig, signo_orig, rhs_orig in restricciones:
    fila = list(fila_orig)
    signo = signo_orig
    rhs = float(rhs_orig)
    if rhs < 0:
        fila = [-val for val in fila]
        rhs = -rhs
        if signo == "<=":
            signo = ">="
        elif signo == ">=":
            signo = "<="
    restricciones_proc.append([fila, signo, rhs])
```
- **Por qué:** El Método Simplex exige que todos los valores del lado derecho sean no negativos ($b \ge 0$). Si un usuario ingresa por ejemplo $x_1 + x_2 \le -5$, se multiplica toda la inecuación por $-1$, quedando $-x_1 - x_2 \ge 5$.

#### Paso 2: Creación de variables de holgura (S), exceso (E) y artificiales (R)
```python
for i in range(num_rest):
    signo = restricciones_proc[i][1]
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
```
- **Por qué:** 
  - Restricciones $\le$: se suma una variable de holgura $+S$ que entra a la base inicial.
  - Restricciones $\ge$: se resta una variable de exceso $-E$ y se suma una artificial $+R$. La variable $R$ entra a la base inicial.
  - Restricciones $=$: se suma una variable artificial $+R$ que entra a la base inicial.

#### Paso 3: Construcción de la fila Z y penalización de las variables R
```python
fila_z = [0.0] * total_cols
for j in range(num_x):
    fila_z[j] = -float(coef_z[j])

for c in range(total_cols):
    if columnas[c].startswith("R"):
        fila_z[c] = M if objetivo == "max" else -M
```
- **Por qué:** 
  - En la ecuación simplex $Z - c_1 x_1 - \dots = 0$, los coeficientes de las variables de decisión entran con signo negativo a la fila $Z$.
  - Las variables artificiales $R$ se penalizan fuertemente: $+M$ en maximización (para que resten en la ganancia) y $-M$ en minimización.

#### Paso 4: Construcción de la matriz de la tabla
```python
tabla = [fila_z]
for i in range(num_rest):
    fila = [0.0] * total_cols
    for j in range(num_x):
        fila[j] = float(restricciones_proc[i][0][j])
    fila[-1] = float(restricciones_proc[i][2])
    tabla.append(fila)

for idx_extra in range(len(vars_extra)):
    fila_destino = vars_extra[idx_extra][1] + 1
    valor = vars_extra[idx_extra][2]
    tabla[fila_destino][num_x + idx_extra] = valor
```
- **Por qué:** Se crea una matriz bidimensional (lista de listas) donde la fila 0 es la fila $Z$ y las filas siguientes corresponden a cada restricción con sus coeficientes y su término independiente al final.

#### Paso 5: Limpieza de la fila Z (Condición Canónica)
```python
for i in range(num_rest):
    if base[i].startswith("R"):
        col_r = columnas.index(base[i])
        multiplicador = tabla[0][col_r]
        for c in range(total_cols):
            tabla[0][c] = tabla[0][c] - multiplicador * tabla[i + 1][c]
```
- **Por qué:** En el Método Simplex, toda variable básica **debe tener coeficiente cero** en la fila $Z$. Como las variables $R$ empiezan en la base pero tienen coeficientes $\pm M$ en la fila $Z$, debemos restar de la fila $Z$ el múltiplo de la fila de cada restricción donde se encuentra $R$.

#### Paso 6: Bucle de iteraciones simplex (Gauss-Jordan)
```python
while iteracion <= 100:
    # 1. Columna pivote (variable que entra)
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

    if col_pivote == -1:
        break # Ya no hay mejora posible: solucion optima alcanzada
```
- **Por qué:** 
  - En **Maximizar**, entra la variable con el coeficiente más negativo en la fila $Z$.
  - En **Minimizar**, entra la variable con el coeficiente más positivo en la fila $Z$.
  - Si ningún coeficiente califica, el algoritmo concluye porque se alcanzó el óptimo.

```python
    # 2. Fila pivote (variable que sale - razon minima)
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
        return False, historial, "Problema no acotado (crece al infinito)."
```
- **Por qué:** 
  - Se divide la columna Solución entre el elemento de la columna pivote, **únicamente si este es estrictamente positivo** ($> 0$).
  - La fila con la menor razón positiva determina qué variable básica llega primero a cero y debe salir de la base.
  - Si ningún elemento es positivo, significa que la variable puede crecer indefinidamente sin violar restricciones, por lo que el problema es **no acotado**.

```python
    # 3. Operaciones de fila de Gauss-Jordan
    base[fila_pivote - 1] = columnas[col_pivote]
    pivote = tabla[fila_pivote][col_pivote]

    for c in range(total_cols):
        tabla[fila_pivote][c] = tabla[fila_pivote][c] / pivote

    for f in range(len(tabla)):
        if f != fila_pivote:
            factor = tabla[f][col_pivote]
            for c in range(total_cols):
                tabla[f][c] = tabla[f][c] - factor * tabla[fila_pivote][c]
```
- **Por qué:** 
  - Se actualiza la variable en la base.
  - Se divide la fila pivote entre el elemento pivote para convertirlo en `1.0`.
  - En todas las demás filas (incluyendo la fila $Z$), se resta `factor * fila_pivote` para convertir en `0.0` los demás elementos de esa columna.

#### Paso 7: Comprobación de factibilidad y extracción de la solución
```python
for i in range(len(base)):
    if base[i].startswith("R") and tabla[i + 1][-1] > 0.001:
        return False, historial, "Problema infactible (no existe solucion factible)."
```
- **Por qué:** Si el algoritmo se detiene pero una variable artificial $R$ sigue en la base con valor positivo, significa que las restricciones se contradicen y el problema no tiene solución factible en el mundo real.
- Si todas las $R$ salieron o valen cero, el valor óptimo de $Z$ se extrae de `tabla[0][-1]` y los valores de cada variable $x_j$ se leen de su fila correspondiente en la base.

---

### 5.3. Interfaz gráfica: Clase `InterfazGranM`

La clase `InterfazGranM` organiza visualmente todos los elementos de Tkinter.

#### 1. Constructor `__init__`
```python
def __init__(self, root):
    self.root = root
    self.root.title("Metodo de la Gran M - Programacion Lineal")
    self.root.geometry("900x700")
    self.entries_z = []
    self.entries_rest = []
    self.crear_widgets()
    self.generar_campos()
```
- **Qué hace:** Inicializa la ventana con tamaño 900x700 píxeles, prepara las listas de casillas y construye los componentes visuales.

#### 2. Canvas con Scrollbar para los datos
```python
self.canvas = tk.Canvas(frame_datos, height=170, highlightthickness=0)
scrollbar = ttk.Scrollbar(frame_datos, orient="vertical", command=self.canvas.yview)
self.frame_interior = ttk.Frame(self.canvas)
```
- **Por qué:** Si el usuario ingresa 8 o 10 restricciones, una ventana estática se desbordaría de la pantalla. Al incrustar el `frame_interior` dentro de un `Canvas` con barra de desplazamiento vertical, el formulario puede desplazarse suavemente sin importar cuántas restricciones tenga el modelo.

#### 3. Método `generar_campos`
- **Qué hace:** Lee `entry_x` y `entry_rest`. Borra los campos anteriores con `.destroy()` y crea mediante un ciclo `for` las casillas de texto para $Z$ y cada una de las restricciones con su selector de signo y lado derecho.
- **Validación:** Si el usuario escribe texto o números menores a 1, muestra una alerta con `messagebox.showwarning` en lugar de caerse.

#### 4. Método `resolver`
- **Qué hace:** 
  1. Recorre `entries_z` y `entries_rest` obteniendo los valores escritos con `.get()`.
  2. Convierte los textos a `float`. Si un campo quedó vacío, lo asume automáticamente como `0.0`.
  3. Si el usuario ingresó letras o símbolos inválidos, captura el error con `try ... except ValueError` y notifica con `messagebox.showerror` indicando exactamente en qué variable o restricción está el error.
  4. Llama a `resolver_gran_m(...)`.
  5. Inserta el historial de tablas en el widget `ScrolledText` y actualiza la etiqueta de estado con el resultado final.

#### 5. Widget `ScrolledText` con fuente `Consolas`
```python
self.txt_salida = scrolledtext.ScrolledText(frame_res, font=("Consolas", 10), wrap=tk.NONE)
```
- **Por qué:** La fuente `Consolas` es monoespaciada (cada carácter, número o espacio tiene exactamente el mismo ancho físico en pantalla). Esto garantiza que las columnas de las tablas simplex se mantengan perfectamente derechas y legibles.

---

## 6. Casos especiales y cómo los detecta el programa

| Caso | Condición matemática | Cómo lo detecta el código | Mensaje mostrado |
|---|---|---|---|
| **Solución óptima** | Todos los coeficientes de la fila $Z$ cumplen la condición de parada ($\ge 0$ en Max, $\le 0$ en Min) y no quedan variables $R > 0$ en la base. | `col_pivote == -1` y ninguna $R$ básica tiene valor $> 0.001$. | `Solucion optima: Z = ...` |
| **Problema no acotado** | Existe una variable candidata a entrar, pero todos los coeficientes de su columna en las restricciones son $\le 0$. | `fila_pivote == -1` tras recorrer todas las filas con `elemento > 0.00001`. | `Problema no acotado (crece al infinito).` |
| **Problema infactible** | El algoritmo termina las iteraciones, pero una variable artificial $R$ permanece en la base con valor positivo. | Al finalizar, `base[i].startswith("R") and tabla[i + 1][-1] > 0.001`. | `Problema infactible (no existe solucion factible).` |

---

## 7. Archivos del proyecto

- [gran_m.py](gran_m.py): Código fuente completo del programa (algoritmo simplex manual e interfaz gráfica en Tkinter).
- [README.md](README.md): Documentación del proyecto, tecnologías y guía de uso.
- [GUIA_ESTUDIO_GRAN_M.md](GUIA_ESTUDIO_GRAN_M.md): Guía de estudio personal con fundamentos teóricos, deducción matemática y preguntas frecuentes de examen (ignorado en Git para uso privado).
