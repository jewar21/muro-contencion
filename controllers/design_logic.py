from tkinter import ttk, messagebox
from math import atan, degrees, radians, tan, sqrt, sin, cos

import numpy as np

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
        angle_friction = radians(float(data.get("angle_friction", 0)))
        angle_soil_wall = radians(float(data.get("angle_soil_wall", 0)))
        unit_weight = float(data.get("unit_weight", 0))
        soil_bearing_capacity = float(data.get("soil_bearing_capacity", 0))
        concrete_resistance = float(data.get("concrete_resistance", 0))
        fy = float(data.get("steel_resistance", 420))
        wall_height = float(data.get("wall_height", 0))
        angle_inclination = float(data.get("angle_inclination", 0))
        aa = float(data.get("aa", 0))
        pga = float(data.get("pga", 0))
        diente = float(data.get("diente", 0))
        type_soil = data.get("type_soil")

        # Validaciones de los valores de entrada
        if angle_inclination > 45:
            raise ValueError(
                "El ángulo de inclinación del relleno (i) no puede ser mayor a 45 grados.")

        if wall_height < 1.5 or wall_height > 6.0:
            raise ValueError(
                "Altura no admitida: Ingrese una altura entre 1.5m y 6m.")

        return {
            "angle_friction": angle_friction,
            "angle_soil_wall": angle_soil_wall,
            "unit_weight": unit_weight,
            "soil_bearing_capacity": soil_bearing_capacity,
            "concrete_resistance": concrete_resistance,
            "pga": pga,
            "fy": fy,
            "wall_height": wall_height,
            "angle_inclination": angle_inclination,
            "aa": aa,
            "diente": diente,
            "type_soil": type_soil,
        }
    except ValueError as e:
        raise ValueError(f"Error en la validación de datos: {e}")


def calculate_design_logic(select_design, data):
    print(f"Calculando diseño para: {select_design}")
    """
    Realiza los cálculos de diseño a partir de los datos validados.
    """

    try:
        validated_data = validate_inputs(data)
        angle_friction = validated_data["angle_friction"]
        angle_soil_wall = validated_data["angle_soil_wall"]
        unit_weight = validated_data["unit_weight"]
        soil_bearing_capacity = validated_data["soil_bearing_capacity"]
        concrete_resistance = validated_data["concrete_resistance"]
        pga = validated_data["pga"]
        fy = validated_data["fy"]
        wall_height = validated_data["wall_height"]
        angle_inclination = validated_data["angle_inclination"]
        aa = validated_data["aa"]
        diente = validated_data["diente"]
        type_soil = validated_data["type_soil"]

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
        altura_zapata = round((
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
        ), 2)

        # Cálculo de la base inferior (b2max)
        base_vastago = round((base_muro - pie - talon), 2)
        # Cálculo de la altura de la pantalla (h)
        altura_pantalla = round((wall_height - altura_zapata), 2)
        # Cálculo del ángulo de inclinación del vástago (β)
        beta_rad = round((degrees(
            atan((base_vastago - base_corona) / altura_pantalla))), 2)
        print("Estos son los datos:_ ", base_vastago,
              base_corona, altura_pantalla)

        if select_design == "Con inclinación":
            soil_loads(soil_bearing_capacity)
            area_barrera, centroide_x_barrera, f = select_barrier(base_corona)
            vdc, mdc = weight_wall(base_corona, altura_pantalla, base_vastago, pie, base_muro,
                                   altura_zapata, angle_inclination, area_barrera, centroide_x_barrera)
            vev, mev = weight_soil(base_vastago, base_corona, altura_pantalla,
                                   unit_weight, pie, talon, angle_inclination)
            ka, kp, total_height, Horizontal_component, meho = Active_and_passive_thrust(angle_friction, beta_rad, angle_soil_wall,
                                                                                         angle_inclination, base_vastago, base_corona,
                                                                                         talon, wall_height, unit_weight, altura_zapata, diente)
            fpga = f_pga(type_soil, pga)
            seismic_thrust(pga, angle_soil_wall, angle_friction, angle_inclination,
                           beta_rad, unit_weight, total_height, vdc, vev, Horizontal_component, fpga)
        elif select_design == "Sin inclinación - vías":
            print("Sin inclinación - vías")
        elif select_design == "Sin inclinación":
            print("Sin inclinación")

        # Resultados
        results = {
            "Base del muro": base_muro,
            "Pie": pie,
            "Talón": talon,
            "Base corona": base_corona,
            "Base vástago": base_vastago,
            "Altura de zapata": altura_zapata,
            "h": altura_pantalla,
            "Ángulo de inclinación del Vástago": beta_rad,
            "Resistencia del acero (fy)": fy
        }

        # Mostrar resultados
        return results

    except ValueError as e:
        raise ValueError(f"Error en el cálculo: {e}")


def soil_loads(soil_bearing_capacity):
    """Estado limite resistencia 1"""

    capacidad_portante_r1 = round(0.45 * soil_bearing_capacity, 2)
    print(capacidad_portante_r1)

    """Estado limite evento extremo 1"""

    capacidad_portante_ex1 = round(0.8 * soil_bearing_capacity, 2)
    print(capacidad_portante_ex1)

    """Estado limite evento extremo 2"""

    capacidad_portante_ex2 = round(0.8 * soil_bearing_capacity, 2)
    print(capacidad_portante_ex2)

    """Estado límite de servicio"""

    capacidad_portante_s = round(0.65 * soil_bearing_capacity, 2)
    print(capacidad_portante_s)


def select_barrier(base_corona):
    if base_corona < 0.30:
        area_barrera = 0.195
        centroide_x_barrera = 0.13
        f = 0.87
    elif base_corona == 0.30:
        area_barrera = 0.18765
        centroide_x_barrera = 0.112494
        f = 0.87
    else:  # base_corona >= 0.35
        area_barrera = 0.21
        centroide_x_barrera = 0.15
        f = 0.87
    return area_barrera, centroide_x_barrera, f


def weight_wall(base_corona, altura_pantalla, base_vastago, pie, base_muro, altura_zapata, angle_inclination, area_barrera, centroide_x_barrera):
    print("BASES y ALTURA", base_muro, altura_zapata)
    DCP1 = round((base_corona * altura_pantalla * 24), 2)
    # print(DCP1)
    DCX1 = round(pie + (base_corona / 2), 2)
    # print(DCX1)

    DCP2 = round(((base_vastago - base_corona) * altura_pantalla * 24) / 2, 2)
    # print(DCP2)
    DCX2 = round(pie + base_corona + (base_vastago - base_corona) / 3, 2)
    # print(DCX2)

    DCP3 = round(base_muro * altura_zapata * 24, 2)
    # print(DCP3)
    DCX3 = round(base_muro / 2, 2)
    # print(DCX3)

    if angle_inclination == 0:
        DCP4 = round(area_barrera * 24, 2)
        DCX4 = round(centroide_x_barrera, 2)
    else:
        DCP4 = 0
        DCX4 = 0

    # print(DCP4)
    # print(DCX4)

    vdc = round((DCP1 + DCP2 + DCP3 + DCP4), 2)
    # print(VDC)

    mdc = round(DCP1*DCX1 + DCP2*DCX2 + DCP3*DCX3 + DCP4*DCX4, 2)
    # print(MDC)
    return {vdc, mdc}


def weight_soil(base_vastago, base_corona, altura_pantalla, unit_weight, pie, talon, angle_inclination):
    print("SUELO")
    EVP5 = round(((base_vastago - base_corona) *
                 altura_pantalla * unit_weight * 10) / 2, 2)
    # print(EVP5)
    EVX5 = round(pie + base_corona + (2 * (base_vastago - base_corona) / 3), 2)
    # print(EVX5)

    EVP6 = round(talon * altura_pantalla * unit_weight * 10, 2)
    # print(EVP6)
    EVX6 = round(pie + base_vastago + (talon / 2), 2)
    # print(EVX6)

    EVP7 = round(((base_vastago - base_corona + talon) * (tan(radians(angle_inclination))
                 * (base_vastago - base_corona + talon)) * unit_weight * 10) / 2, 2)
    # print(base_vastago, base_corona, talon, angle_inclination, unit_weight)

    # print(EVP7)
    EVX7 = round(pie + base_corona +
                 (2 * (base_vastago - base_corona + talon) / 3), 2)
    # print(EVX7)

    vev = round((EVP5 + EVP6 + EVP7), 2)
    # print(VEV)

    mev = round((EVP5 * EVX5 + EVP6 * EVX6 + EVP7 * EVX7), 2)
    # print(MEV)
    return {vev, mev}


def Active_and_passive_thrust(angle_friction, beta_rad, angle_soil_wall, angle_inclination, base_vastago, base_corona, talon, wall_height, unit_weight, altura_zapata, diente):
    print("EMPUJE ACT Y PAS")
    "2.4.1 Empuje activo y pasivo del relleno (EH)"
    # Caso i = 0
    ka1 = round(((tan(radians(45) - (angle_friction / 2))) ** 2), 2)
    # print(ka1)

    # Caso i > 0
    numerador = (cos(angle_friction - radians(beta_rad))) ** 2
    # print(numerador)
    denominador = cos(radians(beta_rad)) ** 2 * \
        cos(angle_soil_wall + radians(beta_rad))
    # print(denominador)
    raiz = sqrt((sin(angle_soil_wall + angle_friction) * sin(angle_friction - radians(angle_inclination))) /
                (cos(angle_soil_wall - radians(beta_rad)) * cos(radians(angle_inclination) - radians(beta_rad))))
    # print(raiz)
    ka2 = round((numerador / (denominador * (1 + raiz))), 2)
    # print(ka2)

    if angle_inclination == 0:
        ka = ka1
    else:
        ka = ka2
    # print(ka)

    """Coeficiente Pasivo"""

    kp = round(((tan(radians(45) + (angle_friction / 2))) ** 2), 2)
    # print(kp)

    """Empuje Activo estatico"""

    # Calculo altura
    h2 = (tan(radians(angle_inclination))) * \
        (base_vastago - base_corona + talon)
    total_height = round((wall_height + h2), 2)
    # print(total_height)

    # Empuje activo
    active_thrust = round(
        ((1 / 2) * ka * (unit_weight * 10) * ((total_height) ** 2)), 2)
    # print(active_thrust)

    # NOTE: Eliminar # Componente vertical
    # vertical_component = round(
    #     (active_thrust * sin(angle_soil_wall + radians(beta_rad))), 2)
    # # print(vertical_component)

    # Componente horizontal
    Horizontal_component = round(
        (active_thrust * cos(angle_soil_wall + radians(beta_rad))), 2)
    # print(Horizontal_component)

    # centroide y
    yEH = round((total_height / 3), 2)
    # print(yEH)

    # Momento en el punto O
    meho = round((Horizontal_component * yEH), 2)
    # print(MEHO)

    """Empuje pasivo"""

    passive_thrust = round(
        ((1 / 2) * kp * (unit_weight * 10) * ((altura_zapata + diente) ** 2)), 2)
    # print(passive_thrust)

    return {ka, kp, total_height, Horizontal_component, meho}


def f_pga(type_soil, pga):
    print("--- FPGA ---")
    # Definimos los valores de la tabla
    tabla = {
        "C": [1.2, 1.2, 1.2, 1.1, 1.1, 1.0],
        "D": [1.6, 1.4, 1.2, 1.1, 1.0, 0.9]
    }

    PGA_valores = [0.1, 0.2, 0.3, 0.4, 0.5, 0.55]  # Valores en la tabla

    if type_soil not in tabla:
        raise ValueError("Tipo de suelo no válido. Debe ser 'C' o 'D'.")

    F_PGA_valores = tabla[type_soil]  # Obtiene la fila correspondiente

    # Si PGA está exactamente en la tabla, devolvemos el valor correspondiente
    if pga in PGA_valores:
        print(F_PGA_valores[PGA_valores.index(pga)])
        return F_PGA_valores[PGA_valores.index(pga)]

    # Si no está, hacemos interpolación lineal
    print(np.interp(pga, PGA_valores, F_PGA_valores))
    return np.interp(pga, PGA_valores, F_PGA_valores)


def seismic_thrust(pga, angle_soil_wall, angle_friction, angle_inclination, beta_rad, unit_weight, total_height, vdc, vev, Horizontal_component, fpga):
    """Coeficiente sismico suponiendo que no hay deslizamiento del muro"""
    print("SISMO")
    # El valor de 1.0 debe calcularse dependiendo del type_soil y PGA
    kho = round((pga * fpga), 2)

    print(kho)

    """Coeficiente sismico horizontal"""

    kh = round((kho * 0.5), 2)
    _1 = radians(kh)
    print(_1)
    print(kh)

    """Coeficiente de empuje dinamico activo"""

    Ɵ = (atan(kh))

    theta_degrees = degrees(Ɵ)
    print(Ɵ)
    print(theta_degrees)

    numerador2 = sin(angle_soil_wall + angle_friction) * \
        sin(angle_friction - Ɵ - radians(angle_inclination))
    denominador2 = cos(angle_soil_wall + radians(beta_rad) + Ɵ) * \
        cos(angle_inclination - radians(beta_rad))
    raiz2 = sqrt(numerador2 / denominador2)
    Ψ = round(((1 + raiz2) ** 2), 2)
    print(Ψ)

    """Coeficiente Empuje dinamico activo"""

    numerador3 = cos(angle_friction - Ɵ - radians(beta_rad)) ** 2
    denominador3 = Ψ * cos(Ɵ) * cos(radians(beta_rad)) * \
        cos(angle_soil_wall + radians(beta_rad) + Ɵ)
    dynamic_active_coefficient = round((numerador3 / denominador3), 2)
    print(dynamic_active_coefficient)

    """Empuje dinamico activo"""

    active_dynamic_thrust = round(
        ((1 / 2) * unit_weight * 10 * dynamic_active_coefficient * (total_height ** 2)), 2)
    print(active_dynamic_thrust)

    """Diferencia de empujes"""

    thrust_difference = round(
        (active_dynamic_thrust - Horizontal_component), 2)
    print(thrust_difference)

    """Calculo de l fuerza PIR"""

    PIR = round(kh * (vdc + vev), 2)
    print(PIR)

    """CombinaciÓn mas desfavorable PSEIS"""

    PSEIS1 = round(thrust_difference + 0.5 * PIR, 2)
    print(PSEIS1)
    PSEIS2 = round(0.5 * thrust_difference + PIR, 2)
    print(PSEIS2)

    PSEIS = round(max(PSEIS1, PSEIS2), 2)
    print(PSEIS)

    # El mayor de los dos

    yPIR = round(total_height * 0.4, 2)
    print(yPIR)

    MPSEIS = round(PSEIS * yPIR, 2)
    print(MPSEIS)
