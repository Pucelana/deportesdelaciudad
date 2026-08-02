from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_hockey_bp = Blueprint(
    "sitemap_hockey",
    __name__
)


@sitemap_hockey_bp.route("/sitemap_hockey.xml")
def sitemap_hockey():

    rutas = obtener_rutas("hockey")

    return Response(
            generar_xml(rutas),
            mimetype="application/xml"
        )