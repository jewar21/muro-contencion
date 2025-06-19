
import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from customtkinter import CTkImage

from utils.pdf_generator import build_complete_pdf


class Predimensioning(ctk.CTkToplevel):
    def __init__(self, root, input_data, full_data):
        super().__init__(root)
        self.input_data = input_data
        self.full_data = full_data
        self.title("Cálculo de Muros - Predimensionamiento")
        self.geometry("1400x700")
        self.resizable(False, False)
        self.configure(fg_color="#f9f9f9")

        self.verification_results = self.calculate_verification_results()
        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, pady=10)

        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack()

        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, rowspan=2, padx=(0, 40), sticky="n")

        self.image_label = ctk.CTkLabel(left_frame, text="")
        self.image_label.pack(pady=(10, 10))
        self.update_image()

        self.predim_table = ctk.CTkFrame(
            left_frame, fg_color="#ffffff", corner_radius=12)
        self.predim_table.pack(pady=10)

        self.predim_fields = [
            ("Base del muro (B)", "Base del muro", "m"),
            ("Pie (b1)", "Pie", "m"),
            ("Talón (b3)", "Talón", "m"),
            ("Base corona (b2min)", "Base corona", "m"),
            ("Base máxima (b2max)", "Base vástago", "m"),
            ("Altura de zapata (d)", "Altura de zapata", "m"),
            ("Pantalla (h)", "h", "m"),
            ("Inclinación de vástago (β)", "Ángulo de inclinación del Vástago", "°"),
        ]

        self.predim_entries = {}
        for display, key, unit in self.predim_fields:
            row = ctk.CTkFrame(self.predim_table, fg_color="transparent")
            row.pack(pady=4, fill="x")
            display_text = display if len(
                display) <= 30 else f"{display[:30]}\n{display[30:]}"
            ctk.CTkLabel(row, text=display_text, width=180,
                         anchor="e", justify="right").pack(side="left")
            entry = ctk.CTkEntry(row, width=100)
            entry.insert(0, f"{self.input_data.get(key, 0.0):.2f}")
            entry.configure(state="disabled")
            entry.pack(side="left", padx=5)
            self.predim_entries[key] = entry
            ctk.CTkLabel(row, text=unit, width=40,
                         anchor="w").pack(side="left")

        # Verificaciones
        top_right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_right_frame.grid(row=0, column=1, sticky="nsew", pady=(10, 0))

        self.create_verification_table(
            top_right_frame, "DESLIZAMIENTO", "deslizamiento", 0)
        self.create_verification_table(
            top_right_frame, "VOLCAMIENTO", "volcamiento", 1)

        bottom_right_frame = ctk.CTkFrame(
            content_frame, fg_color="transparent")
        bottom_right_frame.grid(row=1, column=1, sticky="nsew")

        self.create_verification_table(
            bottom_right_frame, "PRESIÓN", "presion", 0)

        # Botones
        button_frame = ctk.CTkFrame(bottom_right_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, sticky="s", padx=10)

        buttons = [
            ("Ingresar Manualmente", self.enable_editing),
            ("Calcular Vista", self.calculate_view),
            ("Exportar PDF", self.export_to_pdf),
            ("Cerrar", self.destroy),
        ]

        # Crear una cuadrícula de 2x2
        for index, (text, cmd) in enumerate(buttons):
            row = index // 2
            col = index % 2
            ctk.CTkButton(
                button_frame,
                text=text,
                command=cmd,
                fg_color="#0087F2",
                hover_color="#0070cc",
                width=180,
                height=35,
                corner_radius=20,
            ).grid(row=row, column=col, padx=10, pady=10)

    def create_verification_table(self, parent, title, key, col_idx):
        frame = ctk.CTkFrame(parent, fg_color="#ffffff", corner_radius=12)
        frame.grid(row=0, column=col_idx, padx=10, pady=10, sticky="n")

        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(
            size=14, weight="bold")).pack(pady=(10, 5))

        columns = self.get_table_columns(key) or []
        table = ctk.CTkFrame(frame, fg_color="#f3f3f3")
        table.pack(padx=5, pady=5, fill="x")

        header = ctk.CTkFrame(table, fg_color="transparent")
        header.pack(fill="x", padx=5)
        for i, col in enumerate(columns):
            wrap = 90 if i == 0 else 80
            ctk.CTkLabel(header, text=col, width=wrap, wraplength=wrap,
                         anchor="center", font=ctk.CTkFont(weight="bold")).pack(side="left")

        for row_data in self.verification_results.get(key, []):
            row = ctk.CTkFrame(table, fg_color="transparent")
            row.pack(fill="x", padx=5, pady=1)
            for i, val in enumerate(row_data):
                wrap = 90 if i == 0 else 80
                ctk.CTkLabel(row, text=str(val), width=wrap,
                             wraplength=wrap, anchor="center").pack(side="left")

    def get_table_columns(self, key):
        if key == "deslizamiento":
            return ("ESTADO LÍMITE", "CASO", "FX (KN)", "RR (KN)", "CUMPLE")
        elif key == "volcamiento":
            return ("ESTADO LÍMITE", "CASO", "e (m)", "eₘₐₓ (m)", "CUMPLE")
        elif key == "presion":
            return ("ESTADO LÍMITE", "CASO", "σᵥ (KN/m²)", "σₘₐₓ (KN/m²)", "CUMPLE")

    def calculate_verification_results(self):
        try:
            return {
                "deslizamiento": [
                    ("RESISTENCIA 1", "MÁXIMO", self.input_data["fhr1cmax"],
                     self.input_data["RRR1CMAX"], self.input_data["controlRRR1CMAX"]),
                    ("", "MÍNIMO", self.input_data["fhr1cmin"],
                     self.input_data["RRR1CMIN"], self.input_data["controlRRR1CMIN"]),
                    ("EVENTO EXTREMO I", "MÁXIMO",
                     self.input_data["fhex1cmax"], self.input_data["RREX1CMAX"], self.input_data["controlRREX1CMAX"]),
                    ("", "MÍNIMO", self.input_data["fhex1cmin"],
                     self.input_data["RREX1CMIN"], self.input_data["controlRREX1CMIN"]),
                    ("EVENTO EXTREMO II", "MÁXIMO",
                     self.input_data["fhex2cmax"], self.input_data["RREX2CMAX"], self.input_data["controlRREX2CMAX"]),
                    ("", "MÍNIMO", self.input_data["fhex2cmin"],
                     self.input_data["RREXC2MIN"], self.input_data["controlRREX2CMIN"]),
                    ("SERVICIO 1", "", self.input_data["fhs"],
                     self.input_data["RR"], self.input_data["controlRRS"]),
                ],
                "volcamiento": [
                    ("RESISTENCIA 1", "MÁXIMO",
                     self.input_data["eMAX"], self.input_data["eR1CMAX"], self.input_data["controleR1MAX"]),
                    ("", "MÍNIMO", self.input_data["eMAX"],
                     self.input_data["eR1CMIN"], self.input_data["controleR1MIN"]),
                    ("EVENTO EXTREMO I", "MÁXIMO",
                     self.input_data["eMAX"], self.input_data["eEX1CMAX"], self.input_data["controleX1MAX"]),
                    ("", "MÍNIMO", self.input_data["eMAX"],
                     self.input_data["eEX1CMIN"], self.input_data["controleX1MIN"]),
                    ("EVENTO EXTREMO II", "MÁXIMO",
                     self.input_data["eMAX"], self.input_data["eEX2CMAX"], self.input_data["controleX2MAX"]),
                    ("", "MÍNIMO", self.input_data["eMAX"],
                     self.input_data["eEX2CMIN"], self.input_data["controleX2MIN"]),
                    ("SERVICIO 1", "", self.input_data["eMAX"],
                     self.input_data["eS"], self.input_data["controleS"]),
                ],
                "presion": [
                    ("RESISTENCIA 1", "MÁXIMO", self.input_data["capacidad_portante_r1"],
                     self.input_data["esfuerzoR1CMAX"], self.input_data["controlesfuerzoR1CMAX"]),
                    ("", "MÍNIMO", self.input_data["capacidad_portante_r1"],
                     self.input_data["esfuerzoR1CMIN"], self.input_data["controlesfuerzoR1CMIN"]),
                    ("EVENTO EXTREMO I", "MÁXIMO", self.input_data["capacidad_portante_ex1"],
                     self.input_data["esfuerzoEX1CMAX"], self.input_data["controlesfuerzoEX1CMAX"]),
                    ("", "MÍNIMO", self.input_data["capacidad_portante_ex1"],
                     self.input_data["esfuerzoEX1CMIN"], self.input_data["controlesfuerzoEX1CMIN"]),
                    ("EVENTO EXTREMO II", "MÁXIMO", self.input_data["capacidad_portante_ex2"],
                     self.input_data["esfuerzoEX2CMAX"], self.input_data["controlesfuerzoEX2CMAX"]),
                    ("", "MÍNIMO", self.input_data["capacidad_portante_ex2"],
                     self.input_data["esfuerzoEX2CMIN"], self.input_data["controlesfuerzoEX2CMIN"]),
                    ("SERVICIO 1", "", self.input_data["capacidad_portante_s"],
                     self.input_data["esfuerzoS"], self.input_data["controlesfuerzoS"]),
                ],
            }
        except KeyError as e:
            messagebox.showerror(
                "Error", f"Falta el dato {e} en los resultados.")
            return {}

    def update_image(self):
        design = self.full_data.get("tipo_diseño", "Sin inclinación - vías")
        print("ESTEEEEEEEE: ", design)
        image_map = {
            "Con inclinación": "segunda_con_inclinacion.png",
            "Sin inclinación - vías": "segunda_sin_inclinacion_vias.png",
            "Sin inclinación": "segunda_sin_inclinacion.png",
        }
        filename = image_map.get(design)
        if filename:
            path = os.path.join("assets", "images", filename)
        if os.path.exists(path):
            pil_image = Image.open(path)
            ctk_image = CTkImage(light_image=pil_image, size=(360, 360))
            self.image_label.configure(image=ctk_image, text="")
            self.image_label._image = ctk_image  # Mantener la referencia
        else:
            self.image_label.configure(text="Imagen no encontrada")

    def export_to_pdf(self):
        # output_path = "predimensionamiento_resultado.pdf"
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar como"
        )

        print("INFORMACION PDF", self.input_data)

        predim_data = {
            "notas": [
                "Se recomienda instalar drenajes de 3” con separación máxima de 3 m en ambas direcciones, junto con un sistema de filtración para evitar el incremento de presiones hidrostáticas.",
                "Si existen estudios de microzonificación o de sitio, se debe verificar la aceleración pico-efectiva en la roca (PGA) para garantizar el cumplimiento de los parámetros sísmicos.",
                "Este diseño no considera la influencia del nivel freático; en caso de ser relevante, se recomienda su evaluación para determinar su impacto en la estabilidad del muro.",
                "El análisis de estabilidad realizado es local; se deben desarrollar estudios específicos para identificar superficies de falla que puedan comprometer la estabilidad global del muro.",
                "Se recomienda el uso de suelos grava-arenosos SW, SP y GP, con compactación adecuada y un contenido de finos inferior al 5% para garantizar su estabilidad.",
                "Es fundamental realizar controles de densidad en campo para verificar el cumplimiento de los niveles de compactación requeridos."
            ],
            "parametros": [
                ("Altura del muro (m)", f'{self.input_data.get(
                    "h", "N/A"): .2f} m'),
                ("Aceleración pico-efectiva en la roca (PGA)", "0,40"),
                ("Capacidad portante del suelo de cimentación (qN)",
                 f'{self.input_data.get("capacidad_portante_r1", "N/A")} kN/m²'),
                ("Inclinación de terreno (i)", "20°"),
                ("Ángulo fricción interna (ϕ)", "38°"),
                ("Peso específico del relleno (γrelleno)", "1,8 Ton/m³"),
                ("Resistencia del concreto (f′c)", "24,5 MPa"),
                ("Resistencia del acero (fy)",
                 f'{self.input_data.get("Resistencia del acero (fy)", "N/A")} MPa'),
                ("Ángulo de fricción suelo-muro (δ)", "12°")
            ],

        }

        logos = {
            "logo_civil": "assets/images/pdf/logoCivil.png",
            "logo_ufpso": "assets/images/pdf/Logoufpso.png"
        }

        image_path = "assets/images/pdf/Diseno_para_barrera.png"
        
        if output_path:
            try:
                build_complete_pdf(output_path, predim_data,
                           self.verification_results, image_path, logos)
                messagebox.showinfo("Exportación Exitosa",
                            f"PDF guardado como {output_path}")
            except Exception as e:
                messagebox.showinfo("No se pudo exportar PDF")

    def enable_editing(self):
        for entry in self.predim_entries.values():
            entry.configure(state="normal")

    def calculate_view(self):
        self.update_input_data_from_entries()
        self.verification_results = self.calculate_verification_results()

        print("Recalculando vista con nuevos datos:", self.input_data)

    def update_input_data_from_entries(self):
        for key, entry in self.predim_entries.items():
            try:
                value = float(entry.get().strip().replace(",", "."))
                self.input_data[key] = value
            except ValueError:
                messagebox.showwarning(
                    "Advertencia", f"El valor de '{key}' no es válido.")
