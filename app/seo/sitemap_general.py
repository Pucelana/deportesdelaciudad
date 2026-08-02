from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_general_bp = Blueprint(
    "sitemap_general",
    __name__
)


@sitemap_general_bp.route("/sitemap_general.xml")
def sitemap_general():

    rutas = obtener_rutas("general")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )