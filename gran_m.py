"""
Metodo de la Gran M - Programacion Lineal
Interfaz grafica con Tkinter para resolver problemas de optimizacion.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Valor M grande para penalizar las variables artificiales
M = 1000.0


def resolver_gran_m(objetivo, num_x, coef_z, restricciones):
    """
    Aplica el algoritmo del Metodo de la Gran M paso a paso.
    Retorna: (exito, texto_completo_tablas, resumen_final)
    """
    historial = []

    # Si el lado derecho es negativo, multiplicamos la fila por -1 y cambiamos el signo
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

    num_rest = len(restricciones_proc)
    columnas = [f"x{j + 1}" for j in range(num_x)]
    base = []
    vars_extra = []
    cont_s, cont_e, cont_r = 1, 1, 1

    # Identificar variables de holgura (S), exceso (E) y artificiales (R)
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

    for item in vars_extra:
        columnas.append(item[0])
    columnas.append("Solucion")
    total_cols = len(columnas)

    # Armar la fila Z
    fila_z = [0.0] * total_cols
    for j in range(num_x):
        fila_z[j] = -float(coef_z[j])

    for c in range(total_cols):
        if columnas[c].startswith("R"):
            fila_z[c] = M if objetivo == "max" else -M

    # Armar las filas de las restricciones
    tabla = [fila_z]
    for i in range(num_rest):
        fila = [0.0] * total_cols
        for j in range(num_x):
            fila[j] = float(restricciones_proc[i][0][j])
        fila[-1] = float(restricciones_proc[i][2])
        tabla.append(fila)

    # Ubicar los coeficientes de las variables extra (+1 o -1)
    for idx_extra in range(len(vars_extra)):
        fila_destino = vars_extra[idx_extra][1] + 1
        valor = vars_extra[idx_extra][2]
        tabla[fila_destino][num_x + idx_extra] = valor

    # Limpiar las variables artificiales R de la fila Z
    for i in range(num_rest):
        if base[i].startswith("R"):
            col_r = columnas.index(base[i])
            multiplicador = tabla[0][col_r]
            for c in range(total_cols):
                tabla[0][c] = tabla[0][c] - multiplicador * tabla[i + 1][c]

    def texto_tabla(titulo):
        lineas = [f"=== {titulo} ==="]
        header = "Base   |" + "".join(f"{col:>9}" for col in columnas)
        lineas.append(header)
        lineas.append("-" * len(header))
        nombres = ["Z"] + base
        for idx in range(len(tabla)):
            lineas.append(f"{nombres[idx]:<6} |" + "".join(f"{num:9.2f}" for num in tabla[idx]))
        lineas.append("")
        return "\n".join(lineas)

    historial.append(texto_tabla("TABLA INICIAL"))

    # Iteraciones del metodo Simplex
    iteracion = 1
    while iteracion <= 100:
        # Columna que entra (columna pivote)
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
            break

        # Fila que sale (prueba de razon minima)
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
            historial.append("[!] El problema no tiene solucion acotada.")
            return False, "\n".join(historial), "Problema no acotado (crece al infinito)."

        # Pivoteo Gauss-Jordan
        base[fila_pivote - 1] = columnas[col_pivote]
        pivote = tabla[fila_pivote][col_pivote]

        for c in range(total_cols):
            tabla[fila_pivote][c] = tabla[fila_pivote][c] / pivote

        for f in range(len(tabla)):
            if f != fila_pivote:
                factor = tabla[f][col_pivote]
                for c in range(total_cols):
                    tabla[f][c] = tabla[f][c] - factor * tabla[fila_pivote][c]

        historial.append(texto_tabla(f"ITERACION {iteracion} (Entra: {columnas[col_pivote]} | Sale: fila {fila_pivote})"))
        iteracion += 1

    # Revisar si quedaron variables artificiales R en la base
    for i in range(len(base)):
        if base[i].startswith("R") and tabla[i + 1][-1] > 0.001:
            historial.append("[!] El problema no tiene solucion factible (variable R > 0 en la base).")
            return False, "\n".join(historial), "Problema infactible (no existe solucion factible)."

    z_optimo = tabla[0][-1]
    valores_x = []
    for j in range(num_x):
        nombre_x = f"x{j + 1}"
        if nombre_x in base:
            fila_x = base.index(nombre_x) + 1
            valores_x.append(f"{nombre_x} = {tabla[fila_x][-1]:.2f}")
        else:
            valores_x.append(f"{nombre_x} = 0.00")

    resumen_lineas = [
        "================ RESULTADO FINAL ================",
        f"Valor optimo de Z = {z_optimo:.2f}",
        "  " + ", ".join(valores_x)
    ]
    historial.append("\n".join(resumen_lineas))

    resumen_corto = f"Z = {z_optimo:.2f}  |  " + ", ".join(valores_x)
    return True, "\n".join(historial), resumen_corto


class InterfazGranM:
    """
    Ventana grafica sencilla con Tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Metodo de la Gran M - Programacion Lineal")
        self.root.geometry("900x700")

        self.entries_z = []
        self.entries_rest = []

        self.crear_widgets()
        self.generar_campos()

    def crear_widgets(self):
        # Panel superior de configuracion
        frame_config = ttk.LabelFrame(self.root, text="Configuracion", padding=10)
        frame_config.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_config, text="Objetivo:").grid(row=0, column=0, padx=5, sticky="w")
        self.var_objetivo = tk.StringVar(value="max")
        ttk.Radiobutton(frame_config, text="Maximizar", variable=self.var_objetivo, value="max").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(frame_config, text="Minimizar", variable=self.var_objetivo, value="min").grid(row=0, column=2, padx=5)

        ttk.Label(frame_config, text="Variables:").grid(row=0, column=3, padx=(15, 5))
        self.entry_x = ttk.Entry(frame_config, width=5)
        self.entry_x.insert(0, "3")
        self.entry_x.grid(row=0, column=4, padx=5)

        ttk.Label(frame_config, text="Restricciones:").grid(row=0, column=5, padx=(15, 5))
        self.entry_rest = ttk.Entry(frame_config, width=5)
        self.entry_rest.insert(0, "3")
        self.entry_rest.grid(row=0, column=6, padx=5)

        ttk.Button(frame_config, text="Generar campos", command=self.generar_campos).grid(row=0, column=7, padx=(15, 5))
        ttk.Button(frame_config, text="Limpiar", command=self.limpiar).grid(row=0, column=8, padx=5)

        # Panel de ingreso de datos
        frame_datos = ttk.LabelFrame(self.root, text="Datos del problema", padding=10)
        frame_datos.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)

        self.canvas = tk.Canvas(frame_datos, height=170, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_datos, orient="vertical", command=self.canvas.yview)
        self.frame_interior = ttk.Frame(self.canvas)

        self.frame_interior.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.frame_interior, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Boton resolver
        ttk.Button(self.root, text="Resolver", command=self.resolver).pack(fill=tk.X, padx=10, pady=5)

        # Panel de resultados
        frame_res = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        frame_res.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.lbl_estado = ttk.Label(frame_res, text="Esperando datos...", font=("Segoe UI", 9, "bold"))
        self.lbl_estado.pack(anchor="w", pady=(0, 5))

        self.txt_salida = scrolledtext.ScrolledText(frame_res, font=("Consolas", 10), wrap=tk.NONE)
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

    def generar_campos(self):
        """Crea las cajitas para Z y las restricciones segun los valores indicados."""
        try:
            num_x = int(self.entry_x.get().strip())
            num_rest = int(self.entry_rest.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Ingresa numeros enteros en variables y restricciones.")
            return

        if num_x < 1 or num_rest < 1:
            messagebox.showwarning("Error", "Debe haber al menos 1 variable y 1 restriccion.")
            return

        for widget in self.frame_interior.winfo_children():
            widget.destroy()

        self.entries_z = []
        self.entries_rest = []

        # Funcion Objetivo
        ttk.Label(self.frame_interior, text="Funcion Objetivo (Z):", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 4))
        frame_z = ttk.Frame(self.frame_interior)
        frame_z.grid(row=1, column=0, sticky="w", pady=(0, 10))

        ttk.Label(frame_z, text="Z = ").pack(side=tk.LEFT)
        for j in range(num_x):
            ent = ttk.Entry(frame_z, width=7)
            ent.pack(side=tk.LEFT, padx=2)
            self.entries_z.append(ent)
            txt = f" x{j + 1} + " if j < num_x - 1 else f" x{j + 1}"
            ttk.Label(frame_z, text=txt).pack(side=tk.LEFT)

        # Restricciones
        ttk.Label(self.frame_interior, text="Restricciones:", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 4))
        frame_rest_box = ttk.Frame(self.frame_interior)
        frame_rest_box.grid(row=3, column=0, sticky="w")

        for i in range(num_rest):
            fila = ttk.Frame(frame_rest_box)
            fila.pack(fill=tk.X, pady=2, anchor="w")

            ttk.Label(fila, text=f"R{i + 1}: ").pack(side=tk.LEFT)
            fila_entries = []
            for j in range(num_x):
                ent = ttk.Entry(fila, width=7)
                ent.pack(side=tk.LEFT, padx=2)
                fila_entries.append(ent)
                txt = f" x{j + 1} + " if j < num_x - 1 else f" x{j + 1} "
                ttk.Label(fila, text=txt).pack(side=tk.LEFT)

            cb_signo = ttk.Combobox(fila, values=["<=", ">=", "="], width=4, state="readonly")
            cb_signo.set("<=")
            cb_signo.pack(side=tk.LEFT, padx=4)

            ent_rhs = ttk.Entry(fila, width=8)
            ent_rhs.pack(side=tk.LEFT, padx=4)

            self.entries_rest.append((fila_entries, cb_signo, ent_rhs))

    def limpiar(self):
        """Limpia las cajitas de texto y el area de resultados."""
        for ent in self.entries_z:
            ent.delete(0, tk.END)
        for fila_ents, cb, ent_rhs in self.entries_rest:
            for ent in fila_ents:
                ent.delete(0, tk.END)
            cb.set("<=")
            ent_rhs.delete(0, tk.END)
        self.txt_salida.delete("1.0", tk.END)
        self.lbl_estado.config(text="Campos limpios.")

    def resolver(self):
        """Lee los datos ingresados, valida y ejecuta la solucion."""
        objetivo = self.var_objetivo.get()
        num_x = len(self.entries_z)

        # Leer coeficientes de Z
        coef_z = []
        for j, ent in enumerate(self.entries_z):
            txt = ent.get().strip()
            if not txt:
                coef_z.append(0.0)
            else:
                try:
                    coef_z.append(float(txt))
                except ValueError:
                    messagebox.showerror("Error", f"El coeficiente de x{j + 1} en Z no es valido.")
                    return

        # Leer restricciones
        restricciones = []
        for i, (fila_ents, cb, ent_rhs) in enumerate(self.entries_rest):
            fila = []
            for j, ent in enumerate(fila_ents):
                txt = ent.get().strip()
                if not txt:
                    fila.append(0.0)
                else:
                    try:
                        fila.append(float(txt))
                    except ValueError:
                        messagebox.showerror("Error", f"En R{i + 1}, el valor de x{j + 1} no es valido.")
                        return

            txt_rhs = ent_rhs.get().strip()
            if not txt_rhs:
                messagebox.showerror("Error", f"En R{i + 1}, falta ingresar el lado derecho.")
                return
            try:
                rhs = float(txt_rhs)
            except ValueError:
                messagebox.showerror("Error", f"En R{i + 1}, el lado derecho no es valido.")
                return

            restricciones.append([fila, cb.get(), rhs])

        exito, texto_tablas, resumen = resolver_gran_m(objetivo, num_x, coef_z, restricciones)

        self.txt_salida.delete("1.0", tk.END)
        self.txt_salida.insert(tk.END, texto_tablas)
        if exito:
            self.lbl_estado.config(text=f"Solucion optima: {resumen}")
        else:
            self.lbl_estado.config(text=f"Atencion: {resumen}")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazGranM(ventana)
    ventana.mainloop()
