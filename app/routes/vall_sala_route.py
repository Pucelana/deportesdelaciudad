from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from collections import OrderedDict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.historial import obtener_evolucion_puntos
from ..models.historial import Historial, Palmaress
from ..models.vall_sala import JornadaVallSala, VallSalaPartido, VallSalaClub, CopaVallSala, PlayoffVallSala, TemporadaVallSala

vall_sala_route_bp = Blueprint('vall_sala_route_bp', __name__)

# LIGA VALLADOLID S.S
# Crear el calendario Valladolid S.S
@vall_sala_route_bp.route('/crear_calendario_vall_sala', methods=['GET', 'POST'])
def ingresar_resultado_vall_sala():
    if request.method == 'POST':
        temporada_nombre = request.form['temporada']
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaVallSala.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaVallSala(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaVallSala(
            nombre=nombre_jornada,
            temporada_id=temporada.id
        )
        db.session.add(jornada)
        db.session.flush()        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            partido = VallSalaPartido(
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
        return redirect(url_for('vall_sala_route_bp.calendarios_vall_sala'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_vall_sala.html')
# Ver calendario Valladolid S.S en Admin
@vall_sala_route_bp.route('/calendarios_vall_sala')
def calendarios_vall_sala():
    temporada = TemporadaVallSala.query.filter_by(activa=True).first()
    if temporada:
        jornadas = JornadaVallSala.query.filter_by(
        temporada_id=temporada.id
        ).order_by(JornadaVallSala.id.asc()).all()
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(VallSalaPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(VallSalaPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_vall_sala.html', jornadas=jornadas)
# Modificar jornada
@vall_sala_route_bp.route('/modificar_jornada_vall_sala/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_vall_sala(id):
    jornada = db.session.query(JornadaVallSala).filter(JornadaVallSala.id == id).first()
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
                partido = db.session.query(VallSalaPartido).filter(VallSalaPartido.id == partido_id).first()
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
            return redirect(url_for('vall_sala_route_bp.calendarios_vall_sala'))
    return render_template('admin/calendarios/calend_vall_sala.html', jornada=jornada)
# Eliminar jornada
@vall_sala_route_bp.route('/eliminar_jornada_vall_sala/<int:id>', methods=['GET','POST'])
def eliminar_jornada_vall_sala(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaVallSala).filter(JornadaVallSala.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(VallSalaPartido).filter(VallSalaPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('vall_sala_route_bp.calendarios_vall_sala'))    
# Obtener datos Valladolid S.S
def obtener_datos_vall_sala(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaVallSala.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaVallSala.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            VallSalaPartido.query
            .filter_by(jornada_id=jornada.id)
            .order_by(VallSalaPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({
            'nombre': jornada.nombre,
            'partidos': partidos
        })
    return jornadas_con_partidos
# Calendario Valladolid S.S
@vall_sala_route_bp.route('/equipos_futsal/calendario_vall_sala')
def calendario_vall_sala():
    datos = obtener_datos_vall_sala()
    equipo_vall_sala = 'FS Valladolid'
    tabla_partidos_vall_sala = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Valladolid S.S está jugando
            if equipo_local == equipo_vall_sala or equipo_visitante == equipo_vall_sala:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_vall_sala:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vall_sala = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vall_sala = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vall_sala:
                    tabla_partidos_vall_sala[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_vall_sala[equipo_contrario]:
                    tabla_partidos_vall_sala[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vall_sala[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_vall_sala[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_vall_sala[equipo_contrario]:
                    tabla_partidos_vall_sala[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vall_sala[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_vall_sala[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_vall_sala[equipo_contrario]['jornadas']:
                    tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_vall_sala': rol_vall_sala
                    }               
                # Asignamos los resultados según el rol del Valladolid S.S
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vall_sala'] = rol_vall_sala
                    else:
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vall_sala'] = rol_vall_sala
                else:
                    if not tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vall_sala'] = rol_vall_sala
                    else:
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAAA'] = resultado_a
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBBB'] = resultado_b
                        tabla_partidos_vall_sala[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vall_sala'] = rol_vall_sala
    return render_template('equipos_vall/calendario_vall_sala.html', tabla_partidos_vall_sala=tabla_partidos_vall_sala)
# Jornadas Valladolid S.S
@vall_sala_route_bp.route('/equipos_futsal/resultados_vall_sala')
def resultados_vall_sala():
    datos = obtener_datos_vall_sala()
    nuevos_datos_vall_sala = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_vall_sala):
        jornada_completa = all(
            p.resultadoA not in (None, "") and
            p.resultadoB not in (None, "")
            for p in jornada['partidos']
        )
        if not jornada_completa:
            jornada_activa = jornada['nombre']
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_vall_sala:
        jornada_activa = nuevos_datos_vall_sala[-1]['nombre']
    return render_template(
        'equipos_vall/jornadas_vall_sala.html',
        nuevos_datos_vall_sala=nuevos_datos_vall_sala,
        jornada_activa=jornada_activa
    )
# Jornada 0 Valladolid S.S
@vall_sala_route_bp.route('/jornada0_vall_sala', methods=['GET', 'POST'])
def jornada0_vall_sala():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = VallSalaClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('vall_sala_route_bp.jornada0_vall_sala'))
    clubs = VallSalaClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_vall_sala.html', clubs=clubs)
# Eliminar clubs jornada 0
@vall_sala_route_bp.route('/eliminar_club_vall_sala/<int:club_id>', methods=['POST'])
def eliminar_club_vall_sala(club_id):
    club = VallSalaClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('vall_sala_route_bp.jornada0_vall_sala'))
# Crear la clasificación RV Galvan
def generar_clasificacion_analisis_futsal_vall_sala(data):
    clasificacion = defaultdict(lambda: {
        'jugados': 0,
        'ganados': 0,
        'empatados': 0,
        'perdidos': 0,
        'favor': 0,
        'contra': 0,
        'diferencia_goles': 0,
        'puntos': 0
    })

    # ================================
    # ENFRENTAMIENTOS DIRECTOS
    # ================================
    enfrentamientos = defaultdict(list)

    # ================================
    # RECORRER PARTIDOS
    # ================================
    for jornada in data:

        for partido in jornada['partidos']:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if (
                r1 is None or r2 is None or
                r1 == '' or r2 == ''
            ):
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

                clasificacion[local]['puntos'] += 3
                clasificacion[local]['ganados'] += 1
                clasificacion[visitante]['perdidos'] += 1

            elif r1 < r2:

                clasificacion[visitante]['puntos'] += 3
                clasificacion[visitante]['ganados'] += 1
                clasificacion[local]['perdidos'] += 1

            else:

                clasificacion[local]['puntos'] += 1
                clasificacion[visitante]['puntos'] += 1

                clasificacion[local]['empatados'] += 1
                clasificacion[visitante]['empatados'] += 1

            # ================================
            # JUGADOS
            # ================================
            clasificacion[local]['jugados'] += 1
            clasificacion[visitante]['jugados'] += 1

            # ================================
            # GOLES
            # ================================
            clasificacion[local]['favor'] += r1
            clasificacion[local]['contra'] += r2

            clasificacion[visitante]['favor'] += r2
            clasificacion[visitante]['contra'] += r1

            clasificacion[local]['diferencia_goles'] += (r1 - r2)
            clasificacion[visitante]['diferencia_goles'] += (r2 - r1)

            # ================================
            # ENFRENTAMIENTOS DIRECTOS
            # ================================
            enfrentamientos[frozenset([local, visitante])].append({
                'local': local,
                'visitante': visitante,
                'goles_local': r1,
                'goles_visitante': r2
            })

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

            l = p['local']
            v = p['visitante']
            gl = p['goles_local']
            gv = p['goles_visitante']

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
            'puntos_a': puntos_a,
            'puntos_b': puntos_b,
            'diff_a': goles_a - goles_b,
            'diff_b': goles_b - goles_a
        }

    # ================================
    # COMPARADOR PRO OFICIAL
    # ================================
    def comparar(a, b):

        na, da = a
        nb, db = b

        # 1. puntos
        if da['puntos'] != db['puntos']:
            return db['puntos'] - da['puntos']

        # 2. enfrentamiento directo
        av = average_particular(na, nb)

        if av:

            if av['puntos_a'] != av['puntos_b']:
                return av['puntos_b'] - av['puntos_a']

            if av['diff_a'] != av['diff_b']:
                return av['diff_b'] - av['diff_a']

        # 3. diferencia goles
        if da['diferencia_goles'] != db['diferencia_goles']:
            return db['diferencia_goles'] - da['diferencia_goles']

        # 4. goles a favor
        return db['favor'] - da['favor']

    # ================================
    # ORDEN FINAL
    # ================================
    equipos = list(clasificacion.items())
    equipos.sort(key=cmp_to_key(comparar))

    return [
        {'equipo': e, 'datos': d}
        for e, d in equipos
    ]
# Ruta para mostrar la clasificación y análisis del Valladolid S.S
@vall_sala_route_bp.route('/equipos_futsal/clasif_vall_sala')
def clasif_analisis_vall_sala():
    data = obtener_datos_vall_sala()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_vall_sala = generar_clasificacion_analisis_futsal_vall_sala(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_vall_sala = VallSalaClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_vall_sala:
        if not any(
            equipo['equipo'] == club.nombre
            for equipo in clasificacion_analisis_vall_sala
        ):

            clasificacion_analisis_vall_sala.append({
                'equipo': club.nombre,
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            })

    clasificacion_analisis_vall_sala.sort(
        key=lambda x: x['datos']['puntos'],
        reverse=True
    )
    return render_template('equipos_vall/clasif_vall_sala.html',
        clasificacion_analisis_vall_sala=clasificacion_analisis_vall_sala)
# TEMPORADAS RV Promesas
@vall_sala_route_bp.route('/temporadas_vall_sala')
def temporadas_vall_sala():
    temporadas = TemporadaVallSala.query.order_by(
        TemporadaVallSala.id.desc()
    ).all()
    return render_template(
        'admin/temporadas/temporada_vall_sala.html',
        temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@vall_sala_route_bp.route('/activar_temporada_vall_sala/<int:id>')
def activar_temporada_vall_sala(id):
    TemporadaVallSala.query.update({"activa": False})
    temporada = TemporadaVallSala.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for('vall_sala_route_bp.temporadas_vall_sala'))

# HISTORIAL FS VALLADOLID
# Creación del historial de temporadas del FS Valladolid
@vall_sala_route_bp.route("/admin/crear_historial_vall_sala", methods=["GET", "POST"])
def crear_historial_vall_sala():
    if request.method == "POST":
        historial = Historial(
            deporte="futbol sala",
            equipo="FS Valladolid",
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
        return redirect(url_for("vall_sala_route_bp.crear_historial_vall_sala"))
    historial = (Historial.query.filter_by(
        deporte="futbol sala",
        equipo="FS Valladolid"
    ).order_by(Historial.temporada.desc()).all()
                 )
    temporadas = TemporadaVallSala.query.order_by(
        TemporadaVallSala.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial.html",
        historial=historial,
        temporadas=temporadas,
        deporte="futbol sala",
        equipo="FS Valladolid",
        crear_url="vall_sala_route_bp.crear_historial_vall_sala",
        modificar_url="vall_sala_route_bp.modificar_historial_vall_sala",
        eliminar_url="vall_sala_route_bp.eliminar_historial_vall_sala"
    )
@vall_sala_route_bp.route("/admin/eliminar_historial_vall_sala/<int:id>", methods=["POST"])
def eliminar_historial_vall_sala(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("vall_sala_route_bp.crear_historial_vall_sala"))
# Modificar historial de temporadas del FS Valladolid
@vall_sala_route_bp.route("/admin/modificar_historial_vall_sala/<int:id>", methods=["POST"])
def modificar_historial_vall_sala(id):
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
    return redirect(url_for("vall_sala_route_bp.crear_historial_vall_sala"))
# Ver Historial de temporadas del FS Valladolid en la página principal
@vall_sala_route_bp.route("/vall_sala/historial")
def historial_vall_sala():
    historial = (Historial.query.filter_by(
        deporte="futbol sala",
        equipo="FS Valladolid"
    ).order_by(Historial.temporada.desc()).all())
    # GRÁFICO TEMPORADAS
    labels_temporadas = [h.temporada for h in historial]
    puntos_temporadas = [h.puntos for h in historial]
    # GRÁFICO JORNADAS
    temporadas = TemporadaVallSala.query.order_by(TemporadaVallSala.id).all()
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
            deporte="futbol sala",
            equipo="FS Valladolid"
        ).order_by(Palmaress.orden.asc(),Palmaress.temporada.desc()).all())
    palmares = OrderedDict()
    for titulo in titulos:
        if titulo.competicion not in palmares:
            palmares[titulo.competicion] = []
        palmares[titulo.competicion].append(titulo)
    labels_jornadas = []
    for i, temporada in enumerate(temporadas):
        jornadas = (
            JornadaVallSala.query.filter_by(temporada_id=temporada.id)
            .order_by(JornadaVallSala.id)
            .all()
        )
        if not jornadas:
            continue
        labels, puntos = obtener_evolucion_puntos(
            jornadas, "FS Valladolid", generar_clasificacion_analisis_futsal_vall_sala,"puntos"
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
        "historia/historia_vall_sala.html",
        historial=historial,
        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,
        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,
        palmares=palmares,
        deporte="Fútbol sala",
        equipo="FS Valladolid"
  )

# PALMARES FS VALLADOLID
# Crear Palmares del FS Valladolid
@vall_sala_route_bp.route("/admin/crear_palmares_vall_sala", methods=["GET", "POST"])
def crear_palmares_vall_sala():
    if request.method == "POST":
        titulo = Palmaress(
            deporte="futbol sala",
            equipo="FS Valladolid",
            temporada=request.form.get("temporada"),
            competicion=request.form.get("competicion"),
            imagen=request.form.get("imagen"),
            orden=int(request.form.get("orden", 0))
        )
        db.session.add(titulo)
        db.session.commit()
        return redirect(url_for("vall_sala_route_bp.crear_palmares_vall_sala"))
    palmares = (
        Palmaress.query.filter_by(
            deporte="futbol sala",
            equipo="FS Valladolid"
        )
        .order_by( Palmaress.orden.asc(),Palmaress.temporada.desc())
        .all()
    )
    return render_template(
        "admin/historial/palmares.html",
        palmares=palmares,
        deporte="Fútbol sala",
        equipo="FS Valladolid",
        crear_url="vall_sala_route_bp.crear_palmares_vall_sala",
        modificar_url="vall_sala_route_bp.modificar_palmares_vall_sala",
        eliminar_url="vall_sala_route_bp.eliminar_palmares_vall_sala",
    )
# Modificar Palmares del FS Valladolid
@vall_sala_route_bp.route("/admin/modificar_palmares_vall_sala/<int:id>", methods=["POST"])
def modificar_palmares_vall_sala(id):
    titulo = Palmaress.query.get_or_404(id)
    titulo.temporada = request.form.get("temporada")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    titulo.orden = request.form.get("orden")
    db.session.commit()
    return redirect(url_for("galvan_route_bp.crear_palmares_galvan"))
# Eliminar Palmares del FS Valladolid
@vall_sala_route_bp.route("/admin/eliminar_palmares_vall_sala/<int:id>", methods=["POST"])
def eliminar_palmares_vall_sala(id):
    titulo = Palmaress.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("vall_sala_route_bp.crear_palmares_vall_sala"))

# COPA DEL REY Valladolid S.S
# Creación de las eliminatorias de copa
@vall_sala_route_bp.route('/crear_copa_vall_sala', methods=['GET', 'POST'])
def crear_copa_vall_sala():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')
        max_partidos = {
            'ronda1': 16,
            'ronda2': 8,
            'ronda3': 8,
            'octavos': 8,
            'cuartos': 4,
            'semifinales': 4,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos = int(request.form.get('num_partidos', '0').strip() or 0)
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaVallSala(
                eliminatoria=eliminatoria,
                fecha=request.form.get(f'fecha{i}', ''),
                hora=request.form.get(f'hora{i}', ''),
                local=request.form.get(f'local{i}', ''),
                resultadoA=request.form.get(f'resultadoA{i}', ''),
                resultadoB=request.form.get(f'resultadoB{i}', ''),
                visitante=request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('vall_sala_route_bp.ver_copa_vall_sala'))
    return render_template('admin/copa/copa_vall_sala.html')   
# Ver las eliminatorias en Admin
@vall_sala_route_bp.route('/copa_vall_sala/')
def ver_copa_vall_sala():
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {
        e: CopaVallSala.query.filter_by(eliminatoria=e).all()
        for e in eliminatorias
    }
    return render_template('admin/copa/copa_vall_sala.html', datos_eliminatorias=datos_eliminatorias)
# Modificar las eliminatorias
@vall_sala_route_bp.route('/modificar_copa_vall_sala_post', methods=['POST'])
def modificar_copa_vall_sala_post():
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        partido = CopaVallSala.query.get(partido_id)
        if partido:
            partido.eliminatoria = eliminatoria  # Opcional: si quieres actualizarla por partido
            partido.fecha = request.form.get(f'fecha{i}', '')
            partido.hora = request.form.get(f'hora{i}', '')
            partido.local = request.form.get(f'local{i}', '')
            partido.resultadoA = request.form.get(f'resultadoA{i}', '')
            partido.resultadoB = request.form.get(f'resultadoB{i}', '')
            partido.visitante = request.form.get(f'visitante{i}', '')
    db.session.commit()
    return redirect(url_for('vall_sala_route_bp.ver_copa_vall_sala'))
# Eliminar las eliminatorias en Admin
@vall_sala_route_bp.route('/eliminar_copa_vall_sala/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_vall_sala(eliminatoria):
    CopaVallSala.query.filter_by(eliminatoria=eliminatoria).delete()
    db.session.commit()
    return redirect(url_for('vall_sala_route_bp.ver_copa_vall_sala'))
# Ver las eliminatorias en la página principal Copa
@vall_sala_route_bp.route('/vall_sala_copa/')
def copas_vall_sala():
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_copa = {
        e: CopaVallSala.query.filter_by(eliminatoria=e).all()
        for e in eliminatorias
    }
    return render_template('copas/vall_sala_copa.html', datos_copa=datos_copa)

# PLAYOFF ASCENSO Valladolid S.S
# Crear formulario para los playoff
@vall_sala_route_bp.route('/crear_playoff_vall_sala', methods=['GET', 'POST'])
def crear_playoff_vall_sala():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'cuartos': 8,
            'semifinales': 4,
            'final': 2
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        # 🧹 Eliminar partidos ANTES de agregar nuevos
        PlayoffVallSala.query.filter_by(eliminatoria=eliminatoria).delete()
        
        for i in range(num_partidos):
            partido = PlayoffVallSala(
                eliminatoria = eliminatoria,
                fecha = request.form.get(f'fecha{i}', ''),
                hora = request.form.get(f'hora{i}', ''),
                local = request.form.get(f'local{i}', ''),
                resultadoA = request.form.get(f'resultadoA{i}', ''),
                resultadoB = request.form.get(f'resultadoB{i}', ''),
                visitante = request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('vall_sala_route_bp.ver_playoff_vall_sala'))
    return render_template('admin/playoffs/playoff_vall_sala.html')
# Ver encuentros playoff en Admin
@vall_sala_route_bp.route('/playoff_vall_sala/')
def ver_playoff_vall_sala():
    eliminatorias = ['cuartos','semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffVallSala.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffVallSala.orden).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_vall_sala.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@vall_sala_route_bp.route('/modificar_playoff_vall_sala/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_vall_sala(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffVallSala.query.get(int(partido_id))
            if not partido_obj:
                continue
            partido_obj.fecha = request.form.get(f'fecha{i}', '')
            partido_obj.hora = request.form.get(f'hora{i}', '')
            partido_obj.local = request.form.get(f'local{i}', '')
            partido_obj.resultadoA = request.form.get(f'resultadoA{i}', '')
            partido_obj.resultadoB = request.form.get(f'resultadoB{i}', '')
            partido_obj.visitante = request.form.get(f'visitante{i}', '')
            partido_obj.orden = i
        # Commit para guardar los cambios
        db.session.commit()
        flash('Playoff actualizado correctamente', 'success')
        return redirect(url_for('vall_sala_route_bp.ver_playoff_vall_sala'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('vall_sala_route_bp.ver_playoff_vall_sala'))
# Eliminar los partidos de los playoff
@vall_sala_route_bp.route('/eliminar_playoff_vall_sala/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_vall_sala(eliminatoria):
    partidos = PlayoffVallSala.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('vall_sala_route_bp.ver_playoff_vall_sala'))
# Mostrar los playoffs del Valladolid S.S
@vall_sala_route_bp.route('/playoffs_vall_sala/')
def playoffs_vall_sala():
    eliminatorias = ['cuartos','semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffVallSala.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('playoff/vall_sala_playoff.html', datos_playoff=datos_playoff)