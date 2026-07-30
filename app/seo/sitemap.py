from flask import Blueprint, Response, current_app
from datetime import datetime

seo_bp = Blueprint("seo", __name__)


@seo_bp.route("/sitemap.xml")
def sitemap():
    hoy = datetime.utcnow().strftime("%Y-%m-%d")

    urls = []

    for rule in current_app.url_map.iter_rules():

        # Excluir rutas del panel de administración
        if rule.rule.startswith("/admin"):
            continue

        # Excluir archivos estáticos
        if rule.rule.startswith("/static"):
            continue

        # Excluir rutas con parámetros
        if len(rule.arguments) > 0:
            continue

    urls.append(rule.rule)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>https://deportesdelaciudad.es/</loc>
        <lastmod>{hoy}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>

    </urlset>
    """
    return "<br>".join(sorted(urls))

    """return Response(xml, mimetype="application/xml")"""
