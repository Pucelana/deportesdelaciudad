from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_europa_bp = Blueprint(
    "sitemap_europa",
    __name__
)


@sitemap_europa_bp.route("/sitemap_europa.xml")
def sitemap_europa():

    rutas = obtener_rutas("europa")

    return Response(
            generar_xml(rutas),
            mimetype="application/xml"
        )