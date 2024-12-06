import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from math import atan, degrees


class Predimensioning(tk.Toplevel):
    def __init__(self, root, input_data):
        super().__init__(root)
        self.input_data = input_data
        self.title("Cálculo de Muros - Predimensionamiento")
        self.geometry("900x600")
        self.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Contenedor principal
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.grid(sticky="nsew")

        # Imagen a la izquierda
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Mostrar imagen
        img_path = os.path.join("assets", "images", "design.png")
        try:
            img = Image.open(img_path)
            img = img.resize((400, 300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            label_img = tk.Label(left_frame, image=img_tk)
            label_img.image = img_tk
            label_img.pack()
        except FileNotFoundError:
            tk.Label(left_frame, text="Imagen no encontrada", font=("Arial", 12, "bold")).pack()

        # Tablas a la derecha
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Tabla 1: Predimensionamiento Calculado
        predimensioning_title = tk.Label(right_frame, text="Predimensionamiento Calculado", font=("Arial", 12, "bold"))
        predimensioning_title.pack(pady=5)
        self.predimensioning_results = ttk.Treeview(
            right_frame, columns=("name", "value", "unit"), show="headings", height=8
        )
        self.predimensioning_results.heading("name", text="Parámetro")
        self.predimensioning_results.heading("value", text="Valor")
        self.predimensioning_results.heading("unit", text="Unidad")
        self.predimensioning_results.column("name", anchor="w", width=200)
        self.predimensioning_results.column("value", anchor="center", width=100)
        self.predimensioning_results.column("unit", anchor="center", width=80)
        self.predimensioning_results.pack(pady=10)

        # Tabla 2: Verificaciones
        verification_title = tk.Label(right_frame, text="Verificaciones", font=("Arial", 12, "bold"))
        verification_title.pack(pady=5)
        self.verification_results = ttk.Treeview(
            right_frame, columns=("name", "result"), show="headings", height=5
        )
        self.verification_results.heading("name", text="Parámetro")
        self.verification_results.heading("result", text="Resultado")
        self.verification_results.column("name", anchor="w", width=200)
        self.verification_results.column("result", anchor="center", width=100)
        self.verification_results.pack(pady=10)

        # Botón para cerrar
        close_button = tk.Button(right_frame, text="Cerrar", command=self.destroy)
        close_button.pack(pady=10)

        # Llenar los datos
        self.calculate_predimensioning_results()
        self.perform_verification()

    def calculate_predimensioning_results(self):
        """
        Llena la tabla de predimensionamiento con los datos proporcionados.
        """
        try:
            mapping = [
                ("Base del muro (B)", "Base del muro", "m"),
                ("Pie (b1)", "Pie", "m"),
                ("Talón (b3)", "Talón", "m"),
                ("Base corona (b2min)", "Base corona", "m"),
                ("Base máxima (b2max)", "Base abajo", "m"),
                ("Altura de zapata (d)", "Altura de zapata", "m"),
                ("Pantalla (h)", "h", "m"),
                ("Inclinación de vástago (β)", "Ángulo de inclinación del Vástago", "°"),
            ]

            for display_name, key, unit in mapping:
                value = self.input_data.get(key, 0.0)
                self.predimensioning_results.insert(
                    "", "end", values=(display_name, f"{value:.2f}", unit)
                )
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al llenar los resultados:\n{e}")

    def perform_verification(self):
        """
        Llena la tabla de verificaciones con los resultados de las comprobaciones.
        """
        try:
            # Simulación de datos de verificación
            verification_results = [
                ("Factor de seguridad al volcamiento", "CUMPLE"),
                ("Factor de seguridad al deslizamiento", "CUMPLE"),
                ("Esfuerzo máximo a presión", "NO CUMPLE"),
                ("Esfuerzo mínimo a presión", "CUMPLE"),
            ]

            for name, result in verification_results:
                self.verification_results.insert("", "end", values=(name, result))

                # Estilo según resultado
                color = "green" if result == "CUMPLE" else "red"
                self.verification_results.tag_configure("green", foreground="green")
                self.verification_results.tag_configure("red", foreground="red")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en las verificaciones:\n{e}")
