# 📐 Proyecto Muro de Contención

Este documento describe la estructura, funcionalidades y lógica técnica del sistema desarrollado para el diseño y verificación de muros de contención, utilizando Python y CustomTkinter como base para la interfaz gráfica.

---

## 📁 Estructura del Proyecto

```plaintext
- muro-contencion-main/
    - muro-contencion-main/
        - .gitignore
        - README.md
        - main.py
        - main.spec
        - .vscode/
            - settings.json
        - assets/
            - images/
                - primera_con_inclinacion.png
                - primera_sin_inclinacion.png
                - primera_sin_inclinacion_vias.png
                - segunda_con_inclinacion.png
                - segunda_sin_inclinacion.png
                - segunda_sin_inclinacion_vias.png
                ...
        - controllers/
            - data_manager.py
            - design_logic.py
            - verification_logic.py
            - __pycache__/
                - design_logic.cpython-312.pyc
                - verification_logic.cpython-312.pyc
        - models/
            - project_data.py
            - seismic_data.py
            - __pycache__/
                - project_data.cpython-312.pyc
                - seismic_data.cpython-312.pyc
        - utils/
            - helpers.py
        - views/
            - components.py
            - design_parameters.py
            - predimensioning.py
            - __pycache__/
                - design_parameters.cpython-312.pyc
                - predimensioning.cpython-312.pyc
```

---

## 🧩 Descripción de Carpetas

- `assets/`: contiene imágenes visuales utilizadas en la interfaz (inclinación, predimensionamiento).
- `controllers/`: contiene la lógica de diseño estructural y cálculo (deslizamiento, volcamiento, presión).
- `models/`: datos y estructuras necesarias para el diseño (factores de suelo, resistencias).
- `views/`: interfaces gráficas en `customtkinter`, organizadas en pantallas como predimensionamiento y diseño.
- `utils/`: funciones auxiliares de uso común.
- `main.py`: archivo principal para ejecutar la aplicación.

---

## ⚙️ Funcionalidades Principales

- Predimensionamiento de muros basado en parámetros del terreno.
- Selección del tipo de diseño: con inclinación, sin inclinación, sin inclinación - vías.
- Cálculos estructurales:
  - Verificación al deslizamiento.
  - Verificación al volcamiento.
  - Verificación por presión.
- Visualización de resultados en tablas.
- Botones de edición, cálculo, cierre y exportación a PDF (en desarrollo).
- Actualización dinámica de imágenes según tipo de diseño.

---

## 🔢 Tecnologías Usadas

- Python 3.12+
- CustomTkinter
- PIL (Pillow)
- PyInstaller (para despliegue)
- tkinter (librería base)

---

## 🚀 Ejecución

```bash
pip install -r requirements.txt
python main.py
```

---

## 📌 Siguientes pasos

- Finalizar integración con `reportlab` para exportación PDF.
- Mejorar validación de entrada para campos numéricos.
- Documentar cálculos estructurales paso a paso.

---

## ✍️ Autoría

Proyecto académico desarrollado como solución computacional para estudiantes e ingenieros civiles, integrando principios de diseño estructural y visualización UX.