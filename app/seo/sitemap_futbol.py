from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_futbol_bp = Blueprint(
    "sitemap_futbol",
    __name__
)


@sitemap_futbol_bp.route("/sitemap_futbol.xml")
def sitemap_futbol():

    rutas = obtener_rutas("futbol")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )