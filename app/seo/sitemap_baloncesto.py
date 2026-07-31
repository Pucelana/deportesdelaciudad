from flask import Blueprint, Response

from .utils import (
    obtener_rutas,
    generar_xml
)

sitemap_baloncesto_bp = Blueprint(
    "sitemap_baloncesto",
    __name__
)

@sitemap_baloncesto_bp.route("/sitemap_baloncesto.xml")
def sitemap_baloncesto():

    rutas = obtener_rutas("baloncesto")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )