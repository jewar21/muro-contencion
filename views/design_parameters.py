import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from views.predimensioning import Predimensioning
from models.seismic_data import get_municipality, get_seismic_info
from models.project_data import (
    CONCRETE_VALUES,
    DIENTE_VALUES,
    TYPE_SOIL_VALUES,
    FORM_FIELDS
)
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
        """ Configura la interfaz gráfica del formulario """
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.grid(sticky="nsew")

        # Lado Izquierdo - Imagen
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10)
        img_path = os.path.join("assets", "images", "imagen_main.png")

        try:
            img = Image.open(img_path).resize((390, 390), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(left_frame, image=img_tk)
            label_img.image = img_tk
            label_img.grid()
        except FileNotFoundError:
            tk.Label(left_frame, text="Imagen no encontrada",
                     font=("Arial", 12, "bold")).grid()

        # Selección de Diseño
        select_frame = tk.Label(left_frame)
        select_frame.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Label(select_frame, text="Seleccione el tipo de diseño: ",
                 font=("Arial", 12)).grid(row=0, column=0, padx=3)

        self.design_button = ttk.Combobox(select_frame, state="readonly",
                                          values=["Con inclinación", "Sin inclinación - vías", "Sin inclinación"], width=20)
        self.design_button.set("Sin inclinación - vías")
        self.design_button.grid(row=0, column=1, pady=5)

        # Lado Derecho - Formulario
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        tk.Label(right_frame, text="PARÁMETROS DE DISEÑO",
                 font=("Arial", 16, "bold")).pack(pady=10)

        self.entries = {}
        form_frame = tk.Frame(right_frame)
        form_frame.pack(fill="x", pady=5)

        for label_text, symbol, key, unit in FORM_FIELDS:
            row_frame = tk.Frame(form_frame)
            row_frame.pack(fill="x", pady=5)

            tk.Label(row_frame, text=label_text, anchor="e",
                     width=30).pack(side="left", padx=(0, 5))

            if symbol:
                tk.Label(row_frame, text=symbol, width=6, font=(
                    "Arial", 8)).pack(side="left", padx=(0, 5))

            widget = self.create_input_widget(row_frame, key)
            widget.pack(side="left", padx=(0, 5))
            self.entries[key] = widget

            if unit:
                tk.Label(row_frame, text=unit, width=5).pack(side="left")

        # Botones
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Calcular Diseño",
                  command=self.calculate_design).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Nuevo Diseño",
                  command=self.clear_entries).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Salir", command=self.quit).pack(
            side="left", padx=5)

    def create_input_widget(self, parent, key):
        """ Crea y retorna el widget de entrada adecuado """
        if key == "project_location":
            widget = ttk.Combobox(parent, state="readonly",
                                  values=get_municipality() + ["Otro"], width=20)
            widget.bind("<<ComboboxSelected>>", self.handle_project_location)
        elif key in {"aa", "pga"}:
            widget = tk.Entry(parent, width=15, state="disabled")
        elif key == "concrete_resistance":
            widget = ttk.Combobox(parent, state="readonly",
                                  values=CONCRETE_VALUES, width=12)
        elif key == "steel_resistance":
            widget = tk.Label(parent, text="420", font=(
                "Arial", 10), width=12, anchor="w")
        elif key in {"diente", "type_soil"}:
            widget = ttk.Combobox(
                parent, state="readonly", values=DIENTE_VALUES if key == "diente" else TYPE_SOIL_VALUES, width=12)
        else:
            widget = tk.Entry(parent, width=15)

        return widget

    def handle_project_location(self, event):
        """ Actualiza los valores de Aa y PGA según la ubicación seleccionada """
        location = self.entries["project_location"].get()
        aa_entry, pga_entry = self.entries["aa"], self.entries["pga"]

        if location == "Otro":
            self.update_entry(aa_entry, "", True)
            self.update_entry(pga_entry, "", True)
        else:
            factor_value = self.calculate_factor(location)
            self.update_entry(aa_entry, factor_value["aa"])
            self.update_entry(pga_entry, factor_value["pga"])

    def update_entry(self, entry, value, enable=False):
        """ Actualiza un campo de entrada con un valor específico """
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value if value is not None else "0.0")
        if not enable:
            entry.config(state="disabled")

    def calculate_factor(self, location):
        """ Obtiene la aceleración sísmica Aa y PGA de la ubicación seleccionada """
        seismic_info = get_seismic_info(location) or {}
        return {
            "aa": seismic_info.get("Aa", "0.0"),
            "pga": seismic_info.get("pga", "0.0")
        }

    def calculate_design(self):
        """ Llama a la lógica de cálculo y muestra los resultados """
        try:
            select_design = self.design_button.get()
            data = self.get_all_entries()
            results = calculate_design_logic(select_design, data)
            Predimensioning(self, results, data)
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def get_all_entries(self):
        """ Obtiene y valida todos los valores ingresados por el usuario """
        return {key: (entry.get().strip().replace(",", ".") if isinstance(entry, (tk.Entry, ttk.Combobox)) else "420") for key, entry in self.entries.items()}

    def clear_entries(self):
        """ Limpia todos los campos del formulario """
        for widget in self.entries.values():
            if isinstance(widget, (tk.Entry, ttk.Combobox)):
                widget.delete(0, tk.END)


if __name__ == "__main__":
    app = DesignParameters()
    app.mainloop()