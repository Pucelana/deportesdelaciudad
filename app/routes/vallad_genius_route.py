from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from collections import OrderedDict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app.seo.schema import jsonld, obtener_partidos_schema, schema_partidos, schema_sports_competition, schema_sports_team, schema_breadcrumb_equipo
from ..models.historial import obtener_evolucion_puntos
from ..models.historial import Historial, Palmaress
from ..models.vallad_genius import (
    JornadaValladGenius,
    ValladGeniusPartido,
    ValladGeniusClub,
    TemporadaValladGenius 
)

vallad_genius_route_bp = Blueprint("vallad_genius_route_bp", __name__)

# LIGA REAL VALLADOLIDI
# Crear el calendario Real Valladolid
@vallad_genius_route_bp.route("/admin/crear_calendario_vallad_genius", methods=["GET", "POST"])
def ingresar_resultado_vallad_genius():
    if request.method == "POST":
        temporada_nombre = request.form["temporada"]
        nombre_jornada = request.form["nombre"]
        num_partidos = int(request.form["num_partidos"])
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaValladGenius.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaValladGenius(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaValladGenius(nombre=nombre_jornada, temporada_id=temporada.id)
        db.session.add(jornada)
        db.session.flush()
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            partido = ValladGeniusPartido(
                jornada_id=jornada.id,
                fecha=request.form.get(f"fecha{i}"),
                hora=request.form.get(f"hora{i}"),
                local=request.form.get(f"local{i}"),
                resultadoA=request.form.get(f"resultadoA{i}"),
                resultadoB=request.form.get(f"resultadoB{i}"),
                visitante=request.form.get(f"visitante{i}"),
                pfp_local=request.form.get(f"pfp_local{i}") or None,
                pfp_visitante=request.form.get(f"pfp_visitante{i}") or None,
                orden=i,
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for("vallad_genius_route_bp.calendarios_vallad_genius"))
    # Si es un GET, renderizamos el formulario de creación
    return render_template("admin/calendarios/calend_vallad_genius.html")
# Ver calendario Real Valladolid en Admin
@vallad_genius_route_bp.route("/admin/calendario_vallad_genius")
def calendarios_vallad_genius():
    temporada = TemporadaValladGenius.query.filter_by(activa=True).first()
    if temporada:
        jornadas = (
            JornadaValladGenius.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaValladGenius.id.asc())
            .all()
        )
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = (
            db.session.query(ValladGeniusPartido)
            .filter_by(jornada_id=jornada.id)
            .order_by(ValladGeniusPartido.orden.asc())
            .all()
        )
    return render_template(
        "admin/calendarios/calend_vallad_genius.html", jornadas=jornadas
    )
# Modificar jornada
@vallad_genius_route_bp.route("/modificar_jornada_vallad_genius/<int:id>", methods=["GET", "POST"])
def modificar_jornada_vallad_genius(id):
    jornada = (db.session.query(JornadaValladGenius).filter(JornadaValladGenius.id == id).first())
    if jornada:
        if request.method == "POST":
            nombre_jornada = request.form["nombre"]
            num_partidos = int(request.form["num_partidos"])
            jornada.nombre = nombre_jornada
            for i in range(num_partidos):
                partido_id = request.form[f"partido_id{i}"]
                partido = (db.session.query(ValladGeniusPartido).filter(
                        ValladGeniusPartido.id == partido_id).first())
                if partido:
                    partido.fecha = request.form.get(f"fecha{i}")
                    partido.hora = request.form.get(f"hora{i}")
                    partido.local = request.form.get(f"local{i}")
                    partido.resultadoA = request.form.get(f"resultadoA{i}")
                    partido.resultadoB = request.form.get(f"resultadoB{i}")
                    partido.visitante = request.form.get(f"visitante{i}")
                    # FAIR PLAY
                    partido.pfp_local = (request.form.get(f"pfp_local{i}") or None)
                    partido.pfp_visitante = (request.form.get(f"pfp_visitante{i}") or None)
                    partido.orden = int(request.form.get(f"orden{i}",i))
            db.session.commit()
            return redirect(url_for("vallad_genius_route_bp.calendarios_vallad_genius"))
        # Preparar hora para el formulario
        for partido in jornada.partidos:
            if partido.hora:
                try:
                    partido.hora = partido.hora.strftime("%H:%M")
                except AttributeError:
                    pass
    return render_template(
        "admin/calendarios/calend_vallad_genius.html",
        jornada=jornada
    )
# Eliminar jornada
@vallad_genius_route_bp.route("/eliminar_jornada_vallad_genius/<int:id>", methods=["GET", "POST"])
def eliminar_jornada_vallad_genius(id):
    # Obtener la jornada
    jornada = (
        db.session.query(JornadaValladGenius).filter(JornadaValladGenius.id == id).first()
    )
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(ValladGeniusPartido).filter(
            ValladGeniusPartido.jornada_id == id
        ).delete()
        # Eliminar la jornada
        db.session.delete(jornada)
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for("vallad_genius_route_bp.calendarios_vallad_genius"))
# Obtener datos Real Valladolid
def obtener_datos_vallad_genius(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaValladGenius.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaValladGenius.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            ValladGeniusPartido.query.filter_by(jornada_id=jornada.id)
            .order_by(ValladGeniusPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({"nombre": jornada.nombre, "partidos": partidos})
    return jornadas_con_partidos
# Calendario Real Valladolid
@vallad_genius_route_bp.route("/equipos_futbol/calendario_vallad_genius")
def calendario_vallad_genius():

    datos = obtener_datos_vallad_genius()

    equipo_vallad_genius = "R.ValladoliDi"

    tabla_partidos_vallad_genius = []

    for jornada in datos:

        for partido in jornada["partidos"]:

            # Solo partidos del R.ValladoliDi
            if (
                partido.local != equipo_vallad_genius
                and partido.visitante != equipo_vallad_genius
            ):
                continue

            # R.ValladoliDi como local
            if partido.local == equipo_vallad_genius:

                rival = partido.visitante
                rol = "L"

                resultado_vallad_genius = partido.resultadoA
                resultado_rival = partido.resultadoB

            # R.ValladoliDi como visitante
            else:

                rival = partido.local
                rol = "V"

                resultado_vallad_genius = partido.resultadoB
                resultado_rival = partido.resultadoA

            tabla_partidos_vallad_genius.append({
                "jornada": jornada["nombre"],
                "equipo": rival,
                "rol": rol,
                "resultado_vallad_genius": resultado_vallad_genius,
                "resultado_rival": resultado_rival
            })

    partidos_schema = obtener_partidos_schema(datos)

    return render_template(
        "equipos_vall/calendario_vallad_genius.html",

        tabla_partidos_vallad_genius=tabla_partidos_vallad_genius,

        breadcrumb=jsonld(
            schema_breadcrumb_equipo("valladoliDi")
        ),

        schema_team=jsonld(
            schema_sports_team(
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_vallad_genius"
            )
        ),

        schema_competition=jsonld(
            schema_sports_competition(
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_vallad_genius"
            )
        ),

        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_vallad_genius"
            )
        )
    )
# Jornadas Real Valladolid
@vallad_genius_route_bp.route("/equipos_futbol/resultados_vallad_genius")
def resultados_vallad_genius():
    datos = obtener_datos_vallad_genius()
    nuevos_datos_vallad_genius = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_vallad_genius):
        jornada_completa = all(
            p.resultadoA not in (None, "") and p.resultadoB not in (None, "")
            for p in jornada["partidos"]
        )
        if not jornada_completa:
            jornada_activa = jornada["nombre"]
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_vallad_genius:
        jornada_activa = nuevos_datos_vallad_genius[-1]["nombre"]
    partidos_schema = obtener_partidos_schema(nuevos_datos_vallad_genius)    
    return render_template(
        "equipos_vall/jornadas_vallad_genius.html",
        nuevos_datos_vallad_genius=nuevos_datos_vallad_genius,
        jornada_activa=jornada_activa,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("valladoliDi")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_vallad_genius"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_vallad_genius"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_vallad_genius"
            )
        )
    )
# Jornada 0 Real Valladolid
@vallad_genius_route_bp.route("/admin/jornada0_vallad_genius", methods=["GET", "POST"])
def jornada0_vallad_genius():
    if request.method == "POST":
        if "equipo" in request.form:
            club = request.form["equipo"]
            if club:
                nuevo_club = ValladGeniusClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for("vallad_genius_route_bp.jornada0_vallad_genius"))
    clubs = ValladGeniusClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template("admin/clubs/clubs_vallad_genius.html", clubs=clubs)
# Eliminar clubs jornada 0
@vallad_genius_route_bp.route("/eliminar_club_vallad_genius/<int:club_id>", methods=["POST"])
def eliminar_club_vallad_genius(club_id):
    club = ValladGeniusClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for("vallad_genius_route_bp.jornada0_vallad_genius"))
# Crear la clasificación Real ValladoliDi competividad
def generar_clasificacion_analisis_futbol_vallad_genius(data):
    clasificacion = defaultdict(
        lambda: {
            "jugados": 0,
            "ganados": 0,
            "empatados": 0,
            "perdidos": 0,
            "puntos": 0,
            "ptg": 0,
            "pte": 0,
            "ptp": 0,
        }
    )

    # ================================
    # ENFRENTAMIENTOS DIRECTOS
    # ================================
    enfrentamientos = defaultdict(list)

    # ================================
    # RECORRER PARTIDOS
    # ================================
    for jornada in data:

        for partido in jornada["partidos"]:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            # Partido sin resultado
            if r1 is None or r2 is None or r1 == "" or r2 == "":
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            # ================================
            # JUGADOS
            # ================================
            clasificacion[local]["jugados"] += 1
            clasificacion[visitante]["jugados"] += 1

            # ================================
            # RESULTADO DEL PARTIDO
            # ================================
            if r1 > r2:

                clasificacion[local]["puntos"] += 3
                clasificacion[local]["ganados"] += 1
                
                clasificacion[visitante]["puntos"] += 1
                clasificacion[visitante]["perdidos"] += 1

            elif r1 < r2:

                clasificacion[visitante]["puntos"] += 3
                clasificacion[visitante]["ganados"] += 1
                
                clasificacion[local]["puntos"] += 1
                clasificacion[local]["perdidos"] += 1

            else:

                clasificacion[local]["puntos"] += 2
                clasificacion[visitante]["puntos"] += 2

                clasificacion[local]["empatados"] += 1
                clasificacion[visitante]["empatados"] += 1

            # ================================
            # PARTES
            # ================================
            ptg_local = r1
            ptp_local = r2
            pte_local = 4 - ptg_local - ptp_local

            ptg_visitante = r2
            ptp_visitante = r1
            pte_visitante = 4 - ptg_visitante - ptp_visitante

            clasificacion[local]["ptg"] += ptg_local
            clasificacion[local]["pte"] += pte_local
            clasificacion[local]["ptp"] += ptp_local

            clasificacion[visitante]["ptg"] += ptg_visitante
            clasificacion[visitante]["pte"] += pte_visitante
            clasificacion[visitante]["ptp"] += ptp_visitante

            # ================================
            # ENFRENTAMIENTOS DIRECTOS
            # ================================
            enfrentamientos[frozenset([local, visitante])].append(
                {
                    "local": local,
                    "visitante": visitante,
                    "resultado_local": r1,
                    "resultado_visitante": r2,
                }
            )

    # ================================
    # AVERAGE PARTICULAR
    # ================================
    def average_particular(a, b):

        partidos = enfrentamientos.get(
            frozenset([a, b]),
            []
        )

        if len(partidos) < 2:
            return None

        puntos_a = 0
        puntos_b = 0

        ptg_a = 0
        ptg_b = 0

        for p in partidos:

            local = p["local"]
            visitante = p["visitante"]

            rl = p["resultado_local"]
            rv = p["resultado_visitante"]

            if local == a:
                ra = rl
                rb = rv
            else:
                ra = rv
                rb = rl

            # Puntos del partido
            if ra > rb:
                puntos_a += 3

            elif rb > ra:
                puntos_b += 3

            else:
                puntos_a += 1
                puntos_b += 1

            # Partes ganadas
            ptg_a += ra
            ptg_b += rb

        return {
            "puntos_a": puntos_a,
            "puntos_b": puntos_b,
            "ptg_a": ptg_a,
            "ptg_b": ptg_b,
        }

    # ================================
    # COMPARADOR
    # ================================
    def comparar(a, b):

        na, da = a
        nb, db = b

        # 1. PUNTOS
        if da["puntos"] != db["puntos"]:
            return db["puntos"] - da["puntos"]

        # 2. ENFRENTAMIENTO DIRECTO
        av = average_particular(na, nb)

        if av:

            if av["puntos_a"] != av["puntos_b"]:
                return av["puntos_b"] - av["puntos_a"]

            if av["ptg_a"] != av["ptg_b"]:
                return av["ptg_b"] - av["ptg_a"]

        # 3. PARTES GANADAS
        if da["ptg"] != db["ptg"]:
            return db["ptg"] - da["ptg"]

        # 4. PARTES EMPATADAS
        if da["pte"] != db["pte"]:
            return db["pte"] - da["pte"]

        # 5. PARTES PERDIDAS
        if da["ptp"] != db["ptp"]:
            return da["ptp"] - db["ptp"]

        return 0

    # ================================
    # ORDEN FINAL
    # ================================
    equipos = list(clasificacion.items())

    equipos.sort(key=cmp_to_key(comparar))

    return [
        {
            "equipo": equipo,
            "datos": datos
        }
        for equipo, datos in equipos
    ]
# Crear clasificación Real ValladoliDi fair play
def generar_clasificacion_fair_play_vallad_genius(data):

    clasificacion = defaultdict(
        lambda: {
            "jugados": 0,
            "pfp": 0,
        }
    )

    # ================================
    # RECORRER PARTIDOS
    # ================================
    for jornada in data:

        for partido in jornada["partidos"]:

            local = partido.local
            visitante = partido.visitante

            # ----------------------------
            # FAIR PLAY LOCAL
            # ----------------------------
            pfp_local = partido.pfp_local

            # ----------------------------
            # FAIR PLAY VISITANTE
            # ----------------------------
            pfp_visitante = partido.pfp_visitante

            # Si no hay puntuación de Fair Play,
            # no contamos el partido para esta clasificación
            if (
                pfp_local is None
                or pfp_local == ""
                or pfp_visitante is None
                or pfp_visitante == ""
            ):
                continue

            try:
                pfp_local = int(pfp_local)
                pfp_visitante = int(pfp_visitante)

            except (ValueError, TypeError):
                continue

            # ================================
            # PARTIDO JUGADO
            # ================================
            clasificacion[local]["jugados"] += 1
            clasificacion[visitante]["jugados"] += 1

            # ================================
            # PUNTOS FAIR PLAY
            # ================================
            clasificacion[local]["pfp"] += pfp_local
            clasificacion[visitante]["pfp"] += pfp_visitante

    # ================================
    # ORDEN
    # ================================
    equipos = list(clasificacion.items())

    equipos.sort(
        key=lambda x: (
            x[1]["pfp"],
            x[1]["pfp"] / x[1]["jugados"]
            if x[1]["jugados"] > 0
            else 0,
            x[0],
        ),
        reverse=True,
    )

    return [
        {
            "equipo": equipo,
            "datos": datos,
        }
        for equipo, datos in equipos
    ]
# Ruta para mostrar la clasificación y análisis del Real Valladolid
@vallad_genius_route_bp.route("/equipos_futbol/clasif_vallad_genius")
def clasif_analisis_vallad_genius():

    # ==================================================
    # DATOS DE LOS PARTIDOS
    # ==================================================

    data = obtener_datos_vallad_genius()


    # ==================================================
    # CLASIFICACIÓN COMPETITIVIDAD
    # ==================================================

    clasificacion_analisis_vallad_genius = (
        generar_clasificacion_analisis_futbol_vallad_genius(data)
    )


    # ==================================================
    # CLASIFICACIÓN FAIR PLAY
    # ==================================================

    clasificacion_fair_play_vallad_genius = (
        generar_clasificacion_fair_play_vallad_genius(data)
    )


    # ==================================================
    # EQUIPOS DE LA BASE DE DATOS
    # ==================================================

    clubs_vallad_genius = ValladGeniusClub.query.all()


    # ==================================================
    # AÑADIR EQUIPOS SIN PARTIDOS A COMPETITIVIDAD
    # ==================================================

    for club in clubs_vallad_genius:

        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_analisis_vallad_genius
        ):

            clasificacion_analisis_vallad_genius.append(
                {
                    "equipo": club.nombre,
                    "datos": {
                        "puntos": 0,
                        "jugados": 0,
                        "ganados": 0,
                        "empatados": 0,
                        "perdidos": 0,
                        "ptg": 0,
                        "pte": 0,
                        "ptp": 0,
                    },
                }
            )


    # ==================================================
    # AÑADIR EQUIPOS SIN FAIR PLAY
    # ==================================================

    for club in clubs_vallad_genius:

        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_fair_play_vallad_genius
        ):

            clasificacion_fair_play_vallad_genius.append(
                {
                    "equipo": club.nombre,
                    "datos": {
                        "jugados": 0,
                        "pfp": 0,
                    },
                }
            )


    # ==================================================
    # ORDEN COMPETITIVIDAD
    # ==================================================

    clasificacion_analisis_vallad_genius.sort(
        key=lambda x: x["datos"]["puntos"],
        reverse=True
    )


    # ==================================================
    # ORDEN FAIR PLAY
    # ==================================================

    clasificacion_fair_play_vallad_genius.sort(
        key=lambda x: x["datos"]["pfp"],
        reverse=True
    )


    # ==================================================
    # RENDER
    # ==================================================

    return render_template(
        "equipos_vall/clasif_vallad_genius.html",

        clasificacion_analisis_vallad_genius=(
            clasificacion_analisis_vallad_genius
        ),

        clasificacion_fair_play_vallad_genius=(
            clasificacion_fair_play_vallad_genius
        ),

        breadcrumb=jsonld(
            schema_breadcrumb_equipo("valladoliDi")
        ),

        schema_team=jsonld(
            schema_sports_team(
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/clasif_vallad_genius"
            )
        ),

        schema_competition=jsonld(
            schema_sports_competition(
                "valladoliDi",
                "https://deportesdelaciudad.es/equipos_futbol/clasif_vallad_genius"
            )
        )
    )
# TEMPORADAS REAL VALLADOLID
@vallad_genius_route_bp.route("/admin/temporadas_vallad_genius")
def temporadas_vallad_genius():
    temporadas = TemporadaValladGenius.query.order_by(TemporadaValladGenius.id.desc()).all()
    return render_template(
        "admin/temporadas/temporada_vallad_genius.html", temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@vallad_genius_route_bp.route("/activar_temporada_vallad_genius/<int:id>")
def activar_temporada_vallad_genius(id):
    TemporadaValladGenius.query.update({"activa": False})
    temporada = TemporadaValladGenius.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for("vallad_genius_route_bp.temporadas_vallad_genius"))

# HISTORIAL REAL VALLADOLID
# Creación del historial de temporadas del Real Valladolid
@vallad_genius_route_bp.route("/admin/crear_historial_vallad_genius", methods=["GET", "POST"])
def crear_historial_vallad_genius():
    if request.method == "POST":
        historial = Historial(
            deporte="futbol",
            equipo="R.ValladoliDi",
            temporada=request.form.get("temporada"),
            liga=request.form.get("liga"),
            puntos=request.form.get("puntos"),
            puesto=request.form.get("puesto"),
            playoff=request.form.get("playoff"),
            copa=request.form.get("copa"),
            europa=request.form.get("europa"),
            titulos=request.form.get("titulos"),
            siguiente_temporada=request.form.get("siguiente_temporada"),
            observaciones=request.form.get("observaciones"),
        )
        db.session.add(historial)
        db.session.commit()
        return redirect(url_for("vallad_genius_route_bp.crear_historial_vallad_genius"))
    historial = (Historial.query.filter_by(
        deporte="futbol",
        equipo="R.ValladoliDi"
    ).order_by(Historial.temporada.desc()).all()
                 )
    temporadas = TemporadaValladGenius.query.order_by(
        TemporadaValladGenius.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial.html",
        historial=historial,
        temporadas=temporadas,
        deporte="futbol",
        equipo="R.ValladoliDi",
        crear_url="vallad_genius_route_bp.crear_historial_vallad_genius",
        modificar_url="vallad_genius_route_bp.modificar_historial_vallad_genius",
        eliminar_url="vallad_genius_route_bp.eliminar_historial_vallad_genius"
    )
# Eliminar historial de temporadas del Real Valladolid
@vallad_genius_route_bp.route("/admin/eliminar_historial_vallad_genius/<int:id>", methods=["POST"])
def eliminar_historial_vallad_genius(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("vallad_genius_route_bp.crear_historial_vallad_genius"))
# Modificar historial de temporadas del Real Valladolid
@vallad_genius_route_bp.route("/admin/modificar_historial_vallad_genius/<int:id>", methods=["POST"])
def modificar_historial_vallad_genius(id):
    historial = Historial.query.get_or_404(id)
    historial.temporada = request.form.get("temporada")
    historial.liga = request.form.get("liga")
    historial.puntos = request.form.get("puntos")
    historial.puesto = request.form.get("puesto")
    historial.playoff = request.form.get("playoff")
    historial.copa = request.form.get("copa")
    historial.europa = request.form.get("europa")
    historial.siguiente_temporada = request.form.get("siguiente_temporada")
    historial.titulos = request.form.get("titulos")
    historial.observaciones = request.form.get("observaciones")
    db.session.commit()
    return redirect(url_for("vallad_genius_route_bp.crear_historial_vallad_genius"))
# Ver Historial de temporadas del Real Valladolid en la página principal
@vallad_genius_route_bp.route("/vallad_genius/historial")
def historial_vallad_genius():

    historial = (
        Historial.query
        .filter_by(
            deporte="futbol",
            equipo="R.ValladoliDi"
        )
        .order_by(Historial.temporada.desc())
        .all()
    )
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = (
        TemporadaValladGenius.query
        .order_by(TemporadaValladGenius.id)
        .all()
    )
    datasets_jornadas = []

    colores = [
        "#672e8d",
        "#FFD700",
        "#00BFFF",
        "#32CD32",
        "#FF4500",
        "#FF1493",
        "#FF6A00",
        "#20B2AA",
    ]

    labels_jornadas = []

    for i, temporada in enumerate(temporadas):
        jornadas = (
            JornadaValladGenius.query
            .filter_by(temporada_id=temporada.id)
            .order_by(JornadaValladGenius.id)
            .all()
        )
        if not jornadas:
            continue

        labels, puntos = obtener_evolucion_puntos(
            jornadas,
            "R.ValladoliDi",
            generar_clasificacion_analisis_futbol_vallad_genius,
            "puntos"
        )
        # Guardamos las etiquetas
        labels_jornadas = labels

        datasets_jornadas.append(
            {
                "label": temporada.nombre,
                "data": puntos,
                "borderColor": colores[i % len(colores)],
                "backgroundColor": colores[i % len(colores)],
                "borderWidth": 3,
                "pointRadius": 4,
                "pointHoverRadius": 7,
                "fill": False,
                "tension": 0.3,
            }
        )

    # ================================
    # PALMARÉS
    # ================================

    titulos = (
        Palmaress.query
        .filter_by(
            deporte="futbol",
            equipo="R.ValladoliDi"
        )
        .order_by(
            Palmaress.orden.asc(),
            Palmaress.temporada.desc()
        )
        .all()
    )

    palmares = OrderedDict()

    for titulo in titulos:

        if titulo.competicion not in palmares:
            palmares[titulo.competicion] = []

        palmares[titulo.competicion].append(titulo)

    # ================================
    # RENDER
    # ================================

    return render_template(
        "historia/historia_vallad_genius.html",

        historial=historial,

        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,

        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,

        palmares=palmares,

        deporte="Fútbol",
        equipo="R.ValladoliDi",

        breadcrumb=jsonld(
            schema_breadcrumb_equipo("valladoliDi")
        ),

        schema_team=jsonld(
            schema_sports_team(
                "valladoliDi",
                "https://deportesdelaciudad.es/vallad_genius/historial"
            )
        ),

        schema_competition=jsonld(
            schema_sports_competition(
                "valladoliDi",
                "https://deportesdelaciudad.es/vallad_genius/historial"
            )
        )
    )

# PALMARES REAL VALLADOLID
# Crear Palmares del Real Valladolid
@vallad_genius_route_bp.route("/admin/crear_palmares_vallad_genius", methods=["GET", "POST"])
def crear_palmares_vallad_genius():
    if request.method == "POST":
        titulo = Palmaress(
            deporte="futbol",
            equipo="R.ValladoliDi",
            temporada=request.form.get("temporada"),
            competicion=request.form.get("competicion"),
            imagen=request.form.get("imagen"),
            orden=int(request.form.get("orden", 0))
        )
        db.session.add(titulo)
        db.session.commit()
        return redirect(url_for("vallad_genius_route_bp.crear_palmares_vallad_genius"))
    palmares = (
        Palmaress.query.filter_by(
            deporte="futbol",
            equipo="R.ValladoliDi"
        )
        .order_by(Palmaress.orden.asc(),Palmaress.temporada.desc())
        .all()
    )
    return render_template(
        "admin/historial/palmares.html",
        palmares=palmares,
        deporte="Fútbol",
        equipo="R.ValladoliDi",
        crear_url="vallad_genius_route_bp.crear_palmares_vallad_genius",
        modificar_url="vallad_genius_route_bp.modificar_palmares_vallad_genius",
        eliminar_url="vallad_genius_route_bp.eliminar_palmares_vallad_genius",
    )
# Modificar Palmares del Real Valladolid
@vallad_genius_route_bp.route("/admin/modificar_palmares_vallad_genius/<int:id>", methods=["POST"])
def modificar_palmares_vallad_genius(id):
    titulo = Palmaress.query.get_or_404(id)
    titulo.temporada = request.form.get("temporada")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    titulo.orden = request.form.get("orden")
    db.session.commit()
    return redirect(url_for("vallad_genius_route_bp.crear_palmares_vallad_genius"))
# Eliminar Palmares del RV Promesas
@vallad_genius_route_bp.route("/admin/eliminar_palmares_vallad_genius/<int:id>", methods=["POST"])
def eliminar_palmares_vallad_genius(id):
    titulo = Palmaress.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("vallad_genius_route_bp.crear_palmares_vallad_genius"))