from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.historial import obtener_evolucion_puntos
from ..models.historial import Historial, Palmaress
from ..models.simancas import JornadaSimancas, SimancasPartido, SimancasClub, CopaSimancas, PlayoffSimancas, TemporadaSimancas

simancas_route_bp = Blueprint('simancas_route_bp', __name__)

# LIGA RV SIMANCAS
# Crear el calendario RV Simancas
@simancas_route_bp.route('/crear_calendario_simancas', methods=['GET', 'POST'])
def ingresar_resultado_simancas():
    if request.method == 'POST':
        temporada_nombre = request.form['temporada']
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        temporada = TemporadaSimancas.query.filter_by(nombre=temporada_nombre).first()
        if not temporada:
            temporada = TemporadaSimancas(nombre=temporada_nombre, activa=False)
            db.session.add(temporada)
            db.session.flush()
        # 2. crear jornada correcta
        jornada = JornadaSimancas(
            nombre=nombre_jornada,
            temporada_id=temporada.id
        )
        db.session.add(jornada)
        db.session.flush()        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            partido = SimancasPartido(
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
        return redirect(url_for('simancas_route_bp.calendarios_simancas'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_simancas.html')
# Ver calendario Real Valladolid en Admin
@simancas_route_bp.route('/calendario_simancas')
def calendarios_simancas():
    temporada = TemporadaSimancas.query.filter_by(activa=True).first()
    if temporada:
        jornadas = JornadaSimancas.query.filter_by(
        temporada_id=temporada.id
        ).order_by(JornadaSimancas.id.asc()).all()
    else:
        jornadas = []
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(SimancasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(SimancasPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_simancas.html', jornadas=jornadas)
# Modificar jornada
@simancas_route_bp.route('/modificar_jornada_simancas/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_simancas(id):
    jornada = db.session.query(JornadaSimancas).filter(JornadaSimancas.id == id).first()
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
                partido = db.session.query(SimancasPartido).filter(SimancasPartido.id == partido_id).first()
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
            return redirect(url_for('simancas_route_bp.calendarios_simancas'))
    return render_template('admin/calendarios/calend_simancas.html', jornada=jornada)
# Eliminar jornada
@simancas_route_bp.route('/eliminar_jornada_simancas/<int:id>', methods=['GET','POST'])
def eliminar_jornada_simancas(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaSimancas).filter(JornadaSimancas.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(SimancasPartido).filter(SimancasPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('simancas_route_bp.calendarios_simancas'))    
# Obtener datos RV Simancas
def obtener_datos_simancas(nombre_temporada=None):
    if nombre_temporada is None:
        temporada = TemporadaSimancas.query.filter_by(activa=True).first()
    else:
        temporada = TemporadaSimancas.query.filter_by(nombre=nombre_temporada).first()
    if not temporada:
        return []
    jornadas_con_partidos = []
    for jornada in temporada.jornadas:
        partidos = (
            SimancasPartido.query
            .filter_by(jornada_id=jornada.id)
            .order_by(SimancasPartido.orden.asc())
            .all()
        )
        jornadas_con_partidos.append({
            'nombre': jornada.nombre,
            'partidos': partidos
        })
    return jornadas_con_partidos
# Calendario Real Valladolid
@simancas_route_bp.route('/equipos_futbol/calendario_rv_fem')
def calendario_simancas():
    datos = obtener_datos_simancas()
    equipo_simancas = 'RV Femenino'
    tabla_partidos_simancas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_simancas or equipo_visitante == equipo_simancas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_simancas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_simancas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_simancas = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_simancas:
                    tabla_partidos_simancas[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_simancas[equipo_contrario]:
                    tabla_partidos_simancas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_simancas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_simancas[equipo_contrario]:
                    tabla_partidos_simancas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_simancas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_simancas[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_simancas[equipo_contrario]['jornadas']:
                    tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_simancas': rol_simancas
                    }               
                # Asignamos los resultados según el rol del RV Simancas
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
                    else:
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
                else:
                    if not tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
                    else:
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_simancas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_simancas'] = rol_simancas
    return render_template('equipos_vall/calendario_rv_fem.html', tabla_partidos_simancas=tabla_partidos_simancas)
# Jornadas Simancas
@simancas_route_bp.route('/equipos_futbol/resultados_rv_fem')
def resultados_simancas():
    datos = obtener_datos_simancas()
    nuevos_datos_simancas = [dato for dato in datos if dato]
    jornada_activa = None
    # Buscar primera jornada sin completar
    for i, jornada in enumerate(nuevos_datos_simancas):
        jornada_completa = all(
            p.resultadoA not in (None, "") and
            p.resultadoB not in (None, "")
            for p in jornada['partidos']
        )
        if not jornada_completa:
            jornada_activa = jornada['nombre']
            break
    # Si todas están completas mostrar la última
    if jornada_activa is None and nuevos_datos_simancas:
        jornada_activa = nuevos_datos_simancas[-1]['nombre']
    return render_template(
        'equipos_vall/jornadas_rv_fem.html',
        nuevos_datos_simancas=nuevos_datos_simancas,
        jornada_activa=jornada_activa
    )
# Jornada 0 RV Simancas
@simancas_route_bp.route('/jornada0_simancas', methods=['GET', 'POST'])
def jornada0_simancas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = SimancasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('simancas_route_bp.jornada0_simancas'))
    clubs = SimancasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_simancas.html', clubs=clubs)
# Eliminar clubs jornada 0
@simancas_route_bp.route('/eliminar_club_simancas/<int:club_id>', methods=['POST'])
def eliminar_club_simancas(club_id):
    club = SimancasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('simancas_route_bp.jornada0_simancas'))
# Crear la clasificación RV Simancas
def generar_clasificacion_analisis_futbol_simancas(data):
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
# Ruta para mostrar la clasificación y análisis del UEMC
@simancas_route_bp.route('/equipos_futbol/clasif_rv_fem')
def clasif_analisis_simancas():
    data = obtener_datos_simancas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_simancas = generar_clasificacion_analisis_futbol_simancas(data)
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_simancas = SimancasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_simancas:

        if not any(
            equipo['equipo'] == club.nombre
            for equipo in clasificacion_analisis_simancas
        ):

            clasificacion_analisis_simancas.append({
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

    clasificacion_analisis_simancas.sort(
        key=lambda x: x['datos']['puntos'],
        reverse=True
    )
    return render_template('equipos_vall/clasif_rv_fem.html',
        clasificacion_analisis_simancas=clasificacion_analisis_simancas)
# TEMPORADAS RV Promesas
@simancas_route_bp.route('/temporadas_simancas')
def temporadas_simancas():
    temporadas = TemporadaSimancas.query.order_by(
        TemporadaSimancas.id.desc()
    ).all()
    return render_template(
        'admin/temporadas/temporada_simancas.html',
        temporadas=temporadas
    )
# ACTIVAR Y DESACTIVAR TEMPORADAS
@simancas_route_bp.route('/activar_temporada_simancas/<int:id>')
def activar_temporada_simancas(id):
    TemporadaSimancas.query.update({"activa": False})
    temporada = TemporadaSimancas.query.get_or_404(id)
    temporada.activa = True
    db.session.commit()
    return redirect(url_for('simancas_route_bp.temporadas_simancas')) 

# HISTORIAL RV FEMENINO
# Creación del historial de temporadas del RV Femenino
@simancas_route_bp.route("/admin/crear_historial_simancas", methods=["GET", "POST"])
def crear_historial_simancas():
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
        return redirect(url_for("simancas_route_bp.crear_historial_simancas"))
    historial = (Historial.query.filter_by(
        deporte="futbol",
        equipo="RV Femenino"
    ).order_by(Historial.temporada.desc()).all()
                 )
    temporadas = TemporadaSimancas.query.order_by(
        TemporadaSimancas.nombre.desc()
    ).all()
    return render_template(
        "admin/historial/historial.html",
        historial=historial,
        temporadas=temporadas,
        deporte="futbol",
        equipo="RV Femenino",
        crear_url="simancas_route_bp.crear_historial_simancas",
        modificar_url="simancas_route_bp.modificar_historial_simancas",
        eliminar_url="simancas_route_bp.eliminar_historial_simancas"
    )
@simancas_route_bp.route("/admin/eliminar_historial_simancas/<int:id>", methods=["POST"])
def eliminar_historial_simancas(id):
    historial = Historial.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return redirect(url_for("simancas_route_bp.crear_historial_simancas"))
@simancas_route_bp.route("/admin/modificar_historial_simancas/<int:id>", methods=["POST"])
def modificar_historial_simancas(id):
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
    return redirect(url_for("simancas_route_bp.crear_historial_simancas"))
# Ver Historial de temporadas del RV Femenino en la página principal
@simancas_route_bp.route("/simancas/historial")
def historial_promesas():
    historial = (Historial.query.filter_by(
        deporte="futbol",
        equipo="RV Femenino"
    ).order_by(Historial.temporada.desc()).all())
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
    titulos = (Palmaress.query.filter_by(
            deporte="futbol",
            equipo="RV Femenino"
        ).order_by(Palmaress.temporada.desc()).all())

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
            jornadas, "RV Femenino", generar_clasificacion_analisis_futbol_simancas,"puntos"
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
        "historia/historia_simancas.html",
        historial=historial,
        labels_temporadas=labels_temporadas,
        puntos_temporadas=puntos_temporadas,
        labels_jornadas=labels_jornadas,
        datasets_jornadas=datasets_jornadas,
        titulos=titulos,
        deporte="Fútbol",
        equipo="RV Femennino"
  )

# PALMARES RV FEMENINO
# Crear Palmares del RV Femenino
@simancas_route_bp.route("/admin/crear_palmares_simancas", methods=["GET", "POST"])
def crear_palmares_simancas():
    if request.method == "POST":
        titulo = Palmaress(
            deporte="futbol",
            equipo="RV Femenino",
            temporada=request.form.get("temporada"),
            competicion=request.form.get("competicion"),
            imagen=request.form.get("imagen"),
        )
        db.session.add(titulo)
        db.session.commit()
        return redirect(url_for("simancas_route_bp.crear_palmares_simancas"))
    palmares = (
        Palmaress.query.filter_by(
            deporte="futbol",
            equipo="RV Femenino"
        )
        .order_by(Palmaress.temporada.desc())
        .all()
    )
    return render_template(
        "admin/historial/palmares.html",
        palmares=palmares,
        deporte="Fútbol",
        equipo="RV Femenino",
        crear_url="simancas_route_bp.crear_palmares_simancas",
        modificar_url="simancas_route_bp.modificar_palmares_simancas",
        eliminar_url="simancas_route_bp.eliminar_palmares_simancas",
    )
# Modificar Palmares del RV Femenino
@simancas_route_bp.route("/admin/modificar_palmares_simancas/<int:id>", methods=["POST"])
def modificar_palmares_simancas(id):
    titulo = Palmaress.query.get_or_404(id)
    titulo.temporada = request.form.get("temporada")
    titulo.competicion = request.form.get("competicion")
    titulo.imagen = request.form.get("imagen")
    db.session.commit()
    return redirect(url_for("simancas_route_bp.crear_palmares_simancas"))
# Eliminar Palmares del RV Promesas
@simancas_route_bp.route("/admin/eliminar_palmares_simancas/<int:id>", methods=["POST"])
def eliminar_palmares_simancas(id):
    titulo = Palmaress.query.get_or_404(id)
    db.session.delete(titulo)
    db.session.commit()
    return redirect(url_for("simancas_route_bp.crear_palmares_simancas"))

# COPA DEL REY RV Simancas
# Creación de las eliminatorias de copa
@simancas_route_bp.route('/crear_copa_simancas', methods=['GET', 'POST'])
def crear_copa_simancas():
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
            partido = CopaSimancas(
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
        return redirect(url_for('simancas_route_bp.ver_copa_simancas'))
    return render_template('admin/copa/copa_simancas.html')   
# Ver las eliminatorias en Admin
@simancas_route_bp.route('/copa_simancas/')
def ver_copa_simancas():
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {
        e: CopaSimancas.query.filter_by(eliminatoria=e).all()
        for e in eliminatorias
    }
    return render_template('admin/copa/copa_simancas.html', datos_eliminatorias=datos_eliminatorias)
# Modificar las eliminatorias
@simancas_route_bp.route('/modificar_copa_simancas_post', methods=['POST'])
def modificar_copa_simancas_post():
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        partido = CopaSimancas.query.get(partido_id)
        if partido:
            partido.eliminatoria = eliminatoria  # Opcional: si quieres actualizarla por partido
            partido.fecha = request.form.get(f'fecha{i}', '')
            partido.hora = request.form.get(f'hora{i}', '')
            partido.local = request.form.get(f'local{i}', '')
            partido.resultadoA = request.form.get(f'resultadoA{i}', '')
            partido.resultadoB = request.form.get(f'resultadoB{i}', '')
            partido.visitante = request.form.get(f'visitante{i}', '')
    db.session.commit()
    return redirect(url_for('simancas_route_bp.ver_copa_simancas'))
# Eliminar las eliminatorias en Admin
@simancas_route_bp.route('/eliminar_copa_simancas/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_simancas(eliminatoria):
    CopaSimancas.query.filter_by(eliminatoria=eliminatoria).delete()
    db.session.commit()
    return redirect(url_for('simancas_route_bp.ver_copa_simancas'))
# Ver las eliminatorias en la página principal Copa
@simancas_route_bp.route('/simancas_copa/')
def copas_simancas():
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_copa = {
        e: CopaSimancas.query.filter_by(eliminatoria=e).all()
        for e in eliminatorias
    }
    return render_template('copas/simancas_copa.html', datos_copa=datos_copa)

# PLAYOFF ASCENSO RV Simancas
# Crear formulario para los playoff
@simancas_route_bp.route('/crear_playoff_simancas', methods=['GET', 'POST'])
def crear_playoff_simancas():
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
        PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).delete()
        
        for i in range(num_partidos):
            partido = PlayoffSimancas(
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
        return redirect(url_for('simancas_route_bp.ver_playoff_simancas'))
    return render_template('admin/playoffs/playoff_simancas.html')
# Ver encuentros playoff en Admin
@simancas_route_bp.route('/playoff_simancas/')
def ver_playoff_simancas():
    eliminatorias = ['cuartos','semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffSimancas.orden).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_simancas.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@simancas_route_bp.route('/modificar_playoff_simancas/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_simancas(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffSimancas.query.get(int(partido_id))
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
        return redirect(url_for('simancas_route_bp.ver_playoff_simancas'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('simancas_route_bp.ver_playoff_simancas'))
# Eliminar los partidos de los playoff
@simancas_route_bp.route('/eliminar_playoff_simancas/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_simancas(eliminatoria):
    partidos = PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('simancas_route_bp.ver_playoff_simancas'))
# Mostrar los playoffs del RV Simancas
@simancas_route_bp.route('/playoffs_simancas/')
def playoffs_simancas():
    eliminatorias = ['cuartos','semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffSimancas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('playoff/simancas_playoff.html', datos_playoff=datos_playoff)