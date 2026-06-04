from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from itertools import groupby
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.vcv import JornadaVCV, VCVPartido, VCVClub, PlayoffVCV, CopaVCV, EuropaVCV, Clasificacion

vcv_route_bp = Blueprint('vcv_route_bp', __name__)
#EQUIPOS VOLEIBOL
#Todo el proceso de calendario y clasificación del Univ. Valladolid VCV
# Ingresar los resultados de los partidos de Univ. Valladolid VCV
@vcv_route_bp.route('/admin/crear_calendario_vcv', methods=['POST'])
def ingresar_resultado_vcv():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])
        jornada = JornadaVCV(nombre=nombre_jornada)       
        db.session.add(jornada)
        db.session.flush()       
        for i in range(num_partidos):
            fecha = request.form[f'fecha{i}']
            hora = request.form[f'hora{i}']
            local = request.form[f'local{i}']
            resultadoA = request.form[f'resultadoA{i}']
            resultadoB = request.form[f'resultadoB{i}']
            visitante = request.form[f'visitante{i}']          
            partido = VCVPartido(jornada_id=jornada.id, fecha=fecha, hora=hora, local=local, resultadoA=resultadoA, resultadoB=resultadoB, visitante=visitante)
            db.session.add(partido)
        db.session.commit()
     # Redirigir al calendario después de crear la jornada
        return redirect(url_for('vcv_route_bp.calendarios_vcv'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_vcv.html')
# Partidos Univ. Valladolid VCV
@vcv_route_bp.route('/admin/calendario_vcv')
def calendarios_vcv():
    jornadas = JornadaVCV.query.order_by(JornadaVCV.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(VCVPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(VCVPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_vcv.html', jornadas=jornadas)
# Modificar los partidos de cada jornada
@vcv_route_bp.route('/modificar_jornada_vcv/<string:id>', methods=['POST'])
def modificar_jornada_vcv(id):
    jornada = db.session.query(JornadaVCV).filter(JornadaVCV.id == id).first()
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
                bonusA = request.form[f'bonusA{i}']
                resultadoA = request.form[f'resultadoA{i}']
                resultadoB = request.form[f'resultadoB{i}']
                bonusB = request.form[f'bonusB{i}']
                visitante = request.form[f'visitante{i}']                
                # Obtener el partido correspondiente por ID
                partido = db.session.query(VCVPartido).filter(VCVPartido.id == partido_id).first()
                if partido:
                    partido.fecha = fecha
                    partido.hora = hora
                    partido.local = local
                    partido.bonusA = bonusA
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.bonusB = bonusB
                    partido.visitante = visitante                 
                    orden = int(request.form.get(f'orden{i}', i))  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('vcv_route_bp.calendarios_vcv'))
    return render_template('admin/calendarios/calend_vcv.html', jornada=jornada)
# Ruta para borrar jornadas
@vcv_route_bp.route('/eliminar_jorn_vcv/<string:id>', methods=['POST'])
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
    return redirect(url_for('vcv_route_bp.calendarios_vcv'))
def obtener_datos_vcv():
    # Obtener todas las jornadas VCV
    jornadas = JornadaVCV.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(VCVPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(VCVPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Ruta y creación del calendario individual del Univ. Valladolid VCV
@vcv_route_bp.route('/equipos_voley/calendario_vcv')
def calendario_vcv():
    datos = obtener_datos_vcv()
    nuevos_datos_vcv = [dato for dato in datos if dato]
    equipo_vcv = 'Universidad VCV'
    tabla_partidos_vcv = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
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
                    rol_vcv = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vcv = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vcv:
                    tabla_partidos_vcv[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_vcv[equipo_contrario]:
                    tabla_partidos_vcv[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vcv[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_vcv[equipo_contrario]:
                    tabla_partidos_vcv[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vcv[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_vcv[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_vcv[equipo_contrario]['jornadas']:
                    tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_vcv': rol_vcv
                    }               
                # Asignamos los resultados según el rol del Vcv
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
                    else:
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
                else:
                    if not tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
                    else:
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vcv[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vcv'] = rol_vcv
    return render_template('equipos_voley/calendario_vcv.html', tabla_partidos_vcv=tabla_partidos_vcv, nuevos_datos_vcv=nuevos_datos_vcv)
# Crear la clasificación de Univ. Valladolid VCV
def generar_clasificacion_analisis_voley_vcv(data):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados3': 0, 'ganados2': 0, 'perdidos1': 0, 'perdidos0': 0, 'favor': 0, 'contra': 0, 'diferencia_sets': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido['local']
            equipo_visitante = partido['visitante']
            try:
                resultado_local = int(partido['resultadoA'])
                resultado_visitante = int(partido['resultadoB'])
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1           
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local           
            if resultado_local > resultado_visitante:  # Equipo local gana
                if resultado_local == 3 and resultado_visitante <= 1:  # 3-0 ó 3-1
                    clasificacion[equipo_local]['puntos'] += 3
                    clasificacion[equipo_local]['ganados3'] += 1
                    clasificacion[equipo_visitante]['puntos'] += 0
                    clasificacion[equipo_visitante]['perdidos0'] += 1
                else:
                    clasificacion[equipo_local]['puntos'] += 2  # 3-2
                    clasificacion[equipo_local]['ganados2'] += 1
                    clasificacion[equipo_visitante]['puntos'] += 1
                    clasificacion[equipo_visitante]['perdidos1'] += 1
            elif resultado_local < resultado_visitante:  # Equipo visitante gana
                if resultado_visitante == 3 and resultado_local <= 1:  # 3-0 ó 3-1
                    clasificacion[equipo_visitante]['puntos'] += 3
                    clasificacion[equipo_visitante]['ganados3'] += 1
                    clasificacion[equipo_local]['puntos'] += 0
                    clasificacion[equipo_local]['perdidos0'] += 1
                else:
                    clasificacion[equipo_visitante]['puntos'] += 2  # 3-2
                    clasificacion[equipo_visitante]['ganados2'] += 1
                    clasificacion[equipo_local]['puntos'] += 1
                    clasificacion[equipo_local]['perdidos1'] += 1
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['favor'] - x[1]['contra']), reverse=True)]
    return clasificacion_ordenada
# Ruta para mostrar la clasificación y analisis del Univ. Valladolid VCV
@vcv_route_bp.route('/equipos_voley/clasif_analisis_vcv/')
def clasif_analisis_vcv():
    data = obtener_datos_vcv()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_vcv = generar_clasificacion_analisis_voley_vcv(data)
    clubs_vcv = VCVClub.query.all()    
    # Inicializa las estadísticas de los equipos de la jornada 0 si no están ya en la clasificación
    for club in clubs_vcv:
        if not any(equipo['equipo'] == club['nombre'] for equipo in clasificacion_analisis_vcv):
            equipo = {
                'equipo': club['nombre'],
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados3': 0,
                    'ganados2': 0,
                    'perdidos1': 0,
                    'perdidos0': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_sets': 0,
                }
            }
            clasificacion_analisis_vcv.append(equipo)
    return render_template('equipos_voley/clasif_analisis_vcv.html', clasificacion_analisis_vcv=clasificacion_analisis_vcv)
@vcv_route_bp.route('/admin/jornada0_vcv', methods=['GET', 'POST'])
def jornada0_vcv():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = VCVClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('vcv_route_bp.jornada0_vcv'))
    clubs = VCVClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_vcv.html', clubs=clubs)
@vcv_route_bp.route('/admin/eliminar_club_vcv/<string:club_id>', methods=['POST'])
def eliminar_club_vcv(club_id):
    club = VCVClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('vcv_route_bp.jornada0_vcv'))
#Fin proceso Univ. Valladolid VCV