# Muro de Contención

## Arquitectura del Proyecto

El proyecto está estructurado de la siguiente manera:

project/
│
├── main.py                # Archivo principal para iniciar la aplicación
├── controllers/           # Lógica de negocio y validaciones
│   ├── design_logic.py    # Funciones para los cálculos del diseño
│   └── data_manager.py    # Funciones para manejar datos (lectura/escritura si es necesario)
├── models/                # Modelos de datos, si se requiere manejar estructuras específicas
│   └── project_data.py    # Modelos de datos como parámetros del proyecto
├── views/                 # Interfaces gráficas de la aplicación
│   ├── design_parameters.py # Primera interfaz (parámetros de diseño)
│   └── components.py      # Componentes comunes como botones personalizados, etc.
├── assets/                # Recursos como imágenes, íconos y estilos
│   └── images/            # Imágenes para la interfaz
│       └── design.png     # Imagen para la primera pantalla
└── utils/                 # Utilidades generales
    └── helpers.py         # Funciones comunes, validaciones, y herramientas auxiliares
# muro-contencion


## Descripción de los Directorios

### **main.py**
Archivo principal que sirve como punto de entrada para iniciar la aplicación.

### **controllers/**
Contiene la lógica de negocio y validaciones principales:
- `design_logic.py`: Funciones específicas para realizar cálculos del diseño estructural.
- `data_manager.py`: Maneja la lectura, escritura y validación de datos relacionados al proyecto.

### **models/**
Define estructuras y modelos de datos que organizan los parámetros y configuraciones:
- `project_data.py`: Clase y estructuras que representan los datos relevantes del proyecto.

### **views/**
Maneja la interfaz gráfica de usuario (GUI) y sus componentes:
- `design_parameters.py`: Interfaz principal donde se ingresan los parámetros de diseño.
- `components.py`: Componentes reutilizables como botones, cuadros de mensajes, etc.

### **assets/**
Contiene recursos estáticos del proyecto:
- **images/**: Carpeta con imágenes y gráficos para la interfaz:
  - `design.png`: Imagen representativa para la primera pantalla.

### **utils/**
Incluye utilidades generales y funciones de soporte:
- `helpers.py`: Funciones comunes, validaciones y herramientas auxiliares para el proyecto.

---