from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_playoff_bp = Blueprint(
    "sitemap_playoff",
    __name__
)


@sitemap_playoff_bp.route("/sitemap_playoff.xml")
def sitemap_playoff():

    rutas = obtener_rutas("playoff")

    return Response(
            generar_xml(rutas),
            mimetype="application/xml"
        )