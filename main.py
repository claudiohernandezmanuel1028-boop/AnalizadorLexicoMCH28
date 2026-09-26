import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEXER_EXE = os.path.join(BASE_DIR, "build", "lexer.exe")

NOMBRES_TOKEN = {
    "PALABRA_RESERVADA":   "Palabra Reservada",
    "IDENTIFICADOR":       "Identificador",
    "NUMERO_ENTERO":       "Número Entero",
    "NUMERO_DECIMAL":      "Número Decimal",
    "CADENA":              "Cadena de Texto",
    "OP_SUMA":             "Operador Suma",
    "OP_RESTA":            "Operador Resta",
    "OP_MULTIPLICACION":   "Operador Multiplicación",
    "OP_DIVISION":         "Operador División",
    "OP_ASIGNACION":       "Operador Asignación",
    "OP_IGUAL":            "Operador Igual",
    "OP_DIFERENTE":        "Operador Diferente",
    "OP_MAYOR":            "Operador Mayor que",
    "OP_MENOR":            "Operador Menor que",
    "OP_MAYOR_IGUAL":      "Operador Mayor o Igual",
    "OP_MENOR_IGUAL":      "Operador Menor o Igual",
    "OP_AND":              "Operador AND",
    "OP_OR":               "Operador OR",
    "OP_NOT":              "Operador NOT",
    "PARENTESIS_ABRE":     "Paréntesis Abre",
    "PARENTESIS_CIERRA":   "Paréntesis Cierra",
    "LLAVE_ABRE":          "Llave Abre",
    "LLAVE_CIERRA":        "Llave Cierra",
    "CORCHETE_ABRE":       "Corchete Abre",
    "CORCHETE_CIERRA":     "Corchete Cierra",
    "PUNTO_COMA":          "Punto y Coma",
    "COMA":                "Coma",
    "ERROR_LEXICO":        "⚠ Error Léxico",
}


class AnalizadorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Claudio — ClaudioComp")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#1e1e2e")
        self._construir_interfaz()

    def _construir_interfaz(self):
        frame_titulo = tk.Frame(self.root, bg="#181825", pady=10)
        frame_titulo.pack(fill=tk.X)

        tk.Label(
            frame_titulo,
            text="🔍 Compilador Claudio",
            font=("Segoe UI", 16, "bold"),
            bg="#181825",
            fg="#cdd6f4",
        ).pack()

        tk.Label(
            frame_titulo,
            text="Manuel Claudio Hernandez  |  2-21-0644",
            font=("Segoe UI", 10),
            bg="#181825",
            fg="#cba6f7",
        ).pack()

        frame_principal = tk.Frame(self.root, bg="#1e1e2e")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._construir_panel_editor(frame_principal)
        self._construir_panel_tokens(frame_principal)
        self._construir_barra_botones()
        self._construir_barra_estado()

    def _construir_panel_editor(self, parent):
        frame = tk.Frame(parent, bg="#1e1e2e")
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(
            frame,
            text="📝 Código Fuente ClaudioComp",
            font=("Segoe UI", 10, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa",
        ).pack(anchor="w", pady=(0, 3))

        frame_editor = tk.Frame(frame, bg="#313244", bd=1, relief=tk.FLAT)
        frame_editor.pack(fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(frame_editor, bg="#45475a")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(frame_editor, orient=tk.HORIZONTAL, bg="#45475a")
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.editor = tk.Text(
            frame_editor,
            font=("Consolas", 12),
            bg="#1e1e2e",
            fg="#cdd6f4",
            insertbackground="#f5c2e7",
            selectbackground="#45475a",
            wrap=tk.NONE,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.editor.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.editor.yview)
        scroll_x.config(command=self.editor.xview)

        self.editor.insert(
            "1.0",
            "// Escribe tu código ClaudioComp aquí\n"
            "int edad = 20;\n"
            "float precio = 150.50;\n\n"
            "if (edad >= 18) {\n"
            "    precio = precio + 10;\n"
            "}\n",
        )

    def _construir_panel_tokens(self, parent):
        frame = tk.Frame(parent, bg="#1e1e2e")
        frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(
            frame,
            text="🧩 Tokens Encontrados",
            font=("Segoe UI", 10, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa",
        ).pack(anchor="w", pady=(0, 3))

        frame_tabla = tk.Frame(frame, bg="#313244")
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("#", "Lexema", "Tipo de Token", "Línea")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
        )

        self.tabla.heading("#",             text="#")
        self.tabla.heading("Lexema",        text="Lexema")
        self.tabla.heading("Tipo de Token", text="Tipo de Token")
        self.tabla.heading("Línea",         text="Línea")

        self.tabla.column("#",             width=45,  anchor=tk.CENTER)
        self.tabla.column("Lexema",        width=130, anchor=tk.W)
        self.tabla.column("Tipo de Token", width=200, anchor=tk.W)
        self.tabla.column("Línea",         width=55,  anchor=tk.CENTER)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1e1e2e",
            foreground="#cdd6f4",
            rowheight=24,
            fieldbackground="#1e1e2e",
            font=("Consolas", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#313244",
            foreground="#89b4fa",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
        )
        style.map("Treeview", background=[("selected", "#45475a")])

        self.tabla.tag_configure("error",        foreground="#f38ba8", background="#2a1a1a")
        self.tabla.tag_configure("reservada",    foreground="#cba6f7")
        self.tabla.tag_configure("numero",       foreground="#fab387")
        self.tabla.tag_configure("cadena",       foreground="#a6e3a1")
        self.tabla.tag_configure("operador",     foreground="#89dceb")
        self.tabla.tag_configure("identificador",foreground="#cdd6f4")

        scroll_tabla = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_tabla.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tabla.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame_errores = tk.Frame(frame, bg="#1e1e2e")
        self.frame_errores.pack(fill=tk.X, pady=(6, 0))

        tk.Label(
            self.frame_errores,
            text="⚠ Errores Léxicos",
            font=("Segoe UI", 10, "bold"),
            bg="#1e1e2e",
            fg="#f38ba8",
        ).pack(anchor="w")

        frame_txt_err = tk.Frame(self.frame_errores, bg="#2a1a1a", height=100)
        frame_txt_err.pack(fill=tk.X)
        frame_txt_err.pack_propagate(False)

        scroll_err = tk.Scrollbar(frame_txt_err, bg="#45475a")
        scroll_err.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_errores = tk.Text(
            frame_txt_err,
            font=("Consolas", 10),
            bg="#2a1a1a",
            fg="#f38ba8",
            relief=tk.FLAT,
            borderwidth=0,
            padx=8,
            pady=5,
            state=tk.DISABLED,
            yscrollcommand=scroll_err.set,
        )
        self.txt_errores.pack(fill=tk.BOTH, expand=True)
        scroll_err.config(command=self.txt_errores.yview)

    def _construir_barra_botones(self):
        frame = tk.Frame(self.root, bg="#181825", pady=8)
        frame.pack(fill=tk.X, padx=10)

        estilo_btn = {
            "font": ("Segoe UI", 10, "bold"),
            "relief": tk.FLAT,
            "cursor": "hand2",
            "padx": 18,
            "pady": 6,
            "bd": 0,
        }

        tk.Button(
            frame,
            text="▶  Analizar",
            bg="#89b4fa",
            fg="#1e1e2e",
            activebackground="#74c7ec",
            command=self.analizar,
            **estilo_btn,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            frame,
            text="🗑  Limpiar",
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            command=self.limpiar,
            **estilo_btn,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            frame,
            text="📂  Cargar Archivo",
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            command=self.cargar_archivo,
            **estilo_btn,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            frame,
            text="💾  Guardar Resultados",
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            command=self.guardar_resultados,
            **estilo_btn,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            frame,
            text="✕  Salir",
            bg="#f38ba8",
            fg="#1e1e2e",
            activebackground="#eba0ac",
            command=self.root.quit,
            **estilo_btn,
        ).pack(side=tk.RIGHT)

    def _construir_barra_estado(self):
        frame = tk.Frame(self.root, bg="#181825", pady=5)
        frame.pack(fill=tk.X)

        self.lbl_tokens = tk.Label(
            frame,
            text="Tokens encontrados: 0",
            font=("Segoe UI", 9),
            bg="#181825",
            fg="#a6e3a1",
        )
        self.lbl_tokens.pack(side=tk.LEFT, padx=15)

        self.lbl_errores = tk.Label(
            frame,
            text="Errores léxicos: 0",
            font=("Segoe UI", 9),
            bg="#181825",
            fg="#f38ba8",
        )
        self.lbl_errores.pack(side=tk.LEFT, padx=15)

        self.lbl_estado = tk.Label(
            frame,
            text="Listo",
            font=("Segoe UI", 9),
            bg="#181825",
            fg="#6c7086",
        )
        self.lbl_estado.pack(side=tk.RIGHT, padx=15)

    def analizar(self):
        if not os.path.exists(LEXER_EXE):
            messagebox.showerror(
                "Error",
                f"No se encontró el analizador léxico.\n\n"
                f"Ejecuta primero build_lexer.bat para compilarlo.\n\n"
                f"Ruta esperada: {LEXER_EXE}"
            )
            return

        codigo = self.editor.get("1.0", tk.END)
        if not codigo.strip():
            messagebox.showwarning("Aviso", "El editor está vacío. Escribe código ClaudioComp primero.")
            return

        self.lbl_estado.config(text="Analizando...", fg="#f9e2af")
        self.root.update()

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".claudio", delete=False, encoding="utf-8"
            ) as f_entrada:
                f_entrada.write(codigo)
                ruta_entrada = f_entrada.name

            ruta_salida = ruta_entrada + ".tokens"

            cmd = f'"{LEXER_EXE}" "{ruta_entrada}" "{ruta_salida}"'
            resultado = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if resultado.returncode != 0:
                messagebox.showerror("Error del analizador", resultado.stderr or "Error desconocido al ejecutar el analizador.")
                return

            self._mostrar_tokens(ruta_salida)

        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "El análisis tardó demasiado. Verifica tu código.")
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))
        finally:
            try:
                os.unlink(ruta_entrada)
                if os.path.exists(ruta_salida):
                    os.unlink(ruta_salida)
            except Exception:
                pass

        self.lbl_estado.config(text="Análisis completado", fg="#a6e3a1")

    def _mostrar_tokens(self, ruta_salida):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        self.txt_errores.config(state=tk.NORMAL)
        self.txt_errores.delete("1.0", tk.END)

        if not os.path.exists(ruta_salida):
            messagebox.showwarning("Aviso", "No se generaron tokens. El código puede estar vacío.")
            return

        conteo_tokens = 0
        conteo_errores = 0
        errores_lista = []

        with open(ruta_salida, "r", encoding="utf-8") as f:
            for numero, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea:
                    continue

                partes = linea.split("|")
                if len(partes) != 4:
                    continue

                tipo_raw, lexema, tipo_token, num_linea = partes
                nombre_token = NOMBRES_TOKEN.get(tipo_token, tipo_token)

                if tipo_raw == "ERROR":
                    tag = "error"
                    conteo_errores += 1
                    nombre_token = "⚠ Error Léxico — Carácter no reconocido"
                    errores_lista.append(
                        f"  Línea {num_linea}  |  Lexema: '{lexema}'  |  Descripción: Carácter no reconocido en ClaudioComp"
                    )
                elif tipo_token == "PALABRA_RESERVADA":
                    tag = "reservada"
                    conteo_tokens += 1
                elif tipo_token in ("NUMERO_ENTERO", "NUMERO_DECIMAL"):
                    tag = "numero"
                    conteo_tokens += 1
                elif tipo_token == "CADENA":
                    tag = "cadena"
                    conteo_tokens += 1
                elif tipo_token.startswith("OP_"):
                    tag = "operador"
                    conteo_tokens += 1
                else:
                    tag = "identificador"
                    conteo_tokens += 1

                self.tabla.insert(
                    "",
                    tk.END,
                    values=(numero, lexema, nombre_token, num_linea),
                    tags=(tag,),
                )

        if errores_lista:
            self.txt_errores.insert(tk.END, "\n".join(errores_lista))
        else:
            self.txt_errores.insert(tk.END, "  ✓ No se encontraron errores léxicos.")
            self.txt_errores.config(fg="#a6e3a1")

        self.txt_errores.config(state=tk.DISABLED, fg="#f38ba8" if errores_lista else "#a6e3a1")

        self.lbl_tokens.config(text=f"Tokens encontrados: {conteo_tokens}")
        self.lbl_errores.config(
            text=f"Errores léxicos: {conteo_errores}",
            fg="#f38ba8" if conteo_errores > 0 else "#a6e3a1",
        )

    def limpiar(self):
        self.editor.delete("1.0", tk.END)
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.txt_errores.config(state=tk.NORMAL)
        self.txt_errores.delete("1.0", tk.END)
        self.txt_errores.config(state=tk.DISABLED)
        self.lbl_tokens.config(text="Tokens encontrados: 0")
        self.lbl_errores.config(text="Errores léxicos: 0", fg="#f38ba8")
        self.lbl_estado.config(text="Listo", fg="#6c7086")

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Abrir archivo ClaudioComp",
            filetypes=[
                ("Archivos ClaudioComp", "*.claudio *.txt"),
                ("Todos los archivos", "*.*"),
            ],
            initialdir=os.path.join(BASE_DIR, "examples"),
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", contenido)
                self.lbl_estado.config(
                    text=f"Archivo cargado: {os.path.basename(ruta)}", fg="#a6e3a1"
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar_resultados(self):
        items = self.tabla.get_children()
        if not items:
            messagebox.showwarning("Aviso", "No hay resultados para guardar. Analiza el código primero.")
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
        )
        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("=" * 65 + "\n")
                f.write("  RESULTADOS DEL ANÁLISIS LÉXICO ClaudioComp\n")
                f.write("=" * 65 + "\n")
                f.write(f"{'#':<5} {'Lexema':<20} {'Tipo de Token':<30} {'Línea':<6}\n")
                f.write("-" * 65 + "\n")
                for item in items:
                    vals = self.tabla.item(item)["values"]
                    f.write(f"{str(vals[0]):<5} {str(vals[1]):<20} {str(vals[2]):<30} {str(vals[3]):<6}\n")
                f.write("=" * 65 + "\n")
                f.write(f"\n{self.lbl_tokens.cget('text')}\n{self.lbl_errores.cget('text')}\n")

            messagebox.showinfo("Guardado", f"Resultados guardados en:\n{ruta}")
            self.lbl_estado.config(text="Resultados guardados", fg="#a6e3a1")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorApp(root)
    root.mainloop()
