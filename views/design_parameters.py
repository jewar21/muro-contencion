import os
import tkinter as tk

from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from math import atan, degrees

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
        # Contenedor principal
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.grid(sticky="nsew")

        # Lado izquierdo: Imagen
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10)
        img_path = os.path.join(
            "assets", "images", "imagen_main.png")
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
                symbol_label = tk.Label(
                    row_frame, text=symbol, width=6, font=("Arial", 8)
                )
                symbol_label.pack(side="left", padx=(0, 5))

            # Entry o Combobox
            if key == "project_location":
                widget = ttk.Combobox(
                    row_frame,
                    state="readonly",
                    values=get_municipality() + ["Otro"],
                    width=20,
                )
                widget.bind("<<ComboboxSelected>>",
                            self.handle_project_location)
            elif key == "aa":  # Aceleración pico efectiva
                widget = tk.Entry(
                    row_frame, width=15, state="disabled"
                )  # Bloqueado por defecto
            elif key == "concrete_resistance":
                widget = ttk.Combobox(
                    row_frame, state="readonly", values=CONCRETE_VALUES, width=12
                )
            elif key == "steel_resistance":  # Para el caso de `fy`
                widget = tk.Label(
                    row_frame,
                    text="420",  # Valor constante
                    font=("Arial", 10),
                    width=12,
                    anchor="w",
                )
                self.entries[key] = 420
            elif key == "diente":
                widget = ttk.Combobox(
                    row_frame, state="readonly", values=DIENTE_VALUES, width=12
                )
            elif key == "type_soil":
                widget = ttk.Combobox(
                    row_frame, state="readonly", values=TYPE_SOIL_VALUES, width=12
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

    def handle_project_location(self, event):
        """
        Maneja la selección del proyecto. Si el usuario selecciona "Otro",
        habilita el campo para ingresar Aa manualmente.
        Si selecciona una ubicación predefinida, muestra el valor calculado de Aa.
        """
        location = self.entries["project_location"].get()
        aa_entry = self.entries["aa"]  # Campo de Aa
        pga_entry = self.entries["pga"]  # Campo de pga

        if location == "Otro":
            aa_entry.config(state="normal")  # Habilitar entrada manual
            aa_entry.delete(0, tk.END)  # Limpiar cualquier valor previo
            pga_entry.config(state="normal")
            pga_entry.delete(0, tk.END)
        else:
            # Deshabilitar el campo y calcular Aa automáticamente
            # Obtén el valor calculado de Aa
            factor_value = self.calculate_factor(location)
            # Habilitar temporalmente para insertar el valor
            aa_entry.config(state="normal")
            aa_entry.delete(0, tk.END)
            # Mostrar el valor calculado
            aa_entry.insert(0, factor_value["aa"])
            aa_entry.config(state="disabled")  # Bloquear nuevamente el campo
            # Mostrar el valor calculado
            pga_entry.insert(0, factor_value["pga"])
            pga_entry.config(state="disabled")  # Bloquear nuevamente el campo

    def calculate_factor(self, location):
        """
        Calcula el valor de Aa para una ubicación específica y lo devuelve.
        """
        seismic_info = get_seismic_info(location)  # Obtiene los datos sísmicos
        # Retorna Aa o un valor por defecto
        return {"aa": seismic_info.get("Aa", "0.0") if seismic_info else "0.0",
                "pga": seismic_info.get("pga", "0.0") if seismic_info else "0.0"}

    def get_factor(self, value, ranges, default=0):
        """
        Obtiene el factor correspondiente a un valor según los rangos especificados.
        """
        for min_val, max_val, factor in ranges:
            if min_val <= value <= max_val:
                return factor
        return default

    def calculate_design(self):
        # Llama a la lógica de cálculo y muestra los resultados en la interfaz.
        try:
            # Obtener los valores ingresados por el usuario
            data = {}
            for key, entry in self.entries.items():
                if isinstance(entry, (tk.Entry, ttk.Combobox)):
                    raw_value = entry.get().strip()
                    if raw_value == "":
                        raise ValueError(
                            f"El campo '{key}' está vacío. Por favor ingrese un valor.")
                    value = raw_value.replace(",", ".")  # Manejo de decimales
                    data[key] = value
                elif isinstance(entry, tk.Label):
                    data[key] = "420"
                else:
                    data[key] = entry  # Para valores fijos como fy
            # Llamar a la lógica de cálculo
            results = calculate_design_logic(data)
            Predimensioning(self, results, data)

        except ValueError as e:
            tk.messagebox.showerror("Error", f"Entrada inválida: {e}")
        except Exception as e:
            tk.messagebox.showerror(
                "Error", f"Ocurrió un error inesperado: {e}")

    def clear_entries(self):
        """
        Limpia todos los campos del formulario generados dinámicamente,
        incluidos combobox, entradas de texto y valores calculados.
        """
        if messagebox.askyesno(
            "Confirmación", "¿Estás seguro de que deseas limpiar todos los campos?"
        ):
            for key, widget in self.entries.items():
                # Limpiar Entry
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                # Limpiar Combobox
                elif isinstance(widget, ttk.Combobox):
                    widget.set("")
                # Ignorar Label fijo como fy
                elif isinstance(widget, tk.Label):
                    continue

            # Limpieza específica para campos mencionados
            if "project_location" in self.entries:
                self.entries["project_location"].set("")
            if "concrete_resistance" in self.entries:
                self.entries["concrete_resistance"].set("")

            # Mostrar un mensaje opcional de confirmación
            tk.messagebox.showinfo(
                "Formulario Limpiado",
                "Todos los campos han sido reiniciados correctamente.",
            )


if __name__ == "__main__":
    app = DesignParameters()
    app.mainloop()