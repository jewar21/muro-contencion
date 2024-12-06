# Diccionario de datos de municipios y sus características sísmicas
MUNICIPALITY_SEISMIC_DATA = {
    "Cúcuta": {"Aa": 0.35, "Zone": "Alta"},
    "Abrego": {"Aa": 0.30, "Zone": "Alta"},
    "Arboledas": {"Aa": 0.30, "Zone": "Alta"},
    "Bochalema": {"Aa": 0.35, "Zone": "Alta"},
    "Bucarasica": {"Aa": 0.30, "Zone": "Alta"},
    "Cáchira": {"Aa": 0.25, "Zone": "Alta"},
    "Cácota": {"Aa": 0.30, "Zone": "Alta"},
    "Chinácota": {"Aa": 0.35, "Zone": "Alta"},
    "Chitagá": {"Aa": 0.30, "Zone": "Alta"},
    "Convención": {"Aa": 0.20, "Zone": "Intermedia"},
    "Cucutilla": {"Aa": 0.30, "Zone": "Alta"},
    "Durania": {"Aa": 0.35, "Zone": "Alta"},
    "El Carmen": {"Aa": 0.15, "Zone": "Intermedia"},
    "El Tarra": {"Aa": 0.20, "Zone": "Intermedia"},
    "El Zulia": {"Aa": 0.35, "Zone": "Alta"},
    "Gramalote": {"Aa": 0.30, "Zone": "Alta"},
    "Hacarí": {"Aa": 0.25, "Zone": "Alta"},
    "Herrán": {"Aa": 0.35, "Zone": "Alta"},
    "La Esperanza": {"Aa": 0.20, "Zone": "Intermedia"},
    "La Playa": {"Aa": 0.20, "Zone": "Intermedia"},
    "Labateca": {"Aa": 0.35, "Zone": "Alta"},
    "Los Patios": {"Aa": 0.35, "Zone": "Alta"},
    "Lourdes": {"Aa": 0.30, "Zone": "Alta"},
    "Mutiscua": {"Aa": 0.30, "Zone": "Alta"},
    "Ocaña": {"Aa": 0.20, "Zone": "Intermedia"},
    "Pamplona": {"Aa": 0.30, "Zone": "Alta"},
    "Pamplonita": {"Aa": 0.35, "Zone": "Alta"},
    "Puerto Santander": {"Aa": 0.35, "Zone": "Alta"},
    "Ragonvalia": {"Aa": 0.35, "Zone": "Alta"},
    "Salazar": {"Aa": 0.30, "Zone": "Alta"},
    "San Calixto": {"Aa": 0.20, "Zone": "Intermedia"},
    "San Cayetano": {"Aa": 0.35, "Zone": "Alta"},
    "Santiago": {"Aa": 0.30, "Zone": "Alta"},
    "Sardinata": {"Aa": 0.30, "Zone": "Alta"},
    "Silos": {"Aa": 0.25, "Zone": "Alta"},
    "Teorama": {"Aa": 0.20, "Zone": "Intermedia"},
    "Tibú": {"Aa": 0.20, "Zone": "Intermedia"},
    "Toledo": {"Aa": 0.35, "Zone": "Alta"},
    "Villa Caro": {"Aa": 0.30, "Zone": "Alta"},
    "Villa del Rosario": {"Aa": 0.35, "Zone": "Alta"},
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
