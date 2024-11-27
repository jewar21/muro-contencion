import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from controllers.design_logic import calculate_predimensioning
from controllers.verification_logic import check_compliance

class Predimensioning:
    def __init__(self, root, input_data):
        self.root = root
        self.input_data = input_data  # Datos obtenidos de la primera interfaz
        self.root.title("Cálculo de Muros - Predimensionamiento")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.grid(sticky="nsew")

        # Lado izquierdo: Imagen
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10)
        img = Image.open("assets/images/predimension.png")
        img = img.resize((250, 450), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(left_frame, image=img_tk)
        label_img.image = img_tk
        label_img.pack()

        # Lado derecho: Tablas
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        title = tk.Label(right_frame, text="Predimensionamiento Calculado", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Tabla 1: Predimensionamiento
        self.create_table(right_frame, "Predimensionamiento Calculado", [
            ("Base del muro (B)", "m"),
            ("Pie (b1)", "m"),
            ("Talón (b3)", "m"),
            ("Base corona (b2min)", "m"),
            ("Base máxima (b2max)", "m"),
            ("Altura de zapata (d)", "m"),
            ("Pantalla (h)", "m"),
            ("Inclinación de vástago (beta)", "°"),
        ], "predimensioning_results")

        # Tabla 2: Verificaciones
        self.create_table(right_frame, "Verificaciones", [
            ("Factor de seguridad al volcamiento", ""),
            ("Factor de seguridad al deslizamiento", ""),
            ("Esfuerzo máximo a presión", ""),
            ("Esfuerzo mínimo a presión", ""),
        ], "verification_results")

        # Botón para cerrar
        close_button = tk.Button(right_frame, text="Cerrar", command=self.root.quit)
        close_button.pack(pady=20)

        # Realizar cálculos
        self.calculate_results()

    def create_table(self, parent, title, columns, attribute_name):
        label = tk.Label(parent, text=title, font=("Arial", 12, "bold"))
        label.pack(pady=5)

        tree = ttk.Treeview(parent, columns=("value", "unit"), show="headings", height=len(columns))
        tree.column("value", anchor="center")
        tree.column("unit", anchor="center")
        tree.heading("value", text="Valor")
        tree.heading("unit", text="Unidad")

        for name, unit in columns:
            tree.insert("", "end", values=(name, "-", unit))

        tree.pack(pady=10)
        setattr(self, attribute_name, tree)

    def calculate_results(self):
        # Predimensionamiento
        predimensioning_results = calculate_predimensioning(self.input_data)
        for i, (name, value, unit) in enumerate(predimensioning_results):
            self.predimensioning_results.item(i, values=(name, value, unit))

        # Verificaciones
        verification_results = check_compliance(self.input_data)
        for i, (name, result) in enumerate(verification_results):
            color = "green" if result == "CUMPLE" else "red"
            self.verification_results.item(i, values=(name, result), tags=(color,))
            self.verification_results.tag_configure("green", foreground="green")
            self.verification_results.tag_configure("red", foreground="red")
