import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class Predimensioning(tk.Toplevel):
    def __init__(self, root, input_data, full_data):
        super().__init__(root)
        self.input_data = input_data
        self.full_data = full_data
        self.title("Cálculo de Muros - Predimensionamiento")

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        self.geometry(f"{width}x{height}+0+0")
        self.resizable(False, False)

        # print("Datos ingresados por el usuario:", self.full_data)
        # print("Resultados de predimensionamiento:", self.input_data)

        # Calcular valores de verificación
        self.verification_results = self.calculate_verification_results()

        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.grid(sticky="nsew")

        # Imagen a la izquierda
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Mostrar imagen
        img_path = os.path.join(
            "assets", "images", "imagen_predimensioning.png")
        try:
            img = Image.open(img_path)
            img = img.resize((400, 300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(left_frame, image=img_tk)
            label_img.image = img_tk
            label_img.pack()
        except FileNotFoundError:
            tk.Label(left_frame, text="Imagen no encontrada",
                     font=("Arial", 12, "bold")).pack()

        # Tablas a la derecha
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Tabla Predimensionamiento Calculado
        predimensioning_title = tk.Label(
            right_frame, text="Predimensionamiento Calculado", font=("Arial", 12, "bold"))
        predimensioning_title.grid(pady=5)
        self.predimensioning_results = ttk.Treeview(
            right_frame, columns=("parameter", "value", "unit"), show="headings", height=8
        )
        self.predimensioning_results.heading("parameter", text="Parámetro")
        self.predimensioning_results.heading("value", text="Valor")
        self.predimensioning_results.heading("unit", text="Unidad")
        self.predimensioning_results.column("parameter", anchor="w", width=200)
        self.predimensioning_results.column(
            "value", anchor="center", width=100)
        self.predimensioning_results.column("unit", anchor="center", width=80)
        self.predimensioning_results.grid(pady=10)

        # Bloquear redimensionamiento y edición
        self.predimensioning_results["displaycolumns"] = (
            "parameter", "value", "unit")
        self.predimensioning_results.grid(pady=10)

        # Sección para las tres tablas alineadas horizontalmente
        verification_frame = tk.Frame(main_frame)
        verification_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Crear las tres tablas de verificación en horizontal
        self.create_verification_table(
            verification_frame,
            "VERIFICACIÓN DE LA ESTABILIDAD AL DESLIZAMIENTO DEL MURO",
            ("ESTADO LÍMITE", "CASO", "FX (KN)", "RR (KN)", "CUMPLE"),
            "deslizamiento",
            0
        )

        self.create_verification_table(
            verification_frame,
            "VERIFICACIÓN DE LA ESTABILIDAD AL VOLCAMIENTO DEL MURO",
            ("ESTADO LÍMITE", "CASO", "e (m)", "eₘₐₓ (m)", "CUMPLE"),
            "volcamiento",
            1
        )

        self.create_verification_table(
            verification_frame,
            "ESFUERZO ÚLTIMO ACTUANTE SOBRE SUELO NO ROCOSO",
            ("ESTADO LÍMITE", "CASO", "σᵥ (KN/m²)", "σₘₐₓ (KN/m²)", "CUMPLE"),
            "presion",
            2
        )

        # Sección para los botones
        buttons_frame = tk.Frame(right_frame)
        buttons_frame.grid(row=2, column=1, columnspan=2, pady=5)

        # Botón para realizar el diseño
        btn_calculate = tk.Button(
            buttons_frame, text="Calcular Vista",
            command=self.calculate_view
        )
        btn_calculate.grid(row=0, column=0, padx=5)

        # Botón para cerrar
        close_button = tk.Button(
            buttons_frame, text="Cerrar", command=self.destroy)
        close_button.grid(row=0, column=1, padx=5)

        # Llenar los datos
        self.calculate_predimensioning_results()

    def calculate_predimensioning_results(self):
        """
        Llena la tabla de predimensionamiento con los datos proporcionados.
        """
        try:
            mapping = [
                ("Base del muro (B)", "Base del muro", "m"),
                ("Pie (b1)", "Pie", "m"),
                ("Talón (b3)", "Talón", "m"),
                ("Base corona (b2min)", "Base corona", "m"),
                ("Base máxima (b2max)", "Base vástago", "m"),
                ("Altura de zapata (d)", "Altura de zapata", "m"),
                ("Pantalla (h)", "h", "m"),
                ("Inclinación de vástago (β)",
                 "Ángulo de inclinación del Vástago", "°"),
            ]
            for display_name, key, unit in mapping:
                value = self.input_data.get(key, 0.0)
                self.predimensioning_results.insert(
                    "", "end", values=(display_name, f"{value:.2f}", unit))
        except Exception as e:
            messagebox.showerror(
                "Error", f"Ocurrió un error al llenar los resultados:\n{e}")

    def calculate_view(self):
        select_design = self.design_button.get()
        print(f"Calculando diseño para: {select_design}")

    def create_verification_table(self, parent, title, columns, table_key, col_position):
        """
        Crea una tabla de verificación con los valores calculados.
        """
        frame = tk.Frame(parent)
        frame.grid(row=0, column=col_position, pady=5)

        # Título de la tabla
        table_title = tk.Label(frame, text=title, font=(
            "Arial", 10, "bold"), anchor="w")
        table_title.pack(fill="x")

        # Crear tabla
        table = ttk.Treeview(frame, columns=columns, show="headings", height=7)
        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=100)

        # Bloquear redimensionamiento y edición
        table["displaycolumns"] = columns
        table.pack(fill="x", padx=5, pady=5)

        # Llenar la tabla con los valores calculados
        self.populate_verification_table(table, table_key)

    def populate_verification_table(self, table, table_key):
        """
        Llena la tabla con datos calculados a partir de los valores ingresados.
        """
        data = self.verification_results.get(table_key, [])

        for row in data:
            table.insert("", "end", values=row)

    def calculate_verification_results(self):
        """
        Realiza cálculos basados en input_data y full_data y devuelve los resultados en un diccionario.
        """
        # Simulación de cálculos para las tablas
        return {
            "deslizamiento": [
                ("RESISTENCIA 1", "MÁXIMO", "100", "80", "SÍ"),
                ("", "MÍNIMO", "90", "85", "SÍ"),
                ("EVENTO EXTREMO I", "MÁXIMO", "85", "70", "NO"),
                ("", "MÍNIMO", "80", "75", "SÍ"),
                ("EVENTO EXTREMO II", "MÁXIMO", "85", "70", "NO"),
                ("", "MÍNIMO", "80", "75", "SÍ"),
                ("SERVICIO 1", "", "100", "80", "SÍ"),
            ],
            "volcamiento": [
                ("RESISTENCIA 1", "MÁXIMO", "200", "150", "Sí"),
                ("", "MÍNIMO", "180", "160", "Sí"),
            ],
            "carga": [
                ("CAPACIDAD CARGA", "MÁXIMO", "300", "250", "Sí"),
            ],
        }
