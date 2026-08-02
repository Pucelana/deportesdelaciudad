from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_rugby_bp = Blueprint(
    "sitemap_rugby",
    __name__
)


@sitemap_rugby_bp.route("/sitemap_rugby.xml")
def sitemap_rugby():

    rutas = obtener_rutas("rugby")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )