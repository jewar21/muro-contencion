import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

from views.predimensioning import Predimensioning
from models.seismic_data import get_municipality, get_seismic_info
from models.project_data import (
    CONCRETE_VALUES,
    DIENTE_VALUES,
    TYPE_SOIL_VALUES,
    FORM_FIELDS,
)
from controllers.design_logic import calculate_design_logic


class DesignParameters(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.title("Cálculo de Muros - Parámetros de Diseño")
        self.geometry("1100x700")
        self.resizable(False, False)

        self.entries = {}
        self.image_label = None
        self.image_objects = {}
        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=12)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=(0, 40), pady=20)

        # Imagen dinámica
        self.image_label = ctk.CTkLabel(left_frame, text="")
        self.image_label.pack(pady=(40, 10))
        # self.load_images()
        self.update_image("Sin inclinación - vías")

        # Combo tipo de diseño
        ctk.CTkLabel(left_frame, text="Tipo de diseño", font=ctk.CTkFont(size=14)).pack(
            pady=(0, 4)
        )
        self.design_button = ctk.CTkComboBox(
            left_frame,
            values=["Con inclinación", "Sin inclinación - vías", "Sin inclinación"],
            command=self.handle_design_change,
            width=240,
        )
        self.design_button.set("Selecciona un tipo")
        self.design_button.pack()

        # Formulario a la derecha
        right_frame = ctk.CTkFrame(main_frame, corner_radius=12, fg_color="#ffffff")
        right_frame.grid(row=0, column=1, pady=20)

        ctk.CTkLabel(
            right_frame,
            text="PARÁMETROS DE DISEÑO",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(10, 20))

        form_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_frame.pack()

        for label_text, symbol, key, unit in FORM_FIELDS:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=6)

            # Texto dividido si es muy largo
            display_text = (
                label_text
                if len(label_text) <= 35
                else f"{label_text[:35]}\n{label_text[35:]}"
            )
            ctk.CTkLabel(
                row, text=display_text, width=220, anchor="e", justify="right"
            ).pack(side="left", padx=(0, 10))

            if symbol:
                ctk.CTkLabel(row, text=symbol, width=40).pack(side="left")

            widget = self.create_input_widget(row, key)
            widget.pack(side="left", padx=5)
            self.entries[key] = widget

            if unit:
                ctk.CTkLabel(row, text=unit, width=40).pack(side="left")

        # Botones
        button_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        for text, cmd in [
            ("Calcular Diseño", self.calculate_design),
            ("Nuevo Diseño", self.clear_entries),
            ("Salir", self.quit),
        ]:
            ctk.CTkButton(
                button_frame,
                text=text,
                command=cmd,
                fg_color="#0087F2",
                hover_color="#0070cc",
                corner_radius=20,
                width=130,
                height=35,
            ).pack(side="left", padx=10)

    def create_input_widget(self, parent, key):
        if key == "project_location":
            combo = ctk.CTkComboBox(
                parent,
                values=get_municipality() + ["Otro"],
                command=self.handle_project_location,
                width=220,
            )
            combo.set("Seleccione una ubicación")
            combo.configure(fg_color="#ffffff", text_color="#888888")
            return combo
        elif key in {"aa", "pga"}:
            return ctk.CTkEntry(parent, width=220, state="disabled")
        elif key == "concrete_resistance":
            combo = ctk.CTkComboBox(parent, values=CONCRETE_VALUES, width=220)
            return combo
        elif key == "steel_resistance":
            return ctk.CTkLabel(
                parent, text="420", anchor="e", justify="right", width=220
            )
        elif key in {"diente", "type_soil"}:
            values = DIENTE_VALUES if key == "diente" else TYPE_SOIL_VALUES
            return ctk.CTkComboBox(parent, values=values, width=220)
        else:
            return ctk.CTkEntry(parent, width=220)

    def handle_project_location(self, selected_location):
        combo = self.entries["project_location"]
        if selected_location != "Seleccione una ubicación":
            combo.configure(text_color="#000000")

        aa_entry = self.entries["aa"]
        pga_entry = self.entries["pga"]

        if selected_location == "Otro":
            aa_entry.configure(state="normal")
            aa_entry.delete(0, "end")
            pga_entry.configure(state="normal")
            pga_entry.delete(0, "end")
        else:
            factors = self.calculate_factor(selected_location)
            aa_entry.configure(state="normal")
            aa_entry.delete(0, "end")
            aa_entry.insert(0, str(factors["aa"]))
            aa_entry.configure(state="disabled")

            pga_entry.configure(state="normal")
            pga_entry.delete(0, "end")
            pga_entry.insert(0, str(factors["pga"]))
            pga_entry.configure(state="disabled")

    def handle_design_change(self, selected):
        self.update_image(selected)

        angle_input = self.entries["angle_inclination"]
        if selected.startswith("Sin inclinación"):
            angle_input.configure(state="normal")
            angle_input.delete(0, "end")
            angle_input.insert(0, "0")
            angle_input.configure(state="disabled")
        else:
            angle_input.configure(state="normal")

    def update_image(self, design_type):
        image_map = {
            "Con inclinación": "primera_con_inclinacion.png",
            "Sin inclinación - vías": "primera_sin_inclinacion_vias.png",
            "Sin inclinación": "primera_sin_inclinacion.png",
        }
        filename = image_map.get(design_type)
        path = os.path.join("assets", "images", filename)
        if os.path.exists(path):
            img = Image.open(path).resize((360, 360), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        else:
            self.image_label.configure(text="Imagen no encontrada")

    def calculate_factor(self, location):
        seismic_info = get_seismic_info(location) or {}
        return {
            "aa": seismic_info.get("Aa", "0.0"),
            "pga": seismic_info.get("pga", "0.0"),
        }

    def calculate_design(self):
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
        result = {}
        for key, widget in self.entries.items():
            if isinstance(widget, ctk.CTkEntry):
                result[key] = widget.get().strip().replace(",", ".")
            elif isinstance(widget, ctk.CTkComboBox):
                result[key] = widget.get().strip()
            elif isinstance(widget, ctk.CTkLabel):
                result[key] = "420"
        return result

    def clear_entries(self):
        for key, widget in self.entries.items():
            if isinstance(widget, (ctk.CTkEntry, ctk.CTkComboBox)):
                widget.configure(state="normal")
                widget.delete(0, "end")


if __name__ == "__main__":
    app = DesignParameters()
    app.mainloop()
