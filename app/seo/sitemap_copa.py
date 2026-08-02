from flask import Blueprint, Response
from .utils import obtener_rutas, generar_xml

sitemap_copa_bp = Blueprint(
    "sitemap_copa",
    __name__
)

@sitemap_copa_bp.route("/sitemap_copa.xml")
def sitemap_copa():

    rutas = obtener_rutas("copa")

    return Response(
        generar_xml(rutas),
        mimetype="application/xml"
    )