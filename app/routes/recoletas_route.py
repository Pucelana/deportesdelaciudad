from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.recoletas import JornadaRecoletas, RecoletasPartido, RecoletasClub, PlayoffRecoletas, CopaRecoletas, SupercopaIbericaRecoletas, EuropaRecoletas

recoletas_route_bp = Blueprint('recoletas_route_bp', __name__)

# LIGA RECOLETAS ATL.VALLADOLID
# Crear el calendario Recoletas Atl.Valladolid
@recoletas_route_bp.route('/crear_calendario_recoletas', methods=['GET', 'POST'])
def ingresar_resultado_recoletas():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaRecoletas(nombre=nombre_jornada)
        db.session.add(jornada)
        db.session.flush()  # Esto nos da el ID antes del commit        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')            
            # Crear el objeto partido y agregarlo a la sesión
            partido = RecoletasPartido(
                jornada_id=jornada.id,
                fecha=fecha,
                hora=hora,
                local=local,
                resultadoA=resultadoA,
                resultadoB=resultadoB,
                visitante=visitante,
                orden=i
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('recoletas_route_bp.calendarios_recoletas'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_recoletas.html')
# Ver calendario Atl.Valladolid en Admin
@recoletas_route_bp.route('/calendario_recoletas')
def calendarios_recoletas():
    jornadas = JornadaRecoletas.query.order_by(JornadaRecoletas.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(RecoletasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(RecoletasPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_recoletas.html', jornadas=jornadas)
# Modificar jornada
@recoletas_route_bp.route('/modificar_jornada_recoletas/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_recoletas(id):
    jornada = db.session.query(JornadaRecoletas).filter(JornadaRecoletas.id == id).first()
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
                partido = db.session.query(RecoletasPartido).filter(RecoletasPartido.id == partido_id).first()
                if partido:
                    partido.hora = hora
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante                 
                    orden = int(request.form.get(f'orden{i}', i))  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('recoletas_route_bp.calendarios_recoletas'))
    return render_template('admin/calendarios/calend_recoletas.html', jornada=jornada)
# Eliminar jornada
@recoletas_route_bp.route('/eliminar_jornada_recoletas/<int:id>', methods=['GET','POST'])
def eliminar_jornada_recoletas(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaRecoletas).filter(JornadaRecoletas.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(RecoletasPartido).filter(RecoletasPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('recoletas_route_bp.calendarios_recoletas'))    
# Obtener datos Atl.Valladolid
def obtener_datos_recoletas():
    # Obtener todas las jornadas Atl.Valladolid
    jornadas = JornadaRecoletas.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(RecoletasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(RecoletasPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Atl.Valladolid
@recoletas_route_bp.route('/equipos_balonmano/calendario_recoletas')
def calendario_recoletas():
    datos = obtener_datos_recoletas()
    nuevos_datos_recoletas = [dato for dato in datos if dato]
    equipo_recoletas = 'Atl.Valladolid'
    tabla_partidos_recoletas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Aula está jugando
            if equipo_local == equipo_recoletas or equipo_visitante == equipo_recoletas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_recoletas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_recoletas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_recoletas = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_recoletas:
                    tabla_partidos_recoletas[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_recoletas[equipo_contrario]:
                    tabla_partidos_recoletas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_recoletas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_recoletas[equipo_contrario]:
                    tabla_partidos_recoletas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_recoletas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_recoletas[equipo_contrario]['jornadas']:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_recoletas': rol_recoletas
                    }               
                # Asignamos los resultados según el rol del Atl.Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                    else:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                else:
                    if not tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                    else:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
    return render_template('equipos_balonmano/calendario_recoletas.html', tabla_partidos_recoletas=tabla_partidos_recoletas, nuevos_datos_recoletas=nuevos_datos_recoletas)
# Jornada 0 Atl.Valladolid
@recoletas_route_bp.route('/jornada0_recoletas', methods=['GET', 'POST'])
def jornada0_recoletas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = RecoletasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('recoletas_route_bp.jornada0_recoletas'))
    clubs = RecoletasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_recoletas.html', clubs=clubs)
# Eliminar clubs jornada 0
@recoletas_route_bp.route('/eliminar_club_recoletas/<int:club_id>', methods=['POST'])
def eliminar_club_recoletas(club_id):
    club = RecoletasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('recoletas_route_bp.jornada0_recoletas'))
# Crear la clasificación Atl.Valladolid
def generar_clasificacion_analisis_balonmano_recoletas(data):
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'puntos': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido.local 
            equipo_visitante = partido.visitante   
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB 
            if resultado_local is None or resultado_visitante is None:
                print(f"Partido sin resultados válidos: {partido}")
                continue            
            try:
                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1          
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local  
    clasificacion_ordenada = sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)
    return [{'equipo': equipo, 'datos': datos} for equipo, datos in clasificacion_ordenada]
# Ruta para mostrar la clasificación y análisis del Atl.Valladolid
@recoletas_route_bp.route('/equipos_balonmano/clasif_analisis_recoletas')
def clasif_analisis_recoletas():
    data = obtener_datos_recoletas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_recoletas = generar_clasificacion_analisis_balonmano_recoletas(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_recoletas = RecoletasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_recoletas:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_recoletas):
            equipo = {
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
            }
            clasificacion_analisis_recoletas.append(equipo)
    return render_template('equipos_balonmano/clasif_analisis_recoletas.html',
        clasificacion_analisis_recoletas=clasificacion_analisis_recoletas)