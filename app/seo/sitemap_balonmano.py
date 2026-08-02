from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_balonmano_bp = Blueprint(
    "sitemap_balonmano",
    __name__
)


@sitemap_balonmano_bp.route("/sitemap_balonmano.xml")
def sitemap_balonmano():

    rutas = obtener_rutas("balonmano")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )