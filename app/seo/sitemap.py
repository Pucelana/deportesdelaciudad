from flask import Blueprint, Response
from datetime import datetime

seo_bp = Blueprint("seo", __name__)


@seo_bp.route("/sitemap.xml")
def sitemap():
    hoy = datetime.utcnow().strftime("%Y-%m-%d")

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

    return Response(xml, mimetype="application/xml")