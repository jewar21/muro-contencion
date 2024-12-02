import os
import tkinter as tk

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from views.predimensioning import Predimensioning
from controllers.design_logic import calculate_design_logic


class DesignParameters(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo de Muros - Parámetros de Diseño")
        self.geometry("800x600")
        self.resizable(False, False)

        # Layout general
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.grid(sticky="nsew")

        # Lado izquierdo: Imagen
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10)
        img_path = os.path.join("assets", "images", "Dibujo1-Presentación1.png")
        img = Image.open(img_path)
        img = img.resize((400, 320), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(left_frame, image=img_tk)
        label_img.image = img_tk
        label_img.pack()

        # Lado derecho: Formulario
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        title = tk.Label(
            right_frame, text="PÁRAMETROS DE DISEÑO", font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # Campos de entrada
        fields = [
            ("Ángulo de fricción (°):", "angle_friction"),
            ("Ángulo de fricción suelo-muro (°):", "angle_soil_wall"),
            ("Peso unitario del concreto (kN/m³):", "unit_weight"),
            ("Resistencia del acero (MPa):", "steel_resistance"),
            ("Altura de muro (H) (m):", "wall_height"),
            ("Ubicación del proyecto:", "project_location"),
            ("Aa (automático):", "aa"),
        ]

        self.entries = {}

        for field, key in fields:
            label = tk.Label(right_frame, text=field)
            label.pack(anchor="w", pady=5)
            if key == "project_location":
                combo = ttk.Combobox(
                    right_frame,
                    state="readonly",
                    values=[
                        "Ábrego",
                        "Arboledas",
                        "Bochalema",
                        "Bucarasica",
                        "Cáchira",
                        "Cácota",
                        "Chinácota",
                        "Chitagá",
                        "Convención",
                        "Cúcuta",
                        "Cucutilla",
                        "Durania",
                        "El Carmen",
                        "El Tarra",
                        "El Zulia",
                        "Gramalote",
                        "Hacarí",
                        "Herrán",
                        "Labateca",
                        "La Esperanza",
                        "La Playa",
                        "Los Patios",
                        "Lourdes",
                        "Mutiscua",
                        "Ocaña",
                        "Pamplona",
                        "Pamplonita",
                        "Puerto Santander",
                        "Ragonvalia",
                        "Salazar",
                        "San Calixto",
                        "San Cayetano",
                        "Santiago",
                        "Sardinata",
                        "Silos",
                        "Teorama",
                        "Tibú",
                        "Toledo",
                        "Villa Caro",
                        "Villa del Rosario",
                        "Otro", #En caso de que esto sea la selección, el usuario deberá ingresar el parametro
                    ],
                )
                combo.pack(fill="x", pady=5)
                combo.bind(
                    "<<ComboboxSelected>>", self.calculate_aa
                )  # Actualiza Aa automáticamente
                self.entries[key] = combo
            else:
                entry = tk.Entry(right_frame)
                entry.pack(fill="x", pady=5)
                self.entries[key] = entry

        # Reglas y botones
        rules = tk.Label(
            right_frame,
            text="F.S Volcamiento < 3.00 | F.S Deslizamiento > 2.00\nRecubrimiento mínimo: 75 mm",
            font=("Arial", 10, "italic"),
        )
        rules.pack(pady=10)

        btn_calculate = tk.Button(
            right_frame, text="Calcular Diseño", command=self.calculate_design
        )
        btn_calculate.pack(side="left", padx=5)

        btn_new = tk.Button(
            right_frame, text="Nuevo Diseño", command=self.clear_entries
        )
        btn_new.pack(side="left", padx=5)

        btn_exit = tk.Button(right_frame, text="Salir", command=self.quit)
        btn_exit.pack(side="left", padx=5)

    def calculate_aa(self, event):
        location = self.entries["project_location"].get()
        aa_value = {
            "Ábrego": "0.1",
            "Arboledas": "0.2",
            "Bochalema": "0.3",
        }.get(location, "0.0")
        self.entries["aa"].delete(0, tk.END)
        self.entries["aa"].insert(0, aa_value)

    def calculate_design(self):
        # Lógica de cálculo usando los valores ingresados
        # Predimensioning(tk.Toplevel(self.root), data)  # Abrir nueva ventana
        data = {key: entry.get() for key, entry in self.entries.items()}
        result = calculate_design_logic(data)
        print("Resultados:", result)
        
    #     try:             
    #         data = {key: entry.get() for key, entry in self.entries.items()}
    #         required_fields = ["angle_friction", "unit_weight", "steel_resistance", "wall_height"]
    #         for field in required_fields:
    #             if not data[field]:
    #                 raise ValueError(f"El campo '{field}' es obligatorio")
    #         # Valida que ciertos campos sean numéricos
    #         numeric_fields = ["angle_friction", "unit_weight", "steel_resistance", "wall_height"]
    #         for field in numeric_fields:
    #             if not data[field].replace('.', '', 1).isdigit():
    #                 raise ValueError(f"El campo '{field}' debe ser un número.")
                
    #         print("Datos capturados:", data)
    #     except ValueError as e:
    #         messagebox.showinfo('Error de validación', str(e))

    def clear_entries(self):
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas limpiar los campos?"):
            for key, entry in self.entries.items():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set("")


if __name__ == "__main__":
    app = DesignParameters()
    app.mainloop()
