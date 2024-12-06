# Valores permitidos para la resistencia del concreto
CONCRETE_VALUES = ["21", "24.5", "28"]

# Campos del formulario (label, símbolo, key, unidad)
FORM_FIELDS = [
    ("Angulo de fricción interna de relleno", "ø", "angle_friction", "°"),
    ("Ángulo de fricción suelo-muro", "δ", "angle_soil_wall", "°"),
    ("Peso unitario del relleno", "γrelleno", "unit_weight", "T/m³"),
    ("Esfuerzo admisible del suelo", "σadm", "soil_bearing_capacity", "KN/m²"),
    ("Resistencia del concreto", "fc", "concrete_resistance", "MPa"),
    ("Resistencia del acero", "fy", "steel_resistance", "MPa"),
    ("Altura de muro", "H", "wall_height", "m"),
    ("Ángulo de inclinación del relleno", "i", "angle_soil_wall", "°"),
    ("Ubicación del proyecto", "", "project_location", ""),
    ("Aceleración pico efectiva", "Aa", "aa", ""),
]