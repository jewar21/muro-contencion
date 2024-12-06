import os
import tkinter as tk

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from math import atan, degrees

from views.predimensioning import Predimensioning
from models.seismic_data import get_municipality, get_seismic_info
from models.project_data import CONCRETE_VALUES, FORM_FIELDS
from controllers.design_logic import calculate_design_logic


class DesignParameters(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo de Muros - Parámetros de Diseño")
        self.geometry("900x600")
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
        img = img.resize((390, 390), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(left_frame, image=img_tk)
        label_img.image = img_tk
        label_img.pack()

        # Lado derecho: Formulario
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        title = tk.Label(
            right_frame, text="PARÁMETROS DE DISEÑO", font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        self.entries = {}
        
        # Frame para organizar los campos en forma de tabla
        form_frame = tk.Frame(right_frame)
        form_frame.pack(fill="x", pady=5)

        for label_text, symbol, key, unit in FORM_FIELDS:
            # Crear un frame para cada fila
            row_frame = tk.Frame(form_frame)
            row_frame.pack(fill="x", pady=5)
            
            # Label principal
            label = tk.Label(row_frame, text=label_text, anchor="e", width=30)
            label.pack(side="left", padx=(0, 5))
            
            # Símbolo (si existe)
            if symbol:
                symbol_label = tk.Label(row_frame, text=symbol, width=6, font=("Arial", 8) )
                symbol_label.pack(side="left", padx=(0, 5))
            
            # Entry o Combobox
            if key == "project_location":
                widget = ttk.Combobox(
                    row_frame,
                    state="readonly",
                    values=get_municipality(),
                    width=20
                )
                widget.bind("<<ComboboxSelected>>", self.calculate_aa)
            elif key == "concrete_resistance":
                widget = ttk.Combobox(
                    row_frame,
                    state="readonly",
                    values=CONCRETE_VALUES,
                    width=12
                )
            else:
                widget = tk.Entry(row_frame, width=15)
            widget.pack(side="left", padx=(0, 5))
            self.entries[key] = widget

            # Unidad (si existe)
            if unit:
                unit_label = tk.Label(row_frame, text=unit, width=5)
                unit_label.pack(side="left")

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
        seismic_info = get_seismic_info(location)
        aa_value = seismic_info["Aa"] if seismic_info else "0.0"
        self.entries["aa"].delete(0, tk.END)
        self.entries["aa"].insert(0, aa_value)

    def get_factor(self, value, ranges, default=0):
        """
        Obtiene el factor correspondiente a un valor según los rangos especificados.
        """
        for min_val, max_val, factor in ranges:
            if min_val <= value <= max_val:
                return factor
        return default
    
    def calculate_design(self):
        try:
            # Lógica de cálculo usando los valores ingresados 
            data = {key: entry.get() for key, entry in self.entries.items()}
            wall_height = float(data.get("wall_height", 0))  # H
            
            # Validar la altura del muro
            if wall_height <= 0:
                raise ValueError("La altura del muro debe ser mayor a 0.")
            
            # Cálculo de la base del muro (B)
            base_factor = self.get_factor(wall_height, [
                (1.5, 2, 0.5),
                (2, 2.5, 0.49),
                (2.5, 4.5, 0.48),
                (4.5, 6, 0.47),
            ])
            base_muro = wall_height * base_factor
            
            # Cálculo del pie (b1)
            pie_factor = self.get_factor(base_muro, [
                (0.5, 1, 0.25),
                (1, 1.5, 0.26),
                (1.5, 2, 0.27),
                (2, 2.5, 0.28),
                (2.5, 3, 0.29),
            ])
            pie = base_muro * pie_factor
            
            # Cálculo del talón (b3)
            talon_factor = self.get_factor(base_muro, [
                (0.5, 1, 0.45),
                (1, 1.5, 0.55),
                (1.5, 2, 0.56),
                (2, 2.5, 0.57),
                (2.5, 3, 0.58),
            ])
            talon = base_muro * talon_factor
            
            # Cálculo de la base corona (b2min)
            base_corona = self.get_factor(wall_height, [
                (1.5, 3.5, 0.25),
                (3.5, 5.5, 0.30),
            ], default=0.35)
            
            # Cálculo de la base inferior (b2max)
            base_abajo = base_muro - pie - talon
            
            # Cálculo de la altura de zapata (d)
            altura_zapata = self.get_factor(wall_height, [
                (1.5, 2, 0.20),
                (2, 2.5, 0.18),
                (2.5, 3, 0.15),
            ], default=0.11) * wall_height
            
             # Cálculo de la altura de la pantalla (h)
            altura_pantalla = wall_height - altura_zapata
            
            # Cálculo del ángulo de inclinación del vástago (β)
            inclinacion = degrees(atan((base_abajo - base_corona) / altura_pantalla))
            
            # Resultados
            results = {
                "Base del muro": base_muro,
                "Pie": pie,
                "Talón": talon,
                "Base corona": base_corona,
                "Base abajo": base_abajo,
                "Altura de zapata": altura_zapata,
                "h": altura_pantalla,
                "Ángulo de inclinación del Vástago": inclinacion,
            }
            
            # Mostrar resultados
            print(results)
            Predimensioning(self, results)

        except ValueError as e:
            tk.messagebox.showerror("Error", f"Entrada inválida: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def clear_entries(self):
        if messagebox.askyesno(
            "Confirmación", "¿Estás seguro de que deseas limpiar los campos?"
        ):
            for key, entry in self.entries.items():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set("")


if __name__ == "__main__":
    app = DesignParameters()
    app.mainloop()
