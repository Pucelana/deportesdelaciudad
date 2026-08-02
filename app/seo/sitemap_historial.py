from flask import Blueprint, Response, current_app

from .utils import generar_xml


sitemap_historial_bp = Blueprint(
    "sitemap_historial",
    __name__
)


@sitemap_historial_bp.route("/sitemap_historial.xml")
def sitemap_historial():

    rutas = []

    for rule in current_app.url_map.iter_rules():

        if rule.methods and "GET" not in rule.methods:
            continue

        ruta = str(rule)

        # Excluir administración
        if "/admin" in ruta:
            continue

        # Solo páginas públicas de historial
        if "/historial" in ruta:
            rutas.append(ruta)

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )