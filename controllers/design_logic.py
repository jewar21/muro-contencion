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

            capacidad_portante_r1, capacidad_portante_ex1, capacidad_portante_ex2, capacidad_portante_s = soil_loads(
                soil_bearing_capacity)

            area_barrera, centroide_x_barrera, f = select_barrier(base_corona)

            vdc, mdc = weight_wall(base_corona=base_corona, altura_pantalla=altura_pantalla, base_vastago=base_vastago, pie=pie, base_muro=base_muro,
                                   altura_zapata=altura_zapata, area_barrera=area_barrera, centroide_x_barrera=centroide_x_barrera, angle_inclination=angle_inclination)

            vev, mev = weight_soil(base_vastago, base_corona, altura_pantalla,
                                   unit_weight, pie, talon, angle_inclination)

            ka, kp, total_height, Horizontal_component, meho, passive_thrust = Active_and_passive_thrust(angle_friction, beta_rad, angle_soil_wall, base_vastago, base_corona,
                                                                                                         talon, wall_height, unit_weight, altura_zapata, diente,
                                                                                                         angle_inclination)

            fpga = f_pga(type_soil, pga)

            pseis, mpseis = seismic_thrust(pga, angle_soil_wall, angle_friction,
                                           beta_rad, unit_weight, total_height, vdc, vev, Horizontal_component, fpga, angle_inclination)

            ls, mls = live_load(
                ka=ka, unit_weight=unit_weight, wall_height=wall_height, angle_inclination=angle_inclination)

            vct, mct = barrier_collision(
                wall_height=wall_height, f=f, angle_inclination=angle_inclination)
            # TODO: Las funciones que estan debajo son iguales para el caso 2
            fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin, fvex2cmax, fvex2cmin, fvs = vertical_forces(
                vdc, vev)
            fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs = horizontal_forces(
                ls, pseis, Horizontal_component, vct)
            mvr1cmax, mvr1cmin, mvex1cmax, mvex1cmin, mvex2cmax, mvex2cmin, mvs = horizontal_moments(
                mdc, mev)
            mhr1cmax, mhr1cmin, mhex1cmax, mhex1cmin, mhex2cmax, mhex2cmin, mhs = vertical_moments(
                mls, meho, mpseis, mct)
            slip_verification(angle_friction, passive_thrust, fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin,
                              fvex2cmax, fvex2cmin, fvs, fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs)
            eR1CMAX, eR1CMIN, eEX1CMAX, eEX1CMIN, eEX2CMAX, eEX2CMIN, eS = rollover_verification(
                base_muro, mvr1cmax, mhr1cmax, fvr1cmax, mvr1cmin, mhr1cmin, fvr1cmin, mvex1cmax, mhex1cmax, fvex1cmax, mvex1cmin, mhex1cmin, fvex1cmin, mvex2cmax, mhex2cmax, fvex2cmax, mvex2cmin, mhex2cmin, fvex2cmin, mvs, mhs, fvs)
            stress_verification(base_muro, fvr1cmax, eR1CMAX, capacidad_portante_ex1, capacidad_portante_r1, fvr1cmin, eR1CMIN, fvex1cmax,
                                eEX1CMAX, capacidad_portante_ex2, fvex1cmin, eEX1CMIN, fvex2cmax, eEX2CMAX, fvex2cmin, eEX2CMIN, fvs, eS, capacidad_portante_s)

        elif select_design == "Sin inclinación - vías":
            capacidad_portante_r1, capacidad_portante_ex1, capacidad_portante_ex2, capacidad_portante_s = soil_loads(
                soil_bearing_capacity)

            area_barrera, centroide_x_barrera, f = select_barrier(base_corona)

            vdc, mdc = weight_wall(base_corona=base_corona, altura_pantalla=altura_pantalla, base_vastago=base_vastago, pie=pie, base_muro=base_muro,
                                   altura_zapata=altura_zapata, area_barrera=area_barrera, centroide_x_barrera=centroide_x_barrera)

            vev, mev = weight_soil(base_vastago, base_corona, altura_pantalla,
                                   unit_weight, pie, talon)

            ka, kp, total_height, Horizontal_component, meho, passive_thrust = Active_and_passive_thrust(angle_friction, beta_rad, angle_soil_wall, base_vastago, base_corona,
                                                                                                         talon, wall_height, unit_weight, altura_zapata, diente)
            fpga = f_pga(type_soil, pga)

            pseis, mpseis = seismic_thrust(pga, angle_soil_wall, angle_friction,
                                           beta_rad, unit_weight, total_height, vdc, vev, Horizontal_component, fpga)

            ls, mls = live_load(
                ka=ka, unit_weight=unit_weight, wall_height=wall_height)

            vct, mct = barrier_collision(wall_height=wall_height, f=f)

            fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin, fvex2cmax, fvex2cmin, fvs = vertical_forces(
                vdc, vev)
            fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs = horizontal_forces(
                ls, pseis, Horizontal_component, vct)
            mvr1cmax, mvr1cmin, mvex1cmax, mvex1cmin, mvex2cmax, mvex2cmin, mvs = horizontal_moments(
                mdc, mev)
            mhr1cmax, mhr1cmin, mhex1cmax, mhex1cmin, mhex2cmax, mhex2cmin, mhs = vertical_moments(
                mls, meho, mpseis, mct)
            slip_verification(angle_friction, passive_thrust, fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin,
                              fvex2cmax, fvex2cmin, fvs, fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs)
            eR1CMAX, eR1CMIN, eEX1CMAX, eEX1CMIN, eEX2CMAX, eEX2CMIN, eS = rollover_verification(
                base_muro, mvr1cmax, mhr1cmax, fvr1cmax, mvr1cmin, mhr1cmin, fvr1cmin, mvex1cmax, mhex1cmax, fvex1cmax, mvex1cmin, mhex1cmin, fvex1cmin, mvex2cmax, mhex2cmax, fvex2cmax, mvex2cmin, mhex2cmin, fvex2cmin, mvs, mhs, fvs)
            stress_verification(base_muro, fvr1cmax, eR1CMAX, capacidad_portante_ex1, capacidad_portante_r1, fvr1cmin, eR1CMIN, fvex1cmax,
                                eEX1CMAX, capacidad_portante_ex2, fvex1cmin, eEX1CMIN, fvex2cmax, eEX2CMAX, fvex2cmin, eEX2CMIN, fvs, eS, capacidad_portante_s)

        elif select_design == "Sin inclinación":
            # TODO: Esto es igual al caso anterior
            capacidad_portante_r1, capacidad_portante_ex1, capacidad_portante_ex2, capacidad_portante_s = soil_loads(
                soil_bearing_capacity)

            area_barrera, centroide_x_barrera, f = select_barrier(base_corona)

            vdc, mdc = weight_wall(base_corona=base_corona, altura_pantalla=altura_pantalla, base_vastago=base_vastago, pie=pie, base_muro=base_muro,
                                   altura_zapata=altura_zapata, area_barrera=area_barrera, centroide_x_barrera=centroide_x_barrera, case3=True)

            vev, mev = weight_soil(base_vastago, base_corona, altura_pantalla,
                                   unit_weight, pie, talon)

            ka, kp, total_height, Horizontal_component, meho, passive_thrust = Active_and_passive_thrust(angle_friction, beta_rad, angle_soil_wall, base_vastago, base_corona,
                                                                                                         talon, wall_height, unit_weight, altura_zapata, diente)
            fpga = f_pga(type_soil, pga)

            pseis, mpseis = seismic_thrust(pga, angle_soil_wall, angle_friction,
                                           beta_rad, unit_weight, total_height, vdc, vev, Horizontal_component, fpga)
            # -----------------------------------------------------

            ls, mls = live_load()

            vct, mct = barrier_collision(case3=True)
            # -----------------------------------------------------
            fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin, fvex2cmax, fvex2cmin, fvs = vertical_forces(
                vdc, vev)
            fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs = horizontal_forces(
                ls, pseis, Horizontal_component, vct)
            mvr1cmax, mvr1cmin, mvex1cmax, mvex1cmin, mvex2cmax, mvex2cmin, mvs = horizontal_moments(
                mdc, mev)
            mhr1cmax, mhr1cmin, mhex1cmax, mhex1cmin, mhex2cmax, mhex2cmin, mhs = vertical_moments(
                mls, meho, mpseis, mct)
            slip_verification(angle_friction, passive_thrust, fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin,
                              fvex2cmax, fvex2cmin, fvs, fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs)
            eR1CMAX, eR1CMIN, eEX1CMAX, eEX1CMIN, eEX2CMAX, eEX2CMIN, eS = rollover_verification(
                base_muro, mvr1cmax, mhr1cmax, fvr1cmax, mvr1cmin, mhr1cmin, fvr1cmin, mvex1cmax, mhex1cmax, fvex1cmax, mvex1cmin, mhex1cmin, fvex1cmin, mvex2cmax, mhex2cmax, fvex2cmax, mvex2cmin, mhex2cmin, fvex2cmin, mvs, mhs, fvs)
            stress_verification(base_muro, fvr1cmax, eR1CMAX, capacidad_portante_ex1, capacidad_portante_r1, fvr1cmin, eR1CMIN, fvex1cmax,
                                eEX1CMAX, capacidad_portante_ex2, fvex1cmin, eEX1CMIN, fvex2cmax, eEX2CMAX, fvex2cmin, eEX2CMIN, fvs, eS, capacidad_portante_s)

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
    """Estado limite evento extremo 1"""

    capacidad_portante_ex1 = round(0.8 * soil_bearing_capacity, 2)
    """Estado limite evento extremo 2"""

    capacidad_portante_ex2 = round(0.8 * soil_bearing_capacity, 2)
    """Estado límite de servicio"""

    capacidad_portante_s = round(0.65 * soil_bearing_capacity, 2)
    print("soil_loads", capacidad_portante_r1, capacidad_portante_ex1,
          capacidad_portante_ex2, capacidad_portante_s)
    return (capacidad_portante_r1, capacidad_portante_ex1, capacidad_portante_ex2, capacidad_portante_s)


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
    print("select_barrier", area_barrera, centroide_x_barrera, f)
    return (area_barrera, centroide_x_barrera, f)


def weight_wall(base_corona, altura_pantalla, base_vastago, pie, base_muro, altura_zapata, area_barrera, centroide_x_barrera, angle_inclination=0, case3=False):

    DCP1 = round((base_corona * altura_pantalla * 24), 2)
    DCX1 = round(pie + (base_corona / 2), 2)
    DCP2 = round(((base_vastago - base_corona) * altura_pantalla * 24) / 2, 2)
    DCX2 = round(pie + base_corona + (base_vastago - base_corona) / 3, 2)
    DCP3 = round(base_muro * altura_zapata * 24, 2)
    DCX3 = round(base_muro / 2, 2)

    if angle_inclination == 0:
        DCP4 = round(area_barrera * 24, 2)
        DCX4 = round(centroide_x_barrera, 2)
    elif case3:
        DCP4 = 0
        DCX4 = 0
    else:
        DCP4 = 0
        DCX4 = 0

    vdc = round((DCP1 + DCP2 + DCP3 + DCP4), 2)
    mdc = round(DCP1*DCX1 + DCP2*DCX2 + DCP3*DCX3 + DCP4*DCX4, 2)
    print("weight_wall", vdc, mdc)

    return (vdc, mdc)


def weight_soil(base_vastago, base_corona, altura_pantalla, unit_weight, pie, talon, angle_inclination=0):

    EVP5 = round(((base_vastago - base_corona) *
                 altura_pantalla * unit_weight * 10) / 2, 2)
    EVX5 = round(pie + base_corona + (2 * (base_vastago - base_corona) / 3), 2)
    EVP6 = round(talon * altura_pantalla * unit_weight * 10, 2)
    EVX6 = round(pie + base_vastago + (talon / 2), 2)
    EVP7 = round(((base_vastago - base_corona + talon) * (tan(radians(angle_inclination))
                 * (base_vastago - base_corona + talon)) * unit_weight * 10) / 2, 2)
    EVX7 = round(pie + base_corona +
                 (2 * (base_vastago - base_corona + talon) / 3), 2)
    vev = round((EVP5 + EVP6 + EVP7), 2)
    mev = round((EVP5 * EVX5 + EVP6 * EVX6 + EVP7 * EVX7), 2)

    print("weight_soil", vev, mev)

    return (vev, mev)


def Active_and_passive_thrust(angle_friction, beta_rad, angle_soil_wall, base_vastago, base_corona, talon, wall_height, unit_weight, altura_zapata, diente, angle_inclination=0):
    "2.4.1 Empuje activo y pasivo del relleno (EH)"
    # Caso i = 0
    ka1 = round(((tan(radians(45) - (angle_friction / 2))) ** 2), 2)

    # Caso i > 0
    numerador = (cos(angle_friction - radians(beta_rad))) ** 2
    denominador = cos(radians(beta_rad)) ** 2 * \
        cos(angle_soil_wall + radians(beta_rad))
    raiz = sqrt((sin(angle_soil_wall + angle_friction) * sin(angle_friction - radians(angle_inclination))) /
                (cos(angle_soil_wall - radians(beta_rad)) * cos(radians(angle_inclination) - radians(beta_rad))))
    ka2 = round((numerador / (denominador * (1 + raiz))), 2)

    if angle_inclination == 0:
        ka = ka1
    else:
        ka = ka2

    """Coeficiente Pasivo"""

    kp = round(((tan(radians(45) + (angle_friction / 2))) ** 2), 2)

    """Empuje Activo estatico"""

    # Calculo altura
    h2 = (tan(radians(angle_inclination))) * \
        (base_vastago - base_corona + talon)
    total_height = round((wall_height + h2), 2)
    print("TOTAL HEIGHT CALCULADO", total_height)

    # Empuje activo
    active_thrust = round(
        ((1 / 2) * ka * (unit_weight * 10) * ((total_height) ** 2)), 2)

    # NOTE: Eliminar # Componente vertical
    # vertical_component = round(
    #     (active_thrust * sin(angle_soil_wall + radians(beta_rad))), 2)
    # # print(vertical_component)

    # Componente horizontal
    Horizontal_component = round(
        (active_thrust * cos(angle_soil_wall + radians(beta_rad))), 2)

    # centroide y
    yEH = round((total_height / 3), 2)

    # Momento en el punto O
    meho = round((Horizontal_component * yEH), 2)

    """Empuje pasivo"""

    passive_thrust = round(
        ((1 / 2) * kp * (unit_weight * 10) * ((altura_zapata + diente) ** 2)), 2)

    print("Active_and_passive_thrust", ka, kp, total_height,
          Horizontal_component, meho, passive_thrust)

    return (ka, kp, total_height, Horizontal_component, meho, passive_thrust)


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


def seismic_thrust(pga, angle_soil_wall, angle_friction, beta_rad, unit_weight, total_height, vdc, vev, Horizontal_component, fpga, angle_inclination=0):
    """Coeficiente sismico suponiendo que no hay deslizamiento del muro"""
    print("SISMO")
    # El valor de 1.0 debe calcularse dependiendo del type_soil y PGA
    kho = round((pga * fpga), 2)

    """Coeficiente sismico horizontal"""

    kh = round((kho * 0.5), 2)
    _1 = radians(kh)

    """Coeficiente de empuje dinamico activo"""

    Ɵ = (atan(kh))

    numerador2 = sin(angle_soil_wall + angle_friction) * \
        sin(angle_friction - Ɵ - radians(angle_inclination))
    denominador2 = cos(angle_soil_wall + radians(beta_rad) + Ɵ) * \
        cos(angle_inclination - radians(beta_rad))
    raiz2 = sqrt(numerador2 / denominador2)
    Ψ = round(((1 + raiz2) ** 2), 2)

    """Coeficiente Empuje dinamico activo"""

    numerador3 = cos(angle_friction - Ɵ - radians(beta_rad)) ** 2
    denominador3 = Ψ * cos(Ɵ) * cos(radians(beta_rad)) * \
        cos(angle_soil_wall + radians(beta_rad) + Ɵ)
    dynamic_active_coefficient = round((numerador3 / denominador3), 2)

    """Empuje dinamico activo"""
    print("TOTAL HEIGHT --->", total_height)
    active_dynamic_thrust = round(
        ((1 / 2) * unit_weight * 10 * dynamic_active_coefficient * (total_height ** 2)), 2)

    """Diferencia de empujes"""

    thrust_difference = round(
        (active_dynamic_thrust - Horizontal_component), 2)

    """Calculo de l fuerza PIR"""

    pir = round(kh * (vdc + vev), 2)

    """CombinaciÓn mas desfavorable PSEIS"""

    pseis1 = round(thrust_difference + 0.5 * pir, 2)
    pseis2 = round(0.5 * thrust_difference + pir, 2)

    pseis = round(max(pseis1, pseis2), 2)

    # El mayor de los dos

    yPIR = round(total_height * 0.4, 2)

    mpseis = round(pseis * yPIR, 2)
    print(pseis, mpseis)

    return (pseis, mpseis)


def live_load(ka=0, unit_weight=0, wall_height=0, angle_inclination=0):
    print("""# 2.4.3 sobrecarga por carga viva (LS)""")

    heq = 0.6
    delta_p = (ka * (unit_weight * 9.806) * heq * 100 * ((10) ** (-3)))
    print(delta_p)

    if angle_inclination == 0:
        ls = round(wall_height * delta_p, 2)
    else:
        ls = 0

    yLS = round(wall_height / 2, 2)
    print(yLS)

    mls = round(ls * yLS, 2)
    print(ls, mls)
    return (ls, mls)


def barrier_collision(wall_height=0, f=0, angle_inclination=0, case3=False):
    print("""# 2.4.4 Fuerza de colisión CT sobre la barrera""")
    """# 2.4.4 Fuerza de colisión CT sobre la barrera"""
    fhb = 240
    lifh = 1.07

    if angle_inclination == 0:
        vct = round(fhb / (lifh + wall_height + f), 2)
    elif case3:
        vct = 0
        mct = 0
    else:
        vct = round(fhb / (lifh + wall_height + f), 2)
        yct = round(0.81 + wall_height, 2)
        mct = round(vct * yct, 2)


def vertical_forces(vdc, vev):
    # print("""# FUERZAS VERTICALES DC+EV""")
    """# FUERZAS VERTICALES DC+EV"""

    fvr1cmax = round(1.25 * vdc + 1.35 * vev, 2)
    fvr1cmin = round(0.9 * vdc + vev, 2)
    fvex1cmax = round(1.25 * vdc + 1.35 * vev, 2)
    fvex1cmin = round(0.9 * vdc + vev, 2)
    fvex2cmax = round(1.25 * vdc + 1.35 * vev, 2)
    fvex2cmin = round(0.9 * vdc + vev, 2)
    fvs = round(1 * vdc + 1 * vev, 2)
    print(fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin, fvex2cmax, fvex2cmin, fvs)

    return (fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin, fvex2cmax, fvex2cmin, fvs)


def horizontal_forces(ls, pseis, Horizontal_component, vct):
    # print("""# FUERZAS HORIZONTALES EH+LS, CT, EQ""")
    """# FUERZAS HORIZONTALES EH+LS, CT, EQ"""

    fhr1cmax = round(1.75 * ls + 1.5 * Horizontal_component, 2)
    fhr1cmin = round(1.75 * ls + 0.9 * Horizontal_component, 2)
    fhex1cmax = round(0.5 * ls + 1.5 * Horizontal_component + 1 * pseis, 2)
    fhex1cmin = round(0.5 * ls + 0.9 * Horizontal_component + 1 * pseis, 2)
    fhex2cmax = round(0.5 * ls + 1.5 * Horizontal_component + 1 * vct, 2)
    fhex2cmin = round(0.5 * ls + 0.9 * Horizontal_component + 1 * vct, 2)
    fhs = round(1 * ls + 1 * Horizontal_component, 2)
    print(fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs)

    return (fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs)


def horizontal_moments(mdc, mev):
    print("# MOMENTOS DC+EV")
    """# MOMENTOS DC+EV"""

    mvr1cmax = round(1.25 * mdc + 1.35 * mev, 2)
    mvr1cmin = round(0.9 * mdc + mev, 2)
    mvex1cmax = round(1.25 * mdc + 1.35 * mev, 2)
    mvex1cmin = round(0.9 * mdc + mev, 2)
    mvex2cmax = round(1.25 * mdc + 1.35 * mev, 2)
    mvex2cmin = round(0.9 * mdc + mev, 2)
    mvs = round(1 * mdc + 1 * mev, 2)
    print(mvr1cmax, mvr1cmin, mvex1cmax, mvex1cmin, mvex2cmax, mvex2cmin, mvs)

    return (mvr1cmax, mvr1cmin, mvex1cmax, mvex1cmin, mvex2cmax, mvex2cmin, mvs)


def vertical_moments(mls, meho, mpseis, mct):

    print("# MOMENTOS DC+EV")
    """# MOMENTOS MH EH+LS Y CT"""

    mhr1cmax = round(1.75 * mls + 1.5 * meho, 2)
    mhr1cmin = round(1.75 * mls + 0.9 * meho, 2)
    mhex1cmax = round(0.5 * mls + 1.5 * meho + 1 * mpseis, 2)
    mhex1cmin = round(0.5 * mls + 0.9 * meho + 1 * mpseis, 2)
    mhex2cmax = round(0.5 * mls + 1.5 * meho + 1 * mct, 2)
    mhex2cmin = round(0.5 * mls + 0.9 * meho + 1 * mct, 2)
    mhs = round(1 * mls + 1 * meho, 2)

    print(mhr1cmax, mhr1cmin, mhex1cmax, mhex1cmin, mhex2cmax, mhex2cmin, mhs)

    return (mhr1cmax, mhr1cmin, mhex1cmax, mhex1cmin, mhex2cmax, mhex2cmin, mhs)


def slip_verification(angle_friction, passive_thrust, fvr1cmax, fvr1cmin, fvex1cmax, fvex1cmin, fvex2cmax, fvex2cmin, fvs, fhr1cmax, fhr1cmin, fhex1cmax, fhex1cmin, fhex2cmax, fhex2cmin, fhs):
    print("""# VERIFICACION  DE LA ESTABILIDAD AL DESLIZAMIENTO DEL MURO""")
    """# VERIFICACION  DE LA ESTABILIDAD AL DESLIZAMIENTO DEL MURO"""

    RRR1CMAX = round(0.8 * tan(angle_friction) *
                     fvr1cmax + 0.5 * passive_thrust, 2)

    if fhr1cmax < RRR1CMAX:
        print("Cumple")
    else:
        print("No cumple")

    RRR1CMIN = round(0.8 * tan(angle_friction) *
                     fvr1cmin + 0.5 * passive_thrust, 2)

    if fhr1cmin < RRR1CMIN:
        print("Cumple")
    else:
        print("No cumple")

    RREX1CMAX = round(0.8 * tan(angle_friction) *
                      fvex1cmax + 0.5 * passive_thrust, 2)

    if fhex1cmax < RREX1CMAX:
        print("Cumple")
    else:
        print("No cumple")

    RREX1CMIN = round(0.8 * tan(angle_friction) *
                      fvex1cmin + 0.5 * passive_thrust, 2)
    print(RREX1CMIN)

    if fhex1cmin < RREX1CMIN:
        print("Cumple")
    else:
        print("No cumple")

    RREX2CMAX = round(0.8 * tan(angle_friction) *
                      fvex2cmax + 0.5 * passive_thrust, 2)

    if fhex2cmax < RREX2CMAX:
        print("Cumple")
    else:
        print("No cumple")

    RREXC2MIN = round(0.8 * tan(angle_friction) *
                      fvex2cmin + 0.5 * passive_thrust, 2)

    if fhex2cmin < RREXC2MIN:
        print("Cumple")
    else:
        print("No cumple")

    RRS = round(0.8 * tan(angle_friction) * fvs + 0.5 * passive_thrust, 2)

    if fhs < RRS:
        print("Cumple")
    else:
        print("No cumple")


def rollover_verification(base_muro, mvr1cmax, mhr1cmax, fvr1cmax, mvr1cmin, mhr1cmin, fvr1cmin, mvex1cmax, mhex1cmax, fvex1cmax, mvex1cmin, mhex1cmin, fvex1cmin, mvex2cmax, mhex2cmax, fvex2cmax, mvex2cmin, mhex2cmin, fvex2cmin, mvs, mhs, fvs):
    print("""# VERIFICACION  DE LA ESTABILIDAD AL VOLCAMIENTO DEL MURO""")
    """# VERIFICACION  DE LA ESTABILIDAD AL VOLCAMIENTO DEL MURO"""

    eMAX = round((base_muro / 3), 2)
    print(eMAX)

    dR1CMAX = round((mvr1cmax - mhr1cmax) / fvr1cmax, 2)
    print(dR1CMAX)
    eR1CMAX = round((base_muro / 2) - dR1CMAX, 2)
    print(eR1CMAX)

    if eMAX > eR1CMAX:
        print("Cumple")
    else:
        print("No cumple")

    dR1CMIN = round((mvr1cmin - mhr1cmin) / fvr1cmin, 2)
    print(dR1CMIN)
    eR1CMIN = round((base_muro / 2) - dR1CMIN, 2)
    print(eR1CMIN)

    if eMAX > eR1CMIN:
        print("Cumple")
    else:
        print("No cumple")

    dEX1CMAX = round((mvex1cmax - mhex1cmax) / fvex1cmax, 2)
    print(dEX1CMAX)
    eEX1CMAX = round((base_muro / 2) - dEX1CMAX, 2)
    print(eEX1CMAX)

    if eMAX > eEX1CMAX:
        print("Cumple")
    else:
        print("No cumple")

    dEX1CMIN = round((mvex1cmin - mhex1cmin) / fvex1cmin, 2)
    print(dEX1CMIN)
    eEX1CMIN = round((base_muro / 2) - dEX1CMIN, 2)
    print(eEX1CMIN)

    if eMAX > eEX1CMIN:
        print("Cumple")
    else:
        print("No cumple")

    dEX2CMAX = round((mvex2cmax - mhex2cmax) / fvex2cmax, 2)
    print(dEX2CMAX)
    eEX2CMAX = round((base_muro / 2) - dEX2CMAX, 2)
    print(eEX2CMAX)

    if eMAX > eEX2CMAX:
        print("Cumple")
    else:
        print("No cumple")

    dEX2CMIN = round((mvex2cmin - mhex2cmin) / fvex2cmin, 2)
    print(dEX2CMIN)
    eEX2CMIN = round((base_muro / 2) - dEX2CMIN, 2)
    print(eEX2CMIN)

    if eMAX > eEX2CMIN:
        print("Cumple")
    else:
        print("No cumple")

    dS = round((mvs - mhs) / fvs, 2)
    print(dS)
    eS = round((base_muro / 2) - dS, 2)
    print(eS)

    if eMAX > eS:
        print("Cumple")
    else:
        print("No cumple")

    return (eR1CMAX, eR1CMIN, eEX1CMAX, eEX1CMIN, eEX2CMAX, eEX2CMIN, eS)


def stress_verification(base_muro, FVR1CMAX, eR1CMAX, capacidad_portante_ex1, capacidad_portante_r1, fVR1CMIN, eR1CMIN, fVEX1CMAX, eEX1CMAX, capacidad_portante_ex2, fVEX1CMIN, eEX1CMIN, fVEX2CMAX, eEX2CMAX, fVEX2CMIN, eEX2CMIN, fvs, eS, capacidad_portante_s):
    """# ESFUERZO ULTIMO ACTUANTE SOBRE SUELO NO ROCOSO"""

    esfuerzoR1CMAX = round(FVR1CMAX / (base_muro - 2 * eR1CMAX), 2)
    print(esfuerzoR1CMAX)

    if capacidad_portante_r1 > esfuerzoR1CMAX:
        print("Cumple")
    else:
        print("No cumple")

    esfuerzoR1CMIN = round(fVR1CMIN / (base_muro - 2 * eR1CMIN), 2)
    print(esfuerzoR1CMIN)

    if capacidad_portante_ex1 > esfuerzoR1CMIN:
        print("Cumple")
    else:
        print("No cumple")

    esfuerzoEX1CMAX = round(fVEX1CMAX / (base_muro - 2 * eEX1CMAX), 2)
    print(esfuerzoEX1CMAX)

    if capacidad_portante_ex2 > esfuerzoEX1CMAX:
        print("Cumple")
    else:
        print("No cumple")

    esfuerzoEX1CMIN = round(fVEX1CMIN / (base_muro - 2 * eEX1CMIN), 2)
    print(esfuerzoEX1CMIN)

    if capacidad_portante_ex2 > esfuerzoEX1CMIN:
        print("Cumple")
    else:
        print("No cumple")

    esfuerzoEX2CMAX = round(fVEX2CMAX / (base_muro - 2 * eEX2CMAX), 2)
    print(esfuerzoEX2CMAX)

    if capacidad_portante_ex2 > esfuerzoEX2CMAX:
        print("Cumple")
    else:
        print("No cumple")

    esfuerzoEX2CMIN = round(fVEX2CMIN / (base_muro - 2 * eEX2CMIN), 2)
    print(esfuerzoEX2CMIN)

    if capacidad_portante_ex2 > esfuerzoEX2CMIN:
        print("Cumple")
    else:
        print("No cumple")

    esfuerzoS = round(fvs / (base_muro - 2 * eS), 2)
    print(esfuerzoS)

    if capacidad_portante_s > esfuerzoS:
        print("Cumple")
    else:
        print("No cumple")
