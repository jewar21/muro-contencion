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

        # Aquí va la lógica específica para el diseño
        # Ejemplo ficticio: Calcular estabilidad
        stability_factor = (angle_friction + unit_weight) / (steel_resistance * wall_height)
        # return {"stability_factor": stability_factor}
        return angle_friction, angle_soil_wall, unit_weight, steel_resistance, wall_height

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
