from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from collections import OrderedDict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app.seo.schema import jsonld, obtener_partidos_schema, schema_breadcrumb_equipo, schema_partidos, schema_sports_competition, schema_sports_team
from ..models.historial import obtener_evolucion_puntos
from ..models.historial import Historial, Palmaress
from ..models.rv_fem import (
    JornadaSimancas,
    SimancasPartido,
    SimancasClub,
    CopaSimancas,
    PlayoffSimancas,
    TemporadaSimancas,
)

rv_fem_route_bp = Blueprint("rv_fem_route_bp", __name__)

# LIGA RV FEMENINO
# Crear el calendario RV FEMENINO
@rv_fem_route_bp.route("/admin/crear_calendario_rv_fem", methods=["GET", "POST"])
def ingresar_resultado_rv_fem():
    if request.method == "POST":
        temporada_nombre = request.form["temporada"]
        nombre_jornada = request.form["nombre"]
        num_partidos = int(request.form["num_partidos"])
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaSimancas.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaSimancas(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaSimancas(nombre=nombre_jornada, temporada_id=temporada.id)
        db.session.add(jornada)
        db.session.flush()
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            partido = SimancasPartido(
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
        return redirect(url_for("rv_fem_route_bp.calendarios_rv_fem"))
    # Si es un GET, renderizamos el formulario de creación
    return render_template("admin/calendarios/calend_rv_fem.html")
# Ver calendario Real Valladolid en Admin
@rv_fem_route_bp.route("/admin/calendario_rv_fem")
def calendarios_rv_fem():
    temporada = TemporadaSimancas.query.filter_by(activa=True).first()
    if temporada:
        jornadas = (
            JornadaSimancas.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaSimancas.id.asc())
            .all()
        )
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = (
            db.session.query(SimancasPartido)
            .filter_by(jornada_id=jornada.id)
            .order_by(SimancasPartido.orden.asc())
            .all()
        )
    return render_template("admin/calendarios/calend_rv_fem.html", jornadas=jornadas)
# Modificar jornada
@rv_fem_route_bp.route("/modificar_jornada_rv_fem/<int:id>", methods=["GET", "POST"])
def modificar_jornada_rv_fem(id):
    jornada = db.session.query(JornadaSimancas).filter(JornadaSimancas.id == id).first()
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
                    db.session.query(SimancasPartido)
                    .filter(SimancasPartido.id == partido_id)
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
            return redirect(url_for("rv_fem_route_bp.calendarios_rv_fem"))
    return render_template("admin/calendarios/calend_rv_fem.html", jornada=jornada)
# Eliminar jornada
@rv_fem_route_bp.route("/eliminar_jornada_rv_fem/<int:id>", methods=["GET", "POST"])
def eliminar_jornada_rv_fem(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaSimancas).filter(JornadaSimancas.id == id).first()
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(SimancasPartido).filter(
            SimancasPartido.jornada_id == id
        ).delete()
        # Eliminar la jornada
        db.session.delete(jornada)
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for("rv_fem_route_bp.calendarios_rv_fem"))
# Obtener datos RV FEMENINO
def obtener_datos_rv_fem(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaSimancas.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaSimancas.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            SimancasPartido.query.filter_by(jornada_id=jornada.id)
            .order_by(SimancasPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({"nombre": jornada.nombre, "partidos": partidos})
    return jornadas_con_partidos
# Calendario RV FEMRNINO
@rv_fem_route_bp.route("/equipos_futbol/calendario_rv_fem")
def calendario_rv_fem():
    datos = obtener_datos_rv_fem()
    equipo_rv_fem = "RV Femenino"
    tabla_partidos_rv_fem = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada["partidos"]:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_rv_fem or equipo_visitante == equipo_rv_fem:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_rv_fem:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_rv_fem = "C"
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_rv_fem = "F"
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_rv_fem:
                    tabla_partidos_rv_fem[equipo_contrario] = {"jornadas": {}}
                # Verificamos si es el primer o segundo enfrentamiento
                if (
                    "primer_enfrentamiento"
                    not in tabla_partidos_rv_fem[equipo_contrario]
                ):
                    tabla_partidos_rv_fem[equipo_contrario][
                        "primer_enfrentamiento"
                    ] = jornada["nombre"]
                    tabla_partidos_rv_fem[equipo_contrario][
                        "resultadoA"
                    ] = resultado_a
                    tabla_partidos_rv_fem[equipo_contrario][
                        "resultadoB"
                    ] = resultado_b
                elif (
                    "segundo_enfrentamiento"
                    not in tabla_partidos_rv_fem[equipo_contrario]
                ):
                    tabla_partidos_rv_fem[equipo_contrario][
                        "segundo_enfrentamiento"
                    ] = jornada["nombre"]
                    tabla_partidos_rv_fem[equipo_contrario][
                        "resultadoAA"
                    ] = resultado_a
                    tabla_partidos_rv_fem[equipo_contrario][
                        "resultadoBB"
                    ] = resultado_b
                # Agregamos la jornada y resultados
                if (
                    jornada["nombre"]
                    not in tabla_partidos_rv_fem[equipo_contrario]["jornadas"]
                ):
                    tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ] = {
                        "resultadoA": resultado_a,
                        "resultadoB": resultado_b,
                        "rol_rv_fem": rol_rv_fem,
                    }
                # Asignamos los resultados según el rol del RV FEMENINO
                if (
                    equipo_local == equipo_contrario
                    or equipo_visitante == equipo_contrario
                ):
                    if not tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoA"]:
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoA"] = resultado_a
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoB"] = resultado_b
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_rv_fem"] = rol_rv_fem
                    else:
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_rv_fem"] = rol_rv_fem
                else:
                    if not tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoAA"]:
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_rv_fem"] = rol_rv_fem
                    else:
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_rv_fem[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_rv_fem"] = rol_rv_fem
    partidos_schema = obtener_partidos_schema(datos)                    
    return render_template(
        "equipos_vall/calendario_rv_fem.html",
        tabla_partidos_rv_fem=tabla_partidos_rv_fem,
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(
            schema_sports_team(
                "rv_fem",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_rv_fem",
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "rv_fem",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_rv_fem"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "uemc",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_rv_fem"
            )
        )
    )
# Jornadas RV FEMENINO
@rv_fem_route_bp.route("/equipos_futbol/resultados_rv_fem")
def resultados_rv_fem():
    datos = obtener_datos_rv_fem()
    nuevos_datos_rv_fem = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_rv_fem):
        jornada_completa = all(
            p.resultadoA not in (None, "") and p.resultadoB not in (None, "")
            for p in jornada["partidos"]
        )
        if not jornada_completa:
            jornada_activa = jornada["nombre"]
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_rv_fem:
        jornada_activa = nuevos_datos_rv_fem[-1]["nombre"]
    partidos_schema = obtener_partidos_schema(nuevos_datos_rv_fem)    
    return render_template(
        "equipos_vall/jornadas_rv_fem.html",
        nuevos_datos_rv_fem=nuevos_datos_rv_fem,
        jornada_activa=jornada_activa,
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(
            schema_sports_team(
                "rv_fem",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_rv_fem",
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "rv_fem",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_rv_fem"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "uemc",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_rv_frm"
            )
        )
    )
# Jornada 0 RV FEMENINO
@rv_fem_route_bp.route("/admin/jornada0_rv_fem", methods=["GET", "POST"])
def jornada0_rv_fem():
    if request.method == "POST":
        if "equipo" in request.form:
            club = request.form["equipo"]
            if club:
                nuevo_club = SimancasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for("rv_fem_route_bp.jornada0_rv_fem"))
    clubs = SimancasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template("admin/clubs/clubs_rv_fem.html", clubs=clubs)
# Eliminar clubs jornada 0
@rv_fem_route_bp.route("/eliminar_club_rv_fem/<int:club_id>", methods=["POST"])
def eliminar_club_rv_fem(club_id):
    club = SimancasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for("rv_fem_route_bp.jornada0_rv_fem"))
# Crear la clasificación RV FEMENINO
def generar_clasificacion_analisis_futbol_rv_fem(data):
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
# Ruta para mostrar la clasificación y análisis del UEMC
@rv_fem_route_bp.route("/equipos_futbol/clasif_rv_fem")
def clasif_analisis_rv_fem():
    data = obtener_datos_rv_fem()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_rv_fem = generar_clasificacion_analisis_futbol_rv_fem(
        data
    )
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_rv_fem = SimancasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_rv_fem:

        if not any(
            equipo["equipo"] == club.nombre
            for equipo in clasificacion_analisis_rv_fem
        ):

            clasificacion_analisis_rv_fem.append(
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

    clasificacion_analisis_rv_fem.sort(
        key=lambda x: x["datos"]["puntos"], reverse=True
    )
    return render_template(
        "equipos_vall/clasif_rv_fem.html",
        clasificacion_analisis_rv_fem=clasificacion_analisis_rv_fem,
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(
            schema_sports_team(
                "rv_fem", "https://deportesdelaciudad.es/equipos_futbol/clasif_rv_fem"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "rv_fem",
                "https://deportesdelaciudad.es/equipos_futbol/clasif_rv_fem"
            )
        )
    )
# TEMPORADAS RV Promesas
@rv_fem_route_bp.route("/admin/temporadas_rv_fem")
def temporadas_rv_fem():
    temporadas = TemporadaSimancas.query.order_by(TemporadaSimancas.id.desc()).all()
    return render_template(
        "admin/temporadas/temporada_rv_fem.html", temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@rv_fem_route_bp.route("/activar_temporada_rv_fem/<int:id>")
def activar_temporada_rv_fem(id):
    TemporadaSimancas.query.update({"activa": False})
    temporada = TemporadaSimancas.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for("rv_fem_route_bp.temporadas_rv_fem"))

# HISTORIAL RV FEMENINO
# Creación del historial de temporadas del RV Femenino
@rv_fem_route_bp.route("/admin/crear_historial_rv_fem", methods=["GET", "POST"])
def crear_historial_rv_fem():
    if request.method == "POST":
        historial = Historial(
            deporte="futbol",
            equipo="RV Femenino",
            temporada=request.form.get("temporada"),
            liga=request.form.get("liga"),
            puntos=request.form.get("puntos"),
            puesto=request.form.get("puesto"),
            playoff=request.form.get("playoff"),
            copa=request.form.get("copa"),
            titulos=request.form.get("titulos"),
            siguiente_temporada=request.form.get("siguiente_temporada"),
            observaciones=request.form.get("observaciones"),
        )
        db.session.add(historial)
        db.session.commit()
        return redirect(url_for("rv_fem_route_bp.crear_historial_rv_fem"))
    historial = (
        Historial.query.filter_by(deporte="futbol", equipo="RV Femenino")
        .order_by(Historial.temporada.desc())
        .all()
    )
    temporadas = TemporadaSimancas.query.order_by(TemporadaSimancas.nombre.desc()).all()
    return render_template(
        "admin/historial/historial.html",
        historial=historial,
        temporadas=temporadas,
        deporte="futbol",
        equipo="RV Femenino",
        crear_url="rv_fem_route_bp.crear_historial_rv_fem",
        modificar_url="rv_fem_route_bp.modificar_historial_rv_fem",
        eliminar_url="rv_fem_route_bp.eliminar_historial_rv_fem",
    )
@rv_fem_route_bp.route("/admin/eliminar_historial_rv_fem/<int:id>", methods=["POST"])
def eliminar_historial_rv_fem(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("rv_fem_route_bp.crear_historial_rv_fem"))
@rv_fem_route_bp.route("/admin/modificar_historial_rv_fem/<int:id>", methods=["POST"])
def modificar_historial_rv_fem(id):
    historial = Historial.query.get_or_404(id)
    historial.temporada = request.form.get("temporada")
    historial.liga = request.form.get("liga")
    historial.puntos = request.form.get("puntos")
    historial.puesto = request.form.get("puesto")
    historial.playoff = request.form.get("playoff")
    historial.copa = request.form.get("copa")
    historial.siguiente_temporada = request.form.get("siguiente_temporada")
    historial.titulos = request.form.get("titulos")
    historial.observaciones = request.form.get("observaciones")
    db.session.commit()
    return redirect(url_for("rv_fem_route_bp.crear_historial_rv_fem"))
# Ver Historial de temporadas del RV Femenino en la página principal
@rv_fem_route_bp.route("/rv_fem/historial")
def historial_promesas():
    historial = (
        Historial.query.filter_by(deporte="futbol", equipo="RV Femenino")
        .order_by(Historial.temporada.desc())
        .all()
    )
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = TemporadaSimancas.query.order_by(TemporadaSimancas.id).all()
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
    titulos = (
        Palmaress.query.filter_by(deporte="futbol", equipo="RV Femenino")
        .order_by(Palmaress.orden.asc(), Palmaress.temporada.desc())
        .all()
    )
    palmares = OrderedDict()
    for titulo in titulos:
        if titulo.competicion not in palmares:
            palmares[titulo.competicion] = []
        palmares[titulo.competicion].append(titulo)

    labels_jornadas = []

    for i, temporada in enumerate(temporadas):

        jornadas = (
            JornadaSimancas.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaSimancas.id)
            .all()
        )

        if not jornadas:
            continue

        labels, puntos = obtener_evolucion_puntos(
            jornadas,
            "RV Femenino",
            generar_clasificacion_analisis_futbol_rv_fem,
            "puntos",
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
        "historia/historia_rv_fem.html",
        historial=historial,
        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,
        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,
        palmares=palmares,
        deporte="Fútbol",
        equipo="RV Femennino",
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(
            schema_sports_team(
                "rv_fem", "https://deportesdelaciudad.es/rv_fem/historial"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "rv_fem",
                "https://deportesdelaciudad.es/rv_fem/historial"
            )
        )
    )

# PALMARES RV FEMENINO
# Crear Palmares del RV Femenino
@rv_fem_route_bp.route("/admin/crear_palmares_rv_fem", methods=["GET", "POST"])
def crear_palmares_rv_fem():
    if request.method == "POST":
        titulo = Palmaress(
            deporte="futbol",
            equipo="RV Femenino",
            temporada=request.form.get("temporada"),
            competicion=request.form.get("competicion"),
            imagen=request.form.get("imagen"),
            orden=int(request.form.get("orden", 0)),
        )
        db.session.add(titulo)
        db.session.commit()
        return redirect(url_for("rv_fem_route_bp.crear_palmares_rv_fem"))
    palmares = (
        Palmaress.query.filter_by(deporte="futbol", equipo="RV Femenino")
        .order_by(Palmaress.orden.asc(), Palmaress.temporada.desc())
        .all()
    )
    return render_template(
        "admin/historial/palmares.html",
        palmares=palmares,
        deporte="Fútbol",
        equipo="RV Femenino",
        crear_url="rv_fem_route_bp.crear_palmares_rv_fem",
        modificar_url="rv_fem_route_bp.modificar_palmares_rv_fem",
        eliminar_url="rv_fem_route_bp.eliminar_palmares_rv_fem",
    )
# Modificar Palmares del RV Femenino
@rv_fem_route_bp.route("/admin/modificar_palmares_rv_fem/<int:id>", methods=["POST"])
def modificar_palmares_rv_fem(id):
    titulo = Palmaress.query.get_or_404(id)
    titulo.temporada = request.form.get("temporada")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    titulo.orden = request.form.get("orden")
    db.session.commit()
    return redirect(url_for("rv_fem_route_bp.crear_palmares_rv_fem"))
# Eliminar Palmares del RV Promesas
@rv_fem_route_bp.route("/admin/eliminar_palmares_rv_fem/<int:id>", methods=["POST"])
def eliminar_palmares_rv_fem(id):
    titulo = Palmaress.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("rv_fem_route_bp.crear_palmares_rv_fem"))

# COPA DEL REY RV FEMENINO
# Creación de las eliminatorias de copa
@rv_fem_route_bp.route("/admin/crear_copa_rv_fem", methods=["GET", "POST"])
def crear_copa_rv_fem():
    if request.method == "POST":
        eliminatoria = request.form.get("eliminatoria")
        max_partidos = {
            "ronda1": 16,
            "ronda2": 8,
            "ronda3": 8,
            "octavos": 8,
            "cuartos": 4,
            "semifinales": 4,
            "final": 1,
        }.get(eliminatoria, 0)
        num_partidos = int(request.form.get("num_partidos", "0").strip() or 0)
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaSimancas(
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
        return redirect(url_for("rv_fem_route_bp.ver_copa_rv_fem"))
    return render_template("admin/copa/copa_rv_fem.html")
# Ver las eliminatorias en Admin
@rv_fem_route_bp.route("/admin/copa_rv_fem/")
def ver_copa_rv_fem():
    eliminatorias = [
        "ronda1",
        "ronda2",
        "ronda3",
        "octavos",
        "cuartos",
        "semifinales",
        "final",
    ]
    datos_eliminatorias = {
        e: CopaSimancas.query.filter_by(eliminatoria=e).all() for e in eliminatorias
    }
    return render_template(
        "admin/copa/copa_rv_fem.html", datos_eliminatorias=datos_eliminatorias
    )
# Modificar las eliminatorias
@rv_fem_route_bp.route("/modificar_copa_rv_fem_post", methods=["POST"])
def modificar_copa_rv_fem_post():
    eliminatoria = request.form["eliminatoria"]
    num_partidos = int(request.form["num_partidos"])
    for i in range(num_partidos):
        partido_id = request.form.get(f"partido_id{i}")
        partido = CopaSimancas.query.get(partido_id)
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
    return redirect(url_for("rv_fem_route_bp.ver_copa_rv_fem"))
# Eliminar las eliminatorias en Admin
@rv_fem_route_bp.route("/eliminar_copa_rv_fem/<string:eliminatoria>", methods=["POST"])
def eliminar_copa_rv_fem(eliminatoria):
    CopaSimancas.query.filter_by(eliminatoria=eliminatoria).delete()
    db.session.commit()
    return redirect(url_for("rv_fem_route_bp.ver_copa_rv_fem"))
# Ver las eliminatorias en la página principal Copa
@rv_fem_route_bp.route("/rv_fem_copa/")
def copas_rv_fem():
    eliminatorias = [
        "ronda1",
        "ronda2",
        "ronda3",
        "octavos",
        "cuartos",
        "semifinales",
        "final",
    ]
    datos_copa = {
        e: CopaSimancas.query.filter_by(eliminatoria=e).all() for e in eliminatorias
    }
    partidos_schema = obtener_partidos_schema(eliminatorias)
    return render_template(
        "copas/rv_fem_copa.html",
        datos_copa=datos_copa,
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(
            schema_sports_team(
                "rv_fem", "https://deportesdelaciudad.es/rv_fem_copa"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "rv_fem",
                "https://deportesdelaciudad.es/rv_fem_copa/"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "rv_fem",
                "https://deportesdelaciudad.es/rv_fem_copa/"
            )
        )
    )

# PLAYOFF ASCENSO RV FEMENINO
# Crear formulario para los playoff
@rv_fem_route_bp.route("/admin/crear_playoff_rv_fem", methods=["GET", "POST"])
def crear_playoff_rv_fem():
    if request.method == "POST":
        eliminatoria = request.form.get("eliminatoria")
        max_partidos = {"cuartos": 8, "semifinales": 4, "final": 2}.get(eliminatoria, 0)
        num_partidos_str = request.form.get("num_partidos", "0").strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        # 🧹 Eliminar partidos ANTES de agregar nuevos
        PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).delete()

        for i in range(num_partidos):
            partido = PlayoffSimancas(
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
        return redirect(url_for("rv_fem_route_bp.ver_playoff_rv_fem"))
    return render_template("admin/playoffs/playoff_rv_fem.html")
# Ver encuentros playoff en Admin
@rv_fem_route_bp.route("/admin/playoff_rv_fem/")
def ver_playoff_rv_fem():
    eliminatorias = ["cuartos", "semifinales", "final"]
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = (
            PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria)
            .order_by(PlayoffSimancas.orden)
            .all()
        )
        datos_playoff[eliminatoria] = partidos
    return render_template(
        "admin/playoffs/playoff_rv_fem.html", datos_playoff=datos_playoff
    )
# Modificar los partidos de los playoff
@rv_fem_route_bp.route("/modificar_playoff_rv_fem/<string:eliminatoria>", methods=["GET", "POST"])
def modificar_playoff_rv_fem(eliminatoria):
    if request.method == "POST":
        num_partidos = int(request.form.get("num_partidos", 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f"partido_id{i}")
            if not partido_id:
                continue
            partido_obj = PlayoffSimancas.query.get(int(partido_id))
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
        flash("Playoff actualizado correctamente", "success")
        return redirect(url_for("rv_fem_route_bp.ver_playoff_rv_fem"))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for("rv_fem_route_bp.ver_playoff_rv_fem"))
# Eliminar los partidos de los playoff
@rv_fem_route_bp.route(
    "/eliminar_playoff_rv_fem/<string:eliminatoria>", methods=["POST"]
)
def eliminar_playoff_rv_fem(eliminatoria):
    partidos = PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f"Eliminatoria {eliminatoria} eliminada correctamente", "success")
    return redirect(url_for("rv_fem_route_bp.ver_playoff_rv_fem"))
# Mostrar los playoffs del RV FEMENINO
@rv_fem_route_bp.route("/playoffs_rv_fem/")
def playoffs_rv_fem():
    eliminatorias = ["cuartos", "semifinales", "final"]
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos
    partidos_schema = obtener_partidos_schema(eliminatorias)    
    return render_template(
        "playoff/rv_fem_playoff.html",
        datos_playoff=datos_playoff,
        breadcrumb=jsonld(schema_breadcrumb_equipo("rv_fem")),
        schema_team=jsonld(
            schema_sports_team("rv_fem", "https://deportesdelaciudad.es/playoffs_rv_fem")
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "rv_fem",
                "https://deportesdelaciudad.es/playoffs_rv_fem"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "rv_fem",
                "https://deportesdelaciudad.es/playoffs_rv_fem"
            )
        )
    )
