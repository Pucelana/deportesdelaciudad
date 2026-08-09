from datetime import datetime
from app.seo.social import SOCIAL
import json

BASE_URL = "https://deportesdelaciudad.es"

def schema_website():
    return {
        "@context": "https://schema.org",
        "@graph": [

            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}/#website",
                "url": BASE_URL,
                "name": "Deportes de la Ciudad",
                "description": "Portal de información deportiva de Valladolid con resultados, clasificaciones, calendarios, copas, playoff y competiciones europeas.",
                "inLanguage": "es-ES"
            },

            {
                "@type": "SportsOrganization",
                "@id": f"{BASE_URL}/#organization",
                "name": "Deportes de la Ciudad",
                "url": BASE_URL,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{BASE_URL}/static/img/logo.webp"
                },
                "sameAs": [
                    url for url in [
                        SOCIAL.get("facebook"),
                        SOCIAL.get("instagram"),
                        SOCIAL.get("whatsapp"),
                    ] if url
                ]
            }   
        ]
    }

def schema_breadcrumb(items):

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item["name"],
                "item": item["url"]
            }
            for i, item in enumerate(items)
        ]
    }
EQUIPOS = {

    "uemc": {
        "nombre": "CBC Valladolid",
        "deporte": "Baloncesto",
        "liga": "Segunda FEB",
        "logo": "https://deportesdelaciudad.es/static/img/cbc_sf.png",
    },

    "ponce": {
        "nombre": "Pucela Basket Ponce Valladolid CB",
        "deporte": "Baloncesto",
        "liga": "Primera Nacional",
        "logo": "https://deportesdelaciudad.es/static/img/ponce_sf.png",
    },

    "cdsi_vall": {
        "nombre": "CDSI Valladolid",
        "deporte": "Baloncesto",
        "liga": "Primera Nacional",
        "logo": "https://deportesdelaciudad.es/static/img/cdsi_vall_sf.png",
    },

    "aliados": {
        "nombre": "BSR Valladolid",
        "deporte": "Baloncesto en silla",
        "liga": "División de Honor",
        "logo": "https://deportesdelaciudad.es/static/img/aliados_sf.png",
    },

    "aula": {
        "nombre": "Aula Valladolid",
        "deporte": "Balonmano",
        "liga": "División de Oro",
        "logo": "https://deportesdelaciudad.es/static/img/aula_sf.png",
    },

    "recoletas": {
        "nombre": "Atl. Valladolid",
        "deporte": "Balonmano",
        "liga": "Liga ASOBAL",
        "logo": "https://deportesdelaciudad.es/static/img/reco_fs.png",
    },

    "valladolid": {
        "nombre": "Real Valladolid",
        "deporte": "Fútbol",
        "liga": "Segunda División",
        "logo": "https://deportesdelaciudad.es/static/img/pucela_sf.png",
    },

    "promesas": {
        "nombre": "RV Promesas",
        "deporte": "Fútbol",
        "liga": "Segunda Federación",
        "logo": "https://deportesdelaciudad.es/static/img/pucela_sf.png",
    },

    "rv_fem": {
        "nombre": "RV Femenino",
        "deporte": "Fútbol",
        "liga": "Liga Gonalpi",
        "logo": "https://deportesdelaciudad.es/static/img/pucela_sf.png",
    },

    "parquesol": {
        "nombre": "CD Parquesol",
        "deporte": "Fútbol",
        "liga": "Tercera Federación Femenina",
        "logo": "https://deportesdelaciudad.es/static/img/parquesol_sf1.png",
    },

    "vrac": {
        "nombre": "VRAC",
        "deporte": "Rugby",
        "liga": "División de Honor",
        "logo": "https://deportesdelaciudad.es/static/img/vrac_sf.png",
    },

    "salvador": {
        "nombre": "El Salvador",
        "deporte": "Rugby",
        "liga": "División de Honor",
        "logo": "https://deportesdelaciudad.es/static/img/salvador_sf.png",
    },

    "salvador_fem": {
        "nombre": "El Salvador Femenino",
        "deporte": "Rugby",
        "liga": "Liga Iberdrola",
        "logo": "https://deportesdelaciudad.es/static/img/salvador_sf.png",
    },

    "caja": {
        "nombre": "CPLV Caja Rural",
        "deporte": "Hockey Línea",
        "liga": "Liga Élite",
        "logo": "https://deportesdelaciudad.es/static/img/cplv_sf.png",
    },

    "panteras": {
        "nombre": "Panteras Caja Rural",
        "deporte": "Hockey Línea",
        "liga": "Liga Élite Iberdrola",
        "logo": "https://deportesdelaciudad.es/static/img/cplv_sf.png",
    },

    "galvan": {
        "nombre": "Tierno Galván",
        "deporte": "Fútbol Sala",
        "liga": "Segunda División B",
        "logo": "https://deportesdelaciudad.es/static/img/galvan_sf.png",
    },

    "vall_sala": {
        "nombre": "FS Valladolid",
        "deporte": "Fútbol Sala",
        "liga": "Primera Regional",
        "logo": "https://deportesdelaciudad.es/static/img/vall_sala_sf.png",
    },

    "vcv": {
        "nombre": "Universidad VCV",
        "deporte": "Voleibol",
        "liga": "Superliga 2",
        "logo": "https://deportesdelaciudad.es/static/img/valla_voley_sf.png",
    },

    "san_jose": {
        "nombre": "CD San José",
        "deporte": "Voleibol",
        "liga": "Primera Nacional",
        "logo": "https://deportesdelaciudad.es/static/img/san_jose_sf.png",
    },

}   

COMPETICIONES = {

    "uemc": {
        "nombre": "Segunda FEB",
        "deporte": "Basketball",
    },

    "ponce": {
        "nombre": "Primera División Nacional Femenina",
        "deporte": "Basketball",
    },

    "cdsi_vall": {
        "nombre": "Primera División Nacional Femenina",
        "deporte": "Basketball",
    },

    "aliados": {
        "nombre": "Superliga BSR",
        "deporte": "Wheelchair Basketball",
    },

    "aula": {
        "nombre": "División Honor Oro",
        "deporte": "Handball",
    },

    "recoletas": {
        "nombre": "Liga ASOBAL",
        "deporte": "Handball",
    },

    "valladolid": {
        "nombre": "Liga Hypermotion",
        "deporte": "Soccer",
    },

    "promesas": {
        "nombre": "Segunda Federación",
        "deporte": "Soccer",
    },

    "rv_fem": {
        "nombre": "Liga Gonalpi",
        "deporte": "Soccer",
    },

    "parquesol": {
        "nombre": "Tercera Federación Femenina",
        "deporte": "Soccer",
    },

    "vrac": {
        "nombre": "División de Honor",
        "deporte": "Rugby",
    },

    "salvador": {
        "nombre": "División de Honor",
        "deporte": "Rugby",
    },

    "salvador_fem": {
        "nombre": "División de Honor",
        "deporte": "Rugby",
    },

    "caja": {
        "nombre": "Liga Élite",
        "deporte": "Inline Hockey",
    },

    "panteras": {
        "nombre": "Liga Élite Iberdrola",
        "deporte": "Inline Hockey",
    },

    "galvan": {
        "nombre": "Segunda División B",
        "deporte": "Futsal",
    },

    "vall_sala": {
        "nombre": "Primera Regional",
        "deporte": "Futsal",
    },

    "vcv": {
        "nombre": "Superliga 2",
        "deporte": "Volleyball",
    },

    "san_jose": {
        "nombre": "Primera Nacional",
        "deporte": "Volleyball",
    },

} 
   
DEPORTES = {
    "uemc": "Baloncesto",
    "ponce": "Baloncesto",
    "cdsi_vall": "Baloncesto",
    "aliados": "Baloncesto en silla",
    "aula": "Balonmano",
    "recoletas": "Balonmano",
    "valladolid": "Fútbol",
    "promesas": "Fútbol",
    "parquesol": "Fútbol",
    "rv_fem": "Fútbol",
    "vrac": "Rugby",
    "salvador": "Rugby",
    "salvador_fem": "Rugby",
    "caja": "Hockey Línea",
    "panteras": "Hockey Línea",
    "galvan": "Fútbol Sala",
    "vall_sala": "Fútbol Sala",
    "vcv": "Voleibol",
    "san_jose": "Voleibol",
}   
    
def schema_breadcrumb_equipo(slug):

    equipo = EQUIPOS[slug]

    return schema_breadcrumb([
        {
            "name": "Inicio",
            "url": BASE_URL
        },
        {
            "name": equipo["deporte"],
            "url": f"{BASE_URL}/seccion/{slug}"
        },
        {
            "name": equipo["nombre"],
            "url": f"{BASE_URL}/seccion/{slug}"
        }
    ]) 
    
def schema_sports_team(slug, url):

    equipo = EQUIPOS[slug]

    return {
        "@context": "https://schema.org",
        "@type": "SportsTeam",
        "@id": f"{url}#team",

        "name": equipo["nombre"],

        "sport": equipo["deporte"],

        "url": url,

        "logo": {
            "@type": "ImageObject",
            "url": equipo["logo"]
        },

        "memberOf": {
            "@type": "SportsOrganization",
            "name": equipo["liga"]
        }
    }      

def schema_sports_competition(slug, url):

    competicion = COMPETICIONES[slug]

    return {
        "@context": "https://schema.org",
        "@type": "SportsCompetition",
        "name": competicion["nombre"],
        "sport": competicion["deporte"],
        "url": url,
        "organizer": {
            "@type": "SportsOrganization",
            "name": "Deportes de la Ciudad",
            "url": BASE_URL
        }
    }

def schema_sports_event(
    nombre,
    deporte,
    local,
    visitante,
    fecha_iso,
    url,
    competicion,
    resultado_local=None,
    resultado_visitante=None,
    estado="https://schema.org/EventScheduled",
):

    evento = {
        "@type": "SportsEvent",
        "name": nombre,
        "sport": deporte,
        "startDate": fecha_iso,
        "url": url,
        "eventStatus": estado,
        "competitor": [
            {
                "@type": "SportsTeam",
                "name": local,
            },
            {
                "@type": "SportsTeam",
                "name": visitante,
            },
        ],
        "location": {
            "@type": "Place",
            "name": local
        },
        "superEvent": {
            "@type": "SportsCompetition",
            "name": competicion
        }
    }

    if (
        resultado_local not in (None, "", " ")
        and resultado_visitante not in (None, "", " ")
    ):

        evento["homeTeam"] = {
            "@type": "SportsTeam",
            "name": local
        }

        evento["awayTeam"] = {
            "@type": "SportsTeam",
            "name": visitante
        }

        evento["homeScore"] = resultado_local
        evento["awayScore"] = resultado_visitante
        evento["eventStatus"] = "https://schema.org/EventCompleted"

    return evento

def schema_eventos(eventos):

    return {
        "@context": "https://schema.org",
        "@graph": eventos
    }

def schema_partidos(partidos, slug, url_base):

    competicion = COMPETICIONES[slug]
    deporte = DEPORTES[slug]

    eventos = []

    for partido in partidos:

        if not partido.local or not partido.visitante:
            continue

        nombre = f"{partido.local} vs {partido.visitante}"

        fecha_iso = None

        if partido.fecha:

            try:

                if partido.hora not in (None, "", " "):

                    from datetime import datetime

                    fecha_iso = datetime.strptime(
                        f"{partido.fecha} {partido.hora}",
                        "%d/%m/%Y %H:%M"
                    ).isoformat()

                else:

                    from datetime import datetime

                    fecha_iso = datetime.strptime(
                        partido.fecha,
                        "%d/%m/%Y"
                    ).date().isoformat()

            except Exception:

                fecha_iso = None

        eventos.append(

            schema_sports_event(

                nombre=nombre,

                deporte=deporte,

                local=partido.local,

                visitante=partido.visitante,

                fecha_iso=fecha_iso,

                url=url_base,

                competicion=competicion["nombre"],

                resultado_local=partido.resultadoA,

                resultado_visitante=partido.resultadoB,

            )

        )

    return schema_eventos(eventos)

def obtener_partidos_schema(datos):

    partidos = []

    if isinstance(datos, dict):

        for lista in datos.values():
            partidos.extend(lista)

    else:

        for jornada in datos:

            if isinstance(jornada, dict):
                partidos.extend(jornada.get("partidos", []))

            elif isinstance(jornada, list):
                partidos.extend(jornada)

    return partidos

def jsonld(data):
    return json.dumps(data, ensure_ascii=False)