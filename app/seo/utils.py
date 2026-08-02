from datetime import datetime
from flask import current_app

# CONFIGURACIÓN GENERAL SEO

BASE_URL = "https://deportesdelaciudad.es"

# Endpoints que NO deben aparecer nunca en los sitemaps
EXCLUIR_ENDPOINTS = (
    "static",
    "login",
    "logout",
    "register",
    "perfil",
    "admin",
    "crear",
    "editar",
    "modificar",
    "eliminar",
    "api",
    "robots",
    "sitemap"
)

# COMPROBAR SI UNA RUTA SE DEBE EXCLUIR

def excluir(rule):
    """
    Devuelve True si la ruta NO debe aparecer en el sitemap.
    """

    # Solo indexamos páginas GET
    if "GET" not in rule.methods:
        return True

    # No indexar rutas con parámetros
    if rule.arguments:
        return True
    
    if "/admin" in rule.rule:
        return True

    endpoint = rule.endpoint.lower()

    for palabra in EXCLUIR_ENDPOINTS:
        if palabra in endpoint:
            return True

    return False

# OBTENER TODAS LAS RUTAS PÚBLICAS

def obtener_rutas(tipo=None):
    """
    Devuelve todas las rutas públicas válidas.

    Si se indica un tipo, únicamente devuelve las rutas
    de esa categoría.
    """

    rutas = []

    for rule in current_app.url_map.iter_rules():

        if excluir(rule):
            continue

        ruta = rule.rule

        # No incluir rutas dinámicas
        # Ejemplo:
        # /modificar_jornada_galvan/<int:id>
        if "<" in ruta or ">" in ruta:
            continue

        # Si no se especifica categoría,
        # añadimos todas las rutas públicas válidas.
        if tipo is None:
            rutas.append(ruta)
            continue

        # Si se especifica categoría,
        # añadimos únicamente las correspondientes.
        cat = categoria(ruta)

        if "copa" in ruta.lower():
            print(f"{ruta} ---> {cat}")

        cat = categoria(ruta)

        print(ruta, "=>", cat)

        if cat == tipo:
            rutas.append(ruta)

    return sorted(set(rutas))

# CATEGORIZAR CADA URL

def categoria(url):

    url = url.lower()

    # GENERAL
    if url == "/":
        return "general"

    if url.startswith("/seccion"):
        return "general"

    if url == "/resultados":
        return "general"

    if "sistema_ligas" in url:
        return "general"


    # HISTORIAL
    if (
        "historial" in url
        or "temporadas" in url
        or "palmares" in url
    ):
        return "historial"


    # COPAS
    if (
        "copa" in url
        or "copas" in url
        or "supercopa" in url
        or "supercopas" in url
    ):
        return "copa"


    # PLAYOFF
    if (
        "playoff" in url
        or "playoffs" in url
    ):
        return "playoff"


    # EUROPA
    if (
        "europa" in url
        or "eurocup" in url
        or "iberica" in url
    ):
        return "europa"


    # BALONCESTO
    if (
        "uemc" in url
        or "aliados" in url
        or "ponce" in url
        or "cdsi_vall" in url
    ):
        return "baloncesto"


    # BALONMANO
    if (
        "aula" in url
        or "recoletas" in url
    ):
        return "balonmano"


    # HOCKEY
    if (
        "panteras" in url
        or "caja" in url
    ):
        return "hockey"


    # RUGBY
    if (
        "vrac" in url
        or "salvador" in url
        or "salvador_fem" in url
    ):
        return "rugby"


    # FUTSAL
    if (
        "galvan" in url
        or "vall_sala" in url
    ):
        return "futsal"


    # FÚTBOL
    if (
        "futbol" in url
        or "valladolid" in url
        or "promesas" in url
        or "simancas" in url
        or "parquesol" in url
    ):
        return "futbol"


    # VOLEY
    if (
        "vcv" in url
        or "san_jose" in url
    ):
        return "voley"

    return "otros"

# PRIORIDAD

def prioridad(url):

    url = url.lower()

    if url == "/":
        return "1.0"

    if url == "/resultados":
        return "0.95"

    if url.startswith("/seccion"):
        return "0.90"

    if "resultados_" in url:
        return "0.90"

    if "clasif_" in url:
        return "0.90"

    if "calendario_" in url:
        return "0.85"

    if "playoff" in url:
        return "0.80"

    if "copa" in url:
        return "0.80"

    if "supercopa" in url:
        return "0.80"

    if "europa" in url:
        return "0.80"

    if "historial" in url:
        return "0.70"

    if "temporadas" in url:
        return "0.70"

    if "sistema_ligas" in url:
        return "0.80"

    return "0.75"

# FRECUENCIA DE ACTUALIZACIÓN

def frecuencia(url):

    url = url.lower()

    if url == "/":
        return "daily"

    if url == "/resultados":
        return "daily"

    if "resultados_" in url:
        return "daily"

    if "clasif_" in url:
        return "daily"

    if "calendario_" in url:
        return "weekly"

    if "playoff" in url:
        return "weekly"

    if "copa" in url:
        return "weekly"

    if "supercopa" in url:
        return "weekly"

    if "europa" in url:
        return "weekly"

    if "historial" in url:
        return "monthly"

    if "temporadas" in url:
        return "monthly"

    if "sistema_ligas" in url:
        return "monthly"

    return "weekly"

# FECHA ÚLTIMA MODIFICACIÓN
# (Preparado para conectar con PostgreSQL)

def ultima_modificacion():

    return datetime.now().strftime("%Y-%m-%d")

# GENERADOR XML

def generar_xml(urls):

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for url in urls:

        xml.append(f"""
<url>
    <loc>{BASE_URL}{url}</loc>
    <lastmod>{ultima_modificacion()}</lastmod>
    <changefreq>{frecuencia(url)}</changefreq>
    <priority>{prioridad(url)}</priority>
</url>
""")

    xml.append("</urlset>")

    return "\n".join(xml)