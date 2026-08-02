from flask import Blueprint, Response

from .utils import obtener_rutas, generar_xml


sitemap_futsal_bp = Blueprint(
    "sitemap_futsal",
    __name__
)


@sitemap_futsal_bp.route("/sitemap_futsal.xml")
def sitemap_futsal():

    rutas = obtener_rutas("futsal")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )