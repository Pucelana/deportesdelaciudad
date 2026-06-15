from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from functools import cmp_to_key
from itertools import groupby
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.san_jose import JornadaJose, JosePartido, JoseClub, PlayoffJose, CopaJose, EuropaJose, Clasificacion

san_jose_route_bp = Blueprint('san_jose_route_bp', __name__)
#EQUIPOS VOLEIBOL
#Todo el proceso de calendario y clasificación del CD San Jose
# Ingresar los resultados de los partidos de CD San Jose
@san_jose_route_bp.route("/crear_calendario_san_jose", methods=["POST"])
def ingresar_resultado_san_jose():
    if request.method == "POST":
        nombre_jornada = request.form["nombre"]
        num_partidos = int(request.form["num_partidos"])
        jornada = JornadaJose(nombre=nombre_jornada)
        db.session.add(jornada)
        db.session.flush()
        for i in range(num_partidos):
            fecha = request.form[f"fecha{i}"]
            hora = request.form[f"hora{i}"]
            local = request.form[f"local{i}"]
            resultadoA = request.form[f"resultadoA{i}"]
            puntosA = request.form[f"puntosA{i}"]
            puntosB = request.form[f"puntosB{i}"]
            resultadoB = request.form[f"resultadoB{i}"]
            visitante = request.form[f"visitante{i}"]
            partido = JosePartido(
                jornada_id=jornada.id,
                fecha=fecha,
                hora=hora,
                local=local,
                resultadoA=resultadoA,
                puntosA=puntosA,
                puntosB=puntosB,
                resultadoB=resultadoB,
                visitante=visitante,
            )
            db.session.add(partido)
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for("san_jose_route_bp.calendarios_san_jose"))
    # Si es un GET, renderizamos el formulario de creación
    return render_template("admin/calendarios/calend_san_jose.html")
# Partidos Univ. Valladolid VCV
@san_jose_route_bp.route("/calendario_san_jose")
def calendarios_san_jose():
    jornadas = JornadaJose.query.order_by(JornadaJose.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = (
            db.session.query(JosePartido)
            .filter_by(jornada_id=jornada.id)
            .order_by(JosePartido.orden.asc())
            .all()
        )
    return render_template("admin/calendarios/calend_san_jose.html", jornadas=jornadas)
# Modificar los partidos de cada jornada
@san_jose_route_bp.route("/modificar_jornada_san_jose/<string:id>", methods=["POST"])
def modificar_jornada_san_jose(id):
    jornada = db.session.query(JornadaJose).filter(JornadaJose.id == id).first()
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
                puntosA = request.form[f"puntosA{i}"]
                puntosB = request.form[f"puntosB{i}"]
                resultadoB = request.form[f"resultadoB{i}"]
                visitante = request.form[f"visitante{i}"]
                # Obtener el partido correspondiente por ID
                partido = (
                    db.session.query(JosePartido)
                    .filter(JosePartido.id == partido_id)
                    .first()
                )
                if partido:
                    partido.fecha = fecha
                    partido.hora = hora
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.puntosA = puntosA
                    partido.puntosB = puntosB
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante
                    orden = int(
                        request.form.get(f"orden{i}", i)
                    )  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for("san_jose_route_bp.calendarios_san_jose"))
    return render_template("admin/calendarios/calend_san_jose.html", jornada=jornada)
# Ruta para borrar jornadas
@san_jose_route_bp.route("/eliminar_jorn_san_jose/<string:id>", methods=["POST"])
def eliminar_jornada_san_jose(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaJose).filter(JornadaJose.id == id).first()
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(JosePartido).filter(JosePartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for("san_jose_route_bp.calendarios_san_jose"))
def obtener_datos_san_jose():
    # Obtener todas las jornadas VCV
    jornadas = JornadaJose.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = (
            db.session.query(JosePartido)
            .filter_by(jornada_id=jornada.id)
            .order_by(JosePartido.orden.asc())
            .all()
        )
        jornada_con_partidos = {"nombre": jornada.nombre, "partidos": partidos}
        jornadas_con_partidos.append(jornada_con_partidos)
    return jornadas_con_partidos
# Ruta y creación del calendario individual del CD San Jose
@san_jose_route_bp.route("/equipos_voley/calendario_san_jose")
def calendario_san_jose():
    datos = obtener_datos_san_jose()
    equipo_san_jose = "CD San Jose Rojo"
    tabla_partidos_san_jose = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada["partidos"]:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB
            # Verificamos si el Caja está jugando
            if equipo_local == equipo_san_jose or equipo_visitante == equipo_san_jose:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_san_jose:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_san_jose = "C"
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_san_jose = "F"
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_san_jose:
                    tabla_partidos_san_jose[equipo_contrario] = {"jornadas": {}}
                # Verificamos si es el primer o segundo enfrentamiento
                if "primer_enfrentamiento" not in tabla_partidos_san_jose[equipo_contrario]:
                    tabla_partidos_san_jose[equipo_contrario]["primer_enfrentamiento"] = (
                        jornada["nombre"]
                    )
                    tabla_partidos_san_jose[equipo_contrario]["resultadoA"] = resultado_a
                    tabla_partidos_san_jose[equipo_contrario]["resultadoB"] = resultado_b
                elif (
                    "segundo_enfrentamiento" not in tabla_partidos_san_jose[equipo_contrario]
                ):
                    tabla_partidos_san_jose[equipo_contrario]["segundo_enfrentamiento"] = (
                        jornada["nombre"]
                    )
                    tabla_partidos_san_jose[equipo_contrario]["resultadoAA"] = resultado_a
                    tabla_partidos_san_jose[equipo_contrario]["resultadoBB"] = resultado_b
                # Agregamos la jornada y resultados
                if (
                    jornada["nombre"]
                    not in tabla_partidos_san_jose[equipo_contrario]["jornadas"]
                ):
                    tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ] = {
                        "resultadoA": resultado_a,
                        "resultadoB": resultado_b,
                        "rol_san_jose": rol_san_jose,
                    }
                # Asignamos los resultados según el rol del CD San Jose
                if (
                    equipo_local == equipo_contrario
                    or equipo_visitante == equipo_contrario
                ):
                    if not tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoA"]:
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoA"] = resultado_a
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoB"] = resultado_b
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_san_jose"] = rol_san_jose
                    else:
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_san_jose"] = rol_san_jose
                else:
                    if not tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoAA"]:
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_san_jose"] = rol_san_jose
                    else:
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_san_jose[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_san_jose"] = rol_san_jose
    return render_template(
        "equipos_vall/calendario_san_jose.html", tabla_partidos_san_jose=tabla_partidos_san_jose
    )
# Jornadas VCV
@san_jose_route_bp.route("/equipos_voley/resultados_san_jose")
def resultados_san_jose():
    datos = obtener_datos_san_jose()
    nuevos_datos_san_jose = [dato for dato in datos if dato]
    for jornada in reversed(nuevos_datos_san_jose):
        if any(
            p.resultadoA is not None
            and p.resultadoA != ""
            and p.resultadoB is not None
            and p.resultadoB != ""
            for p in jornada["partidos"]
        ):
            jornada_activa = jornada["nombre"]
            break

    return render_template(
        "equipos_vall/jornadas_san_jose.html",
        nuevos_datos_san_jose=nuevos_datos_san_jose,
        jornada_activa=jornada_activa,
    )
# Crear la clasificación de Univ. Valladolid VCV
def generar_clasificacion_analisis_voley_san_jose(data):
    clasificacion = defaultdict(
        lambda: {
            "puntos": 0,
            "jugados": 0,
            "ganados3": 0,
            "ganados2": 0,
            "perdidos1": 0,
            "perdidos0": 0,
            "favor": 0,
            "contra": 0,
            "pf": 0,
            "pc": 0,
            "diferencia_puntos": 0,
            "diferencia_sets": 0,
        }
    )

    enfrentamientos = defaultdict(list)
    # RECORRER PARTIDOS
    for jornada in data:

        for partido in jornada["partidos"]:

            equipo_local = partido.local
            equipo_visitante = partido.visitante

            try:
                resultado_local = int(partido.resultadoA)
                resultado_visitante = int(partido.resultadoB)

                ptsA = int(partido.puntosA)
                ptsB = int(partido.puntosB)

            except (ValueError, TypeError):
                continue

            clasificacion[equipo_local]["jugados"] += 1
            clasificacion[equipo_visitante]["jugados"] += 1

            clasificacion[equipo_local]["favor"] += resultado_local
            clasificacion[equipo_local]["contra"] += resultado_visitante

            clasificacion[equipo_visitante]["favor"] += resultado_visitante
            clasificacion[equipo_visitante]["contra"] += resultado_local

            clasificacion[equipo_local]["pf"] += ptsA
            clasificacion[equipo_local]["pc"] += ptsB

            clasificacion[equipo_visitante]["pf"] += ptsB
            clasificacion[equipo_visitante]["pc"] += ptsA

            # Puntos de liga

            if resultado_local > resultado_visitante:

                if resultado_local == 3 and resultado_visitante <= 1:

                    clasificacion[equipo_local]["puntos"] += 3
                    clasificacion[equipo_local]["ganados3"] += 1
                    clasificacion[equipo_visitante]["perdidos0"] += 1

                else:

                    clasificacion[equipo_local]["puntos"] += 2
                    clasificacion[equipo_local]["ganados2"] += 1

                    clasificacion[equipo_visitante]["puntos"] += 1
                    clasificacion[equipo_visitante]["perdidos1"] += 1

            else:

                if resultado_visitante == 3 and resultado_local <= 1:

                    clasificacion[equipo_visitante]["puntos"] += 3
                    clasificacion[equipo_visitante]["ganados3"] += 1
                    clasificacion[equipo_local]["perdidos0"] += 1

                else:

                    clasificacion[equipo_visitante]["puntos"] += 2
                    clasificacion[equipo_visitante]["ganados2"] += 1

                    clasificacion[equipo_local]["puntos"] += 1
                    clasificacion[equipo_local]["perdidos1"] += 1

            clasificacion[equipo_local]["diferencia_sets"] = (
                clasificacion[equipo_local]["favor"]
                - clasificacion[equipo_local]["contra"]
            )

            clasificacion[equipo_visitante]["diferencia_sets"] = (
                clasificacion[equipo_visitante]["favor"]
                - clasificacion[equipo_visitante]["contra"]
            )

            clasificacion[equipo_local]["diferencia_puntos"] = (
                clasificacion[equipo_local]["pf"]
                - clasificacion[equipo_local]["pc"]
            )

            clasificacion[equipo_visitante]["diferencia_puntos"] = (
                clasificacion[equipo_visitante]["pf"]
                - clasificacion[equipo_visitante]["pc"]
            )

            enfrentamientos[frozenset([equipo_local, equipo_visitante])].append(
                {
                    "local": equipo_local,
                    "visitante": equipo_visitante,
                    "sets_local": resultado_local,
                    "sets_visitante": resultado_visitante,
                }
            )

    # ==========================================
    # ENFRENTAMIENTO DIRECTO
    # ==========================================

    def average_particular(a, b):

        partidos = enfrentamientos.get(frozenset([a, b]), [])

        if len(partidos) < 2:
            return None

        puntos_a = 0
        puntos_b = 0

        sets_a = 0
        sets_b = 0

        for p in partidos:

            sl = p["sets_local"]
            sv = p["sets_visitante"]

            if p["local"] == a:

                sets_a += sl
                sets_b += sv

                if sl > sv:

                    if sl == 3 and sv <= 1:
                        puntos_a += 3
                    else:
                        puntos_a += 2
                        puntos_b += 1

                else:

                    if sv == 3 and sl <= 1:
                        puntos_b += 3
                    else:
                        puntos_b += 2
                        puntos_a += 1

            else:

                sets_a += sv
                sets_b += sl

                if sv > sl:

                    if sv == 3 and sl <= 1:
                        puntos_a += 3
                    else:
                        puntos_a += 2
                        puntos_b += 1

                else:

                    if sl == 3 and sv <= 1:
                        puntos_b += 3
                    else:
                        puntos_b += 2
                        puntos_a += 1

        return {
            "puntos_a": puntos_a,
            "puntos_b": puntos_b,
            "sets_a": sets_a,
            "sets_b": sets_b,
        }

    # ==========================================
    # COMPARADOR
    # ==========================================

    def comparar(a, b):

        na, da = a
        nb, db = b

        # 1 Puntos

        if da["puntos"] != db["puntos"]:
            return db["puntos"] - da["puntos"]

        # 2 Enfrentamiento directo

        av = average_particular(na, nb)

        if av:

            if av["puntos_a"] != av["puntos_b"]:
                return av["puntos_b"] - av["puntos_a"]

            ratio_a = av["sets_a"] / max(av["sets_b"], 1)
            ratio_b = av["sets_b"] / max(av["sets_a"], 1)

            if ratio_a != ratio_b:
                return -1 if ratio_a > ratio_b else 1

        # 3 Cociente sets

        ratio_sets_a = da["favor"] / max(da["contra"], 1)
        ratio_sets_b = db["favor"] / max(db["contra"], 1)

        if ratio_sets_a != ratio_sets_b:
            return -1 if ratio_sets_a > ratio_sets_b else 1

        # 4 Cociente puntos

        ratio_pts_a = da["pf"] / max(da["pc"], 1)
        ratio_pts_b = db["pf"] / max(db["pc"], 1)

        if ratio_pts_a != ratio_pts_b:
            return -1 if ratio_pts_a > ratio_pts_b else 1

        return 0

    # ==========================================
    # ORDENAR
    # ==========================================

    equipos = list(clasificacion.items())

    equipos.sort(key=cmp_to_key(comparar))

    return [
        {"equipo": equipo, "datos": datos}
        for equipo, datos in equipos
    ]
# Ruta para mostrar la clasificación y analisis del Univ. Valladolid VCV
@san_jose_route_bp.route("/equipos_voley/clasif_san_jose")
def clasif_analisis_san_jose():
    data = obtener_datos_san_jose()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_san_jose = generar_clasificacion_analisis_voley_san_jose(data)
    clubs_san_jose = JoseClub.query.all()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_san_jose:
        if not any(
            equipo["equipo"] == club.nombre for equipo in clasificacion_analisis_san_jose
        ):
            clasificacion_analisis_san_jose.append(
                {
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
                        "diferencia_puntos": 0,
                    },
                }
            )
    clasificacion_analisis_san_jose.sort(key=lambda x: x["datos"]["puntos"], reverse=True)
    return render_template(
        "equipos_vall/clasif_san_jose.html",
        clasificacion_analisis_san_jose=clasificacion_analisis_san_jose,
    )
@san_jose_route_bp.route("/jornada0_san_jose", methods=["GET", "POST"])
def jornada0_san_jose():
    if request.method == "POST":
        if "equipo" in request.form:
            club = request.form["equipo"]
            if club:
                nuevo_club = JoseClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for("san_jose_route_bp.jornada0_san_jose"))
    clubs = JoseClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template("admin/clubs/clubs_san_jose.html", clubs=clubs)


@san_jose_route_bp.route("/admin/eliminar_club_san_jose/<string:club_id>", methods=["POST"])
def eliminar_club_san_jose(club_id):
    club = JoseClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for("san_jose_route_bp.jornada0_san_jose"))
#Fin proceso Univ. Valladolid VCV