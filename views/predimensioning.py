
import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk


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

        columns = self.get_table_columns(key)
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
        path = os.path.join("assets", "images", filename)
        if os.path.exists(path):
            img = Image.open(path).resize((360, 360), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        else:
            self.image_label.configure(text="Imagen no encontrada")

    def export_to_pdf(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        pdf_path = "predimensionamiento_resultado.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, "Resultados de Predimensionamiento")

        y = height - 100
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, y, "Datos de Predimensionamiento:")
        y -= 20

        c.setFont("Helvetica", 10)
        for key, entry in self.predim_entries.items():
            value = entry.get()
            c.drawString(80, y, f"{key}: {value}")
            y -= 14
            if y < 72:
                c.showPage()
                y = height - 72

        for section, rows in self.verification_results.items():
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 72

            c.setFont("Helvetica-Bold", 12)
            c.drawString(72, y, f"Verificación - {section.upper()}")
            y -= 20

            c.setFont("Helvetica", 10)
            for row in rows:
                c.drawString(80, y, " | ".join([str(col) for col in row]))
                y -= 14
                if y < 72:
                    c.showPage()
                    y = height - 72

        c.save()
        messagebox.showinfo("Exportación Exitosa",
                            f"PDF guardado como {pdf_path}")

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
