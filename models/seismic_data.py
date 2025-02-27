# Diccionario de datos de municipios y sus características sísmicas
MUNICIPALITY_SEISMIC_DATA = {
    "Cúcuta": {"Aa": 0.35, "Zone": "Alta", "pga": 0.55},
    "Abrego": {"Aa": 0.30, "Zone": "Alta", "pga": 0.25},
    "Arboledas": {"Aa": 0.30, "Zone": "Alta", "pga": 0.35},
    "Bochalema": {"Aa": 0.35, "Zone": "Alta", "pga": 0.45},
    "Bucarasica": {"Aa": 0.30, "Zone": "Alta", "pga": 0.40},
    "Cáchira": {"Aa": 0.25, "Zone": "Alta", "pga": 0.25},
    "Cácota": {"Aa": 0.30, "Zone": "Alta", "pga": 0.35},
    "Chinácota": {"Aa": 0.35, "Zone": "Alta", "pga": 0.45},
    "Chitagá": {"Aa": 0.30, "Zone": "Alta", "pga": 0.35},
    "Convención": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.20},
    "Cucutilla": {"Aa": 0.30, "Zone": "Alta", "pga": 0.35},
    "Durania": {"Aa": 0.35, "Zone": "Alta", "pga": 0.45},
    "El Carmen": {"Aa": 0.15, "Zone": "Intermedia", "pga": 0.20},
    "El Tarra": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.25},
    "El Zulia": {"Aa": 0.35, "Zone": "Alta", "pga": 0.50},
    "Gramalote": {"Aa": 0.30, "Zone": "Alta", "pga": 0.40},
    "Hacarí": {"Aa": 0.25, "Zone": "Alta", "pga": 0.25},
    "Herrán": {"Aa": 0.35, "Zone": "Alta", "pga": 0.55},
    "La Esperanza": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.20},
    "La Playa": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.25},
    "Labateca": {"Aa": 0.35, "Zone": "Alta", "pga": 0.50},
    "Los Patios": {"Aa": 0.35, "Zone": "Alta", "pga": 0.55},
    "Lourdes": {"Aa": 0.30, "Zone": "Alta", "pga": 0.40},
    "Mutiscua": {"Aa": 0.30, "Zone": "Alta", "pga": 0.30},
    "Ocaña": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.20},
    "Pamplona": {"Aa": 0.30, "Zone": "Alta", "pga": 0.40},
    "Pamplonita": {"Aa": 0.35, "Zone": "Alta", "pga": 0.40},
    "Puerto Santander": {"Aa": 0.35, "Zone": "Alta", "pga": 0.50},
    "Ragonvalia": {"Aa": 0.35, "Zone": "Alta", "pga": 0.55},
    "Salazar": {"Aa": 0.30, "Zone": "Alta", "pga": 0.35},
    "San Calixto": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.20},
    "San Cayetano": {"Aa": 0.35, "Zone": "Alta", "pga": 0.50},
    "Santiago": {"Aa": 0.30, "Zone": "Alta", "pga": 0.45},
    "Sardinata": {"Aa": 0.30, "Zone": "Alta", "pga": 0.30},
    "Silos": {"Aa": 0.25, "Zone": "Alta", "pga": 0.45},
    "Teorama": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.20},
    "Tibú": {"Aa": 0.20, "Zone": "Intermedia", "pga": 0.45},
    "Toledo": {"Aa": 0.35, "Zone": "Alta", "pga": 0.55},
    "Villa Caro": {"Aa": 0.30, "Zone": "Alta", "pga": 0.30},
    "Villa del Rosario": {"Aa": 0.35, "Zone": "Alta", "pga": 0.55},
}


def get_municipality():
    return list(MUNICIPALITY_SEISMIC_DATA.keys())


def get_seismic_info(municipio):
    """
    Retorna la información sísmica de un municipio dado.
    :param municipio: Nombre del municipio
    :return: Diccionario con Aa y Zona, o None si el municipio no existe.
    """
    return MUNICIPALITY_SEISMIC_DATA.get(municipio)