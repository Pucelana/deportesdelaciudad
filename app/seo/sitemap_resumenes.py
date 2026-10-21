from flask import Blueprint, Response
from xml.sax.saxutils import escape

from app.extensions import db
from app.models.resumenes import ResumenJornada

from .utils import (
    BASE_URL,
    frecuencia,
    prioridad,
    ultima_modificacion,
)


sitemap_resumenes_bp = Blueprint(
    "sitemap_resumenes",
    __name__
)


@sitemap_resumenes_bp.route("/sitemap_resumenes.xml")
def sitemap_resumenes():

    # Obtener los periodos reales con resúmenes publicados.
    periodos = db.session.query(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).label("inicio")
    ).filter(
        ResumenJornada.publicado.is_(True)
    ).distinct().order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc()
    ).all()

    rutas = [
        f"/resumenes/{periodo.inicio.isoformat()}"
        for periodo in periodos
    ]

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for ruta in rutas:

        xml.append(f"""
<url>
    <loc>{escape(BASE_URL + ruta)}</loc>
    <lastmod>{ultima_modificacion()}</lastmod>
    <changefreq>{frecuencia(ruta)}</changefreq>
    <priority>{prioridad(ruta)}</priority>
</url>
""")

    xml.append("</urlset>")

    return Response(
        "\n".join(xml),
        mimetype="application/xml"
    )

