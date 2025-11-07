"""
ruta_grafo_recursiva_mapa.py

Versión recursiva y dinámica con mapa real (Folium, sin API Key).
Calcula la mejor ruta entre ciudades colombianas y genera un mapa interactivo.

Requisitos:
    pip install networkx folium
"""

import networkx as nx
import folium

# ---------------------- COORDENADAS DE CIUDADES ----------------------
# Coordenadas aproximadas de algunas ciudades de Colombia
ciudades = {
    "Bogotá": (4.7110, -74.0721),
    "Ibagué": (4.4389, -75.2322),
    "Medellín": (6.2442, -75.5812),
    "Cali": (3.4516, -76.5320),
    "Barranquilla": (10.9639, -74.7964),
    "Cartagena": (10.3910, -75.4794),
    "Bucaramanga": (7.1254, -73.1198),
    "Villavicencio": (4.1420, -73.6266),
    "Pereira": (4.8143, -75.6946),
    "Manizales": (5.0703, -75.5138),
    "Santa Marta": (11.2408, -74.1990),
    "Neiva": (2.9273, -75.2819),
    "Cúcuta": (7.8939, -72.5078),
    "Popayán": (2.4448, -76.6147),
    "Tunja": (5.5353, -73.3678),
}

# ---------------------- DISTANCIAS SIMPLIFICADAS ----------------------
# Distancias aproximadas (en km)
distancias = {
    ("Bogotá", "Ibagué"): 200,
    ("Bogotá", "Medellín"): 415,
    ("Bogotá", "Cali"): 460,
    ("Bogotá", "Barranquilla"): 1000,
    ("Bogotá", "Cartagena"): 1050,
    ("Bogotá", "Bucaramanga"): 400,
    ("Bogotá", "Villavicencio"): 120,
    ("Ibagué", "Medellín"): 380,
    ("Ibagué", "Cali"): 230,
    ("Ibagué", "Barranquilla"): 960,
    ("Ibagué", "Cartagena"): 1000,
    ("Medellín", "Barranquilla"): 700,
    ("Medellín", "Cartagena"): 640,
    ("Medellín", "Bucaramanga"): 380,
    ("Cali", "Barranquilla"): 1070,
    ("Cali", "Cartagena"): 1040,
    ("Cali", "Bucaramanga"): 720,
    ("Barranquilla", "Cartagena"): 120,
    ("Barranquilla", "Bucaramanga"): 600,
    ("Cartagena", "Bucaramanga"): 580,
    ("Bucaramanga", "Villavicencio"): 450,
}

# Hacer simétrica
for (a, b), d in list(distancias.items()):
    distancias[(b, a)] = d


# ---------------------- FUNCIÓN RECURSIVA ----------------------

def mejor_ruta(origen, destino, paradas, visitadas=None, memo=None):
    """
    Encuentra recursivamente la mejor ruta entre origen y destino pasando por todas las paradas.
    Retorna (distancia_total, camino)
    """
    if visitadas is None:
        visitadas = set()
    if memo is None:
        memo = {}

    estado = (origen, tuple(sorted(paradas - visitadas)))
    if estado in memo:
        return memo[estado]

    # Caso base
    if visitadas == paradas:
        return distancias.get((origen, destino), float("inf")), [origen, destino]

    mejor_dist = float("inf")
    mejor_camino = []

    for ciudad in paradas - visitadas:
        if (origen, ciudad) in distancias:
            d = distancias[(origen, ciudad)]
            sub_dist, sub_camino = mejor_ruta(ciudad, destino, paradas, visitadas | {ciudad}, memo)
            total = d + sub_dist
            if total < mejor_dist:
                mejor_dist = total
                mejor_camino = [origen] + sub_camino

    memo[estado] = (mejor_dist, mejor_camino)
    return memo[estado]


# ---------------------- PROGRAMA PRINCIPAL ----------------------

print("=== RUTA RECURSIVA CON MAPA REAL DE COLOMBIA ===")
print("Ciudades disponibles:")
print(", ".join(sorted(ciudades.keys())))

origen = input("\nOrigen: ").strip() or "Ibagué"
destino = input("Destino: ").strip() or "Barranquilla"
paradas_raw = input("Paradas (separa con ; ej: Medellín; Cartagena): ").strip()
paradas = {p.strip() for p in paradas_raw.split(';') if p.strip()}

if origen not in ciudades or destino not in ciudades or not all(p in ciudades for p in paradas):
    print("⚠️  Alguna ciudad ingresada no está en la lista.")
    exit()

dist_total, camino = mejor_ruta(origen, destino, paradas)

print(f"\n🗺️  Mejor ruta encontrada: {' → '.join(camino)}")
print(f"📏  Distancia total aproximada: {dist_total} km")

# ---------------------- MAPA CON FOLIUM ----------------------

# Centrar mapa en Colombia
mapa = folium.Map(location=[4.5, -74.1], zoom_start=6, tiles="OpenStreetMap")

# Agregar marcadores
for ciudad in camino:
    lat, lon = ciudades[ciudad]
    folium.Marker(
        location=[lat, lon],
        popup=ciudad,
        tooltip=ciudad,
        icon=folium.Icon(color="blue" if ciudad not in [origen, destino] else "green"),
    ).add_to(mapa)

# Dibujar línea de la ruta
puntos = [(ciudades[c][0], ciudades[c][1]) for c in camino]
folium.PolyLine(puntos, color="red", weight=4.5, opacity=0.8).add_to(mapa)

# Guardar mapa
nombre_archivo = "ruta_colombia.html"
mapa.save(nombre_archivo)
print(f"\n✅ Mapa generado correctamente: {nombre_archivo}")
print("Ábrelo en tu navegador para ver la ruta sobre el mapa real de Colombia.")
