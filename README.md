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
