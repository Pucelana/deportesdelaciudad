from flask import Blueprint, Response
from .utils import BASE_URL

sitemap_index_bp = Blueprint("sitemap_index", __name__)

@sitemap_index_bp.route("/sitemap.xml")
def sitemap_index():
    sitemaps = [
        "sitemap_general.xml",

        "sitemap_baloncesto.xml",

        "sitemap_futbol.xml",

        "sitemap_balonmano.xml",

        "sitemap_hockey.xml",

        "sitemap_rugby.xml",

        "sitemap_futsal.xml",

        "sitemap_voley.xml",
        
        "sitemap_playoff.xml",

        "sitemap_copas.xml",

        "sitemap_europa.xml",

        "sitemap_historial.xml"
    ]

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for sitemap in sitemaps:

        xml.append(f"""
<sitemap>
    <loc>{BASE_URL}/{sitemap}</loc>
</sitemap>
""")
    xml.append("</sitemapindex>")
    return Response(
        "\n".join(xml),
        mimetype="application/xml"
    )