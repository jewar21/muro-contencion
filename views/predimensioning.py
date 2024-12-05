import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from controllers.design_logic import calculate_predimensioning
from controllers.verification_logic import check_compliance


class Predimensioning(tk.Toplevel):
    def __init__(self, root, input_data):
        super().__init__(root)
        self.input_data = input_data
        self.title("Cálculo de Muros - Predimensionamiento")
        self.geometry("900x600")
        self.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal con grid
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.grid(sticky="nsew")
        # main_frame.grid_rowconfigure(0, weight=1)
        # main_frame.grid_columnconfigure(1, weight=1)
        # main_frame.pack(fill="both", expand=True)

        # Imagen a la izquierda
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Cargar y mostrar la imagen
        img_path = os.path.join(
            "assets", "images", "design.png"
        )  # Cambia la ruta según tu imagen
        try:
            img = Image.open(img_path)
            img = img.resize((500, 400), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(left_frame, image=img_tk)
            label_img.image = img_tk  # Necesario para evitar que se recolecte basura
            label_img.pack(fill="y", expand=True)
        except FileNotFoundError:
            tk.Label(
                left_frame, text="Imagen no encontrada", font=("Arial", 12, "bold")
            ).pack()

        # Tablas a la derecha
        right_frame = tk.Frame(main_frame, width=300)
        right_frame.pack_propagate(False)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Tabla 1: Predimensionamiento Calculado
        self.create_table(
            right_frame,
            "Predimensionamiento Calculado",
            [
                ("Base del muro (B)", "m"),
                ("Pie (b1)", "m"),
                ("Talón (b3)", "m"),
                ("Base corona (b2min)", "m"),
                ("Base máxima (b2max)", "m"),
                ("Altura de zapata (d)", "m"),
                ("Pantalla (h)", "m"),
                ("Inclinación de vástago (beta)", "°"),
            ],
            "predimensioning_results",
            headers=["Ubicación", "Valor", "Unidad"],
            total_width=300,
        )

        # Encabezado y botón para verificaciones
        verif_title_frame = tk.Frame(right_frame)
        verif_title_frame.pack(fill="x", pady=5)

        verif_label = tk.Label(
            verif_title_frame, text="Verificaciones", font=("Arial", 12, "bold")
        )
        verif_label.pack(side="left", padx=5)

        verify_button = tk.Button(
            verif_title_frame,
            text="Verificar",
            font=("Arial", 12, "bold"),
            command=self.perform_verification,
        )
        verify_button.pack(side="left", padx=10)

        # Tabla 2: Verificaciones
        self.create_table(
            right_frame,
            "",
            [
                ("Factor de seguridad al volcamiento", ""),
                ("Factor de seguridad al deslizamiento", ""),
                ("Esfuerzo máximo a presión", ""),
                ("Esfuerzo mínimo a presión", ""),
            ],
            "verification_results",
            headers=["Parámetro", "Resultado"],
            total_width=300,
        )

        # Botón para cerrar al final
        close_button = tk.Button(right_frame, text="Cerrar", command=self.destroy)
        close_button.pack(pady=20)

        # Calcular predimensionamiento inicial
        self.calculate_predimensioning_results()

    def create_table(
        self, parent, title, columns, attribute_name, headers=None, total_width=300
    ):
        if title:
            title_label = tk.Label(
                parent, text=title, font=("Arial", 12, "bold"), anchor="w", bg="#f0f0f0"
            )
            title_label.pack(fill="x", pady=2)

        # Configuración dinámica de encabezados
        headers = headers if headers else ["Ubicación", "Valor", "Unidad"]
        column_width = total_width // len(
            headers
        )  # Divide el ancho total entre las columnas

        tree = ttk.Treeview(
            parent,
            columns=[f"col{i}" for i in range(len(headers))],
            show="headings",
            height=len(columns),
        )

        # Configuración de columnas según los encabezados
        for i, header in enumerate(headers):
            col_id = f"col{i}"
            tree.column(col_id, anchor="center", width=column_width, stretch=False)
            tree.heading(col_id, text=header)

        # Insertar filas iniciales
        for row in columns:
            tree.insert("", "end", values=row)

        tree.pack(pady=5)
        setattr(self, attribute_name, tree)

    def calculate_predimensioning_results(self):
        """
        Calcula los resultados del predimensionamiento y los actualiza en la primera tabla.
        """
        try:
            predimensioning_results = calculate_predimensioning(self.input_data)
            for i, (name, value, unit) in enumerate(predimensioning_results):
                self.predimensioning_results.item(
                    i, values=(name, f"{value:.2f}", unit)
                )
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Ocurrió un error al calcular el predimensionamiento:\n{e}"
            )

    def perform_verification(self):
        """
        Realiza las verificaciones y actualiza la segunda tabla con los resultados.
        """
        try:
            verification_results = check_compliance(self.input_data)
            for i, (name, result) in enumerate(verification_results):
                color = "green" if result == "CUMPLE" else "red"
                self.verification_results.item(
                    i, values=(name, result, ""), tags=(color,)
                )
                self.verification_results.tag_configure("green", foreground="green")
                self.verification_results.tag_configure("red", foreground="red")
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Ocurrió un error al verificar los resultados:\n{e}"
            )
