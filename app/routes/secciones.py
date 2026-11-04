from flask import Blueprint, render_template, url_for
from app.extensions import db
from datetime import datetime
from app.models.comercial import COMERCIAL
from app.seo.menu_secciones import MENU_SECCIONES
from app.models.menu_competiciones import (SeccionConfig,CompeticionConfig,)
from app.models.menu_competiciones import SeccionConfig
from app.seo.schema import schema_breadcrumb_equipo,jsonld, schema_sports_team
from ..models.resumenes import ResumenJornada
from app.utils.resumen_temporada import (obtener_ultimo_partido, obtener_proximo_partido,)
from app.routes.valladolid_route import (obtener_datos_valladolid,generar_clasificacion_analisis_futbol_valladolid)
from app.routes.uemc_route import (obtener_datos_uemc,
    generar_clasificacion_analisis_baloncesto_uemc)
from app.routes.ponce_route import (obtener_datos_ponce,
    generar_clasificacion_analisis_baloncesto_ponce)
from app.routes.aliados_route import (obtener_datos_aliados,
    generar_clasificacion_analisis_baloncesto_aliados)
from app.routes.aula_route import (obtener_datos_aula,
    generar_clasificacion_analisis_balonmano_aula)
from app.routes.tordesillas_route import (obtener_datos_tordesillas,
    generar_clasificacion_analisis_futbol_tordesillas)
from app.routes.recoletas_route import (obtener_datos_recoletas,
    generar_clasificacion_analisis_balonmano_recoletas)
from app.routes.promesas_route import (obtener_datos_promesas,
    generar_clasificacion_analisis_futbol_promesas)
from app.routes.vallad_genius_route import (obtener_datos_vallad_genius,
    generar_clasificacion_analisis_futbol_vallad_genius)
from app.routes.rv_fem_route import (obtener_datos_rv_fem,
    generar_clasificacion_analisis_futbol_rv_fem)
from app.routes.parquesol_route import (obtener_datos_parquesol,
    generar_clasificacion_analisis_futbol_parquesol)
from app.routes.galvan_route import (obtener_datos_galvan,
    generar_clasificacion_analisis_futsal_galvan)
from app.routes.vall_sala_route import (obtener_datos_vall_sala,
    generar_clasificacion_analisis_futsal_vall_sala)
from app.routes.caja_route import (obtener_datos_caja,
    generar_clasificacion_analisis_hockey_caja)
from app.routes.panteras_route import (obtener_datos_panteras,
    generar_clasificacion_analisis_hockey_panteras)
from app.routes.vrac_route import (obtener_datos_vrac,
    generar_clasificacion_analisis_rugby_vrac, aplicar_h2h_en_empates)
from app.routes.salvador_route import (obtener_datos_salvador,
    generar_clasificacion_analisis_rugby_salvador, aplicar_h2h_en_empates)
from app.routes.salvador_fem_route import (obtener_datos_salvador_fem,
    generar_clasificacion_analisis_rugby_salvador_fem, aplicar_h2h_en_empates)
from app.routes.vcv_route import (obtener_datos_vcv,
    generar_clasificacion_analisis_voley_vcv)
from app.routes.vacceas_route import (obtener_datos_vacceas,
    generar_clasificacion_analisis_voley_vacceas)
from app.routes.valcyl_route import (obtener_datos_valcyl,
    generar_clasificacion_analisis_voley_valcyl)
from app.routes.san_jose_route import (obtener_datos_san_jose,
    generar_clasificacion_analisis_voley_san_jose)
from ..models.valladolid import ValladolidClub, CopaValladolid, PlayoffValladolid
from ..models.uemc import UEMCClub, CopaUEMC, PlayoffUEMC
from ..models.ponce import PonceClub, PlayoffPonce
from ..models.aliados import AliadosClub, PlayoffAliados, CopaAliados, SupercopaAliados, EurocupAliados
from ..models.aula import AulaClub, PlayoffAula, CopaAula
from ..models.recoletas import RecoletasClub, PlayoffRecoletas, CopaRecoletas, CopaReyRecoletas
from ..models.tordesillas import TordesillasClub, CopaTordesillas, PlayoffTordesillas
from ..models.promesas import PromesasClub, PlayoffPromesas
from ..models.vallad_genius import ValladGeniusClub
from ..models.rv_fem import SimancasClub, CopaSimancas, PlayoffSimancas
from ..models.parquesol import ParquesolClub, CopaParquesol, PlayoffParquesol
from ..models.galvan import GalvanClub, CopaGalvan, PlayoffGalvan
from ..models.vall_sala import VallSalaClub, CopaVallSala, PlayoffVallSala
from ..models.caja import CajaClub, PlayoffCaja, CopaCaja, SupercopaCaja, EuropaCaja
from ..models.panteras import PanterasClub, PlayoffPanteras, CopaPanteras, SupercopaPanteras, EuropaPanteras
from ..models.vrac import VracClub, PlayoffVrac, CopaVrac, SupercopaIbericaVrac, EuropaVrac, TemporadaVrac, JornadaVrac
from ..models.salvador import SalvadorClub, PlayoffSalvador, CopaSalvador, SupercopaIbericaSalvador, EuropaSalvador, TemporadaSalvador, JornadaSalvador
from ..models.salvador_fem import SalvadorFemClub, PlayoffSalvadorFem, CopaSalvadorFem, SupercopaIbericaSalvadorFem, EuropaSalvadorFem, TemporadaSalvadorFem, JornadaSalvadorFem
from ..models.vcv import VCVClub, PlayoffVCV, CopaVCV, EuropaVCV
from ..models.vacceas import VacceasClub, PlayoffVacceas, CopaVacceas, EuropaVacceas
from ..models.valcyl import ValcylClub, PlayoffValcyl, CopaValcyl, EuropaValcyl
from ..models.san_jose import JoseClub, PlayoffJose, CopaJose, EuropaJose

secciones_bp = Blueprint("secciones", __name__)

def obtener_menu_seccion(nombre):
    seccion = SeccionConfig.query.filter_by(nombre=nombre).first()

    if not seccion:
        return MENU_SECCIONES.get(nombre, {})

    menu = {}

    for competicion in seccion.competiciones:
        menu[competicion.nombre] = competicion.activa

    return menu

def render_seccion(
    template,
    nombre,
    zona="seccion",
    breadcrumb=None,
    schema_team=None,
    **contexto
):

    comercial = COMERCIAL.get(nombre, {})

    seccion = SeccionConfig.query.filter_by(nombre=nombre).first()

    menu = {}

    if seccion:
        for competicion in seccion.competiciones:
            menu[competicion.nombre] = competicion.activa

    return render_template(
        template,
        comercial=comercial,
        menu=menu,
        zona=zona,
        breadcrumb=breadcrumb,
        schema_team=schema_team,
        **contexto
    )

# Rutas de los equipos
#SECCIÓN CBC VALLADOLID
@secciones_bp.route("/seccion/uemc")
def seccion_uemc():

    # Obtener los datos de la temporada activa
    data = obtener_datos_uemc()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_baloncesto_uemc(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_uemc = UEMCClub.query.all()

    for club in clubs_uemc:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del CBC Valladolid
    datos_uemc = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "CBC Valladolid"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "CBC Valladolid"
        ),
        "--"
    )

    # Competiciones del CBC Valladolid
    competiciones_uemc = [
        {
            "nombre": "2ª FEB - A",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Copa de España",
            "tipo": "eliminatoria",
            "partidos": CopaUEMC.query.all(),
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffUEMC.query.all(),
        },
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "CBC Valladolid",
        competiciones_uemc
    )

    # Próximo partido pendiente
    proximo_partido = obtener_proximo_partido(
        "CBC Valladolid",
        competiciones_uemc
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "CBC Valladolid",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#baloncesto"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/uemc.html",
        "uemc",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_uemc.get("puntos", 0),
        partidos_jugados=datos_uemc.get("jugados", 0),
        victorias=datos_uemc.get("ganados", 0),
        empates=datos_uemc.get("empatados", 0),
        derrotas=datos_uemc.get("perdidos", 0),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=proximo_partido["visitante"] if proximo_partido else "--",
        proximo_jornada=proximo_partido["jornada"] if proximo_partido else "--",
        proximo_fecha=proximo_partido["fecha"].strftime("%d/%m/%y") if proximo_partido else "--",
        proximo_hora=proximo_partido["hora"] if proximo_partido else "--",

        # Último resultado
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Datos SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("uemc")),
        schema_team=jsonld(schema_sports_team(
            "uemc",
            "https://deportesdelaciudad.es/seccion/uemc"
        ))
    )
# SECCION PUCELA BASKET
@secciones_bp.route("/seccion/ponce")
def seccion_ponce():

    # Obtener los datos de la temporada activa
    data = obtener_datos_ponce()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_baloncesto_ponce(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_ponce = PonceClub.query.all()

    for club in clubs_ponce:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del Pucela Basket
    datos_ponce = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Pucela Basket"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Pucela Basket"
        ),
        "--"
    )

    # Competiciones de Pucela Basket
    competiciones_ponce = [
        {
            "nombre": "1ª Nacional - A1",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Copa",
            "tipo": "eliminatoria",
            "partidos": CopaUEMC.query.all(),
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffUEMC.query.all(),
        },
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "Pucela Basket",
        competiciones_ponce
    )

    # Próximo partido pendiente
    proximo_partido = obtener_proximo_partido(
        "Pucela Basket",
        competiciones_ponce
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Pucela Basket",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#baloncesto"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/ponce.html",
        "ponce",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_ponce.get("puntos", 0),
        partidos_jugados=datos_ponce.get("jugados", 0),
        victorias=datos_ponce.get("ganados", 0),
        empates=datos_ponce.get("empatados", 0),
        derrotas=datos_ponce.get("perdidos", 0),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=proximo_partido["visitante"] if proximo_partido else "--",
        proximo_jornada=proximo_partido["jornada"] if proximo_partido else "--",
        proximo_fecha=proximo_partido["fecha"].strftime("%d/%m/%y") if proximo_partido else "--",
        proximo_hora=proximo_partido["hora"] if proximo_partido else "--",

        # Último resultado
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Datos SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("ponce")),
        schema_team=jsonld(schema_sports_team(
            "ponce",
            "https://deportesdelaciudad.es/seccion/ponce"
        ))
    )
# SECCION UNIVERSIDAD VCV 
@secciones_bp.route("/seccion/vcv")
def seccion_vcv():
    # Obtener los datos de la temporada activa
    data = obtener_datos_vcv()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_voley_vcv(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_vcv = VCVClub.query.all()

    for club in clubs_vcv:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos de Universidad VCV
    datos_vcv = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Universidad VCV"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Universidad VCV"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones = [
        {
            "nombre": "SuperLiga 2-Grp A",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "copa",
            "partidos": CopaVCV.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "playoff",
            "partidos": PlayoffVCV.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "copa",
            "partidos": EuropaVCV.query.all()
        }
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "Universidad VCV",
        competiciones
    )

    # Próximo partido
    proximo_partido = obtener_proximo_partido(
        "Universidad VCV",
        competiciones
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Universidad VCV",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    # URL del último resumen
    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#voleibol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/vcv.html",
        "vcv",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_vcv.get("puntos", 0),
        partidos_jugados=datos_vcv.get("jugados", 0),
        victorias=(
            datos_vcv.get("ganados3", 0)
            + datos_vcv.get("ganados2", 0)
        ),
        derrotas=(
            datos_vcv.get("perdidos1", 0)
            + datos_vcv.get("perdidos0", 0)
        ),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else None,
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else None
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else None
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else None
        ),
        proximo_hora=proximo_partido["hora"] if proximo_partido else None,

        # Último resumen
        ultimo_resumen_titular=(
            ultimo_resumen.titular if ultimo_resumen else None
        ),
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("vcv")),
        schema_team=jsonld(schema_sports_team(
            "vcv",
            "https://deportesdelaciudad.es/seccion/vcv"
        ))
    )
# SECCION CD SAN JOSÉ
@secciones_bp.route("/seccion/san_jose")
def seccion_san_jose():
    # Obtener los datos de la temporada activa
    data = obtener_datos_san_jose()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_voley_san_jose(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_san_jose = JoseClub.query.all()

    for club in clubs_san_jose:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados3": 0,
                    "ganados2": 0,
                    "perdidos1": 0,
                    "perdidos0": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del CD San José
    datos_san_jose = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "CD San José"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "CD San José"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones = [
        {
            "nombre": "1° Div. Masc.-Grp A",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "copa",
            "partidos": CopaJose.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "playoff",
            "partidos": PlayoffJose.query.all()
        }
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "CD San José",
        competiciones
    )

    # Próximo partido
    proximo_partido = obtener_proximo_partido(
        "CD San José",
        competiciones
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "CD San José",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    # URL del último resumen
    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#voleibol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/san_jose.html",
        "san_jose",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_san_jose.get("puntos", 0),
        partidos_jugados=datos_san_jose.get("jugados", 0),
        victorias=(
            datos_san_jose.get("ganados3", 0)
            + datos_san_jose.get("ganados2", 0)
        ),
        derrotas=(
            datos_san_jose.get("perdidos0", 0)
            + datos_san_jose.get("perdidos1", 0)
        ),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else None,
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else None
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else None
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else None
        ),
        proximo_hora=proximo_partido["hora"] if proximo_partido else None,

        # Último resumen
        ultimo_resumen_titular=(
            ultimo_resumen.titular if ultimo_resumen else None
        ),
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("san_jose")),
        schema_team=jsonld(schema_sports_team(
            "san_jose",
            "https://deportesdelaciudad.es/seccion/san_jose"
        ))
    )
# SECCION BSR VALLADOLID
@secciones_bp.route("/seccion/aliados")
def seccion_aliados():
    # Obtener los datos de la temporada activa
    data = obtener_datos_aliados()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_baloncesto_aliados(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_aliados = AliadosClub.query.all()

    for club in clubs_aliados:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del BSR Valladolid
    datos_aliados = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "BSR Valladolid"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "BSR Valladolid"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones_aliados = [
        {
            "nombre": "Superliga BSR",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa de España",
            "tipo": "eliminatoria",
            "partidos": CopaAliados.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffAliados.query.all()
        },
        {
            "nombre": "SuperCopa",
            "tipo": "eliminatoria",
            "partidos": SupercopaAliados.query.all()
        },
        {
            "nombre": "Eurocup",
            "tipo": "liga",
            "partidos": EurocupAliados.query.all()
        },
    ]

    # Último resultado y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "BSR Valladolid",
        competiciones_aliados
    )

    proximo_partido = obtener_proximo_partido(
        "BSR Valladolid",
        competiciones_aliados
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "BSR Valladolid",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#baloncesto"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/aliados.html",
        "aliados",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_aliados.get("puntos", 0),
        partidos_jugados=datos_aliados.get("jugados", 0),
        victorias=datos_aliados.get("ganados", 0),
        empates=datos_aliados.get("empatados", 0),
        derrotas=datos_aliados.get("perdidos", 0),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("aliados")),
        schema_team=jsonld(schema_sports_team(
            "aliados",
            "https://deportesdelaciudad.es/seccion/aliados"
        ))
    )
# SECCION AULA
@secciones_bp.route("/seccion/aula")
def seccion_aula():
    # Obtener los datos de la temporada activa
    data = obtener_datos_aula()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_balonmano_aula(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_aula = AulaClub.query.all()

    for club in clubs_aula:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del Aula Valladolid
    datos_aula = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Aula Valladolid"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Aula Valladolid"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones_aula = [
        {
            "nombre": "Div. Honor Oro",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa de la Reina",
            "tipo": "eliminatoria",
            "partidos": CopaAula.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffAula.query.all()
        },
    ]

    # Último resultado y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "Aula Valladolid",
        competiciones_aula
    )

    proximo_partido = obtener_proximo_partido(
        "Aula Valladolid",
        competiciones_aula
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Aula Valladolid",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#balonmano"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/aula.html",
        "aula",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_aula.get("puntos", 0),
        partidos_jugados=datos_aula.get("jugados", 0),
        victorias=datos_aula.get("ganados", 0),
        empates=datos_aula.get("empatados", 0),
        derrotas=datos_aula.get("perdidos", 0),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("aula")),
        schema_team=jsonld(schema_sports_team(
            "aula",
            "https://deportesdelaciudad.es/seccion/aula"
        ))
    )
# SECCION ATL. VALLADOLID
@secciones_bp.route("/seccion/recoletas")
def seccion_recoletas():
    # Obtener los datos de la temporada activa
    data = obtener_datos_recoletas()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_balonmano_recoletas(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_recoletas = RecoletasClub.query.all()

    for club in clubs_recoletas:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del Atlético Valladolid
    datos_recoletas = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Atl. Valladolid"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Atl. Valladolid"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones_recoletas = [
        {
            "nombre": "Liga Asobal",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaReyRecoletas.query.all()
        },
        {
            "nombre": "Copa de España",
            "tipo": "eliminatoria",
            "partidos": CopaRecoletas.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffRecoletas.query.all()
        },
    ]

    # Último resultado y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "Atl. Valladolid",
        competiciones_recoletas
    )

    proximo_partido = obtener_proximo_partido(
        "Atl. Valladolid",
        competiciones_recoletas
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Atlético Valladolid",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#balonmano"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/recoletas.html",
        "recoletas",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_recoletas.get("puntos", 0),
        partidos_jugados=datos_recoletas.get("jugados", 0),
        victorias=datos_recoletas.get("ganados", 0),
        empates=datos_recoletas.get("empatados", 0),
        derrotas=datos_recoletas.get("perdidos", 0),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("recoletas")),
        schema_team=jsonld(schema_sports_team(
            "recoletas",
            "https://deportesdelaciudad.es/seccion/recoletas"
        ))
    )
#SECCION REAL VALLADOLID
@secciones_bp.route("/seccion/valladolid")
def seccion_valladolid():
    # Obtener los datos de la temporada activa
    data = obtener_datos_valladolid()

    # ÚLTIMO RESUMEN PUBLICADO

    ultimo_resumen = (
        ResumenJornada.query.filter(
            ResumenJornada.equipo.in_([
                "Real Valladolid",
                "R.Valladolid"
            ]),
            ResumenJornada.publicado.is_(True)
        )
        .order_by(
            db.func.coalesce(
                ResumenJornada.fecha_inicio,
                ResumenJornada.fecha
            ).desc(),
            ResumenJornada.id.desc()
        )
        .first()
    )

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol"
        if ultimo_resumen else None
    )

    # CLASIFICACIÓN

    clasificacion = generar_clasificacion_analisis_futbol_valladolid(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_valladolid = ValladolidClub.query.all()

    for club in clubs_valladolid:
        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion
        ):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Datos del Real Valladolid
    datos_valladolid = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "R.Valladolid"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "R.Valladolid"
        ),
        "--"
    )

    # COMPETICIONES DEL REAL VALLADOLID

    competiciones_valladolid = [
        {
            "nombre": "Liga Hypermotion",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaValladolid.query.all(),
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffValladolid.query.all(),
        },
    ]

    # ÚLTIMO PARTIDO

    ultimo_partido = obtener_ultimo_partido(
        ["R.Valladolid", "Real Valladolid"],
        competiciones_valladolid
    )

    # PRÓXIMO PARTIDO

    proximo_partido = obtener_proximo_partido(
        ["R.Valladolid", "Real Valladolid"],
        competiciones_valladolid
    )

    proximo_local = (
        proximo_partido["local"]
        if proximo_partido else None
    )

    proximo_visitante = (
        proximo_partido["visitante"]
        if proximo_partido else None
    )

    proximo_jornada = (
        proximo_partido["jornada"]
        if proximo_partido else None
    )

    proximo_fecha = (
        proximo_partido["fecha"].strftime("%d/%m/%y")
        if proximo_partido else None
    )

    proximo_hora = (
        proximo_partido["hora"]
        if proximo_partido else None
    )

    # RENDERIZAR SECCIÓN

    return render_seccion(
        "secciones/valladolid.html",
        "valladolid",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_valladolid.get("puntos", 0),
        partidos_jugados=datos_valladolid.get("jugados", 0),
        victorias=datos_valladolid.get("ganados", 0),
        empates=datos_valladolid.get("empatados", 0),
        derrotas=datos_valladolid.get("perdidos", 0),
        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,
        # Próximo partido
        proximo_local=proximo_local,
        proximo_visitante=proximo_visitante,
        proximo_jornada=proximo_jornada,
        proximo_fecha=proximo_fecha,
        proximo_hora=proximo_hora,
        # Último partido
        ultimo_competicion=(
            ultimo_partido["competicion"]
            if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"]
            if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"]
            if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"]
            if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"]
            if ultimo_partido else "--"
        ),

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
# SECCION ATL. TORDESILLAS
@secciones_bp.route("/seccion/tordesillas")
def seccion_tordesillas():

    # Obtener los datos de la temporada activa
    data = obtener_datos_tordesillas()

    # ==========================================
    # ÚLTIMO RESUMEN PUBLICADO
    # ==========================================

    ultimo_resumen = (
        ResumenJornada.query.filter(
            ResumenJornada.equipo.in_([
                "Atl.Tordesillas",
                "Atlético Tordesillas"
            ]),
            ResumenJornada.publicado.is_(True)
        )
        .order_by(
            db.func.coalesce(
                ResumenJornada.fecha_inicio,
                ResumenJornada.fecha
            ).desc(),
            ResumenJornada.id.desc()
        )
        .first()
    )

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol"
        if ultimo_resumen else None
    )

    # ==========================================
    # CLASIFICACIÓN
    # ==========================================

    clasificacion = generar_clasificacion_analisis_futbol_tordesillas(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_tordesillas = TordesillasClub.query.all()

    for club in clubs_tordesillas:
        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion
        ):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Datos del Atlético Tordesillas
    datos_tordesillas = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Atl.Tordesillas"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Atl.Tordesillas"
        ),
        "--"
    )

    # ==========================================
    # COMPETICIONES DEL ATLÉTICO TORDESILLAS
    # ==========================================

    competiciones_tordesillas = [
        {
            "nombre": "2ª RFEF-Grp 5",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaTordesillas.query.all(),
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffTordesillas.query.all(),
        },
    ]

    # ==========================================
    # ÚLTIMO PARTIDO
    # ==========================================

    ultimo_partido = obtener_ultimo_partido(
        "Atl.Tordesillas",
        competiciones_tordesillas
    )

    # ==========================================
    # PRÓXIMO PARTIDO
    # ==========================================

    proximo_partido = obtener_proximo_partido(
        "Atl.Tordesillas",
        competiciones_tordesillas
    )

    proximo_local = (
        proximo_partido["local"]
        if proximo_partido else None
    )

    proximo_visitante = (
        proximo_partido["visitante"]
        if proximo_partido else None
    )

    proximo_jornada = (
        proximo_partido["jornada"]
        if proximo_partido else None
    )

    proximo_fecha = (
        proximo_partido["fecha"].strftime("%d/%m/%y")
        if proximo_partido else None
    )

    proximo_hora = (
        proximo_partido["hora"]
        if proximo_partido else None
    )

    # ==========================================
    # RENDERIZAR SECCIÓN
    # ==========================================

    return render_seccion(
        "secciones/tordesillas.html",
        "tordesillas",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_tordesillas.get("puntos", 0),
        partidos_jugados=datos_tordesillas.get("jugados", 0),
        victorias=datos_tordesillas.get("ganados", 0),
        empates=datos_tordesillas.get("empatados", 0),
        derrotas=datos_tordesillas.get("perdidos", 0),

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Próximo partido
        proximo_local=proximo_local,
        proximo_visitante=proximo_visitante,
        proximo_jornada=proximo_jornada,
        proximo_fecha=proximo_fecha,
        proximo_hora=proximo_hora,

        # Último partido
        ultimo_competicion=(
            ultimo_partido["competicion"]
            if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"]
            if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"]
            if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"]
            if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"]
            if ultimo_partido else "--"
        ),
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "tordesillas",
                "https://deportesdelaciudad.es/seccion/tordesillas"
            )
        )
    )
# SECCION VALLADOLIDI
@secciones_bp.route("/seccion/vallad_genius")
def seccion_vallad_genius():

    # Obtener los datos de la temporada activa
    data = obtener_datos_vallad_genius()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futbol_vallad_genius(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_vallad_genius = ValladGeniusClub.query.all()

    for club in clubs_vallad_genius:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del Real ValladoliDi
    datos_vallad_genius = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "R.ValladoliDi"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "R.ValladoliDi"
        ),
        "--"
    )

    # Competición del Real ValladoliDi
    competiciones_vallad_genius = [
        {
            "nombre": "Liga Genius",
            "tipo": "liga",
            "partidos": data,
        },
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "R.ValladoliDi",
        competiciones_vallad_genius
    )

    # Próximo partido pendiente
    proximo_partido = obtener_proximo_partido(
        "R.ValladoliDi",
        competiciones_vallad_genius
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "R.ValladoliDi",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/vallad_genius.html",
        "valladoliDi",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_vallad_genius.get("puntos", 0),
        partidos_jugados=datos_vallad_genius.get("jugados", 0),
        victorias=datos_vallad_genius.get("ganados", 0),
        empates=datos_vallad_genius.get("empatados", 0),
        derrotas=datos_vallad_genius.get("perdidos", 0),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=proximo_partido["visitante"] if proximo_partido else "--",
        proximo_jornada=proximo_partido["jornada"] if proximo_partido else "--",
        proximo_fecha=proximo_partido["fecha"].strftime("%d/%m/%y") if proximo_partido else "--",
        proximo_hora=proximo_partido["hora"] if proximo_partido else "--",

        # Último resultado
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Datos SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("valladoliDi")),
        schema_team=jsonld(schema_sports_team(
            "valladoliDi",
            "https://deportesdelaciudad.es/seccion/vallad_genius"
        ))
    )
# SECCION RV PROMESAS
@secciones_bp.route("/seccion/promesas")
def seccion_promesas():

    # Obtener los datos de la temporada activa
    data = obtener_datos_promesas()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futbol_promesas(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_promesas = PromesasClub.query.all()

    for club in clubs_promesas:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del RV Promesas
    datos_promesas = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "RV Promesas"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "RV Promesas"
        ),
        "--"
    )

    # Competiciones del RV Promesas
    competiciones_promesas = [
        {
            "nombre": "2ª RFEF-Grp 5",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffPromesas.query.all(),
        },
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "RV Promesas",
        competiciones_promesas
    )

    # Próximo partido pendiente
    proximo_partido = obtener_proximo_partido(
        "RV Promesas",
        competiciones_promesas
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "RV Promesas",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/promesas.html",
        "promesas",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_promesas.get("puntos", 0),
        partidos_jugados=datos_promesas.get("jugados", 0),
        victorias=datos_promesas.get("ganados", 0),
        empates=datos_promesas.get("empatados", 0),
        derrotas=datos_promesas.get("perdidos", 0),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=proximo_partido["visitante"] if proximo_partido else "--",
        proximo_jornada=proximo_partido["jornada"] if proximo_partido else "--",
        proximo_fecha=proximo_partido["fecha"].strftime("%d/%m/%y") if proximo_partido else "--",
        proximo_hora=proximo_partido["hora"] if proximo_partido else "--",

        # Último resultado
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Datos SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("promesas")),
        schema_team=jsonld(schema_sports_team(
            "promesas",
            "https://deportesdelaciudad.es/seccion/promesas"
        ))
    )
# SECCION CPLV CAJA RURAL
@secciones_bp.route("/seccion/caja")
def seccion_caja():
    # Obtener los datos de la temporada activa
    data = obtener_datos_caja()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_hockey_caja(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_caja = CajaClub.query.all()

    for club in clubs_caja:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del CPLV Caja Rural
    datos_caja = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "CPLV Caja Rural"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "CPLV Caja Rural"
        ),
        "--"
    )

    # Preparar las competiciones para los helpers comunes
    competiciones_caja = [
        {
            "nombre": "Liga Élite Masc.",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaCaja.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffCaja.query.all()
        },
        {
            "nombre": "Supercopa",
            "tipo": "eliminatoria",
            "partidos": SupercopaCaja.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "eliminatoria",
            "partidos": EuropaCaja.query.all()
        },
    ]

    # Obtener último partido y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "CPLV Caja Rural",
        competiciones_caja
    )

    proximo_partido = obtener_proximo_partido(
        "CPLV Caja Rural",
        competiciones_caja
    )

    # Obtener el último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "CPLV Caja Rural",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#hockey linea"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/caja.html",
        "caja",
        posicion_liga=posicion_liga,
        puntos_liga=datos_caja.get("puntos", 0),
        partidos_jugados=datos_caja.get("jugados", 0),
        victorias=datos_caja.get("ganados", 0),
        empates=datos_caja.get("empatados", 0),
        derrotas=datos_caja.get("perdidos", 0),

        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"] if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        proximo_local=(
            proximo_partido["local"] if proximo_partido else "--"
        ),
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        breadcrumb=jsonld(schema_breadcrumb_equipo("caja")),
        schema_team=jsonld(schema_sports_team(
            "caja",
            "https://deportesdelaciudad.es/seccion/caja"
        ))
    )
# SECCION CPLV PANTERAS
@secciones_bp.route("/seccion/panteras")
def seccion_panteras():
    # Obtener los datos de la temporada activa
    data = obtener_datos_panteras()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_hockey_panteras(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_panteras = PanterasClub.query.all()

    for club in clubs_panteras:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del CPLV Panteras
    datos_panteras = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "CPLV Panteras C.R"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "CPLV Panteras C.R"
        ),
        "--"
    )

    # Preparar las competiciones para los helpers comunes
    competiciones_panteras = [
        {
            "nombre": "Élite Iberdrola",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaPanteras.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffPanteras.query.all()
        },
        {
            "nombre": "Supercopa",
            "tipo": "eliminatoria",
            "partidos": SupercopaPanteras.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "eliminatoria",
            "partidos": EuropaPanteras.query.all()
        },
    ]

    # Obtener último partido y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "CPLV Panteras C.R",
        competiciones_panteras
    )

    proximo_partido = obtener_proximo_partido(
        "CPLV Panteras C.R",
        competiciones_panteras
    )

    # Obtener el último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "CPLV Panteras",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#hockey linea"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/panteras.html",
        "panteras",
        posicion_liga=posicion_liga,
        puntos_liga=datos_panteras.get("puntos", 0),
        partidos_jugados=datos_panteras.get("jugados", 0),
        victorias=datos_panteras.get("ganados", 0),
        empates=datos_panteras.get("empatados", 0),
        derrotas=datos_panteras.get("perdidos", 0),

        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"] if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        proximo_local=(
            proximo_partido["local"] if proximo_partido else "--"
        ),
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        breadcrumb=jsonld(schema_breadcrumb_equipo("panteras")),
        schema_team=jsonld(schema_sports_team(
            "panteras",
            "https://deportesdelaciudad.es/seccion/panteras"
        ))
    )
# SECCIION VRAC
@secciones_bp.route("/seccion/vrac")
def seccion_vrac():
    # Obtener los datos de la temporada activa
    data = obtener_datos_vrac()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_rugby_vrac(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_vrac = VracClub.query.all()

    for club in clubs_vrac:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del VRAC
    datos_vrac = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "VRAC"
        ),
        {}
    )

    # Obtener la fase regular de la temporada activa
    temporada = TemporadaVrac.query.filter_by(activa=True).first()

    fase_regular = []

    if temporada:
        fase_regular = JornadaVrac.query.filter_by(
            temporada_id=temporada.id,
            fase="Regular"
        ).order_by(JornadaVrac.id).all()

    # Generar clasificación general de la fase regular
    clasificacion_posiciones = generar_clasificacion_analisis_rugby_vrac(
        fase_regular
    )

    # Incorporar clubes sin partidos
    clubs = VracClub.query.all()

    for club in clubs:
        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_posiciones
        ):
            clasificacion_posiciones.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                    "bonus": 0
                }
            })

    # Aplicar el orden de la clasificación oficial
    clasificacion_posiciones = sorted(
        clasificacion_posiciones,
        key=lambda x: (
            x["datos"]["puntos"],
            x["datos"]["diferencia_goles"],
            x["datos"]["favor"]
        ),
        reverse=True
    )

    clasificacion_posiciones = aplicar_h2h_en_empates(
        clasificacion_posiciones,
        fase_regular
    )

    # Obtener posición del VRAC
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion_posiciones)
            if equipo["equipo"] == "VRAC"
        ),
        "--"
    )

    # Preparar las competiciones para los helpers comunes
    competiciones_vrac = [
        {
            "nombre": "División de Honor",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaVrac.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffVrac.query.all()
        },
    ]

    # Obtener último partido y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "VRAC",
        competiciones_vrac
    )

    proximo_partido = obtener_proximo_partido(
        "VRAC",
        competiciones_vrac
    )

    # Obtener el último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "VRAC",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#rugby"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/vrac.html",
        "vrac",
        posicion_liga=posicion_liga,
        puntos_liga=datos_vrac.get("puntos", 0),
        partidos_jugados=datos_vrac.get("jugados", 0),
        victorias=datos_vrac.get("ganados", 0),
        empates=datos_vrac.get("empatados", 0),
        derrotas=datos_vrac.get("perdidos", 0),

        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"] if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        proximo_local=(
            proximo_partido["local"] if proximo_partido else "--"
        ),
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        breadcrumb=jsonld(schema_breadcrumb_equipo("vrac")),
        schema_team=jsonld(schema_sports_team(
            "vrac",
            "https://deportesdelaciudad.es/seccion/vrac"
        ))
    )
# SECCION VCV VACCEAS
@secciones_bp.route("/seccion/vacceas")
def seccion_vacceas():
    # Obtener los datos de la temporada activa
    data = obtener_datos_vacceas()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_voley_vacceas(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_vacceas = VacceasClub.query.all()

    for club in clubs_vacceas:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del VCV Vacceas
    datos_vacceas = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "VCV Vacceas"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "VCV Vacceas"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones = [
        {
            "nombre": "1° Div. Fem.-Grp D",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "copa",
            "partidos": CopaVacceas.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "playoff",
            "partidos": PlayoffVacceas.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "copa",
            "partidos": EuropaVacceas.query.all()
        }
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "VCV Vacceas",
        competiciones
    )

    # Próximo partido
    proximo_partido = obtener_proximo_partido(
        "VCV Vacceas",
        competiciones
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "VCV Vacceas",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    # URL del último resumen
    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#voleibol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/vacceas.html",
        "vacceas",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_vacceas.get("puntos", 0),
        partidos_jugados=datos_vacceas.get("jugados", 0),
        victorias=(
            datos_vacceas.get("ganados3", 0)
            + datos_vacceas.get("ganados2", 0)
        ),
        derrotas=(
            datos_vacceas.get("perdidos1", 0)
            + datos_vacceas.get("perdidos0", 0)
        ),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else None,
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else None
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else None
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else None
        ),
        proximo_hora=proximo_partido["hora"] if proximo_partido else None,

        # Último resumen
        ultimo_resumen_titular=(
            ultimo_resumen.titular if ultimo_resumen else None
        ),
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("vacceas")),
        schema_team=jsonld(schema_sports_team(
            "vacceas",
            "https://deportesdelaciudad.es/seccion/vacceas"
        ))
    )
# SECCION VALCYL VCV
@secciones_bp.route("/seccion/valcyl")
def seccion_valcyl():
    # Obtener los datos de la temporada activa
    data = obtener_datos_valcyl()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_voley_valcyl(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_valcyl = ValcylClub.query.all()

    for club in clubs_valcyl:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados3": 0,
                    "ganados2": 0,
                    "perdidos1": 0,
                    "perdidos0": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del Valcyl VCV
    datos_valcyl = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Valcyl VCV"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Valcyl VCV"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones = [
        {
            "nombre": "1° Div. Masc.-Grp A",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "copa",
            "partidos": CopaValcyl.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "playoff",
            "partidos": PlayoffValcyl.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "copa",
            "partidos": EuropaValcyl.query.all()
        }
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "Valcyl VCV",
        competiciones
    )

    # Próximo partido
    proximo_partido = obtener_proximo_partido(
        "Valcyl VCV",
        competiciones
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Valcyl VCV",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    # URL del último resumen
    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#voleibol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/valcyl.html",
        "valcyl",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_valcyl.get("puntos", 0),
        partidos_jugados=datos_valcyl.get("jugados", 0),
        victorias=(
            datos_valcyl.get("ganados3", 0)
            + datos_valcyl.get("ganados2", 0)
        ),
        derrotas=(
            datos_valcyl.get("perdidos1", 0)
            + datos_valcyl.get("perdidos0", 0)
        ),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else None,
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else None
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else None
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else None
        ),
        proximo_hora=proximo_partido["hora"] if proximo_partido else None,

        # Último resumen
        ultimo_resumen_titular=(
            ultimo_resumen.titular if ultimo_resumen else None
        ),
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("valcyl")),
        schema_team=jsonld(schema_sports_team(
            "valcyl",
            "https://deportesdelaciudad.es/seccion/valcyl"
        ))
    )
# SECCION SALVADOR
@secciones_bp.route("/seccion/salvador")
def seccion_salvador():
    # Obtener los datos de la temporada activa
    data = obtener_datos_salvador()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_rugby_salvador(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_salvador = SalvadorClub.query.all()

    for club in clubs_salvador:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos de CR El Salvador
    datos_salvador = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "CR El Salvador"
        ),
        {}
    )

    # Obtener la fase regular de la temporada activa
    temporada = TemporadaSalvador.query.filter_by(activa=True).first()

    fase_regular = []

    if temporada:
        fase_regular = JornadaSalvador.query.filter_by(
            temporada_id=temporada.id,
            fase="Regular"
        ).order_by(JornadaSalvador.id).all()

    # Generar clasificación general de la fase regular
    clasificacion_posiciones = generar_clasificacion_analisis_rugby_salvador(
        fase_regular
    )

    # Incorporar clubes sin partidos
    clubs = SalvadorClub.query.all()

    for club in clubs:
        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_posiciones
        ):
            clasificacion_posiciones.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                    "bonus": 0
                }
            })

    # Aplicar el orden de la clasificación oficial
    clasificacion_posiciones = sorted(
        clasificacion_posiciones,
        key=lambda x: (
            x["datos"]["puntos"],
            x["datos"]["diferencia_goles"],
            x["datos"]["favor"]
        ),
        reverse=True
    )

    clasificacion_posiciones = aplicar_h2h_en_empates(
        clasificacion_posiciones,
        fase_regular
    )

    # Obtener posición de CR El Salvador
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion_posiciones)
            if equipo["equipo"] == "CR El Salvador"
        ),
        "--"
    )

    # Preparar las competiciones para los helpers comunes
    competiciones_salvador = [
        {
            "nombre": "División de Honor",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaSalvador.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffSalvador.query.all()
        },
        {
            "nombre": "Supercopa Ibérica",
            "tipo": "eliminatoria",
            "partidos": SupercopaIbericaSalvador.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "eliminatoria",
            "partidos": EuropaSalvadorFem.query.all()
        },
    ]

    # Obtener último partido y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "CR El Salvador",
        competiciones_salvador
    )

    proximo_partido = obtener_proximo_partido(
        "CR El Salvador",
        competiciones_salvador
    )

    # Obtener el último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "CR El Salvador",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#rugby"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/salvador.html",
        "salvador",
        posicion_liga=posicion_liga,
        puntos_liga=datos_salvador.get("puntos", 0),
        partidos_jugados=datos_salvador.get("jugados", 0),
        victorias=datos_salvador.get("ganados", 0),
        empates=datos_salvador.get("empatados", 0),
        derrotas=datos_salvador.get("perdidos", 0),

        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"] if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        proximo_local=(
            proximo_partido["local"] if proximo_partido else "--"
        ),
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        breadcrumb=jsonld(schema_breadcrumb_equipo("salvador")),
        schema_team=jsonld(schema_sports_team(
            "salvador",
            "https://deportesdelaciudad.es/seccion/salvador"
        ))
    )
# SECCION SALVADOR FEMENINO
@secciones_bp.route("/seccion/salvador_fem")
def seccion_salvador_fem():
    # Obtener los datos de la temporada activa
    data = obtener_datos_salvador_fem()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_rugby_salvador_fem(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_salvador_fem = SalvadorFemClub.query.all()

    for club in clubs_salvador_fem:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos de El Salvador R.C.
    datos_salvador_fem = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "El Salvador R.C."
        ),
        {}
    )

    # Generar clasificación general
    clasificacion_posiciones = generar_clasificacion_analisis_rugby_salvador_fem(
        data
    )

    # Incorporar clubes sin partidos
    clubs = SalvadorFemClub.query.all()

    for club in clubs:
        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_posiciones
        ):
            clasificacion_posiciones.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                    "bonus": 0
                }
            })

    # Aplicar el orden de la clasificación oficial
    clasificacion_posiciones = sorted(
        clasificacion_posiciones,
        key=lambda x: (
            x["datos"]["puntos"],
            x["datos"]["diferencia_goles"],
            x["datos"]["favor"]
        ),
        reverse=True
    )

    # El desempate directo permanece desactivado, como en la ruta original

    # Obtener posición de El Salvador R.C.
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion_posiciones)
            if equipo["equipo"] == "El Salvador R.C."
        ),
        "--"
    )

    # Preparar las competiciones para los helpers comunes
    competiciones_salvador_fem = [
        {
            "nombre": "División de Honor",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaSalvadorFem.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffSalvadorFem.query.all()
        },
        {
            "nombre": "Supercopa Ibérica",
            "tipo": "eliminatoria",
            "partidos": SupercopaIbericaSalvadorFem.query.all()
        },
        {
            "nombre": "Europa",
            "tipo": "eliminatoria",
            "partidos": EuropaSalvadorFem.query.all()
        },
    ]

    # Obtener último partido y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "El Salvador R.C.",
        competiciones_salvador_fem
    )

    proximo_partido = obtener_proximo_partido(
        "El Salvador R.C.",
        competiciones_salvador_fem
    )

    # Obtener el último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "El Salvador R.C",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#rugby"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/salvador_fem.html",
        "salvador_fem",
        posicion_liga=posicion_liga,
        puntos_liga=datos_salvador_fem.get("puntos", 0),
        partidos_jugados=datos_salvador_fem.get("jugados", 0),
        victorias=datos_salvador_fem.get("ganados", 0),
        empates=datos_salvador_fem.get("empatados", 0),
        derrotas=datos_salvador_fem.get("perdidos", 0),

        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=(
            ultimo_partido["local"] if ultimo_partido else "--"
        ),
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        proximo_local=(
            proximo_partido["local"] if proximo_partido else "--"
        ),
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        breadcrumb=jsonld(schema_breadcrumb_equipo("salvador_fem")),
        schema_team=jsonld(schema_sports_team(
            "salvador_fem",
            "https://deportesdelaciudad.es/seccion/salvador_fem"
        ))
    )
# RV FEMENNO
@secciones_bp.route("/seccion/rv_femenino")
def seccion_rv_femenino():

    # Obtener los datos de la temporada activa
    data = obtener_datos_rv_fem()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futbol_rv_fem(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_rv_fem = SimancasClub.query.all()

    for club in clubs_rv_fem:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del RV Femenino
    datos_rv_fem = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "RV Femenino"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "RV Femenino"
        ),
        "--"
    )

    # Competiciones del RV Femenino
    competiciones_rv_fem = [
        {
            "nombre": "Liga Gonalpi",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffSimancas.query.all(),
        },
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "RV Femenino",
        competiciones_rv_fem
    )

    # Próximo partido pendiente
    proximo_partido = obtener_proximo_partido(
        "RV Femenino",
        competiciones_rv_fem
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "RV Femenino",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/rv_femenino.html",
        "rv_fem",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_rv_fem.get("puntos", 0),
        partidos_jugados=datos_rv_fem.get("jugados", 0),
        victorias=datos_rv_fem.get("ganados", 0),
        empates=datos_rv_fem.get("empatados", 0),
        derrotas=datos_rv_fem.get("perdidos", 0),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=proximo_partido["visitante"] if proximo_partido else "--",
        proximo_jornada=proximo_partido["jornada"] if proximo_partido else "--",
        proximo_fecha=proximo_partido["fecha"].strftime("%d/%m/%y") if proximo_partido else "--",
        proximo_hora=proximo_partido["hora"] if proximo_partido else "--",

        # Último resultado
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Datos SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(schema_sports_team(
            "rv_fem",
            "https://deportesdelaciudad.es/seccion/rv_femenino"
        ))
    )
# CD PARQUESOL
@secciones_bp.route("/seccion/parquesol")
def seccion_parquesol():

    # Obtener los datos de la temporada activa
    data = obtener_datos_parquesol()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futbol_parquesol(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_parquesol = ParquesolClub.query.all()

    for club in clubs_parquesol:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del CD Parquesol
    datos_parquesol = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "CD Parquesol"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "CD Parquesol"
        ),
        "--"
    )

    # Competiciones del CD Parquesol
    competiciones_parquesol = [
        {
            "nombre": "3ª Federación-Grp 8",
            "tipo": "liga",
            "partidos": data,
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffParquesol.query.all(),
        },
    ]

    # Último partido disputado
    ultimo_partido = obtener_ultimo_partido(
        "CD Parquesol",
        competiciones_parquesol
    )

    # Próximo partido pendiente
    proximo_partido = obtener_proximo_partido(
        "CD Parquesol",
        competiciones_parquesol
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "CD Parquesol",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/parquesol.html",
        "parquesol",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_parquesol.get("puntos", 0),
        partidos_jugados=datos_parquesol.get("jugados", 0),
        victorias=datos_parquesol.get("ganados", 0),
        empates=datos_parquesol.get("empatados", 0),
        derrotas=datos_parquesol.get("perdidos", 0),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=proximo_partido["visitante"] if proximo_partido else "--",
        proximo_jornada=proximo_partido["jornada"] if proximo_partido else "--",
        proximo_fecha=proximo_partido["fecha"].strftime("%d/%m/%y") if proximo_partido else "--",
        proximo_hora=proximo_partido["hora"] if proximo_partido else "--",

        # Último resultado
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # Datos SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("parquesol")),
        schema_team=jsonld(schema_sports_team(
            "parquesol",
            "https://deportesdelaciudad.es/seccion/parquesol"
        ))
    )
# SECCION GALVAN
@secciones_bp.route("/seccion/galvan")
def seccion_galvan():
    # Obtener los datos de la temporada activa
    data = obtener_datos_galvan()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futsal_galvan(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_galvan = GalvanClub.query.all()

    for club in clubs_galvan:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del VTG FS
    datos_galvan = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "VTG FS"
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "VTG FS"
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones_galvan = [
        {
            "nombre": "2ª División B-Grp 1",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaGalvan.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffGalvan.query.all()
        },
    ]

    # Último resultado y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "VTG FS",
        competiciones_galvan
    )

    proximo_partido = obtener_proximo_partido(
        "VTG FS",
        competiciones_galvan
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Valladolid Tierno Galván",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol-sala"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/galvan.html",
        "galvan",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_galvan.get("puntos", 0),
        partidos_jugados=datos_galvan.get("jugados", 0),
        victorias=datos_galvan.get("ganados", 0),
        empates=datos_galvan.get("empatados", 0),
        derrotas=datos_galvan.get("perdidos", 0),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("galvan")),
        schema_team=jsonld(schema_sports_team(
            "galvan",
            "https://deportesdelaciudad.es/seccion/galvan"
        ))
    )
# SECCION VALLADOLID S.S.
@secciones_bp.route("/seccion/vall_sala")
def seccion_vall_sala():
    # Obtener los datos de la temporada activa
    data = obtener_datos_vall_sala()

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futsal_vall_sala(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_vall_sala = VallSalaClub.query.all()

    for club in clubs_vall_sala:
        if not any(equipo["equipo"] == club.nombre for equipo in clasificacion):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": {
                    "puntos": 0,
                    "jugados": 0,
                    "ganados": 0,
                    "empatados": 0,
                    "perdidos": 0,
                    "favor": 0,
                    "contra": 0,
                    "diferencia_goles": 0,
                },
            })

    # Buscar los datos del Valladolid Sport Sala
    datos_vall_sala = next(
        (
            equipo["datos"]
            for equipo in clasificacion
            if equipo["equipo"] == "Valladolid S.S."
        ),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion)
            if equipo["equipo"] == "Valladolid S.S."
        ),
        "--"
    )

    # Preparar las competiciones
    competiciones_vall_sala = [
        {
            "nombre": "3ª División-Grp 9",
            "tipo": "liga",
            "partidos": data
        },
        {
            "nombre": "Copa del Rey",
            "tipo": "eliminatoria",
            "partidos": CopaVallSala.query.all()
        },
        {
            "nombre": "Playoff",
            "tipo": "eliminatoria",
            "partidos": PlayoffVallSala.query.all()
        },
    ]

    # Último resultado y próximo partido
    ultimo_partido = obtener_ultimo_partido(
        "Valladolid S.S.",
        competiciones_vall_sala
    )

    proximo_partido = obtener_proximo_partido(
        "Valladolid S.S.",
        competiciones_vall_sala
    )

    # Último resumen publicado
    ultimo_resumen = ResumenJornada.query.filter(
        ResumenJornada.equipo == "Valladolid Sport Sala",
        ResumenJornada.publicado.is_(True)
    ).order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        ResumenJornada.id.desc()
    ).first()

    ultimo_resumen_titular = (
        ultimo_resumen.titular if ultimo_resumen else None
    )

    ultimo_resumen_url = (
        url_for(
            "resumenes_route_bp.pagina_resumenes",
            fecha=(
                ultimo_resumen.fecha_inicio or ultimo_resumen.fecha
            ).isoformat()
        ) + "#futbol-sala"
        if ultimo_resumen else None
    )

    return render_seccion(
        "secciones/vall_sala.html",
        "vall_sala",

        # Clasificación
        posicion_liga=posicion_liga,
        puntos_liga=datos_vall_sala.get("puntos", 0),
        partidos_jugados=datos_vall_sala.get("jugados", 0),
        victorias=datos_vall_sala.get("ganados", 0),
        empates=datos_vall_sala.get("empatados", 0),
        derrotas=datos_vall_sala.get("perdidos", 0),

        # Último resultado
        ultimo_competicion=(
            ultimo_partido["competicion"] if ultimo_partido else "--"
        ),
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=(
            ultimo_partido["visitante"] if ultimo_partido else "--"
        ),
        ultimo_goles_local=(
            ultimo_partido["goles_local"] if ultimo_partido else "--"
        ),
        ultimo_goles_visitante=(
            ultimo_partido["goles_visitante"] if ultimo_partido else "--"
        ),

        # Próximo partido
        proximo_local=proximo_partido["local"] if proximo_partido else "--",
        proximo_visitante=(
            proximo_partido["visitante"] if proximo_partido else "--"
        ),
        proximo_jornada=(
            proximo_partido["jornada"] if proximo_partido else "--"
        ),
        proximo_fecha=(
            proximo_partido["fecha"].strftime("%d/%m/%y")
            if proximo_partido else "--"
        ),
        proximo_hora=(
            proximo_partido["hora"] if proximo_partido else "--"
        ),

        # Último resumen
        ultimo_resumen_titular=ultimo_resumen_titular,
        ultimo_resumen_url=ultimo_resumen_url,

        # SEO
        breadcrumb=jsonld(schema_breadcrumb_equipo("vall_sala")),
        schema_team=jsonld(schema_sports_team(
            "vall_sala",
            "https://deportesdelaciudad.es/seccion/vall_sala"
        ))
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