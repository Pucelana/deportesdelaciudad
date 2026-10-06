from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from collections import OrderedDict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app.routes.main import NOMBRES_EQUIPOS
from app.seo.schema import jsonld, obtener_partidos_schema, schema_partidos, schema_sports_competition, schema_sports_team, schema_breadcrumb_equipo
from ..models.historial import obtener_evolucion_puntos
from ..models.historial import Historial, Palmaress
from ..models.tordesillas import (
    JornadaTordesillas,
    TordesillasPartido,
    TordesillasClub,
    CopaTordesillas,
    PlayoffTordesillas,
    TemporadaTordesillas
)

tordesillas_route_bp = Blueprint("tordesillas_route_bp", __name__)

# LIGA REAL TODESILLAS
# Crear el calendario Real Tordesillas
@tordesillas_route_bp.route("/admin/crear_calendario_tordesillas", methods=["GET", "POST"])
def ingresar_resultado_tordesillas():
    if request.method == "POST":
        temporada_nombre = request.form["temporada"]
        nombre_jornada = request.form["nombre"]
        num_partidos = int(request.form["num_partidos"])
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaTordesillas.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaTordesillas(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaTordesillas(nombre=nombre_jornada, temporada_id=temporada.id)
        db.session.add(jornada)
        db.session.flush()
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            partido = TordesillasPartido(
                jornada_id=jornada.id,
                fecha=request.form.get(f"fecha{i}"),
                hora=request.form.get(f"hora{i}"),
                local=request.form.get(f"local{i}"),
                resultadoA=request.form.get(f"resultadoA{i}"),
                resultadoB=request.form.get(f"resultadoB{i}"),
                visitante=request.form.get(f"visitante{i}"),
                orden=i,
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for("tordesillas_route_bp.calendarios_tordesillas"))
    # Si es un GET, renderizamos el formulario de creación
    return render_template("admin/calendarios/calend_tordesillas.html")
# Ver calendario Real Tordesillas en Admin
@tordesillas_route_bp.route("/admin/calendario_tordesillas")
def calendarios_tordesillas():
    temporada = TemporadaTordesillas.query.filter_by(activa=True).first()
    if temporada:
        jornadas = (
            JornadaTordesillas.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaTordesillas.id.asc())
            .all()
        )
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = (
            db.session.query(TordesillasPartido)
            .filter_by(jornada_id=jornada.id)
            .order_by(TordesillasPartido.orden.asc())
            .all()
        )
    return render_template(
        "admin/calendarios/calend_tordesillas.html", jornadas=jornadas
    )
# Modificar jornada
@tordesillas_route_bp.route("/modificar_jornada_tordesillas/<int:id>", methods=["GET", "POST"])
def modificar_jornada_tordesillas(id):
    jornada = (
        db.session.query(JornadaTordesillas).filter(JornadaTordesillas.id == id).first()
    )
    if jornada:
        if request.method == "POST":
            nombre_jornada = request.form["nombre"]
            num_partidos = int(request.form["num_partidos"])
            jornada.nombre = nombre_jornada  # Actualizar el nombre de la jornada
            # Actualizar los partidos
            for i in range(num_partidos):
                partido_id = request.form[f"partido_id{i}"]
                fecha = request.form[f"fecha{i}"]
                hora = request.form[f"hora{i}"]
                local = request.form[f"local{i}"]
                resultadoA = request.form[f"resultadoA{i}"]
                resultadoB = request.form[f"resultadoB{i}"]
                visitante = request.form[f"visitante{i}"]
                # Obtener el partido correspondiente por ID
                partido = (
                    db.session.query(TordesillasPartido)
                    .filter(TordesillasPartido.id == partido_id)
                    .first()
                )
                if partido:
                    partido.fecha = fecha
                    partido.hora = hora
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante
                    orden = int(
                        request.form.get(f"orden{i}", i)
                    )  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for("tordesillas_route_bp.calendarios_tordesillas"))
        # Si es un GET, pasamos la jornada con sus partidos ya cargados
        for partido in jornada.partidos:
            partido.hora = partido.hora.strftime("%H:%M") if partido.hora else ""
    return render_template("admin/calendarios/calend_tordesillas.html", jornada=jornada)
# Eliminar jornada
@tordesillas_route_bp.route("/eliminar_jornada_tordesillas/<int:id>", methods=["GET", "POST"])
def eliminar_jornada_tordesillas(id):
    # Obtener la jornada
    jornada = (
        db.session.query(JornadaTordesillas).filter(JornadaTordesillas.id == id).first()
    )
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(TordesillasPartido).filter(
            TordesillasPartido.jornada_id == id
        ).delete()
        # Eliminar la jornada
        db.session.delete(jornada)
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for("tordesillas_route_bp.calendarios_tordesillas"))
# Obtener datos Real Valladolid
def obtener_datos_tordesillas(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaTordesillas.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaTordesillas.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            TordesillasPartido.query.filter_by(jornada_id=jornada.id)
            .order_by(TordesillasPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({"nombre": jornada.nombre, "partidos": partidos})
    return jornadas_con_partidos
# Calendario Real Valladolid
@tordesillas_route_bp.route("/equipos_futbol/calendario_tordesillas")
def calendario_tordesillas():
    datos = obtener_datos_tordesillas()
    equipo_tordesillas = NOMBRES_EQUIPOS["tordesillas"]
    tabla_partidos_tordesillas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada["partidos"]:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB
            # Verificamos si el UEMC está jugando
            if (
                equipo_local in equipo_tordesillas
                or equipo_visitante in equipo_tordesillas
            ):
                # Determinamos el equipo contrario y los resultados
                if equipo_local in equipo_tordesillas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_tordesillas = "C"
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_tordesillas = "F"
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_tordesillas:
                    tabla_partidos_tordesillas[equipo_contrario] = {"jornadas": {}}
                # Verificamos si es el primer o segundo enfrentamiento
                if (
                    "primer_enfrentamiento"
                    not in tabla_partidos_tordesillas[equipo_contrario]
                ):
                    tabla_partidos_tordesillas[equipo_contrario][
                        "primer_enfrentamiento"
                    ] = jornada["nombre"]
                    tabla_partidos_tordesillas[equipo_contrario][
                        "resultadoA"
                    ] = resultado_a
                    tabla_partidos_tordesillas[equipo_contrario][
                        "resultadoB"
                    ] = resultado_b
                elif (
                    "segundo_enfrentamiento"
                    not in tabla_partidos_tordesillas[equipo_contrario]
                ):
                    tabla_partidos_tordesillas[equipo_contrario][
                        "segundo_enfrentamiento"
                    ] = jornada["nombre"]
                    tabla_partidos_tordesillas[equipo_contrario][
                        "resultadoAA"
                    ] = resultado_a
                    tabla_partidos_tordesillas[equipo_contrario][
                        "resultadoBB"
                    ] = resultado_b
                # Agregamos la jornada y resultados
                if (
                    jornada["nombre"]
                    not in tabla_partidos_tordesillas[equipo_contrario]["jornadas"]
                ):
                    tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ] = {
                        "resultadoA": resultado_a,
                        "resultadoB": resultado_b,
                        "rol_tordesillas": rol_tordesillas,
                    }
                # Asignamos los resultados según el rol del UEMC
                if (
                    equipo_local == equipo_contrario
                    or equipo_visitante == equipo_contrario
                ):
                    if not tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoA"]:
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoA"] = resultado_a
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoB"] = resultado_b
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_tordesillas"] = rol_tordesillas
                    else:
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_tordesillas"] = rol_tordesillas
                else:
                    if not tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoAA"]:
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_tordesillas"] = rol_tordesillas
                    else:
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_tordesillas[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_tordesillas"] = rol_tordesillas
    partidos_schema = obtener_partidos_schema(datos)                    
    return render_template(
        "equipos_vall/calendario_tordesillas.html",
        tabla_partidos_tordesillas=tabla_partidos_tordesillas,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_tordesillas"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_tordesillas"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_tordesillas"
            )
        )
    )
# Jornadas Tordesillas
@tordesillas_route_bp.route("/equipos_futbol/resultados_tordesillas")
def resultados_tordesillas():
    datos = obtener_datos_tordesillas()
    nuevos_datos_tordesillas = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_tordesillas):
        jornada_completa = all(
            p.resultadoA not in (None, "") and p.resultadoB not in (None, "")
            for p in jornada["partidos"]
        )
        if not jornada_completa:
            jornada_activa = jornada["nombre"]
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_tordesillas:
        jornada_activa = nuevos_datos_tordesillas[-1]["nombre"]
    partidos_schema = obtener_partidos_schema(nuevos_datos_tordesillas)    
    return render_template(
        "equipos_vall/jornadas_tordesillas.html",
        nuevos_datos_tordesillas=nuevos_datos_tordesillas,
        jornada_activa=jornada_activa,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_tordesillas"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_tordesillas"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_tordesillas"
            )
        )
    )
# Jornada 0 Real Tordesillas
@tordesillas_route_bp.route("/admin/jornada0_tordesillas", methods=["GET", "POST"])
def jornada0_tordesillas():
    if request.method == "POST":
        if "equipo" in request.form:
            club = request.form["equipo"]
            if club:
                nuevo_club = TordesillasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for("tordesillas_route_bp.jornada0_tordesillas"))
    clubs = TordesillasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template("admin/clubs/clubs_tordesillas.html", clubs=clubs)
# Eliminar clubs jornada 0
@tordesillas_route_bp.route("/eliminar_club_tordesillas/<int:club_id>", methods=["POST"])
def eliminar_club_tordesillas(club_id):
    club = TordesillasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for("tordesillas_route_bp.jornada0_tordesillas"))
# Crear la clasificación Real Tordesillas
def generar_clasificacion_analisis_futbol_tordesillas(data):
    clasificacion = defaultdict(
        lambda: {
            "jugados": 0,
            "ganados": 0,
            "empatados": 0,
            "perdidos": 0,
            "favor": 0,
            "contra": 0,
            "diferencia_goles": 0,
            "puntos": 0,
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

            if r1 is None or r2 is None or r1 == "" or r2 == "":
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except ValueError:
                continue

            # ================================
            # PUNTOS LIGA
            # ================================
            if r1 > r2:

                clasificacion[local]["puntos"] += 3
                clasificacion[local]["ganados"] += 1
                clasificacion[visitante]["perdidos"] += 1

            elif r1 < r2:

                clasificacion[visitante]["puntos"] += 3
                clasificacion[visitante]["ganados"] += 1
                clasificacion[local]["perdidos"] += 1

            else:

                clasificacion[local]["puntos"] += 1
                clasificacion[visitante]["puntos"] += 1

                clasificacion[local]["empatados"] += 1
                clasificacion[visitante]["empatados"] += 1

            # ================================
            # JUGADOS
            # ================================
            clasificacion[local]["jugados"] += 1
            clasificacion[visitante]["jugados"] += 1

            # ================================
            # GOLES
            # ================================
            clasificacion[local]["favor"] += r1
            clasificacion[local]["contra"] += r2

            clasificacion[visitante]["favor"] += r2
            clasificacion[visitante]["contra"] += r1

            clasificacion[local]["diferencia_goles"] += r1 - r2
            clasificacion[visitante]["diferencia_goles"] += r2 - r1

            # ================================
            # ENFRENTAMIENTOS DIRECTOS
            # ================================
            enfrentamientos[frozenset([local, visitante])].append(
                {
                    "local": local,
                    "visitante": visitante,
                    "goles_local": r1,
                    "goles_visitante": r2,
                }
            )

    # ================================
    # AVERAGE PARTICULAR
    # ================================
    def average_particular(a, b):

        partidos = enfrentamientos.get(frozenset([a, b]), [])

        if len(partidos) < 2:
            return None

        puntos_a = 0
        puntos_b = 0
        goles_a = 0
        goles_b = 0

        for p in partidos:

            l = p["local"]
            v = p["visitante"]
            gl = p["goles_local"]
            gv = p["goles_visitante"]

            if l == a:
                goles_a += gl
                goles_b += gv
            else:
                goles_a += gv
                goles_b += gl

            if gl > gv:
                ganador = l
            elif gv > gl:
                ganador = v
            else:
                ganador = None

            if ganador == a:
                puntos_a += 3
            elif ganador == b:
                puntos_b += 3
            else:
                puntos_a += 1
                puntos_b += 1

        return {
            "puntos_a": puntos_a,
            "puntos_b": puntos_b,
            "diff_a": goles_a - goles_b,
            "diff_b": goles_b - goles_a,
        }

    # ================================
    # COMPARADOR PRO OFICIAL
    # ================================
    def comparar(a, b):

        na, da = a
        nb, db = b

        # 1. puntos
        if da["puntos"] != db["puntos"]:
            return db["puntos"] - da["puntos"]

        # 2. enfrentamiento directo
        av = average_particular(na, nb)

        if av:

            if av["puntos_a"] != av["puntos_b"]:
                return av["puntos_b"] - av["puntos_a"]

            if av["diff_a"] != av["diff_b"]:
                return av["diff_b"] - av["diff_a"]

        # 3. diferencia goles
        if da["diferencia_goles"] != db["diferencia_goles"]:
            return db["diferencia_goles"] - da["diferencia_goles"]

        # 4. goles a favor
        return db["favor"] - da["favor"]

    # ================================
    # ORDEN FINAL
    # ================================
    equipos = list(clasificacion.items())
    equipos.sort(key=cmp_to_key(comparar))

    return [{"equipo": e, "datos": d} for e, d in equipos]
# Ruta para mostrar la clasificación y análisis del Tordesillas
@tordesillas_route_bp.route("/equipos_futbol/clasif_tordesillas")
def clasif_analisis_tordesillas():
    data = obtener_datos_tordesillas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_tordesillas = (
        generar_clasificacion_analisis_futbol_tordesillas(data)
    )
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_tordesillas = TordesillasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_tordesillas:

        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_analisis_tordesillas
        ):

            clasificacion_analisis_tordesillas.append(
                {
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
                }
            )

    clasificacion_analisis_tordesillas.sort(
        key=lambda x: x["datos"]["puntos"], reverse=True
    )
    return render_template(
        "equipos_vall/clasif_tordesillas.html",
        clasificacion_analisis_tordesillas=clasificacion_analisis_tordesillas,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/clasif_tordesillas"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "tordesillas",
                "https://deportesdelaciudad.es/equipos_futbol/clasif_tordesillas"
            )
        )
    )
# TEMPORADAS REAL TODESILLAS
@tordesillas_route_bp.route("/admin/temporadas_tordesillas")
def temporadas_tordesillas():
    temporadas = TemporadaTordesillas.query.order_by(TemporadaTordesillas.id.desc()).all()
    return render_template(
        "admin/temporadas/temporada_tordesillas.html", temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@tordesillas_route_bp.route("/activar_temporada_tordesillas/<int:id>")
def activar_temporada_tordesillas(id):
    TemporadaTordesillas.query.update({"activa": False})
    temporada = TemporadaTordesillas.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.temporadas_tordesillas"))

# HISTORIAL REAL TODESILLAS
# Creación del historial de temporadas del Real Tordesillas
@tordesillas_route_bp.route("/admin/crear_historial_tordesillas", methods=["GET", "POST"])
def crear_historial_tordesillas():
    if request.method == "POST":
        historial = Historial(
            deporte="futbol",
            equipo="Atl.Tordesillas",
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
        return redirect(url_for("tordesillas_route_bp.crear_historial_tordesillas"))
    historial = (Historial.query.filter_by(
        deporte="futbol",
        equipo="Atl.Tordesillas"
    ).order_by(Historial.temporada.desc()).all()
                 )
    temporadas = TemporadaTordesillas.query.order_by(
        TemporadaTordesillas.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial.html",
        historial=historial,
        temporadas=temporadas,
        deporte="futbol",
        equipo="Atl.Tordesillas",
        crear_url="tordesillas_route_bp.crear_historial_tordesillas",
        modificar_url="tordesillas_route_bp.modificar_historial_tordesillas",
        eliminar_url="tordesillas_route_bp.eliminar_historial_tordesillas"
    )
# Eliminar historial de temporadas del Real Tordesillas
@tordesillas_route_bp.route("/admin/eliminar_historial_tordesillas/<int:id>", methods=["POST"])
def eliminar_historial_tordesillas(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.crear_historial_tordesillas"))
# Modificar historial de temporadas del Real Tordesillas
@tordesillas_route_bp.route("/admin/modificar_historial_tordesillas/<int:id>", methods=["POST"])
def modificar_historial_tordesillas(id):
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
    return redirect(url_for("tordesillas_route_bp.crear_historial_tordesillas"))
# Ver Historial de temporadas del Real Tordesillas en la página principal
@tordesillas_route_bp.route("/tordesillas/historial")
def historial_tordesillas():
    historial = (Historial.query.filter_by(
        deporte="futbol",
        equipo="Atl.Tordesillas"
    ).order_by(Historial.temporada.desc()).all())
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = TemporadaTordesillas.query.order_by(TemporadaTordesillas.id).all()
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
    titulos = (Palmaress.query.filter_by(
            deporte="futbol",
            equipo="Atl.Tordesillas"
        ).order_by(Palmaress.orden.asc(),Palmaress.temporada.desc()).all())
    palmares = OrderedDict()
    for titulo in titulos:
        if titulo.competicion not in palmares:
            palmares[titulo.competicion] = []
        palmares[titulo.competicion].append(titulo)
    labels_jornadas = []

    for i, temporada in enumerate(temporadas):

        jornadas = (
            JornadaTordesillas.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaTordesillas.id)
            .all()
        )

        if not jornadas:
            continue

        labels, puntos = obtener_evolucion_puntos(
                
            jornadas, "tordesillas", generar_clasificacion_analisis_futbol_tordesillas,"puntos"
        )
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
        

    return render_template(
        "historia/historia_tordesillas.html",
        historial=historial,
        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,
        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,
        palmares=palmares,
        deporte="Fútbol",
        equipo="Atl.Tordesillas",
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
               "tordesillas",
               "https://deportesdelaciudad.es/tordesillas/historial"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "tordesillas",
                "https://deportesdelaciudad.es/tordesillas/historial"
            )
        )
    )

# PALMARES Tordesillas
# Crear Palmares del Tordesillas
@tordesillas_route_bp.route("/admin/crear_palmares_tordesillas", methods=["GET", "POST"])
def crear_palmares_tordesillas():
    if request.method == "POST":
        titulo = Palmaress(
            deporte="futbol",
            equipo="Atl.Tordesillas",
            temporada=request.form.get("temporada"),
            competicion=request.form.get("competicion"),
            imagen=request.form.get("imagen"),
            orden=int(request.form.get("orden", 0))
        )
        db.session.add(titulo)
        db.session.commit()
        return redirect(url_for("tordesillas_route_bp.crear_palmares_tordesillas"))
    palmares = (
        Palmaress.query.filter_by(
            deporte="futbol",
            equipo="Atl.Tordesillas"
        )
        .order_by(Palmaress.orden.asc(),Palmaress.temporada.desc())
        .all()
    )
    return render_template(
        "admin/historial/palmares.html",
        palmares=palmares,
        deporte="Fútbol",
        equipo="Atl.Tordesillas",
        crear_url="tordesillas_route_bp.crear_palmares_tordesillas",
        modificar_url="tordesillas_route_bp.modificar_palmares_tordesillas",
        eliminar_url="tordesillas_route_bp.eliminar_palmares_tordesillas",
    )
# Modificar Palmares del Tordesillas
@tordesillas_route_bp.route("/admin/modificar_palmares_tordesillas/<int:id>", methods=["POST"])
def modificar_palmares_tordesillas(id):
    titulo = Palmaress.query.get_or_404(id)
    titulo.temporada = request.form.get("temporada")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    titulo.orden = request.form.get("orden")
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.crear_palmares_tordesillas"))
# Eliminar Palmares del Tordesillas
@tordesillas_route_bp.route("/admin/eliminar_palmares_tordesillas/<int:id>", methods=["POST"])
def eliminar_palmares_tordesillas(id):
    titulo = Palmaress.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.crear_palmares_tordesillas"))


# COPA DEL REY Tordesillas
# Creación de las eliminatorias de copa
@tordesillas_route_bp.route("/admin/crear_copa_tordesillas", methods=["GET", "POST"])
def crear_copa_tordesillas():
    if request.method == "POST":
        eliminatoria = request.form.get("eliminatoria")
        max_partidos = {
            "ronda1": 20,
            "ronda2": 56,
            "ronda3": 28,
            "ronda4": 16,
            "octavos": 8,
            "cuartos": 4,
            "semifinales": 4,
            "final": 1,
        }.get(eliminatoria, 0)
        num_partidos = int(request.form.get("num_partidos", "0").strip() or 0)
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaTordesillas(
                eliminatoria=eliminatoria,
                fecha=request.form.get(f"fecha{i}", ""),
                hora=request.form.get(f"hora{i}", ""),
                local=request.form.get(f"local{i}", ""),
                resultadoA=request.form.get(f"resultadoA{i}", ""),
                resultadoB=request.form.get(f"resultadoB{i}", ""),
                visitante=request.form.get(f"visitante{i}", ""),
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for("tordesillas_route_bp.ver_copa_tordesillas"))
    return render_template("admin/copa/copa_tordesillas.html")
# Ver las eliminatorias en Admin
@tordesillas_route_bp.route("/admin/copa_tordesillas/")
def ver_copa_tordesillas():
    eliminatorias = [
        "ronda1",
        "ronda2",
        "ronda3",
        "ronda4",
        "octavos",
        "cuartos",
        "semifinales",
        "final",
    ]
    datos_eliminatorias = {
        e: CopaTordesillas.query.filter_by(eliminatoria=e).all() for e in eliminatorias
    }
    return render_template(
        "admin/copa/copa_tordesillas.html", datos_eliminatorias=datos_eliminatorias
    )
# Modificar las eliminatorias
@tordesillas_route_bp.route("/modificar_copa_tordesillas_post", methods=["POST"])
def modificar_copa_tordesillas_post():
    eliminatoria = request.form["eliminatoria"]
    num_partidos = int(request.form["num_partidos"])
    for i in range(num_partidos):
        partido_id = request.form.get(f"partido_id{i}")
        partido = CopaTordesillas.query.get(partido_id)
        if partido:
            partido.eliminatoria = (
                eliminatoria  # Opcional: si quieres actualizarla por partido
            )
            partido.fecha = request.form.get(f"fecha{i}", "")
            partido.hora = request.form.get(f"hora{i}", "")
            partido.local = request.form.get(f"local{i}", "")
            partido.resultadoA = request.form.get(f"resultadoA{i}", "")
            partido.resultadoB = request.form.get(f"resultadoB{i}", "")
            partido.visitante = request.form.get(f"visitante{i}", "")
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.ver_copa_tordesillas"))
# Eliminar las eliminatorias en Admin
@tordesillas_route_bp.route("/eliminar_copa_tordesillas/<string:eliminatoria>", methods=["POST"])
def eliminar_copa_tordesillas(eliminatoria):
    CopaTordesillas.query.filter_by(eliminatoria=eliminatoria).delete()
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.ver_copa_tordesillas"))
# Ver las eliminatorias en la página principal Copa
@tordesillas_route_bp.route("/tordesillas_copa/")
def copas_tordesillas():
    eliminatorias = [
        "ronda1",
        "ronda2",
        "ronda3",
        "ronda4",
        "octavos",
        "cuartos",
        "semifinales",
        "final",
    ]
    datos_copa = {
        e: CopaTordesillas.query.filter_by(eliminatoria=e).all() for e in eliminatorias
    }
    partidos_schema = obtener_partidos_schema(eliminatorias)
    return render_template(
        "copas/tordesillas_copa.html", 
        datos_copa=datos_copa,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "tordesillas",
                "https://deportesdelaciudad.es/tordesillas_copa/"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "tordesillas",
                "https://deportesdelaciudad.es/tordesillas_copa/"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "tordesillas",
                "https://deportesdelaciudad.es/tordesillas_copa/"
            )
        )
    )

# PLAYOFF ASCENSO REAL VALLADOLID
# Crear formulario para los playoff
@tordesillas_route_bp.route("/admin/crear_playoff_tordesillas", methods=["GET", "POST"])
def crear_playoff_tordesillas():
    if request.method == "POST":
        eliminatoria = request.form.get("eliminatoria")
        max_partidos = {"semifinales": 4, "final": 2}.get(eliminatoria, 0)
        num_partidos_str = request.form.get("num_partidos", "0").strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = PlayoffTordesillas(
                eliminatoria=eliminatoria,
                fecha=request.form.get(f"fecha{i}", ""),
                hora=request.form.get(f"hora{i}", ""),
                local=request.form.get(f"local{i}", ""),
                resultadoA=request.form.get(f"resultadoA{i}", ""),
                resultadoB=request.form.get(f"resultadoB{i}", ""),
                visitante=request.form.get(f"visitante{i}", ""),
            )
            PlayoffTordesillas.query.filter_by(eliminatoria=eliminatoria).delete()
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for("tordesillas_route_bp.ver_playoff_tordesillas"))
    return render_template("admin/playoffs/playoff_tordesillas.html")
# Ver encuentros playoff en Admin
@tordesillas_route_bp.route("/admin/playoff_tordesillas/")
def ver_playoff_tordesillas():
    eliminatorias = ["semifinales", "final"]
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = (
            PlayoffTordesillas.query.filter_by(eliminatoria=eliminatoria)
            .order_by(PlayoffTordesillas.orden)
            .all()
        )
        datos_playoff[eliminatoria] = partidos
    return render_template(
        "admin/playoffs/playoff_tordesillas.html", datos_playoff=datos_playoff
    )
# Modificar los partidos de los playoff
@tordesillas_route_bp.route(
    "/modificar_playoff_tordesillas/<string:eliminatoria>", methods=["GET", "POST"]
)
def modificar_playoff_tordesillas(eliminatoria):
    if request.method == "POST":
        num_partidos = int(request.form.get("num_partidos", 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f"partido_id{i}")
            if not partido_id:
                continue
            partido_obj = PlayoffTordesillas.query.get(int(partido_id))
            if not partido_obj:
                continue
            partido_obj.fecha = request.form.get(f"fecha{i}", "")
            partido_obj.hora = request.form.get(f"hora{i}", "")
            partido_obj.local = request.form.get(f"local{i}", "")
            partido_obj.resultadoA = request.form.get(f"resultadoA{i}", "")
            partido_obj.resultadoB = request.form.get(f"resultadoB{i}", "")
            partido_obj.visitante = request.form.get(f"visitante{i}", "")
            partido_obj.orden = i
        # Commit para guardar los cambios
        db.session.commit()
        return redirect(url_for("tordesillas_route_bp.ver_playoff_tordesillas"))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for("tordesillas_route_bp.ver_playoff_tordesillas"))
# Eliminar los partidos de los playoff
@tordesillas_route_bp.route("/eliminar_playoff_tordesillas/<string:eliminatoria>", methods=["POST"])
def eliminar_playoff_tordesillas(eliminatoria):
    partidos = PlayoffTordesillas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    return redirect(url_for("tordesillas_route_bp.ver_playoff_tordesillas"))
# Mostrar los playoffs del Real Valladolid
@tordesillas_route_bp.route("/playoffs_tordesillas/")
def playoffs_tordesillas():
    eliminatorias = ["semifinales", "final"]
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffTordesillas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos
    partidos_schema = obtener_partidos_schema(eliminatorias)    
    return render_template(
        "playoff/tordesillas_playoff.html", 
        datos_playoff=datos_playoff,
        breadcrumb=jsonld(
           schema_breadcrumb_equipo("tordesillas")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "tordesillas",
                "https://deportesdelaciudad.es/playoffs_tordesillas"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "tordesillas",
                "https://deportesdelaciudad.es/playoffs_tordesillas"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "tordesillas",
                "https://deportesdelaciudad.es/playoffs_tordesillas"
            )
        )
    )
