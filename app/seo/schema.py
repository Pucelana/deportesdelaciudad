import json

def schema_website():
    return {
        "@context": "https://schema.org",
        "@graph": [

            {
                "@type": "WebSite",
                "@id": "https://deportesdelaciudad.es/#website",
                "url": "https://deportesdelaciudad.es",
                "name": "Deportes de la Ciudad",
                "description": "Portal de información deportiva de Valladolid con resultados, clasificaciones, calendarios, copas, playoff y competiciones europeas.",
                "inLanguage": "es-ES"
            },

            {
                "@type": "SportsOrganization",
                "@id": "https://deportesdelaciudad.es/#organization",
                "name": "Deportes de la Ciudad",
                "url": "https://deportesdelaciudad.es",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://deportesdelaciudad.es/static/img/logo.webp"
                }
            }

        ]
    }

def schema_breadcrumb(items):

    lista = []

    for i, item in enumerate(items):

        lista.append({
            "@type": "ListItem",
            "position": i + 1,
            "name": item["name"],
            "item": item["url"]
        })

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": lista
    }

def jsonld(data):
    return json.dumps(data, ensure_ascii=False)