from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from collections import OrderedDict
from itertools import groupby
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.historial import obtener_evolucion_puntos
from ..models.historial import Historial, Palmaress
from ..models.vcv import JornadaVCV, VCVPartido, VCVClub, PlayoffVCV, CopaVCV, EuropaVCV, Clasificacion, TemporadaVCV

vcv_route_bp = Blueprint("vcv_route_bp", __name__)

# EQUIPOS VOLEIBOL
# Ingresar los resultados de los partidos de Univ. Valladolid VCV
@vcv_route_bp.route('/crear_calendario_vcv', methods=['GET', 'POST'])
def ingresar_resultado_vcv():
    if request.method == 'POST':
        temporada_nombre = request.form['temporada']
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaVCV.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaVCV(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaVCV(
            nombre=nombre_jornada,
            temporada_id=temporada.id
        )
        db.session.add(jornada)
        db.session.flush()  # Esto nos da el ID antes del commit        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):

            local = request.form.get(f'local{i}')
            visitante = request.form.get(f'visitante{i}')

            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            # 🔥 CLAVE: ignorar partidos vacíos
            if not local or not visitante:
                continue

            partido = VCVPartido(
                jornada_id=jornada.id,
                fecha=request.form.get(f'fecha{i}'),
                hora=request.form.get(f'hora{i}'),
                local=local,
                visitante=visitante,
                resultadoA=resultadoA or "",
                resultadoB=resultadoB or "",
                puntosA=request.form.get(f'puntosA{i}') or 0,
                puntosB=request.form.get(f'puntosB{i}') or 0,
                orden=i
            )

            db.session.add(partido)
            # Confirmar todos los cambios en la base de datos
        db.session.commit()
        print("JORNADA:", jornada.nombre)
        print("PARTIDOS GUARDADOS:", len(jornada.partidos))
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('vcv_route_bp.calendarios_vcv'))
# Partidos Univ. Valladolid VCV
@vcv_route_bp.route("/calendario_vcv")
def calendarios_vcv():
    temporada = TemporadaVCV.query.filter_by(activa=True).first()
    if temporada:
        jornadas = JornadaVCV.query.filter_by(
        temporada_id=temporada.id
        ).order_by(JornadaVCV.id.asc()).all()
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(VCVPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(VCVPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_vcv.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@vcv_route_bp.route("/modificar_jornada_vcv/<string:id>", methods=["POST"])
def modificar_jornada_vcv(id):
    jornada = db.session.query(JornadaVCV).filter(JornadaVCV.id == id).first()
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
                    db.session.query(VCVPartido)
                    .filter(VCVPartido.id == partido_id)
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
            return redirect(url_for("vcv_route_bp.calendarios_vcv"))
    return render_template("admin/calendarios/calend_vcv.html", jornada=jornada)
# Ruta para borrar jornadas
@vcv_route_bp.route("/eliminar_jorn_vcv/<string:id>", methods=["POST"])
def eliminar_jornada_vcv(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaVCV).filter(JornadaVCV.id == id).first()
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(VCVPartido).filter(VCVPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for("vcv_route_bp.calendarios_vcv"))
def obtener_datos_vcv(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaVCV.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaVCV.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            VCVPartido.query
            .filter_by(jornada_id=jornada.id)
            .order_by(VCVPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({
            'nombre': jornada.nombre,
            'partidos': partidos
        })
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Univ. Valladolid VCV
@vcv_route_bp.route("/equipos_voley/calendario_vcv")
def calendario_vcv():
    datos = obtener_datos_vcv()
    equipo_vcv = "Universidad VCV"
    tabla_partidos_vcv = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada["partidos"]:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB
            # Verificamos si el Caja está jugando
            if equipo_local == equipo_vcv or equipo_visitante == equipo_vcv:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_vcv:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vcv = "C"
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vcv = "F"
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vcv:
                    tabla_partidos_vcv[equipo_contrario] = {"jornadas": {}}
                # Verificamos si es el primer o segundo enfrentamiento
                if "primer_enfrentamiento" not in tabla_partidos_vcv[equipo_contrario]:
                    tabla_partidos_vcv[equipo_contrario]["primer_enfrentamiento"] = (
                        jornada["nombre"]
                    )
                    tabla_partidos_vcv[equipo_contrario]["resultadoA"] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]["resultadoB"] = resultado_b
                elif (
                    "segundo_enfrentamiento" not in tabla_partidos_vcv[equipo_contrario]
                ):
                    tabla_partidos_vcv[equipo_contrario]["segundo_enfrentamiento"] = (
                        jornada["nombre"]
                    )
                    tabla_partidos_vcv[equipo_contrario]["resultadoAA"] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]["resultadoBB"] = resultado_b
                # Agregamos la jornada y resultados
                if (
                    jornada["nombre"]
                    not in tabla_partidos_vcv[equipo_contrario]["jornadas"]
                ):
                    tabla_partidos_vcv[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ] = {
                        "resultadoA": resultado_a,
                        "resultadoB": resultado_b,
                        "rol_vcv": rol_vcv,
                    }
                # Asignamos los resultados según el rol del Vcv
                if (
                    equipo_local == equipo_contrario
                    or equipo_visitante == equipo_contrario
                ):
                    if not tabla_partidos_vcv[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoA"]:
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoA"] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoB"] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vcv"] = rol_vcv
                    else:
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vcv"] = rol_vcv
                else:
                    if not tabla_partidos_vcv[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoAA"]:
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vcv"] = rol_vcv
                    else:
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vcv"] = rol_vcv
    return render_template(
        "equipos_vall/calendario_vcv.html", tabla_partidos_vcv=tabla_partidos_vcv
    )
# Jornadas VCV
@vcv_route_bp.route('/equipos_voley/resultados_vcv')
def resultados_vcv():
    datos = obtener_datos_vcv()
    nuevos_datos_vcv = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_vcv):
        jornada_completa = all(
            p.resultadoA not in (None, "") and
            p.resultadoB not in (None, "")
            for p in jornada['partidos']
        )
        if not jornada_completa:
            jornada_activa = jornada['nombre']
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_vcv:
        jornada_activa = nuevos_datos_vcv[-1]['nombre']
    return render_template(
        'equipos_vall/jornadas_vcv.html',
        nuevos_datos_vcv=nuevos_datos_vcv,
        jornada_activa=jornada_activa
    )
# Crear la clasificación de Univ. Valladolid VCV
def generar_clasificacion_analisis_voley_vcv(data):

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

    # ==========================================
    # RECORRER PARTIDOS
    # ==========================================

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
@vcv_route_bp.route("/equipos_voley/clasif_vcv")
def clasif_analisis_vcv():
    data = obtener_datos_vcv()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_vcv = generar_clasificacion_analisis_voley_vcv(data)
    clubs_vcv = VCVClub.query.all()
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_vcv:
        if not any(
            equipo["equipo"] == club.nombre for equipo in clasificacion_analisis_vcv
        ):
            clasificacion_analisis_vcv.append(
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
    clasificacion_analisis_vcv.sort(key=lambda x: x["datos"]["puntos"], reverse=True)
    return render_template(
        "equipos_vall/clasif_vcv.html",
        clasificacion_analisis_vcv=clasificacion_analisis_vcv,
    )
@vcv_route_bp.route("/jornada0_vcv", methods=["GET", "POST"])
def jornada0_vcv():
    if request.method == "POST":
        if "equipo" in request.form:
            club = request.form["equipo"]
            if club:
                nuevo_club = VCVClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for("vcv_route_bp.jornada0_vcv"))
    clubs = VCVClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template("admin/clubs/clubs_vcv.html", clubs=clubs)
@vcv_route_bp.route("/admin/eliminar_club_vcv/<string:club_id>", methods=["POST"])
def eliminar_club_vcv(club_id):
    club = VCVClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for("vcv_route_bp.jornada0_vcv"))
# TEMPORADAS Panteras
@vcv_route_bp.route('/temporadas_vcv')
def temporadas_vcv():
    temporadas = TemporadaVCV.query.order_by(
        TemporadaVCV.id.desc()
    ).all()
    return render_template(
        'admin/temporadas/temporada_vcv.html',
        temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@vcv_route_bp.route('/activar_temporada_vcv/<int:id>')
def activar_temporada_vcv(id):
    TemporadaVCV.query.update({"activa": False})
    temporada = TemporadaVCV.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for('vcv_route_bp.temporadas_vcv')) 

# HISTORIAL UNIVERSIDAD VCV
# Creación del historial de temporadas del VCV
@vcv_route_bp.route("/admin/crear_historial_vcv", methods=["GET", "POST"])
def crear_historial_vcv():
    if request.method == "POST":
        historial = Historial(
            deporte="voley",
            equipo="Universidad VCV",
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
        return redirect(url_for("vcv_route_bp.crear_historial_vcv"))
    historial = (Historial.query.filter_by(
        deporte="voley",
        equipo="Universidad VCV"
    ).order_by(Historial.temporada.desc()).all()
                 )
    temporadas = TemporadaVCV.query.order_by(
        TemporadaVCV.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial.html",
        historial=historial,
        temporadas=temporadas,
        deporte="voley",
        equipo="Universidad VCV",
        crear_url="vcv_route_bp.crear_historial_vcv",
        modificar_url="vcv_route_bp.modificar_historial_vcv",
        eliminar_url="vcv_route_bp.eliminar_historial_vcv"
    )
# Eliminar historial de temporadas del VCV
@vcv_route_bp.route("/admin/eliminar_historial_vcv/<int:id>", methods=["POST"])
def eliminar_historial_vcv(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("vcv_route_bp.crear_historial_vcv"))
# Modificar historial de temporadas del VCV
@vcv_route_bp.route("/admin/modificar_historial_vcv/<int:id>", methods=["POST"])
def modificar_historial_vcv(id):
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
    return redirect(url_for("vcv_route_bp.crear_historial_vcv"))
# Ver Historial de temporadas del VCV en la página principal
@vcv_route_bp.route("/vcv/historial")
def historial_vcv():
    historial = (Historial.query.filter_by(
        deporte="voley",
        equipo="Universidad VCV"
    ).order_by(Historial.temporada.desc()).all())
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = TemporadaVCV.query.order_by(TemporadaVCV.id).all()
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
            deporte="voley",
            equipo="Universidad VCV"
        ).order_by(Palmaress.orden.asc(),Palmaress.temporada.desc()).all())
    palmares = OrderedDict()
    for titulo in titulos:
        if titulo.competicion not in palmares:
            palmares[titulo.competicion] = []
        palmares[titulo.competicion].append(titulo)
    labels_jornadas = []
    for i, temporada in enumerate(temporadas):
        jornadas = (
            JornadaVCV.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaVCV.id)
            .all()
        )
        if not jornadas:
            continue
        labels, puntos = obtener_evolucion_puntos(
            jornadas, "Universidad VCV", generar_clasificacion_analisis_voley_vcv,"puntos"
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
        "historia/historia_vcv.html",
        historial=historial,
        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,
        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,
        palmares=palmares,
        deporte="voley",
        equipo="Universidad VCV"
  )

# PALMARES UNIVERSIDAD VCV
# Crear Palmares del VCV
@vcv_route_bp.route("/admin/crear_palmares_vcv", methods=["GET", "POST"])
def crear_palmares_vcv():
    if request.method == "POST":
        titulo = Palmaress(
            deporte="voley",
            equipo="Universidad VCV",
            temporada=request.form.get("temporada"),
            competicion=request.form.get("competicion"),
            imagen=request.form.get("imagen"),
            orden=int(request.form.get("orden", 0))
        )
        db.session.add(titulo)
        db.session.commit()
        return redirect(url_for("vcv_route_bp.crear_palmares_vcv"))
    palmares = (
        Palmaress.query.filter_by(
            deporte="voley",
            equipo="Universidad VCV"
        )
        .order_by(
            Palmaress.orden.asc(),
            Palmaress.temporada.desc()
        )
        .all()
    )
    return render_template(
        "admin/historial/palmares.html",
        palmares=palmares,
        deporte="Voley",
        equipo="Universidad VCV",
        crear_url="vcv_route_bp.crear_palmares_vcv",
        modificar_url="vcv_route_bp.modificar_palmares_vc",
        eliminar_url="vcv_route_bp.eliminar_palmares_vcv",
    )
# Modificar Palmares del VCV
@vcv_route_bp.route("/admin/modificar_palmares_vcv/<int:id>", methods=["POST"])
def modificar_palmares_vcv(id):
    titulo = Palmaress.query.get_or_404(id)
    titulo.temporada = request.form.get("temporada")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    titulo.orden = request.form.get("orden")
    db.session.commit()
    return redirect(url_for("vcv_route_bp.crear_palmares_vcv"))
# Eliminar Palmares del VCV
@vcv_route_bp.route("/admin/eliminar_palmares_vcv/<int:id>", methods=["POST"])
def eliminar_palmares_vcv(id):
    titulo = Palmaress.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("vcv_route_bp.crear_palmares_vcv"))

# Fin proceso Univ. Valladolid VCV

