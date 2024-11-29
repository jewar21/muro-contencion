import tkinter as tk
from tkinter.ttk import Combobox

raiz = tk.Tk()

raiz.title("Aplicativo para diseño de muros de contención en voladizo")
raiz.config(bg="grey")

miFrame = tk.Frame()
miFrame.pack()
miFrame.config(width="1000", height="600", bg="white")

# Creamos el label del titulo
tk.Label(
    miFrame,
    text="PÁRAMETROS DE DISEÑO",
    font=("Times New Roman", 14),
    bg="white"
    ).place(x=500, y=10)

# Campo angulo de friccion
friction_angle_label = tk.Label(
    miFrame,
    text="Ángulo de fricción",
    font=("Times New Roman", 12),
    bg="white")
friction_angle_label.place(x=500, y=50)
friction_angle_entry = tk.Entry(miFrame, width=13)
friction_angle_entry.place(x=720, y=50)
tk.Label(miFrame, text = "°", font=("Times New Roman", 12), bg="white").place(x = 830, y = 50)

# Campo de coeficiente de friccion
friction_coeficient_label = tk.Label(
    miFrame,
    text="Coeficiente de fricción suelo-muro",
    font=("Times New Roman", 12),
    bg="white"
)
friction_coeficient_label.place(x=500, y=80)
friction_coeficient_entry = tk.Entry(miFrame, width=13)
friction_coeficient_entry.place(x=720, y=80)

# Campo peso unitario del relleno
unitary_weigth_label = tk.Label(
    miFrame,
    text="Peso unitario del relleno",
    font=("Times New Roman", 12),
    bg="white")
unitary_weigth_label.place(x=500, y=110)
unitary_weight_entry = tk.Entry(miFrame, width=13)
unitary_weight_entry.place(x=720, y=110)
tk.Label(miFrame, text = "Ton/m^3", font=("Times New Roman", 10), bg="white").place(x = 830, y = 110)

# Campo de resistencia del concreto
concrete_resistance = tk.Label(
    miFrame,
    text="Resistencia del concreto",
    font=("Times New Roman", 12),
    bg="white")
concrete_resistance.place(x=500, y=140)
concrete_resistance_entry = tk.Entry(miFrame, width=13)
concrete_resistance_entry.place(x=720, y=140)
tk.Label(miFrame, text = "MPa", font=("Times New Roman", 10), bg="white").place(x = 830, y = 140)

# Campo de resistencia del acero
steel_resistance_label = tk.Label(
    miFrame,
    text="Resistencia del acero",
    font=("Times New Roman", 12),
    bg="white")
steel_resistance_label.place(x=500, y=170)
steel_resistance_entry = tk.Entry(miFrame, width=13)
steel_resistance_entry.place(x=720, y=170)
tk.Label(miFrame, text = "MPa", font=("Times New Roman", 10), bg="white").place(x = 830, y = 170)

# Campo de altura H
floor_wall_friction_label = tk.Label(
    miFrame,
    text="Altura de muro (H)",
    font=("Times New Roman", 12),
    bg="white")
floor_wall_friction_label.place(x=500, y=200)
altura_entry = tk.Entry(miFrame, width=13)
altura_entry.place(x=720, y=200)
tk.Label(miFrame, text = "m", font=("Times New Roman", 12), bg="white").place(x = 830, y = 200)

# Campo Ubicación
ubi_label = tk.Label(
    miFrame,
    text="Ubicación del proyecto",
    font=("Times New Roman", 12),
    bg="white")
ubi_label.place(x=500, y=230)



# Campo de Aa
aa_label = tk.Label(
    miFrame,
    text="Aa",
    font=("Times New Roman", 12),
    bg="white")
aa_label.place(x=500, y=260)
aa_entry = tk.Entry(miFrame, width=13)
aa_entry.place(x=720, y=260)

#Campo de f.S Volcamiento
volcamiento_label = tk.Label(
    miFrame,
    text="F.S Volcamiento",
    font=("Times New Roman", 12),
    bg="white")
volcamiento_label.place(x=500, y=290)
tk.Label(miFrame, text = "< 3,00", font=("Times New Roman", 12), bg="white").place(x = 700, y = 290)


# Campo de F.S Deslizamiento
glide_label = tk.Label(
    miFrame,
    text="F.S Deslizamiento",
    font=("Times New Roman", 12),
    bg="white")
glide_label.place(x=500, y=320)
tk.Label(miFrame, text = "> 2,00", font=("Times New Roman", 12), bg="white").place(x = 700, y = 320)


# Campo de recubrimiento minimo
covering_label = tk.Label(
    miFrame,
    text="Recubrimiento mínimo",
    font=("Times New Roman", 12),
    bg="white")
covering_label.place(x=500, y=350)
tk.Label(miFrame, text = "75 mm", font=("Times New Roman", 12), bg="white").place(x = 700, y = 350)

botonSalir = tk.Button(miFrame, text="Salir", width=14)
botonSalir.place(x=400, y=550)

# Crear un Combobox (lista desplegable)
municipios = ["Ábrego", "Arboledas", "Bochalema", "Bucarasica", "Cáchira", "Cácota", "Chinácota", "Chitagá", "Convención", "Cúcuta", "Cucutilla", "Durania", "El Carmen", "El Tarra", "El Zulia", "Gramalote", "Hacarí", "Herrán", "Labateca", "La Esperanza", "La Playa", "Los Patios", "Lourdes", "Mutiscua", "Ocaña", "Pamplona", "Pamplonita", "Puerto Santander", "Ragonvalia", "Salazar", "San Calixto", "San Cayetano", "Santiago", "Sardinata", "Silos", "Teorama", "Tibú", "Toledo", "Villa Caro", "Villa del Rosario","Otro"]
combo = Combobox(miFrame, values=municipios)
combo.set("Selecciona una opción")  
combo.place(x=720, y=230)

# imagen = tk.PhotoImage(file="assets/images/design.png")

# Crear un label y agregar la imagen
# label = tk.Label(miFrame, image=imagen, background="white")
# label.place(x=60, y=60)

# Función para abrir la segunda ventana
def abrir_segunda_ventana():
    # Crear la segunda ventana
    segunda_ventana = tk.Toplevel()
    segunda_ventana.title("Diseño creado")
    segunda_ventana.geometry("1000x600")
    label = tk.Label(segunda_ventana, text="Resultados de diseño")
    label.pack(pady=20)

# Función para eliminar el contenido de los cuadros de texto
def limpiar_campos():
    friction_angle_entry.delete(0, tk.END) 
    friction_coeficient_entry.delete(0, tk.END)  
    unitary_weight_entry.delete(0, tk.END) 
    concrete_resistance_entry.delete(0, tk.END) 
    steel_resistance_entry.delete(0, tk.END) 
    altura_entry.delete(0, tk.END)
    aa_entry.delete(0, tk.END)
   

#Función para salir
def cerrar_ventana():
    raiz.destroy()
    
botonSalir = tk.Button(miFrame, text="Salir", width=14, command= cerrar_ventana)
botonSalir.place(x=400, y=550)
    
boton_nuevo_diseño = tk.Button(raiz, text="Nuevo diseño", width=14, command=limpiar_campos)
boton_nuevo_diseño.place(x=250, y=550)

# Debemos crear una funcion que reciba los datos del formulario para poder procesarlos


def design_contention_wall():
    # obtenemos los datos de cada entrada
    friction_angle = friction_angle_entry.get()
    friction_coeficient = friction_coeficient_entry.get()
    # Aqui seguis colocando las entradas de los diferentes campos

    # Cuando ya se tienen las entradas hacer la operacion que se requieran

    
    return friction_angle + friction_coeficient


submmit_button = tk.Button(
    miFrame,
    text='Calcular diseño', 
    command = abrir_segunda_ventana,
    width=14
)
submmit_button.place(x=100, y=550)


# Arrancamos el frame
raiz.mainloop()
