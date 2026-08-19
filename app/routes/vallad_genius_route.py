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
    TemporadaValladGenius,
    ValladGeniusGrupo,
    ValladGeniusGrupoEquipo 
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
    jornada = (
        db.session.query(JornadaValladGenius).filter(JornadaValladGenius.id == id).first()
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
                    db.session.query(ValladGeniusPartido)
                    .filter(ValladGeniusPartido.id == partido_id)
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
            return redirect(url_for("vallad_genius_route_bp.calendarios_vallad_genius"))
        # Si es un GET, pasamos la jornada con sus partidos ya cargados
        for partido in jornada.partidos:
            partido.hora = partido.hora.strftime("%H:%M") if partido.hora else ""
    return render_template("admin/calendarios/calend_vallad_genius.html", jornada=jornada)
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
    tabla_partidos_vallad_genius = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada["partidos"]:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB
            # Verificamos si el UEMC está jugando
            if (
                equipo_local == equipo_vallad_genius
                or equipo_visitante == equipo_vallad_genius
            ):
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_vallad_genius:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vallad_genius = "C"
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vallad_genius = "F"
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vallad_genius:
                    tabla_partidos_vallad_genius[equipo_contrario] = {"jornadas": {}}
                # Verificamos si es el primer o segundo enfrentamiento
                if (
                    "primer_enfrentamiento"
                    not in tabla_partidos_vallad_genius[equipo_contrario]
                ):
                    tabla_partidos_vallad_genius[equipo_contrario][
                        "primer_enfrentamiento"
                    ] = jornada["nombre"]
                    tabla_partidos_vallad_genius[equipo_contrario][
                        "resultadoA"
                    ] = resultado_a
                    tabla_partidos_vallad_genius[equipo_contrario][
                        "resultadoB"
                    ] = resultado_b
                elif (
                    "segundo_enfrentamiento"
                    not in tabla_partidos_vallad_genius[equipo_contrario]
                ):
                    tabla_partidos_vallad_genius[equipo_contrario][
                        "segundo_enfrentamiento"
                    ] = jornada["nombre"]
                    tabla_partidos_vallad_genius[equipo_contrario][
                        "resultadoAA"
                    ] = resultado_a
                    tabla_partidos_vallad_genius[equipo_contrario][
                        "resultadoBB"
                    ] = resultado_b
                # Agregamos la jornada y resultados
                if (
                    jornada["nombre"]
                    not in tabla_partidos_vallad_genius[equipo_contrario]["jornadas"]
                ):
                    tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ] = {
                        "resultadoA": resultado_a,
                        "resultadoB": resultado_b,
                        "rol_vallad_genius": rol_vallad_genius,
                    }
                # Asignamos los resultados según el rol del UEMC
                if (
                    equipo_local == equipo_contrario
                    or equipo_visitante == equipo_contrario
                ):
                    if not tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoA"]:
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoA"] = resultado_a
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoB"] = resultado_b
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vallad_genius"] = rol_vallad_genius
                    else:
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vallad_genius"] = rol_vallad_genius
                else:
                    if not tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                        jornada["nombre"]
                    ]["resultadoAA"]:
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vallad_genius"] = rol_vallad_genius
                    else:
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoAA"] = resultado_a
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["resultadoBB"] = resultado_b
                        tabla_partidos_vallad_genius[equipo_contrario]["jornadas"][
                            jornada["nombre"]
                        ]["rol_vallad_genius"] = rol_vallad_genius
    partidos_schema = obtener_partidos_schema(datos)                    
    return render_template(
        "equipos_vall/calendario_vallad_genius.html",
        tabla_partidos_vallad_genius=tabla_partidos_vallad_genius,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("vallad_genius")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "vallad_genius",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_vallad_genius"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "vallad_genius",
                "https://deportesdelaciudad.es/equipos_futbol/calendario_vallad_genius"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "vallad_genius",
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
            schema_breadcrumb_equipo("vallad_genius")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "vallad_genius",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_vallad_genius"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "vallad_genius",
                "https://deportesdelaciudad.es/equipos_futbol/resultados_vallad_genius"
            )
        ),
        schema_eventos=jsonld(
            schema_partidos(
                partidos_schema,
                "vallad_genius",
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
# Crear la clasificación Real Valladolid
def generar_clasificacion_analisis_futbol_vallad_genius(data):
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
# Ruta para mostrar la clasificación y análisis del Real Valladolid
@vallad_genius_route_bp.route("/equipos_futbol/clasif_vallad_genius")
def clasif_analisis_vallad_genius():
    data = obtener_datos_vallad_genius()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_vallad_genius = (
        generar_clasificacion_analisis_futbol_vallad_genius(data)
    )
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_vallad_genius = ValladGeniusClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
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
                        "favor": 0,
                        "contra": 0,
                        "diferencia_goles": 0,
                    },
                }
            )

    clasificacion_analisis_vallad_genius.sort(
        key=lambda x: x["datos"]["puntos"], reverse=True
    )
    return render_template(
        "equipos_vall/clasif_vallad_genius.html",
        clasificacion_analisis_vallad_genius=clasificacion_analisis_vallad_genius,
        breadcrumb=jsonld(
            schema_breadcrumb_equipo("vallad_genius")
        ),
        schema_team=jsonld(
            schema_sports_team(
                "vallad_genius",
                "https://deportesdelaciudad.es/equipos_futbol/clasif_vallad_genius"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "vallad_genius",
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

# GRUPOS FORMATO LIGA ValladoliDi 
@vallad_genius_route_bp.route('/admin/grupos_vallad_genius', methods=['GET'])
def grupos_vallad_genius():
    grupos = (
        ValladGeniusGrupo.query
        .order_by(
            ValladGeniusGrupo.fase.asc(),
            ValladGeniusGrupo.id.asc()
        )
        .all()
    )

    return render_template(
        'admin/clubs/clubs_vallad_genius.html',
        grupos=grupos
    )
# Crear grupo
@vallad_genius_route_bp.route('/admin/crear_grupo_vallad_genius', methods=['POST'])
def crear_grupo_vallad_genius():
    nombre = request.form.get('nombre')
    fase = request.form.get('fase')

    if not nombre or not fase:
        flash(
            'Debes indicar el grupo y la fase.',
            'warning'
        )

        return redirect(
            url_for(
                'vallad_genius_route_bp.grupos_vallad_genius'
            )
        )

    # Evitar grupos duplicados
    existe = ValladGeniusGrupo.query.filter_by(
        nombre=nombre,
        fase=fase
    ).first()

    if existe:
        flash(
            'Ese grupo ya existe.',
            'warning'
        )

        return redirect(
            url_for(
                'vallad_genius_route_bp.grupos_vallad_genius'
            )
        )

    grupo = ValladGeniusGrupo(
        nombre=nombre,
        fase=fase
    )

    db.session.add(grupo)
    db.session.commit()

    flash(
        f'Grupo {nombre} creado correctamente.',
        'success'
    )

    return redirect(
        url_for(
            'vallad_genius_route_bp.grupos_vallad_genius'
        )
    )    
#Añadir equipo al grupo
@vallad_genius_route_bp.route('/admin/crear_equipo_grupo_vallad_genius',methods=['POST'])
def crear_equipo_grupo_vallad_genius():
    grupo_id = request.form.get('grupo_id')
    equipo = request.form.get('equipo', '').strip()

    if not grupo_id or not equipo:
        flash(
            'Debes indicar un equipo.',
            'warning'
        )

        return redirect(
            url_for(
                'vallad_genius_route_bp.grupos_vallad_genius'
            )
        )

    grupo = ValladGeniusGrupo.query.get_or_404(grupo_id)

    # No permitir más de 8 equipos
    if len(grupo.equipos) >= 17:
        flash(
            'Este grupo ya tiene 8 equipos.',
            'warning'
        )

        return redirect(
            url_for(
                'vallad_genius_route_bp.grupos_vallad_genius'
            )
        )

    # Evitar que el mismo equipo esté dos veces en el grupo
    existe = ValladGeniusGrupoEquipo.query.filter_by(
        grupo_id=grupo.id,
        equipo=equipo
    ).first()

    if existe:
        flash(
            'Ese equipo ya está en este grupo.',
            'warning'
        )

        return redirect(
            url_for(
                'vallad_genius_route_bp.grupos_vallad_genius'
            )
        )

    nuevo_equipo = ValladGeniusGrupoEquipo(
        grupo_id=grupo.id,
        equipo=equipo
    )

    db.session.add(nuevo_equipo)
    db.session.commit()

    flash(
        f'{equipo} añadido al Grupo {grupo.nombre}.',
        'success'
    )

    return redirect(
        url_for(
            'vallad_genius_route_bp.grupos_vallad_genius'
        )
    )    
#Eliminar equipo
@vallad_genius_route_bp.route( '/admin/eliminar_equipo_grupo_vallad_genius/<int:id>', methods=['POST'])
def eliminar_equipo_grupo_vallad_genius(id):
    equipo = ValladGeniusGrupoEquipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash(
        'Equipo eliminado del grupo.',
        'success'
    )
    return redirect(url_for('vallad_genius_route_bp.grupos_vallad_genius')
    )

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
    historial = (Historial.query.filter_by(
        deporte="futbol",
        equipo="R.ValladoliDi"
    ).order_by(Historial.temporada.desc()).all())
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = TemporadaValladGenius.query.order_by(TemporadaValladGenius.id).all()
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
            equipo="R.ValladoliDi"
        ).order_by(Palmaress.orden.asc(),Palmaress.temporada.desc()).all())
    palmares = OrderedDict()
    for titulo in titulos:
        if titulo.competicion not in palmares:
            palmares[titulo.competicion] = []
        palmares[titulo.competicion].append(titulo)
    labels_jornadas = []

    for i, temporada in enumerate(temporadas):

        jornadas = (
            JornadaValladGenius.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaValladGenius.id)
            .all()
        )

        if not jornadas:
            continue

        labels, puntos = obtener_evolucion_puntos(
            jornadas, "R.ValladoliDi", generar_clasificacion_analisis_futbol_vallad_genius,"puntos"
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
            schema_breadcrumb_equipo("vallad_genius")
        ),
        schema_team=jsonld(
            schema_sports_team(
               "vallad_genius",
               "https://deportesdelaciudad.es/vallad_genius/historial"
            )
        ),
        schema_competition=jsonld(
            schema_sports_competition(
                "vallad_genius",
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