from flask import Blueprint, render_template
from app.models.comercial import COMERCIAL
from app.seo.schema import schema_breadcrumb_equipo,jsonld, schema_sports_team

secciones_bp = Blueprint("secciones", __name__)

def render_seccion(template, nombre, zona="seccion", breadcrumb=None, schema_team=None):
    comercial = COMERCIAL.get(nombre, {})

    return render_template(
        template,
        comercial=comercial,
        zona=zona,
        breadcrumb=breadcrumb,
        schema_team=schema_team
    )

# Rutas de los equipos
@secciones_bp.route("/seccion/uemc")
def seccion_uemc():
    return render_seccion(
        "secciones/uemc.html",
        "uemc",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("uemc")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "uemc",
                "https://deportesdelaciudad.es/seccion/uemc"
            )
        )
    )

@secciones_bp.route("/seccion/ponce")
def seccion_ponce():
    return render_seccion(
        "secciones/ponce.html", 
        "ponce",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("ponce")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "ponce",
                "https://deportesdelaciudad.es/seccion/ponce"
            )
        )
    )

@secciones_bp.route("/seccion/cdsi_vall")
def seccion_cdsi_vall():
    return render_seccion(
        "secciones/cdsi_vall.html", 
        "vall_sala",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("cdsi_vall")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "cdsi_vall",
                "https://deportesdelaciudad.es/seccion/cdsi_vall"
            )
        )
    )

@secciones_bp.route("/seccion/vcv")
def seccion_vcv():
    return render_seccion(
        "secciones/vcv.html", 
        "vcv",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("vcv")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "vcv",
                "https://deportesdelaciudad.es/seccion/vcv"
            )
        )
    )

@secciones_bp.route("/seccion/san_jose")
def seccion_san_jose():
    return render_seccion(
        "secciones/san_jose.html", 
        "san_jose",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("san_jose")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "san_jose",
                "https://deportesdelaciudad.es/seccion/san_jose"
            )
        )
    )

@secciones_bp.route("/seccion/aliados")
def seccion_aliados():
    return render_seccion(
        "secciones/aliados.html", 
        "aliados",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("aliados")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "aliados",
                "https://deportesdelaciudad.es/seccion/aliados"
            )
        )
    )

@secciones_bp.route("/seccion/aula")
def seccion_aula():
    return render_seccion(
        "secciones/aula.html",
        "aula",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("aula")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "aula",
                "https://deportesdelaciudad.es/seccion/aula"
            )
        )
    )

@secciones_bp.route("/seccion/recoletas")
def seccion_recoletas():
    return render_seccion(
        "secciones/recoletas.html", 
        "recoletas",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("recoletas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "recoletas",
                "https://deportesdelaciudad.es/seccion/recoletas"
            )
        )
    )

@secciones_bp.route("/seccion/valladolid")
def seccion_valladolid():
    return render_seccion(
        "secciones/valladolid.html", 
        "valladolid",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("valladolid")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "valladolid",
                "https://deportesdelaciudad.es/seccion/valladolid"
            )
        )
    )

@secciones_bp.route("/seccion/promesas")
def seccion_promesas():
    return render_seccion(
        "secciones/promesas.html", 
        "promesas",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("promesas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "promesas",
                "https://deportesdelaciudad.es/seccion/promesas"
            )
        )
    )

@secciones_bp.route("/seccion/caja")
def seccion_caja():
    return render_seccion(
        "secciones/caja.html", 
        "caja",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("caja")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "caja",
                "https://deportesdelaciudad.es/seccion/caja"
            )
        )
    )

@secciones_bp.route("/seccion/panteras")
def seccion_panteras():
    return render_seccion(
        "secciones/panteras.html", 
        "panteras",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("panteras")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "panteras",
                "https://deportesdelaciudad.es/seccion/panteras"
            )
        )
    )

@secciones_bp.route("/seccion/vrac")
def seccion_vrac():
    return render_seccion(
        "secciones/vrac.html", 
        "vrac",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("vrac")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "vrac",
                "https://deportesdelaciudad.es/seccion/vrac"
            )
        )
    )

@secciones_bp.route("/seccion/salvador")
def seccion_salvador():
    return render_seccion(
        "secciones/salvador.html", 
        "salvador",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("salvador")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "salvador",
                "https://deportesdelaciudad.es/seccion/salvador"
            )
        )
    )

@secciones_bp.route("/seccion/salvador_fem")
def seccion_salvador_fem():
    return render_seccion(
        "secciones/salvador_fem.html", 
        "salvador_fem",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("salvador_fem")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "salvador_fem",
                "https://deportesdelaciudad.es/seccion/salvador_fem"
            )
        )
    )

@secciones_bp.route("/seccion/rv_femenino")
def seccion_rv_femenino():
    return render_seccion(
        "secciones/rv_femenino.html", 
        "rv_fem",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("rv_fem")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "rv_fem",
                "https://deportesdelaciudad.es/seccion/rv_femenino"
            )
        )
    )

@secciones_bp.route("/seccion/parquesol")
def seccion_parquesol():
    return render_seccion(
        "secciones/parquesol.html", 
        "parquesol",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("parquesol")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "parquesol",
                "https://deportesdelaciudad.es/seccion/parquesol"
            )
        )
    )

@secciones_bp.route("/seccion/galvan")
def seccion_galvan():
    return render_seccion(
        "secciones/galvan.html", 
        "galvan",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("galvan")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "galvan",
                "https://deportesdelaciudad.es/seccion/galvan"
            )
        )
    )

@secciones_bp.route("/seccion/vall_sala")
def seccion_vall_sala():
    return render_seccion(
        "secciones/vall_sala.html", 
        "vall_sala",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("vall_sala")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "vall_sala",
                "https://deportesdelaciudad.es/seccion/vall_sala"
            )
        )
    )

# Rutas de sistemas de ligas
@secciones_bp.route("/sistema_ligas/futbol")
def sistema_ligas_futbol():
    return render_template("sistema_ligas/sistema_futbol.html")

@secciones_bp.route("/sistema_ligas/baloncesto")
def sistema_ligas_baloncesto():
    return render_template("sistema_ligas/sistema_baloncesto.html")

@secciones_bp.route("/sistema_ligas/balonmano")
def sistema_ligas_balonmano():
    return render_template("sistema_ligas/sistema_balonmano.html")

@secciones_bp.route("/sistema_ligas/rugby")
def sistema_ligas_rugby():
    return render_template("sistema_ligas/sistema_rugby.html")

@secciones_bp.route("/sistema_ligas/hockey")
def sistema_ligas_hockey():
    return render_template("sistema_ligas/sistema_hockey.html")

@secciones_bp.route("/sistema_ligas/futbol_sala")
def sistema_ligas_futbol_sala():
    return render_template("sistema_ligas/sistema_futbol_sala.html")

@secciones_bp.route("/sistema_ligas/voleibol")
def sistema_ligas_voleibol():
    return render_template("sistema_ligas/sistema_voleibol.html")