from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_voley_bp = Blueprint(
    "sitemap_voley",
    __name__
)


@sitemap_voley_bp.route("/sitemap_voley.xml")
def sitemap_voley():

    rutas = obtener_rutas("voley")

    return Response(
            generar_xml(rutas),
            mimetype="application/xml"
        )