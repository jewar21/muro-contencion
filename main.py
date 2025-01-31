import tkinter as tk
from tkinter import messagebox
from views.design_parameters import DesignParameters

def main():
    """
    Punto de entrada principal para la aplicación.
    Inicializa la ventana principal de la interfaz gráfica.
    """
    try:
        # Inicializa la aplicación
        app = DesignParameters()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación:\n{e}")

if __name__ == "__main__":
    main()
