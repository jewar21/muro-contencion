from tkinter import ttk, messagebox
from math import atan, degrees

from models.project_data import (
    FACTORS_BY_AA,
    FACTORS_BY_AA_INCLINED
)
from views.predimensioning import Predimensioning


def calculate_design_logic(data):
    """
    Realiza los cálculos de diseño basados en los datos proporcionados.

    :param data: Diccionario con los valores de entrada.
    :return: Resultado del diseño.
    """
    try:
        # Convertir los valores a numéricos donde sea necesario
        angle_friction = float(data["angle_friction"])
        angle_soil_wall = float(data["angle_soil_wall"])
        unit_weight = float(data["unit_weight"])
        steel_resistance = float(data["steel_resistance"])
        wall_height = float(data["wall_height"])

        return (
            angle_friction,
            angle_soil_wall,
            unit_weight,
            steel_resistance,
            wall_height,
        )

    except ValueError as e:
        return {"error": f"Entrada inválida: {e}"}


def calculate_predimensioning(data):
    """
    Realiza los cálculos de predimensionamiento basados en las fórmulas del archivo.
    """
    H = float(data.get("wall_height", 0))  # Altura del muro

    # Calcular valores
    B = 0.48 * H  # Base del muro
    b1 = 0.28 * B  # Pie
    b3 = 0.58 * B  # Talón
    b2min = 0.30  # Ejemplo fijo
    b2max = B - b1 - b3  # Base máxima
    d = 0.11 * H  # Altura de la zapata
    h = H - d  # Altura de la pantalla
    beta = round((b2max - b2min) / h, 2)  # Inclinación de vástago

    return [
        ("Base del muro (B)", round(B, 2), "m"),
        ("Pie (b1)", round(b1, 2), "m"),
        ("Talón (b3)", round(b3, 2), "m"),
        ("Base corona (b2min)", b2min, "m"),
        ("Base máxima (b2max)", round(b2max, 2), "m"),
        ("Altura de zapata (d)", round(d, 2), "m"),
        ("Pantalla (h)", round(h, 2), "m"),
        ("Inclinación de vástago (beta)", beta, "°"),
    ]


def get_factor(value, ranges, default=0):
    """
    Obtiene el factor correspondiente a un valor según los rangos especificados.
    """
    for min_val, max_val, factor in ranges:
        if min_val <= value <= max_val:
            return factor
    return default


def validate_inputs(data):
    # Valida los valores ingresados por el usuario y devuelve un diccionario con valores procesados.
    try:
        wall_height = float(data.get("wall_height", 0))
        angle_inclination = float(data.get("angle_inclination", 0))
        fy = float(data.get("steel_resistance", 420))
        aa = float(data.get("aa", 0))

        # Validaciones de los valores de entrada
        if angle_inclination > 45:
            raise ValueError(
                "El ángulo de inclinación del relleno (i) no puede ser mayor a 45 grados.")

        if wall_height < 1.5 or wall_height > 6.0:
            raise ValueError(
                "Altura no admitida: Ingrese una altura entre 1.5m y 6m.")

        return {
            "wall_height": wall_height,
            "angle_inclination": angle_inclination,
            "fy": fy,
            "aa": aa
        }
    except ValueError as e:
        raise ValueError(f"Error en la validación de datos: {e}")


def calculate_design_logic(data):
    """
    Realiza los cálculos de diseño a partir de los datos validados.
    """
    try:
        validated_data = validate_inputs(data)
        wall_height = validated_data["wall_height"]
        angle_inclination = validated_data["angle_inclination"]
        fy = validated_data["fy"]
        aa = validated_data["aa"]

        # Seleccionar el conjunto de factores según el ángulo
        factors = FACTORS_BY_AA if angle_inclination == 0 else FACTORS_BY_AA_INCLINED

        # Validar que Aa esté en los factores
        if aa not in factors:
            raise ValueError(
                f"El valor de Aa ({aa}) no es válido o no tiene factores asignados.")

        # Obtener factores para base, pie y talón
        base_factor = get_factor(
            wall_height, factors[aa]["base_factor"])
        base_muro = round((wall_height * base_factor), 2)

        pie_factor = get_factor(
            base_muro, factors[aa]["pie_factor"])
        talon_factor = get_factor(
            base_muro, factors[aa]["talon_factor"])

        pie = round((base_muro * pie_factor), 2)
        talon = round((base_muro * talon_factor), 2)

        # Cálculo de la base corona (b2min)
        base_corona = get_factor(
            wall_height,
            [
                (1.5, 3.5, 0.25),
                (3.5, 5.5, 0.30),
            ],
            default=0.35,
        )

        # Cálculo de la altura de zapata (d)
        altura_zapata = (
            get_factor(
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
        base_vastago = round((base_muro - pie - talon), 2)
        # Cálculo de la altura de la pantalla (h)
        altura_pantalla = round((wall_height - altura_zapata), 2)
        # Cálculo del ángulo de inclinación del vástago (β)
        inclinacion = round((degrees(
            atan((base_vastago - base_corona) / altura_pantalla))), 2)
        # print("inclinacion", base_abajo, base_corona, altura_pantalla)

        # Resultados
        results = {
            "Base del muro": base_muro,
            "Pie": pie,
            "Talón": talon,
            "Base corona": base_corona,
            "Base vástago": base_vastago,
            "Altura de zapata": altura_zapata,
            "h": altura_pantalla,
            "Ángulo de inclinación del Vástago": inclinacion,  # beta_rad
            "Resistencia del acero (fy)": fy,
        }

        # Mostrar resultados
        return results

    except ValueError as e:
        raise ValueError(f"Error en el cálculo: {e}")
