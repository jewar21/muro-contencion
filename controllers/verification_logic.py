def check_compliance(data):
    """
    Verifica si los valores cumplen con las condiciones de seguridad.
    """
    # Cálculos ficticios de ejemplo
    volcamiento = True  # Resultado de cálculo
    deslizamiento = False  # Resultado de cálculo
    esfuerzo_max = True
    esfuerzo_min = True

    return [
        ("Factor de seguridad al volcamiento", "CUMPLE" if volcamiento else "NO CUMPLE"),
        ("Factor de seguridad al deslizamiento", "CUMPLE" if deslizamiento else "NO CUMPLE"),
        ("Esfuerzo máximo a presión", "CUMPLE" if esfuerzo_max else "NO CUMPLE"),
        ("Esfuerzo mínimo a presión", "CUMPLE" if esfuerzo_min else "NO CUMPLE"),
    ]
