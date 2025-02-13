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
        img_path = os.path.join(
            "assets", "images", "Dibujo1-Presentación1.png")
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

        if location == "Otro":
            aa_entry.config(state="normal")  # Habilitar entrada manual
            aa_entry.delete(0, tk.END)  # Limpiar cualquier valor previo
        else:
            # Deshabilitar el campo y calcular Aa automáticamente
            # Obtén el valor calculado de Aa
            aa_value = self.calculate_aa(location)
            # Habilitar temporalmente para insertar el valor
            aa_entry.config(state="normal")
            aa_entry.delete(0, tk.END)
            aa_entry.insert(0, aa_value)  # Mostrar el valor calculado
            aa_entry.config(state="disabled")  # Bloquear nuevamente el campo

    def calculate_aa(self, location):
        """
        Calcula el valor de Aa para una ubicación específica y lo devuelve.
        """
        seismic_info = get_seismic_info(location)  # Obtiene los datos sísmicos
        # Retorna Aa o un valor por defecto
        return seismic_info.get("Aa", "0.0") if seismic_info else "0.0"

    def get_factor(self, value, ranges, default=0):
        """
        Obtiene el factor correspondiente a un valor según los rangos especificados.
        """
        for min_val, max_val, factor in ranges:
            if min_val <= value <= max_val:
                return factor
        return default

    def calculate_design(self):
        factors_by_aa = {
            # (Rangos y factores para inclinación 0)
            0.15: {"base_factor": [(1.5, 2, 0.5), (2, 2.5, 0.49), (2.5, 3, 0.48), (3.5, 5.5, 0.48), (5.5, 6, 0.47)],
                   "pie_factor": [(0.5, 1, 0.23), (1, 1.5, 0.26), (1.5, 2, 0.27), (2, 3, 0.29)],
                   "talon_factor": [(0.5, 1, 0.44), (1, 1.5, 0.50), (1.5, 2, 0.55), (2, 2.5, 0.56), (2.5, 3, 0.57)]
                   },
            0.20: {"base_factor": [(1.5, 2, 0.53), (2, 2.5, 0.52), (2.5, 3, 0.51), (3, 6, 0.50)],
                   "pie_factor": [(0.5, 1, 0.23), (1, 1.5, 0.25), (1.5, 2.5, 0.28), (2.5, 3, 0.29)],
                   "talon_factor": [(0.5, 1, 0.46), (1, 1.5, 0.50), (1.5, 2, 0.55), (2, 2.5, 0.57), (2.5, 3, 0.58)]
                   },
            0.25: {"base_factor": [(1.5, 2, 0.56), (2, 2.5, 0.55), (2.5, 3, 0.54), (3, 5, 0.53), (5, 6, 0.52)],
                   "pie_factor": [(0.5, 1, 0.23), (1, 1.5, 0.25), (1.5, 2, 0.27), (2, 2.5, 0.28), (2.5, 3.5, 0.29)],
                   "talon_factor": [(0.5, 1, 0.46), (1, 1.5, 0.50), (1.5, 2, 0.56), (2, 2.5, 0.57), (2.5, 3, 0.58), (3, 3.5, 0.59)]
                   },
            0.30: {"base_factor": [(1.5, 2, 0.59), (2, 2.5, 0.57), (2.5, 3, 0.56), (3, 6, 0.55)],
                   "pie_factor": [(0.5, 1, 0.24), (1, 1.5, 0.25), (1.5, 2, 0.27), (2, 2.5, 0.28), (2.5, 3.5, 0.29)],
                   "talon_factor": [(0.5, 1, 0.46), (1, 1.5, 0.50), (1.5, 2, 0.56), (2, 2.5, 0.57), (2.5, 3, 0.58), (3, 3.5, 0.59)]
                   },
            0.35: {"base_factor": [(1.5, 2, 0.63), (2, 2.5, 0.60), (2.5, 3.5, 0.59), (3.5, 5.5, 0.58), (5.5, 6, 0.57)],
                   "pie_factor": [(0.5, 1, 0.24), (1, 1.5, 0.25), (1.5, 2, 0.27), (2, 2.5, 0.28), (2.5, 3, 0.29), (3, 3.5, 0.30)],
                   "talon_factor": [(0.5, 1, 0.46), (1, 1.5, 0.50), (1.5, 2, 0.56), (2, 2.5, 0.57), (2.5, 3, 0.58), (3, 3.5, 0.59)]
                   },
        }

        factors_by_aa_inclined = {
            # (Rangos y factores para inclinación > 0)
            0.15: {"base_factor": [(1.5, 2, 0.64), (2, 5.5, 0.63), (5.5, 6, 0.62)],
                   "pie_factor": [(0.5, 1, 0.24), (1, 1.5, 0.25), (1.5, 2, 0.28), (2, 2.5, 0.29), (2.5, 4, 0.30)],
                   "talon_factor": [(0.5, 1, 0.49), (1, 1.5, 0.50), (1.5, 2, 0.55), (2, 2.5, 0.57), (2.5, 3, 0.58), (3, 3.5, 0.59), (3.5, 4, 0.60)]
                   },
            0.20: {"base_factor": [(1.5, 2, 0.7), (2, 2.5, 0.69), (2.5, 3, 0.68), (3, 6, 0.67)],
                   "pie_factor": [(1, 1.5, 0.26), (1.5, 2, 0.28), (2, 3.5, 0.30), (3.5, 4.5, 0.31)],
                   "talon_factor": [(1, 1.5, 0.50), (1.5, 2, 0.55), (2, 2.5, 0.57), (2.5, 3, 0.58), (3, 4.5, 0.59)]
                   },
            0.25: {"base_factor": [(1.5, 2, 0.76), (2, 2.5, 0.75), (2.5, 4.5, 0.74), (4.5, 6, 0.73)],
                   "pie_factor": [(1, 1.5, 0.27), (1.5, 2, 0.28), (2, 3.5, 0.30), (3.5, 4.5, 0.31)],
                   "talon_factor": [(1, 1.5, 0.51), (1.5, 2, 0.55), (2, 2.5, 0.57), (2.5, 3, 0.58), (3, 3.5, 0.59), (3.5, 4.5, 0.60)]
                   },
            0.30: {"base_factor": [(1.5, 2, 0.83), (2, 3, 0.82), (3, 3.5, 0.81), (3.5, 6, 0.80)],
                   "pie_factor": [(1, 1.5, 0.27), (1.5, 2, 0.28), (2, 2.5, 0.29), (2.5, 3.5, 0.30), (3.5, 5, 0.31)],
                   "talon_factor": [(1, 1.5, 0.53), (1.5, 2, 0.56), (2, 2.5, 0.58), (2.5, 3, 0.59), (3, 4, 0.60), (4, 5, 0.61)]
                   },
            0.35: {"base_factor": [(1.5, 2.5, 0.96), (2.5, 3.5, 0.95), (3.5, 6, 0.94)],
                   "pie_factor": [(1, 1.5, 0.27), (1.5, 2, 0.28), (2, 2.5, 0.29), (2.5, 3, 0.30), (3, 6, 0.31)],
                   "talon_factor": [(1, 1.5, 0.55), (1.5, 2, 0.56), (2, 2.5, 0.57), (2.5, 3, 0.59), (3, 4, 0.60), (4, 4.5, 0.61), (4.5, 6, 0.62)]
                   },
        }
        
        try:
            # Lógica de cálculo usando los valores ingresados
            data = {}
            for key, entry in self.entries.items():
                if isinstance(entry, (tk.Entry, ttk.Combobox)):
                    raw_value = entry.get().strip()
                    if raw_value == "":
                        raise ValueError(
                            f"El campo '{key}' está vacío. Por favor ingrese un valor.")
                    # Reemplazar comas con puntos para manejar valores decimales
                    value = raw_value.replace(",", ".")
                    data[key] = value
                else:
                    # Para valores fijos como fy
                    data[key] = entry

            wall_height = float(data.get("wall_height", 0))  # H
            angle_inclination = float(data.get("angle_inclination", 0))
            # el valor de fy, resistencia del acero
            fy = data.get("steel_resistance", 420)
            aa = float(data.get("aa", 0))

            # Validar ángulo de inclinación del relleno (i)
            if angle_inclination > 45:
                raise ValueError(
                    "El ángulo de inclinación del relleno (i) no puede ser mayor a 45 grados.")

            # Validar la altura del muro
            if wall_height < 1.5 or wall_height > 6.0:
                raise ValueError(
                    "Altura no admitida: Ingrese una altura entre 1.5m y 6m."
                )

            # Seleccionar el conjunto de factores según el ángulo
            factors = factors_by_aa if angle_inclination == 0 else factors_by_aa_inclined

            # Validar que Aa esté en los factores
            if aa not in factors:
                raise ValueError(
                    f"El valor de Aa ({aa}) no es válido o no tiene factores asignados.")

            # Obtener factores para base, pie y talón
            base_factor = self.get_factor(
                wall_height, factors[aa]["base_factor"])
            base_muro = round((wall_height * base_factor), 2)

            pie_factor = self.get_factor(base_muro, factors[aa]["pie_factor"])
            talon_factor = self.get_factor(
                base_muro, factors[aa]["talon_factor"])

            pie = round((base_muro * pie_factor), 2)
            talon = round((base_muro * talon_factor), 2)

            # Cálculo de la base corona (b2min)
            base_corona = self.get_factor(
                wall_height,
                [
                    (1.5, 3.5, 0.25),
                    (3.5, 5.5, 0.30),
                ],
                default=0.35,
            )

            # Cálculo de la altura de zapata (d)
            altura_zapata = (
                self.get_factor(
                    wall_height,
                    [
                        (1.5, 2, 0.18),
                        (2, 2.5, 0.14),
                        (2.5, 3, 0.12),
                    ],
                    default=0.11,
                )
                * wall_height
            )

            # Cálculo de la base inferior (b2max)
            base_abajo = round((base_muro - pie - talon), 2)
            # Cálculo de la altura de la pantalla (h)
            altura_pantalla = round((wall_height - altura_zapata), 2)
            # Cálculo del ángulo de inclinación del vástago (β)
            inclinacion = round((degrees(
                atan((base_abajo - base_corona) / altura_pantalla))), 2)
            # print("inclinacion", base_abajo, base_corona, altura_pantalla)

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
                "Resistencia del acero (fy)": fy,
            }

            # Mostrar resultados
            print(results)
            Predimensioning(self, results)

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
