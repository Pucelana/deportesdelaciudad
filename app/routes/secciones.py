from flask import Blueprint, render_template
from app.extensions import db
from datetime import datetime
from app.models.comercial import COMERCIAL
from app.seo.menu_secciones import MENU_SECCIONES
from app.models.menu_competiciones import (SeccionConfig,CompeticionConfig,)
from app.models.menu_competiciones import SeccionConfig
from app.seo.schema import schema_breadcrumb_equipo,jsonld, schema_sports_team
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
            (equipo["datos"] for equipo in clasificacion
             if equipo["equipo"] == "CBC Valladolid"),
            {}
        )
    
        # Posición en la clasificación
        posicion_liga = next(
            (i + 1 for i, equipo in enumerate(clasificacion)
             if equipo["equipo"] == "CBC Valladolid"),
            "--"
        )
        # Buscar el último partido disputado por el CBC Valladolid
        ultimo_partido = None
    
        for jornada in data:
            for partido in jornada["partidos"]:
    
                if "CBC Valladolid" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                ultimo_partido = {
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
            }
            partidos_ultimo_resultado = []
    
            # 1. Partidos de Liga
            for jornada in data:
                for partido in jornada["partidos"]:
                    if "CBC Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
    
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "2ª FEB - A"
                  })
    
            # 2. Partidos de Copa
            for partido in CopaUEMC.query.all():
                if "CBC Valladolid" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Copa de España"
                })
    
            # 3. Partidos de Playoff
            for partido in PlayoffUEMC.query.all():
                if "CBC Valladolid" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Playoff"
                })
            # 4. Seleccionar el partido más reciente
            ultimo_partido = (
                max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
                if partidos_ultimo_resultado else None
            )    
    
        return render_seccion(
            "secciones/uemc.html",
            "uemc",
            posicion_liga=posicion_liga,
            puntos_liga=datos_uemc.get("puntos", 0),
            partidos_jugados=datos_uemc.get("jugados", 0),
            victorias=datos_uemc.get("ganados", 0),
            empates=datos_uemc.get("empatados", 0),
            derrotas=datos_uemc.get("perdidos", 0),
            ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
            ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
            ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
            ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
            ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
            breadcrumb=jsonld(schema_breadcrumb_equipo("uemc")),
            schema_team=jsonld(schema_sports_team(
                "uemc",
                "https://deportesdelaciudad.es/seccion/uemc"
            ))
        )
# SECCION PYCELA BASKET
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
                (equipo["datos"] for equipo in clasificacion
                 if equipo["equipo"] == "Pucela Basket"),
                {}
            )
        
            # Posición en la clasificación
            posicion_liga = next(
                (i + 1 for i, equipo in enumerate(clasificacion)
                 if equipo["equipo"] == "Pucela Basket"),
                "--"
            )
            # Buscar el último partido disputado por el Pucela Basket
            ultimo_partido = None
        
            for jornada in data:
                for partido in jornada["partidos"]:
        
                    if "Pucela Basket" not in (partido.local, partido.visitante):
                        continue
        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
        
                    try:
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
        
                    ultimo_partido = {
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                }
                partidos_ultimo_resultado = []
        
                # 1. Partidos de Liga
                for jornada in data:
                    for partido in jornada["partidos"]:
                        if "Pucela Basket" not in (partido.local, partido.visitante):
                            continue
        
                        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                            continue
        
                        try:
                            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                            goles_local = int(partido.resultadoA)
                            goles_visitante = int(partido.resultadoB)
                        except (ValueError, TypeError):
                            continue
        
                        partidos_ultimo_resultado.append({
                            "fecha": fecha_partido,
                            "local": partido.local,
                            "visitante": partido.visitante,
                            "goles_local": goles_local,
                            "goles_visitante": goles_visitante,
                            "competicion": "1ª Nacional - A1"
                      })
        
                # 2. Partidos de Copa
                for partido in CopaUEMC.query.all():
                    if "Pucela Basket" not in (partido.local, partido.visitante):
                        continue
        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
        
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
        
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": ""
                    })
        
                # 3. Partidos de Playoff
                for partido in PlayoffUEMC.query.all():
                    if "Pucela Basket" not in (partido.local, partido.visitante):
                        continue
        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
        
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Playoff"
                    })
                # 4. Seleccionar el partido más reciente
                ultimo_partido = (
                    max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
                    if partidos_ultimo_resultado else None
                )    
        
            return render_seccion(
                "secciones/ponce.html",
                "ponce",
                posicion_liga=posicion_liga,
                puntos_liga=datos_ponce.get("puntos", 0),
                partidos_jugados=datos_ponce.get("jugados", 0),
                victorias=datos_ponce.get("ganados", 0),
                empates=datos_ponce.get("empatados", 0),
                derrotas=datos_ponce.get("perdidos", 0),
                ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
                ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
                ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
                ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
                ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del Universidad VCV
    datos_vcv = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "Universidad VCV"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "Universidad VCV"),
        "--"
    )
    # Buscar el último partido disputado por el Universidad VCV
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "Universidad VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "Universidad VCV" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "SuperLiga 2-Grp A"
              })
    
        # 2. Partidos de Copa
        for partido in CopaVCV.query.all():
            if "Universidad VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffVCV.query.all():
            if "Universidad VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 3. Partidos de Europa
        for partido in EuropaVCV.query.all():
            if "Universidad VCV" not in (partido.local, partido.visitante):
                continue
        
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
        
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })    
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/vcv.html",
        "vcv",
        posicion_liga=posicion_liga,
        puntos_liga=datos_vcv.get("puntos", 0),
        partidos_jugados=datos_vcv.get("jugados", 0),
        victorias=datos_vcv.get("ganados3", 0)+ datos_vcv.get("ganados2", 0),
        derrotas=datos_vcv.get("perdidos1", 0)+ datos_vcv.get("perdidos0", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del San José
    datos_san_jose = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "CD San José"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "CD San José"),
        "--"
    )
    # Buscar el último partido disputado por el San José
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "CD San José" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "CD San José" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "1° Div. Masc.-Grp A"
              })
    
        # 2. Partidos de Copa
        for partido in CopaJose.query.all():
            if "CD San José" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffJose.query.all():
            if "CD San José" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })   
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/san_jose.html",
        "san_jose",
        posicion_liga=posicion_liga,
        puntos_liga=datos_san_jose.get("puntos", 0),
        partidos_jugados=datos_san_jose.get("jugados", 0),
        victorias=datos_san_jose.get("ganados3", 0)+ datos_san_jose.get("ganados2", 0),
        derrotas=datos_san_jose.get("perdidos0", 0)+ datos_san_jose.get("perdidos1", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
                (equipo["datos"] for equipo in clasificacion
                 if equipo["equipo"] == "BSR Valladolid"),
                {}
            )
        
            # Posición en la clasificación
            posicion_liga = next(
                (i + 1 for i, equipo in enumerate(clasificacion)
                 if equipo["equipo"] == "BSR Valladolid"),
                "--"
            )
            # Buscar el último partido disputado por el BSR Valladolid
            ultimo_partido = None
        
            for jornada in data:
                for partido in jornada["partidos"]:
        
                    if "BSR Valladolid" not in (partido.local, partido.visitante):
                        continue
        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
        
                    try:
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
        
                    ultimo_partido = {
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                }
                partidos_ultimo_resultado = []
        
                # 1. Partidos de Liga
                for jornada in data:
                    for partido in jornada["partidos"]:
                        if "BSR Valladolid" not in (partido.local, partido.visitante):
                            continue
        
                        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                            continue
        
                        try:
                            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                            goles_local = int(partido.resultadoA)
                            goles_visitante = int(partido.resultadoB)
                        except (ValueError, TypeError):
                            continue
        
                        partidos_ultimo_resultado.append({
                            "fecha": fecha_partido,
                            "local": partido.local,
                            "visitante": partido.visitante,
                            "goles_local": goles_local,
                            "goles_visitante": goles_visitante,
                            "competicion": "Superliga BSR"
                        })
        
                # 2. Partidos de Copa
                for partido in CopaAliados.query.all():
                    if "BSR Valladolid" not in (partido.local, partido.visitante):
                        continue
        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
        
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
        
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Copa de España"
                    })
        
                # 3. Partidos de Playoff
                for partido in PlayoffAliados.query.all():
                    if "BSR Valladolid" not in (partido.local, partido.visitante):
                        continue
        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
        
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Playoff"
                    })
                # 4. Partidos de Supercopa
                for partido in PlayoffAliados.query.all():
                    if "BSR Valladolid" not in (partido.local, partido.visitante):
                        continue
                            
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
                            
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "SuperCopa"
                    })
                # 5. Partidos de Eurocup
                for partido in PlayoffAliados.query.all():
                    if "BSR Valladolid" not in (partido.local, partido.visitante):
                        continue
                        
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
                        
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Eurocup"
                    })    
                # 4. Seleccionar el partido más reciente
                ultimo_partido = (
                    max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
                    if partidos_ultimo_resultado else None
                )    
        
            return render_seccion(
                "secciones/aliados.html",
                "aliados",
                posicion_liga=posicion_liga,
                puntos_liga=datos_aliados.get("puntos", 0),
                partidos_jugados=datos_aliados.get("jugados", 0),
                victorias=datos_aliados.get("ganados", 0),
                empates=datos_aliados.get("empatados", 0),
                derrotas=datos_aliados.get("perdidos", 0),
                ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
                ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
                ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
                ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
                ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
            # Buscar los datos del AULA Valladolid
            datos_aula = next(
                (equipo["datos"] for equipo in clasificacion
                 if equipo["equipo"] == "Aula Valladolid"),
                {}
            )
    
            # Posición en la clasificación
            posicion_liga = next(
                (i + 1 for i, equipo in enumerate(clasificacion)
                 if equipo["equipo"] == "Aula Valladolid"),
                "--"
            )
            # Buscar el último partido disputado por el AULA Valladolid
            ultimo_partido = None
    
            for jornada in data:
                for partido in jornada["partidos"]:
    
                    if "Aula Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
    
                    try:
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    ultimo_partido = {
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                }
                partidos_ultimo_resultado = []
    
                # 1. Partidos de Liga
                for jornada in data:
                    for partido in jornada["partidos"]:
                        if "Aula Valladolid" not in (partido.local, partido.visitante):
                            continue
    
                        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                            continue
    
                        try:
                            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                            goles_local = int(partido.resultadoA)
                            goles_visitante = int(partido.resultadoB)
                        except (ValueError, TypeError):
                            continue
    
                        partidos_ultimo_resultado.append({
                            "fecha": fecha_partido,
                            "local": partido.local,
                            "visitante": partido.visitante,
                            "goles_local": goles_local,
                            "goles_visitante": goles_visitante,
                            "competicion": "Div. Honor Oro"
                        })
    
                # 2. Partidos de Copa
                for partido in CopaAula.query.all():
                    if "Aula Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
    
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Copa de la Reina"
                    })
    
                # 3. Partidos de Playoff
                for partido in PlayoffAula.query.all():
                    if "Aula Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Playoff"
                    })
                  
                # 4. Seleccionar el partido más reciente
                ultimo_partido = (
                    max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
                    if partidos_ultimo_resultado else None
                )    
    
            return render_seccion(
                "secciones/aula.html",
                "aula",
                posicion_liga=posicion_liga,
                puntos_liga=datos_aula.get("puntos", 0),
                partidos_jugados=datos_aula.get("jugados", 0),
                victorias=datos_aula.get("ganados", 0),
                empates=datos_aula.get("empatados", 0),
                derrotas=datos_aula.get("perdidos", 0),
                ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
                ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
                ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
                ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
                ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
            # Buscar los datos del Atl. Valladolid
            datos_recoletas = next(
                (equipo["datos"] for equipo in clasificacion
                 if equipo["equipo"] == "Atl. Valladolid"),
                {}
            )
    
            # Posición en la clasificación
            posicion_liga = next(
                (i + 1 for i, equipo in enumerate(clasificacion)
                 if equipo["equipo"] == "Atl. Valladolid"),
                "--"
            )
            # Buscar el último partido disputado por el Atl. Valladolid
            ultimo_partido = None
    
            for jornada in data:
                for partido in jornada["partidos"]:
    
                    if "Atl. Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
    
                    try:
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    ultimo_partido = {
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                }
                partidos_ultimo_resultado = []
    
                # 1. Partidos de Liga
                for jornada in data:
                    for partido in jornada["partidos"]:
                        if "Atl. Valladolid" not in (partido.local, partido.visitante):
                            continue
    
                        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                            continue
    
                        try:
                            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                            goles_local = int(partido.resultadoA)
                            goles_visitante = int(partido.resultadoB)
                        except (ValueError, TypeError):
                            continue
    
                        partidos_ultimo_resultado.append({
                            "fecha": fecha_partido,
                            "local": partido.local,
                            "visitante": partido.visitante,
                            "goles_local": goles_local,
                            "goles_visitante": goles_visitante,
                            "competicion": "Liga Asobal"
                        })
    
                # 2. Partidos de Copa
                for partido in CopaReyRecoletas.query.all():
                    if "Atl. Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
    
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Copa del Rey"
                    })
                # 2. Partidos de Copa
                for partido in CopaRecoletas.query.all():
                    if "Atl. Valladolid" not in (partido.local, partido.visitante):
                        continue
                    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
                    
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Copa de España"
                    })    
    
                # 3. Partidos de Playoff
                for partido in PlayoffRecoletas.query.all():
                    if "Atl. Valladolid" not in (partido.local, partido.visitante):
                        continue
    
                    if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                        continue
                    try:
                        fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                        goles_local = int(partido.resultadoA)
                        goles_visitante = int(partido.resultadoB)
                    except (ValueError, TypeError):
                        continue
    
                    partidos_ultimo_resultado.append({
                        "fecha": fecha_partido,
                        "local": partido.local,
                        "visitante": partido.visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante,
                        "competicion": "Playoff"
                    })
    
                # 4. Seleccionar el partido más reciente
                ultimo_partido = (
                    max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
                    if partidos_ultimo_resultado else None
                )    
    
            return render_seccion(
                "secciones/recoletas.html",
                "recoletas",
                posicion_liga=posicion_liga,
                puntos_liga=datos_recoletas.get("puntos", 0),
                partidos_jugados=datos_recoletas.get("jugados", 0),
                victorias=datos_recoletas.get("ganados", 0),
                empates=datos_recoletas.get("empatados", 0),
                derrotas=datos_recoletas.get("perdidos", 0),
                ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
                ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
                ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
                ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
                ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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

    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futbol_valladolid(data)

    # Incorporar los clubes que todavía no tienen partidos
    clubs_valladolid = ValladolidClub.query.all()

    for club in clubs_valladolid:
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

    # Buscar los datos del Real Valladolid
    datos_valladolid = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "R.Valladolid"),
        {}
    )

    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "R.Valladolid"),
        "--"
    )
    # Buscar el último partido disputado por el Real Valladolid
    ultimo_partido = None

    for jornada in data:
        for partido in jornada["partidos"]:

            if "R.Valladolid" not in (partido.local, partido.visitante):
                continue

            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue

            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue

            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []

        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "R.Valladolid" not in (partido.local, partido.visitante):
                    continue

                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue

                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue

                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Liga Hypermotion"
              })

        # 2. Partidos de Copa
        for partido in CopaValladolid.query.all():
            if "Real Valladolid" not in (partido.local, partido.visitante):
                continue

            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue

            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue

            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })

        # 3. Partidos de Playoff
        for partido in PlayoffValladolid.query.all():
            if "Real Valladolid" not in (partido.local, partido.visitante):
                continue

            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue

            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    

    return render_seccion(
        "secciones/valladolid.html",
        "valladolid",
        posicion_liga=posicion_liga,
        puntos_liga=datos_valladolid.get("puntos", 0),
        partidos_jugados=datos_valladolid.get("jugados", 0),
        victorias=datos_valladolid.get("ganados", 0),
        empates=datos_valladolid.get("empatados", 0),
        derrotas=datos_valladolid.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
        breadcrumb=jsonld(schema_breadcrumb_equipo("valladolid")),
        schema_team=jsonld(schema_sports_team(
            "valladolid",
            "https://deportesdelaciudad.es/seccion/valladolid"
        ))
    )
# SECCION ATL. TORDESILLAS
@secciones_bp.route("/seccion/tordesillas")
def seccion_tordesillas():
    # Obtener los datos de la temporada activa
    data = obtener_datos_tordesillas()
    
    # Generar la clasificación
    clasificacion = generar_clasificacion_analisis_futbol_tordesillas(data)
    
    # Incorporar los clubes que todavía no tienen partidos
    clubs_tordesillas = TordesillasClub.query.all()
    
    for club in clubs_tordesillas:
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
    
    # Buscar los datos del Real Valladolid
    datos_tordesillas = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "Atl.Tordesillas"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "Atl.Tordesillas"),
        "--"
    )
    # Buscar el último partido disputado por el Atl. Tordesillas
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "Atl.Tordesillas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "Atl.Tordesillas" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "2ª RFEF-Grp 5"
              })
    
        # 2. Partidos de Copa
        for partido in CopaTordesillas.query.all():
            if "Atl.Tordesillas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffTordesillas.query.all():
            if "Atl.Tordesillas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/tordesillas.html",
        "tordesillas",
        posicion_liga=posicion_liga,
        puntos_liga=datos_tordesillas.get("puntos", 0),
        partidos_jugados=datos_tordesillas.get("jugados", 0),
        victorias=datos_tordesillas.get("ganados", 0),
        empates=datos_tordesillas.get("empatados", 0),
        derrotas=datos_tordesillas.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
        breadcrumb=jsonld(schema_breadcrumb_equipo("tordesillas")),
        schema_team=jsonld(schema_sports_team(
            "tordesillas",
            "https://deportesdelaciudad.es/seccion/tordesillas"
        ))
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
    
    # Buscar los datos del RV Promesas
    datos_vallad_genius = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "R.ValladoliDi"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "R.ValladoliDi"),
        "--"
    )
    # Buscar el último partido disputado por el Real ValladoliDi
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "R.ValladoliDi" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "R.ValladoliDi" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Liga Genius"
              })
    
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/vallad_genius.html",
        "valladoliDi",
        posicion_liga=posicion_liga,
        puntos_liga=datos_vallad_genius.get("puntos", 0),
        partidos_jugados=datos_vallad_genius.get("jugados", 0),
        victorias=datos_vallad_genius.get("ganados", 0),
        empates=datos_vallad_genius.get("empatados", 0),
        derrotas=datos_vallad_genius.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "RV Promesas"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "RV Promesas"),
        "--"
    )
    # Buscar el último partido disputado por el RV Promesas
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "RV Promesas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "RV Promesas" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "2ª RFEF-Grp 5"
              })
    
        # 3. Partidos de Playoff
        for partido in PlayoffPromesas.query.all():
            if "RV Promesas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/promesas.html",
        "promesas",
        posicion_liga=posicion_liga,
        puntos_liga=datos_promesas.get("puntos", 0),
        partidos_jugados=datos_promesas.get("jugados", 0),
        victorias=datos_promesas.get("ganados", 0),
        empates=datos_promesas.get("empatados", 0),
        derrotas=datos_promesas.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del CPLV CAJA RURAL
    datos_caja = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "CPLV Caja Rural"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "CPLV Caja Rural"),
        "--"
    )
    # Buscar el último partido disputado por el CPLV CAJA RURAL
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "CPLV Caja Rural" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "CPLV Caja Rural" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Liga Élite Masc."
              })
    
        # 2. Partidos de Copa
        for partido in CopaCaja.query.all():
            if "CPLV Caja Rural" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffCaja.query.all():
            if "CPLV Caja Rural" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Partidos de Supercopa
        for partido in PlayoffCaja.query.all():
            if "CPLV Caja Rural" not in (partido.local, partido.visitante):
                continue
        
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
        
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Supercopa"
            })
        # 5. Partidos de Europa
        for partido in PlayoffCaja.query.all():
            if "CPLV Caja Rural" not in (partido.local, partido.visitante):
                continue
        
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
        
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })        
        # 6. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
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
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del CPLV PANTERAS
    datos_panteras = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "CPLV Panteras C.R"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "CPLV Panteras C.R"),
        "--"
    )
    # Buscar el último partido disputado por el CPLV PANTERAS
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "CPLV Panteras C.R" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "CPLV Panteras C.R" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Élite Iberdrola"
              })
    
        # 2. Partidos de Copa
        for partido in CopaPanteras.query.all():
            if "CPLV Panteras C.R" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffPanteras.query.all():
            if "CPLV Panteras C.R" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Partidos de Supercopa
        for partido in SupercopaPanteras.query.all():
            if "CPLV Panteras C.R" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Supercopa"
            })
        # 5. Partidos de Europa
        for partido in EuropaPanteras.query.all():
            if "CPLV Panteras C.R" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })        
        # 6. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
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
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "VRAC"),
        {}
    )
    
    # Obtener la fase regular de la temporada activa
    temporada = TemporadaVrac.query.filter_by(activa=True).first()

    fase_regular = JornadaVrac.query.filter_by(
        temporada_id=temporada.id,
        fase="Regular"
    ).order_by(JornadaVrac.id).all()

    # Generar clasificación general igual que en la página oficial
    clasificacion_posiciones = generar_clasificacion_analisis_rugby_vrac(
        fase_regular
    )

    # Incorporar clubes sin partidos
    clubs = VracClub.query.all()

    for club in clubs:
        if not any(e["equipo"] == club.nombre for e in clasificacion_posiciones):
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

    # Aplicar el mismo orden que la clasificación oficial
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
    # Buscar el último partido disputado por el VRAC
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "VRAC" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "VRAC" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "División de Honor"
              })
    
        # 2. Partidos de Copa
        for partido in CopaVrac.query.all():
            if "VRAC" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffVrac.query.all():
            if "VRAC" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Partidos de Supercopa
        for partido in PlayoffCaja.query.all():
            if "VRAC" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "SupercopaIberica"
            })
        # 5. Partidos de Europa
        for partido in PlayoffVrac.query.all():
            if "VRAC" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })        
        # 6. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
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
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "VCV Vacceas"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "VCV Vacceas"),
        "--"
    )
    # Buscar el último partido disputado por el VCV Vacceas
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "VCV Vacceas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "VCV Vacceas" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "1° Div. Fem.-Grp D"
              })
    
        # 2. Partidos de Copa
        for partido in CopaVacceas.query.all():
            if "VCV Vacceas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffVacceas.query.all():
            if "VCV Vacceas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 3. Partidos de Europa
        for partido in EuropaVacceas.query.all():
            if "VCV Vacceas" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })    
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/vacceas.html",
        "vacceas",
        posicion_liga=posicion_liga,
        puntos_liga=datos_vacceas.get("puntos", 0),
        partidos_jugados=datos_vacceas.get("jugados", 0),
        victorias=datos_vacceas.get("ganados3", 0)+ datos_vacceas.get("ganados2", 0),
        derrotas=datos_vacceas.get("perdidos1", 0)+ datos_vacceas.get("perdidos0", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "Valcyl VCV"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "Valcyl VCV"),
        "--"
    )
    # Buscar el último partido disputado por el Valcyl VCV
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "Valcyl VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "Valcyl VCV" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "1° Div. Masc.-Grp A"
              })
    
        # 2. Partidos de Copa
        for partido in CopaValcyl.query.all():
            if "Valcyl VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffValcyl.query.all():
            if "Valcyl VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 3. Partidos de Europa
        for partido in EuropaValcyl.query.all():
            if "Valcyl VCV" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })    
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/valcyl.html",
        "valcyl",
        posicion_liga=posicion_liga,
        puntos_liga=datos_valcyl.get("puntos", 0),
        partidos_jugados=datos_valcyl.get("jugados", 0),
        victorias=datos_valcyl.get("ganados3", 0)+ datos_valcyl.get("ganados2", 0),
        derrotas=datos_valcyl.get("perdidos1", 0)+ datos_valcyl.get("perdidos0", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del SALVADOR
    datos_salvador = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "CR El Salvador"),
        {}
    )
    
    # Obtener la fase regular de la temporada activa
    temporada = TemporadaSalvador.query.filter_by(activa=True).first()
    
    fase_regular = JornadaSalvador.query.filter_by(
        temporada_id=temporada.id,
        fase="Regular"
    ).order_by(JornadaSalvador.id).all()
    
    # Generar clasificación general igual que en la página oficial
    clasificacion_posiciones = generar_clasificacion_analisis_rugby_salvador(
        fase_regular
    )
    
    # Incorporar clubes sin partidos
    clubs = SalvadorClub.query.all()
    
    for club in clubs:
        if not any(e["equipo"] == club.nombre for e in clasificacion_posiciones):
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
    
    # Aplicar el mismo orden que la clasificación oficial
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
    
    # Obtener posición del SALVADOR
    posicion_liga = next(
        (    
            i + 1
            for i, equipo in enumerate(clasificacion_posiciones)
            if equipo["equipo"] == "CR El Salvador"
        ),
        "--"
    )
    # Buscar el último partido disputado por el SALVADOR
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "CR El Salvador" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "CR El Salvador" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "División de Honor"
              })
    
        # 2. Partidos de Copa
        for partido in CopaSalvador.query.all():
            if "CR El Salvador" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffSalvador.query.all():
            if "CR El Salvador" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Partidos de Supercopa
        for partido in SupercopaIbericaSalvador.query.all():
            if "CR El Salvador" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "SupercopaIberica"
            })
        # 5. Partidos de Europa
        for partido in EuropaSalvadorFem.query.all():
            if "CR El Salvador" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Europa"
            })        
        # 6. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
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
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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

    # Buscar los datos del SALVADOR FEM
    datos_salvador_fem = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "El Salvador R.C."),
        {}
    )
    # Generar clasificación general igual que en la página oficial
    clasificacion_posiciones = generar_clasificacion_analisis_rugby_salvador_fem(data)

    # Incorporar clubes sin partidos
    clubs = SalvadorFemClub.query.all()

    for club in clubs:
        if not any(e["equipo"] == club.nombre for e in clasificacion_posiciones):
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

    # Aplicar el mismo orden que la clasificación oficial
    clasificacion_posiciones = sorted(
        clasificacion_posiciones,
        key=lambda x: (
            x["datos"]["puntos"],
            x["datos"]["diferencia_goles"],
            x["datos"]["favor"]
        ),
        reverse=True
    )

    #clasificacion_posiciones = aplicar_h2h_en_empates(
    #   clasificacion_posiciones,
    #   data
    #)

    # Obtener posición del SALVADOR FEM
    posicion_liga = next(
        (
            i + 1
            for i, equipo in enumerate(clasificacion_posiciones)
            if equipo["equipo"] == "El Salvador R.C."
        ),
        "--"
    )

    # Recopilar resultados de todas las competiciones
    partidos_ultimo_resultado = []

    # 1. Partidos de Liga
    for jornada in data:
        for partido in jornada["partidos"]:
            if "El Salvador R.C." not in (partido.local, partido.visitante):
                continue

            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue

            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue

            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "División de Honor"
            })

    # 2. Partidos de Copa
    for partido in CopaSalvadorFem.query.all():
        if "El Salvador R.C." not in (partido.local, partido.visitante):
            continue

        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
            continue

        try:
            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
            goles_local = int(partido.resultadoA)
            goles_visitante = int(partido.resultadoB)
        except (ValueError, TypeError):
            continue

        partidos_ultimo_resultado.append({
            "fecha": fecha_partido,
            "local": partido.local,
            "visitante": partido.visitante,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "competicion": "Copa del Rey"
        })

    # 3. Partidos de Playoff
    for partido in PlayoffSalvadorFem.query.all():
        if "El Salvador R.C." not in (partido.local, partido.visitante):
            continue

        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
            continue

        try:
            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
            goles_local = int(partido.resultadoA)
            goles_visitante = int(partido.resultadoB)
        except (ValueError, TypeError):
            continue

        partidos_ultimo_resultado.append({
            "fecha": fecha_partido,
            "local": partido.local,
            "visitante": partido.visitante,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "competicion": "Playoff"
        })

    # 4. Partidos de Supercopa
    for partido in SupercopaIbericaSalvadorFem.query.all():
        if "El Salvador R.C." not in (partido.local, partido.visitante):
            continue

        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
            continue

        try:
            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
            goles_local = int(partido.resultadoA)
            goles_visitante = int(partido.resultadoB)
        except (ValueError, TypeError):
            continue

        partidos_ultimo_resultado.append({
            "fecha": fecha_partido,
            "local": partido.local,
            "visitante": partido.visitante,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "competicion": "Supercopa Ibérica"
        })

    # 5. Partidos de Europa
    for partido in EuropaSalvadorFem.query.all():
        if "El Salvador R.C." not in (partido.local, partido.visitante):
            continue

        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
            continue

        try:
            fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
            goles_local = int(partido.resultadoA)
            goles_visitante = int(partido.resultadoB)
        except (ValueError, TypeError):
            continue

        partidos_ultimo_resultado.append({
            "fecha": fecha_partido,
            "local": partido.local,
            "visitante": partido.visitante,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "competicion": "Europa"
        })

    # 6. Seleccionar el partido más reciente
    ultimo_partido = (
        max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
        if partidos_ultimo_resultado else None
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
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "RV Femenino"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "RV Femenino"),
        "--"
    )
    # Buscar el último partido disputado por el RV Femenino
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "RV Femenino" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "RV Femenino" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "Liga Gonalpi"
              })
    
        # 3. Partidos de Playoff
        for partido in PlayoffSimancas.query.all():
            if "RV Femenino" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/rv_femenino.html",
        "rv_fem",
        posicion_liga=posicion_liga,
        puntos_liga=datos_rv_fem.get("puntos", 0),
        partidos_jugados=datos_rv_fem.get("jugados", 0),
        victorias=datos_rv_fem.get("ganados", 0),
        empates=datos_rv_fem.get("empatados", 0),
        derrotas=datos_rv_fem.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(schema_sports_team(
            "rv_fem",
            "https://deportesdelaciudad.es/seccion/rv_fem"
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
    
    # Buscar los datos del Parquesol
    datos_parquesol = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "CD Parquesol"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "CD Parquesol"),
        "--"
    )
    # Buscar el último partido disputado por el Parquesol
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "CD Parquesol" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "CD Parquesol" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "3ª Federación-Grp 8"
              })
    
        # 3. Partidos de Playoff
        for partido in PlayoffParquesol.query.all():
            if "CD Parquesol" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/parquesol.html",
        "parquesol",
        posicion_liga=posicion_liga,
        puntos_liga=datos_parquesol.get("puntos", 0),
        partidos_jugados=datos_parquesol.get("jugados", 0),
        victorias=datos_parquesol.get("ganados", 0),
        empates=datos_parquesol.get("empatados", 0),
        derrotas=datos_parquesol.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del VTG
    datos_galvan = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "VTG FS"),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "VTG FS"),
        "--"
    )
    # Buscar el último partido disputado por el VTG
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "VTG FS" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "VTG FS" not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "2ª División B-Grp 1"
              })
    
        # 2. Partidos de Copa
        for partido in CopaGalvan.query.all():
            if "VTG FS" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffGalvan.query.all():
            if "VTG FS" not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/galvan.html",
        "galvan",
        posicion_liga=posicion_liga,
        puntos_liga=datos_galvan.get("puntos", 0),
        partidos_jugados=datos_galvan.get("jugados", 0),
        victorias=datos_galvan.get("ganados", 0),
        empates=datos_galvan.get("empatados", 0),
        derrotas=datos_galvan.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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
    
    # Buscar los datos del VALLADOLID S.S
    datos_vall_sala = next(
        (equipo["datos"] for equipo in clasificacion
         if equipo["equipo"] == "Valladolid S.S."),
        {}
    )
    
    # Posición en la clasificación
    posicion_liga = next(
        (i + 1 for i, equipo in enumerate(clasificacion)
         if equipo["equipo"] == "Valladolid S.S."),
        "--"
    )
    # Buscar el último partido disputado por el VALLADOLID S.S
    ultimo_partido = None
    
    for jornada in data:
        for partido in jornada["partidos"]:
    
            if "Valladolid S.S." not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            ultimo_partido = {
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
        }
        partidos_ultimo_resultado = []
    
        # 1. Partidos de Liga
        for jornada in data:
            for partido in jornada["partidos"]:
                if "Valladolid S.S." not in (partido.local, partido.visitante):
                    continue
    
                if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                    continue
    
                try:
                    fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue
    
                partidos_ultimo_resultado.append({
                    "fecha": fecha_partido,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": "3ª División-Grp 9"
              })
    
        # 2. Partidos de Copa
        for partido in CopaVallSala.query.all():
            if "Valladolid S.S." not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
    
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Copa del Rey"
            })
    
        # 3. Partidos de Playoff
        for partido in PlayoffVallSala.query.all():
            if "Valladolid S.S." not in (partido.local, partido.visitante):
                continue
    
            if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
                continue
            try:
                fecha_partido = datetime.strptime(partido.fecha, "%d.%m.%y")
                goles_local = int(partido.resultadoA)
                goles_visitante = int(partido.resultadoB)
            except (ValueError, TypeError):
                continue
    
            partidos_ultimo_resultado.append({
                "fecha": fecha_partido,
                "local": partido.local,
                "visitante": partido.visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante,
                "competicion": "Playoff"
            })
        # 4. Seleccionar el partido más reciente
        ultimo_partido = (
            max(partidos_ultimo_resultado, key=lambda p: p["fecha"])
            if partidos_ultimo_resultado else None
        )    
    
    return render_seccion(
        "secciones/vall_sala.html",
        "vall_sala",
        posicion_liga=posicion_liga,
        puntos_liga=datos_vall_sala.get("puntos", 0),
        partidos_jugados=datos_vall_sala.get("jugados", 0),
        victorias=datos_vall_sala.get("ganados", 0),
        empates=datos_vall_sala.get("empatados", 0),
        derrotas=datos_vall_sala.get("perdidos", 0),
        ultimo_competicion=ultimo_partido["competicion"] if ultimo_partido else "--",
        ultimo_local=ultimo_partido["local"] if ultimo_partido else "--",
        ultimo_visitante=ultimo_partido["visitante"] if ultimo_partido else "--",
        ultimo_goles_local=ultimo_partido["goles_local"] if ultimo_partido else "--",
        ultimo_goles_visitante=ultimo_partido["goles_visitante"] if ultimo_partido else "--",
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