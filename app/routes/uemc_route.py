from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.historial import obtener_evolucion_puntos
from ..models.uemc import JornadaUEMC, UEMCPartido, UEMCClub, CopaUEMC, Clasificacion, PlayoffUEMC, TemporadaUEMC, HistorialUEMC, PalmaresUEMC

uemc_route_bp = Blueprint('uemc_route_bp', __name__)

# LIGA UEMC
#Todo el proceso de calendario y clasificación del UEMC
# Ingresar los resultados de los partidos UEMC
@uemc_route_bp.route('/crear_calendario_uemc', methods=['GET', 'POST'])
def ingresar_resultado_uemc():
    if request.method == 'POST':
        temporada_nombre = request.form['temporada']
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaUEMC.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaUEMC(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaUEMC(
            nombre=nombre_jornada,
            temporada_id=temporada.id
        )
        db.session.add(jornada)
        db.session.flush()  # Esto nos da el ID antes del commit        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            partido = UEMCPartido(
                jornada_id=jornada.id,
                fecha=request.form.get(f'fecha{i}'),
                hora=request.form.get(f'hora{i}'),
                local=request.form.get(f'local{i}'),
                resultadoA=request.form.get(f'resultadoA{i}'),
                resultadoB=request.form.get(f'resultadoB{i}'),
                visitante=request.form.get(f'visitante{i}'),
                orden=i
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('uemc_route_bp.calendarios_uemc'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_uemc.html')
# Ver calendario UEMC en Admin
@uemc_route_bp.route('/calendario_uemc')
def calendarios_uemc():
    temporada = TemporadaUEMC.query.filter_by(activa=True).first()
    if temporada:
        jornadas = JornadaUEMC.query.filter_by(
        temporada_id=temporada.id
        ).order_by(JornadaUEMC.id.asc()).all()
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(UEMCPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(UEMCPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_uemc.html', jornadas=jornadas)
# Modificar jornada
@uemc_route_bp.route('/modificar_jornada_uemc/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_uemc(id):
    jornada = db.session.query(JornadaUEMC).filter(JornadaUEMC.id == id).first()
    if jornada:
        if request.method == 'POST':
            nombre_jornada = request.form['nombre']
            num_partidos = int(request.form['num_partidos'])
            jornada.nombre = nombre_jornada  # Actualizar el nombre de la jornada          
            # Actualizar los partidos
            for i in range(num_partidos):
                partido_id = request.form[f'partido_id{i}']
                fecha = request.form[f'fecha{i}']
                hora = request.form[f'hora{i}']
                local = request.form[f'local{i}']
                resultadoA = request.form[f'resultadoA{i}']
                resultadoB = request.form[f'resultadoB{i}']
                visitante = request.form[f'visitante{i}']                
                # Obtener el partido correspondiente por ID
                partido = db.session.query(UEMCPartido).filter(UEMCPartido.id == partido_id).first()
                if partido:
                    partido.fecha = fecha
                    partido.hora = hora
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante
                    orden = int(request.form.get(f'orden{i}', i))  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('uemc_route_bp.calendarios_uemc'))        
    return render_template('admin/calendarios/calend_uemc.html', jornada=jornada)
# Eliminar jornada
@uemc_route_bp.route('/eliminar_jornada_uemc/<int:id>', methods=['GET','POST'])
def eliminar_jornada_uemc(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaUEMC).filter(JornadaUEMC.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(UEMCPartido).filter(UEMCPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('uemc_route_bp.calendarios_uemc'))
# Obtener datos UEMC
def obtener_datos_uemc(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaUEMC.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaUEMC.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            UEMCPartido.query
            .filter_by(jornada_id=jornada.id)
            .order_by(UEMCPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({
            'nombre': jornada.nombre,
            'partidos': partidos
        })
    return jornadas_con_partidos
# Calendario UEMC
@uemc_route_bp.route('/equipos_basket/calendario_uemc')
def calendario_uemc():
    datos = obtener_datos_uemc()
    equipo_uemc = 'CBC Valladolid'
    tabla_partidos_uemc = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_uemc or equipo_visitante == equipo_uemc:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_uemc:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_uemc = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_uemc = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_uemc:
                    tabla_partidos_uemc[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_uemc[equipo_contrario]:
                    tabla_partidos_uemc[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_uemc[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_uemc[equipo_contrario]:
                    tabla_partidos_uemc[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_uemc[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_uemc[equipo_contrario]['jornadas']:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_uemc': rol_uemc
                    }               
                # Asignamos los resultados según el rol del UEMC
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                    else:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                else:
                    if not tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                    else:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
    return render_template('equipos_vall/calendario_uemc.html', tabla_partidos_uemc=tabla_partidos_uemc)
# Jornadas UEMC
@uemc_route_bp.route('/equipos_basket/resultados_uemc')
def resultados_uemc():
    datos = obtener_datos_uemc()
    nuevos_datos_uemc = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_uemc):
        jornada_completa = all(
            p.resultadoA not in (None, "") and
            p.resultadoB not in (None, "")
            for p in jornada['partidos']
        )
        if not jornada_completa:
            jornada_activa = jornada['nombre']
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_uemc:
        jornada_activa = nuevos_datos_uemc[-1]['nombre']
    return render_template(
        'equipos_vall/jornadas_uemc.html',
        nuevos_datos_uemc=nuevos_datos_uemc,
        jornada_activa=jornada_activa
    )
# Jornada 0 UEMC
@uemc_route_bp.route('/jornada0_uemc', methods=['GET', 'POST'])
def jornada0_uemc():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = UEMCClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('uemc_route_bp.jornada0_uemc'))
    clubs = UEMCClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_uemc.html', clubs=clubs)
# Eliminar clubs jornada 0
@uemc_route_bp.route('/eliminar_club_uemc/<int:club_id>', methods=['POST'])
def eliminar_club_uemc(club_id):
    club = UEMCClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('uemc_route_bp.jornada0_uemc'))
# Crear la clasificación UEMC
def generar_clasificacion_analisis_baloncesto_uemc(data):

    clasificacion = defaultdict(lambda: {
        'jugados': 0,
        'ganados': 0,
        'perdidos': 0,
        'favor': 0,
        'contra': 0,
        'diferencia_canastas': 0,
        'puntos': 0
    })

# GUARDAR ENFRENTAMIENTOS

    enfrentamientos = []

    for jornada in data:

        for partido in jornada['partidos']:

            equipo_local = partido.local
            equipo_visitante = partido.visitante

            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB

            # Saltar vacíos
            if (
                resultado_local is None
                or resultado_visitante is None
                or resultado_local == ''
                or resultado_visitante == ''
            ):
                continue

            try:

                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)

            except ValueError:
                continue

# CLASIFICACIÓN GENERAL

            if resultado_local > resultado_visitante:

                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1

                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1

            else:

                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1

                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['perdidos'] += 1

            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1

            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante

            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local

            clasificacion[equipo_local]['diferencia_canastas'] += (
                resultado_local - resultado_visitante
            )

            clasificacion[equipo_visitante]['diferencia_canastas'] += (
                resultado_visitante - resultado_local
            )

# GUARDAR PARTIDO

            enfrentamientos.append({
                'local': equipo_local,
                'visitante': equipo_visitante,
                'puntos_local': resultado_local,
                'puntos_visitante': resultado_visitante
            })

    # =========================================================
    # MINI LIGA ENTRE EMPATADOS
    # =========================================================

    def clasificacion_particular(equipos_empatados):

        mini = defaultdict(lambda: {
            'victorias': 0,
            'derrotas': 0,
            'favor': 0,
            'contra': 0,
            'average': 0,
            'puntos': 0
        })

        for partido in enfrentamientos:

            local = partido['local']
            visitante = partido['visitante']

            if (
                local not in equipos_empatados
                or visitante not in equipos_empatados
            ):
                continue

            pl = partido['puntos_local']
            pv = partido['puntos_visitante']

            # FAVOR / CONTRA

            mini[local]['favor'] += pl
            mini[local]['contra'] += pv

            mini[visitante]['favor'] += pv
            mini[visitante]['contra'] += pl

            mini[local]['average'] += (pl - pv)
            mini[visitante]['average'] += (pv - pl)

            # VICTORIAS

            if pl > pv:

                mini[local]['victorias'] += 1
                mini[visitante]['derrotas'] += 1

                mini[local]['puntos'] += 2
                mini[visitante]['puntos'] += 1

            else:

                mini[visitante]['victorias'] += 1
                mini[local]['derrotas'] += 1

                mini[visitante]['puntos'] += 2
                mini[local]['puntos'] += 1

        return mini

    # =========================================================
    # COMPARADOR OFICIAL
    # =========================================================

    def comparar_equipos(a, b):

        nombre_a, datos_a = a
        nombre_b, datos_b = b

        # =========================================================
        # 1. PUNTOS GENERALES
        # =========================================================

        if datos_a['puntos'] != datos_b['puntos']:

            return datos_b['puntos'] - datos_a['puntos']

        # =========================================================
        # 2. EQUIPOS EMPATADOS
        # =========================================================

        equipos_empatados = []

        for equipo, datos in clasificacion.items():

            if datos['puntos'] == datos_a['puntos']:

                equipos_empatados.append(equipo)

        # =========================================================
        # 3. MINI LIGA
        # =========================================================

        if len(equipos_empatados) >= 2:

            mini = clasificacion_particular(equipos_empatados)

            mini_a = mini[nombre_a]
            mini_b = mini[nombre_b]

            # Puntos mini liga

            if mini_a['puntos'] != mini_b['puntos']:

                return mini_b['puntos'] - mini_a['puntos']

            # Average mini liga

            if mini_a['average'] != mini_b['average']:

                return mini_b['average'] - mini_a['average']

            # Favor mini liga

            if mini_a['favor'] != mini_b['favor']:

                return mini_b['favor'] - mini_a['favor']

        # =========================================================
        # 4. DIFERENCIA GENERAL
        # =========================================================

        if (
            datos_a['diferencia_canastas']
            != datos_b['diferencia_canastas']
        ):

            return (
                datos_b['diferencia_canastas']
                - datos_a['diferencia_canastas']
            )

        # =========================================================
        # 5. PUNTOS A FAVOR
        # =========================================================

        if datos_a['favor'] != datos_b['favor']:

            return datos_b['favor'] - datos_a['favor']

        return 0

    # =========================================================
    # ORDENAR
    # =========================================================

    equipos = list(clasificacion.items())

    equipos.sort(
        key=cmp_to_key(comparar_equipos)
    )

    # =========================================================
    # DEVOLVER
    # =========================================================

    return [
        {
            'equipo': equipo,
            'datos': datos
        }
        for equipo, datos in equipos
    ]   
# Ruta para mostrar la clasificación y análisis del UEMC
@uemc_route_bp.route('/equipos_basket/clasif_uemc')
def clasif_analisis_uemc():
    data = obtener_datos_uemc()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_uemc = generar_clasificacion_analisis_baloncesto_uemc(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_uemc = UEMCClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_uemc:
        if not any(
            equipo['equipo'] == club.nombre
            for equipo in clasificacion_analisis_uemc
        ):

            clasificacion_analisis_uemc.append({
                'equipo': club.nombre,
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            })

    clasificacion_analisis_uemc.sort(
        key=lambda x: x['datos']['puntos'],
        reverse=True
    )
    return render_template(
        'equipos_vall/clasif_uemc.html',
        clasificacion_analisis_uemc=clasificacion_analisis_uemc
    )
# TEMPORADAS ATL VALLADOLID
@uemc_route_bp.route('/temporadas_uemc')
def temporadas_uemc():
    temporadas = TemporadaUEMC.query.order_by(
        TemporadaUEMC.id.desc()
    ).all()
    return render_template(
        'admin/temporadas/temporada_uemc.html',
        temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@uemc_route_bp.route('/activar_temporada_uemc/<int:id>')
def activar_temporada_uemc(id):
    TemporadaUEMC.query.update({"activa": False})
    temporada = TemporadaUEMC.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for('uemc_route_bp.temporadas_uemc')) 

# HISTORIAL UEMC
# Creación del historial de temporadas del UEMC
@uemc_route_bp.route("/admin/crear_historial_uemc", methods=["GET", "POST"])
def crear_historial_uemc():
    if request.method == "POST":
        historial = HistorialUEMC(
            temporada_id=request.form.get("temporada_id"),
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
        return redirect(url_for("uemc_route_bp.crear_historial_uemc"))
    historial = (
        HistorialUEMC.query.join(TemporadaUEMC)
        .order_by(TemporadaUEMC.nombre.desc())
        .all()
    )
    temporadas = TemporadaUEMC.query.order_by(
        TemporadaUEMC.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial_uemc.html",
        historial=historial,
        temporadas=temporadas,
    )

# Ver Historial de temporadas del UEMC
@uemc_route_bp.route("/historial_uemc")
def historial_uemc_admin():
    historial = (
        HistorialUEMC.query.join(TemporadaUEMC)
        .order_by(TemporadaUEMC.nombre.desc())
        .all()
    )
    temporadas = TemporadaUEMC.query.order_by(
        TemporadaUEMC.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial_uemc.html",
        historial=historial,
        temporadas=temporadas,
    )

# Eliminar historial de temporadas del UEMC
@uemc_route_bp.route(
    "/admin/eliminar_historial_uemc/<int:id>", methods=["POST"]
)
def eliminar_historial_uemc(id):
    historial = HistorialUEMC.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("uemc_route_bp.crear_historial_uemc"))

# Modificar historial de temporadas del UEMC
@uemc_route_bp.route("/admin/modificar_historial_uemc/<int:id>", methods=["POST"])
def modificar_historial_uemc(id):
    historial = HistorialUEMC.query.get_or_404(id)
    historial.temporada_id = request.form.get("temporada_id")
    historial.liga = request.form.get("liga")
    historial.puntos = request.form.get("puntos")
    historial.puesto = request.form.get("puesto")
    historial.playoff = request.form.get("playoff")
    historial.copa = request.form.get("copa")
    historial.siguiente_temporada = request.form.get("siguiente_temporada")
    historial.titulos = request.form.get("titulos")
    historial.observaciones = request.form.get("observaciones")
    db.session.commit()
    return redirect(url_for("uemc_route_bp.crear_historial_uemc"))

# Ver Historial de temporadas del UEMC en la página principal
@uemc_route_bp.route("/uemc/historial")
def historial_uemc():
    historial = HistorialUEMC.query.order_by(
        HistorialUEMC.temporada_id.desc()
    ).all()
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada.nombre for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = TemporadaUEMC.query.order_by(TemporadaUEMC.id).all()
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
            JornadaUEMC.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaUEMC.id)
            .all()
        )
        if not jornadas:
            continue
        labels, puntos = obtener_evolucion_puntos(
            jornadas, "CBC Valladolid", generar_clasificacion_analisis_baloncesto_uemc,"ganados"
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
        titulos = (
            PalmaresUEMC.query.join(TemporadaUEMC)
            .order_by(TemporadaUEMC.nombre.desc())
            .all()
        )
    return render_template(
        "historia/historia_uemc.html",
        historial=historial,
        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,
        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,
        titulos=titulos,
  )

# PALMARES UEMC
# Crear Palmares del UEMC
@uemc_route_bp.route("/admin/crear_palmares_uemc", methods=["POST"])
def crear_palmares_uemc():
    titulo = PalmaresUEMC(
        temporada_id=request.form.get("temporada_id"),
        competicion=request.form.get("competicion"),
        imagen=request.form.get("imagen"),
    )
    db.session.add(titulo)
    db.session.commit()
    return redirect(url_for("uemc_route_bp.ver_palmares_uemc"))
# Modificar Palmares del UEMC
@uemc_route_bp.route("/admin/modificar_palmares_uemc/<int:id>", methods=["POST"])
def modificar_palmares_uemc(id):
    titulo = PalmaresUEMC.query.get_or_404(id)
    titulo.temporada_id = request.form.get("temporada_id")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    db.session.commit()
    return redirect(url_for("uemc_route_bp.ver_palmares_uemc"))
# Eliminar Palmares del UEMC
@uemc_route_bp.route("/admin/eliminar_palmares_uemc/<int:id>", methods=["POST"])
def eliminar_palmares_uemc(id):
    titulo = PalmaresUEMC.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("uemc_route_bp.ver_palmares_uemc"))
# Ver Palmares del UEMC en Admin
@uemc_route_bp.route("/palmares_uemc")
def ver_palmares_uemc():
    temporadas = TemporadaUEMC.query.order_by(TemporadaUEMC.id.desc()).all()
    palmares = PalmaresUEMC.query.order_by(PalmaresUEMC.temporada_id.desc()).all()
    return render_template(
        "admin/historial/palma_uemc.html",
        temporadas=temporadas,
        palmares=palmares,
    )

# COPA UEMC
# Crear formulario para los grupos de la Copa UEMC
@uemc_route_bp.route('/crear_copa_uemc', methods=['GET', 'POST'])
def crear_copa_uemc():

    def safe_int(value):
        try:
            if value is None or value == '':
                return None
            return int(value)
        except ValueError:
            return None

    if request.method == 'POST':

        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))

        for i in range(num_partidos):

            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            visitante = request.form.get(f'visitante{i}')

            resultadoA = safe_int(request.form.get(f'resultadoA{i}'))
            resultadoB = safe_int(request.form.get(f'resultadoB{i}'))

            nuevo_partido = CopaUEMC(
                encuentros=encuentros,
                fecha=fecha or '',
                hora=hora or '',
                local=local or '',
                resultadoA=resultadoA,
                resultadoB=resultadoB,
                visitante=visitante or ''
            )

            db.session.add(nuevo_partido)

        db.session.commit()

        return redirect(url_for('uemc_route_bp.ver_copa_uemc'))

    return render_template('admin/copa/copa_uemc.html')
# Ver la Copa UEMC en Admin (crear/editar partidos)
@uemc_route_bp.route('/copa_uemc/')
def ver_copa_uemc():
    # Definimos todas las jornadas de la fase regular
    jornadas = ['liga_j1', 'liga_j2', 'liga_j3']
    # Y las fases de eliminatorias
    fases_eliminatorias = ['dieciseisavos', 'octavos', 'cuartos', 'semifinales', 'final']
    # Diccionario para la fase regular
    datos_jornadas = {j: CopaUEMC.query.filter_by(encuentros=j).order_by(CopaUEMC.id).all() for j in jornadas}
    # Diccionario para eliminatorias
    datos_eliminatorias = {f: CopaUEMC.query.filter_by(encuentros=f).order_by(CopaUEMC.id).all() for f in fases_eliminatorias}
    return render_template('admin/copa/copa_uemc.html',datos_jornadas=datos_jornadas, datos_eliminatorias=datos_eliminatorias)
# Actualizar clasificación de los grupos
def actualizar_clasificacion(local, resultado_local, resultado_visitante, visitante):
    # Convertir los resultados a enteros
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Consultar si los equipos ya están en la clasificación
    clasificacion_local = Clasificacion.query.filter_by(equipo=local).first()
    clasificacion_visitante = Clasificacion.query.filter_by( equipo=visitante).first()
    # Si el local no existe, lo creamos
    if not clasificacion_local:
        clasificacion_local = Clasificacion( equipo=local, jugados=0, ganados=0, perdidos=0, puntos=0, pf=0, pc=0)
        db.session.add(clasificacion_local)  
    # Si el visitante no existe, lo creamos
    if not clasificacion_visitante:
        clasificacion_visitante = Clasificacion( equipo=visitante, jugados=0, ganados=0, perdidos=0, puntos=0, pf=0, pc=0)
        db.session.add(clasificacion_visitante)   
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_local.jugados += 1
        clasificacion_visitante.jugados += 1       
        # Determinar el resultado del partido y actualizar clasificaciones
        if resultado_local > resultado_visitante:
            clasificacion_local.ganados += 1
            clasificacion_local.puntos += 2
            clasificacion_visitante.perdidos += 1
            clasificacion_visitante.puntos += 1
        elif resultado_local < resultado_visitante:
            clasificacion_visitante.ganados += 1
            clasificacion_visitante.puntos += 2
            clasificacion_local.perdidos += 1
            clasificacion_local.puntos += 1
        else:
            clasificacion_local.puntos += 1
            clasificacion_visitante.puntos += 1  
    # Guardar los cambios en la base de datos
    db.session.commit()
    return clasificacion_local, clasificacion_visitante
def obtener_jornadas_liga():
    jornadas = {}

    partidos = CopaUEMC.query.filter(
        CopaUEMC.encuentros.like('liga_%')
    ).order_by(CopaUEMC.orden, CopaUEMC.id).all()

    for partido in partidos:
        jornada = partido.encuentros  # liga_j1, liga_j2...
        if jornada not in jornadas:
            jornadas[jornada] = []
        jornadas[jornada].append(partido)
    return jornadas
def obtener_eliminatorias():
    fases = ['dieciseisavos', 'octavos', 'cuartos', 'semifinales', 'final']
    eliminatorias = {fase: [] for fase in fases}

    partidos = CopaUEMC.query.filter(CopaUEMC.encuentros.in_(fases)).order_by(CopaUEMC.orden).all()

    for partido in partidos:
        eliminatorias[partido.encuentros].append(partido)

    return eliminatorias
# Recalcular clasificación
def recalcular_clasificacion(jornadas):
    clasificacion = {}

    for jornada, partidos in jornadas.items():
        for p in partidos:
            if not p.local or not p.visitante:
                continue
            
            local = p.local.strip()
            visitante = p.visitante.strip()

            if local not in clasificacion:
                clasificacion[local] = {
                    'equipo': local, 'jugados': 0, 'ganados': 0,
                    'perdidos': 0, 'puntos': 0, 'favor': 0, 'contra': 0
                }

            if visitante not in clasificacion:
                clasificacion[visitante] = {
                    'equipo': visitante, 'jugados': 0, 'ganados': 0,
                    'perdidos': 0, 'puntos': 0, 'favor': 0, 'contra': 0
                }

            # 👉 si no hay resultado, NO se calcula nada más
            if not p.resultadoA or not p.resultadoB:
                continue

            if p.resultadoA is None or p.resultadoB is None:
                continue

            resA = int(p.resultadoA)
            resB = int(p.resultadoB)

            clasificacion[local]['jugados'] += 1
            clasificacion[visitante]['jugados'] += 1

            clasificacion[local]['favor'] += resA
            clasificacion[local]['contra'] += resB
            clasificacion[visitante]['favor'] += resB
            clasificacion[visitante]['contra'] += resA

            if resA > resB:
                clasificacion[local]['ganados'] += 1
                clasificacion[local]['puntos'] += 2
                clasificacion[visitante]['perdidos'] += 1
                clasificacion[visitante]['puntos'] += 1
            elif resA < resB:
                clasificacion[visitante]['ganados'] += 1
                clasificacion[visitante]['puntos'] += 2
                clasificacion[local]['perdidos'] += 1
                clasificacion[local]['puntos'] += 1
            else:
                clasificacion[local]['puntos'] += 1
                clasificacion[visitante]['puntos'] += 1

    clasificacion_ordenada = sorted(
        clasificacion.items(),
        key=lambda x: (
            -x[1]["puntos"],
            -(x[1]["favor"] - x[1]["contra"]),
            -x[1]["favor"]
        )
    )

    return clasificacion_ordenada
# Modificar los partidos de los playoff
@uemc_route_bp.route('/modificar_copa_uemc/<string:encuentros>', methods=['POST'])
def modificar_copa_uemc(encuentros):
    try:
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            partido = CopaUEMC.query.get(int(partido_id))
            if partido:
                partido.fecha = request.form.get(f'fecha{i}', partido.fecha)
                partido.hora = request.form.get(f'hora{i}', partido.hora)
                partido.local = request.form.get(f'local{i}', partido.local)
                partido.resultadoA = request.form.get(f'resultadoA{i}', partido.resultadoA)
                partido.resultadoB = request.form.get(f'resultadoB{i}', partido.resultadoB)
                partido.visitante = request.form.get(f'visitante{i}', partido.visitante)
                partido.encuentros = encuentros
            db.session.commit()
            flash('Partidos modificados correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error al modificar partidos: {e}")
        flash('Hubo un error al modificar los partidos', 'error')
    return redirect(url_for('uemc_route_bp.ver_copa_uemc'))
# Eliminar partidos Copa UEMC
@uemc_route_bp.route('/eliminar_copa_uemc/<string:identificador>', methods=['POST'])
def eliminar_copa_uemc(identificador):
    partidos = CopaUEMC.query.filter_by(encuentros=identificador).all()

    for p in partidos:
        db.session.delete(p)

    db.session.commit()
    return redirect(url_for('uemc_route_bp.ver_copa_uemc'))
# Mostrar la Copa UEMC
@uemc_route_bp.route('/uemc_copa/')
def uemc_copa():
    jornadas = obtener_jornadas_liga()
    clasificacion = recalcular_clasificacion(jornadas)
    eliminatorias = obtener_eliminatorias()
    return render_template('copas/uemc_copa.html', jornadas=jornadas, clasificacion=clasificacion, eliminatorias=eliminatorias
    )

# PLAYOFF UEMC
# Crear formulario para los playoff
@uemc_route_bp.route('/crear_playoff_uemc', methods=['GET', 'POST'])
def crear_playoff_uemc():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'ascenso': 2,
            'octavos': 14,
            'cuartos': 8,
            'semifinales': 4,
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        
        for i in range(num_partidos):
            resultadoA_raw = request.form.get(f'resultadoA{i}')
            resultadoB_raw = request.form.get(f'resultadoB{i}')

            resultadoA = int(resultadoA_raw) if resultadoA_raw not in ("", "None", None) else None
            resultadoB = int(resultadoB_raw) if resultadoB_raw not in ("", "None", None) else None
            partido = PlayoffUEMC(
                eliminatoria = eliminatoria,
                fecha = request.form.get(f'fecha{i}', ''),
                hora = request.form.get(f'hora{i}', ''),
                local = request.form.get(f'local{i}', ''),
                resultadoA = resultadoA,
                resultadoB = resultadoB,
                visitante = request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('uemc_route_bp.ver_playoff_uemc'))
    return render_template('admin/playoffs/playoff_uemc.html')
# Ver encuentros playoff en Admin
@uemc_route_bp.route('/playoff_uemc/')
def ver_playoff_uemc():
    eliminatorias = ['ascenso', 'octavos','cuartos', 'semifinales']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffUEMC.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffUEMC.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_uemc.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@uemc_route_bp.route('/modificar_playoff_uemc/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_uemc(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))

        for i in range(num_partidos):

            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue

            partido_obj = PlayoffUEMC.query.get(int(partido_id))
            if not partido_obj:
                continue

            # 🔥 AQUÍ es donde tienes que coger los valores
            resultadoA_raw = request.form.get(f'resultadoA{i}')
            resultadoB_raw = request.form.get(f'resultadoB{i}')

            # 🔥 convertir correctamente
            resultadoA = int(resultadoA_raw) if resultadoA_raw not in ("", "None", None) else None
            resultadoB = int(resultadoB_raw) if resultadoB_raw not in ("", "None", None) else None

            # actualizar datos
            partido_obj.fecha = request.form.get(f'fecha{i}', '')
            partido_obj.hora = request.form.get(f'hora{i}', '')
            partido_obj.local = request.form.get(f'local{i}', '')
            partido_obj.resultadoA = resultadoA
            partido_obj.resultadoB = resultadoB
            partido_obj.visitante = request.form.get(f'visitante{i}', '')
            partido_obj.orden = i

        db.session.commit()
        flash('Playoff actualizado correctamente', 'success')
        return redirect(url_for('uemc_route_bp.ver_playoff_uemc'))

    return redirect(url_for('uemc_route_bp.ver_playoff_uemc'))
# Eliminar los partidos de los playoff
@uemc_route_bp.route('/eliminar_playoff_uemc/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_uemc(eliminatoria):
    partidos = PlayoffUEMC.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('uemc_route_bp.ver_playoff_uemc'))
# Mostrar los playoffs del UEMC
@uemc_route_bp.route('/playoffs_uemc/')
def playoffs_uemc():
    eliminatorias = ['ascenso', 'octavos','cuartos', 'semifinales']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffUEMC.query.filter_by(eliminatoria=eliminatoria).all()
        datos_europa[eliminatoria] = partidos
    return render_template('playoff/uemc_playoff.html', datos_europa=datos_europa)